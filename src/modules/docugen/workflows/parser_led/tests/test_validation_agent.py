"""
Test Validation Agent with gap detection and refinement.
"""

import pytest
from pathlib import Path
from loguru import logger

from ..state import (
    ParserLedState,
    ParserLedConfig,
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod
)
from ..agents.parser_agent import parser_agent_node
from ..agents.documentation_agent import documentation_agent_node
from ..agents.validation_agent import (
    validation_agent_node,
    detect_gaps,
    calculate_coverage
)


@pytest.fixture
def incomplete_documentation_project(tmp_path):
    """Create a C# project with a class that has methods we'll intentionally not document."""
    test_dir = tmp_path / "test_project"
    test_dir.mkdir()

    # Create a C# file with multiple methods
    sample_file = test_dir / "Calculator.cs"
    sample_file.write_text("""
namespace MathLibrary
{
    public class Calculator
    {
        private int _lastResult;

        public int LastResult { get; set; }

        public Calculator()
        {
            _lastResult = 0;
        }

        public int Add(int a, int b)
        {
            _lastResult = a + b;
            return _lastResult;
        }

        public int Subtract(int a, int b)
        {
            _lastResult = a - b;
            return _lastResult;
        }

        public int Multiply(int a, int b)
        {
            _lastResult = a * b;
            return _lastResult;
        }

        private void Reset()
        {
            _lastResult = 0;
        }
    }
}
""")

    return test_dir


def test_gap_detection(incomplete_documentation_project):
    """Test that gap detection identifies missing documentation."""

    # Initialize state and run parser
    state = ParserLedState(
        directory_path=str(incomplete_documentation_project),
        config=ParserLedConfig(
            include_private_members=True,
            llm_model="mistral-nemo:latest"
        )
    )

    state = parser_agent_node(state)

    # Create intentionally incomplete documentation (only document Add, not Subtract/Multiply/Reset)
    file_doc = FileDocumentation(
        file_path="Calculator.cs",
        namespace="MathLibrary"
    )

    # Document class
    calc_doc = DocumentedClass(
        name="Calculator",
        description="A calculator class",
        purpose="Perform calculations"
    )

    # Only document Add method
    calc_doc.methods["Add"] = DocumentedMethod(
        name="Add",
        description="Adds two numbers",
        parameters={"a": "First number", "b": "Second number"},
        returns="Sum of a and b"
    )

    # Document constructor
    calc_doc.methods["Calculator"] = DocumentedMethod(
        name="Calculator",
        description="Constructor",
        parameters={},
        returns=None
    )

    file_doc.classes["Calculator"] = calc_doc

    # Put incomplete doc in state
    state.documented_files["Calculator.cs"] = file_doc

    # Detect gaps
    snapshot = state.structure_snapshots["Calculator.cs"]
    gaps = detect_gaps(snapshot, file_doc, include_private=True)

    logger.info(f"Detected {len(gaps)} gaps")
    for gap in gaps:
        logger.info(f"  Gap: {gap.element_type} '{gap.element_name}' - {gap.reason}")

    # Should detect missing methods: Subtract, Multiply, Reset
    gap_methods = [g.element_name for g in gaps if g.element_type == "method"]
    assert "Subtract" in gap_methods, "Should detect missing Subtract method"
    assert "Multiply" in gap_methods, "Should detect missing Multiply method"
    assert "Reset" in gap_methods, "Should detect missing Reset method"

    # Should detect missing property: LastResult
    gap_properties = [g.element_name for g in gaps if g.element_type == "property"]
    assert "LastResult" in gap_properties, "Should detect missing LastResult property"

    # Should detect missing field: _lastResult
    gap_fields = [g.element_name for g in gaps if g.element_type == "field"]
    assert "_lastResult" in gap_fields, "Should detect missing _lastResult field"


