"""
DocuGen LangGraph Orchestrator

Orchestrates the three-layer documentation pipeline using LangGraph state machine.
Implements sequential processing with validation loops and iteration limits.

Architecture:
- Layer 1: File Summarization → Validation → (pass → L2 | fail → retry/flag)
- Layer 2: Detailed Documentation → Validation → (pass → L3 | fail → retry/flag)
- Layer 3: Relationship Mapping → Validation → (pass → Output | fail → retry/flag)

Each layer has max N=3 iterations to prevent infinite refinement loops.
"""

from typing import Literal
from pathlib import Path
from langgraph.graph import StateGraph, END
from loguru import logger

from .state import FileState, GraphConfig
from .agents.file_summarizer_agent import summarize_file
from .agents.detailing_agent import generate_details
from .agents.relationship_mapper_agent import map_relationships
from .agents.validation_agent import validate_layer1, validate_layer2, validate_layer3


class DocuGenOrchestrator:
    """
    LangGraph orchestrator for multi-layer documentation generation.

    Manages state transitions, validation loops, and iteration limits.
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the orchestrator with configuration.

        Args:
            config: Graph configuration with model settings and validation rules
        """
        self.config = config
        self.graph = self._build_graph()

        logger.info(
            "DocuGenOrchestrator initialized",
            max_iterations=config.max_iterations,
            summarizer_model=config.summarizer_model,
            detailing_model=config.detailing_model,
            relationship_model=config.relationship_model
        )

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph state machine.

        Graph structure:
        START → layer1 → validate_l1 → (pass → layer2 | fail → retry_l1/flag)
                layer2 → validate_l2 → (pass → layer3 | fail → retry_l2/flag)
                layer3 → validate_l3 → (pass → END | fail → retry_l3/flag)

        Returns:
            Compiled LangGraph workflow
        """
        workflow = StateGraph(FileState)

        # Add nodes
        workflow.add_node("layer1", self._layer1_node)
        workflow.add_node("validate_l1", self._validate_l1_node)
        workflow.add_node("layer2", self._layer2_node)
        workflow.add_node("validate_l2", self._validate_l2_node)
        workflow.add_node("layer3", self._layer3_node)
        workflow.add_node("validate_l3", self._validate_l3_node)

        # Set entry point
        workflow.set_entry_point("layer1")

        # Layer 1 flow
        workflow.add_edge("layer1", "validate_l1")
        workflow.add_conditional_edges(
            "validate_l1",
            self._should_retry_layer1,
            {
                "proceed": "layer2",
                "retry": "layer1",
                "flag": END
            }
        )

        # Layer 2 flow
        workflow.add_edge("layer2", "validate_l2")
        workflow.add_conditional_edges(
            "validate_l2",
            self._should_retry_layer2,
            {
                "proceed": "layer3",
                "retry": "layer2",
                "flag": END
            }
        )

        # Layer 3 flow
        workflow.add_edge("layer3", "validate_l3")
        workflow.add_conditional_edges(
            "validate_l3",
            self._should_retry_layer3,
            {
                "proceed": END,
                "retry": "layer3",
                "flag": END
            }
        )

        return workflow.compile()

    def _layer1_node(self, state: FileState) -> FileState:
        """Layer 1: File Summarization."""
        logger.info("Executing Layer 1: File Summarization", file=str(state.file_path))
        state.current_layer = "layer1"
        return summarize_file(state, self.config)

    def _validate_l1_node(self, state: FileState) -> FileState:
        """Validate Layer 1 output."""
        logger.info("Validating Layer 1", file=str(state.file_path))
        return validate_layer1(state, self.config)

    def _layer2_node(self, state: FileState) -> FileState:
        """Layer 2: Detailed Documentation."""
        logger.info("Executing Layer 2: Detailed Documentation", file=str(state.file_path))
        state.current_layer = "layer2"
        return generate_details(state, self.config)

    def _validate_l2_node(self, state: FileState) -> FileState:
        """Validate Layer 2 output."""
        logger.info("Validating Layer 2", file=str(state.file_path))
        return validate_layer2(state, self.config)

    def _layer3_node(self, state: FileState) -> FileState:
        """Layer 3: Relationship Mapping."""
        logger.info("Executing Layer 3: Relationship Mapping", file=str(state.file_path))
        state.current_layer = "layer3"
        return map_relationships(state, self.config)

    def _validate_l3_node(self, state: FileState) -> FileState:
        """Validate Layer 3 output."""
        logger.info("Validating Layer 3", file=str(state.file_path))
        return validate_layer3(state, self.config)

    def _should_retry_layer1(self, state: FileState) -> Literal["proceed", "retry", "flag"]:
        """
        Determine next step after Layer 1 validation.

        Returns:
            - "proceed": Validation passed, move to Layer 2
            - "retry": Validation failed, retry Layer 1 (if under max iterations)
            - "flag": Max iterations reached, flag for manual review
        """
        if not state.layer1_validation:
            logger.error("Layer 1 validation result missing", file=str(state.file_path))
            state.flagged_for_review = True
            return "flag"

        if state.layer1_validation.passed:
            logger.success("Layer 1 validation passed, proceeding to Layer 2")
            return "proceed"

        # Validation failed
        if state.layer1_iterations >= self.config.max_iterations:
            logger.warning(
                "Layer 1 max iterations reached, flagging for review",
                file=str(state.file_path),
                iterations=state.layer1_iterations
            )
            state.flagged_for_review = True
            return "flag"

        logger.info(
            "Layer 1 validation failed, retrying",
            file=str(state.file_path),
            iteration=state.layer1_iterations,
            issues=len(state.layer1_validation.issues)
        )
        return "retry"

    def _should_retry_layer2(self, state: FileState) -> Literal["proceed", "retry", "flag"]:
        """
        Determine next step after Layer 2 validation.

        Returns:
            - "proceed": Validation passed, move to Layer 3
            - "retry": Validation failed, retry Layer 2 (if under max iterations)
            - "flag": Max iterations reached, flag for manual review
        """
        if not state.layer2_validation:
            logger.error("Layer 2 validation result missing", file=str(state.file_path))
            state.flagged_for_review = True
            return "flag"

        if state.layer2_validation.passed:
            logger.success("Layer 2 validation passed, proceeding to Layer 3")
            return "proceed"

        # Validation failed
        if state.layer2_iterations >= self.config.max_iterations:
            logger.warning(
                "Layer 2 max iterations reached, flagging for review",
                file=str(state.file_path),
                iterations=state.layer2_iterations
            )
            state.flagged_for_review = True
            return "flag"

        logger.info(
            "Layer 2 validation failed, retrying",
            file=str(state.file_path),
            iteration=state.layer2_iterations,
            issues=len(state.layer2_validation.issues)
        )
        return "retry"

    def _should_retry_layer3(self, state: FileState) -> Literal["proceed", "retry", "flag"]:
        """
        Determine next step after Layer 3 validation.

        Returns:
            - "proceed": Validation passed, complete processing
            - "retry": Validation failed, retry Layer 3 (if under max iterations)
            - "flag": Max iterations reached, flag for manual review
        """
        if not state.layer3_validation:
            logger.error("Layer 3 validation result missing", file=str(state.file_path))
            state.flagged_for_review = True
            return "flag"

        if state.layer3_validation.passed:
            logger.success("Layer 3 validation passed, documentation complete")
            return "proceed"

        # Validation failed
        if state.layer3_iterations >= self.config.max_iterations:
            logger.warning(
                "Layer 3 max iterations reached, flagging for review",
                file=str(state.file_path),
                iterations=state.layer3_iterations
            )
            state.flagged_for_review = True
            return "flag"

        logger.info(
            "Layer 3 validation failed, retrying",
            file=str(state.file_path),
            iteration=state.layer3_iterations,
            issues=len(state.layer3_validation.issues)
        )
        return "retry"

    def process_file(self, file_path: Path) -> FileState:
        """
        Process a single C# file through the documentation pipeline.

        Args:
            file_path: Path to the C# file to process

        Returns:
            Final FileState with all documentation layers
        """
        logger.info("Starting documentation pipeline", file=str(file_path))

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file: {e}", file=str(file_path))
            raise

        # Initialize state
        initial_state = FileState(
            file_path=file_path,
            file_content=content
        )

        # Run the graph
        try:
            result = self.graph.invoke(initial_state)

            # LangGraph returns dict, convert back to FileState
            if isinstance(result, dict):
                final_state = FileState(**result)
            else:
                final_state = result

            if final_state.flagged_for_review:
                logger.warning(
                    "File flagged for manual review",
                    file=str(file_path),
                    current_layer=final_state.current_layer
                )
            else:
                logger.success("Documentation pipeline completed successfully", file=str(file_path))

            return final_state

        except Exception as e:
            logger.exception(f"Pipeline execution failed: {e}", file=str(file_path))
            initial_state.error_message = f"Pipeline failed: {str(e)}"
            initial_state.flagged_for_review = True
            return initial_state

    def process_directory(self, directory: Path, pattern: str = "*.cs") -> dict[Path, FileState]:
        """
        Process all C# files in a directory.

        Args:
            directory: Directory containing C# files
            pattern: Glob pattern for file matching (default: "*.cs")

        Returns:
            Dictionary mapping file paths to their final states
        """
        logger.info("Processing directory", directory=str(directory), pattern=pattern)

        results = {}
        files = list(directory.rglob(pattern))

        logger.info(f"Found {len(files)} files to process")

        for file_path in files:
            logger.info(f"Processing file {len(results) + 1}/{len(files)}", file=str(file_path))
            try:
                results[file_path] = self.process_file(file_path)
            except Exception as e:
                logger.error(f"Failed to process file: {e}", file=str(file_path))
                # Create error state
                results[file_path] = FileState(
                    file_path=file_path,
                    file_content="",
                    error_message=str(e),
                    flagged_for_review=True
                )

        # Summary statistics
        total = len(results)
        completed = sum(1 for s in results.values() if not s.flagged_for_review and not s.error_message)
        flagged = sum(1 for s in results.values() if s.flagged_for_review)
        errors = sum(1 for s in results.values() if s.error_message)

        logger.info(
            "Directory processing complete",
            total=total,
            completed=completed,
            flagged=flagged,
            errors=errors
        )

        return results


def create_orchestrator(config: GraphConfig = None) -> DocuGenOrchestrator:
    """
    Factory function to create a configured orchestrator.

    Args:
        config: Optional GraphConfig (uses defaults if not provided)

    Returns:
        Configured DocuGenOrchestrator instance
    """
    if config is None:
        config = GraphConfig()

    return DocuGenOrchestrator(config)
