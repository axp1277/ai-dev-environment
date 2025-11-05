"""ChartViz CLI - Single file managing all functionality."""

import sys
from pathlib import Path
from typing import Optional, Tuple, List

import click
import pandas as pd

# Handle imports for both module and direct execution
try:
    from .utils.logging import log_error, log_info, log_success, setup_logging
except ImportError:
    # Direct execution fallback
    sys.path.insert(0, str(Path(__file__).parent))
    from utils.logging import log_error, log_info, log_success, setup_logging


# ============= MAIN CLI GROUP =============
@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output except errors')
@click.option('--log-file', type=click.Path(), help='Log file path')
@click.version_option(version='1.0.0', prog_name='ChartViz')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, log_file: str) -> None:
    """ChartViz - Financial Chart Visualization Framework.
    
    Create highly customizable financial candlestick charts with layered
    visual elements for trading analysis and client presentations.
    """
    ctx.ensure_object(dict)
    
    # Set up logging based on options
    if quiet:
        log_level = "ERROR"
    elif verbose:
        log_level = "DEBUG"
    else:
        log_level = "INFO"
    
    log_file_path = Path(log_file) if log_file else None
    setup_logging(log_level, log_file_path)
    
    # Store CLI options in context for subcommands
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['log_file'] = log_file_path
    
    if not quiet:
        log_info("ChartViz CLI initialized")


@cli.command()
def version():
    """Show version information."""
    click.echo("ChartViz 1.0.0")
    click.echo("Financial Chart Visualization Framework")


# ============= DATA PROVIDER COMMANDS =============
@cli.command(name='from-db')
@click.option('--symbol', '-s', required=True, help='Symbol to chart')
@click.option('--timeframe', '-tf', default='5minute', 
              type=click.Choice(['1minute', '5minute', '15minute', '60minute']),
              help='Timeframe for data')
