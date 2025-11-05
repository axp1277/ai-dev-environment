#!/usr/bin/env python3
"""
NY Midnight Timing Diagnostic Script

Investigates the NY Midnight line offset issue in Layer1 where the line
doesn't start at the actual midnight candle but appears offset to ~3 AM.
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

class NYMidnightDiagnostic:
    """Diagnostic tool for NY Midnight timing issues."""
    
    def __init__(self):
        self.provider = SchwabDataProvider()
        self.console = Console()
        self.ny_tz = pytz.timezone('America/New_York')
    
    def analyze_ny_midnight_timing(self, symbol: str = "/ESU25", timeframe: str = "5minute"):
        """Comprehensive analysis of NY Midnight timing in the data."""
        
        self.console.print(f"\n🔍 [bold blue]NY Midnight Timing Analysis for {symbol}[/bold blue]")
        
        # Fetch recent data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        
        df = self.provider.get_historical_data(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            timeframe=timeframe
        )
        
        if df.empty:
            self.console.print("[red]❌ No data retrieved[/red]")
            return
        
        self.console.print(f"✅ Retrieved {len(df)} bars from {df.index[0]} to {df.index[-1]}")
        
        # Analyze all potential midnight candidates
        self._analyze_midnight_candidates(df)
        
        # Test current Layer1 logic
        self._test_current_logic(df)
        
        # Analyze timezone conversions
        self._analyze_timezone_conversions(df)
        
        # Recommend solutions
        self._recommend_solutions(df)
    
    def _analyze_midnight_candidates(self, df: pd.DataFrame):
        """Find all potential NY Midnight candidates in the data."""
        
        self.console.print("\n📊 [bold yellow]Analyzing Potential NY Midnight Candidates[/bold yellow]")
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Index", width=8)
        table.add_column("Original Timestamp", width=20)
        table.add_column("UTC Timestamp", width=20) 
        table.add_column("NY Time", width=20)
        table.add_column("Hour:Min", width=10)
        table.add_column("Open Price", width=12)
        table.add_column("Is Midnight?", width=12)
        
        midnight_candidates = []
        
        for i in range(len(df)):
            timestamp = df.index[i]
            original_ts = timestamp
            
            # Convert to UTC if timezone-naive (assume UTC)
            if timestamp.tzinfo is None:
                timestamp = pytz.UTC.localize(timestamp)
            
            # Convert to NY timezone
            ny_time = timestamp.astimezone(self.ny_tz)
            
            # Check for midnight or near-midnight times
            is_midnight_candidate = (
                ny_time.hour == 0 or  # Exact midnight
                (ny_time.hour == 23 and ny_time.minute >= 55) or  # Just before midnight
                (ny_time.hour == 0 and ny_time.minute <= 15)  # Just after midnight
            )
            
            if is_midnight_candidate or i < 20 or i % 50 == 0:  # Show first 20 bars + samples
                open_price = df.iloc[i]['open']
                
                is_exact_midnight = ny_time.hour == 0 and ny_time.minute == 0
                midnight_status = "✅ YES" if is_exact_midnight else ("🟡 NEAR" if is_midnight_candidate else "❌ NO")
                
                table.add_row(
                    str(i),
                    str(original_ts),
                    str(timestamp),
                    str(ny_time),
                    f"{ny_time.hour:02d}:{ny_time.minute:02d}",
                    f"{open_price:.2f}",
                    midnight_status
                )
                
                if is_exact_midnight:
                    midnight_candidates.append((i, open_price, timestamp, ny_time))
        
        self.console.print(table)
        self.console.print(f"\n🎯 Found {len(midnight_candidates)} exact NY Midnight candidates")
        
        for i, (bar_idx, price, ts, ny_time) in enumerate(midnight_candidates):
            self.console.print(f"   {i+1}. Bar {bar_idx}: {ny_time} → Price: {price:.2f}")
        
        return midnight_candidates
    
    def _test_current_logic(self, df: pd.DataFrame):
        """Test the current Layer1 find_ny_midnight_bar logic."""
        
        self.console.print("\n🧪 [bold yellow]Testing Current Layer1 Logic[/bold yellow]")
        
        # Replicate current Layer1 logic exactly
        for i in range(len(df) - 1, -1, -1):
            timestamp = df.index[i]
            
            # Convert to NY timezone (current logic)
            if timestamp.tzinfo is None:
                # Assume UTC if no timezone
                timestamp = pytz.UTC.localize(timestamp)
            
            ny_time = timestamp.astimezone(self.ny_tz)
            
            # Check if this is midnight (00:00) - current logic
            if ny_time.hour == 0 and ny_time.minute == 0:
                open_price = df.iloc[i]['open']
                
                self.console.print(Panel(
                    f"[green]✅ Current Logic Found NY Midnight[/green]\n"
                    f"Bar Index: {i}\n"
                    f"Original Timestamp: {df.index[i]}\n"
                    f"NY Time: {ny_time}\n"
                    f"Open Price: {open_price:.2f}\n"
                    f"Bars from current: {len(df) - i - 1}",
                    title="Current Layer1 Logic Result",
                    border_style="green"
                ))
                return i, open_price, timestamp
        
        self.console.print(Panel(
            "[red]❌ Current Logic: No NY Midnight found in data range[/red]",
            title="Current Layer1 Logic Result",
            border_style="red"
        ))
        return None
    
    def _analyze_timezone_conversions(self, df: pd.DataFrame):
        """Analyze potential timezone conversion issues."""
        
        self.console.print("\n🌍 [bold yellow]Analyzing Timezone Conversions[/bold yellow]")
        
        # Sample a few timestamps for detailed analysis
        sample_indices = [0, len(df)//4, len(df)//2, 3*len(df)//4, -1]
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Sample", width=8)
        table.add_column("Raw Timestamp", width=20)
        table.add_column("Has Timezone?", width=12)
        table.add_column("Assumed UTC", width=20)
        table.add_column("NY Time", width=20)
        table.add_column("Chicago Time", width=20)
        
        for idx in sample_indices:
            if idx < 0:
                idx = len(df) + idx
            
            raw_ts = df.index[idx]
            has_tz = raw_ts.tzinfo is not None
            
            # Convert assuming UTC
            if raw_ts.tzinfo is None:
                utc_ts = pytz.UTC.localize(raw_ts)
            else:
                utc_ts = raw_ts.astimezone(pytz.UTC)
            
            ny_time = utc_ts.astimezone(self.ny_tz)
            chicago_tz = pytz.timezone('America/Chicago')
            chicago_time = utc_ts.astimezone(chicago_tz)
            
            table.add_row(
                f"{idx}",
                str(raw_ts),
                "✅" if has_tz else "❌",
                str(utc_ts),
                str(ny_time),
                str(chicago_time)
            )
        
        self.console.print(table)
        
        # Check if futures data might be in Chicago time
        self.console.print("\n💡 [bold cyan]Timezone Analysis Notes:[/bold cyan]")
        self.console.print("• Futures typically trade on Chicago time (CME)")
        self.console.print("• If data comes in Chicago time but we assume UTC, times will be offset")
        self.console.print("• 3 AM offset suggests data might be in Chicago time (UTC-6/-5)")
    
    def _recommend_solutions(self, df: pd.DataFrame):
        """Recommend solutions for the NY Midnight timing issue."""
        
        self.console.print("\n💡 [bold green]Recommended Solutions[/bold green]")
        
        solutions = [
            {
                "title": "1. Enhanced Midnight Detection",
                "description": "Search for nearest-to-midnight bar instead of exact match",
                "code_snippet": """
