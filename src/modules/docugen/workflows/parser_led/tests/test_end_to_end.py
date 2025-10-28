"""
End-to-End Workflow Test

Tests the complete parser-led documentation pipeline from parsing to final output.
"""

import pytest
from pathlib import Path
from loguru import logger

from ..state import ParserLedState, ParserLedConfig
from ..agents.parser_agent import parser_agent_node
from ..agents.file_controller import file_controller_node
from ..agents.compiler_agent import compiler_agent_node


@pytest.fixture
def sample_csharp_project(tmp_path):
    """Create a sample C# project with multiple files."""
    test_dir = tmp_path / "test_project"
    test_dir.mkdir()

    # Create multiple C# files
    # File 1: Calculator
    (test_dir / "Calculator.cs").write_text("""
namespace MathLibrary
{
    public class Calculator
    {
        public int Add(int a, int b)
        {
            return a + b;
        }

        public int Multiply(int a, int b)
        {
            return a * b;
        }
    }
}
""")

    # File 2: StringHelper
    (test_dir / "StringHelper.cs").write_text("""
namespace TextUtilities
{
    public class StringHelper
    {
        public string ToUpperCase(string input)
        {
            return input.ToUpper();
        }

        public string Reverse(string input)
        {
            char[] chars = input.ToCharArray();
            Array.Reverse(chars);
            return new string(chars);
        }
    }
}
""")

    # Create Services subdirectory
    services_dir = test_dir / "Services"
    services_dir.mkdir()

    # File 3: Logger in Services
    (services_dir / "Logger.cs").write_text("""
namespace MathLibrary.Services
{
    public class Logger
    {
        public void Log(string message)
        {
            Console.WriteLine(message);
        }

        public void Error(string error)
        {
            Console.Error.WriteLine(error);
        }
    }
}
""")

    return test_dir


def test_end_to_end_workflow(sample_csharp_project):
    """Test the complete workflow from parsing to final documentation."""

    logger.info(f"Testing end-to-end workflow with project: {sample_csharp_project}")

    # Initialize state
    state = ParserLedState(
        directory_path=str(sample_csharp_project),
        config=ParserLedConfig(
            include_private_members=False,  # Only public for faster test
            llm_model="mistral-nemo:latest",
            max_validation_iterations=2
        )
    )

    # Phase 1: Run parser agent
    logger.info("Phase 1: Parsing...")
    state = parser_agent_node(state)

    # Verify parsing
    assert len(state.structure_snapshots) == 3, "Should have parsed 3 files"
    assert "Calculator.cs" in state.structure_snapshots
    assert "StringHelper.cs" in state.structure_snapshots
    assert "Services/Logger.cs" in state.structure_snapshots

    logger.info(f"Parsed {len(state.structure_snapshots)} files")

    # Phase 2-3: Run file controller (handles documentation + validation)
    logger.info("Phase 2-3: Documentation and Validation...")
    state = file_controller_node(state)

    # Verify documentation
    assert len(state.documented_files) == 3, "Should have documented 3 files"
    assert len(state.validation_results) == 3, "Should have validation results for 3 files"

    # Check validation metrics
    for file_path, validation in state.validation_results.items():
        logger.info(
            f"File: {file_path}",
            coverage=f"{validation.coverage_percentage:.1f}%",
            complete=validation.is_complete
        )
        assert validation.coverage_percentage > 0, f"{file_path} should have coverage"

    # Phase 4: Run compiler agent
    logger.info("Phase 4: Compiling final documentation...")
    output_path = sample_csharp_project / "documentation"
    state = compiler_agent_node(state, output_path=str(output_path))

    # Verify output files
    assert output_path.exists(), "Documentation directory should exist"

    main_doc = output_path / "documentation.md"
    assert main_doc.exists(), "Main documentation file should exist"

    per_file_dir = output_path / "files"
    assert per_file_dir.exists(), "Per-file documentation directory should exist"

    # Verify content
    with open(main_doc, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for key sections
    assert "# Code Documentation" in content, "Should have main header"
    assert "# Documentation Summary" in content, "Should have summary"
    assert "# Table of Contents" in content, "Should have TOC"
    assert "# Detailed Documentation" in content, "Should have detailed section"

    # Check for documented classes
    assert "Calculator" in content, "Should document Calculator class"
    assert "StringHelper" in content, "Should document StringHelper class"
    assert "Logger" in content, "Should document Logger class"

    # Check for methods
    assert "Add" in content, "Should document Add method"
    assert "Multiply" in content, "Should document Multiply method"
    assert "ToUpperCase" in content, "Should document ToUpperCase method"
    assert "Reverse" in content, "Should document Reverse method"
    assert "Log" in content, "Should document Log method"
    assert "Error" in content, "Should document Error method"

    # Check coverage metrics in content
    assert "Overall Metrics" in content, "Should have overall metrics"
    assert "Total Files:** 3" in content, "Should report 3 files"

    logger.info(f"Documentation size: {len(content) / 1024:.1f} KB")
    logger.info(f"Output location: {main_doc}")

    # Verify per-file documentation
    per_file_docs = list(per_file_dir.glob("*.md"))
    assert len(per_file_docs) == 3, "Should have 3 per-file documentation files"

    logger.info("End-to-end workflow test passed!")


def test_workflow_with_incomplete_coverage(sample_csharp_project):
    """Test workflow behavior with incomplete coverage (max iterations)."""

    state = ParserLedState(
        directory_path=str(sample_csharp_project),
        config=ParserLedConfig(
            include_private_members=False,
            llm_model="mistral-nemo:latest",
            max_validation_iterations=1  # Limited iterations
        )
    )

    # Run full workflow
    state = parser_agent_node(state)
    state = file_controller_node(state)

    # Even with limited iterations, should complete
    assert len(state.documented_files) > 0, "Should have documentation"
    assert len(state.validation_results) > 0, "Should have validation results"

    # Compile documentation
    output_path = sample_csharp_project / "documentation_limited"
    state = compiler_agent_node(state, output_path=str(output_path))

    # Verify output exists
    main_doc = output_path / "documentation.md"
    assert main_doc.exists(), "Should create documentation even with incomplete coverage"

    with open(main_doc, 'r', encoding='utf-8') as f:
        content = f.read()

    # Should still have structure
    assert "# Code Documentation" in content
    assert "# Documentation Summary" in content

    logger.info("Workflow with limited iterations test passed!")


if __name__ == "__main__":
    # Run test manually for debugging
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create sample project
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()

        (test_dir / "Calculator.cs").write_text("""
namespace MathLibrary
{
    public class Calculator
    {
        public int Add(int a, int b) { return a + b; }
    }
}
""")

        # Run test
        test_end_to_end_workflow(test_dir)
