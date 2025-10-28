"""
Test Documentation Agent with Parser Agent Integration

This test verifies the full pipeline from parsing to documentation.
"""

import pytest
from pathlib import Path
from loguru import logger

from ..state import ParserLedState, ParserLedConfig
from ..agents.parser_agent import parser_agent_node
from ..agents.documentation_agent import documentation_agent_node


@pytest.fixture
def sample_csharp_project(tmp_path):
    """Create a sample C# project for testing."""
    test_dir = tmp_path / "test_project"
    test_dir.mkdir()

    # Create a sample C# file
    sample_file = test_dir / "Calculator.cs"
    sample_file.write_text("""
namespace MathLibrary
{
    /// <summary>
    /// Basic calculator class
    /// </summary>
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

        private void Reset()
        {
            _lastResult = 0;
        }
    }
}
""")

    return test_dir


def test_documentation_agent_pipeline(sample_csharp_project):
    """Test the full pipeline: parsing -> documentation."""

    # Initialize state
    state = ParserLedState(
        directory_path=str(sample_csharp_project),
        config=ParserLedConfig(
            include_private_members=True,
            llm_model="mistral-nemo:latest"
        )
    )

    logger.info("Testing parser agent...")
    # Run parser agent
    state = parser_agent_node(state)

    # Verify parsing worked
    assert len(state.structure_snapshots) == 1, "Should have parsed 1 file"
    assert "Calculator.cs" in state.structure_snapshots, "Should have Calculator.cs"

    snapshot = state.structure_snapshots["Calculator.cs"]
    assert len(snapshot.classes) == 1, "Should have 1 class"
    assert snapshot.classes[0].name == "Calculator"
    assert snapshot.namespace == "MathLibrary"

    logger.info("Testing documentation agent...")
    # Run documentation agent
    state = documentation_agent_node(state)

    # Verify documentation was generated
    assert len(state.documented_files) == 1, "Should have documented 1 file"
    assert "Calculator.cs" in state.documented_files

    file_doc = state.documented_files["Calculator.cs"]
    assert file_doc.namespace == "MathLibrary"
    assert "Calculator" in file_doc.classes

    calc_doc = file_doc.classes["Calculator"]
    assert calc_doc.name == "Calculator"
    assert len(calc_doc.description) > 0, "Should have class description"
    assert len(calc_doc.purpose) > 0, "Should have class purpose"

    # Check methods were documented
    assert "Add" in calc_doc.methods, "Should have Add method"
    assert "Subtract" in calc_doc.methods, "Should have Subtract method"

    add_method = calc_doc.methods["Add"]
    assert add_method.name == "Add"
    assert len(add_method.description) > 0, "Should have method description"
    assert "a" in add_method.parameters, "Should document parameter 'a'"
    assert "b" in add_method.parameters, "Should document parameter 'b'"
    # Note: returns field may be None if LLM doesn't provide it, but description and params are present

    # Check properties were documented
    assert "LastResult" in calc_doc.properties, "Should have LastResult property"

    # Check fields were documented
    assert "_lastResult" in calc_doc.fields, "Should have _lastResult field"

    # Check private method was documented (include_private_members=True)
    assert "Reset" in calc_doc.methods, "Should have private Reset method"

    logger.info("Documentation agent test passed!")
    logger.info(f"Documented class: {calc_doc.name}")
    logger.info(f"Class description: {calc_doc.description}")
    logger.info(f"Class purpose: {calc_doc.purpose}")
    logger.info(f"Methods: {list(calc_doc.methods.keys())}")
    logger.info(f"Properties: {list(calc_doc.properties.keys())}")
    logger.info(f"Fields: {list(calc_doc.fields.keys())}")


def test_exclude_private_members(sample_csharp_project):
    """Test that private members can be excluded."""

    state = ParserLedState(
        directory_path=str(sample_csharp_project),
        config=ParserLedConfig(
            include_private_members=False,  # Exclude private members
            llm_model="mistral-nemo:latest"
        )
    )

    # Run pipeline
    state = parser_agent_node(state)
    state = documentation_agent_node(state)

    # Verify private members were excluded
    calc_doc = state.documented_files["Calculator.cs"].classes["Calculator"]

    assert "Reset" not in calc_doc.methods, "Private method should not be documented"
    assert "_lastResult" not in calc_doc.fields, "Private field should not be documented"

    # Public members should still be there
    assert "Add" in calc_doc.methods, "Public method should be documented"
    assert "LastResult" in calc_doc.properties, "Public property should be documented"

    logger.info("Private member exclusion test passed!")


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
        private int _lastResult;

        public int LastResult { get; set; }

        public int Add(int a, int b)
        {
            _lastResult = a + b;
            return _lastResult;
        }
    }
}
""")

        # Run test
        test_documentation_agent_pipeline(test_dir)
