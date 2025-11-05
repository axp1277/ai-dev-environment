# Polygon Market Data Fetcher

A minimalistic CLI tool for fetching OHLCV data from Polygon.io and storing it in a local SQLite database.

## Purpose

Fetches aggregate bars (OHLCV) data from Polygon.io REST API and stores it in a local SQLite database with automatic duplicate prevention.

## Installation

1. Install dependencies (from project root):
```bash
# Project uses uv for dependency management
uv sync
```

2. Set up environment:
```bash
# Option 1: Add to existing project root .env file (recommended)
echo "POLYGON_API_KEY=your_api_key_here" >> .env

# Option 2: Create local .env file in polygon directory
echo "POLYGON_API_KEY=your_api_key_here" > src/brokers/polygon/.env
```

3. Install CLI shortcut (from project root):
```bash
# Install the package in editable mode to enable CLI shortcuts
uv pip install -e .
```

## Usage

### Using the CLI shortcut (recommended):
```bash
# Display help
polygon --help

# Fetch data for a ticker
polygon SPY 5minute 500

# More examples
polygon AAPL 1minute 100
polygon MSFT 15minute 200
polygon GOOGL 60minute 50
```

### Using the script directly:
```bash
# From the polygon directory
cd src/brokers/polygon
python fetch.py SPY 5minute 500
```

### Supported timeframes:
- `1minute` - 1-minute bars
- `5minute` - 5-minute bars
- `15minute` - 15-minute bars
- `60minute` - 60-minute bars

## Database

Data is stored in `data/market_data.db` (in the project root data directory) with tables named `market_data_{TICKER}_{TIMEFRAME}`.

Example: `market_data_SPY_5Minute`

The database file is automatically created in the project's `data/` directory when you first run the tool.

## API Documentation

Uses Polygon.io aggregate bars endpoint:
- Endpoint: `/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}`
- Authentication: API key via query parameter