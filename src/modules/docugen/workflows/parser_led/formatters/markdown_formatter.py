"""
Markdown Formatter - Generates formatted markdown documentation

Transforms documented elements into clean, consistent markdown output.

Responsibilities:
- Format class documentation
- Format method documentation with parameters
- Format property and field documentation
- Generate table of contents
- Apply consistent styling
- Clean special characters
"""

import re
from typing import List, Dict
from loguru import logger

from ..state import (
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField,
    ValidationResult
)


def clean_text(text: str) -> str:
    """Remove special characters and clean text for markdown."""
    if not text:
        return ""

    # Remove or replace common problematic characters
    text = text.replace('\u2018', "'")  # Left single quote
    text = text.replace('\u2019', "'")  # Right single quote
    text = text.replace('\u201c', '"')  # Left double quote
    text = text.replace('\u201d', '"')  # Right double quote
    text = text.replace('\u2013', '-')  # En dash
    text = text.replace('\u2014', '--')  # Em dash
    text = text.replace('\u2026', '...')  # Ellipsis

    # Remove zero-width spaces and other invisible characters
    text = re.sub(r'[\u200b-\u200f\ufeff]', '', text)

    return text.strip()


def format_method(method: DocumentedMethod, indent: str = "  ") -> str:
    """Format a method's documentation as markdown."""
    lines = []

    # Method header
    lines.append(f"{indent}### `{clean_text(method.name)}`")
    lines.append("")

    # Description
    if method.description:
        lines.append(f"{indent}{clean_text(method.description)}")
        lines.append("")

    # Parameters
    if method.parameters:
        lines.append(f"{indent}**Parameters:**")
        for param_name, param_desc in method.parameters.items():
            lines.append(f"{indent}- `{clean_text(param_name)}`: {clean_text(param_desc)}")
        lines.append("")

    # Returns
    if method.returns:
        lines.append(f"{indent}**Returns:** {clean_text(method.returns)}")
        lines.append("")

    return "\n".join(lines)


def format_property(prop: DocumentedProperty, indent: str = "  ") -> str:
    """Format a property's documentation as markdown."""
    lines = []

    lines.append(f"{indent}### `{clean_text(prop.name)}`")
    lines.append("")

    if prop.description:
        lines.append(f"{indent}{clean_text(prop.description)}")
        lines.append("")

    return "\n".join(lines)


def format_field(field: DocumentedField, indent: str = "  ") -> str:
    """Format a field's documentation as markdown."""
    lines = []

    lines.append(f"{indent}### `{clean_text(field.name)}`")
    lines.append("")

    if field.description:
        lines.append(f"{indent}{clean_text(field.description)}")
        lines.append("")

    return "\n".join(lines)


def format_class(doc_class: DocumentedClass) -> str:
    """Format a class's complete documentation as markdown."""
    lines = []

    # Class header
    lines.append(f"## Class: `{clean_text(doc_class.name)}`")
    lines.append("")

    # Description
    if doc_class.description:
        lines.append(clean_text(doc_class.description))
        lines.append("")

    # Purpose
    if doc_class.purpose:
        lines.append(f"**Purpose:** {clean_text(doc_class.purpose)}")
        lines.append("")

    # Methods section
    if doc_class.methods:
        lines.append("### Methods")
        lines.append("")
        for method_name, method_doc in sorted(doc_class.methods.items()):
            lines.append(format_method(method_doc))

    # Properties section
    if doc_class.properties:
        lines.append("### Properties")
        lines.append("")
        for prop_name, prop_doc in sorted(doc_class.properties.items()):
            lines.append(format_property(prop_doc))

    # Fields section
    if doc_class.fields:
        lines.append("### Fields")
        lines.append("")
        for field_name, field_doc in sorted(doc_class.fields.items()):
            lines.append(format_field(field_doc))

    return "\n".join(lines)


