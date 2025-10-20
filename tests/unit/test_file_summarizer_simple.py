"""
Simple unit tests for FileSummarizerAgent that don't require Ollama.

Tests agent structure, configuration, and preparatory methods.
"""

import pytest
from pathlib import Path

from src.modules.docugen.agents.file_summarizer_agent import FileSummarizerAgent
from src.modules.docugen.state import FileState, GraphConfig


@pytest.fixture
def test_config():
    """Create test configuration."""
    return GraphConfig(
        summarizer_model="codellama:7b",
        summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md")
    )


@pytest.fixture
def agent(test_config):
    """Create agent instance."""
    return FileSummarizerAgent(test_config)


@pytest.fixture
def sample_csharp_code():
    """Sample C# code for testing."""
    return """
using System;

namespace TestNamespace
{
    public class TestClass
    {
        public void TestMethod()
        {
            Console.WriteLine("Hello World");
        }
    }
}
"""


class TestAgentStructure:
    """Test agent follows Four Pillars pattern."""

    def test_pillar_1_model_configuration(self, agent):
        """Test Pillar 1: Model is properly configured."""
        assert agent.model_name == "codellama:7b"
        assert isinstance(agent.model_name, str)

    def test_pillar_2_prompt_loaded(self, agent):
        """Test Pillar 2: Prompt is loaded from external file."""
        assert agent.prompt_path == Path("src/modules/docugen/prompts/file_summarizer.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100

        # Verify prompt contains key instructions
        assert "File Summarizer" in agent.system_prompt
        assert "JSON" in agent.system_prompt.upper()

    def test_pillar_3_context_preparation(self, agent, sample_csharp_code):
        """Test Pillar 3: Context handler properly formats input."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content=sample_csharp_code
        )

        context = agent._prepare_context(state)

        # Verify context includes necessary information
        assert "Test.cs" in context
        assert "TestClass" in context  # Should include code
        assert "```csharp" in context  # Should use code blocks
        assert "JSON" in context.upper()  # Should mention JSON output

    def test_pillar_4_tools_none_for_this_agent(self, agent):
        """Test Pillar 4: This agent uses no external tools (LLM only)."""
        # This agent analyzes code directly via LLM, no external tools
        # Just verify agent has required methods
        assert hasattr(agent, 'invoke')
        assert hasattr(agent, '_prepare_context')
        assert hasattr(agent, '_parse_response')
        assert hasattr(agent, '_load_prompt')


class TestContextPreparation:
    """Test context preparation method."""

    def test_context_includes_filename(self, agent):
        """Test context includes file name."""
        state = FileState(
            file_path=Path("/some/path/MyService.cs"),
            file_content="using System;"
        )

        context = agent._prepare_context(state)
        assert "MyService.cs" in context

    def test_context_includes_full_path(self, agent):
        """Test context includes full path."""
        state = FileState(
            file_path=Path("/project/src/Services/UserService.cs"),
            file_content="using System;"
        )

        context = agent._prepare_context(state)
        assert "/project/src/Services/UserService.cs" in context

    def test_context_includes_code(self, agent, sample_csharp_code):
        """Test context includes the actual code."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content=sample_csharp_code
        )

        context = agent._prepare_context(state)
        assert "TestClass" in context
        assert "TestMethod" in context

    def test_context_uses_csharp_code_blocks(self, agent, sample_csharp_code):
        """Test context uses proper code formatting."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content=sample_csharp_code
        )

        context = agent._prepare_context(state)
        assert "```csharp" in context


class TestAgentConfiguration:
    """Test agent configuration handling."""

    def test_custom_model_name(self):
        """Test agent accepts custom model name."""
        custom_config = GraphConfig(
            summarizer_model="custom-model:latest",
            summarizer_prompt_path=Path("src/modules/docugen/prompts/file_summarizer.md")
        )

        agent = FileSummarizerAgent(custom_config)
        assert agent.model_name == "custom-model:latest"

    def test_missing_prompt_file_raises_error(self):
        """Test that missing prompt file is caught."""
        invalid_config = GraphConfig(
            summarizer_prompt_path=Path("nonexistent/file.md")
        )

        with pytest.raises(FileNotFoundError):
            FileSummarizerAgent(invalid_config)


class TestStateManagement:
    """Test state handling."""

    def test_state_creation(self):
        """Test creating FileState with required fields."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;"
        )

        assert state.file_path == Path("test.cs")
        assert state.file_content == "using System;"
        assert state.layer1_summary is None
        assert state.layer1_iterations == 0
        assert state.error_message is None

    def test_state_tracks_iterations(self):
        """Test that state properly tracks iteration count."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;"
        )

        assert state.layer1_iterations == 0

        # Simulate iteration increment (this would happen in invoke())
        state.layer1_iterations += 1
        assert state.layer1_iterations == 1

        state.layer1_iterations += 1
        assert state.layer1_iterations == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
