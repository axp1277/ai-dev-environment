"""Positions command implementations for Schwab CLI"""
from typing import Optional
from rich.console import Console
from rich.table import Table
from src.brokers.schwab.client import SchwabClient
from src.utils.schwab_token_manager import with_token_refresh

console = Console()

@with_token_refresh
def get_positions_command(symbol: Optional[str] = None):
    """Get current positions with optional symbol filter"""
    client = SchwabClient()
    positions = client.get_open_positions(symbol)
    
    if not positions:
        console.print(f"[yellow]No positions found{f' for {symbol}' if symbol else ''}[/yellow]")
        return
    
    # Create positions table
    table = Table(title=f"Open Positions{f' - {symbol}' if symbol else ''} ({len(positions)} total)")
    [table.add_column(col, style=style, justify="right" if "Price" in col or "P&L" in col or "Qty" in col else "left")
     for col, style in [("Symbol", "cyan"), ("Qty", "green"), ("Avg Price", "yellow"), 
                       ("Market Value", "blue"), ("P&L", "red"), ("P&L %", "magenta")]]
    
    # Add position rows with color-coded P&L
    [table.add_row(
        pos.instrument.symbol,
        f"{pos.longQuantity:,.0f}",
        f"${pos.averagePrice:.2f}",
        f"${pos.marketValue:,.2f}",
        f"[{'green' if pos.currentDayProfitLoss >= 0 else 'red'}]${pos.currentDayProfitLoss:+,.2f}[/{'green' if pos.currentDayProfitLoss >= 0 else 'red'}]",
        f"[{'green' if pos.currentDayProfitLossPercentage >= 0 else 'red'}]{pos.currentDayProfitLossPercentage:+.2f}%[/{'green' if pos.currentDayProfitLossPercentage >= 0 else 'red'}]"
     ) for pos in positions]
    
    console.print(table)
    
    # Summary statistics
    total_value = sum(pos.marketValue for pos in positions)
    total_pnl = sum(pos.currentDayProfitLoss for pos in positions)
    console.print(f"\n[cyan]Total Market Value:[/cyan] ${total_value:,.2f} | "
                 f"[cyan]Total P&L:[/cyan] [{'green' if total_pnl >= 0 else 'red'}]${total_pnl:+,.2f}[/{'green' if total_pnl >= 0 else 'red'}]")