#!/usr/bin/env python3
"""
Schwab API Diagnostic Script

Quick diagnostic to test valid API parameters and identify the OHLC delay issue.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytz

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.client import SchwabClient
from loguru import logger

def test_api_parameters():
    """Test different API parameter combinations to find what works."""
    
    client = SchwabClient()
    symbol = "/ESZ24"  # December 2024 ES futures
    
    # Test configurations
    test_configs = [
        # Config 1: Current Layer1 logic
        {
            "name": "Current Layer1 (7 days, minute)",
            "params": {
                "symbol": symbol,
                "period_type": "day",
                "period": 7,
                "frequency_type": "minute", 
                "frequency": 5,
                "need_extended_hours_data": True,
                "need_previous_close": True
            }
        },
        # Config 2: 1 day period
        {
            "name": "1 Day Period",
            "params": {
                "symbol": symbol,
                "period_type": "day",
                "period": 1,
                "frequency_type": "minute",
                "frequency": 5,
                "need_extended_hours_data": True,
                "need_previous_close": True
            }
        },
        # Config 3: 2 day period  
        {
            "name": "2 Day Period",
            "params": {
                "symbol": symbol,
                "period_type": "day", 
                "period": 2,
                "frequency_type": "minute",
                "frequency": 5,
                "need_extended_hours_data": True,
                "need_previous_close": True
            }
        },
        # Config 4: 10 day period (max for minute freq)
        {
            "name": "10 Day Period (Max)",
            "params": {
                "symbol": symbol,
                "period_type": "day",
                "period": 10,
                "frequency_type": "minute",
                "frequency": 5,
                "need_extended_hours_data": True,
                "need_previous_close": True
            }
        },
        # Config 5: Date range instead of period
        {
            "name": "Date Range (3 days)",
            "params": {
                "symbol": symbol,
                "start_date": int((datetime.now() - timedelta(days=3)).timestamp() * 1000),
                "end_date": int(datetime.now().timestamp() * 1000),
                "frequency_type": "minute",
                "frequency": 5,
                "need_extended_hours_data": True,
                "need_previous_close": True
            }
        }
    ]
    
    print("🔍 Testing Schwab API parameter combinations...\n")
    
    for i, config in enumerate(test_configs, 1):
        print(f"Test {i}: {config['name']}")
        print(f"Parameters: {config['params']}")
        
        try:
            if symbol.startswith('/'):
                response = client.get_futures_price_history(**config['params'])
            else:
                response = client.get_price_history(**config['params'])
            
            if response and hasattr(response, 'candles') and response.candles:
                latest_candle = response.candles[-1]
                latest_time = datetime.fromtimestamp(latest_candle.datetime / 1000)
                current_time = datetime.now()
                delay_minutes = (current_time - latest_time).total_seconds() / 60
                
                print(f"✅ SUCCESS: {len(response.candles)} bars received")
                print(f"   Latest bar: {latest_time}")
                print(f"   Delay: {delay_minutes:.1f} minutes")
                print(f"   Sample OHLC: O:{latest_candle.open} H:{latest_candle.high} L:{latest_candle.low} C:{latest_candle.close}")
            else:
                print("❌ FAILED: No candle data in response")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print("-" * 60)
    
    # Test current quotes for comparison
    print("\n📊 Testing current quotes for delay comparison...")
    try:
        quotes = client.get_quotes([symbol])
        if symbol in quotes:
            quote = quotes[symbol].quote
            print(f"✅ Current quote: {quote.lastPrice} (Volume: {quote.totalVolume})")
            
            # Check quote timestamp if available
            if hasattr(quote, 'quoteTime'):
                quote_time = datetime.fromtimestamp(quote.quoteTime / 1000)
                quote_delay = (datetime.now() - quote_time).total_seconds() / 60
                print(f"   Quote time: {quote_time}")
                print(f"   Quote delay: {quote_delay:.1f} minutes")
        else:
            print(f"❌ No quote data for {symbol}")
    except Exception as e:
        print(f"❌ Quote error: {e}")

if __name__ == "__main__":
    test_api_parameters()