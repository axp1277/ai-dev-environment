"""Historical data command implementations for Schwab CLI"""
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from src.brokers.schwab.client import SchwabClient
from src.utils.schwab_token_manager import with_token_refresh

console = Console()

@with_token_refresh
def get_historical_command(symbol: str, days: int, timeframe: str):
    """Get historical price data with optimized display"""
    client = SchwabClient()
    
    # Determine if symbol is futures or equity and call appropriate method
    history = (client.get_futures_price_history if symbol.startswith('/') else client.get_price_history)(
        symbol=symbol,
        period_type="day",
        period=min(days, 10),  # Schwab API limit
        frequency_type="minute" if "minute" in timeframe else "daily",
        frequency=int(timeframe.replace("minute", "")) if "minute" in timeframe else 1,
        need_extended_hours_data=symbol.startswith('/'),
        need_previous_close=True
    )
    
    # Create and populate table with candle data
    table = Table(title=f"{symbol} Historical Data ({timeframe}, {days} days)")
    [table.add_column(col, style=style, justify="right" if style != "cyan" else "left") 
     for col, style in [("DateTime", "cyan"), ("Open", "green"), ("High", "yellow"), 
                       ("Low", "red"), ("Close", "blue"), ("Volume", "magenta")]]
    
    # Add candle rows with formatted data
    [table.add_row(
        datetime.fromtimestamp(candle.datetime / 1000).strftime("%m/%d %H:%M"),
        f"${candle.open:.2f}", f"${candle.high:.2f}", f"${candle.low:.2f}",
        f"${candle.close:.2f}", f"{candle.volume:,}"
     ) for candle in history.candles[-50:]]  # Show last 50 candles
    
    console.print(table)
    
    # Display summary statistics
    candles = history.candles
    price_change = candles[-1].close - candles[0].open if candles else 0
    pct_change = (price_change / candles[0].open * 100) if candles and candles[0].open else 0
    
    console.print(f"\n[cyan]Summary:[/cyan] {len(candles)} data points | "
                 f"Change: [{'green' if price_change >= 0 else 'red'}]${price_change:+.2f} "
                 f"({pct_change:+.2f}%)[/{'green' if price_change >= 0 else 'red'}]")