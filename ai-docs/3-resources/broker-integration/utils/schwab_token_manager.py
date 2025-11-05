"""
Schwab Token Manager

This module provides utilities for managing Schwab API tokens, including automatic
token refresh when they expire.

Usage:
    from src.utils.schwab_token_manager import with_token_refresh

    @with_token_refresh
    def my_function_that_uses_schwab_api():
        # Function that uses the Schwab API
        ...
"""
import functools
import subprocess
import sys
import os
from typing import Callable, Any, TypeVar, cast
from rich.console import Console
from rich.panel import Panel

console = Console()

# Type variable for the decorator
F = TypeVar('F', bound=Callable[..., Any])

def with_token_refresh(func: F) -> F:
    """
    Decorator that automatically refreshes Schwab API tokens when they expire.
    
    This decorator wraps a function that uses the Schwab API and automatically
    refreshes the tokens if they expire during execution. It then retries the
    original function with the new tokens.
    
    Args:
        func: The function to wrap
        
    Returns:
        The wrapped function
        
    Example:
        @with_token_refresh
        def get_market_data(symbol):
            # Function that uses the Schwab API
            ...
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            # Try to execute the original function
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            
            # Check if the error is related to token expiration
            if "refresh token expired" in error_message.lower() or "token expired" in error_message.lower():
                console.print(Panel.fit(
                    "[yellow]Schwab API tokens have expired. Running token refresh utility...[/yellow]",
                    title="Token Refresh Required",
                    border_style="yellow"
                ))
                
                # Run the token refresh utility
                refresh_tokens()
                
                # Retry the function with new tokens
                console.print("[cyan]Retrying operation with new tokens...[/cyan]")
                return func(*args, **kwargs)
            else:
                # For other errors, re-raise
                raise
    
    return cast(F, wrapper)

def refresh_tokens() -> bool:
    """
    Run the token refresh utility script.
    
    Returns:
        bool: True if tokens were refreshed successfully, False otherwise
    """
    try:
        console.print("[cyan]Launching Schwab token refresh utility...[/cyan]")
        
        # Get the path to the refresh_schwab_tokens.py script
        # It should be in the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        refresh_script_path = os.path.join(project_root, "refresh_schwab_tokens.py")
        
        if not os.path.exists(refresh_script_path):
            console.print(f"[red]Token refresh script not found at {refresh_script_path}[/red]")
            return False
        
        # Run the refresh_schwab_tokens.py script
        result = subprocess.run(
            [sys.executable, refresh_script_path],
            check=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green]Token refresh completed successfully![/green]")
            return True
        else:
            console.print(f"[red]Token refresh failed with exit code {result.returncode}[/red]")
            return False
            
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running token refresh utility: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Unexpected error during token refresh: {e}[/red]")
        return False

# Example usage
if __name__ == "__main__":
    # This is just an example to demonstrate how to use the decorator
    @with_token_refresh
    def example_function():
        """Example function that uses the Schwab API"""
        from src.brokers.schwab import SchwabClient as SchwabApi
        
        api = SchwabApi()
        # This will trigger token refresh if tokens are expired
        quotes = api.get_quotes(["SPY"])
        return quotes
    
    # Call the example function
    try:
        result = example_function()
        console.print(f"[green]Function executed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
