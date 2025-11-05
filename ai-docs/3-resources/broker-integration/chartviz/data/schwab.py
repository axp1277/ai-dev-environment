"""Schwab data provider for ChartViz using direct Schwab client integration."""

from datetime import datetime
from typing import List, Optional
import pandas as pd
from .base import DataProvider

try:
    from src.brokers.schwab.client import SchwabClient
    from src.utils.schwab_token_manager import with_token_refresh
except ImportError as e:
    raise ImportError(f"Could not import Schwab client: {e}. Ensure Schwab broker is properly configured.") from e


class SchwabProvider(DataProvider):
    """Schwab data provider for ChartViz using direct Schwab client integration."""
    
    def __init__(self):
        """Initialize Schwab provider."""
        self.client = SchwabClient()
        
    @property
    def name(self) -> str:
        """Provider name for display."""
        return "Schwab"
    
    @property  
    def is_live(self) -> bool:
        """Whether provider returns live data."""
        return True
        
    @with_token_refresh
    def get_ohlcv(self, symbol: str, timeframe: str = "5minute", days: int = 5, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Get OHLCV data using direct Schwab client (following existing charting module pattern).
        
        Args:
            symbol: Trading symbol (e.g., '/ESU25', 'SPY')
            timeframe: Data timeframe (5minute, 15minute, 1day)
            days: Number of days of historical data
            limit: Maximum number of bars to return
            
        Returns:
            DataFrame with OHLCV data indexed by timestamp
        """
        try:
            # Use same logic as existing charting module
            is_futures = symbol.startswith('/')
            is_minute_data = "minute" in timeframe
            
            # Choose correct API method
            method_name = "get_futures_price_history" if is_futures else "get_price_history"
            
            # Parse timeframe
            if is_minute_data:
                frequency_type = "minute"
                frequency = int(timeframe.replace("minute", ""))
            else:
                frequency_type = "daily"
                frequency = 1
            
            # Fetch data using appropriate method
            history = getattr(self.client, method_name)(
                symbol=symbol,
                period_type="day",
                period=min(days, 10),  # Max 10 days for intraday data
                need_previous_close=True,
                need_extended_hours_data=is_futures,
                frequency_type=frequency_type,
                frequency=frequency
            )
            
            if not history.candles:
                return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
            
            # Convert to DataFrame (same format as expected by ChartViz)
            data = []
            for candle in history.candles:
                timestamp = datetime.fromtimestamp(candle.datetime / 1000)
                data.append({
                    'open': candle.open,
                    'high': candle.high,
                    'low': candle.low,
                    'close': candle.close,
                    'volume': candle.volume
                })
            
            df = pd.DataFrame(data)
            df.index = [datetime.fromtimestamp(c.datetime / 1000) for c in history.candles]
            df.index.name = 'timestamp'
            
            # Apply limit if specified
            if limit and len(df) > limit:
                df = df.tail(limit)
                
            return df.sort_index()
            
        except Exception as e:
            print(f"Error fetching data from Schwab: {e}")
            return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        
    def list_symbols(self) -> List[str]:
        """Get available symbols - common futures with current contracts and stocks."""
        return [
            # Major Futures (with current contract months - update as needed)
            "/ESZ24",   # E-mini S&P 500 December 2024
            "/ESH25",   # E-mini S&P 500 March 2025
            "/ESM25",   # E-mini S&P 500 June 2025
            "/ESU25",   # E-mini S&P 500 September 2025
            "/NQZ24",   # E-mini Nasdaq December 2024
            "/NQH25",   # E-mini Nasdaq March 2025
            "/RTYZ24",  # E-mini Russell 2000 December 2024
            "/RTYM25",  # E-mini Russell 2000 June 2025
            "/CLX24",   # Crude Oil November 2024
            "/CLZ24",   # Crude Oil December 2024
            "/GCZ24",   # Gold December 2024
            "/GCG25",   # Gold February 2025
            
            # Major Stocks
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
            "NVDA", "META", "NFLX", "SPY", "QQQ"
        ]
        
    def validate_connection(self) -> bool:
        """Validate connection using existing Schwab client."""
        try:
            return self.client.is_authenticated() if hasattr(self.client, 'is_authenticated') else True
        except Exception:
            return False