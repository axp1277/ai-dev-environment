"""SQLite data provider for market_data.db - Default provider."""

import sqlite3
from pathlib import Path
from typing import List, Optional
import pandas as pd
from .base import DataProvider


class SQLiteProvider(DataProvider):
    """SQLite provider for local database - Default provider."""
    
    def __init__(self, db_path: str = "data/market_data.db"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}")
    
    @property
    def name(self) -> str:
        return "SQLite"
    
    @property
    def is_live(self) -> bool:
        return False
    
    def get_ohlcv(self, symbol: str, timeframe: str, days: int = 5, limit: Optional[int] = None) -> pd.DataFrame:
        """Fetch OHLCV from SQLite database."""
        table_name = f"{symbol.upper()}_{self._map_timeframe(timeframe)}"
        
        with sqlite3.connect(self.db_path) as conn:
            # Check table exists
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                raise ValueError(f"No data for {symbol} {timeframe}")
            
            # Build query
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
            "1minute": "1Minute", "5minute": "5Minute", 
            "15minute": "15Minute", "60minute": "60Minute"
        }
        return mapping.get(timeframe, timeframe)
    
    def list_symbols(self) -> List[str]:
        """Extract symbols from table names."""
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
    
    def validate_connection(self) -> bool:
        """Test database connection."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1").fetchone()
            return True
        except:
            return False