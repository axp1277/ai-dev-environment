"""CLI interface for Polygon market data fetcher."""
import sys
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.brokers.polygon.core import (
    calculate_date_range,
    create_table,
    fetch_ohlcv,
    insert_bars,
    map_timeframe_for_api,
    map_timeframe_for_table,
)

console = Console()


def main():
    """Main CLI entry point."""
    # Check for help flag
    if len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h']:
        console.print(Panel(
            "[bold blue]Polygon Market Data Fetcher[/bold blue]",
            subtitle="Fetch OHLCV data from Polygon.io API"
        ))
        
        # Usage table
        usage_table = Table(show_header=False, box=None)
        usage_table.add_column("", style="cyan", width=12)
        usage_table.add_column("", style="white")
        usage_table.add_row("Usage:", "polygon <ticker> <timeframe> <bars>")
        usage_table.add_row("", "")
        usage_table.add_row("ticker", "Stock symbol (e.g., SPY, AAPL)")
        usage_table.add_row("timeframe", "Time interval: 1minute, 5minute, 15minute, 60minute")
        usage_table.add_row("bars", "Number of bars to fetch")
        console.print(usage_table)
        
        # Examples panel
        examples = "[cyan]polygon SPY 5minute 500[/cyan]\n[cyan]polygon AAPL 1minute 100[/cyan]"
        console.print(Panel(examples, title="[bold]Examples[/bold]"))
        
        console.print("[yellow]Note:[/yellow] Requires POLYGON_API_KEY in .env file")
        return 0
    
    # Parse command line arguments
    if len(sys.argv) != 4:
        console.print("[red]Usage:[/red] polygon <ticker> <timeframe> <bars>")
        console.print("Try [cyan]'polygon --help'[/cyan] for more information")
        return 1
    
    ticker = sys.argv[1].upper()
    timeframe = sys.argv[2].lower()
    
    try:
        bars = int(sys.argv[3])
    except ValueError:
        console.print(f"[red]Error:[/red] bars must be a number, got [yellow]'{sys.argv[3]}'[/yellow]")
        return 1
    
    # Validate timeframe
    valid_timeframes = ["1minute", "5minute", "15minute", "60minute"]
    if timeframe not in valid_timeframes:
        console.print(f"[red]Error:[/red] invalid timeframe [yellow]'{timeframe}'[/yellow]")
        console.print(f"Valid timeframes: [cyan]{', '.join(valid_timeframes)}[/cyan]")
        return 1
    
    try:
        # Log the operation start
        logger.info(f"Starting data fetch for {ticker} {timeframe} (last {bars} bars)")
        
        # Calculate date range
        from_date, to_date = calculate_date_range(bars, timeframe)
        logger.debug(f"Date range calculated: {from_date} to {to_date}")
        
        # Get API parameters
        multiplier, timespan = map_timeframe_for_api(timeframe)
        logger.debug(f"API parameters: multiplier={multiplier}, timespan={timespan}")
        
        # Show progress
        with console.status(f"[bold blue]Fetching {ticker} data from Polygon.io..."):
            # Fetch data from Polygon
            bars_data = fetch_ohlcv(ticker, multiplier, timespan, from_date, to_date)
            logger.info(f"Received {len(bars_data)} bars from API")
        
        # Create table if needed
        table_timeframe = map_timeframe_for_table(timeframe)
        logger.debug(f"Creating/verifying table: market_data_{ticker}_{table_timeframe}")
        create_table(ticker, table_timeframe)
        
        # Insert data
        with console.status(f"[bold blue]Storing data in database..."):
            inserted = insert_bars(ticker, table_timeframe, bars_data)
        
        logger.info(f"Successfully inserted {inserted} bars into database")
        
        # Success output with rich formatting
        if inserted > 0:
            result_table = Table(show_header=False, box=None)
            result_table.add_column("", style="cyan", width=12)
            result_table.add_column("", style="green")
            result_table.add_row("✓ Ticker:", ticker)
            result_table.add_row("✓ Timeframe:", timeframe)
            result_table.add_row("✓ Bars fetched:", str(inserted))
            result_table.add_row("✓ Table:", f"{ticker}_{table_timeframe}")
            
            console.print(Panel(
                result_table,
                title="[bold green]Data Fetch Completed[/bold green]",
                border_style="green"
            ))
            
            console.print("[yellow]ℹ Note:[/yellow] Data may be delayed 15+ minutes for free Polygon.io accounts")
        else:
            console.print("[yellow]⚠ No new data to insert (may be duplicates)[/yellow]")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during data fetch: {str(e)}")
        console.print(f"[red]✗ Error:[/red] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())