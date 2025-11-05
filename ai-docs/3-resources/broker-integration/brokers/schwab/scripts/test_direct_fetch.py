#!/usr/bin/env python3
"""
Direct test of Schwab adapter to verify it's working with Layer1 parameters
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.adapter import SchwabDataProvider

def test_direct_fetch():
    """Test direct Schwab data fetch with Layer1 parameters."""
    
    provider = SchwabDataProvider()
    symbol = "/ESZ24"  # Use December 2024 contract
    
    # Test configurations matching Layer1 config
    test_cases = [
        {"timeframe": "5minute", "days": 3},
        {"timeframe": "15minute", "days": 5}
    ]
    
    for case in test_cases:
        timeframe = case["timeframe"]
        days = case["days"]
        
        print(f"\n🔍 Testing {symbol} {timeframe} with {days} days lookback...")
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            print(f"   Date range: {start_date} to {end_date}")
            
            df = provider.get_historical_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                timeframe=timeframe
            )
            
            if not df.empty:
                latest_bar = df.index[-1]
                current_time = datetime.now()
                
                # Convert latest_bar to timezone-naive for comparison if needed
                if latest_bar.tzinfo is not None:
                    latest_bar = latest_bar.replace(tzinfo=None)
                
                delay_minutes = (current_time - latest_bar).total_seconds() / 60
                
                print(f"✅ SUCCESS: {len(df)} bars received")
                print(f"   Date range: {df.index[0]} to {df.index[-1]}")
                print(f"   Latest bar: {latest_bar}")
                print(f"   Delay: {delay_minutes:.1f} minutes")
                print(f"   Sample OHLC: O:{df.iloc[-1]['open']:.2f} H:{df.iloc[-1]['high']:.2f} L:{df.iloc[-1]['low']:.2f} C:{df.iloc[-1]['close']:.2f}")
                
                # Check if delay indicates stale data
                if delay_minutes > 60:  # More than 1 hour delay
                    print(f"⚠️  WARNING: Data appears stale (>{delay_minutes:.0f} min delay)")
                elif delay_minutes > 30:  # More than 30 min delay
                    print(f"⚠️  WARNING: Data appears delayed (>{delay_minutes:.0f} min delay)")
                else:
                    print(f"✅ Data freshness looks good ({delay_minutes:.0f} min delay)")
                    
            else:
                print("❌ FAILED: No data returned")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            logger.error(f"Direct fetch failed for {timeframe}: {e}")

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {level} | {message}")
    test_direct_fetch()