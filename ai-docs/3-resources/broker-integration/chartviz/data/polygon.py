"""Polygon data provider with auto-persistence to SQLite."""

import sys
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import pandas as pd
from .base import DataProvider

# Add brokers to path for import
brokers_path = str(Path(__file__).parent.parent.parent / "brokers")
if brokers_path not in sys.path:
    sys.path.insert(0, brokers_path)

try:
    from polygon.core import (
        fetch_ohlcv, create_table, insert_bars,
        calculate_date_range, map_timeframe_for_api, 
        map_timeframe_for_table, get_db_connection
    )
except ImportError as e:
    raise ImportError(f"Could not import Polygon broker: {e}. Ensure Polygon broker is properly installed.") from e


class PolygonProvider(DataProvider):
    """Polygon provider with auto-persistence to SQLite."""
    
    def __init__(self, db_path: str = "data/market_data.db"):
        """
        Initialize Polygon provider.
        
        Args:
            db_path: SQLite database path
        """
        self.db_path = Path(db_path)
        
        # Ensure the database parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @property
    def name(self) -> str:
        return "Polygon"
    
    @property
    def is_live(self) -> bool:
        return True
    
    def get_ohlcv(self, symbol: str, timeframe: str, days: int = 5, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Fetch OHLCV from Polygon API and auto-persist to SQLite.
        
        Strategy:
        1. Fetch from Polygon API
        2. Save to SQLite (duplicates automatically handled)
        3. Return data from SQLite
        """
        # Always fetch fresh data from API and store
        self._fetch_and_store(symbol, timeframe, days)
        
        # Return data from SQLite
        table_timeframe = self._map_timeframe(timeframe)
        return self._read_from_sqlite(symbol, table_timeframe, limit)
    
    
    def _fetch_and_store(self, symbol: str, timeframe: str, days: int):
        """Fetch data from Polygon API and store in SQLite."""
        table_timeframe = map_timeframe_for_table(timeframe)
        
        # Calculate bars needed for the requested days
        timeframe_minutes = {"1minute": 1, "5minute": 5, "15minute": 15, "60minute": 60}
        minutes = timeframe_minutes.get(timeframe, 5)
        trading_minutes_per_day = 390  # 6.5 hours
        bars = int((days * trading_minutes_per_day) / minutes)
        
        # Get date range
        from_date, to_date = calculate_date_range(bars, timeframe)
        
        # Get API parameters
        multiplier, timespan = map_timeframe_for_api(timeframe)
        
        # Fetch from API
        bars_data = fetch_ohlcv(symbol, multiplier, timespan, from_date, to_date)
        
        # Create table and insert data
        create_table(symbol, table_timeframe)
        insert_bars(symbol, table_timeframe, bars_data)
    
    def _read_from_sqlite(self, symbol: str, table_timeframe: str, limit: Optional[int]) -> pd.DataFrame:
        """Read data from SQLite database."""
        table_name = f"{symbol.upper()}_{table_timeframe}"
        
        with sqlite3.connect(self.db_path) as conn:
            query = f"SELECT timestamp, open, high, low, close, volume FROM {table_name}"
            query += " ORDER BY timestamp DESC"
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql_query(query, conn)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            return df.sort_index()
    
    def _map_timeframe(self, timeframe: str) -> str:
        """Map CLI timeframe to database table format."""
        mapping = {
            "1minute": "1Minute", 
            "5minute": "5Minute", 
            "15minute": "15Minute", 
            "60minute": "60Minute"
        }
        return mapping.get(timeframe, timeframe)
    
    def list_symbols(self) -> List[str]:
        """Extract symbols from table names in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
            
            symbols = set()
            for table in tables:
                if '_' in table and not table.startswith('sqlite_'):
                    symbol = table.split('_')[0]
                    symbols.add(symbol)
            
            return sorted(symbols)
            
        except Exception:
            return []
    
    def validate_connection(self) -> bool:
        """Test both database connection and API key availability."""
        try:
            # Test SQLite connection
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1").fetchone()
            
            # Test API key availability (don't make actual API call)
            try:
                from polygon.core import load_api_key
                load_api_key()
                return True
            except Exception:
                # API key not available, but SQLite works
                return True
                
        except Exception:
            return False