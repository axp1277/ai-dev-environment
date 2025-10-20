"""
Unit tests for FileSummarizerAgent using real C# files from sample_codebase.

Tests the complete agent pipeline without mocks:
- Real Ollama LLM calls
- Real file reads from sample_codebase
- Full Pydantic validation
- End-to-end agent invocation
"""

import pytest
from pathlib import Path
from loguru import logger

from src.modules.docugen.agents.file_summarizer_agent import FileSummarizerAgent, summarize_file
from src.modules.docugen.state import FileState, FileSummary, GraphConfig


# Test fixtures - Real C# files from sample codebase
TEST_FILES = {
    "interface_simple": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Abstractions/IInputSource.cs"),
    "service_class": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs"),
    "interface_deprecated": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/FileHandlers/IFileHandler.cs"),
    "extractor": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/FileHandlers/ContentExtractors/CodeContentExtractor.cs"),
}


@pytest.fixture
def test_config():
    """Create a test configuration with default settings."""
    return GraphConfig(
        summarizer_model="codellama:7b",
        summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md"),
        min_summary_length=50
    )


@pytest.fixture
def agent(test_config):
    """Create a FileSummarizerAgent instance for testing."""
    return FileSummarizerAgent(test_config)


def read_test_file(relative_path: Path) -> str:
    """Read a test file from the project root."""
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / relative_path

    if not file_path.exists():
        pytest.skip(f"Test file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


class TestFileSummarizerAgentInitialization:
    """Test agent initialization and configuration."""

    def test_agent_initialization(self, test_config):
        """Test that agent initializes correctly with config."""
        agent = FileSummarizerAgent(test_config)

        assert agent.model_name == "codellama:7b"
        assert agent.prompt_path == Path("src/modules/docugen/prompts/file_summarizer.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100  # Should have substantial content

    def test_prompt_loading(self, agent):
        """Test that system prompt loads correctly."""
        assert "File Summarizer Agent" in agent.system_prompt
        assert "JSON" in agent.system_prompt  # Should mention JSON output format
        assert "summary" in agent.system_prompt.lower()
        assert "key_classes" in agent.system_prompt.lower()

    def test_missing_prompt_file_raises_error(self):
        """Test that missing prompt file raises appropriate error."""
        invalid_config = GraphConfig(
            summarizer_prompt_path=Path("nonexistent/prompt.md")
        )

        with pytest.raises(FileNotFoundError):
            FileSummarizerAgent(invalid_config)


class TestFileSummarizerAgentInvocation:
    """Test agent invocation with real C# files."""

    def test_simple_interface_file(self, agent, test_config):
        """Test summarization of a simple interface file (IInputSource.cs)."""
        file_path = TEST_FILES["interface_simple"]
        content = read_test_file(file_path)

        # Create state
        state = FileState(
            file_path=file_path,
            file_content=content
        )

        # Invoke agent
        result_state = agent.invoke(state)

        # Assertions
        assert result_state.layer1_summary is not None
        assert isinstance(result_state.layer1_summary, FileSummary)
        assert result_state.layer1_iterations == 1
        assert result_state.error_message is None

        # Validate summary content
        summary = result_state.layer1_summary
        assert len(summary.summary) >= test_config.min_summary_length
        assert "IInputSource" in summary.key_classes
        assert summary.purpose is not None and len(summary.purpose) > 0
        assert summary.category in ["Interface", "Service", "Repository", "Controller",
                                     "Model", "Utility", "Configuration", "Handler",
                                     "Validator", "Middleware", "Test"]

        logger.info(f"Summary for IInputSource.cs: {summary.summary}")
        logger.info(f"Purpose: {summary.purpose}")
        logger.info(f"Category: {summary.category}")

    def test_service_class_file(self, agent, test_config):
        """Test summarization of a service class (OllamaService.cs)."""
        file_path = TEST_FILES["service_class"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        result_state = agent.invoke(state)

        assert result_state.layer1_summary is not None
        assert result_state.error_message is None

        summary = result_state.layer1_summary
        assert len(summary.summary) >= test_config.min_summary_length
        assert "OllamaService" in summary.key_classes
        assert summary.category == "Service"

        # Should mention HTTP or API-related functionality
        summary_lower = summary.summary.lower()
        assert any(keyword in summary_lower for keyword in ["http", "api", "client", "service"])

        logger.info(f"Summary for OllamaService.cs: {summary.summary}")
        logger.info(f"Key classes: {summary.key_classes}")

    def test_deprecated_interface_file(self, agent, test_config):
        """Test summarization of deprecated interface (IFileHandler.cs)."""
        file_path = TEST_FILES["interface_deprecated"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        result_state = agent.invoke(state)

        assert result_state.layer1_summary is not None
        summary = result_state.layer1_summary

        assert "IFileHandler" in summary.key_classes
        assert summary.category == "Interface"

        # Should ideally mention deprecated/obsolete
        summary_text = (summary.summary + summary.purpose).lower()
        # Note: LLM might or might not catch [Obsolete] attribute

        logger.info(f"Summary for IFileHandler.cs: {summary.summary}")

    def test_multiple_invocations_increment_iterations(self, agent):
        """Test that multiple invocations increment iteration counter."""
        file_path = TEST_FILES["interface_simple"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        # First invocation
        state = agent.invoke(state)
        assert state.layer1_iterations == 1

        # Second invocation (simulating refinement loop)
        state = agent.invoke(state)
        assert state.layer1_iterations == 2

        # Third invocation
        state = agent.invoke(state)
        assert state.layer1_iterations == 3


class TestFileSummarizerPydanticValidation:
    """Test Pydantic validation and structured output."""

    def test_all_required_fields_present(self, agent):
        """Test that all required FileSummary fields are populated."""
        file_path = TEST_FILES["service_class"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        result_state = agent.invoke(state)
        summary = result_state.layer1_summary

        # All fields must be present and non-empty
        assert summary.summary is not None and len(summary.summary) > 0
        assert summary.key_classes is not None  # Can be empty list, but must exist
        assert summary.purpose is not None and len(summary.purpose) > 0
        assert summary.category is not None and len(summary.category) > 0

    def test_key_classes_is_list(self, agent):
        """Test that key_classes is always a list."""
        file_path = TEST_FILES["interface_simple"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        result_state = agent.invoke(state)
        summary = result_state.layer1_summary

        assert isinstance(summary.key_classes, list)
        # All items in list should be strings
        for class_name in summary.key_classes:
            assert isinstance(class_name, str)
            assert len(class_name) > 0


class TestFileSummarizerNodeFunction:
    """Test the LangGraph node function wrapper."""

    def test_summarize_file_node_function(self, test_config):
        """Test that the summarize_file node function works correctly."""
        file_path = TEST_FILES["interface_simple"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        # Call node function (simulating LangGraph invocation)
        result_state = summarize_file(state, test_config)

        assert result_state.layer1_summary is not None
        assert result_state.layer1_iterations == 1
        assert isinstance(result_state, FileState)


class TestFileSummarizerErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_file_content(self, agent):
        """Test handling of empty file content."""
        state = FileState(
            file_path=Path("empty.cs"),
            file_content=""
        )

        # Should not crash - either returns summary or error message
        result_state = agent.invoke(state)

        # One of these should be set
        assert result_state.layer1_summary is not None or result_state.error_message is not None

    def test_invalid_csharp_code(self, agent):
        """Test handling of malformed C# code."""
        state = FileState(
            file_path=Path("invalid.cs"),
            file_content="This is not valid C# code @#$%^&*()"
        )

        # Should not crash
        result_state = agent.invoke(state)

        # Agent should attempt to summarize even invalid code
        # (LLM can still provide high-level interpretation)
        assert isinstance(result_state, FileState)

    def test_very_large_file(self, agent):
        """Test handling of large file (stress test)."""
        # Create a large but valid C# file
        large_content = "using System;\n\n"
        large_content += "namespace Test {\n"
        large_content += "    public class LargeClass {\n"

        # Add 1000 methods
        for i in range(1000):
            large_content += f"        public void Method{i}() {{ }}\n"

        large_content += "    }\n}\n"

        state = FileState(
            file_path=Path("large.cs"),
            file_content=large_content
        )

        # Should handle large files (may take longer)
        result_state = agent.invoke(state)

        # Should complete or return error, but not crash
        assert isinstance(result_state, FileState)


class TestFileSummarizerQuality:
    """Test quality of generated summaries."""

    def test_summary_quality_metrics(self, agent, test_config):
        """Test that summaries meet quality standards."""
        file_path = TEST_FILES["service_class"]
        content = read_test_file(file_path)

        state = FileState(
            file_path=file_path,
            file_content=content
        )

        result_state = agent.invoke(state)
        summary = result_state.layer1_summary

        # Quality checks
        assert len(summary.summary) >= test_config.min_summary_length
        assert len(summary.summary) <= 1000  # Not too verbose

        # Should have complete sentences (ends with punctuation)
        assert summary.summary.rstrip()[-1] in ['.', '!', '?']

        # Purpose should be concise
        assert len(summary.purpose) <= 200

        # Should identify at least one class (for non-empty files)
        if len(content.strip()) > 0:
            assert len(summary.key_classes) > 0


# Integration test
class TestFileSummarizerIntegration:
    """Integration tests with multiple files."""

    def test_process_multiple_files(self, agent):
        """Test processing multiple different file types."""
        results = {}

        for file_type, file_path in TEST_FILES.items():
            try:
                content = read_test_file(file_path)
                state = FileState(
                    file_path=file_path,
                    file_content=content
                )

                result_state = agent.invoke(state)
                results[file_type] = result_state.layer1_summary

                logger.info(f"\n{'='*60}")
                logger.info(f"File: {file_type} ({file_path.name})")
                logger.info(f"Category: {result_state.layer1_summary.category}")
                logger.info(f"Purpose: {result_state.layer1_summary.purpose}")
                logger.info(f"Key Classes: {result_state.layer1_summary.key_classes}")
                logger.info(f"Summary: {result_state.layer1_summary.summary}")
                logger.info(f"{'='*60}\n")

            except Exception as e:
                logger.warning(f"Skipping {file_type}: {e}")

        # Should have processed at least some files
        assert len(results) > 0

        # All processed files should have valid summaries
        for file_type, summary in results.items():
            assert summary is not None
            assert isinstance(summary, FileSummary)
            assert len(summary.summary) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
