"""
Schwab Broker Module

Unified Schwab API integration with CLI interface, data provider adapter,
and comprehensive API client functionality.

Usage:
    # CLI Interface
    uv run src/brokers/schwab/cli.py --help
    
    # API Client
    from src.brokers.schwab import SchwabClient
    client = SchwabClient()
    
    # Data Provider
    from src.brokers.schwab import SchwabDataProvider
    provider = SchwabDataProvider()
"""

from .client import SchwabClient
from .adapter import SchwabDataProvider
from .auth import SchwabAuth
from .models import (
    QuoteResponse, PriceHistoryResponse, OptionChainResponse, 
    Position, AccountInfo, Candle, QuoteData
)

__all__ = [
    'SchwabClient',
    'SchwabDataProvider', 
    'SchwabAuth',
    'QuoteResponse',
    'PriceHistoryResponse',
    'OptionChainResponse',
    'Position',
    'AccountInfo'
]