def find_ny_midnight_bar_enhanced(df: pd.DataFrame) -> Optional[Tuple]:
    ny_tz = pytz.timezone('America/New_York')
    best_candidate = None
    min_distance = float('inf')
    
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        if timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        ny_time = timestamp.astimezone(ny_tz)
        
        # Calculate minutes from midnight
        minutes_from_midnight = ny_time.hour * 60 + ny_time.minute
        if minutes_from_midnight > 12 * 60:  # After noon, calculate to next midnight
            minutes_from_midnight = (24 * 60) - minutes_from_midnight
        
        if minutes_from_midnight < min_distance:
            min_distance = minutes_from_midnight
            best_candidate = (i, df.iloc[i]['open'], timestamp)
    
    return best_candidate
"""
            },
            {
                "title": "2. Timezone-Aware Data Handling", 
                "description": "Properly handle data timezone (might be Chicago time for futures)",
                "code_snippet": """
def find_midnight_with_proper_timezone(df: pd.DataFrame, symbol: str) -> Optional[Tuple]:
    # Detect instrument timezone
    if symbol.startswith('/'):
        # Futures - likely Chicago time
        data_tz = pytz.timezone('America/Chicago')
    else:
        # Stocks - likely Eastern time
        data_tz = pytz.timezone('America/New_York')
    
    ny_tz = pytz.timezone('America/New_York')
    
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        
        # Assume data is in instrument's native timezone
        if timestamp.tzinfo is None:
            timestamp = data_tz.localize(timestamp)
        
        ny_time = timestamp.astimezone(ny_tz)
        
        if ny_time.hour == 0 and ny_time.minute == 0:
            return i, df.iloc[i]['open'], timestamp
    
    return None
