"""
DocuGen CLI - Language-agnostic code documentation generator.

This module provides the command-line interface for the DocuGen multi-agent
documentation system.
"""

import sys
from pathlib import Path
from typing import Optional

import click
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from .core import (
    validate_config_path,
    validate_input_path,
    verify_ollama_running,
    DocuGenConfig,
)
from .agents.file_summarizer_agent import FileSummarizerAgent
from .agents.detailing_agent import DetailingAgent
from .agents.relationship_mapper_agent import RelationshipMapperAgent
from .agents.documentation_agent import DocumentationAgent
from .state import FileState, GraphConfig, FileSummary
from .orchestrator import create_orchestrator
from .writers import save_layer_outputs

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="docugen")
def main():
    """
    DocuGen - Multi-agent code documentation generator.

    Automatically generates comprehensive, multi-layered documentation
    for legacy codebases using local LLMs.

    Initial support: C# codebases
    Planned: Java, Python, JavaScript, and more
    """
    pass


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to configuration YAML file",
)
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to source code directory",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output directory for generated documentation (overrides config)",
)
@click.option(
    "--incremental",
    is_flag=True,
    help="Only process files changed since last run",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Validate configuration and show what would be processed without generating docs",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging (DEBUG level)",
)
def document(
    config: str,
    input: str,
    output: Optional[str],
    incremental: bool,
    dry_run: bool,
    verbose: bool,
):
    """
    Generate documentation for a codebase.

    This command processes source code files through a multi-layer
    agent pipeline to generate comprehensive documentation.

    Example:
        docugen document -c config.yaml -i /path/to/codebase
    """
    # Configure logging
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=log_level, format="<level>{message}</level>")

    try:
        # Validate inputs
        config_path = validate_config_path(config)
        input_path = validate_input_path(input)

        # Verify Ollama is running
        if not verify_ollama_running():
            console.print(
                Panel(
                    "[red]Error: Ollama is not running[/red]\n\n"
                    "Please start Ollama with: [cyan]ollama serve[/cyan]",
                    title="Ollama Not Available",
                    border_style="red",
                )
            )
            sys.exit(1)

        # Load configuration
        doc_config = DocuGenConfig.from_yaml(config_path)

        if output:
            doc_config.output_path = Path(output)

        # Display configuration summary
        console.print(
            Panel(
                f"[cyan]Config:[/cyan] {config_path}\n"
                f"[cyan]Input:[/cyan] {input_path}\n"
                f"[cyan]Output:[/cyan] {doc_config.output_path}\n"
                f"[cyan]Mode:[/cyan] {'Incremental' if incremental else 'Full'}\n"
                f"[cyan]Dry Run:[/cyan] {dry_run}",
                title="DocuGen Configuration",
                border_style="cyan",
            )
        )

        if dry_run:
            console.print("[yellow]Dry run mode - no documentation will be generated[/yellow]")

            # Find C# files
            cs_files = list(input_path.rglob("*.cs"))

            console.print("[green]✓ Configuration valid[/green]")
            console.print("[green]✓ Input directory accessible[/green]")
            console.print("[green]✓ Ollama connection verified[/green]")
            console.print(f"[cyan]ℹ Found {len(cs_files)} C# files to process[/cyan]")
            sys.exit(0)

        # Create GraphConfig from DocuGenConfig
        graph_config = GraphConfig(
            summarizer_model=doc_config.models.summarizer,
            detailing_model=doc_config.models.detailing,
            relationship_model=doc_config.models.relationship_mapper,
            documentation_model=doc_config.models.documentation,
            validation_model=doc_config.models.validation,
            llm_base_url=doc_config.llm.base_url,
                llm_api_key_env=doc_config.llm.api_key_env,
                llm_timeout=doc_config.llm.timeout,
            summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md"),
            detailing_prompt_path=Path("src/modules/docugen/prompts/detailing_agent.md"),
            relationship_prompt_path=Path("src/modules/docugen/prompts/relationship_mapper.md"),
            max_iterations=doc_config.validation.max_iterations,
        )

        # Create orchestrator
        orchestrator = create_orchestrator(graph_config)

        # Find C# files
        cs_files = list(input_path.rglob("*.cs"))

        if not cs_files:
            console.print("[yellow]No C# files found in the specified directory[/yellow]")
            sys.exit(0)

        console.print(f"\n[bold cyan]Starting documentation pipeline for {len(cs_files)} files...[/bold cyan]\n")

        # Process directory
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Processing files...", total=len(cs_files))

            # Process the directory
            results = orchestrator.process_directory(input_path, pattern="*.cs")

            progress.update(task, completed=len(cs_files))

        # Save JSON outputs
        console.print("\n[bold cyan]Saving layer outputs...[/bold cyan]")
        json_files = save_layer_outputs(results, doc_config.output_path)
        console.print(f"[green]✓ JSON outputs saved to {doc_config.output_path}[/green]")

        # Generate final documentation
        console.print("\n[bold cyan]Generating comprehensive documentation...[/bold cyan]")
        doc_agent = DocumentationAgent(graph_config)
        project_name = input_path.name
        final_doc_path = doc_config.output_path / "DOCUMENTATION.md"

        doc_agent.invoke(
            layer1_path=json_files['layer1'],
            layer2_path=json_files['layer2'],
            layer3_path=json_files['layer3'],
            output_path=final_doc_path,
            project_name=project_name
        )

        console.print(f"[green]✓ Documentation generated: {final_doc_path}[/green]")

        # Display summary
        total = len(results)
        completed = sum(1 for s in results.values() if not s.flagged_for_review and not s.error_message)
        flagged = sum(1 for s in results.values() if s.flagged_for_review)
        errors = sum(1 for s in results.values() if s.error_message)

        console.print(
            Panel(
                f"[green]✓ Completed:[/green] {completed}/{total} files\n"
                f"[yellow]⚠ Flagged for review:[/yellow] {flagged}/{total} files\n"
                f"[red]✗ Errors:[/red] {errors}/{total} files\n\n"
                f"[cyan]Success rate:[/cyan] {(completed/total*100):.1f}%",
                title="Pipeline Complete",
                border_style="green" if completed == total else "yellow",
            )
        )

        # List flagged files
        if flagged > 0:
            console.print("\n[yellow]Files flagged for manual review:[/yellow]")
            for file_path, state in results.items():
                if state.flagged_for_review:
                    console.print(f"  • {file_path.name} (failed at {state.current_layer})")

        sys.exit(0 if errors == 0 else 1)

    except Exception as e:
        logger.error(f"Error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to configuration YAML file",
)
def status(config: str):
    """
    Show current documentation generation status.

    Displays progress, validation metrics, and estimated completion time
    for running or paused documentation jobs.
    """
    try:
        config_path = validate_config_path(config)

        console.print(
            Panel(
                "[yellow]Status monitoring not yet implemented[/yellow]\n\n"
                "This feature will display:\n"
                "• Current file being processed\n"
                "• Progress (files completed / total)\n"
                "• Current layer (L1/L2/L3)\n"
                "• Validation pass rate\n"
                "• Estimated time remaining",
                title="Status",
                border_style="yellow",
            )
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to configuration YAML file",
)
def resume(config: str):
    """
    Resume interrupted documentation generation.

    Continues from the last successfully completed file, preserving
    all previously generated documentation.
    """
    try:
        config_path = validate_config_path(config)

        console.print(
            Panel(
                "[yellow]Resume functionality not yet implemented[/yellow]\n\n"
                "This feature will:\n"
                "• Load saved state from last run\n"
                "• Continue from last completed file\n"
                "• Preserve existing documentation\n"
                "• Update progress metrics",
                title="Resume",
                border_style="yellow",
            )
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to configuration YAML file",
)
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to documentation output directory",
)
def validate(config: str, input: str):
    """
    Validate existing documentation against quality rules.

    Checks generated documentation for completeness, consistency,
    and compliance with validation schemas.
    """
    try:
        config_path = validate_config_path(config)
        input_path = validate_input_path(input)

        console.print(
            Panel(
                "[yellow]Validation command not yet implemented[/yellow]\n\n"
                "This feature will:\n"
                "• Check documentation completeness\n"
                "• Validate against Pydantic schemas\n"
                "• Report quality metrics\n"
                "• Identify files needing manual review",
                title="Validate",
                border_style="yellow",
            )
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


# ============================================================================
# Test Command Group - Isolated Agent Testing
# ============================================================================


@main.group()
def test():
    """
    Test individual agents in isolation.

    Run specific documentation layers on sample files to verify agent
    behavior and output quality without running the full pipeline.
    """
    pass


@test.command(name="layer1")
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to C# file or directory",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration YAML file (optional, uses defaults if not provided)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output JSON file path (optional)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=None,
    help="Limit number of files to process (useful for directories)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging (DEBUG level)",
)
def test_layer1(input: str, config: Optional[str], output: Optional[str], limit: Optional[int], verbose: bool):
    """
    Test FileSummarizerAgent (Layer 1) in isolation.

    Analyzes C# files and generates high-level summaries. This is useful
    for testing the agent before running the full pipeline.

    Examples:
        # Test single file
        docugen test layer1 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs

        # Test directory (limit to 5 files)
        docugen test layer1 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services -l 5

        # Save results to JSON
        docugen test layer1 -i data/sample_codebase/RepoScribe-master -l 3 -o layer1_results.json
    """
    import json
    from rich.table import Table
    from rich.syntax import Syntax
    from pathlib import Path

    # Configure logging
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=log_level, format="<level>{message}</level>")

    try:
        # Verify Ollama is running
        if not verify_ollama_running():
            console.print(
                Panel(
                    "[red]Error: Ollama is not running[/red]\n\n"
                    "Please start Ollama with: [cyan]ollama serve[/cyan]",
                    title="Ollama Not Available",
                    border_style="red",
                )
            )
            sys.exit(1)

        # Load configuration or use defaults
        if config:
            config_path = validate_config_path(config)
            doc_config = DocuGenConfig.from_yaml(config_path)
            graph_config = GraphConfig(
                summarizer_model=doc_config.models.summarizer,
                llm_base_url=doc_config.llm.base_url,
                llm_api_key_env=doc_config.llm.api_key_env,
                llm_timeout=doc_config.llm.timeout,
                summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md"),
            )
        else:
            graph_config = GraphConfig()

        # Find C# files
        input_path = Path(input)
        if input_path.is_file():
            cs_files = [input_path]
        else:
            cs_files = list(input_path.rglob("*.cs"))

        if limit:
            cs_files = cs_files[:limit]

        if not cs_files:
            console.print("[yellow]No C# files found in the specified path[/yellow]")
            sys.exit(0)

        # Display test configuration
        console.print(
            Panel(
                f"[cyan]Agent:[/cyan] FileSummarizerAgent (Layer 1)\n"
                f"[cyan]Model:[/cyan] {graph_config.summarizer_model}\n"
                f"[cyan]Files:[/cyan] {len(cs_files)}\n"
                f"[cyan]Input:[/cyan] {input_path}",
                title="Test Configuration",
                border_style="cyan",
            )
        )

        # Initialize agent
        agent = FileSummarizerAgent(graph_config)

        # Process files
        results = []
        for idx, file_path in enumerate(cs_files, 1):
            console.print(f"\n[bold cyan]Processing {idx}/{len(cs_files)}:[/bold cyan] {file_path.name}")

            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Create state
                state = FileState(file_path=file_path, file_content=content)

                # Run agent
                result_state = agent.invoke(state)

                if result_state.error_message:
                    console.print(f"[red]✗ Error: {result_state.error_message}[/red]")
                    continue

                # Display results
                summary = result_state.layer1_summary
                if summary:
                    console.print(f"[green]✓ Summary generated successfully[/green]\n")

                    # Create results table
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Field", style="cyan", width=20)
                    table.add_column("Value", style="white")

                    table.add_row("Summary", summary.summary)
                    table.add_row("Purpose", summary.purpose)
                    table.add_row("Category", summary.category)
                    table.add_row("Key Classes", ", ".join(summary.key_classes) if summary.key_classes else "None")

                    console.print(table)

                    # Store for JSON output
                    results.append({
                        "file": str(file_path),
                        "summary": summary.summary,
                        "purpose": summary.purpose,
                        "category": summary.category,
                        "key_classes": summary.key_classes,
                    })

            except Exception as e:
                console.print(f"[red]✗ Error processing file: {e}[/red]")
                logger.exception(f"Error processing {file_path}: {e}")

        # Save results to JSON if requested
        if output and results:
            output_path = Path(output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            console.print(f"\n[green]✓ Results saved to {output_path}[/green]")

        # Summary
        console.print(
            Panel(
                f"[green]Processed:[/green] {len(results)}/{len(cs_files)} files\n"
                f"[cyan]Total files:[/cyan] {len(cs_files)}",
                title="Test Summary",
                border_style="green",
            )
        )

    except Exception as e:
        logger.exception(f"Test failed: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@test.command(name="layer2")
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to C# file or directory",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration YAML file (optional, uses defaults if not provided)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output JSON file path (optional)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=None,
    help="Limit number of files to process (useful for directories)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging (DEBUG level)",
)
def test_layer2(input: str, config: Optional[str], output: Optional[str], limit: Optional[int], verbose: bool):
    """
    Test DetailingAgent (Layer 2) in isolation.

    Generates detailed documentation for classes and methods. This requires
    Layer 1 summary first, which is generated automatically.

    Examples:
        # Test single file
        docugen test layer2 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs

        # Test directory (limit to 3 files)
        docugen test layer2 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services -l 3

        # Save results to JSON
        docugen test layer2 -i data/sample_codebase/RepoScribe-master -l 2 -o layer2_results.json
    """
    import json
    from rich.table import Table
    from rich.tree import Tree
    from pathlib import Path

    # Configure logging
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=log_level, format="<level>{message}</level>")

    try:
        # Verify Ollama is running
        if not verify_ollama_running():
            console.print(
                Panel(
                    "[red]Error: Ollama is not running[/red]\n\n"
                    "Please start Ollama with: [cyan]ollama serve[/cyan]",
                    title="Ollama Not Available",
                    border_style="red",
                )
            )
            sys.exit(1)

        # Load configuration or use defaults
        if config:
            config_path = validate_config_path(config)
            doc_config = DocuGenConfig.from_yaml(config_path)
            graph_config = GraphConfig(
                summarizer_model=doc_config.models.summarizer,
                detailing_model=doc_config.models.detailing,
                llm_base_url=doc_config.llm.base_url,
                llm_api_key_env=doc_config.llm.api_key_env,
                llm_timeout=doc_config.llm.timeout,
                summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md"),
                detailing_prompt_path=Path("src/modules/docugen/prompts/detailing_agent.md"),
            )
        else:
            graph_config = GraphConfig()

        # Find C# files
        input_path = Path(input)
        if input_path.is_file():
            cs_files = [input_path]
        else:
            cs_files = list(input_path.rglob("*.cs"))

        if limit:
            cs_files = cs_files[:limit]

        if not cs_files:
            console.print("[yellow]No C# files found in the specified path[/yellow]")
            sys.exit(0)

        # Display test configuration
        console.print(
            Panel(
                f"[cyan]Agent:[/cyan] DetailingAgent (Layer 2)\n"
                f"[cyan]Model:[/cyan] {graph_config.detailing_model}\n"
                f"[cyan]Files:[/cyan] {len(cs_files)}\n"
                f"[cyan]Input:[/cyan] {input_path}",
                title="Test Configuration",
                border_style="cyan",
            )
        )

        # Initialize agents (need Layer 1 first)
        layer1_agent = FileSummarizerAgent(graph_config)
        layer2_agent = DetailingAgent(graph_config)

        # Process files
        results = []
        for idx, file_path in enumerate(cs_files, 1):
            console.print(f"\n[bold cyan]Processing {idx}/{len(cs_files)}:[/bold cyan] {file_path.name}")

            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Create state and run Layer 1 first
                state = FileState(file_path=file_path, file_content=content)
                state = layer1_agent.invoke(state)

                if state.error_message:
                    console.print(f"[red]✗ Layer 1 Error: {state.error_message}[/red]")
                    continue

                # Run Layer 2
                state = layer2_agent.invoke(state)

                if state.error_message:
                    console.print(f"[red]✗ Layer 2 Error: {state.error_message}[/red]")
                    continue

                # Display results
                details = state.layer2_details
                if details:
                    console.print(f"[green]✓ Detailed documentation generated successfully[/green]\n")

                    # Create tree visualization
                    tree = Tree(f"[bold]{file_path.name}[/bold]")

                    # Add classes
                    for cls in details.classes:
                        class_branch = tree.add(f"[cyan]Class: {cls.name}[/cyan]")
                        class_branch.add(f"[dim]{cls.description}[/dim]")

                        if cls.methods:
                            methods_branch = class_branch.add(f"[yellow]Methods ({len(cls.methods)})[/yellow]")
                            for method in cls.methods[:5]:  # Limit to first 5 for display
                                method_node = methods_branch.add(f"[green]{method.name}[/green]")
                                method_node.add(f"[dim]{method.description[:80]}...[/dim]" if len(method.description) > 80 else f"[dim]{method.description}[/dim]")

                    # Add standalone methods
                    if details.standalone_methods:
                        standalone_branch = tree.add(f"[yellow]Standalone Methods ({len(details.standalone_methods)})[/yellow]")
                        for method in details.standalone_methods[:5]:
                            method_node = standalone_branch.add(f"[green]{method.name}[/green]")
                            method_node.add(f"[dim]{method.description[:80]}...[/dim]" if len(method.description) > 80 else f"[dim]{method.description}[/dim]")

                    console.print(tree)

                    # Store for JSON output
                    results.append({
                        "file": str(file_path),
                        "classes": [
                            {
                                "name": cls.name,
                                "description": cls.description,
                                "methods": [
                                    {
                                        "name": m.name,
                                        "signature": m.signature,
                                        "description": m.description,
                                        "parameters": m.parameters,
                                        "returns": m.returns
                                    } for m in cls.methods
                                ]
                            } for cls in details.classes
                        ],
                        "standalone_methods": [
                            {
                                "name": m.name,
                                "signature": m.signature,
                                "description": m.description,
                                "parameters": m.parameters,
                                "returns": m.returns
                            } for m in details.standalone_methods
                        ]
                    })

            except Exception as e:
                console.print(f"[red]✗ Error processing file: {e}[/red]")
                logger.exception(f"Error processing {file_path}: {e}")

        # Save results to JSON if requested
        if output and results:
            output_path = Path(output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            console.print(f"\n[green]✓ Results saved to {output_path}[/green]")

        # Summary
        console.print(
            Panel(
                f"[green]Processed:[/green] {len(results)}/{len(cs_files)} files\n"
                f"[cyan]Total files:[/cyan] {len(cs_files)}",
                title="Test Summary",
                border_style="green",
            )
        )

    except Exception as e:
        logger.exception(f"Test failed: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@test.command(name="layer3")
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to C# file or directory",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration YAML file (optional, uses defaults if not provided)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output JSON file path (optional)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=None,
    help="Limit number of files to process (useful for directories)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging (DEBUG level)",
)
def test_layer3(input: str, config: Optional[str], output: Optional[str], limit: Optional[int], verbose: bool):
    """
    Test RelationshipMapperAgent (Layer 3) in isolation.

    Maps cross-file dependencies and architectural relationships. This requires
    Layer 1 and Layer 2 first, which are generated automatically.

    Examples:
        # Test single file
        docugen test layer3 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs

        # Test directory (limit to 3 files)
        docugen test layer3 -i data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services -l 3

        # Save results to JSON
        docugen test layer3 -i data/sample_codebase/RepoScribe-master -l 2 -o layer3_results.json
    """
    import json
    from rich.table import Table
    from rich.tree import Tree
    from pathlib import Path

    # Configure logging
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=log_level, format="<level>{message}</level>")

    try:
        # Verify Ollama is running
        if not verify_ollama_running():
            console.print(
                Panel(
                    "[red]Error: Ollama is not running[/red]\n\n"
                    "Please start Ollama with: [cyan]ollama serve[/cyan]",
                    title="Ollama Not Available",
                    border_style="red",
                )
            )
            sys.exit(1)

        # Load configuration or use defaults
        if config:
            config_path = validate_config_path(config)
            doc_config = DocuGenConfig.from_yaml(config_path)
            graph_config = GraphConfig(
                summarizer_model=doc_config.models.summarizer,
                detailing_model=doc_config.models.detailing,
                relationship_model=doc_config.models.relationship_mapper,
                llm_base_url=doc_config.llm.base_url,
                llm_api_key_env=doc_config.llm.api_key_env,
                llm_timeout=doc_config.llm.timeout,
                summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md"),
                detailing_prompt_path=Path("src/modules/docugen/prompts/detailing_agent.md"),
                relationship_prompt_path=Path("src/modules/docugen/prompts/relationship_mapper.md"),
            )
        else:
            graph_config = GraphConfig()

        # Find C# files
        input_path = Path(input)
        if input_path.is_file():
            cs_files = [input_path]
        else:
            cs_files = list(input_path.rglob("*.cs"))

        if limit:
            cs_files = cs_files[:limit]

        if not cs_files:
            console.print("[yellow]No C# files found in the specified path[/yellow]")
            sys.exit(0)

        # Display test configuration
        console.print(
            Panel(
                f"[cyan]Agent:[/cyan] RelationshipMapperAgent (Layer 3)\n"
                f"[cyan]Model:[/cyan] {graph_config.relationship_model}\n"
                f"[cyan]Files:[/cyan] {len(cs_files)}\n"
                f"[cyan]Input:[/cyan] {input_path}",
                title="Test Configuration",
                border_style="cyan",
            )
        )

        # Initialize agents (need Layer 1 and 2 first)
        layer1_agent = FileSummarizerAgent(graph_config)
        layer2_agent = DetailingAgent(graph_config)
        layer3_agent = RelationshipMapperAgent(graph_config)

        # Process files
        results = []
        for idx, file_path in enumerate(cs_files, 1):
            console.print(f"\n[bold cyan]Processing {idx}/{len(cs_files)}:[/bold cyan] {file_path.name}")

            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Create state and run Layer 1
                state = FileState(file_path=file_path, file_content=content)
                state = layer1_agent.invoke(state)

                if state.error_message:
                    console.print(f"[red]✗ Layer 1 Error: {state.error_message}[/red]")
                    continue

                # Run Layer 2
                state = layer2_agent.invoke(state)

                if state.error_message:
                    console.print(f"[red]✗ Layer 2 Error: {state.error_message}[/red]")
                    continue

                # Run Layer 3
                state = layer3_agent.invoke(state)

                if state.error_message:
                    console.print(f"[red]✗ Layer 3 Error: {state.error_message}[/red]")
                    continue

                # Display results
                relationships = state.layer3_relationships
                if relationships:
                    console.print(f"[green]✓ Relationship mapping completed successfully[/green]\n")

                    # Create results table
                    table = Table(show_header=True, header_style="bold magenta", title=f"[bold]{file_path.name}[/bold]")
                    table.add_column("Aspect", style="cyan", width=20)
                    table.add_column("Details", style="white")

                    # Architectural role
                    table.add_row("Architectural Role", relationships.architectural_role or "Not specified")

                    # Dependencies
                    if relationships.dependencies:
                        deps_text = "\n".join([
                            f"• {dep.file} ({dep.relationship_type})\n  {dep.purpose}"
                            for dep in relationships.dependencies[:5]  # Limit display
                        ])
                        table.add_row(f"Dependencies ({len(relationships.dependencies)})", deps_text)
                    else:
                        table.add_row("Dependencies", "None identified")

                    # Dependents
                    if relationships.dependents:
                        deps_text = "\n".join([
                            f"• {dep.get('file', 'Unknown')}"
                            for dep in relationships.dependents[:5]  # Limit display
                        ])
                        table.add_row(f"Dependents ({len(relationships.dependents)})", deps_text)
                    else:
                        table.add_row("Dependents", "None identified")

                    console.print(table)

                    # Store for JSON output
                    results.append({
                        "file": str(file_path),
                        "architectural_role": relationships.architectural_role,
                        "dependencies": [
                            {
                                "file": dep.file,
                                "classes_used": dep.classes_used,
                                "purpose": dep.purpose,
                                "relationship_type": dep.relationship_type
                            } for dep in relationships.dependencies
                        ],
                        "dependents": relationships.dependents
                    })

            except Exception as e:
                console.print(f"[red]✗ Error processing file: {e}[/red]")
                logger.exception(f"Error processing {file_path}: {e}")

        # Save results to JSON if requested
        if output and results:
            output_path = Path(output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            console.print(f"\n[green]✓ Results saved to {output_path}[/green]")

        # Summary
        console.print(
            Panel(
                f"[green]Processed:[/green] {len(results)}/{len(cs_files)} files\n"
                f"[cyan]Total files:[/cyan] {len(cs_files)}",
                title="Test Summary",
                border_style="green",
            )
        )

    except Exception as e:
        logger.exception(f"Test failed: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command(name="test-connection")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration YAML file (default: config.yaml)",
)
def test_connection(config: Optional[str]):
    """
    Test LLM connection using config.yaml settings.

    Validates that the configured base_url and default model are accessible
    by sending a simple test prompt. Works with all providers (Ollama, OpenRouter, OpenAI, etc.).

    Examples:
        docugen test-connection
        docugen test-connection -c config.yaml
    """
    from langchain_core.messages import HumanMessage

    console.print("\n[bold blue]DocuGen LLM Connection Test[/bold blue]")
    console.print("[dim]" + "═" * 50 + "[/dim]\n")

    # Load configuration
    try:
        if config:
            config_path = validate_config_path(config)
        else:
            config_path = Path("config.yaml")
            if not config_path.exists():
                console.print("[red]Error: config.yaml not found[/red]")
                console.print("Create one from: cp src/modules/docugen/config/config.example.yaml config.yaml")
                sys.exit(1)

        doc_config = DocuGenConfig.from_yaml(config_path)
        base_url = doc_config.llm.base_url
        model = doc_config.models.default
        api_key_env = doc_config.llm.api_key_env

    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/red]")
        sys.exit(1)

    # Display connection info
    console.print(f"[cyan]Base URL:[/cyan] [yellow]{base_url}[/yellow]")
    console.print(f"[cyan]Model:[/cyan] [yellow]{model}[/yellow]")
    if api_key_env:
        console.print(f"[cyan]API Key:[/cyan] [yellow]{api_key_env} (from .env)[/yellow]\n")
    else:
        console.print(f"[cyan]API Key:[/cyan] [dim]None (local endpoint)[/dim]\n")

    # Test connection
    try:
        console.print("[dim]Sending test prompt: 'Say hello in 5 words or less'[/dim]\n")

        # Create LangChain chat model
        chat_model = create_chat_model(base_url, model, api_key_env, doc_config.llm.timeout)

        # Send test prompt
        response = chat_model.invoke([
            HumanMessage(content="Say hello in 5 words or less")
        ])

        # Extract response
        message = response.content

        # Display success
        console.print(Panel.fit(
            f"[green]✓ Connection successful![/green]\n\n"
            f"Response: [white]{message}[/white]",
            title="[bold green]Test Passed[/bold green]",
            border_style="green"
        ))

        sys.exit(0)

    except Exception as e:
        # Display failure with provider-appropriate troubleshooting
        is_local = "localhost" in base_url or "127.0.0.1" in base_url

        troubleshooting = f"[dim]Troubleshooting:[/dim]\n• Verify {base_url} is accessible\n"

        if is_local:
            troubleshooting += f"• Check if local LLM server is running\n"
            troubleshooting += f"• For Ollama: ollama serve\n"
            troubleshooting += f"• Verify model exists: ollama list\n"
            troubleshooting += f"• Pull model if needed: ollama pull {model}"
        else:
            troubleshooting += f"• Check your API key in .env file\n"
            troubleshooting += f"• Verify API key environment variable: {api_key_env}\n"
            troubleshooting += f"• Check provider model name format\n"
            troubleshooting += f"• Ensure you have API credits/quota"

        console.print(Panel.fit(
            f"[red]✗ Connection failed[/red]\n\n"
            f"Error: [yellow]{str(e)}[/yellow]\n\n"
            f"{troubleshooting}",
            title="[bold red]Test Failed[/bold red]",
            border_style="red"
        ))

        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
