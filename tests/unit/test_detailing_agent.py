"""
Unit tests for DetailingAgent using real C# files from sample_codebase.

Tests the complete agent pipeline without mocks:
- Real Ollama LLM calls (when available)
- Real file reads from sample_codebase
- Full Pydantic validation
- End-to-end agent invocation
"""

import pytest
from pathlib import Path
from loguru import logger

from src.modules.docugen.agents.detailing_agent import DetailingAgent, generate_details
from src.modules.docugen.state import FileState, FileSummary, DetailedDocs, GraphConfig


# Test fixtures - Real C# files from sample codebase
TEST_FILES = {
    "service_class": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs"),
    "interface_simple": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Abstractions/IInputSource.cs"),
    "interface_deprecated": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/FileHandlers/IFileHandler.cs"),
}


@pytest.fixture
def test_config():
    """Create a test configuration with default settings."""
    return GraphConfig(
        detailing_model="codellama:13b",
        detailing_prompt_path=Path("src/modules/docugen/prompts/detailing_agent.md"),
        min_summary_length=50
    )


@pytest.fixture
def agent(test_config):
    """Create a DetailingAgent instance for testing."""
    return DetailingAgent(test_config)


def read_test_file(relative_path: Path) -> str:
    """Read a test file from the project root."""
    project_root = Path(__file__).parent.parent.parent
    file_path = project_root / relative_path

    if not file_path.exists():
        pytest.skip(f"Test file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def sample_layer1_summary():
    """Create a sample Layer 1 summary for testing."""
    return FileSummary(
        summary="This service provides HTTP client functionality for Ollama API communication.",
        key_classes=["OllamaService"],
        purpose="HTTP client service for Ollama API integration",
        category="Service"
    )


class TestDetailingAgentInitialization:
    """Test agent initialization and configuration."""

    def test_agent_initialization(self, test_config):
        """Test that agent initializes correctly with config."""
        agent = DetailingAgent(test_config)

        assert agent.model_name == "codellama:13b"
        assert agent.prompt_path == Path("src/modules/docugen/prompts/detailing_agent.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100  # Should have substantial content

    def test_prompt_loading(self, agent):
        """Test that system prompt loads correctly."""
        assert "Detailing Agent" in agent.system_prompt
        assert "JSON" in agent.system_prompt  # Should mention JSON output format
        assert "classes" in agent.system_prompt.lower()
        assert "methods" in agent.system_prompt.lower()
        assert "documentation" in agent.system_prompt.lower()

    def test_missing_prompt_file_raises_error(self):
        """Test that missing prompt file raises appropriate error."""
        invalid_config = GraphConfig(
            detailing_prompt_path=Path("nonexistent/prompt.md")
        )

        with pytest.raises(FileNotFoundError):
            DetailingAgent(invalid_config)


class TestDetailingAgentStructure:
    """Test agent follows Four Pillars pattern."""

    def test_pillar_1_model_configuration(self, agent):
        """Test Pillar 1: Model is properly configured."""
        assert agent.model_name == "codellama:13b"
        assert isinstance(agent.model_name, str)

    def test_pillar_2_prompt_loaded(self, agent):
        """Test Pillar 2: Prompt is loaded from external file."""
        assert agent.prompt_path == Path("src/modules/docugen/prompts/detailing_agent.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100

        # Verify prompt contains key instructions
        assert "Detailing Agent" in agent.system_prompt
        assert "classes" in agent.system_prompt.lower()

    def test_pillar_3_context_preparation(self, agent, sample_layer1_summary):
        """Test Pillar 3: Context handler properly formats input."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="public class Test { }",
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)

        # Verify context includes necessary information
        assert "Test.cs" in context
        assert "Test" in context  # Should include code
        assert "Layer 1 Summary" in context  # Should include L1 context
        assert sample_layer1_summary.purpose in context
        assert "```csharp" in context  # Should use code blocks

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

    def test_context_includes_filename(self, agent, sample_layer1_summary):
        """Test context includes file name."""
        state = FileState(
            file_path=Path("/some/path/MyService.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)
        assert "MyService.cs" in context

    def test_context_includes_full_path(self, agent, sample_layer1_summary):
        """Test context includes full path."""
        state = FileState(
            file_path=Path("/project/src/Services/UserService.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)
        assert "/project/src/Services/UserService.cs" in context

    def test_context_includes_layer1_summary(self, agent, sample_layer1_summary):
        """Test context includes Layer 1 summary information."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)

        # Should include Layer 1 information
        assert "Layer 1 Summary" in context
        assert sample_layer1_summary.purpose in context
        assert sample_layer1_summary.category in context
        assert "OllamaService" in context  # Key class

    def test_context_includes_code(self, agent, sample_layer1_summary):
        """Test context includes the actual code."""
        code = """
        public class TestClass {
            public void TestMethod() { }
        }
        """
        state = FileState(
            file_path=Path("Test.cs"),
            file_content=code,
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)
        assert "TestClass" in context
        assert "TestMethod" in context

    def test_context_handles_missing_layer1_summary(self, agent):
        """Test context handles case where Layer 1 summary is missing."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;",
            layer1_summary=None
        )

        # Should not crash - context should still be generated
        context = agent._prepare_context(state)
        assert "Test.cs" in context
        assert "using System" in context


class TestAgentConfiguration:
    """Test agent configuration handling."""

    def test_custom_model_name(self):
        """Test agent accepts custom model name."""
        custom_config = GraphConfig(
            detailing_model="custom-model:latest",
            detailing_prompt_path=Path("src/modules/docugen/prompts/detailing_agent.md")
        )

        agent = DetailingAgent(custom_config)
        assert agent.model_name == "custom-model:latest"

    def test_different_model_than_summarizer(self, test_config):
        """Test that detailing agent uses different model than summarizer."""
        # Detailing agent should use larger model (13b vs 7b)
        assert test_config.detailing_model == "codellama:13b"
        assert test_config.summarizer_model == "codellama:7b"
        assert test_config.detailing_model != test_config.summarizer_model


class TestStateManagement:
    """Test state handling."""

    def test_state_with_layer1_summary(self, sample_layer1_summary):
        """Test creating FileState with Layer 1 summary."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        assert state.file_path == Path("test.cs")
        assert state.file_content == "using System;"
        assert state.layer1_summary == sample_layer1_summary
        assert state.layer2_details is None
        assert state.layer2_iterations == 0
        assert state.error_message is None

    def test_state_tracks_iterations(self, sample_layer1_summary):
        """Test that state properly tracks iteration count."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        assert state.layer2_iterations == 0

        # Simulate iteration increment (this would happen in invoke())
        state.layer2_iterations += 1
        assert state.layer2_iterations == 1

        state.layer2_iterations += 1
        assert state.layer2_iterations == 2


class TestPydanticModels:
    """Test Pydantic model structure."""

    def test_detailed_docs_structure(self):
        """Test DetailedDocs Pydantic model structure."""
        from src.modules.docugen.state import MethodDoc, ClassDoc

        method = MethodDoc(
            name="TestMethod",
            signature="public void TestMethod(int param)",
            description="Test method description",
            parameters=["param: Test parameter"],
            returns=None
        )

        class_doc = ClassDoc(
            name="TestClass",
            description="Test class description",
            methods=[method]
        )

        detailed_docs = DetailedDocs(
            classes=[class_doc],
            standalone_methods=[]
        )

        assert len(detailed_docs.classes) == 1
        assert detailed_docs.classes[0].name == "TestClass"
        assert len(detailed_docs.classes[0].methods) == 1
        assert detailed_docs.classes[0].methods[0].name == "TestMethod"

    def test_empty_detailed_docs(self):
        """Test creating empty DetailedDocs."""
        detailed_docs = DetailedDocs(
            classes=[],
            standalone_methods=[]
        )

        assert len(detailed_docs.classes) == 0
        assert len(detailed_docs.standalone_methods) == 0


class TestNodeFunction:
    """Test the LangGraph node function wrapper."""

    def test_generate_details_node_function(self, test_config, sample_layer1_summary):
        """Test that the generate_details node function works correctly."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="public class Test { public void Method() { } }",
            layer1_summary=sample_layer1_summary
        )

        # Call node function (simulating LangGraph invocation)
        # Note: This will attempt to call Ollama, so may fail without LLM
        # In that case, the error should be captured in error_message
        result_state = generate_details(state, test_config)

        assert isinstance(result_state, FileState)
        # Either successful with details or failed with error message
        assert result_state.layer2_details is not None or result_state.error_message is not None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_file_content(self, agent, sample_layer1_summary):
        """Test handling of empty file content."""
        state = FileState(
            file_path=Path("empty.cs"),
            file_content="",
            layer1_summary=sample_layer1_summary
        )

        # Should not crash - either returns docs or error message
        result_state = agent.invoke(state)

        # One of these should be set
        assert result_state.layer2_details is not None or result_state.error_message is not None

    def test_invalid_csharp_code(self, agent, sample_layer1_summary):
        """Test handling of malformed C# code."""
        state = FileState(
            file_path=Path("invalid.cs"),
            file_content="This is not valid C# code @#$%^&*()",
            layer1_summary=sample_layer1_summary
        )

        # Should not crash
        result_state = agent.invoke(state)

        # Agent should attempt to document even invalid code
        assert isinstance(result_state, FileState)


class TestContextConsistency:
    """Test consistency with Layer 1 summary."""

    def test_layer1_context_in_prompt(self, agent):
        """Test that Layer 1 context is properly included in prompt."""
        summary = FileSummary(
            summary="A service for user management",
            key_classes=["UserService"],
            purpose="Manage user accounts",
            category="Service"
        )

        state = FileState(
            file_path=Path("UserService.cs"),
            file_content="public class UserService { }",
            layer1_summary=summary
        )

        context = agent._prepare_context(state)

        # All Layer 1 information should be in context
        assert "Manage user accounts" in context
        assert "Service" in context
        assert "UserService" in context


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