"""
            },
            {
                "title": "3. Session-Based Detection",
                "description": "Find the first bar of NY trading session",
                "code_snippet": """
def find_ny_session_open(df: pd.DataFrame) -> Optional[Tuple]:
    ny_tz = pytz.timezone('America/New_York')
    
    for i in range(len(df) - 1, -1, -1):
        timestamp = df.index[i]
        if timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        ny_time = timestamp.astimezone(ny_tz)
        
        # Find Sunday 18:00 ET (Monday session start) or Monday 00:00 ET
        if ((ny_time.weekday() == 6 and ny_time.hour == 18) or  # Sunday 6PM
            (ny_time.weekday() == 0 and ny_time.hour == 0)):   # Monday midnight
            return i, df.iloc[i]['open'], timestamp
    
    return None
"""
            }
        ]
        
        for solution in solutions:
            self.console.print(Panel(
                f"[bold white]{solution['title']}[/bold white]\n\n"
                f"{solution['description']}\n\n"
                f"[dim]{solution['code_snippet']}[/dim]",
                border_style="blue"
            ))
    
    def test_enhanced_detection(self, df: pd.DataFrame):
        """Test the enhanced midnight detection method."""
        
        self.console.print("\n🧪 [bold yellow]Testing Enhanced Midnight Detection[/bold yellow]")
        
        ny_tz = pytz.timezone('America/New_York')
        best_candidate = None
        min_distance = float('inf')
        
        candidates = []
        
        for i in range(len(df) - 1, -1, -1):
            timestamp = df.index[i]
            if timestamp.tzinfo is None:
                timestamp = pytz.UTC.localize(timestamp)
            
            ny_time = timestamp.astimezone(ny_tz)
            
            # Calculate minutes from midnight
            minutes_from_midnight = ny_time.hour * 60 + ny_time.minute
            if minutes_from_midnight > 12 * 60:  # After noon, calculate to next midnight
                minutes_from_midnight = (24 * 60) - minutes_from_midnight
            
            if minutes_from_midnight <= 15:  # Within 15 minutes of midnight
                candidates.append((i, df.iloc[i]['open'], timestamp, ny_time, minutes_from_midnight))
            
            if minutes_from_midnight < min_distance:
                min_distance = minutes_from_midnight
                best_candidate = (i, df.iloc[i]['open'], timestamp, ny_time, minutes_from_midnight)
        
        if best_candidate:
            i, price, ts, ny_time, distance = best_candidate
            self.console.print(Panel(
                f"[green]✅ Enhanced Detection Found Best Candidate[/green]\n"
                f"Bar Index: {i}\n"
                f"NY Time: {ny_time}\n"
                f"Distance from Midnight: {distance} minutes\n"
                f"Open Price: {price:.2f}\n"
                f"Bars from current: {len(df) - i - 1}",
                title="Enhanced Detection Result",
                border_style="green"
            ))
            
            # Show all candidates
            if len(candidates) > 1:
                self.console.print(f"\n📋 All candidates within 15 minutes of midnight:")
                for i, price, ts, ny_time, distance in candidates:
                    self.console.print(f"   Bar {i}: {ny_time} ({distance} min from midnight) → {price:.2f}")
        else:
            self.console.print(Panel(
                "[red]❌ Enhanced Detection: No suitable candidate found[/red]",
                title="Enhanced Detection Result", 
                border_style="red"
            ))


def main():
    """Main diagnostic entry point."""
    
    diagnostic = NYMidnightDiagnostic()
    
    # Run comprehensive analysis
    diagnostic.analyze_ny_midnight_timing()
    
    # Test enhanced detection
    symbol = "/ESU25"
    timeframe = "5minute"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    
    df = diagnostic.provider.get_historical_data(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        timeframe=timeframe
    )
    
    if not df.empty:
        diagnostic.test_enhanced_detection(df)


if __name__ == "__main__":
    main()