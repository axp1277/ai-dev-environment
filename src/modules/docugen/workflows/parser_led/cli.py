"""
Parser-Led Documentation CLI

Command-line interface for the parser-led documentation workflow.

Usage:
    python -m src.modules.docugen.workflows.parser_led.cli <directory> [options]

Examples:
    # Basic usage
    python -m src.modules.docugen.workflows.parser_led.cli /path/to/csharp/project

    # With custom output
    python -m src.modules.docugen.workflows.parser_led.cli /path/to/project --output ./docs

    # Include private members
    python -m src.modules.docugen.workflows.parser_led.cli /path/to/project --private

    # Custom LLM model
    python -m src.modules.docugen.workflows.parser_led.cli /path/to/project --model qwen3:14b
"""

import argparse
import sys
from pathlib import Path
from loguru import logger
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn
)
from rich.table import Table
from rich.panel import Panel

from .state import ParserLedConfig
from .workflow import run_parser_led_workflow


def setup_logging(verbose: bool = False):
    """Configure logging for CLI."""
    logger.remove()  # Remove default handler

    if verbose:
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG"
        )
    else:
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level="INFO"
        )


def create_summary_table(state):
    """Create a Rich table with summary statistics."""
    table = Table(title="Documentation Summary", show_header=True, header_style="bold magenta")

    table.add_column("Metric", style="cyan", width=30)
    table.add_column("Value", style="green", justify="right")

    if state.validation_results:
        total_files = len(state.validation_results)
        complete_files = sum(1 for v in state.validation_results.values() if v.is_complete)
        avg_coverage = sum(v.coverage_percentage for v in state.validation_results.values()) / total_files
        total_elements = sum(v.total_elements for v in state.validation_results.values())
        documented_elements = sum(v.documented_elements for v in state.validation_results.values())

        table.add_row("Total Files", str(total_files))
        table.add_row("Complete Files", f"{complete_files} ({complete_files/total_files*100:.0f}%)")
        table.add_row("Average Coverage", f"{avg_coverage:.1f}%")
        table.add_row("Total Elements", str(total_elements))
        table.add_row("Documented Elements", str(documented_elements))
        table.add_row("Missing Elements", str(total_elements - documented_elements))

    return table


def create_file_table(state):
    """Create a Rich table with per-file statistics."""
    table = Table(title="Per-File Coverage", show_header=True, header_style="bold magenta")

    table.add_column("File", style="cyan")
    table.add_column("Coverage", justify="right", style="green")
    table.add_column("Elements", justify="center")
    table.add_column("Status", justify="center")

    if state.validation_results:
        for file_path in sorted(state.validation_results.keys()):
            validation = state.validation_results[file_path]

            coverage_str = f"{validation.coverage_percentage:.1f}%"
            elements_str = f"{validation.documented_elements}/{validation.total_elements}"

            if validation.is_complete:
                status = "[green]✓ Complete[/green]"
            else:
                status = f"[yellow]⚠ {validation.missing_elements} gaps[/yellow]"

            table.add_row(file_path, coverage_str, elements_str, status)

    return table


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate documentation for C# projects using parser-led workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "directory",
        type=str,
        help="Path to C# project directory"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output directory for documentation (default: <directory>/documentation)"
    )

    parser.add_argument(
        "--private",
        action="store_true",
        help="Include private members in documentation"
    )

    parser.add_argument(
        "--no-private",
        action="store_true",
        help="Exclude private members from documentation (default)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="mistral-nemo:latest",
        help="LLM model to use (default: mistral-nemo:latest)"
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3,
        help="Maximum validation iterations per file (default: 3)"
    )

    parser.add_argument(
        "--llm-base-url",
        type=str,
        default="http://localhost:11434/v1",
        help="LLM base URL (default: http://localhost:11434/v1 for Ollama)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Validate directory
    directory_path = Path(args.directory)
    if not directory_path.exists():
        logger.error(f"Directory does not exist: {args.directory}")
        sys.exit(1)

    if not directory_path.is_dir():
        logger.error(f"Path is not a directory: {args.directory}")
        sys.exit(1)

    # Create configuration
    config = ParserLedConfig(
        include_private_members=args.private if args.private else not args.no_private,
        max_validation_iterations=args.max_iterations,
        llm_model=args.model,
        llm_base_url=args.llm_base_url
    )

    # Create console for rich output
    console = Console()

    # Display configuration
    console.print(Panel.fit(
        f"[bold cyan]Parser-Led Documentation Workflow[/bold cyan]\n\n"
        f"Directory: [yellow]{args.directory}[/yellow]\n"
        f"Output: [yellow]{args.output or '<directory>/documentation'}[/yellow]\n"
        f"Model: [yellow]{args.model}[/yellow]\n"
        f"Private Members: [yellow]{config.include_private_members}[/yellow]\n"
        f"Max Iterations: [yellow]{config.max_validation_iterations}[/yellow]",
        title="Configuration"
    ))

    # Run workflow with progress indication
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            # Add tasks (we'll update these manually)
            task1 = progress.add_task("[cyan]Parsing C# files...", total=None)
            task2 = progress.add_task("[cyan]Generating documentation...", total=None, start=False)
            task3 = progress.add_task("[cyan]Compiling final output...", total=None, start=False)

            # Run workflow
            logger.info("Starting workflow execution...")

            # We'll run without progress for now since workflow is integrated
            progress.update(task1, description="[green]✓ Parsing C# files")
            progress.start_task(task2)

            final_state = run_parser_led_workflow(
                directory_path=str(directory_path),
                config=config,
                output_path=args.output
            )

            progress.update(task2, description="[green]✓ Documentation generated")
            progress.start_task(task3)
            progress.update(task3, description="[green]✓ Final output compiled")

        # Display summary
        console.print("\n")
        console.print(create_summary_table(final_state))
        console.print("\n")
        console.print(create_file_table(final_state))

        # Display output location
        output_dir = args.output or str(directory_path / "documentation")
        console.print(f"\n[bold green]✓ Documentation generated successfully![/bold green]")
        console.print(f"Output: [cyan]{output_dir}/documentation.md[/cyan]\n")

    except KeyboardInterrupt:
        console.print("\n[yellow]Workflow interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Workflow failed: {e}")
        console.print(f"\n[bold red]✗ Workflow failed: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
