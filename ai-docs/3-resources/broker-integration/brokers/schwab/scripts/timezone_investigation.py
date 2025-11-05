#!/usr/bin/env python3
"""
Timezone Investigation Script

Investigate the timezone handling discrepancy between NY Midnight detection
and chart display that causes the 4 AM offset issue.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple
import pandas as pd
import pytz
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.adapter import SchwabDataProvider

def investigate_timezone_issue():
    """Investigate the timezone handling discrepancy."""
    
    console = Console()
    console.print("\n🕐 [bold blue]Timezone Investigation: NY Midnight vs Chart Display[/bold blue]")
    
    # Fetch data
    provider = SchwabDataProvider()
    symbol = "/ESU25"
    timeframe = "5minute"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2)
    
    df = provider.get_historical_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        timeframe=timeframe
    )
    
    if df.empty:
        console.print("[red]❌ No data retrieved[/red]")
        return
    
    console.print(f"✅ Retrieved {len(df)} bars")
    
    # Find NY Midnight using current logic
    ny_tz = pytz.timezone('America/New_York')
    midnight_bar = None
    
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        
        # Current logic: assume UTC if no timezone
        if timestamp.tzinfo is None:
            timestamp_utc = pytz.UTC.localize(timestamp)
        else:
            timestamp_utc = timestamp.astimezone(pytz.UTC)
        
        ny_time = timestamp_utc.astimezone(ny_tz)
        
        if ny_time.hour == 0 and ny_time.minute == 0:
            midnight_bar = i
            break
    
    if midnight_bar is None:
        console.print("[red]❌ No NY Midnight found[/red]")
        return
    
    # Analyze the timestamps around midnight
    console.print(f"\n📊 [bold yellow]Analysis around NY Midnight (Bar {midnight_bar})[/bold yellow]")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Bar Index", width=10)
    table.add_column("Raw Timestamp", width=20)
    table.add_column("UTC Timestamp", width=20)
    table.add_column("NY Time", width=20)
    table.add_column("Chart Display", width=15)
    table.add_column("Is Midnight?", width=12)
    
    # Show bars around midnight
    start_idx = max(0, midnight_bar - 5)
    end_idx = min(len(df), midnight_bar + 6)
    
    for i in range(start_idx, end_idx):
        raw_ts = df.index[i]
        
        # Convert to UTC
        if raw_ts.tzinfo is None:
            utc_ts = pytz.UTC.localize(raw_ts)
        else:
            utc_ts = raw_ts.astimezone(pytz.UTC)
        
        # Convert to NY time
        ny_time = utc_ts.astimezone(ny_tz)
        
        # What would the chart display? (likely raw timestamp or UTC)
        chart_display = f"{raw_ts.hour:02d}:{raw_ts.minute:02d}"
        
        is_midnight = "✅ YES" if i == midnight_bar else "❌ NO"
        
        # Highlight the midnight bar
        if i == midnight_bar:
            table.add_row(
                f"[bold green]{i}[/bold green]",
                f"[bold green]{raw_ts}[/bold green]",
                f"[bold green]{utc_ts}[/bold green]",
                f"[bold green]{ny_time}[/bold green]",
                f"[bold green]{chart_display}[/bold green]",
                f"[bold green]{is_midnight}[/bold green]"
            )
        else:
            table.add_row(
                str(i),
                str(raw_ts),
                str(utc_ts),
                str(ny_time),
                chart_display,
                is_midnight
            )
    
    console.print(table)
    
    # Show the problem
    midnight_raw = df.index[midnight_bar]
    midnight_utc = pytz.UTC.localize(midnight_raw) if midnight_raw.tzinfo is None else midnight_raw.astimezone(pytz.UTC)
    midnight_ny = midnight_utc.astimezone(ny_tz)
    
    console.print(Panel(
        f"[red]🚨 PROBLEM IDENTIFIED[/red]\n\n"
        f"NY Midnight Detection:\n"
        f"• Finds bar {midnight_bar} correctly\n"
        f"• Raw timestamp: {midnight_raw}\n" 
        f"• NY time: {midnight_ny} ← This IS midnight in NY\n\n"
        f"Chart Display Issue:\n"
        f"• Chart x-axis likely shows: {midnight_raw.hour:02d}:{midnight_raw.minute:02d} ← This shows as 4 AM\n"
        f"• Level line starts at bar {midnight_bar}\n"
        f"• But bar {midnight_bar} appears as '4 AM' on chart\n\n"
        f"[yellow]Solution: Chart needs to display NY time, not UTC time[/yellow]",
        title="Root Cause Analysis",
        border_style="red"
    ))
    
    # Recommend solutions
    console.print(f"\n💡 [bold green]Recommended Solutions[/bold green]")
    
    solutions = [
        {
            "title": "1. Fix Chart Timezone Display",
            "description": "Convert DataFrame index to NY timezone before passing to ChartViz",
            "code": """
# In Layer1 generate_naked_chart method:
def generate_naked_chart(self, df: pd.DataFrame, timeframe: str) -> Chart:
    # Convert DataFrame timestamps to NY timezone for display
    ny_tz = pytz.timezone('America/New_York')
    df_display = df.copy()
    
    if df_display.index.tz is None:
        df_display.index = pd.to_datetime(df_display.index, utc=True)
    
    # Convert to NY time for chart display
    df_display.index = df_display.index.tz_convert(ny_tz)
    
    # Rest of chart generation logic...
    chart.add_candlesticks(df_display, candlestick_config)
"""
        },
        {
            "title": "2. Use Timestamp-Based Level Lines",
            "description": "Instead of bar indices, use actual timestamps for Level positioning",
            "code": """
# Modified add_ny_midnight_line method:
def add_ny_midnight_line(self, chart: Chart, timestamp: pd.Timestamp, price: float) -> None:
    # Convert timestamp to NY time for chart alignment
    ny_tz = pytz.timezone('America/New_York') 
    if timestamp.tz is None:
        timestamp = pytz.UTC.localize(timestamp)
    ny_timestamp = timestamp.tz_convert(ny_tz)
    
    # Use timestamp instead of bar index
    level = Level(
        price=price,
        start_timestamp=ny_timestamp,  # Use timestamp instead of bar index
        # ... rest of config
    )
"""
        },
        {
            "title": "3. Consistent Timezone Throughout Pipeline",
            "description": "Ensure all data processing uses NY timezone consistently",
            "code": """
# At data fetch level in schwab adapter:
def get_historical_data(self, symbol: str, start_date: datetime, end_date: datetime, timeframe: str) -> pd.DataFrame:
    # ... fetch data ...
    
    # Convert all timestamps to NY timezone immediately
    ny_tz = pytz.timezone('America/New_York')
    if df.index.tz is None:
        df.index = pd.to_datetime(df.index, utc=True)
    df.index = df.index.tz_convert(ny_tz)
    
    return df
"""
        }
    ]
    
    for i, solution in enumerate(solutions, 1):
        console.print(Panel(
            f"[bold white]{solution['title']}[/bold white]\n\n"
            f"{solution['description']}\n\n"
            f"[dim]{solution['code']}[/dim]",
            border_style="blue"
        ))


if __name__ == "__main__":
    investigate_timezone_issue()