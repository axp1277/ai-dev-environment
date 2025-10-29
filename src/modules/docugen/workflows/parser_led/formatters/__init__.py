"""
Formatters for documentation output.
"""

from .markdown_formatter import (
    format_class,
    format_method,
    format_property,
    format_field,
    format_file_documentation,
    generate_table_of_contents,
    generate_summary_metrics,
    clean_text
)

from .hierarchical_formatter import (
    generate_hierarchical_documentation,
    format_class_hierarchical,
    format_method_hierarchical,
    format_property_hierarchical,
    format_field_hierarchical,
    format_dependencies_section
)

__all__ = [
    # Markdown formatters
    "format_class",
    "format_method",
    "format_property",
    "format_field",
    "format_file_documentation",
    "generate_table_of_contents",
    "generate_summary_metrics",
    "clean_text",
    # Hierarchical formatters
    "generate_hierarchical_documentation",
    "format_class_hierarchical",
    "format_method_hierarchical",
    "format_property_hierarchical",
    "format_field_hierarchical",
    "format_dependencies_section"
]
