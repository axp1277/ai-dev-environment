"""Abstract Broker Interface

This module defines the abstract base class for all broker implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from enum import Enum


class OrderType(Enum):
    """Enum for order types"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderDirection(Enum):
    """Enum for order directions"""
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    """Enum for order statuses"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Order:
    """Class to represent an order"""
    
    def __init__(self, symbol: str, order_type: OrderType, direction: OrderDirection,
                 quantity: float, price: Optional[float] = None,
                 stop_price: Optional[float] = None):
        """Initialize an order
        
        Args:
            symbol: The market symbol
            order_type: Type of order (MARKET, LIMIT, STOP, STOP_LIMIT)
            direction: Direction of order (BUY or SELL)
            quantity: Quantity to buy or sell
            price: Limit price (required for LIMIT and STOP_LIMIT orders)
            stop_price: Stop price (required for STOP and STOP_LIMIT orders)
        """
        self.symbol = symbol
        self.order_type = order_type
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.stop_price = stop_price
        self.status = OrderStatus.PENDING
        self.filled_quantity = 0.0
        self.average_fill_price = 0.0
        self.order_id = None  # Will be set by broker
        self.timestamp = None  # Will be set by broker
        self.error_message = None  # Will be set if order is rejected


class Position:
    """Class to represent a position"""
    
    def __init__(self, symbol: str, quantity: float, entry_price: float, 
                 direction: OrderDirection):
        """Initialize a position
        
        Args:
            symbol: The market symbol
            quantity: Position size
            entry_price: Average entry price
            direction: Position direction (BUY = long, SELL = short)
        """
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        self.direction = direction
        self.unrealized_pnl = 0.0
        self.realized_pnl = 0.0


class Broker(ABC):
    """Abstract base class for all broker implementations"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the broker with configuration
        
        Args:
            config: Broker configuration parameters
        """
        self.config = config
        self.name = self.config.get("name", "UnknownBroker")
        self.is_connected = False
        
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the broker API
        
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the broker API
        
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    async def get_account_info(self) -> Dict[str, Any]:
        """Get account information
        
        Returns:
            Dict with account information
        """
        pass
    
    @abstractmethod
    async def get_positions(self) -> Dict[str, Position]:
        """Get current positions
        
        Returns:
            Dict of positions by symbol
        """
        pass
    
    @abstractmethod
    async def place_order(self, order: Order) -> Tuple[bool, Optional[str]]:
        """Place an order with the broker
        
        Args:
            order: Order to place
            
        Returns:
            Tuple of (success, order_id)
        """
        pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order
        
        Args:
            order_id: ID of order to cancel
            
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    async def get_order_status(self, order_id: str) -> Optional[Order]:
        """Get status of an order
        
        Args:
            order_id: ID of order to check
            
        Returns:
            Order object with updated status or None if not found
        """
        pass
    
    @abstractmethod
    async def get_market_data(self, symbol: str, timeframe: str, 
                           bars: int = 100) -> Optional[Dict[str, Any]]:
        """Get market data for a symbol
        
        Args:
            symbol: The market symbol
            timeframe: Timeframe for bars (e.g., "5m", "1h", "1d")
            bars: Number of bars to retrieve
            
        Returns:
            Dict with market data or None if not available
        """
        pass
    
    @abstractmethod
    async def flatten_position(self, symbol: str) -> bool:
        """Close all positions for a symbol
        
        Args:
            symbol: Symbol to flatten position for
            
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    async def flatten_all_positions(self) -> bool:
        """Close all positions across all symbols
        
        Returns:
            Success status
        """
        pass