def format_file_documentation(file_doc: FileDocumentation, validation_result: ValidationResult = None) -> str:
    """Format complete file documentation as markdown."""
    lines = []

    # File header
    lines.append(f"# File: `{file_doc.file_path}`")
    lines.append("")

    # Namespace
    if file_doc.namespace:
        lines.append(f"**Namespace:** `{clean_text(file_doc.namespace)}`")
        lines.append("")

    # Validation metrics (if available)
    if validation_result:
        lines.append("## Documentation Coverage")
        lines.append("")
        lines.append(f"- **Coverage:** {validation_result.coverage_percentage:.1f}%")
        lines.append(f"- **Total Elements:** {validation_result.total_elements}")
        lines.append(f"- **Documented:** {validation_result.documented_elements}")
        if validation_result.missing_elements > 0:
            lines.append(f"- **Missing:** {validation_result.missing_elements}")
        lines.append("")

    # Classes
    if file_doc.classes:
        lines.append("---")
        lines.append("")
        for class_name, class_doc in sorted(file_doc.classes.items()):
            lines.append(format_class(class_doc))
            lines.append("")

    return "\n".join(lines)


def generate_table_of_contents(documented_files: Dict[str, FileDocumentation]) -> str:
    """Generate a table of contents for all documented files."""
    lines = []

    lines.append("# Table of Contents")
    lines.append("")

    # Group by directory
    files_by_dir = {}
    for file_path, file_doc in sorted(documented_files.items()):
        dir_name = file_path.rsplit('/', 1)[0] if '/' in file_path else "Root"
        if dir_name not in files_by_dir:
            files_by_dir[dir_name] = []
        files_by_dir[dir_name].append((file_path, file_doc))

    # Generate TOC
    for dir_name, files in sorted(files_by_dir.items()):
        lines.append(f"## {dir_name}")
        lines.append("")

        for file_path, file_doc in files:
            # Link to file section
            anchor = file_path.replace('/', '-').replace('.', '-').lower()
            lines.append(f"- [{file_path}](#{anchor})")

            # List classes
            if file_doc.classes:
                for class_name in sorted(file_doc.classes.keys()):
                    class_anchor = f"{anchor}-class-{class_name.lower()}"
                    lines.append(f"  - [`{class_name}`](#{class_anchor})")

        lines.append("")

    return "\n".join(lines)


def generate_summary_metrics(validation_results: Dict[str, ValidationResult]) -> str:
    """Generate summary metrics section."""
    lines = []

    lines.append("# Documentation Summary")
    lines.append("")

    # Overall metrics
    total_files = len(validation_results)
    complete_files = sum(1 for v in validation_results.values() if v.is_complete)
    avg_coverage = sum(v.coverage_percentage for v in validation_results.values()) / total_files if total_files > 0 else 0
    total_elements = sum(v.total_elements for v in validation_results.values())
    documented_elements = sum(v.documented_elements for v in validation_results.values())

    lines.append("## Overall Metrics")
    lines.append("")
    lines.append(f"- **Total Files:** {total_files}")
    lines.append(f"- **Complete Files:** {complete_files}")
    lines.append(f"- **Average Coverage:** {avg_coverage:.1f}%")
    lines.append(f"- **Total Elements:** {total_elements}")
    lines.append(f"- **Documented Elements:** {documented_elements}")
    lines.append("")

    # Per-file breakdown
    lines.append("## Per-File Coverage")
    lines.append("")
    lines.append("| File | Coverage | Elements | Status |")
    lines.append("|------|----------|----------|--------|")

    for file_path, validation in sorted(validation_results.items()):
        status = "✓ Complete" if validation.is_complete else f"⚠ {validation.missing_elements} gaps"
        coverage_str = f"{validation.coverage_percentage:.1f}%"
        elements_str = f"{validation.documented_elements}/{validation.total_elements}"
        lines.append(f"| `{file_path}` | {coverage_str} | {elements_str} | {status} |")

    lines.append("")

    return "\n".join(lines)


# Export formatters
__all__ = [
    "format_class",
    "format_method",
    "format_property",
    "format_field",
    "format_file_documentation",
    "generate_table_of_contents",
    "generate_summary_metrics",
    "clean_text"
]
