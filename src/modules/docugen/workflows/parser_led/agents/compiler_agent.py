"""
Compiler Agent - Final Documentation Assembly

Compiles all validated documentation into final markdown output.

Responsibilities:
- Aggregate all validated file documentation
- Apply consolidated element definitions (if available)
- Generate table of contents
- Apply consistent formatting
- Create summary metrics
- Export to markdown file
"""

import time
from pathlib import Path
from datetime import datetime
from typing import Dict
from loguru import logger

from ..state import ParserLedState, FileDocumentation, DocumentedMethod, DocumentedProperty, DocumentedField
from ..formatters.hierarchical_formatter import generate_hierarchical_documentation
from ..formatters.markdown_formatter import (
    format_file_documentation,
    generate_table_of_contents,
    generate_summary_metrics
)


def apply_consolidated_definitions(
    documented_files: Dict[str, FileDocumentation],
    consolidated_elements: Dict[str, 'ConsolidatedElement']
) -> Dict[str, FileDocumentation]:
    """
    Replace duplicate element documentation with consolidated versions.

    This preprocessing step applies LLM-consolidated definitions to replace
    redundant documentation for inherited/interface members.

    Args:
        documented_files: Original file documentation
        consolidated_elements: Consolidated element definitions from consolidation agent

    Returns:
        Updated documented_files with consolidated definitions applied
    """
    if not consolidated_elements:
        return documented_files

    logger.info(f"Applying {len(consolidated_elements)} consolidated definitions")
    replacement_count = 0

    # Create a copy to avoid modifying the original
    updated_files = {}

    for file_path, file_doc in documented_files.items():
        # Create new FileDocumentation with potentially updated elements
        updated_file_doc = FileDocumentation(
            file_path=file_doc.file_path,
            namespace=file_doc.namespace,
            classes={}
        )

        # Process each class
        for class_name, doc_class in file_doc.classes.items():
            # Copy class documentation
            updated_class = type(doc_class)(
                name=doc_class.name,
                description=doc_class.description,
                purpose=doc_class.purpose,
                methods={},
                properties={},
                fields={}
            )

            # Process methods - check for consolidated versions
            for method_name, method_doc in doc_class.methods.items():
                element_key = f"method:{method_name}"

                if element_key in consolidated_elements:
                    consolidated = consolidated_elements[element_key]
                    # Use consolidated version
                    updated_class.methods[method_name] = DocumentedMethod(
                        name=method_name,
                        description=consolidated.consolidated_description,
                        parameters=consolidated.consolidated_parameters or {},
                        returns=consolidated.consolidated_returns
                    )
                    replacement_count += 1
                    logger.debug(f"  Replaced {class_name}.{method_name} with consolidated version")
                else:
                    # Keep original
                    updated_class.methods[method_name] = method_doc

            # Process properties
            for prop_name, prop_doc in doc_class.properties.items():
                element_key = f"property:{prop_name}"

                if element_key in consolidated_elements:
                    consolidated = consolidated_elements[element_key]
                    updated_class.properties[prop_name] = DocumentedProperty(
                        name=prop_name,
                        description=consolidated.consolidated_description
                    )
                    replacement_count += 1
                    logger.debug(f"  Replaced {class_name}.{prop_name} with consolidated version")
                else:
                    updated_class.properties[prop_name] = prop_doc

            # Process fields
            for field_name, field_doc in doc_class.fields.items():
                element_key = f"field:{field_name}"

                if element_key in consolidated_elements:
                    consolidated = consolidated_elements[element_key]
                    updated_class.fields[field_name] = DocumentedField(
                        name=field_name,
                        description=consolidated.consolidated_description
                    )
                    replacement_count += 1
                    logger.debug(f"  Replaced {class_name}.{field_name} with consolidated version")
                else:
                    updated_class.fields[field_name] = field_doc

            updated_file_doc.classes[class_name] = updated_class

        updated_files[file_path] = updated_file_doc

    logger.info(f"Applied consolidated definitions: {replacement_count} replacements made")
    return updated_files


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
    agent_start_time = time.time()
    logger.info(
        f"[AGENT START] Compiler Agent | Files: {len(state.documented_files)} | Format: {state.config.output_format}"
    )

    if not state.documented_files:
        logger.warning("No documented files to compile")
        return state

    # Apply consolidated definitions if available
    documented_files_to_compile = state.documented_files
    if state.consolidated_elements:
        logger.info("Applying consolidated element definitions before compilation")
        documented_files_to_compile = apply_consolidated_definitions(
            state.documented_files,
            state.consolidated_elements
        )
    else:
        logger.info("No consolidated elements - using original documentation")

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
            documented_files=documented_files_to_compile,
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
        markdown_content.append(generate_table_of_contents(documented_files_to_compile))
        markdown_content.append("---")
        markdown_content.append("")

        # Individual file documentation
        markdown_content.append("# Detailed Documentation")
        markdown_content.append("")

        for file_path in sorted(documented_files_to_compile.keys()):
            file_doc = documented_files_to_compile[file_path]
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

    for file_path, file_doc in documented_files_to_compile.items():
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
        files=len(documented_files_to_compile),
        directory=str(per_file_dir)
    )

    # Update state with output path
    # We'll add this to the state model later if needed
    # For now, just log it
    agent_duration = time.time() - agent_start_time
    logger.info(
        f"[AGENT END] Compiler Agent | Duration: {agent_duration:.2f}s | Output: {output_file} | Size: {len(full_markdown) / 1024:.1f} KB"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "compiler_agent_node"
]
