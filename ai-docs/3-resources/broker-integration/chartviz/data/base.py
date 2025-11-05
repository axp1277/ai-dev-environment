"""Abstract data provider interface for ChartViz."""

from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd


class DataProvider(ABC):
    """Minimal interface for all data providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name for display."""
        pass
    
    @property  
    @abstractmethod
    def is_live(self) -> bool:
        """Whether provider returns live data."""
        pass
    
    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, days: int = 5, limit: Optional[int] = None) -> pd.DataFrame:
        """Get OHLCV data as DataFrame with timestamp index."""
        pass
    
    @abstractmethod  
    def list_symbols(self) -> List[str]:
        """Get available symbols."""
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """Test connection to data source."""
        pass