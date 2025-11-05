#!/usr/bin/env python3
"""
Schwab CLI - Unified command-line interface for Schwab API operations

This CLI consolidates all Schwab functionality into a single, easy-to-use interface
that supports both interactive use and programmatic access by AI agents.

Usage:
    uv run src/brokers/schwab/cli.py --help
    uv run src/brokers/schwab/cli.py auth refresh
    uv run src/brokers/schwab/cli.py quotes --symbols SPY,AAPL
    uv run src/brokers/schwab/cli.py historical --symbol /ESU25 --days 5
"""

import click
from rich.console import Console
from rich.panel import Panel
from loguru import logger

console = Console()

@click.group()
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx):
    """
    Schwab CLI - Unified interface for Schwab API operations
    
    This tool provides easy access to Schwab API functionality including:
    - Authentication and token management
    - Real-time quotes for stocks, futures, and options
    - Historical data retrieval
    - Account positions and orders
    - Connection testing and diagnostics
    """
    ctx.ensure_object(dict)
    
    # Configure logging for CLI
    logger.remove()
    logger.add(
        "schwab_cli.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

@cli.group()
def auth():
    """Authentication and token management commands"""
    pass

@cli.group()
def quotes():
    """Real-time quote commands for stocks, futures, and options"""
    pass

@cli.group()
def historical():
    """Historical data retrieval commands"""
    pass

@cli.group()
def test():
    """Connection testing and diagnostic commands"""
    pass

@cli.group()
def positions():
    """Account positions and order management commands"""
    pass

@auth.command()
def refresh():
    """Refresh Schwab API tokens"""
    try:
        from src.brokers.schwab.commands.auth import refresh_tokens_command
        refresh_tokens_command()
    except ImportError as e:
        console.print(f"[red]Error importing auth commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@auth.command()
def status():
    """Check token status and validity"""
    try:
        from src.brokers.schwab.commands.auth import token_status_command
        token_status_command()
    except ImportError as e:
        console.print(f"[red]Error importing auth commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@quotes.command()
@click.option('--symbols', '-s', required=True, help='Comma-separated list of symbols (e.g., SPY,AAPL,/ESU25)')
@click.option('--fields', '-f', default='quote', help='Quote fields to retrieve (quote,fundamental,extended,reference,regular)')
def get(symbols, fields):
    """Get real-time quotes for symbols"""
    try:
        from src.brokers.schwab.commands.quotes import get_quotes_command
        symbol_list = [s.strip() for s in symbols.split(',')]
        field_list = [f.strip() for f in fields.split(',')]
        get_quotes_command(symbol_list, field_list)
    except ImportError as e:
        console.print(f"[red]Error importing quotes commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@historical.command()
@click.option('--symbol', '-s', required=True, help='Symbol to get historical data for')
@click.option('--days', '-d', default=5, type=int, help='Number of days of historical data')
@click.option('--timeframe', '-t', default='15minute', help='Data timeframe (1minute, 5minute, 15minute, 30minute, 1day)')
def get(symbol, days, timeframe):
    """Get historical price data for a symbol"""
    try:
        from src.brokers.schwab.commands.historical import get_historical_command
        get_historical_command(symbol, days, timeframe)
    except ImportError as e:
        console.print(f"[red]Error importing historical commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@test.command()
def connection():
    """Test connection to Schwab API"""
    try:
        from src.brokers.schwab.commands.test import test_connection_command
        test_connection_command()
    except ImportError as e:
        console.print(f"[red]Error importing test commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@test.command()
def provider():
    """Test the data provider functionality"""
    try:
        from src.brokers.schwab.commands.test import test_provider_command
        test_provider_command()
    except ImportError as e:
        console.print(f"[red]Error importing test commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@positions.command()
@click.option('--symbol', '-s', help='Filter positions by symbol')
def get(symbol):
    """Get current positions"""
    try:
        from src.brokers.schwab.commands.positions import get_positions_command
        get_positions_command(symbol)
    except ImportError as e:
        console.print(f"[red]Error importing positions commands: {e}[/red]")
        console.print("[yellow]This feature is still being implemented[/yellow]")

@cli.command()
def examples():
    """Show usage examples"""
    examples_text = """
# Authentication
schwab auth refresh        # Refresh tokens
schwab auth status         # Check token status

# Quotes
schwab quotes get --symbols SPY,AAPL
schwab quotes get --symbols /ESU25 --fields quote,fundamental

# Historical Data
schwab historical get --symbol SPY --days 5 --timeframe 15minute
schwab historical get --symbol /ESU25 --days 3 --timeframe 5minute

# Testing
schwab test connection     # Test API connection
schwab test provider       # Test data provider

# Positions
schwab positions get       # Get all positions
schwab positions get --symbol SPY  # Get SPY positions only

# Alternative (if shortcut not available)
uv run src/brokers/schwab/cli.py --help
"""
    
    console.print(Panel.fit(
        examples_text,
        title="Schwab CLI Usage Examples",
        border_style="green"
    ))

if __name__ == '__main__':
    cli()