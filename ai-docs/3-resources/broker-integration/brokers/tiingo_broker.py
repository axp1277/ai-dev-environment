"""Tiingo Broker Implementation

This module implements the Tiingo API broker for fetching OHLC data for crypto, forex, and stocks.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, Union
from pathlib import Path
import pandas as pd
import aiohttp
from dotenv import load_dotenv

from src.brokers.broker import Broker, Order, Position


# Load environment variables from .env file
dotenv_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / '.env'
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)


class TiingoBroker(Broker):
    """Implementation of Broker interface for Tiingo API
    
    This broker allows fetching historical OHLC data from Tiingo's API services.
    It supports crypto, forex, and equity market data.
    """
    
    BASE_URL = "https://api.tiingo.com"
    
    # Supported timeframes mapped to Tiingo's resampleFreq parameter
    TIMEFRAME_MAP = {
        "1m": "1min",
        "5m": "5min", 
        "15m": "15min",
        "30m": "30min",
        "1h": "1hour",
        "2h": "2hour",
        "4h": "4hour",
        "6h": "6hour",
        "12h": "12hour",
        "1d": "1day",
        "1w": "1week"
    }
    
    # Asset type constants
    CRYPTO = "crypto"
    FOREX = "forex"
    STOCK = "stock"
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Tiingo broker with configuration

        Args:
            config: Dictionary containing:
                - api_key: Tiingo API key (optional if TIINGO_API_KEY env variable exists)
                - name: Optional name for this broker instance
                - timeout: Optional API timeout in seconds
        """
        super().__init__(config)
        self.api_key = config.get("api_key")

        # Check for API key in environment if not in config
        if not self.api_key:
            self.api_key = os.environ.get("TIINGO_API_KEY")
            if not self.api_key:
                raise ValueError("Tiingo API key is required in config or as TIINGO_API_KEY environment variable")

        self.timeout = config.get("timeout", 30)  # Default 30 seconds timeout
        self.session = None
    
    async def connect(self) -> bool:
        """Connect to the Tiingo API by initializing an HTTP session

        Returns:
            True if connected successfully
        """
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Token {self.api_key}"
                }
            )

        # Test the connection with a simple API call
        try:
            # Extract to a separate method for easier testing
            return await self._test_connection()
        except Exception as e:
            logger.error(f"Error connecting to Tiingo API: {str(e)}")
            return False

    async def _test_connection(self) -> bool:
        """Test the API connection

        Returns:
            True if connected successfully
        """
        async with self.session.get(f"{self.BASE_URL}/api/test") as response:
            if response.status == 200:
                self.is_connected = True
                logger.info("Successfully connected to Tiingo API")
                return True
            else:
                logger.error(f"Failed to connect to Tiingo API: {response.status}")
                return False
    
    async def disconnect(self) -> bool:
        """Disconnect from the Tiingo API
        
        Returns:
            True if disconnected successfully
        """
        if self.session:
            await self.session.close()
            self.session = None
            self.is_connected = False
            return True
        return False
    
    async def get_account_info(self) -> Dict[str, Any]:
        """Get account information (not applicable for Tiingo data-only broker)
        
        Returns:
            Empty dictionary as Tiingo is a data-only broker
        """
        return {"message": "Tiingo is a data-only broker, no account information available"}
    
    async def get_positions(self) -> Dict[str, Position]:
        """Get current positions (not applicable for Tiingo data-only broker)
        
        Returns:
            Empty dictionary as Tiingo is a data-only broker
        """
        return {}
    
    async def place_order(self, order: Order) -> Tuple[bool, Optional[str]]:
        """Place an order (not applicable for Tiingo data-only broker)
        
        Args:
            order: Order to place
            
        Returns:
            (False, error message) as Tiingo is a data-only broker
        """
        return False, "Tiingo is a data-only broker, trading not supported"
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order (not applicable for Tiingo data-only broker)
        
        Args:
            order_id: ID of order to cancel
            
        Returns:
            False as Tiingo is a data-only broker
        """
        return False
    
    async def get_order_status(self, order_id: str) -> Optional[Order]:
        """Get status of an order (not applicable for Tiingo data-only broker)
        
        Args:
            order_id: ID of order to check
            
        Returns:
            None as Tiingo is a data-only broker
        """
        return None
    
    async def get_market_data(self, symbol: str, timeframe: str, 
                          bars: int = 100) -> Optional[Dict[str, Any]]:
        """Get market data for a symbol (wrapper for compatibility with base class)
        
        Args:
            symbol: The market symbol
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            bars: Number of bars to retrieve
            
        Returns:
            Dict with market data or None if not available
        """
        # Calculate start date based on bars and timeframe
        end_date = datetime.now()
        
        # Determine timeframe in minutes
        if timeframe not in self.TIMEFRAME_MAP:
            logger.error(f"Unsupported timeframe: {timeframe}")
            return None
        
        # Get data
        df = await self.get_ohlc_data(symbol, timeframe, bars=bars)
        if df is None or df.empty:
            return None
        
        # Convert to dictionary format
        result = {
            "symbol": symbol,
            "timeframe": timeframe,
            "data": df.to_dict(orient="records")
        }
        
        return result
    
    async def flatten_position(self, symbol: str) -> bool:
        """Close all positions for a symbol (not applicable for Tiingo data-only broker)
        
        Args:
            symbol: Symbol to flatten position for
            
        Returns:
            False as Tiingo is a data-only broker
        """
        return False
    
    async def flatten_all_positions(self) -> bool:
        """Close all positions (not applicable for Tiingo data-only broker)
        
        Returns:
            False as Tiingo is a data-only broker
        """
        return False
    
    async def get_ohlc_data(self, symbol: str, timeframe: str, 
                          start_date: Optional[Union[str, datetime]] = None,
                          end_date: Optional[Union[str, datetime]] = None,
                          asset_type: str = CRYPTO,
                          bars: Optional[int] = None) -> Optional[pd.DataFrame]:
        """Get OHLC data from Tiingo
        
        Args:
            symbol: The market symbol (e.g., "btcusd" for crypto)
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            start_date: Start date for data retrieval (optional)
            end_date: End date for data retrieval (optional)
            asset_type: Type of asset - "crypto", "forex", or "stock"
            bars: Number of bars to retrieve (optional, used if start_date not provided)
            
        Returns:
            Pandas DataFrame with OHLC data or None if failed
        """
        if not self.is_connected:
            logger.warning("Not connected to Tiingo API, attempting to connect")
            success = await self.connect()
            if not success:
                logger.error("Failed to connect to Tiingo API")
                return None
        
        # Verify timeframe is supported
        if timeframe not in self.TIMEFRAME_MAP:
            logger.error(f"Unsupported timeframe: {timeframe}")
            return None
        
        tiingo_timeframe = self.TIMEFRAME_MAP[timeframe]
        
        # Calculate start date if not provided but bars is
        if start_date is None and bars is not None:
            end_date = end_date or datetime.now()
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
            # Approximate start date based on bars and timeframe
            # This is an estimate as it doesn't account for weekends/holidays
            if timeframe.endswith('m'):
                minutes = int(timeframe[:-1])
                start_date = end_date - timedelta(minutes=minutes * bars)
            elif timeframe.endswith('h'):
                hours = int(timeframe[:-1])
                start_date = end_date - timedelta(hours=hours * bars)
            elif timeframe.endswith('d'):
                days = int(timeframe[:-1])
                start_date = end_date - timedelta(days=days * bars)
            elif timeframe.endswith('w'):
                weeks = int(timeframe[:-1])
                start_date = end_date - timedelta(weeks=weeks * bars)
        
        # Format dates to ISO format
        if start_date and isinstance(start_date, datetime):
            start_date = start_date.strftime('%Y-%m-%d')
        if end_date and isinstance(end_date, datetime):
            end_date = end_date.strftime('%Y-%m-%d')
        
        try:
            # Construct the correct URL based on asset type
            if asset_type == self.CRYPTO:
                endpoint = f"{self.BASE_URL}/tiingo/crypto/prices"
                params = {
                    "tickers": symbol,
                    "resampleFreq": tiingo_timeframe
                }
                if start_date:
                    params["startDate"] = start_date
                if end_date:
                    params["endDate"] = end_date
                
                async with self.session.get(endpoint, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Error fetching Tiingo crypto data: {response.status} - {error_text}")
                        return None
                    
                    data = await response.json()
                    
                    if not data or len(data) == 0:
                        logger.warning(f"No data returned for {symbol}")
                        return None
                    
                    # For crypto, data comes in a different format
                    price_data = data[0]["priceData"]
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(price_data)
                    df.rename(columns={
                        "date": "datetime",
                        "open": "open",
                        "high": "high",
                        "low": "low",
                        "close": "close",
                        "volume": "volume"
                    }, inplace=True)
                    
                    # Convert date strings to datetime objects
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    
                    return df[["datetime", "open", "high", "low", "close", "volume"]]
                
            elif asset_type == self.FOREX:
                endpoint = f"{self.BASE_URL}/tiingo/fx/{symbol}/prices"
                params = {
                    "resampleFreq": tiingo_timeframe
                }
                if start_date:
                    params["startDate"] = start_date
                if end_date:
                    params["endDate"] = end_date
                
                async with self.session.get(endpoint, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Error fetching Tiingo forex data: {response.status} - {error_text}")
                        return None
                    
                    data = await response.json()
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(data)
                    df.rename(columns={
                        "date": "datetime",
                        "open": "open",
                        "high": "high",
                        "low": "low",
                        "close": "close"
                    }, inplace=True)
                    
                    # Add volume column (not available for forex)
                    df["volume"] = 0
                    
                    # Convert date strings to datetime objects
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    
                    return df[["datetime", "open", "high", "low", "close", "volume"]]
                
            elif asset_type == self.STOCK:
                # Use IEX endpoint for intraday data, daily endpoint for daily data
                if tiingo_timeframe == "1day":
                    endpoint = f"{self.BASE_URL}/tiingo/daily/{symbol}/prices"
                    params = {}
                    if start_date:
                        params["startDate"] = start_date
                    if end_date:
                        params["endDate"] = end_date
                else:
                    # Use IEX endpoint for intraday data
                    endpoint = f"{self.BASE_URL}/iex/{symbol}/prices"
                    params = {
                        "columns": "open,high,low,close,volume",  # Explicitly request volume
                        "resampleFreq": tiingo_timeframe
                    }
                    if start_date:
                        params["startDate"] = start_date
                    if end_date:
                        params["endDate"] = end_date
                
                async with self.session.get(endpoint, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Error fetching Tiingo stock data: {response.status} - {error_text}")
                        return None
                    
                    data = await response.json()
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(data)
                    df.rename(columns={
                        "date": "datetime",
                        "open": "open",
                        "high": "high",
                        "low": "low",
                        "close": "close",
                        "volume": "volume"
                    }, inplace=True)
                    
                    # Convert date strings to datetime objects and handle timezone
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    
                    # If this is IEX intraday data, convert from UTC to ET
                    if tiingo_timeframe != "1day":
                        # IEX data comes in UTC, convert to Eastern Time
                        if df["datetime"].dt.tz is None:
                            df["datetime"] = df["datetime"].dt.tz_localize('UTC').dt.tz_convert('America/New_York')
                        else:
                            df["datetime"] = df["datetime"].dt.tz_convert('America/New_York')
                    
                    return df[["datetime", "open", "high", "low", "close", "volume"]]
            
            else:
                logger.error(f"Unsupported asset type: {asset_type}")
                return None
            
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error when fetching data: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    async def get_crypto_data(self, symbol: str, timeframe: str, 
                           start_date: Optional[Union[str, datetime]] = None,
                           end_date: Optional[Union[str, datetime]] = None,
                           bars: Optional[int] = None) -> Optional[pd.DataFrame]:
        """Convenience method to get crypto OHLC data
        
        Args:
            symbol: The crypto pair (e.g., "btcusd")
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            start_date: Start date for data retrieval (optional)
            end_date: End date for data retrieval (optional)
            bars: Number of bars to retrieve (optional, used if start_date not provided)
            
        Returns:
            Pandas DataFrame with OHLC data or None if failed
        """
        return await self.get_ohlc_data(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            asset_type=self.CRYPTO,
            bars=bars
        )
    
    async def get_forex_data(self, symbol: str, timeframe: str, 
                          start_date: Optional[Union[str, datetime]] = None,
                          end_date: Optional[Union[str, datetime]] = None,
                          bars: Optional[int] = None) -> Optional[pd.DataFrame]:
        """Convenience method to get forex OHLC data
        
        Args:
            symbol: The forex pair (e.g., "eurusd")
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            start_date: Start date for data retrieval (optional)
            end_date: End date for data retrieval (optional)
            bars: Number of bars to retrieve (optional, used if start_date not provided)
            
        Returns:
            Pandas DataFrame with OHLC data or None if failed
        """
        return await self.get_ohlc_data(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            asset_type=self.FOREX,
            bars=bars
        )
    
    async def get_stock_data(self, symbol: str, timeframe: str, 
                          start_date: Optional[Union[str, datetime]] = None,
                          end_date: Optional[Union[str, datetime]] = None,
                          bars: Optional[int] = None) -> Optional[pd.DataFrame]:
        """Convenience method to get stock OHLC data
        
        Args:
            symbol: The stock ticker (e.g., "AAPL")
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            start_date: Start date for data retrieval (optional)
            end_date: End date for data retrieval (optional)
            bars: Number of bars to retrieve (optional, used if start_date not provided)
            
        Returns:
            Pandas DataFrame with OHLC data or None if failed
        """
        return await self.get_ohlc_data(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            asset_type=self.STOCK,
            bars=bars
        )
    
    async def get_symbol_metadata(self, symbol: str, asset_type: str = None) -> Optional[Dict[str, Any]]:
        """Get metadata for a symbol including available date range
        
        Args:
            symbol: The symbol to get metadata for
            asset_type: Type of asset (stock, crypto, forex) - auto-detected if None
            
        Returns:
            Dictionary with metadata including startDate and endDate, or None if failed
        """
        if not self.session:
            await self.connect()
            
        try:
            # Auto-detect asset type if not provided
            if asset_type is None:
                asset_type = self.STOCK  # Default to stock
            
            if asset_type == self.STOCK:
                endpoint = f"{self.BASE_URL}/tiingo/daily/{symbol}"
            elif asset_type == self.CRYPTO:
                endpoint = f"{self.BASE_URL}/tiingo/crypto/top"  # Crypto uses different endpoint
                # For crypto, we'll return a default range since metadata is different
                return {
                    "ticker": symbol,
                    "startDate": "2018-01-01",  # Crypto data typically starts around 2018
                    "endDate": dt.now().strftime("%Y-%m-%d")
                }
            elif asset_type == self.FOREX:
                endpoint = f"{self.BASE_URL}/tiingo/fx/top"  # Forex uses different endpoint
                # For forex, return a conservative range
                return {
                    "ticker": symbol,
                    "startDate": "2020-01-01",  # Forex data typically starts around 2020
                    "endDate": dt.now().strftime("%Y-%m-%d")
                }
            else:
                logger.error(f"Unsupported asset type: {asset_type}")
                return None
            
            async with self.session.get(endpoint, timeout=self.timeout) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Error fetching metadata for {symbol}: {response.status} - {error_text}")
                    return None
                
                data = await response.json()
                return data
                
        except Exception as e:
            logger.error(f"Error fetching metadata for {symbol}: {e}")
            return None