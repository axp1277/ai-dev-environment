"""Authentication command implementations for Schwab CLI"""
import os, subprocess, sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
from src.brokers.schwab.auth import SchwabAuth

console = Console()

def refresh_tokens_command():
    """Execute token refresh process"""
    script_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")), "refresh_schwab_tokens.py")
    console.print(Panel.fit("[cyan]Starting Schwab Token Refresh Process[/cyan]", title="Token Refresh", border_style="cyan"))
    handlers = {subprocess.CalledProcessError: lambda e: console.print(f"[red]Error running token refresh utility: {e}[/red]", "[yellow]Try running: python refresh_schwab_tokens.py[/yellow]"), Exception: lambda e: console.print(f"[red]Unexpected error during token refresh: {e}[/red]")}
    try: {True: lambda: (console.print("[cyan]Launching interactive token refresh utility...[/cyan]"), subprocess.run([sys.executable, script_path], check=True, text=True), console.print("[green]✓ Token refresh completed successfully![/green]")), False: lambda: (console.print(f"[red]Token refresh script not found at {script_path}[/red]", "[yellow]Attempting alternative token refresh method...[/yellow]"), _fallback_refresh())}[os.path.exists(script_path)]()
    except Exception as e: handlers.get(type(e), handlers[Exception])(e)

def _fallback_refresh():
    """Fallback token refresh using SchwabAuth"""
    try: access_token, refresh_token = SchwabAuth().refresh_tokens(); console.print(Panel.fit(f"[green]✓ Tokens refreshed successfully![/green]\n\nAccess Token: {access_token[:10]}...{access_token[-10:]}\nRefresh Token: {refresh_token[:10]}...{refresh_token[-10:]}\n\nTokens have been updated in your .env file.", title="Success", border_style="green"))
    except Exception as e: console.print(f"[red]Token refresh failed: {e}[/red]", "[yellow]You may need to run the full OAuth flow manually[/yellow]")

def token_status_command():
    """Check current token status and validity"""
    try: from dotenv import load_dotenv; env_path = os.path.join(os.getcwd(), '.env'); return {True: lambda: console.print("[red]No .env file found in project root[/red]"), False: lambda: _process_tokens(env_path, load_dotenv(env_path))}[not os.path.exists(env_path)]()
    except Exception as e: console.print(f"[red]Error checking token status: {e}[/red]")

def _process_tokens(env_path, _):
    """Process and display token status"""
    tokens, descriptions = {name: os.getenv(name) for name in ['APP_KEY', 'APP_SECRET', 'ACCESS_TOKEN', 'REFRESH_TOKEN']}, {"APP_KEY": "Client application key", "APP_SECRET": "Client application secret", "ACCESS_TOKEN": "API access token", "REFRESH_TOKEN": "Token refresh credential"}
    table = Table(title="Schwab API Token Status")
    [table.add_column(col, style=style) for col, style in [("Credential", "cyan"), ("Status", "green"), ("Details", "yellow")]]
    [table.add_row(name, *({True: lambda: ("[green]✓ Present[/green]", f"{descriptions[name]} ({len(value)} chars)" + (f" - {value[:8]}...{value[-8:]}" * (name in ["ACCESS_TOKEN", "REFRESH_TOKEN"]))), False: lambda: ("[red]✗ Missing[/red]", f"{descriptions[name]} - Not configured")}[bool(value)]())) for name, value in tokens.items()]
    console.print(table); _test_connection(all(tokens.values())); _show_env_modified(env_path)

_test_connection = lambda all_present: console.print("\n[yellow]⚠ Cannot test API connection - missing credentials[/yellow]", "[cyan]Please ensure all required environment variables are set in .env file[/cyan]") if not all_present else (console.print("\n[cyan]Testing API connection...[/cyan]"), _perform_api_test())[-1]

def _perform_api_test():
    """Perform API connection test"""
    try: from src.brokers.schwab.client import SchwabClient; quotes = SchwabClient().get_quotes(["SPY"], fields=["quote"]); return console.print("[green]✓ API connection successful[/green]", f"[dim]Test quote retrieved for SPY: ${quotes['SPY'].quote.lastPrice:.2f}[/dim]") if quotes else console.print("[yellow]⚠ API connection failed - no data returned[/yellow]")
    except Exception as e: error_msg = str(e).lower(); return console.print("[yellow]⚠ Tokens appear to be expired[/yellow]", "[cyan]Run 'schwab-cli auth refresh' to refresh tokens[/cyan]") if any(term in error_msg for term in ["token expired", "unauthorized"]) else console.print(f"[red]✗ API connection failed: {e}[/red]")

_show_env_modified = lambda env_path: console.print(f"\n[dim].env file last modified: {datetime.fromtimestamp(os.stat(env_path).st_mtime).strftime('%Y-%m-%d %H:%M:%S')}[/dim]") or None