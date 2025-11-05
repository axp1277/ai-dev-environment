"""Core functionality for Polygon market data fetcher."""
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from loguru import logger


def load_api_key() -> str:
    """Load Polygon API key from environment."""
    logger.debug("Loading Polygon API key from environment")
    
    # Look for .env files in multiple locations
    current_dir = Path.cwd()
    project_root = None
    
    # Find project root by looking for pyproject.toml
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "pyproject.toml").exists():
            project_root = parent
            logger.debug(f"Found project root: {project_root}")
            break
    
    # Try loading from project root first, then local directory
    if project_root:
        env_file = project_root / ".env"
        if env_file.exists():
            logger.debug(f"Loading .env from project root: {env_file}")
            load_dotenv(env_file)
    
    # Also try local .env file in polygon directory
    polygon_dir = Path(__file__).parent
    local_env = polygon_dir / ".env"
    if local_env.exists():
        logger.debug(f"Loading .env from polygon directory: {local_env}")
        load_dotenv(local_env)
    
    # Finally, load from current working directory
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        logger.debug(f"Loading .env from current directory: {cwd_env}")
        load_dotenv()
    
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        logger.error("POLYGON_API_KEY not found in any .env file")
        raise ValueError("POLYGON_API_KEY not found in environment. Check .env file in project root or polygon directory.")
    
    logger.debug("Successfully loaded Polygon API key")
    return api_key


def fetch_ohlcv(
    ticker: str, 
    multiplier: int, 
    timespan: str, 
    from_date: str, 
    to_date: str
) -> List[Dict]:
    """Fetch OHLCV data from Polygon API."""
    logger.info(f"Fetching OHLCV data for {ticker} ({multiplier} {timespan}, {from_date} to {to_date})")
    
    api_key = load_api_key()
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
    
    params = {
        "apiKey": api_key,
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000
    }
    
    logger.debug(f"Making API request to: {url}")
    logger.debug(f"Request parameters: {dict(params, apiKey='***')}")  # Hide API key in logs
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logger.error(f"API request failed with status {response.status_code}: {response.text}")
        raise Exception(f"API error: {response.status_code} - {response.text}")
    
    data = response.json()
    status = data.get("status")
    result_count = len(data.get("results", []))
    
    logger.info(f"API response status: {status}, received {result_count} results")
    
    if status not in ["OK", "DELAYED"]:
        logger.error(f"API returned unexpected status: {status}")
        raise Exception(f"API returned status: {status}")
    
    if status == "DELAYED":
        logger.warning("Received DELAYED status - data may be 15+ minutes behind")
    
    return data.get("results", [])


def get_db_connection() -> sqlite3.Connection:
    """Get SQLite database connection."""
    # Find project root by looking for pyproject.toml
    current_dir = Path.cwd()
    project_root = None
    
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "pyproject.toml").exists():
            project_root = parent
            break
    
    if not project_root:
        # Fallback to current directory if project root not found
        db_path = Path("market_data.db")
        logger.warning("Could not find project root, using current directory for database")
    else:
        # Create data directory if it doesn't exist
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        db_path = data_dir / "market_data.db"
        logger.debug(f"Using database path: {db_path}")
    
    return sqlite3.connect(str(db_path))


def create_table(ticker: str, timeframe: str) -> None:
    """Create table for ticker/timeframe if it doesn't exist."""
    table_name = f"{ticker}_{timeframe}"
    logger.debug(f"Creating/verifying table: {table_name}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table with exact schema from backtesting.db
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            UNIQUE(timestamp)
        )
    """)
    
    # Create index on timestamp
    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_{table_name}_timestamp 
        ON {table_name}(timestamp)
    """)
    
    conn.commit()
    conn.close()
    logger.debug(f"Table {table_name} created/verified successfully")


def insert_bars(ticker: str, timeframe: str, bars: List[Dict]) -> int:
    """Insert bars into database, returns count of inserted rows."""
    if not bars:
        logger.debug("No bars to insert")
        return 0
    
    table_name = f"{ticker}_{timeframe}"
    logger.debug(f"Inserting {len(bars)} bars into {table_name}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted = 0
    duplicates = 0
    
    for bar in bars:
        # Convert Unix milliseconds to datetime string
        timestamp = datetime.fromtimestamp(bar["t"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, bar["o"], bar["h"], bar["l"], bar["c"], bar["v"]))
            inserted += 1
        except sqlite3.IntegrityError:
            # Duplicate timestamp, skip
            duplicates += 1
            logger.debug(f"Skipped duplicate timestamp: {timestamp}")
    
    conn.commit()
    conn.close()
    
    if duplicates > 0:
        logger.info(f"Inserted {inserted} new bars, skipped {duplicates} duplicates")
    else:
        logger.info(f"Inserted {inserted} bars successfully")
    
    return inserted


def calculate_date_range(bars: int, timeframe: str) -> tuple[str, str]:
    """Calculate from/to dates based on bars lookback."""
    now = datetime.now()
    
    # Map timeframe to minutes
    timeframe_minutes = {
        "1minute": 1,
        "5minute": 5,
        "15minute": 15,
        "60minute": 60
    }
    
    if timeframe not in timeframe_minutes:
        raise ValueError(f"Invalid timeframe: {timeframe}")
    
    # Calculate start date (rough estimate, accounting for weekends)
    minutes = timeframe_minutes[timeframe]
    trading_minutes_per_day = 390  # 6.5 hours
    days_needed = (bars * minutes / trading_minutes_per_day) * 2.0  # 2x for weekends and holidays
    
    # Ensure we go back at least 5 trading days (7 calendar days) for small bar counts
    days_needed = max(days_needed, 7)
    
    start_date = now - timedelta(days=int(days_needed))
    
    # Format dates as YYYY-MM-DD
    return start_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


def map_timeframe_for_api(timeframe: str) -> tuple[int, str]:
    """Map CLI timeframe to API multiplier and timespan."""
    mapping = {
        "1minute": (1, "minute"),
        "5minute": (5, "minute"),
        "15minute": (15, "minute"),
        "60minute": (1, "hour")
    }
    
    if timeframe not in mapping:
        raise ValueError(f"Invalid timeframe: {timeframe}")
    
    return mapping[timeframe]


def map_timeframe_for_table(timeframe: str) -> str:
    """Map CLI timeframe to table name format."""
    mapping = {
        "1minute": "1Minute",
        "5minute": "5Minute",
        "15minute": "15Minute",
        "60minute": "60Minute"
    }
    
    return mapping.get(timeframe, timeframe)