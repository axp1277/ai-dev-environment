"""
Parser-Led Documentation Workflow - LangGraph Definition

Complete workflow orchestration using LangGraph.

Workflow Steps:
1. START → Parser Agent (parse all C# files)
2. Parser Agent → File Controller (orchestrate per-file processing)
3. File Controller → Compiler Agent (generate final documentation)
4. Compiler Agent → END

The File Controller internally handles:
- Documentation Agent (per file)
- Validation Agent (per file)
- Iterative refinement loop (per file)
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from loguru import logger

from .state import ParserLedState, ParserLedConfig
from .agents.parser_agent import parser_agent_node
from .agents.file_controller import file_controller_node
from .agents.compiler_agent import compiler_agent_node


# Define the workflow graph
def create_parser_led_workflow(config: ParserLedConfig = None, checkpointer=None):
    """
    Create the complete parser-led documentation workflow.

    Args:
        config: Configuration for the workflow
        checkpointer: Optional checkpointer for resumable execution

    Returns:
        Compiled LangGraph workflow
    """
    # Create state graph
    workflow = StateGraph(ParserLedState)

    # Add nodes
    workflow.add_node("parser", parser_agent_node)
    workflow.add_node("file_controller", file_controller_node)
    workflow.add_node("compiler", compiler_agent_node)

    # Define edges
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "file_controller")
    workflow.add_edge("file_controller", "compiler")
    workflow.add_edge("compiler", END)

    # Compile workflow with checkpointing
    if checkpointer is None:
        checkpointer = MemorySaver()

    compiled_workflow = workflow.compile(checkpointer=checkpointer)

    return compiled_workflow


def run_parser_led_workflow(
    directory_path: str,
    config: ParserLedConfig = None,
    output_path: str = None
) -> ParserLedState:
    """
    Run the complete parser-led documentation workflow.

    Args:
        directory_path: Path to C# project directory
        config: Configuration options
        output_path: Optional output path for documentation

    Returns:
        Final workflow state
    """
    logger.info(
        "Starting Parser-Led Documentation Workflow",
        directory=directory_path
    )

    # Initialize configuration
    if config is None:
        config = ParserLedConfig()

    # Initialize state
    initial_state = ParserLedState(
        directory_path=directory_path,
        config=config
    )

    # Create workflow
    workflow = create_parser_led_workflow(config)

    # Execute workflow
    logger.info("Executing workflow...")
    final_state = None

    # Configure thread for checkpointer
    config_dict = {"configurable": {"thread_id": "parser_led_workflow"}}

    for step_output in workflow.stream(initial_state, config_dict):
        # Log progress
        for node_name, state_dict in step_output.items():
            if node_name == "parser":
                logger.info(
                    f"✓ Parser completed: {len(state_dict['structure_snapshots'])} files parsed"
                )
            elif node_name == "file_controller":
                validation_results = state_dict.get('validation_results', {})
                avg_coverage = sum(
                    v.coverage_percentage
                    for v in validation_results.values()
                ) / len(validation_results) if validation_results else 0
                logger.info(
                    f"✓ File Controller completed: {len(state_dict.get('documented_files', {}))} files documented "
                    f"({avg_coverage:.1f}% avg coverage)"
                )
            elif node_name == "compiler":
                logger.info("✓ Compiler completed: Final documentation generated")

            # Convert dict back to ParserLedState
            final_state = ParserLedState(**state_dict)

    # Run compiler with custom output path if provided
    if output_path and final_state:
        final_state = compiler_agent_node(final_state, output_path=output_path)

    logger.info("Workflow execution complete")

    # Print summary
    if final_state and final_state.validation_results:
        complete_files = sum(
            1 for v in final_state.validation_results.values() if v.is_complete
        )
        total_files = len(final_state.validation_results)
        avg_coverage = sum(
            v.coverage_percentage
            for v in final_state.validation_results.values()
        ) / total_files if total_files > 0 else 0

        logger.info(
            "\n" + "="*60 +
            "\nWorkflow Summary" +
            f"\n  Files Processed: {total_files}" +
            f"\n  Complete Files: {complete_files}" +
            f"\n  Average Coverage: {avg_coverage:.1f}%" +
            f"\n  Total Elements: {sum(v.total_elements for v in final_state.validation_results.values())}" +
            f"\n  Documented Elements: {sum(v.documented_elements for v in final_state.validation_results.values())}" +
            "\n" + "="*60
        )

    return final_state


# Export workflow creation
__all__ = [
    "create_parser_led_workflow",
    "run_parser_led_workflow"
]
