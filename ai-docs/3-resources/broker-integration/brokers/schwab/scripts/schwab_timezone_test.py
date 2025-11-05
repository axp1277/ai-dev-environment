#!/usr/bin/env python3
"""
Schwab Timezone Detection Script

Test what timezone Schwab data is actually in by comparing with known market events.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pytz
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.adapter import SchwabDataProvider

def test_schwab_timezone():
    """Test what timezone Schwab data is actually in."""
    
    console = Console()
    console.print("\n🕐 [bold blue]Schwab Data Timezone Detection[/bold blue]")
    
    # Fetch data
    provider = SchwabDataProvider()
    symbol = "/ESU25"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2)
    
    df = provider.get_historical_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        timeframe="5minute"
    )
    
    if df.empty:
        console.print("[red]❌ No data retrieved[/red]")
        return
    
    console.print(f"✅ Retrieved {len(df)} bars")
    
    # Test different timezone assumptions
    ny_tz = pytz.timezone('America/New_York')
    chicago_tz = pytz.timezone('America/Chicago')
    utc_tz = pytz.UTC
    
    console.print("\n📊 [bold yellow]Testing Different Timezone Assumptions[/bold yellow]")
    
    # Look for potential midnight candidates
    midnight_candidates = {
        'assume_utc': [],
        'assume_ny': [],  
        'assume_chicago': []
    }
    
    for i in range(min(50, len(df))):  # Check first 50 bars
        raw_ts = df.index[i]
        
        # Test 1: Assume data is UTC (current wrong assumption)
        if raw_ts.tzinfo is None:
            utc_ts = pytz.UTC.localize(raw_ts)
        else:
            utc_ts = raw_ts.astimezone(utc_tz)
        ny_from_utc = utc_ts.astimezone(ny_tz)
        
        if ny_from_utc.hour == 0 and ny_from_utc.minute == 0:
            midnight_candidates['assume_utc'].append((i, raw_ts, ny_from_utc))
        
        # Test 2: Assume data is already NY time (likely correct)
        if raw_ts.tzinfo is None:
            ny_native = ny_tz.localize(raw_ts, is_dst=None)
        else:
            ny_native = raw_ts
        
        if ny_native.hour == 0 and ny_native.minute == 0:
            midnight_candidates['assume_ny'].append((i, raw_ts, ny_native))
        
        # Test 3: Assume data is Chicago time
        if raw_ts.tzinfo is None:
            chicago_native = chicago_tz.localize(raw_ts, is_dst=None) 
        else:
            chicago_native = raw_ts
        ny_from_chicago = chicago_native.astimezone(ny_tz)
        
        if ny_from_chicago.hour == 0 and ny_from_chicago.minute == 0:
            midnight_candidates['assume_chicago'].append((i, raw_ts, ny_from_chicago))
    
    # Display results
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Assumption", width=15)
    table.add_column("Midnight Candidates Found", width=30)
    table.add_column("Analysis", width=40)
    
    for assumption, candidates in midnight_candidates.items():
        if candidates:
            candidate_str = f"{len(candidates)} found:\n"
            for i, raw_ts, converted_ts in candidates[:3]:  # Show first 3
                candidate_str += f"Bar {i}: {raw_ts} → {converted_ts}\n"
        else:
            candidate_str = "None found"
        
        if assumption == 'assume_utc':
            analysis = "Current (wrong) logic - assumes raw data is UTC"
        elif assumption == 'assume_ny':
            analysis = "Likely correct - assumes raw data is NY time"
        else:
            analysis = "Alternative - assumes raw data is Chicago time"
        
        table.add_row(assumption, candidate_str, analysis)
    
    console.print(table)
    
    # Show sample timestamps with all interpretations
    console.print("\n🔍 [bold yellow]Sample Timestamp Analysis[/bold yellow]")
    
    sample_indices = [0, 10, 20] if len(df) > 20 else [0, len(df)//2, -1]
    
    detail_table = Table(show_header=True, header_style="bold blue")
    detail_table.add_column("Bar", width=5)
    detail_table.add_column("Raw Timestamp", width=20)
    detail_table.add_column("If UTC→NY", width=20)
    detail_table.add_column("If Already NY", width=20)
    detail_table.add_column("If Chicago→NY", width=20)
    
    for idx in sample_indices:
        if idx < 0:
            idx = len(df) + idx
        
        raw_ts = df.index[idx]
        
        # UTC assumption
        utc_ts = pytz.UTC.localize(raw_ts) if raw_ts.tzinfo is None else raw_ts.astimezone(utc_tz)
        ny_from_utc = utc_ts.astimezone(ny_tz)
        
        # NY assumption  
        ny_native = ny_tz.localize(raw_ts, is_dst=None) if raw_ts.tzinfo is None else raw_ts
        
        # Chicago assumption
        chicago_ts = chicago_tz.localize(raw_ts, is_dst=None) if raw_ts.tzinfo is None else raw_ts
        ny_from_chicago = chicago_ts.astimezone(ny_tz)
        
        detail_table.add_row(
            str(idx),
            str(raw_ts),
            f"{ny_from_utc.strftime('%H:%M:%S')} EDT",
            f"{ny_native.strftime('%H:%M:%S')} EDT", 
            f"{ny_from_chicago.strftime('%H:%M:%S')} EDT"
        )
    
    console.print(detail_table)
    
    # Market hours analysis
    console.print("\n📈 [bold yellow]Market Hours Analysis[/bold yellow]")
    
    # ES futures trade nearly 24/7 from Sunday 5 PM CT to Friday 4 PM CT
    # In NY time: Sunday 6 PM ET to Friday 5 PM ET
    
    first_bar = df.index[0] 
    last_bar = df.index[-1]
    
    console.print(Panel(
        f"[bold white]Data Range Analysis[/bold white]\n\n"
        f"First bar: {first_bar}\n"
        f"Last bar: {last_bar}\n\n"
        f"[yellow]Key Insights:[/yellow]\n"
        f"• ES futures trade Sunday 6 PM ET - Friday 5 PM ET\n"
        f"• If data shows bars at 18:00-22:00, it's likely NY time\n"
        f"• If data shows bars at 22:00-02:00, it might be UTC\n"
        f"• Futures NY midnight (00:00 ET) is a key session boundary\n\n"
        f"[green]Expected Reality:[/green]\n"
        f"Schwab likely provides futures data in NY time (EST/EDT)\n"
        f"since that's the primary US trading timezone.",
        title="Market Context",
        border_style="blue"
    ))

def recommend_fix():
    """Recommend the correct fix based on findings."""
    
    console = Console()
    
    console.print("\n💡 [bold green]Recommended Fix[/bold green]")
    
    fix_code = '''
def find_ny_midnight_bar_corrected(self, df: pd.DataFrame) -> Optional[Tuple[int, float, pd.Timestamp]]:
    """Find NY Midnight bar assuming Schwab data is ALREADY in NY timezone."""
    
    logger.info("Searching for NY Midnight (assuming data is already NY time)")
    
    # DO NOT convert timezone - data is already in NY time
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        
        # Check if this is exactly midnight (no timezone conversion needed)
        if timestamp.hour == 0 and timestamp.minute == 0:
            open_price = df.iloc[i]['open']
            logger.info(f"Found NY Midnight at index {i}: {timestamp}, price: {open_price}")
            return i, open_price, timestamp
    
    logger.warning("No NY Midnight found in data range")
    return None
'''
    
    console.print(Panel(
        f"[bold white]Corrected NY Midnight Detection[/bold white]\n\n"
        f"[red]Problem:[/red] Current code assumes Schwab data is UTC and converts to NY time\n"
        f"[green]Reality:[/green] Schwab data is already in NY time (EST/EDT)\n"
        f"[blue]Solution:[/blue] Remove the timezone conversion logic\n\n"
        f"[dim]{fix_code}[/dim]",
        title="Code Fix",
        border_style="green"
    ))

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {message}")
    
    test_schwab_timezone()
    recommend_fix()