#!/usr/bin/env python3
"""
Test the corrected NY Midnight detection logic.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytz
from loguru import logger
from rich.console import Console
from rich.panel import Panel

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.adapter import SchwabDataProvider

def test_corrected_midnight_detection():
    """Test the corrected midnight detection with longer lookback."""
    
    console = Console()
    console.print("\n🕐 [bold blue]Testing Corrected NY Midnight Detection[/bold blue]")
    
    provider = SchwabDataProvider()
    symbol = "/ESU25"
    
    # Use 3-day lookback (working limit)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)  # 3 day lookback
    
    df = provider.get_historical_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        timeframe="5minute"
    )
    
    if df.empty:
        console.print("[red]❌ No data retrieved[/red]")
        return
    
    console.print(f"✅ Retrieved {len(df)} bars from {df.index[0]} to {df.index[-1]}")
    
    # Apply corrected logic (no timezone conversion)
    midnight_found = None
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        
        # Check if this is exactly midnight (00:00) - no timezone conversion
        if timestamp.hour == 0 and timestamp.minute == 0:
            open_price = df.iloc[i]['open']
            midnight_found = (i, open_price, timestamp)
            break
    
    if midnight_found:
        i, price, timestamp = midnight_found
        bars_since = len(df) - i - 1
        
        console.print(Panel(
            f"[green]✅ NY Midnight Found with Corrected Logic![/green]\n\n"
            f"Bar Index: {i}\n"
            f"Timestamp: {timestamp}\n"
            f"Open Price: {price:.2f}\n"
            f"Bars since midnight: {bars_since}\n\n"
            f"[yellow]This should now be the ACTUAL midnight candle![/yellow]",
            title="Corrected NY Midnight Detection",
            border_style="green"
        ))
        
        # Show nearby bars for context
        console.print("\n📊 [bold yellow]Context: Bars Around Midnight[/bold yellow]")
        
        start_context = max(0, i - 3)
        end_context = min(len(df), i + 4)
        
        for ctx_i in range(start_context, end_context):
            ctx_ts = df.index[ctx_i]
            ctx_price = df.iloc[ctx_i]['open']
            
            if ctx_i == i:
                console.print(f"→ [bold green]Bar {ctx_i}: {ctx_ts} | Open: {ctx_price:.2f} ← MIDNIGHT[/bold green]")
            else:
                console.print(f"  Bar {ctx_i}: {ctx_ts} | Open: {ctx_price:.2f}")
        
    else:
        console.print(Panel(
            f"[red]❌ No NY Midnight found in {len(df)} bars[/red]\n\n"
            f"Data range: {df.index[0]} to {df.index[-1]}\n"
            f"This might be normal if the data doesn't span a full trading session",
            title="No Midnight Found",
            border_style="red"
        ))
        
        # Show some sample timestamps to understand the data pattern
        console.print("\n📊 [bold yellow]Sample Data Timestamps[/bold yellow]")
        for i in [0, len(df)//4, len(df)//2, 3*len(df)//4, -1]:
            if i < 0:
                i = len(df) + i
            ts = df.index[i]
            console.print(f"Bar {i}: {ts} ({ts.strftime('%A %H:%M')})")

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {message}")
    
    test_corrected_midnight_detection()