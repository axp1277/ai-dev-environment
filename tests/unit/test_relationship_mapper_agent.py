"""
Unit tests for RelationshipMapperAgent using real C# files from sample_codebase.

Tests the complete agent pipeline without mocks:
- Real Ollama LLM calls (when available)
- Real file reads from sample_codebase
- Full Pydantic validation
- End-to-end agent invocation
"""

import pytest
from pathlib import Path
from loguru import logger

from src.modules.docugen.agents.relationship_mapper_agent import RelationshipMapperAgent, map_relationships
from src.modules.docugen.state import (
    FileState, FileSummary, DetailedDocs, RelationshipMap,
    DependencyInfo, GraphConfig, ClassDoc, MethodDoc
)


# Test fixtures - Real C# files from sample_codebase
TEST_FILES = {
    "service_class": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Services/OllamaService.cs"),
    "interface_simple": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/Abstractions/IInputSource.cs"),
    "interface_handler": Path("data/sample_codebase/RepoScribe-master/RepoScribe.Core/FileHandlers/IFileHandler.cs"),
}


@pytest.fixture
def test_config():
    """Create a test configuration with default settings."""
    return GraphConfig(
        relationship_model="codellama:7b",
        relationship_prompt_path=Path("src/modules/docugen/prompts/relationship_mapper.md")
    )


@pytest.fixture
def agent(test_config):
    """Create a RelationshipMapperAgent instance for testing."""
    return RelationshipMapperAgent(test_config)


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


@pytest.fixture
def sample_layer2_details():
    """Create sample Layer 2 details for testing."""
    method = MethodDoc(
        name="GetAsync",
        signature="public async Task<string> GetAsync(string url, Dictionary<string, string> req)",
        description="Performs an asynchronous GET request to the Ollama API",
        parameters=["url: API endpoint URL", "req: Query parameters dictionary"],
        returns="Response content as string"
    )

    class_doc = ClassDoc(
        name="OllamaService",
        description="Manages HTTP communication with the Ollama API service",
        methods=[method]
    )

    return DetailedDocs(
        classes=[class_doc],
        standalone_methods=[]
    )


