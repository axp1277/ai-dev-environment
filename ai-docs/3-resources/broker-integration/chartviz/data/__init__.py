"""Data provider factory - SQLite default."""

from typing import Dict, Type
from .base import DataProvider
from .sqlite import SQLiteProvider

# Provider registry with SQLite as default
PROVIDERS: Dict[str, Type[DataProvider]] = {
    'sqlite': SQLiteProvider,
}

# Conditionally add Polygon provider (may not be available in all environments)
try:
    from .polygon import PolygonProvider
    PROVIDERS['polygon'] = PolygonProvider
except ImportError:
    pass  # Polygon provider not available

# Conditionally add Schwab provider (may not be available in all environments)
try:
    from .schwab import SchwabProvider
    PROVIDERS['schwab'] = SchwabProvider
except ImportError:
    pass  # Schwab provider not available

def create_provider(provider_type: str = 'sqlite', **kwargs) -> DataProvider:
    """Create data provider instance - defaults to SQLite."""
    if provider_type not in PROVIDERS:
        available = ', '.join(PROVIDERS.keys())
        raise ValueError(f"Unknown provider: {provider_type}. Available: {available}")
    
    return PROVIDERS[provider_type](**kwargs)

def get_available_providers() -> list[str]:
    """Get list of available provider types."""
    return list(PROVIDERS.keys())

# Convenience exports
__all__ = ['DataProvider', 'create_provider', 'get_available_providers']