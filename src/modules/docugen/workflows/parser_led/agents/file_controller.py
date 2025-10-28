"""
File Controller - Orchestrates per-file workflow

Routes each file through the documentation and validation pipeline.

Responsibilities:
- Manage file iteration from parser output
- Route each file through Documentation Agent
- Route each file through Validation Agent
- Track progress across files
- Aggregate results for final compilation
"""

from loguru import logger
from typing import Dict

from ..state import ParserLedState
from .documentation_agent import (
    document_class,
    load_prompt_template as load_doc_template
)
from .validation_agent import (
    detect_gaps,
    calculate_coverage,
    refine_missing_element,
    load_refinement_prompt_template
)
from ....shared.core import create_chat_model
from ..state import FileDocumentation, ValidationResult
from pathlib import Path


def process_single_file(
    state: ParserLedState,
    file_path: str,
    llm_model
) -> tuple:
    """
    Process a single file through documentation and validation.

    Args:
        state: Current workflow state
        file_path: Relative path to file
        llm_model: LLM instance

    Returns:
        Tuple of (FileDocumentation, ValidationResult)
    """
    logger.info(f"Processing file: {file_path}")

    if file_path not in state.structure_snapshots:
        logger.warning(f"No structure snapshot for {file_path}")
        return None, None

    snapshot = state.structure_snapshots[file_path]

    # Read file content
    full_path = Path(state.directory_path) / file_path
    with open(full_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Create file documentation
    file_doc = FileDocumentation(
        file_path=file_path,
        namespace=snapshot.namespace
    )

    # Document each class
    logger.info(f"Documenting {len(snapshot.classes)} classes in {file_path}")
    for class_info in snapshot.classes:
        doc_class = document_class(
            class_info=class_info,
            file_content=file_content,
            llm_model=llm_model,
            include_private=state.config.include_private_members
        )

        if doc_class:
            file_doc.classes[class_info.name] = doc_class

    # Initial validation
    gaps = detect_gaps(snapshot, file_doc, state.config.include_private_members)
    total, documented, coverage = calculate_coverage(
        snapshot, file_doc, state.config.include_private_members
    )

    logger.info(
        f"Initial documentation coverage: {coverage:.1f}%",
        file=file_path,
        gaps=len(gaps)
    )

    # Iterative refinement
    iteration = 0
    max_iterations = state.config.max_validation_iterations

    while gaps and iteration < max_iterations:
        iteration += 1
        logger.info(f"Refinement iteration {iteration}/{max_iterations} for {file_path}")

        # Refine each gap
        for gap in gaps:
            doc_data = refine_missing_element(
                gap, snapshot, file_content, file_doc, llm_model
            )

            if doc_data:
                # Add refined documentation (logic from validation_agent.py)
                if gap.element_type == "class":
                    from ..state import DocumentedClass
                    file_doc.classes[gap.element_name] = DocumentedClass(
                        name=gap.element_name,
                        description=doc_data.get("description", ""),
                        purpose=doc_data.get("purpose", "")
                    )
                elif gap.element_type == "method" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        from ..state import DocumentedMethod
                        file_doc.classes[gap.parent_class].methods[gap.element_name] = DocumentedMethod(
                            name=gap.element_name,
                            description=doc_data.get("description", ""),
                            parameters=doc_data.get("parameters", {}),
                            returns=doc_data.get("returns")
                        )
                elif gap.element_type == "property" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        from ..state import DocumentedProperty
                        file_doc.classes[gap.parent_class].properties[gap.element_name] = DocumentedProperty(
                            name=gap.element_name,
                            description=doc_data.get("description", "")
                        )
                elif gap.element_type == "field" and gap.parent_class:
                    if gap.parent_class in file_doc.classes:
                        from ..state import DocumentedField
                        file_doc.classes[gap.parent_class].fields[gap.element_name] = DocumentedField(
                            name=gap.element_name,
                            description=doc_data.get("description", "")
                        )

        # Re-validate
        gaps = detect_gaps(snapshot, file_doc, state.config.include_private_members)
        total, documented, coverage = calculate_coverage(
            snapshot, file_doc, state.config.include_private_members
        )

        logger.info(
            f"After iteration {iteration}: {coverage:.1f}% coverage ({len(gaps)} gaps)"
        )

        if not gaps:
            break

    # Create final validation result
    validation_result = ValidationResult(
        file_path=file_path,
        iteration=iteration,
        coverage_percentage=coverage,
        total_elements=total,
        documented_elements=documented,
        missing_elements=len(gaps),
        gaps=gaps,
        is_complete=(len(gaps) == 0)
    )

    logger.info(
        f"Completed {file_path}",
        coverage=f"{coverage:.1f}%",
        iterations=iteration,
        complete=validation_result.is_complete
    )

    return file_doc, validation_result


def file_controller_node(state: ParserLedState) -> ParserLedState:
    """
    File Controller LangGraph Node - Orchestrates per-file workflow.

    Manages iteration through files and routes each through the pipeline.

    Args:
        state: Current workflow state with structure_snapshots

    Returns:
        Updated state with documented_files and validation_results
    """
    logger.info(
        "Starting File Controller",
        total_files=len(state.structure_snapshots)
    )

    if not state.structure_snapshots:
        logger.warning("No files to process")
        return state

    # Create LLM model once for all files
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

    # Process each file
    total_files = len(state.structure_snapshots)
    completed_files = 0

    for idx, file_path in enumerate(state.structure_snapshots.keys(), start=1):
        logger.info(f"Processing file {idx}/{total_files}: {file_path}")

        try:
            file_doc, validation_result = process_single_file(
                state, file_path, llm_model
            )

            if file_doc and validation_result:
                state.documented_files[file_path] = file_doc
                state.validation_results[file_path] = validation_result
                completed_files += 1

        except Exception as e:
            logger.error(
                f"Failed to process {file_path}: {e}",
                file=file_path,
                error=str(e)
            )
            # Continue with other files

    # Calculate summary metrics
    complete_count = sum(1 for v in state.validation_results.values() if v.is_complete)
    avg_coverage = sum(v.coverage_percentage for v in state.validation_results.values()) / len(state.validation_results) if state.validation_results else 0

    logger.info(
        "File Controller complete",
        completed=completed_files,
        total=total_files,
        complete_files=complete_count,
        avg_coverage=f"{avg_coverage:.1f}%"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "file_controller_node",
    "process_single_file"
]