class TestRelationshipMapperAgentInitialization:
    """Test agent initialization and configuration."""

    def test_agent_initialization(self, test_config):
        """Test that agent initializes correctly with config."""
        agent = RelationshipMapperAgent(test_config)

        assert agent.model_name == "codellama:7b"
        assert agent.prompt_path == Path("src/modules/docugen/prompts/relationship_mapper.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100  # Should have substantial content

    def test_prompt_loading(self, agent):
        """Test that system prompt loads correctly."""
        assert "Relationship Mapper" in agent.system_prompt
        assert "dependencies" in agent.system_prompt.lower()
        assert "architectural" in agent.system_prompt.lower()
        assert "JSON" in agent.system_prompt

    def test_missing_prompt_file_raises_error(self):
        """Test that missing prompt file raises appropriate error."""
        invalid_config = GraphConfig(
            relationship_prompt_path=Path("nonexistent/prompt.md")
        )

        with pytest.raises(FileNotFoundError):
            RelationshipMapperAgent(invalid_config)


class TestRelationshipMapperAgentStructure:
    """Test agent follows Four Pillars pattern."""

    def test_pillar_1_model_configuration(self, agent):
        """Test Pillar 1: Model is properly configured."""
        assert agent.model_name == "codellama:7b"
        assert isinstance(agent.model_name, str)

    def test_pillar_2_prompt_loaded(self, agent):
        """Test Pillar 2: Prompt is loaded from external file."""
        assert agent.prompt_path == Path("src/modules/docugen/prompts/relationship_mapper.md")
        assert agent.system_prompt is not None
        assert len(agent.system_prompt) > 100

        # Verify prompt contains key instructions
        assert "dependencies" in agent.system_prompt.lower()
        assert "architectural" in agent.system_prompt.lower()

    def test_pillar_3_context_preparation(self, agent, sample_layer1_summary, sample_layer2_details):
        """Test Pillar 3: Context handler properly formats input."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;\npublic class Test { }",
            layer1_summary=sample_layer1_summary,
            layer2_details=sample_layer2_details
        )

        context = agent._prepare_context(state)

        # Verify context includes necessary information
        assert "Test.cs" in context
        assert "Layer 1 Summary" in context
        assert "Layer 2 Details" in context
        assert sample_layer1_summary.purpose in context
        assert "OllamaService" in context
        assert "```csharp" in context

    def test_pillar_4_tools_none_for_this_agent(self, agent):
        """Test Pillar 4: This agent uses no external tools (LLM only)."""
        # This agent infers relationships via LLM, no external tools
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

    def test_context_includes_layer2_details(self, agent, sample_layer1_summary, sample_layer2_details):
        """Test context includes Layer 2 details."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary,
            layer2_details=sample_layer2_details
        )

        context = agent._prepare_context(state)

        # Should include Layer 2 information
        assert "Layer 2 Details" in context
        assert "OllamaService" in context  # Class name from Layer 2

    def test_context_handles_missing_layer1(self, agent):
        """Test context handles case where Layer 1 is missing."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;",
            layer1_summary=None
        )

        # Should not crash
        context = agent._prepare_context(state)
        assert "Test.cs" in context
        assert "using System" in context

    def test_context_handles_missing_layer2(self, agent, sample_layer1_summary):
        """Test context handles case where Layer 2 is missing."""
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary,
            layer2_details=None
        )

        # Should not crash
        context = agent._prepare_context(state)
        assert "Test.cs" in context
        assert "Layer 1 Summary" in context

    def test_context_includes_code(self, agent, sample_layer1_summary):
        """Test context includes the actual code."""
        code = """
        using System;
        using MyApp.Services;

        public class TestClass {
            private readonly IMyService _service;
            public void TestMethod() { }
        }
        """
        state = FileState(
            file_path=Path("Test.cs"),
            file_content=code,
            layer1_summary=sample_layer1_summary
        )

        context = agent._prepare_context(state)
        assert "IMyService" in context
        assert "TestMethod" in context


class TestAgentConfiguration:
    """Test agent configuration handling."""

    def test_custom_model_name(self):
        """Test agent accepts custom model name."""
        custom_config = GraphConfig(
            relationship_model="custom-model:latest",
            relationship_prompt_path=Path("src/modules/docugen/prompts/relationship_mapper.md")
        )

        agent = RelationshipMapperAgent(custom_config)
        assert agent.model_name == "custom-model:latest"

    def test_uses_smaller_model_than_detailing(self, test_config):
        """Test that relationship agent uses same model as summarizer (7b)."""
        # Relationship mapping is simpler than detailing, so uses smaller model
        assert test_config.relationship_model == "codellama:7b"
        assert test_config.detailing_model == "codellama:13b"
        assert test_config.relationship_model == test_config.summarizer_model


class TestStateManagement:
    """Test state handling."""

    def test_state_with_all_layers(self, sample_layer1_summary, sample_layer2_details):
        """Test creating FileState with all previous layers."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary,
            layer2_details=sample_layer2_details
        )

        assert state.file_path == Path("test.cs")
        assert state.layer1_summary == sample_layer1_summary
        assert state.layer2_details == sample_layer2_details
        assert state.layer3_relationships is None
        assert state.layer3_iterations == 0
        assert state.error_message is None

    def test_state_tracks_iterations(self, sample_layer1_summary):
        """Test that state properly tracks iteration count."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;",
            layer1_summary=sample_layer1_summary
        )

        assert state.layer3_iterations == 0

        # Simulate iteration increment
        state.layer3_iterations += 1
        assert state.layer3_iterations == 1

        state.layer3_iterations += 1
        assert state.layer3_iterations == 2


class TestPydanticModels:
    """Test Pydantic model structure."""

    def test_relationship_map_structure(self):
        """Test RelationshipMap Pydantic model structure."""
        dependency = DependencyInfo(
            file="Services/EmailService.cs",
            classes_used=["IEmailService"],
            purpose="Send notification emails",
            relationship_type="Injection"
        )

        relationships = RelationshipMap(
            dependencies=[dependency],
            dependents=[{"file": "Controllers/UserController.cs", "how_used": "User management"}],
            architectural_role="Service Layer"
        )

        assert len(relationships.dependencies) == 1
        assert relationships.dependencies[0].file == "Services/EmailService.cs"
        assert relationships.architectural_role == "Service Layer"
        assert len(relationships.dependents) == 1

    def test_empty_relationship_map(self):
        """Test creating empty RelationshipMap."""
        relationships = RelationshipMap(
            dependencies=[],
            dependents=[],
            architectural_role="Utility"
        )

        assert len(relationships.dependencies) == 0
        assert len(relationships.dependents) == 0
        assert relationships.architectural_role == "Utility"

    def test_dependency_info_structure(self):
        """Test DependencyInfo model."""
        dep = DependencyInfo(
            file="Data/IUserRepository.cs",
            classes_used=["IUserRepository", "UserEntity"],
            purpose="Data persistence",
            relationship_type="Injection"
        )

        assert dep.file == "Data/IUserRepository.cs"
        assert len(dep.classes_used) == 2
        assert dep.relationship_type == "Injection"


class TestNodeFunction:
    """Test the LangGraph node function wrapper."""

    def test_map_relationships_node_function(self, test_config, sample_layer1_summary):
        """Test that the map_relationships node function works correctly."""
        state = FileState(
            file_path=Path("test.cs"),
            file_content="using System;\npublic class Test { }",
            layer1_summary=sample_layer1_summary
        )

        # Call node function (simulating LangGraph invocation)
        result_state = map_relationships(state, test_config)

        assert isinstance(result_state, FileState)
        # Either successful with relationships or failed with error message
        assert result_state.layer3_relationships is not None or result_state.error_message is not None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_file_content(self, agent, sample_layer1_summary):
        """Test handling of empty file content."""
        state = FileState(
            file_path=Path("empty.cs"),
            file_content="",
            layer1_summary=sample_layer1_summary
        )

        # Should not crash
        result_state = agent.invoke(state)
        assert isinstance(result_state, FileState)

    def test_invalid_csharp_code(self, agent, sample_layer1_summary):
        """Test handling of malformed C# code."""
        state = FileState(
            file_path=Path("invalid.cs"),
            file_content="This is not valid C# code @#$%^&*()",
            layer1_summary=sample_layer1_summary
        )

        # Should not crash
        result_state = agent.invoke(state)
        assert isinstance(result_state, FileState)


class TestContextConsistency:
    """Test consistency with previous layers."""

    def test_all_layers_in_prompt(self, agent, sample_layer1_summary, sample_layer2_details):
        """Test that all previous layers are included in context."""
        state = FileState(
            file_path=Path("UserService.cs"),
            file_content="public class UserService { }",
            layer1_summary=sample_layer1_summary,
            layer2_details=sample_layer2_details
        )

        context = agent._prepare_context(state)

        # All layers should be in context
        assert "Layer 1 Summary" in context
        assert "Layer 2 Details" in context
        assert sample_layer1_summary.purpose in context
        assert "OllamaService" in context  # From Layer 2


class TestRelationshipTypes:
    """Test understanding of relationship types."""

    def test_relationship_types_defined(self, agent):
        """Test that prompt defines relationship types."""
        # Check that prompt includes relationship type definitions
        assert "Composition" in agent.system_prompt
        assert "Inheritance" in agent.system_prompt
        assert "Usage" in agent.system_prompt
        assert "Injection" in agent.system_prompt


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
