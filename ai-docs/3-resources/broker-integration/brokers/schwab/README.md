# Schwab Broker Module

This module provides unified access to Schwab API functionality through both a command-line interface and programmatic API access.

## Architecture

The Schwab module is organized into the following components:

- **`cli.py`** - Main CLI entry point with Click framework
- **`client.py`** - Core Schwab API client with authentication handling
- **`auth.py`** - Authentication and token management
- **`models.py`** - Pydantic data models for API responses
- **`adapter.py`** - Data provider adapter for seamless integration
- **`commands/`** - CLI command implementations organized by functionality

## CLI Usage

The unified CLI provides access to all Schwab functionality:

```bash
# Global shortcut (after uv pip install -e .)
schwab --help

# Direct execution
uv run src/brokers/schwab/cli.py --help
```

### Available Commands

- **Authentication**: `schwab auth refresh`, `schwab auth status`
- **Quotes**: `schwab quotes get --symbols SPY,AAPL`
- **Historical**: `schwab historical get --symbol SPY --days 5`
- **Testing**: `schwab test connection`, `schwab test provider`
- **Positions**: `schwab positions get`

## Programmatic Usage

```python
from src.brokers.schwab.client import SchwabClient
from src.brokers.schwab.adapter import SchwabDataProvider

# Direct API access
client = SchwabClient()
quotes = await client.get_quotes(['SPY', 'AAPL'])

# Data provider interface
provider = SchwabDataProvider()
data = await provider.get_current_price('SPY')
```

## Configuration

Set environment variables in `.env`:

```bash
APP_KEY=your_schwab_app_key
APP_SECRET=your_schwab_app_secret
ACCESS_TOKEN=your_access_token
REFRESH_TOKEN=your_refresh_token
```

## Features

- **Unified Interface**: Single CLI for all Schwab operations
- **Rich Output**: Beautiful tables and formatted data display
- **Error Handling**: Graceful handling of API errors and token expiration
- **Backward Compatible**: Existing imports continue to work via lazy loading
- **AI-Friendly**: Structured output suitable for programmatic use
- **Token Management**: Automatic refresh and status checking

## Development

All command implementations are in the `commands/` directory, organized by functionality:

- `auth.py` - Authentication commands
- `quotes.py` - Quote retrieval commands  
- `historical.py` - Historical data commands
- `test.py` - Testing and diagnostic commands
- `positions.py` - Position management commands

The CLI uses absolute imports to avoid circular dependencies and implements lazy loading for backward compatibility.