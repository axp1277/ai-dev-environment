"""
Logging Configuration for DocuGen

Configures loguru for structured logging with:
- Console output for interactive use
- File output with rotation (10 days or 10 MB max)
- Contextual logging with module/function information
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_dir: Path = None, level: str = "INFO") -> None:
    """
    Configure loguru logger for DocuGen.

    Args:
        log_dir: Directory for log files (default: ./logs)
        level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Remove default handler
    logger.remove()

    # Console handler - colorized output for interactive use
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )

    # File handler - structured output with rotation
    if log_dir is None:
        log_dir = Path("./logs")

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="10 MB",  # Rotate when file reaches 10 MB
        retention="10 days",  # Keep logs for 10 days
        compression="zip",  # Compress rotated logs
        enqueue=True,  # Thread-safe logging
    )

    logger.info(f"Logger initialized with level={level}, log_dir={log_dir}")


def get_logger():
    """
    Get the configured logger instance.

    Returns:
        loguru.Logger: Configured logger
    """
    return logger


# Example usage patterns for reference
if __name__ == "__main__":
    # Setup logger with default configuration
    setup_logger(level="DEBUG")

    # Example log messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Contextual logging examples
    logger.info("Processing file", file="example.cs", layer="Layer1")

    try:
        # Simulate error for exception logging
        result = 1 / 0
    except Exception as e:
        logger.exception("Error occurred during processing")

    logger.success("Operation completed successfully")
