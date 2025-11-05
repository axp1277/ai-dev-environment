# Schwab Data Provider Integration

This document provides information about the integration of the Schwab API as a data provider for the Confluence AI Digital Twin Trader.

## Overview

The Schwab API integration allows the Confluence AI Digital Twin Trader to fetch real-time and historical market data directly from Schwab's API instead of relying on CSV files. This provides more accurate and up-to-date data for analysis and trading decisions.

## Changes Made

The following changes were made to integrate the Schwab API:

1. Created a `SchwabDataProvider` adapter class in `src/data_providers/schwab_adapter.py` that implements the `DataProvider` interface
2. Updated the import statements in `src/data_providers/__init__.py` to include the new adapter
3. Modified the following files to use the `SchwabDataProvider` instead of the `CSVDataProvider`:
   - `src/pipelines/ai_trader.py`
   - `src/pipelines/market_structure_bias_pipeline.py`
   - `src/pipelines/liquidity_bias_pipeline.py`
   - `src/adr_extractor.py`
4. Created a test script `test_schwab_provider.py` to verify the functionality of the new provider

## Setup Requirements

To use the Schwab API integration, you need to:

1. Create a Schwab Developer account at https://developer.schwab.com/
2. Register an application to get API credentials
3. Create a `.env` file in the project root directory with the following variables:
   ```
   APP_KEY=your_app_key
   APP_SECRET=your_app_secret
   ACCESS_TOKEN=your_access_token
   REFRESH_TOKEN=your_refresh_token
   ```

## Symbol Format and Timeframe Limitations

When using the `SchwabDataProvider`, you need to provide the exact symbol as expected by the Schwab API:

- For futures contracts, use the full symbol with slash prefix, month code, and year. For example:
  - `/ESM25` for E-mini S&P 500 futures, May 2025 contract
  - `/NQM25` for E-mini NASDAQ-100 futures, May 2025 contract
  - `/CLK25` for Crude Oil futures, May 2025 contract
  - `/GCJ25` for Gold futures, April 2025 contract

- For stocks and ETFs, use the standard ticker symbol (e.g., `AAPL`, `SPY`).

### Timeframe Limitations

The Schwab API has the following limitations for timeframes:

- For minute data, only 1, 5, 10, 15, and 30 minute intervals are supported
- The adapter automatically maps unsupported intervals to supported ones:
  - `60minute` → `30minute` (closest supported interval)
  - `240minute` → `30minute` (closest supported interval)

## Usage with Discord Bot

When using the Discord bot commands, you need to specify the exact symbol format:

```
!ai /ESM25  # Use the full futures symbol with slash prefix
!chart /ESM25 1d
!bias /ESM25
!market_structure /ESM25 30minute  # For market structure bias analysis with 30-minute timeframe
!liquidity_bias /ESM25 30minute  # For liquidity bias analysis with 30-minute timeframe
```

The default symbol for the `!ai` command is "ES", but since we've removed symbol mapping, you should use the full symbol format (e.g., `/ESM25`) instead.

### Market Structure Bias Command

The `!market_structure` command allows you to analyze market structure bias for a specific symbol and timeframe:

```
!market_structure <symbol> <timeframe>
```

Parameters:
- `symbol`: The full symbol (e.g., `/ESM25`)
- `timeframe`: One of the supported timeframes: `1day`, `60minute`, `30minute`, `15minute`, `5minute`

Examples:
- `!market_structure /ESM25 1day` - Daily market structure bias analysis
- `!market_structure /ESM25 30minute` - 30-minute market structure bias analysis
- `!market_structure /ESM25 15minute` - 15-minute market structure bias analysis

### Liquidity Bias Command

The `!liquidity_bias` command allows you to analyze liquidity bias for a specific symbol and timeframe:

```
!liquidity_bias <symbol> <timeframe>
```

Parameters:
- `symbol`: The full symbol (e.g., `/ESM25`)
- `timeframe`: One of the supported timeframes: `1day`, `60minute`, `30minute`, `15minute`, `5minute`

Examples:
- `!liquidity_bias /ESM25 1day` - Daily liquidity bias analysis
- `!liquidity_bias /ESM25 30minute` - 30-minute liquidity bias analysis
- `!liquidity_bias /ESM25 15minute` - 15-minute liquidity bias analysis

## Testing

You can test the Schwab API integration by running the test script:

```bash
python test_schwab_provider.py
```

This script will:
1. Initialize the `SchwabDataProvider`
2. Fetch historical data for SPY (stock) and /ESM25 (futures)
3. Display the data in a table format

## Troubleshooting

If you encounter issues with the Schwab API integration, check the following:

1. Verify that your API credentials are correct in the `.env` file
2. Check the `schwab_api.log` file for error messages
3. Ensure that you have the necessary permissions to access the requested data
4. Verify that the symbol mapping is correct for the symbols you're using

## Fallback Mechanism

If needed, you can implement a fallback mechanism to use the `CSVDataProvider` when the `SchwabDataProvider` fails:

```python
try:
    data_provider = SchwabDataProvider()
    # Test connection
    test_data = data_provider.get_market_data("SPY")
    if test_data.empty:
        logger.warning("Could not connect to Schwab API, falling back to CSV provider")
        data_provider = CSVDataProvider(CSVConfig())
except Exception as e:
    logger.error(f"Error initializing Schwab API: {e}")
    logger.warning("Falling back to CSV provider")
    data_provider = CSVDataProvider(CSVConfig())
```

## Future Improvements

Potential future improvements for the Schwab API integration:

1. Implement caching to reduce API calls
2. Add support for real-time streaming data
3. Enhance error handling and retry mechanisms
4. Implement automatic contract roll for futures symbols
5. Add support for options data
