"""
Validation Agent - Layer 2 (Documentation Validation & Refinement)

Validates documentation completeness and refines missing elements iteratively.

Responsibilities:
- Compare parser structure with documented elements
- Identify gaps (missing classes, methods, properties, fields)
- Generate targeted refinement prompts for missing elements
- Re-run LLM to document missing items
- Update documentation with refined results
- Track coverage metrics
- Enforce max iteration limits
"""

import json
from pathlib import Path
from typing import Optional, List, Dict
from loguru import logger

from ..state import (
    ParserLedState,
    ValidationResult,
    ValidationGap,
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField
)
from ....shared.parsers.csharp_structure_parser import (
    StructureSnapshot,
    ClassInfo,
    MethodInfo,
    PropertyInfo,
    AttributeInfo
)
from ....shared.core import create_chat_model


def load_refinement_prompt_template() -> str:
    """Load the refinement documentation prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "refinement_documenter.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def detect_gaps(
    snapshot: StructureSnapshot,
    file_doc: FileDocumentation,
    include_private: bool = True
) -> List[ValidationGap]:
    """
    Detect missing or incomplete documentation by comparing parser and docs.

    Args:
        snapshot: Parser output (ground truth)
        file_doc: LLM-generated documentation
        include_private: Whether to check private members

    Returns:
        List of ValidationGap objects
    """
    gaps = []

    for class_info in snapshot.classes:
        # Check if class is documented
        if class_info.name not in file_doc.classes:
            gaps.append(ValidationGap(
                element_type="class",
                element_name=class_info.name,
                reason="Class not documented"
            ))
            # If class is missing, all its members are missing too
            continue

        doc_class = file_doc.classes[class_info.name]

        # Check methods
        for method in class_info.methods:
            if not include_private and 'private' in method.modifiers:
                continue

            if method.name not in doc_class.methods:
                gaps.append(ValidationGap(
                    element_type="method",
                    element_name=method.name,
                    parent_class=class_info.name,
                    reason="Method not documented"
                ))

        # Check properties
        for prop in class_info.properties:
            if not include_private and 'private' in prop.modifiers:
                continue

            if prop.name not in doc_class.properties:
                gaps.append(ValidationGap(
                    element_type="property",
                    element_name=prop.name,
                    parent_class=class_info.name,
                    reason="Property not documented"
                ))

        # Check fields
        for field in class_info.attributes:
            if not include_private and 'private' in field.modifiers:
                continue

            if field.name not in doc_class.fields:
                gaps.append(ValidationGap(
                    element_type="field",
                    element_name=field.name,
                    parent_class=class_info.name,
                    reason="Field not documented"
                ))

    return gaps


def calculate_coverage(snapshot: StructureSnapshot, file_doc: FileDocumentation, include_private: bool) -> tuple:
    """
    Calculate documentation coverage metrics.

    Args:
        snapshot: Parser output
        file_doc: Documentation
        include_private: Whether to count private members

    Returns:
        Tuple of (total_elements, documented_elements, coverage_percentage)
    """
    total_elements = 0
    documented_elements = 0

    for class_info in snapshot.classes:
        total_elements += 1  # Count the class itself

        if class_info.name in file_doc.classes:
            documented_elements += 1
            doc_class = file_doc.classes[class_info.name]

            # Count methods
            for method in class_info.methods:
                if not include_private and 'private' in method.modifiers:
                    continue
                total_elements += 1
                if method.name in doc_class.methods:
                    documented_elements += 1

            # Count properties
            for prop in class_info.properties:
                if not include_private and 'private' in prop.modifiers:
                    continue
                total_elements += 1
                if prop.name in doc_class.properties:
                    documented_elements += 1

            # Count fields
            for field in class_info.attributes:
                if not include_private and 'private' in field.modifiers:
                    continue
                total_elements += 1
                if field.name in doc_class.fields:
                    documented_elements += 1

    coverage = (documented_elements / total_elements * 100) if total_elements > 0 else 0
    return total_elements, documented_elements, coverage


def generate_existing_doc_summary(file_doc: FileDocumentation) -> str:
    """Generate a summary of existing documentation for context."""
    summary_lines = []

    for class_name, class_doc in file_doc.classes.items():
        summary_lines.append(f"Class '{class_name}': {class_doc.description[:100]}...")

        if class_doc.methods:
            method_names = ", ".join(list(class_doc.methods.keys())[:5])
            summary_lines.append(f"  Methods: {method_names}")

        if class_doc.properties:
            prop_names = ", ".join(list(class_doc.properties.keys())[:5])
            summary_lines.append(f"  Properties: {prop_names}")

    return "\n".join(summary_lines) if summary_lines else "No elements documented yet."


def refine_missing_element(
    gap: ValidationGap,
    snapshot: StructureSnapshot,
    file_content: str,
    file_doc: FileDocumentation,
    llm_model
) -> Optional[Dict]:
    """
    Generate documentation for a single missing element using targeted refinement.

    Args:
        gap: The validation gap to fill
        snapshot: Parser structure
        file_content: Full source file
        file_doc: Existing documentation
        llm_model: LLM instance

    Returns:
        Documentation dict or None if failed
    """
    try:
        template = load_refinement_prompt_template()

        # Find the element in the snapshot
        element_signature = ""
        parent_class_info = ""

        if gap.element_type == "class":
            for class_info in snapshot.classes:
                if class_info.name == gap.element_name:
                    base_str = f" : {class_info.base_class}" if class_info.base_class else ""
                    interfaces_str = f", {', '.join(class_info.interfaces)}" if class_info.interfaces else ""
                    element_signature = f"class {class_info.name}{base_str}{interfaces_str}"
                    break

        elif gap.element_type == "method":
            for class_info in snapshot.classes:
                if class_info.name == gap.parent_class:
                    for method in class_info.methods:
                        if method.name == gap.element_name:
                            params_str = ", ".join(method.parameters) if method.parameters else ""
                            element_signature = f"{method.return_type} {method.name}({params_str})"
                            parent_class_info = f"**Parent Class**: {gap.parent_class}\n"
                            break

        elif gap.element_type == "property":
            for class_info in snapshot.classes:
                if class_info.name == gap.parent_class:
                    for prop in class_info.properties:
                        if prop.name == gap.element_name:
                            element_signature = f"{prop.type} {prop.name}"
                            parent_class_info = f"**Parent Class**: {gap.parent_class}\n"
                            break

        elif gap.element_type == "field":
            for class_info in snapshot.classes:
                if class_info.name == gap.parent_class:
                    for field in class_info.attributes:
                        if field.name == gap.element_name:
                            element_signature = f"{field.type} {field.name}"
                            parent_class_info = f"**Parent Class**: {gap.parent_class}\n"
                            break

        # Generate existing documentation summary
        existing_summary = generate_existing_doc_summary(file_doc)

        # Format the prompt
        prompt = template.format(
            element_type=gap.element_type.capitalize(),
            element_name=gap.element_name,
            parent_class_info=parent_class_info,
            element_signature=element_signature,
            file_content=file_content,
            existing_documentation_summary=existing_summary
        )

        logger.debug(f"Refining {gap.element_type}: {gap.element_name}")
        response = llm_model.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Parse JSON
        try:
            doc_data = json.loads(content)
            return doc_data
        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse JSON for {gap.element_type} {gap.element_name}",
                error=str(e),
                content_preview=content[:200]
            )
            return None

    except Exception as e:
        logger.error(
            f"Failed to refine {gap.element_type} {gap.element_name}: {e}",
            error=str(e)
        )
        return None


def validation_agent_node(state: ParserLedState) -> ParserLedState:
    """
    Validation Agent LangGraph Node - Layer 2 (Documentation Validation & Refinement).

    Validates documentation completeness and iteratively refines missing elements.

    Args:
        state: Current workflow state with documented_files populated

    Returns:
        Updated state with validation_results and refined documentation
    """
    logger.info(
        "Starting Validation Agent",
        iteration=state.validation_iteration + 1,
        max_iterations=state.config.max_validation_iterations,
        files=len(state.documented_files)
    )

    if not state.documented_files:
        logger.warning("No documented files to validate")
        return state

    # Create LLM model for refinement
    try:
        llm_model = create_chat_model(
            base_url=state.config.llm_base_url,
            model_name=state.config.llm_model,
            api_key_env=state.config.llm_api_key_env,
            timeout=state.config.llm_timeout
        )
    except Exception as e:
        logger.error(f"Failed to create LLM model: {e}")
        raise

    # Increment iteration
    state.validation_iteration += 1
    current_iteration = state.validation_iteration

    # Process each documented file
    for file_path, file_doc in state.documented_files.items():
        if file_path not in state.structure_snapshots:
            logger.warning(f"No snapshot for {file_path}, skipping validation")
            continue

        snapshot = state.structure_snapshots[file_path]

        logger.info(f"Validating file: {file_path}")

        # Detect gaps
        gaps = detect_gaps(snapshot, file_doc, state.config.include_private_members)

        # Calculate coverage
        total, documented, coverage = calculate_coverage(
            snapshot, file_doc, state.config.include_private_members
        )

        # Create validation result
        validation_result = ValidationResult(
            file_path=file_path,
            iteration=current_iteration,
            coverage_percentage=coverage,
            total_elements=total,
            documented_elements=documented,
            missing_elements=len(gaps),
            gaps=gaps,
            is_complete=(len(gaps) == 0)
        )

        logger.info(
            f"Validation metrics for {file_path}",
            coverage=f"{coverage:.1f}%",
            total=total,
            documented=documented,
            missing=len(gaps)
        )

        # If gaps exist and we haven't exceeded max iterations, refine
        if gaps and current_iteration < state.config.max_validation_iterations:
            logger.info(f"Refining {len(gaps)} missing elements")

            # Read file content
            full_path = Path(state.directory_path) / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # Refine each gap
            for gap in gaps:
                doc_data = refine_missing_element(
                    gap, snapshot, file_content, file_doc, llm_model
                )

                if not doc_data:
                    continue

                # Add refined documentation to file_doc
                if gap.element_type == "class":
                    file_doc.classes[gap.element_name] = DocumentedClass(
                        name=gap.element_name,
                        description=doc_data.get("description", ""),
                        purpose=doc_data.get("purpose", "")
                    )

                elif gap.element_type == "method" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        file_doc.classes[gap.parent_class].methods[gap.element_name] = DocumentedMethod(
                            name=gap.element_name,
                            description=doc_data.get("description", ""),
                            parameters=doc_data.get("parameters", {}),
                            returns=doc_data.get("returns")
                        )

                elif gap.element_type == "property" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        file_doc.classes[gap.parent_class].properties[gap.element_name] = DocumentedProperty(
                            name=gap.element_name,
                            description=doc_data.get("description", "")
                        )

                elif gap.element_type == "field" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        file_doc.classes[gap.parent_class].fields[gap.element_name] = DocumentedField(
                            name=gap.element_name,
                            description=doc_data.get("description", "")
                        )

            # Re-validate after refinement
            gaps_after = detect_gaps(snapshot, file_doc, state.config.include_private_members)
            total_after, documented_after, coverage_after = calculate_coverage(
                snapshot, file_doc, state.config.include_private_members
            )

            validation_result.coverage_percentage = coverage_after
            validation_result.documented_elements = documented_after
            validation_result.missing_elements = len(gaps_after)
            validation_result.gaps = gaps_after
            validation_result.is_complete = (len(gaps_after) == 0)

            logger.info(
                f"After refinement: {coverage_after:.1f}% coverage ({len(gaps_after)} gaps remaining)"
            )

        # Store validation result
        state.validation_results[file_path] = validation_result

    # Log summary
    complete_files = sum(1 for v in state.validation_results.values() if v.is_complete)
    avg_coverage = sum(v.coverage_percentage for v in state.validation_results.values()) / len(state.validation_results) if state.validation_results else 0

    logger.info(
        "Validation Agent complete",
        iteration=current_iteration,
        complete_files=complete_files,
        total_files=len(state.validation_results),
        avg_coverage=f"{avg_coverage:.1f}%"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "validation_agent_node",
    "detect_gaps",
    "calculate_coverage",
    "refine_missing_element"
]
