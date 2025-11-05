"""Standalone ChartViz CLI entry point to avoid tool registry import conflicts."""

import sys
import os

def main():
    """Standalone entry point that avoids importing the full tools package."""
    # Add the chartviz directory to path
    chartviz_dir = os.path.dirname(os.path.abspath(__file__))
    if chartviz_dir not in sys.path:
        sys.path.insert(0, chartviz_dir)
    
    # Import and run CLI directly
    try:
        from cli import cli
        cli()
    except ImportError as e:
        # Fallback to direct module import
        import importlib.util
        cli_path = os.path.join(chartviz_dir, 'cli.py')
        spec = importlib.util.spec_from_file_location("chartviz_cli", cli_path)
        cli_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli_module)
        cli_module.cli()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()