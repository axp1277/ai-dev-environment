"""
Test parser-led documentation workflow with RepoScribe codebase.
"""

from pathlib import Path
from loguru import logger

from src.modules.docugen.workflows.parser_led.state import ParserLedState, ParserLedConfig
from src.modules.docugen.workflows.parser_led.agents.parser_agent import parser_agent_node
from src.modules.docugen.workflows.parser_led.agents.documentation_agent import documentation_agent_node


def test_reposcribe_documentation():
    """Test documentation generation on RepoScribe.Core codebase."""

    reposcribe_path = Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core")

    if not reposcribe_path.exists():
        logger.error(f"RepoScribe directory not found: {reposcribe_path}")
        return

    logger.info(f"Testing documentation generation on: {reposcribe_path}")

    # Initialize state
    state = ParserLedState(
        directory_path=str(reposcribe_path),
        config=ParserLedConfig(
            include_private_members=False,  # Only public members for cleaner output
            llm_model="mistral-nemo:latest"
        )
    )

    # Run parser agent
    logger.info("Running Parser Agent...")
    state = parser_agent_node(state)

    logger.info(f"Parsed {len(state.structure_snapshots)} files")
    logger.info(f"Total classes: {sum(len(s.classes) for s in state.structure_snapshots.values())}")

    # Limit to first 2 files with actual classes for testing (to save time)
    if state.structure_snapshots:
        logger.info("Limiting to first 2 files with classes for testing...")
        files_with_classes = [f for f, s in state.structure_snapshots.items() if len(s.classes) > 0]
        files_to_keep = files_with_classes[:2]

        limited_snapshots = {f: state.structure_snapshots[f] for f in files_to_keep}
        state.structure_snapshots = limited_snapshots

        logger.info(f"Testing with files: {files_to_keep}")

    # Run documentation agent
    logger.info("Running Documentation Agent...")
    state = documentation_agent_node(state)

    logger.info(f"Documented {len(state.documented_files)} files")

    # Display sample documentation
    for file_path, file_doc in state.documented_files.items():
        logger.info(f"\n{'=' * 80}")
        logger.info(f"File: {file_path}")
        logger.info(f"Namespace: {file_doc.namespace}")
        logger.info(f"Classes: {len(file_doc.classes)}")

        for class_name, class_doc in file_doc.classes.items():
            logger.info(f"\n  Class: {class_name}")
            logger.info(f"  Description: {class_doc.description[:200]}...")
            logger.info(f"  Purpose: {class_doc.purpose}")
            logger.info(f"  Methods: {len(class_doc.methods)}")
            logger.info(f"  Properties: {len(class_doc.properties)}")
            logger.info(f"  Fields: {len(class_doc.fields)}")

            # Show one method as example
            if class_doc.methods:
                method_name = list(class_doc.methods.keys())[0]
                method_doc = class_doc.methods[method_name]
                logger.info(f"\n    Example Method: {method_name}")
                logger.info(f"    Description: {method_doc.description}")
                if method_doc.parameters:
                    logger.info(f"    Parameters:")
                    for param, desc in method_doc.parameters.items():
                        logger.info(f"      - {param}: {desc}")
                if method_doc.returns:
                    logger.info(f"    Returns: {method_doc.returns}")

    logger.info(f"\n{'=' * 80}")
    logger.info("Documentation generation complete!")


if __name__ == "__main__":
    test_reposcribe_documentation()
