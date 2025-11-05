#!/usr/bin/env python3
"""
Schwab OHLC Data Quality Validation Script

This script validates the quality and timeliness of OHLC data from Schwab API
by performing comprehensive checks on data freshness, consistency, and accuracy.

Key Issues Identified in Current Implementation:
1. Timestamp conversion (datetime/1000) - potential timezone issues
2. No explicit delay validation 
3. Period calculations may request stale data for recent timeframes
4. No real-time comparison with market hours

Usage:
    python data_quality_checker.py --symbol EURUSD --timeframe 5minute --check-delay
    python data_quality_checker.py --symbol /ES --timeframe 15minute --reference-time "2024-01-15 14:30:00"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import pytz
from loguru import logger
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.schwab.client import SchwabClient
from src.brokers.schwab.adapter import SchwabDataProvider


@dataclass
class DataQualityMetrics:
    """Data quality assessment metrics."""
    symbol: str
    timeframe: str
    total_bars: int
    latest_bar_timestamp: datetime
    delay_seconds: float
    expected_delay_seconds: float
    gaps_count: int
    duplicates_count: int
    zero_volume_count: int
    ohlc_consistency_errors: int
    timezone_issues: int
    data_completeness_percent: float
    is_market_hours: bool
    assessment: str  # GOOD, DELAYED, POOR, CRITICAL


class SchwabDataQualityChecker:
    """Comprehensive OHLC data quality validation for Schwab API."""
    
    def __init__(self):
        self.schwab_client = SchwabClient()
        self.schwab_provider = SchwabDataProvider()
        self.console = Console()
        
        # Market hours for different instruments
        self.market_hours = {
            'forex': {
                'timezone': 'America/New_York',
                'open': '17:00',  # Sunday 5PM EST
                'close': '17:00',  # Friday 5PM EST
                'days': [0, 1, 2, 3, 4, 6]  # Mon-Fri + Sunday evening
            },
            'futures': {
                'timezone': 'America/Chicago', 
                'open': '17:00',  # Sunday 5PM CST
                'close': '16:00',  # Friday 4PM CST
                'days': [0, 1, 2, 3, 4, 6]  # Mon-Fri + Sunday evening
            },
            'stocks': {
                'timezone': 'America/New_York',
                'open': '09:30',
                'close': '16:00', 
                'days': [0, 1, 2, 3, 4]  # Mon-Fri only
            }
        }
        
        # Expected delays by timeframe (realistic expectations)
        self.expected_delays = {
            '1minute': 60,      # 1 minute delay acceptable
            '5minute': 120,     # 2 minute delay acceptable  
            '15minute': 300,    # 5 minute delay acceptable
            '30minute': 600,    # 10 minute delay acceptable
            '60minute': 900,    # 15 minute delay acceptable
            '240minute': 1800,  # 30 minute delay acceptable
            '1day': 3600        # 1 hour delay acceptable for daily
        }
    
    def detect_instrument_type(self, symbol: str) -> str:
        """Detect instrument type based on symbol format."""
        if symbol.startswith('/'):
            return 'futures'
        elif any(curr in symbol.upper() for curr in ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD']):
            return 'forex'
        else:
            return 'stocks'
    
    def is_market_open(self, symbol: str, timestamp: datetime) -> bool:
        """Check if market is open for given symbol at timestamp."""
        instrument_type = self.detect_instrument_type(symbol)
        market_config = self.market_hours[instrument_type]
        
        # Convert timestamp to market timezone
        market_tz = pytz.timezone(market_config['timezone'])
        if timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        market_time = timestamp.astimezone(market_tz)
        
        # Check if it's a trading day
        if market_time.weekday() not in market_config['days']:
            return False
        
        # For forex/futures, handle Sunday evening opening
        if instrument_type in ['forex', 'futures'] and market_time.weekday() == 6:  # Sunday
            open_time = datetime.strptime(market_config['open'], '%H:%M').time()
            return market_time.time() >= open_time
        
        # Regular trading hours check
        open_time = datetime.strptime(market_config['open'], '%H:%M').time()
        close_time = datetime.strptime(market_config['close'], '%H:%M').time()
        
        return open_time <= market_time.time() <= close_time
    
    def validate_ohlc_consistency(self, df: pd.DataFrame) -> List[int]:
        """Validate OHLC data consistency (High >= Open,Close,Low; Low <= Open,Close,High)."""
        errors = []
        
        for i, row in df.iterrows():
            # High should be >= Open, Close, Low
            if not (row['high'] >= row['open'] and 
                   row['high'] >= row['close'] and 
                   row['high'] >= row['low']):
                errors.append(i)
                continue
            
            # Low should be <= Open, Close, High  
            if not (row['low'] <= row['open'] and
                   row['low'] <= row['close'] and
                   row['low'] <= row['high']):
                errors.append(i)
        
        return errors
    
    def detect_gaps(self, df: pd.DataFrame, timeframe: str) -> List[Tuple[datetime, datetime]]:
        """Detect gaps in the time series based on expected intervals."""
        if len(df) < 2:
            return []
        
        # Convert timeframe to timedelta
        timeframe_mapping = {
            '1minute': timedelta(minutes=1),
            '5minute': timedelta(minutes=5), 
            '15minute': timedelta(minutes=15),
            '30minute': timedelta(minutes=30),
            '60minute': timedelta(hours=1),
            '240minute': timedelta(hours=4),
            '1day': timedelta(days=1)
        }
        
        expected_interval = timeframe_mapping.get(timeframe, timedelta(minutes=5))
        gaps = []
        
        for i in range(1, len(df)):
            actual_gap = df.index[i] - df.index[i-1]
            
            # Allow for some tolerance (market closures, weekends)
            tolerance_multiplier = 3 if timeframe in ['1day'] else 2
            max_expected_gap = expected_interval * tolerance_multiplier
            
            if actual_gap > max_expected_gap:
                gaps.append((df.index[i-1], df.index[i]))
        
        return gaps
    
    def check_data_delay(self, df: pd.DataFrame, timeframe: str) -> Tuple[float, float]:
        """Calculate data delay compared to current time."""
        if df.empty:
            return float('inf'), self.expected_delays.get(timeframe, 300)
        
        latest_bar = df.index[-1]
        current_time = datetime.now()
        
        # If latest bar is timezone-naive, assume UTC
        if latest_bar.tzinfo is None:
            latest_bar = pytz.UTC.localize(latest_bar)
        if current_time.tzinfo is None:
            current_time = pytz.UTC.localize(current_time)
        
        delay_seconds = (current_time - latest_bar).total_seconds()
        expected_delay = self.expected_delays.get(timeframe, 300)
        
        return delay_seconds, expected_delay
    
    def analyze_data_quality(self, symbol: str, timeframe: str, 
                           reference_time: Optional[datetime] = None) -> DataQualityMetrics:
        """Perform comprehensive data quality analysis."""
        
        logger.info(f"Analyzing data quality for {symbol} {timeframe}")
        
        try:
            # Fetch data using same logic as Layer1
            end_time = reference_time or datetime.now()
            start_time = end_time - timedelta(days=3)  # 3 days lookback (reasonable for testing)
            
            df = self.schwab_provider.get_historical_data(
                symbol=symbol,
                start_date=start_time,
                end_date=end_time,
                timeframe=timeframe
            )
            
            if df.empty:
                logger.error(f"No data received for {symbol} {timeframe}")
                return DataQualityMetrics(
                    symbol=symbol,
                    timeframe=timeframe,
                    total_bars=0,
                    latest_bar_timestamp=datetime.min,
                    delay_seconds=float('inf'),
                    expected_delay_seconds=self.expected_delays.get(timeframe, 300),
                    gaps_count=0,
                    duplicates_count=0,
                    zero_volume_count=0,
                    ohlc_consistency_errors=0,
                    timezone_issues=0,
                    data_completeness_percent=0.0,
                    is_market_hours=False,
                    assessment="CRITICAL"
                )
            
            # Perform quality checks
            latest_timestamp = df.index[-1]
            
            # Check delay
            delay_seconds, expected_delay = self.check_data_delay(df, timeframe)
            
            # Detect gaps
            gaps = self.detect_gaps(df, timeframe)
            
            # Check for duplicates
            duplicates = df.index.duplicated().sum()
            
            # Check for zero volume
            zero_volume = (df['volume'] == 0).sum()
            
            # Validate OHLC consistency
            ohlc_errors = self.validate_ohlc_consistency(df)
            
            # Check timezone consistency
            timezone_issues = 0
            if any(pd.isna(df.index)):
                timezone_issues += 1
            
            # Check if we're in market hours
            is_market_open = self.is_market_open(symbol, latest_timestamp)
            
            # Calculate data completeness based on expected vs actual bars
            expected_bars = self._calculate_expected_bars(start_time, end_time, timeframe, symbol)
            completeness = min(100.0, (len(df) / max(1, expected_bars)) * 100)
            
            # Overall assessment
            assessment = self._assess_data_quality(
                delay_seconds, expected_delay, len(gaps), len(ohlc_errors), 
                completeness, is_market_open
            )
            
            return DataQualityMetrics(
                symbol=symbol,
                timeframe=timeframe,
                total_bars=len(df),
                latest_bar_timestamp=latest_timestamp,
                delay_seconds=delay_seconds,
                expected_delay_seconds=expected_delay,
                gaps_count=len(gaps),
                duplicates_count=duplicates,
                zero_volume_count=zero_volume,
                ohlc_consistency_errors=len(ohlc_errors),
                timezone_issues=timezone_issues,
                data_completeness_percent=completeness,
                is_market_hours=is_market_open,
                assessment=assessment
            )
            
        except Exception as e:
            logger.error(f"Data quality analysis failed: {e}")
            raise
    
    def _calculate_expected_bars(self, start: datetime, end: datetime, 
                               timeframe: str, symbol: str) -> int:
        """Calculate expected number of bars for the time period."""
        
        # Basic calculation - this could be made more sophisticated
        # by accounting for market hours and holidays
        total_minutes = (end - start).total_seconds() / 60
        
        timeframe_minutes = {
            '1minute': 1,
            '5minute': 5,
            '15minute': 15, 
            '30minute': 30,
            '60minute': 60,
            '240minute': 240,
            '1day': 1440  # 24 hours
        }
        
        interval_minutes = timeframe_minutes.get(timeframe, 5)
        
        # Rough estimate accounting for market hours
        instrument_type = self.detect_instrument_type(symbol)
        if instrument_type == 'stocks':
            # ~6.5 hours per day, 5 days per week
            trading_ratio = 0.19  # (6.5 * 5) / (24 * 7)
        else:
            # Forex/futures trade ~24/5 + Sunday evening 
            trading_ratio = 0.83  # ~5.8 days / 7 days
        
        expected = int((total_minutes * trading_ratio) / interval_minutes)
        return expected
    
    def _assess_data_quality(self, delay: float, expected_delay: float, 
                           gaps: int, ohlc_errors: int, completeness: float,
                           is_market_open: bool) -> str:
        """Assess overall data quality based on metrics."""
        
        # Critical issues
        if delay == float('inf') or completeness < 50:
            return "CRITICAL"
        
        # Poor quality indicators
        if (delay > expected_delay * 3 or 
            ohlc_errors > 0 or 
            gaps > 10 or 
            completeness < 80):
            return "POOR"
        
        # Delayed but functional
        if delay > expected_delay * 1.5:
            return "DELAYED"
        
        return "GOOD"
    
    def run_comprehensive_check(self, symbol: str, timeframes: List[str],
                              reference_time: Optional[datetime] = None) -> Dict[str, DataQualityMetrics]:
        """Run comprehensive data quality check across multiple timeframes."""
        
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            for timeframe in timeframes:
                task = progress.add_task(f"Checking {timeframe}...", total=None)
                
                try:
                    metrics = self.analyze_data_quality(symbol, timeframe, reference_time)
                    results[timeframe] = metrics
                    progress.update(task, description=f"✅ {timeframe} - {metrics.assessment}")
                    
                except Exception as e:
                    logger.error(f"Failed to check {timeframe}: {e}")
                    progress.update(task, description=f"❌ {timeframe} - ERROR")
                
                progress.remove_task(task)
        
        return results
    
    def display_results(self, results: Dict[str, DataQualityMetrics]):
        """Display data quality results in a formatted table."""
        
        table = Table(title="📊 Schwab OHLC Data Quality Report", show_header=True, header_style="bold blue")
        
        table.add_column("Timeframe", style="cyan", width=10)
        table.add_column("Status", width=10)
        table.add_column("Bars", justify="right", width=8)
        table.add_column("Latest Bar", width=19)
        table.add_column("Delay (sec)", justify="right", width=12)
        table.add_column("Gaps", justify="right", width=6)
        table.add_column("OHLC Errors", justify="right", width=12)
        table.add_column("Completeness", justify="right", width=12)
        
        for timeframe, metrics in results.items():
            # Status color coding
            status_colors = {
                "GOOD": "green",
                "DELAYED": "yellow", 
                "POOR": "orange",
                "CRITICAL": "red"
            }
            status_color = status_colors.get(metrics.assessment, "white")
            
            # Format delay
            if metrics.delay_seconds == float('inf'):
                delay_str = "∞"
            else:
                delay_str = f"{metrics.delay_seconds:.0f}"
                if metrics.delay_seconds > metrics.expected_delay_seconds:
                    delay_str += " ⚠️"
            
            # Format latest bar timestamp
            latest_str = metrics.latest_bar_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            table.add_row(
                timeframe,
                f"[{status_color}]{metrics.assessment}[/{status_color}]",
                str(metrics.total_bars),
                latest_str,
                delay_str,
                str(metrics.gaps_count),
                str(metrics.ohlc_consistency_errors),
                f"{metrics.data_completeness_percent:.1f}%"
            )
        
        self.console.print(table)
        
        # Summary recommendations
        critical_issues = [tf for tf, m in results.items() if m.assessment == "CRITICAL"]
        poor_issues = [tf for tf, m in results.items() if m.assessment == "POOR"]
        delayed_issues = [tf for tf, m in results.items() if m.assessment == "DELAYED"]
        
        if critical_issues:
            self.console.print(Panel(
                f"🚨 CRITICAL: {', '.join(critical_issues)} - No usable data received",
                title="Critical Issues",
                border_style="red"
            ))
        
        if poor_issues:
            self.console.print(Panel(
                f"⚠️ POOR QUALITY: {', '.join(poor_issues)} - Data integrity issues detected",
                title="Quality Issues", 
                border_style="orange"
            ))
        
        if delayed_issues:
            self.console.print(Panel(
                f"🐌 DELAYED: {', '.join(delayed_issues)} - Data is significantly delayed",
                title="Timing Issues",
                border_style="yellow"
            ))
    
    def save_detailed_report(self, results: Dict[str, DataQualityMetrics], 
                           output_path: Path):
        """Save detailed quality report to JSON file."""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_timeframes": len(results),
                "good_quality": len([m for m in results.values() if m.assessment == "GOOD"]),
                "delayed": len([m for m in results.values() if m.assessment == "DELAYED"]),
                "poor_quality": len([m for m in results.values() if m.assessment == "POOR"]),
                "critical": len([m for m in results.values() if m.assessment == "CRITICAL"])
            },
            "details": {}
        }
        
        for timeframe, metrics in results.items():
            report["details"][timeframe] = {
                "symbol": metrics.symbol,
                "timeframe": metrics.timeframe,
                "assessment": metrics.assessment,
                "total_bars": metrics.total_bars,
                "latest_bar": metrics.latest_bar_timestamp.isoformat(),
                "delay_seconds": metrics.delay_seconds,
                "expected_delay_seconds": metrics.expected_delay_seconds,
                "gaps_count": metrics.gaps_count,
                "duplicates_count": metrics.duplicates_count,
                "zero_volume_count": metrics.zero_volume_count,
                "ohlc_consistency_errors": metrics.ohlc_consistency_errors,
                "timezone_issues": metrics.timezone_issues,
                "data_completeness_percent": metrics.data_completeness_percent,
                "is_market_hours": metrics.is_market_hours
            }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Detailed report saved to {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Schwab OHLC Data Quality Checker")
    parser.add_argument("--symbol", required=True, help="Symbol to check (e.g., EURUSD, /ES)")
    parser.add_argument("--timeframe", help="Single timeframe to check")
    parser.add_argument("--timeframes", nargs="+", 
                       default=["1minute", "5minute", "15minute", "30minute", "60minute"],
                       help="List of timeframes to check")
    parser.add_argument("--reference-time", help="Reference time (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--output", help="Save detailed report to JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level, format="{time:HH:mm:ss} | {level} | {message}")
    
    # Parse reference time if provided
    reference_time = None
    if args.reference_time:
        try:
            reference_time = datetime.strptime(args.reference_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"❌ Invalid reference time format. Use: YYYY-MM-DD HH:MM:SS")
            sys.exit(1)
    
    # Determine timeframes to check
    timeframes = [args.timeframe] if args.timeframe else args.timeframes
    
    # Initialize checker and run analysis
    checker = SchwabDataQualityChecker()
    
    try:
        # Test connection first
        print("🔌 Testing Schwab API connection...")
        if not checker.schwab_client.get_quotes(["SPY"]):
            print("❌ Failed to connect to Schwab API")
            sys.exit(1)
        print("✅ Schwab API connection successful")
        
        # Run comprehensive check
        print(f"\n📊 Analyzing data quality for {args.symbol}...")
        results = checker.run_comprehensive_check(args.symbol, timeframes, reference_time)
        
        # Display results
        print()
        checker.display_results(results)
        
        # Save detailed report if requested
        if args.output:
            output_path = Path(args.output)
            checker.save_detailed_report(results, output_path)
            print(f"\n💾 Detailed report saved to {output_path}")
        
        # Exit with appropriate code
        critical_count = len([m for m in results.values() if m.assessment == "CRITICAL"])
        poor_count = len([m for m in results.values() if m.assessment == "POOR"])
        
        if critical_count > 0:
            sys.exit(2)  # Critical issues
        elif poor_count > 0:
            sys.exit(1)  # Quality issues
        else:
            sys.exit(0)  # All good
            
    except Exception as e:
        logger.error(f"Data quality check failed: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()