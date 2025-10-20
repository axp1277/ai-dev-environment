"""
Markdown Documentation Generator

Generates comprehensive markdown documentation from FileState output,
combining all three layers (summary, details, relationships) into a
cohesive, navigable document.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from src.modules.docugen.state import FileState


class MarkdownGenerator:
    """
    Generates markdown documentation from processed FileState.

    Combines Layer 1 (summary), Layer 2 (detailed docs), and Layer 3 (relationships)
    into a single cohesive markdown document with metadata, table of contents,
    and navigation links.
    """

    def __init__(self, include_metadata: bool = True, include_toc: bool = True):
        """
        Initialize the MarkdownGenerator.

        Args:
            include_metadata: Whether to include generation metadata section
            include_toc: Whether to generate table of contents
        """
        self.include_metadata = include_metadata
        self.include_toc = include_toc

    def generate(self, state: FileState) -> str:
        """
        Generate complete markdown documentation from FileState.

        Args:
            state: FileState containing all layer outputs

        Returns:
            Complete markdown document as string
        """
        sections = []

        # Title
        sections.append(f"# {state.file_path.name}\n")

        # Metadata section
        if self.include_metadata:
            sections.append(self._generate_metadata(state))

        # Table of contents
        if self.include_toc:
            sections.append(self._generate_toc(state))

        # Layer 1: Summary
        if state.layer1_summary:
            sections.append(self._generate_layer1_section(state))

        # Layer 2: Detailed Documentation
        if state.layer2_details:
            sections.append(self._generate_layer2_section(state))

        # Layer 3: Relationships
        if state.layer3_relationships:
            sections.append(self._generate_layer3_section(state))

        # Error/Review flags
        if state.error_message or state.flagged_for_review:
            sections.append(self._generate_status_section(state))

        return "\n".join(sections)

    def _generate_metadata(self, state: FileState) -> str:
        """Generate metadata section with generation info."""
        lines = [
            "## Metadata",
            "",
            f"- **File Path**: `{state.file_path}`",
            f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Current Layer**: {state.current_layer}",
        ]

        # Validation status
        if state.layer1_validation:
            status = "✅ Passed" if state.layer1_validation.passed else "❌ Failed"
            lines.append(f"- **Layer 1 Validation**: {status}")

        if state.layer2_validation:
            status = "✅ Passed" if state.layer2_validation.passed else "❌ Failed"
            lines.append(f"- **Layer 2 Validation**: {status}")

        if state.layer3_validation:
            status = "✅ Passed" if state.layer3_validation.passed else "❌ Failed"
            lines.append(f"- **Layer 3 Validation**: {status}")

        # Iteration counts
        if state.layer1_iterations > 0:
            lines.append(f"- **Layer 1 Iterations**: {state.layer1_iterations}")
        if state.layer2_iterations > 0:
            lines.append(f"- **Layer 2 Iterations**: {state.layer2_iterations}")
        if state.layer3_iterations > 0:
            lines.append(f"- **Layer 3 Iterations**: {state.layer3_iterations}")

        lines.append("")
        return "\n".join(lines)

    def _generate_toc(self, state: FileState) -> str:
        """Generate table of contents."""
        lines = [
            "## Table of Contents",
            "",
        ]

        if state.layer1_summary:
            lines.append("- [Overview](#overview)")

        if state.layer2_details:
            lines.append("- [Detailed Documentation](#detailed-documentation)")
            if state.layer2_details.classes:
                lines.append("  - [Classes](#classes)")
            if state.layer2_details.standalone_methods:
                lines.append("  - [Standalone Methods](#standalone-methods)")

        if state.layer3_relationships:
            lines.append("- [Relationships](#relationships)")
            lines.append("  - [Dependencies](#dependencies)")
            lines.append("  - [Dependents](#dependents)")
            lines.append("  - [Architectural Role](#architectural-role)")

        lines.append("")
        return "\n".join(lines)

    def _generate_layer1_section(self, state: FileState) -> str:
        """Generate Layer 1 summary section."""
        summary = state.layer1_summary
        if not summary:
            return ""

        lines = [
            "## Overview",
            "",
            f"**Purpose**: {summary.purpose}",
            "",
            f"**Category**: {summary.category}",
            "",
            f"**Summary**: {summary.summary}",
            "",
        ]

        if summary.key_classes:
            lines.append("**Key Classes**:")
            for cls in summary.key_classes:
                lines.append(f"- `{cls}`")
            lines.append("")

        return "\n".join(lines)

    def _generate_layer2_section(self, state: FileState) -> str:
        """Generate Layer 2 detailed documentation section."""
        details = state.layer2_details
        if not details:
            return ""

        lines = [
            "## Detailed Documentation",
            "",
        ]

        # Classes
        if details.classes:
            lines.append("### Classes")
            lines.append("")

            for cls in details.classes:
                lines.append(f"#### `{cls.name}`")
                lines.append("")
                lines.append(cls.description)
                lines.append("")

                if cls.methods:
                    lines.append("**Methods:**")
                    lines.append("")

                    for method in cls.methods:
                        lines.append(f"##### `{method.name}`")
                        lines.append("")
                        lines.append(f"**Signature**: `{method.signature}`")
                        lines.append("")
                        lines.append(f"**Description**: {method.description}")
                        lines.append("")

                        if method.parameters:
                            lines.append("**Parameters**:")
                            for param in method.parameters:
                                lines.append(f"- {param}")
                            lines.append("")

                        if method.returns:
                            lines.append(f"**Returns**: {method.returns}")
                            lines.append("")

        # Standalone methods
        if details.standalone_methods:
            lines.append("### Standalone Methods")
            lines.append("")

            for method in details.standalone_methods:
                lines.append(f"#### `{method.name}`")
                lines.append("")
                lines.append(f"**Signature**: `{method.signature}`")
                lines.append("")
                lines.append(f"**Description**: {method.description}")
                lines.append("")

                if method.parameters:
                    lines.append("**Parameters**:")
                    for param in method.parameters:
                        lines.append(f"- {param}")
                    lines.append("")

                if method.returns:
                    lines.append(f"**Returns**: {method.returns}")
                    lines.append("")

        return "\n".join(lines)

    def _generate_layer3_section(self, state: FileState) -> str:
        """Generate Layer 3 relationships section."""
        relationships = state.layer3_relationships
        if not relationships:
            return ""

        lines = [
            "## Relationships",
            "",
        ]

        # Dependencies
        lines.append("### Dependencies")
        lines.append("")
        if relationships.dependencies:
            lines.append("This file depends on:")
            lines.append("")
            for dep in relationships.dependencies:
                lines.append(f"#### `{dep.file}`")
                lines.append("")
                lines.append(f"**Classes Used**: {', '.join(f'`{c}`' for c in dep.classes_used)}")
                lines.append("")
                lines.append(f"**Purpose**: {dep.purpose}")
                lines.append("")
                lines.append(f"**Relationship Type**: {dep.relationship_type}")
                lines.append("")
        else:
            lines.append("*No external dependencies*")
            lines.append("")

        # Dependents
        lines.append("### Dependents")
        lines.append("")
        if relationships.dependents:
            lines.append("This file is used by:")
            lines.append("")
            for dep in relationships.dependents:
                file_name = dep.get("file", "Unknown")
                how_used = dep.get("how_used", "No description")
                lines.append(f"- **`{file_name}`**: {how_used}")
            lines.append("")
        else:
            lines.append("*No known dependents*")
            lines.append("")

        # Architectural Role
        lines.append("### Architectural Role")
        lines.append("")
        lines.append(relationships.architectural_role or "*Not specified*")
        lines.append("")

        return "\n".join(lines)

    def _generate_status_section(self, state: FileState) -> str:
        """Generate status/error section if needed."""
        lines = [
            "## Status",
            "",
        ]

        if state.flagged_for_review:
            lines.append("⚠️ **Flagged for Manual Review**")
            lines.append("")
            lines.append("This file has been flagged for manual review due to validation failures exceeding the maximum iteration count.")
            lines.append("")

        if state.error_message:
            lines.append("❌ **Error During Processing**")
            lines.append("")
            lines.append(f"```\n{state.error_message}\n```")
            lines.append("")

        return "\n".join(lines)
