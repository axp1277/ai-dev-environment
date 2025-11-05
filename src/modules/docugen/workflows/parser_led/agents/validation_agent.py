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
import time
import re
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


def call_llm_with_retry(llm_model, prompt: str, element_type: str, element_name: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Call LLM with retry logic for robustness.

    Args:
        llm_model: LLM model instance
        prompt: The prompt to send
        element_type: Type of element being refined (for logging)
        element_name: Name of element being refined (for logging)
        max_retries: Maximum number of retry attempts

    Returns:
        Parsed JSON dict or None if all retries fail
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Make LLM call
            llm_start = time.time()
            response = llm_model.invoke(prompt)
            llm_duration = time.time() - llm_start

            # Extract content
            content = response.content if hasattr(response, 'content') else str(response)

            # Log response
            logger.info(
                f"  [LLM RESPONSE] Refinement - {element_type} {element_name} | "
                f"Attempt: {attempt}/{max_retries} | Duration: {llm_duration:.2f}s | Response: {len(content)} chars"
            )

            # Extract and parse JSON
            json_content = extract_json_from_response(content)
            doc_data = json.loads(json_content)

            # Success!
            if attempt > 1:
                logger.info(f"  [RETRY SUCCESS] Refinement - {element_type} {element_name} succeeded on attempt {attempt}")
            return doc_data

        except json.JSONDecodeError as e:
            logger.warning(
                f"  [JSON PARSE ERROR] Refinement - {element_type} {element_name} | Attempt {attempt}/{max_retries}",
                error=str(e),
                error_line=e.lineno if hasattr(e, 'lineno') else None,
                error_col=e.colno if hasattr(e, 'colno') else None
            )

            if attempt < max_retries:
                logger.info(f"  [RETRY] Retrying refinement for {element_type} {element_name} (attempt {attempt + 1}/{max_retries})")
                continue
            else:
                # Final attempt failed - log full content
                logger.error(
                    f"  [ALL RETRIES FAILED] Refinement - {element_type} {element_name} | All {max_retries} attempts failed",
                    error=str(e),
                    content_preview=content[:500],
                    full_content=content
                )
                return None

        except Exception as e:
            logger.error(
                f"  [LLM ERROR] Refinement - {element_type} {element_name} | Attempt {attempt}/{max_retries}",
                error=str(e)
            )
            if attempt < max_retries:
                logger.info(f"  [RETRY] Retrying refinement for {element_type} {element_name} due to error")
                continue
            else:
                logger.error(f"  [ALL RETRIES FAILED] Refinement - {element_type} {element_name} | Error: {e}")
                return None

    return None


def extract_json_from_response(content: str) -> str:
    """
    Robustly extract JSON from LLM response.

    Handles:
    - Markdown code blocks (```json or ```)
    - Plain JSON with surrounding text
    - Common prefixes like "Here is the JSON:"
    - JSON objects anywhere in the text

    Args:
        content: Raw LLM response content

    Returns:
        Extracted JSON string

    Raises:
        ValueError: If no JSON can be extracted
    """
    # Strategy 1: Try markdown code blocks first
    if "```json" in content:
        try:
            extracted = content.split("```json")[1].split("```")[0].strip()
            if extracted:
                return extracted
        except IndexError:
            pass

    if "```" in content:
        try:
            extracted = content.split("```")[1].split("```")[0].strip()
            if extracted:
                return extracted
        except IndexError:
            pass

    # Strategy 2: Strip common prefixes and try parsing
    common_prefixes = [
        "Here is the JSON:",
        "Here's the JSON:",
        "The JSON is:",
        "JSON:",
        "Output:",
        "Result:",
    ]

    cleaned_content = content.strip()
    for prefix in common_prefixes:
        if cleaned_content.lower().startswith(prefix.lower()):
            cleaned_content = cleaned_content[len(prefix):].strip()
            break

    # Strategy 3: Try to find JSON object using regex
    # Look for { ... } pattern (handles nested braces)
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, cleaned_content, re.DOTALL)

    if matches:
        # Try each match, starting with the longest (likely most complete)
        for match in sorted(matches, key=len, reverse=True):
            try:
                # Validate it's actually JSON
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue

    # Strategy 4: If content looks like it starts with {, try using it directly
    if cleaned_content.startswith('{'):
        # Find the matching closing brace
        brace_count = 0
        for i, char in enumerate(cleaned_content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return cleaned_content[:i+1]

    # Strategy 5: Return original content and let json.loads fail with a clear error
    return content.strip()


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

        logger.info(f"  [LLM CALL] Refinement - {gap.element_type.capitalize()} {gap.element_name} | Prompt: {len(prompt)} chars")

        doc_data = call_llm_with_retry(llm_model, prompt, gap.element_type.capitalize(), gap.element_name)

        return doc_data

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
    agent_start_time = time.time()
    llm_call_count = 0
    logger.info(
        f"[AGENT START] Validation Agent | Iteration: {state.validation_iteration + 1}/{state.config.max_validation_iterations} | Files: {len(state.documented_files)}"
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
            logger.info(f"[REFINEMENT] Starting refinement for {file_path} | Gaps: {len(gaps)}")

            # Read file content
            full_path = Path(state.directory_path) / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # Refine each gap
            refined_count = 0
            for gap in gaps:
                doc_data = refine_missing_element(
                    gap, snapshot, file_content, file_doc, llm_model
                )

                if not doc_data:
                    continue

                refined_count += 1
                llm_call_count += 1

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
                f"[REFINEMENT] Completed {file_path} | Coverage: {coverage:.1f}% -> {coverage_after:.1f}% | Gaps: {len(gaps)} -> {len(gaps_after)} | Refined: {refined_count}"
            )

        # Store validation result
        state.validation_results[file_path] = validation_result

    # Log summary
    agent_duration = time.time() - agent_start_time
    complete_files = sum(1 for v in state.validation_results.values() if v.is_complete)
    avg_coverage = sum(v.coverage_percentage for v in state.validation_results.values()) / len(state.validation_results) if state.validation_results else 0

    logger.info(
        f"[AGENT END] Validation Agent | Duration: {agent_duration:.2f}s | Complete: {complete_files}/{len(state.validation_results)} | Avg Coverage: {avg_coverage:.1f}% | LLM Calls: {llm_call_count}"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "validation_agent_node",
    "detect_gaps",
    "calculate_coverage",
    "refine_missing_element"
]