def test_coverage_calculation(incomplete_documentation_project):
    """Test coverage calculation."""

    state = ParserLedState(
        directory_path=str(incomplete_documentation_project),
        config=ParserLedConfig(
            include_private_members=True,
            llm_model="mistral-nemo:latest"
        )
    )

    state = parser_agent_node(state)

    # Create partial documentation
    file_doc = FileDocumentation(
        file_path="Calculator.cs",
        namespace="MathLibrary"
    )

    calc_doc = DocumentedClass(
        name="Calculator",
        description="A calculator class",
        purpose="Perform calculations"
    )

    # Document only Add method
    calc_doc.methods["Add"] = DocumentedMethod(
        name="Add",
        description="Adds two numbers",
        parameters={"a": "First number", "b": "Second number"},
        returns="Sum"
    )

    file_doc.classes["Calculator"] = calc_doc
    snapshot = state.structure_snapshots["Calculator.cs"]

    # Calculate coverage
    total, documented, coverage = calculate_coverage(snapshot, file_doc, include_private=True)

    logger.info(f"Coverage: {coverage:.1f}% ({documented}/{total} elements)")

    assert total > 0, "Should have elements to document"
    assert documented < total, "Should have incomplete documentation"
    assert coverage < 100, "Coverage should be less than 100%"
    # We documented: 1 class + 1 method (Add) = 2 elements
    # Total should be: 1 class + 5 methods (Calculator constructor, Add, Subtract, Multiply, Reset) + 1 property (LastResult) + 1 field (_lastResult) = 8 elements
    assert total == 8, f"Should have 8 total elements, got {total}"
    assert documented == 2, f"Should have 2 documented elements (class + Add method), got {documented}"


def test_validation_agent_refinement(incomplete_documentation_project):
    """Test the full validation agent with refinement."""

    # Initialize state
    state = ParserLedState(
        directory_path=str(incomplete_documentation_project),
        config=ParserLedConfig(
            include_private_members=False,  # Exclude private to speed up test
            llm_model="mistral-nemo:latest",
            max_validation_iterations=2  # Limit iterations for test
        )
    )

    # Run parser
    logger.info("Running parser agent...")
    state = parser_agent_node(state)

    # Run documentation agent (will document everything initially)
    logger.info("Running documentation agent...")
    state = documentation_agent_node(state)

    # Get initial coverage
    initial_file_doc = state.documented_files["Calculator.cs"]
    initial_snapshot = state.structure_snapshots["Calculator.cs"]
    initial_total, initial_documented, initial_coverage = calculate_coverage(
        initial_snapshot, initial_file_doc, include_private=False
    )

    logger.info(f"Initial coverage: {initial_coverage:.1f}% ({initial_documented}/{initial_total})")

    # Artificially remove some documentation to test refinement
    # Remove Multiply method
    if "Calculator" in initial_file_doc.classes:
        calc_doc = initial_file_doc.classes["Calculator"]
        if "Multiply" in calc_doc.methods:
            del calc_doc.methods["Multiply"]
            logger.info("Removed Multiply method to test refinement")

    # Calculate coverage after removal
    removed_total, removed_documented, removed_coverage = calculate_coverage(
        initial_snapshot, initial_file_doc, include_private=False
    )
    logger.info(f"After removal: {removed_coverage:.1f}% ({removed_documented}/{removed_total})")

    assert removed_coverage < initial_coverage, "Coverage should decrease after removal"

    # Run validation agent (should detect gap and refine)
    logger.info("Running validation agent...")
    state = validation_agent_node(state)

    # Check validation results
    assert "Calculator.cs" in state.validation_results, "Should have validation results"

    validation_result = state.validation_results["Calculator.cs"]
    logger.info(
        f"Validation complete",
        coverage=f"{validation_result.coverage_percentage:.1f}%",
        missing=validation_result.missing_elements,
        is_complete=validation_result.is_complete
    )

    # After refinement, Multiply should be back
    refined_file_doc = state.documented_files["Calculator.cs"]
    if "Calculator" in refined_file_doc.classes:
        calc_doc = refined_file_doc.classes["Calculator"]
        assert "Multiply" in calc_doc.methods, "Multiply method should be refined"
        logger.info(f"Multiply method description: {calc_doc.methods['Multiply'].description}")

    # Coverage should improve after refinement
    assert validation_result.coverage_percentage > removed_coverage, "Coverage should improve after refinement"

    logger.info("Validation agent test passed!")


if __name__ == "__main__":
    # Run tests manually for debugging
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create sample project
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()

        sample_file = test_dir / "Calculator.cs"
        sample_file.write_text("""
namespace MathLibrary
{
    public class Calculator
    {
        public int Add(int a, int b) { return a + b; }
        public int Multiply(int a, int b) { return a * b; }
    }
}
""")

        # Run gap detection test
        test_gap_detection(test_dir)
