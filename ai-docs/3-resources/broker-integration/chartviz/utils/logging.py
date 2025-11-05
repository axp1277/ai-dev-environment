"""Logging configuration for ChartViz using Loguru and Rich."""
import sys
from pathlib import Path
from typing import Any, Dict

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

console = Console()

def setup_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    """Configure Loguru with Rich handler for enhanced output."""
    logger.remove()
    
    logger.add(
        RichHandler(console=console, rich_tracebacks=True),
        format="{message}",
        level=level
    )
    
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="10 MB"
        )

def log_info(message: str, **kwargs: Any) -> None:
    """Log info message with optional Rich formatting."""
    if kwargs:
        console.print(f"[green]ℹ[/green] {message}", **kwargs)
    else:
        logger.info(message)

def log_debug(message: str, data: Dict[str, Any] | None = None) -> None:
    """Log debug message with optional data."""
    if data:
        logger.debug(f"{message} | {data}")
    else:
        logger.debug(message)

def log_error(message: str, exception: Exception | None = None) -> None:
    """Log error message with optional exception."""
    if exception:
        logger.exception(f"{message}: {exception}")
    else:
        logger.error(message)

def log_success(message: str) -> None:
    """Log success message with Rich formatting."""
    console.print(f"[bold green]✓[/bold green] {message}")

def log_warning(message: str) -> None:
    """Log warning message."""
    logger.warning(message)
    
def log_chart_creation(chart_type: str, elements: int) -> None:
    """Log chart creation details."""
    console.print(f"[cyan]📊 Creating {chart_type} chart with {elements} elements[/cyan]")

def log_export(format: str, path: Path) -> None:
    """Log export operation."""
    console.print(f"[green]💾 Exported as {format} to:[/green] {path}")