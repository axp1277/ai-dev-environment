"""
Hierarchical Formatter - Generates numbered hierarchical documentation

Transforms documented elements into hierarchical numbered format matching
the sample template structure.

Responsibilities:
- Format with hierarchical numbering (5.x.x.x.2.x)
- Group by module/library
- Include dependencies with reasoning
- Full method signatures with types
- Namespace and inheritance info
- Public/private indicators
"""

import re
from typing import List, Dict, Tuple
from loguru import logger

from ..state import (
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField,
    ValidationResult,
    StructureSnapshot
)


def clean_text(text: str) -> str:
    """Remove special characters and clean text."""
    if not text:
        return ""

    # Remove or replace common problematic characters
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2014', '--')
    text = text.replace('\u2026', '...')
    text = re.sub(r'[\u200b-\u200f\ufeff]', '', text)

    return text.strip()


class HierarchicalNumbering:
    """Manages hierarchical section numbering."""

    def __init__(self, base_number: str = "5"):
        self.base = base_number
        self.counters = {}

    def get_module_number(self, module_index: int) -> str:
        """Get number for a module (5.x)."""
        return f"{self.base}.{module_index}"

    def get_section_number(self, module_num: str, section: str) -> str:
        """Get number for a section within module (5.x.x.x.1, 5.x.x.x.2)."""
        # For simplicity, use fixed section numbers
        section_map = {
            "dependencies": "1",
            "classes": "2"
        }
        return f"{module_num}.{section_map.get(section, '0')}"

    def get_class_number(self, module_num: str, class_index: int) -> str:
        """Get number for a class (5.x.x.x.2.x)."""
        return f"{module_num}.2.{class_index}"


def format_method_hierarchical(method: DocumentedMethod, method_info=None) -> str:
    """Format a method with full signature."""
    lines = []

    # Build full signature if we have type information
    if method_info and hasattr(method_info, 'parameters'):
        param_list = []
        for param in method_info.parameters:
            param_type = getattr(param, 'type', 'object')
            param_name = getattr(param, 'name', 'param')
            param_list.append(f"{param_type} {param_name}")

        return_type = getattr(method_info, 'return_type', 'void')
        signature = f"{return_type} {method.name}({', '.join(param_list)})"
    else:
        # Fallback to simple signature
        if method.parameters:
            params = ', '.join(method.parameters.keys())
            signature = f"{method.name}({params})"
        else:
            signature = f"{method.name}()"

    # Format: - Signature: Description
    description = clean_text(method.description) if method.description else "No description available"

    # Add parameter descriptions if available
    if method.parameters:
        param_desc = []
        for param_name, param_text in method.parameters.items():
            param_desc.append(f"    {param_name}: {clean_text(param_text)}")
        if param_desc:
            description += "\n" + "\n".join(param_desc)

    # Add return description
    if method.returns:
        description += f"\n    Returns: {clean_text(method.returns)}"

    lines.append(f"- {signature}: {description}")

    return "\n".join(lines)


def format_property_hierarchical(prop: DocumentedProperty, prop_info=None) -> str:
    """Format a property with type."""
    # Get type if available
    prop_type = getattr(prop_info, 'type', 'object') if prop_info else 'object'

    description = clean_text(prop.description) if prop.description else "No description available"
    return f"- {prop_type} {prop.name}: {description}"


def format_field_hierarchical(field: DocumentedField, field_info=None) -> str:
    """Format a field/attribute with type and accessibility."""
    # Get type and accessibility
    field_type = getattr(field_info, 'type', 'object') if field_info else 'object'
    is_public = getattr(field_info, 'is_public', True) if field_info else True
    accessibility = "public" if is_public else "private"

    description = clean_text(field.description) if field.description else "No description available"
    return f"- {field_type} {field.name} ({accessibility}): {description}"