@click.option('--days', '-d', default=5, help='Days of historical data (unused for SQLite but kept for consistency)')
@click.option('--limit', '-l', type=int, help='Maximum number of bars')
@click.option('--db-path', default='data/market_data.db', help='SQLite database path')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--theme', help='Chart theme to apply')
@click.option('--width', type=int, help='Chart width in pixels')
@click.option('--height', type=int, help='Chart height in pixels')
@click.option('--show', is_flag=True, help='Show chart interactively')
@click.pass_context
def from_database(ctx: click.Context, symbol: str, timeframe: str, days: int, limit: Optional[int], 
                  db_path: str, output: str, theme: Optional[str], width: Optional[int], 
                  height: Optional[int], show: bool):
    """Create chart from SQLite database."""
    try:
        try:
            from .data import create_provider
            from .config import ConfigLoader, ThemeRegistry
            from .plotting import Chart, ChartExporter
        except ImportError:
            # Direct execution fallback
            from data import create_provider
            from config import ConfigLoader, ThemeRegistry
            from plotting import Chart, ChartExporter
        
        # Create SQLite provider
        data_provider = create_provider('sqlite', db_path=db_path)
        
        # Validate connection
        if not data_provider.validate_connection():
            raise click.ClickException(f"Cannot connect to SQLite database: {db_path}")
        
        # Fetch data
        if not ctx.obj['quiet']:
            click.echo(f"Fetching {symbol} {timeframe} from SQLite database...")
        
        df = data_provider.get_ohlcv(symbol, timeframe, days, limit)
        
        if not ctx.obj['quiet']:
            click.echo(f"Retrieved {len(df)} bars")
        
        # Create chart
        config_loader = ConfigLoader()
        base_config = config_loader.get_default_config()
        
        if theme:
            theme_registry = ThemeRegistry()
            base_config = theme_registry.apply_theme(theme, base_config)
        
        chart_layout = config_loader.create_chart_layout(base_config)
        
        # Override dimensions if specified
        if width:
            chart_layout.width = width
        if height:
            chart_layout.height = height
        
        chart_title = f"{symbol} - {timeframe} (Historical)"
        chart_obj = Chart(chart_layout, title=chart_title)
        candlestick_config = config_loader.create_candlestick(base_config)
        chart_obj.add_candlesticks(df, candlestick_config)
        
        # Export
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        exporter = ChartExporter(chart_obj.get_figure())
        if output_path.suffix.lower() == '.html':
            exporter.to_html(output_path)
            # Automatically open HTML files in browser
            _open_html_in_browser(output_path)
        elif output_path.suffix.lower() == '.png':
            exporter.to_png(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() in ['.jpeg', '.jpg']:
            exporter.to_jpeg(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.pdf':
            exporter.to_pdf(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.svg':
            exporter.to_svg(output_path, width=width or 1200, height=height or 600)
        else:
            raise click.ClickException(f"Unsupported format: {output_path.suffix}")
        
        if show:
            chart_obj.show()
        
        log_success(f"Chart created from SQLite: {output}")
        
    except Exception as e:
        log_error("Chart creation failed", e)
        raise click.ClickException(str(e))


@cli.command(name='from-polygon')
@click.option('--symbol', '-s', required=True, help='Symbol to chart')
@click.option('--timeframe', '-tf', default='5minute', 
              type=click.Choice(['1minute', '5minute', '15minute', '60minute']),
              help='Timeframe for data')
@click.option('--days', '-d', default=5, help='Days of historical data to fetch')
@click.option('--limit', '-l', type=int, help='Maximum number of bars to chart')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--theme', help='Chart theme to apply')
@click.option('--width', type=int, help='Chart width in pixels')
@click.option('--height', type=int, help='Chart height in pixels')
@click.option('--show', is_flag=True, help='Show chart interactively')
@click.pass_context
def from_polygon(ctx: click.Context, symbol: str, timeframe: str, days: int, limit: Optional[int], 
                 output: str, theme: Optional[str], width: Optional[int], 
                 height: Optional[int], show: bool):
    """Create chart from Polygon API with auto-persistence to SQLite."""
    try:
        try:
            from .data import create_provider
            from .config import ConfigLoader, ThemeRegistry
            from .plotting import Chart, ChartExporter
        except ImportError:
            # Direct execution fallback
            from data import create_provider
            from config import ConfigLoader, ThemeRegistry
            from plotting import Chart, ChartExporter
        
        # Create Polygon provider
        try:
            data_provider = create_provider('polygon')
        except ValueError as e:
            if 'polygon' in str(e):
                raise click.ClickException("Polygon provider not available. Check that Polygon broker is installed and POLYGON_API_KEY is set.")
            raise
        
        # Validate connection
        if not data_provider.validate_connection():
            raise click.ClickException("Cannot connect to Polygon API or SQLite database. Check POLYGON_API_KEY and database path.")
        
        # Fetch data from API and auto-persist to SQLite
        if not ctx.obj['quiet']:
            click.echo(f"Fetching {symbol} {timeframe} data from Polygon API...")
        
        df = data_provider.get_ohlcv(symbol, timeframe, days, limit)
        
        if not ctx.obj['quiet']:
            click.echo(f"Retrieved {len(df)} bars (auto-saved to SQLite)")
        
        # Create chart (same as from-db command)
        config_loader = ConfigLoader()
        base_config = config_loader.get_default_config()
        
        if theme:
            theme_registry = ThemeRegistry()
            base_config = theme_registry.apply_theme(theme, base_config)
        
        chart_layout = config_loader.create_chart_layout(base_config)
        
        # Override dimensions if specified
        if width:
            chart_layout.width = width
        if height:
            chart_layout.height = height
        
        chart_title = f"{symbol} - {timeframe} (Polygon Live Data)"
        chart_obj = Chart(chart_layout, title=chart_title)
        candlestick_config = config_loader.create_candlestick(base_config)
        chart_obj.add_candlesticks(df, candlestick_config)
        
        # Export
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        exporter = ChartExporter(chart_obj.get_figure())
        if output_path.suffix.lower() == '.html':
            exporter.to_html(output_path)
            # Automatically open HTML files in browser
            _open_html_in_browser(output_path)
        elif output_path.suffix.lower() == '.png':
            exporter.to_png(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() in ['.jpeg', '.jpg']:
            exporter.to_jpeg(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.pdf':
            exporter.to_pdf(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.svg':
            exporter.to_svg(output_path, width=width or 1200, height=height or 600)
        else:
            raise click.ClickException(f"Unsupported format: {output_path.suffix}")
        
        if show:
            chart_obj.show()
        
        log_success(f"Chart created from Polygon (auto-saved to SQLite): {output}")
        
    except Exception as e:
        log_error("Chart creation failed", e)
        raise click.ClickException(str(e))


@cli.command(name='from-schwab')
@click.option('--symbol', '-s', required=True, help='Symbol to chart (e.g., /ES, AAPL)')
@click.option('--timeframe', '-tf', default='5minute', 
              type=click.Choice(['5minute', '15minute', '1day']),
              help='Timeframe for data')
@click.option('--days', '-d', default=None, type=int, help='Days of historical data (auto: 3 for 5min, 5 for 15min, or specify custom)')
@click.option('--limit', '-l', type=int, help='Maximum number of bars to chart')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--theme', help='Chart theme to apply')
@click.option('--width', type=int, help='Chart width in pixels')
@click.option('--height', type=int, help='Chart height in pixels')
@click.option('--show', is_flag=True, help='Show chart interactively')
@click.pass_context
def from_schwab(ctx: click.Context, symbol: str, timeframe: str, days: Optional[int], limit: Optional[int], 
                output: str, theme: Optional[str], width: Optional[int], 
                height: Optional[int], show: bool):
    """Create chart from Schwab API."""
    try:
        try:
            from .data import create_provider
            from .config import ConfigLoader, ThemeRegistry
            from .plotting import Chart, ChartExporter
        except ImportError:
            # Direct execution fallback
            from data import create_provider
            from config import ConfigLoader, ThemeRegistry
            from plotting import Chart, ChartExporter
        
        # Create Schwab provider
        try:
            data_provider = create_provider('schwab')
        except ValueError as e:
            if 'schwab' in str(e):
                raise click.ClickException("Schwab provider not available. Check that Schwab broker is installed and configured.")
            raise
        
        # Validate connection
        if not data_provider.validate_connection():
            raise click.ClickException("Cannot connect to Schwab API. Check authentication and configuration.")
        
        # Auto-adjust days based on timeframe for better SMC analysis
        if days is None:
            timeframe_days_map = {
                '5minute': 3,   # 3 days for 5-minute charts
                '15minute': 5,  # 5 days for 15-minute charts  
                '1day': 30      # 30 days for daily charts
            }
            days = timeframe_days_map.get(timeframe, 5)  # Default to 5 if timeframe not found
        
        # Fetch data from Schwab API
        if not ctx.obj['quiet']:
            click.echo(f"Fetching {symbol} {timeframe} data from Schwab API ({days} days)...")
        
        df = data_provider.get_ohlcv(symbol, timeframe, days, limit)
        
        if df.empty:
            raise click.ClickException(f"No data returned for {symbol} {timeframe}")
        
        if not ctx.obj['quiet']:
            click.echo(f"Retrieved {len(df)} bars")
        
        # Create chart (same pattern as other providers)
        config_loader = ConfigLoader()
        base_config = config_loader.get_default_config()
        
        if theme:
            theme_registry = ThemeRegistry()
            base_config = theme_registry.apply_theme(theme, base_config)
        
        chart_layout = config_loader.create_chart_layout(base_config)
        
        # Override dimensions if specified
        if width:
            chart_layout.width = width
        if height:
            chart_layout.height = height
        
        chart_title = f"{symbol} - {timeframe} (Schwab Live Data)"
        chart_obj = Chart(chart_layout, title=chart_title)
        candlestick_config = config_loader.create_candlestick(base_config)
        chart_obj.add_candlesticks(df, candlestick_config)
        
        # Export
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        exporter = ChartExporter(chart_obj.get_figure())
        if output_path.suffix.lower() == '.html':
            exporter.to_html(output_path)
            # Automatically open HTML files in browser
            _open_html_in_browser(output_path)
        elif output_path.suffix.lower() == '.png':
            exporter.to_png(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() in ['.jpeg', '.jpg']:
            exporter.to_jpeg(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.pdf':
            exporter.to_pdf(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.svg':
            exporter.to_svg(output_path, width=width or 1200, height=height or 600)
        else:
            raise click.ClickException(f"Unsupported format: {output_path.suffix}")
        
        if show:
            chart_obj.show()
        
        log_success(f"Chart created from Schwab: {output}")
        
    except Exception as e:
        log_error("Chart creation failed", e)
        raise click.ClickException(str(e))


@cli.command(name='list-symbols')
@click.option('--provider', default='sqlite', help='Data provider (sqlite, polygon, schwab)')
@click.option('--db-path', default='data/market_data.db', help='SQLite database path')
@click.pass_context
def list_symbols(ctx: click.Context, provider: str, db_path: str):
    """List available symbols from data provider."""
    try:
        try:
            from .data import create_provider
        except ImportError:
            from data import create_provider
        
        # Create provider with appropriate arguments
        provider_kwargs = {}
        if provider == 'sqlite':
            provider_kwargs['db_path'] = db_path
        
        data_provider = create_provider(provider, **provider_kwargs)
        
        if not data_provider.validate_connection():
            raise click.ClickException(f"Cannot connect to {provider} provider")
        
        symbols = data_provider.list_symbols()
        
        if not ctx.obj['quiet']:
            click.echo(f"Available symbols from {data_provider.name} provider:")
        
        # Display in columns
        for i, symbol in enumerate(symbols):
            if i % 5 == 0 and i > 0:
                click.echo()
            click.echo(f"  {symbol:<8}", nl=False)
        click.echo()  # Final newline
        
    except Exception as e:
        log_error("Failed to list symbols", e)
        raise click.ClickException(str(e))


# ============= ORIGINAL CHARTVIZ COMMANDS =============
@cli.command(name='create')
@click.option('--data', '-d', type=click.Path(exists=True), required=True,
              help='OHLC data file (CSV or JSON)')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--title', '-t', default='ChartViz Chart', help='Chart title')
@click.option('--theme', help='Theme name to apply')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--level', multiple=True, help='Add level: price,start_bar[,end_bar,color]')
@click.option('--box', multiple=True, help='Add box: x0,y0,x1,y1[,color]')
@click.option('--trade', multiple=True, help='Add trade: entry_bar,entry_price,exit_bar,exit_price')
@click.option('--width', type=int, help='Chart width in pixels')
@click.option('--height', type=int, help='Chart height in pixels')
@click.option('--show', is_flag=True, help='Show chart interactively')
@click.pass_context
def create_chart(ctx: click.Context, data: str, output: str, title: str, theme: Optional[str],
                config: Optional[str], level: Tuple[str], box: Tuple[str], trade: Tuple[str],
                width: Optional[int], height: Optional[int], show: bool):
    """Create chart from CSV/JSON data file."""
    try:
        try:
            from .config import ConfigLoader, ThemeRegistry
            from .plotting import Chart, ChartExporter
            from .models import Level, Box, Trade
        except ImportError:
            from config import ConfigLoader, ThemeRegistry
            from plotting import Chart, ChartExporter
            from models import Level, Box, Trade
        
        # Load data
        df = _load_data_file(Path(data))
        
        # Load configuration
        config_loader = ConfigLoader()
        if config:
            user_config = config_loader.load_config(Path(config))
            base_config = config_loader.merge_configs(config_loader.get_default_config(), user_config)
        else:
            base_config = config_loader.get_default_config()
        
        # Apply theme
        if theme:
            theme_registry = ThemeRegistry()
            base_config = theme_registry.apply_theme(theme, base_config)
        
        # Create chart
        chart_layout = config_loader.create_chart_layout(base_config)
        if width:
            chart_layout.width = width
        if height:
            chart_layout.height = height
        
        chart_obj = Chart(chart_layout, title=title)
        candlestick_config = config_loader.create_candlestick(base_config)
        chart_obj.add_candlesticks(df, candlestick_config)
        
        # Add levels
        for level_str in level:
            level_obj = _parse_level(level_str)
            chart_obj.add_level(level_obj)
            
        # Add boxes
        for box_str in box:
            box_obj = _parse_box(box_str)
            chart_obj.add_box(box_obj)
            
        # Add trades
        for trade_str in trade:
            trade_obj = _parse_trade(trade_str)
            chart_obj.add_trade(trade_obj)
        
        # Export
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        exporter = ChartExporter(chart_obj.get_figure())
        if output_path.suffix.lower() == '.html':
            exporter.to_html(output_path)
            # Automatically open HTML files in browser
            _open_html_in_browser(output_path)
        elif output_path.suffix.lower() == '.png':
            exporter.to_png(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() in ['.jpeg', '.jpg']:
            exporter.to_jpeg(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.pdf':
            exporter.to_pdf(output_path, width=width or 1200, height=height or 600)
        elif output_path.suffix.lower() == '.svg':
            exporter.to_svg(output_path, width=width or 1200, height=height or 600)
        else:
            raise click.ClickException(f"Unsupported format: {output_path.suffix}")
        
        if show:
            chart_obj.show()
        
        log_success(f"Chart created: {output}")
        
    except Exception as e:
        log_error("Chart creation failed", e)
        raise click.ClickException(str(e))


# ============= CONFIGURATION COMMANDS =============
@cli.group(name='config')
def config_group():
    """Configuration management commands."""
    pass


@config_group.command(name='create')
@click.option('--name', required=True, help='Configuration name')
@click.option('--output', '-o', help='Output file path')
def create_config(name: str, output: Optional[str]):
    """Create new configuration file."""
    try:
        try:
            from .config import ConfigLoader
        except ImportError:
            from config import ConfigLoader
        import yaml
        
        config_loader = ConfigLoader()
        default_config = config_loader.get_default_config()
        
        output_path = Path(output) if output else Path(f"{name}_config.yaml")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("# ChartViz Configuration\n")
            f.write(f"# Generated configuration: {name}\n\n")
            yaml.dump(default_config, f, default_flow_style=False)
        
        log_success(f"Configuration created: {output_path}")
        
    except Exception as e:
        log_error("Configuration creation failed", e)
        raise click.ClickException(str(e))


# ============= THEME COMMANDS =============
@cli.group(name='theme')
def theme_group():
    """Theme management commands."""
    pass


@theme_group.command(name='list')
def list_themes():
    """List available themes."""
    try:
        try:
            from .config import ThemeRegistry
        except ImportError:
            from config import ThemeRegistry
        
        theme_registry = ThemeRegistry()
        themes = theme_registry.list_themes()
        
        click.echo("Available themes:")
        for theme_name in themes:
            click.echo(f"  - {theme_name}")
            
    except Exception as e:
        log_error("Failed to list themes", e)
        raise click.ClickException(str(e))


# ============= UTILITY FUNCTIONS =============
def _open_html_in_browser(html_path: Path) -> None:
    """Open HTML file in the default web browser."""
    import webbrowser
    import os
    
    # Convert to absolute path for better browser compatibility
    abs_path = html_path.resolve()
    
    # Use file:// protocol for local files
    file_url = f"file://{abs_path}"
    
    try:
        webbrowser.open(file_url)
    except Exception as e:
        # Fallback: try opening the file directly
        try:
            webbrowser.open(str(abs_path))
        except Exception:
            # Silent failure - don't crash the CLI if browser can't open
            pass

def _load_data_file(file_path: Path) -> pd.DataFrame:
    """Load OHLC data from CSV or JSON file."""
    if not file_path.exists():
        raise click.ClickException(f"Data file not found: {file_path}")
    
    if file_path.suffix.lower() not in ['.csv', '.json']:
        raise click.ClickException(f"Unsupported file format: {file_path.suffix}")
    
    try:
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:  # JSON
            df = pd.read_json(file_path)
        
        # Validate required columns
        required_cols = ['open', 'high', 'low', 'close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Set index if timestamp column exists
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        elif df.index.name != 'timestamp':
            df.index = range(len(df))
        
        return df
        
    except Exception as e:
        raise click.ClickException(f"Error loading data file {file_path}: {e}")


def _parse_level(level_str: str):
    """Parse level string in format 'price,start_bar,end_bar,color'."""
    try:
        from .models import Level
    except ImportError:
        from models import Level
    try:
        parts = level_str.split(',')
        if len(parts) < 2:
            raise ValueError("Level requires at least price,start_bar")
        
        price = float(parts[0])
        start_bar = int(parts[1])
        end_bar = int(parts[2]) if len(parts) > 2 and parts[2] else None
        color = parts[3] if len(parts) > 3 else None
        
        level_kwargs = {'price': price, 'start_bar': start_bar}
        if end_bar is not None:
            level_kwargs['end_bar'] = end_bar
        if color:
            level_kwargs['color'] = color
            
        return Level(**level_kwargs)
        
    except (ValueError, IndexError) as e:
        raise click.ClickException(f"Invalid level format '{level_str}': {e}")


def _parse_box(box_str: str):
    """Parse box string in format 'x0,y0,x1,y1,color'."""
    try:
        from .models import Box
    except ImportError:
        from models import Box
    try:
        parts = box_str.split(',')
        if len(parts) < 4:
            raise ValueError("Box requires x0,y0,x1,y1")
        
        x0 = int(parts[0])
        y0 = float(parts[1])
        x1 = int(parts[2])
        y1 = float(parts[3])
        fillcolor = parts[4] if len(parts) > 4 else None
        
        box_kwargs = {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}
        if fillcolor:
            box_kwargs['fillcolor'] = fillcolor
            
        return Box(**box_kwargs)
        
    except (ValueError, IndexError) as e:
        raise click.ClickException(f"Invalid box format '{box_str}': {e}")


def _parse_trade(trade_str: str):
    """Parse trade string in format 'entry_bar,entry_price,exit_bar,exit_price'."""
    try:
        from .models import Trade
    except ImportError:
        from models import Trade
    try:
        parts = trade_str.split(',')
        if len(parts) < 4:
            raise ValueError("Trade requires entry_bar,entry_price,exit_bar,exit_price")
        
        entry_bar = int(parts[0])
        entry_price = float(parts[1])
        exit_bar = int(parts[2])
        exit_price = float(parts[3])
        
        return Trade(
            entry_bar=entry_bar,
            entry_price=entry_price,
            exit_bar=exit_bar,
            exit_price=exit_price
        )
        
    except (ValueError, IndexError) as e:
        raise click.ClickException(f"Invalid trade format '{trade_str}': {e}")


# ============= MAIN ENTRY POINT =============
def main():
    """Main entry point for CLI application."""
    try:
        # Avoid loading the full tool registry when running ChartViz CLI directly
        import os
        os.environ.setdefault("CHARTVIZ_STANDALONE", "1")
        cli()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user", err=True)
        sys.exit(1)
    except Exception as e:
        try:
            log_error("Unexpected error occurred", e)
        except:
            # Fallback if logging fails during import issues
            pass
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()