"""
Compiler Agent - Final Documentation Assembly

Compiles all validated documentation into final markdown output.

Responsibilities:
- Aggregate all validated file documentation
- Generate table of contents
- Apply consistent formatting
- Create summary metrics
- Export to markdown file
"""

from pathlib import Path
from datetime import datetime
from loguru import logger

from ..state import ParserLedState
from ..formatters.hierarchical_formatter import generate_hierarchical_documentation
from ..formatters.markdown_formatter import (
    format_file_documentation,
    generate_table_of_contents,
    generate_summary_metrics
)


def compiler_agent_node(state: ParserLedState, output_path: str = None) -> ParserLedState:
    """
    Compiler Agent LangGraph Node - Assembles final documentation.

    Compiles all validated documentation into markdown files.

    Args:
        state: Current workflow state with documented_files and validation_results
        output_path: Optional custom output path

    Returns:
        Updated state with final_documentation path
    """
    logger.info(
        "Starting Compiler Agent",
        files=len(state.documented_files),
        output_format=state.config.output_format
    )

    if not state.documented_files:
        logger.warning("No documented files to compile")
        return state

    # Determine output directory
    if output_path is None:
        output_dir = Path(state.directory_path) / "documentation"
    else:
        output_dir = Path(output_path)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check output format from config
    output_format = state.config.output_format if state.config else "hierarchical"

    # Build complete documentation based on format
    if output_format == "hierarchical":
        # Use hierarchical numbered format
        content = []

        # Header
        content.append("=" * 80)
        content.append("CODE DOCUMENTATION")
        content.append("=" * 80)
        content.append(f"Generated: {timestamp}")
        content.append(f"Source Directory: {state.directory_path}")
        content.append("")

        # Generate hierarchical documentation
        hierarchical_doc = generate_hierarchical_documentation(
            documented_files=state.documented_files,
            structure_snapshots=state.structure_snapshots,
            validation_results=state.validation_results,
            base_number="5"
        )
        content.append(hierarchical_doc)

        full_markdown = "\n".join(content)
    else:
        # Use original markdown format
        markdown_content = []

        # Header
        markdown_content.append(f"# Code Documentation")
        markdown_content.append("")
        markdown_content.append(f"**Generated:** {timestamp}")
        markdown_content.append(f"**Source Directory:** `{state.directory_path}`")
        markdown_content.append("")
        markdown_content.append("---")
        markdown_content.append("")

        # Summary metrics
        if state.validation_results:
            markdown_content.append(generate_summary_metrics(state.validation_results))
            markdown_content.append("---")
            markdown_content.append("")

        # Table of contents
        markdown_content.append(generate_table_of_contents(state.documented_files))
        markdown_content.append("---")
        markdown_content.append("")

        # Individual file documentation
        markdown_content.append("# Detailed Documentation")
        markdown_content.append("")

        for file_path in sorted(state.documented_files.keys()):
            file_doc = state.documented_files[file_path]
            validation_result = state.validation_results.get(file_path)

            # Add file documentation
            file_markdown = format_file_documentation(file_doc, validation_result)
            markdown_content.append(file_markdown)
            markdown_content.append("")
            markdown_content.append("---")
            markdown_content.append("")

        # Combine all content
        full_markdown = "\n".join(markdown_content)

    # Write to file
    output_file = output_dir / "documentation.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

    logger.info(
        "Documentation compiled successfully",
        output_file=str(output_file),
        size=f"{len(full_markdown) / 1024:.1f} KB"
    )

    # Also create per-file documentation (optional)
    per_file_dir = output_dir / "files"
    per_file_dir.mkdir(exist_ok=True)

    for file_path, file_doc in state.documented_files.items():
        validation_result = state.validation_results.get(file_path)

        # Create markdown for this file
        file_markdown = format_file_documentation(file_doc, validation_result)

        # Determine output filename
        safe_filename = file_path.replace('/', '_').replace('\\', '_')
        output_filename = per_file_dir / f"{safe_filename}.md"

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(file_markdown)

    logger.info(
        "Per-file documentation created",
        files=len(state.documented_files),
        directory=str(per_file_dir)
    )

    # Update state with output path
    # We'll add this to the state model later if needed
    # For now, just log it
    logger.info(f"Final documentation available at: {output_file}")

    return state


# Export for LangGraph graph construction
__all__ = [
    "compiler_agent_node"
]