def format_class_hierarchical(
    doc_class: DocumentedClass,
    class_number: str,
    snapshot: StructureSnapshot = None
) -> str:
    """Format a class in hierarchical numbered format."""
    lines = []

    # Class header with number
    lines.append(f"{class_number} {doc_class.name}")
    lines.append("")

    # Namespace and inheritance
    namespace = snapshot.namespace if snapshot else "Unknown"
    lines.append(f"Namespace: {namespace}")

    # Find class info from snapshot for inheritance details
    if snapshot:
        class_info = next((c for c in snapshot.classes if c.name == doc_class.name), None)
        if class_info:
            if class_info.base_class:
                lines.append(f"Base class: {class_info.base_class}")
            if class_info.interfaces:
                lines.append(f"Interfaces: {', '.join(class_info.interfaces)}")

    lines.append("")

    # Description
    if doc_class.description:
        lines.append(clean_text(doc_class.description))
    else:
        lines.append("No description available.")
    lines.append("")

    # Attributes/Fields
    if doc_class.fields:
        lines.append("Attributes:")
        lines.append("")

        # Get field info from snapshot if available
        field_infos = {}
        if snapshot:
            class_info = next((c for c in snapshot.classes if c.name == doc_class.name), None)
            if class_info:
                for field_info in class_info.attributes:
                    field_infos[field_info.name] = field_info

        for field_name, field_doc in sorted(doc_class.fields.items()):
            field_info = field_infos.get(field_name)
            lines.append(format_field_hierarchical(field_doc, field_info))

        lines.append("")

    # Properties
    if doc_class.properties:
        lines.append("Properties:")
        lines.append("")

        # Get property info from snapshot if available
        prop_infos = {}
        if snapshot:
            class_info = next((c for c in snapshot.classes if c.name == doc_class.name), None)
            if class_info:
                for prop_info in class_info.properties:
                    prop_infos[prop_info.name] = prop_info

        for prop_name, prop_doc in sorted(doc_class.properties.items()):
            prop_info = prop_infos.get(prop_name)
            lines.append(format_property_hierarchical(prop_doc, prop_info))

        lines.append("")

    # Methods
    if doc_class.methods:
        lines.append("Methods:")
        lines.append("")

        # Get method info from snapshot if available
        method_infos = {}
        if snapshot:
            class_info = next((c for c in snapshot.classes if c.name == doc_class.name), None)
            if class_info:
                for method_info in class_info.methods:
                    method_infos[method_info.name] = method_info

        for method_name, method_doc in sorted(doc_class.methods.items()):
            method_info = method_infos.get(method_name)
            lines.append(format_method_hierarchical(method_doc, method_info))

        lines.append("")

    return "\n".join(lines)


def format_dependencies_section(dependencies: List[str], dependency_map: Dict[str, str] = None) -> str:
    """Format dependencies section with descriptions."""
    if not dependencies:
        return ""

    lines = []
    for dep in sorted(dependencies):
        # Use provided description or generate a default one
        if dependency_map and dep in dependency_map:
            description = dependency_map[dep]
        else:
            description = "Required dependency for functionality"

        lines.append(f"- {dep}: {description}")

    return "\n".join(lines)


def generate_hierarchical_documentation(
    documented_files: Dict[str, FileDocumentation],
    structure_snapshots: Dict[str, StructureSnapshot],
    validation_results: Dict[str, ValidationResult] = None,
    base_number: str = "5"
) -> str:
    """Generate complete hierarchical numbered documentation."""
    lines = []
    numbering = HierarchicalNumbering(base_number)

    # Group files by module/namespace
    modules = {}
    for file_path, file_doc in documented_files.items():
        namespace = file_doc.namespace or "Unknown"
        # Extract module name (first part of namespace)
        module = namespace.split('.')[0] if namespace else "Unknown"

        if module not in modules:
            modules[module] = []
        modules[module].append((file_path, file_doc))

    # Generate documentation for each module
    module_index = 1
    for module_name, files in sorted(modules.items()):
        module_num = numbering.get_module_number(module_index)

        # Module header
        lines.append("=" * 80)
        lines.append(f"Section {module_index}")
        lines.append("=" * 80)
        lines.append(f"{module_num} {module_name}")
        lines.append("")

        # Module description (could be enhanced)
        lines.append(f"Module containing {len(files)} file(s) with related functionality.")
        lines.append("")

        # Dependencies section
        lines.append(f"{module_num}.1 Dependencies")
        lines.append("")

        # Collect all dependencies from files in this module
        all_dependencies = set()
        for file_path, file_doc in files:
            if file_path in structure_snapshots:
                snapshot = structure_snapshots[file_path]
                all_dependencies.update(snapshot.dependencies)

        if all_dependencies:
            lines.append(format_dependencies_section(list(all_dependencies)))
        else:
            lines.append("No external dependencies.")

        lines.append("")

        # Classes section
        lines.append(f"{module_num}.2 Classes")
        lines.append("")

        # Document each class
        class_index = 1
        for file_path, file_doc in sorted(files):
            snapshot = structure_snapshots.get(file_path)

            for class_name, class_doc in sorted(file_doc.classes.items()):
                class_num = numbering.get_class_number(module_num, class_index)
                lines.append(format_class_hierarchical(class_doc, class_num, snapshot))
                class_index += 1

        module_index += 1
        lines.append("")

    return "\n".join(lines)


# Export formatters
__all__ = [
    "generate_hierarchical_documentation",
    "format_class_hierarchical",
    "format_method_hierarchical",
    "format_property_hierarchical",
    "format_field_hierarchical",
    "format_dependencies_section",
    "clean_text"
]
