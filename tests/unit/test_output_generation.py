"""
Unit tests for output generation components.

Tests MarkdownGenerator, OutputManager, and MetricsCollector.
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

from src.modules.docugen.output import MarkdownGenerator, OutputManager, MetricsCollector
from src.modules.docugen.state import (
    FileState, FileSummary, DetailedDocs, RelationshipMap,
    ClassDoc, MethodDoc, DependencyInfo, ValidationResult
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_file_state():
    """Create a complete FileState with all layers."""
    # Layer 1: Summary
    summary = FileSummary(
        summary="This is a comprehensive user service for managing user accounts.",
        key_classes=["UserService", "UserValidator"],
        purpose="Manages user account operations",
        category="Service"
    )

    # Layer 2: Detailed Docs
    method1 = MethodDoc(
        name="CreateUser",
        signature="public User CreateUser(string email, string password)",
        description="Creates a new user account with validation",
        parameters=["email: User's email address", "password: User's password"],
        returns="Newly created User object"
    )
    method2 = MethodDoc(
        name="GetUserById",
        signature="public User GetUserById(int userId)",
        description="Retrieves a user by their unique identifier",
        parameters=["userId: Unique user identifier"],
        returns="User object if found, null otherwise"
    )

    class_doc = ClassDoc(
        name="UserService",
        description="Provides business logic for user management operations",
        methods=[method1, method2]
    )

    details = DetailedDocs(
        classes=[class_doc],
        standalone_methods=[]
    )

    # Layer 3: Relationships
    dependency = DependencyInfo(
        file="Data/IUserRepository.cs",
        classes_used=["IUserRepository"],
        purpose="Data persistence for user entities",
        relationship_type="Injection"
    )

    relationships = RelationshipMap(
        dependencies=[dependency],
        dependents=[{"file": "Controllers/UserController.cs", "how_used": "Handles HTTP requests"}],
        architectural_role="Service Layer"
    )

    # Validation results
    validation1 = ValidationResult(passed=True, issues=[])
    validation2 = ValidationResult(passed=True, issues=[])
    validation3 = ValidationResult(passed=True, issues=[])

    # Create complete state
    state = FileState(
        file_path=Path("Services/UserService.cs"),
        file_content="public class UserService { }",
        layer1_summary=summary,
        layer1_validation=validation1,
        layer1_iterations=0,
        layer2_details=details,
        layer2_validation=validation2,
        layer2_iterations=1,
        layer3_relationships=relationships,
        layer3_validation=validation3,
        layer3_iterations=0,
        current_layer="complete"
    )

    return state


@pytest.fixture
def incomplete_file_state():
    """Create a FileState with only Layer 1."""
    summary = FileSummary(
        summary="Basic file summary",
        key_classes=["TestClass"],
        purpose="Test purpose",
        category="Test"
    )

    state = FileState(
        file_path=Path("Test.cs"),
        file_content="public class Test { }",
        layer1_summary=summary,
        current_layer="layer1"
    )

    return state


@pytest.fixture
def failed_validation_state():
    """Create a FileState with validation failures."""
    summary = FileSummary(
        summary="Short",
        key_classes=[],
        purpose="Test",
        category="Test"
    )

    validation = ValidationResult(
        passed=False,
        issues=["Summary too short", "No key classes identified"],
        refinement_instructions="Please provide more detail"
    )

    state = FileState(
        file_path=Path("Failed.cs"),
        file_content="class Failed { }",
        layer1_summary=summary,
        layer1_validation=validation,
        layer1_iterations=3,
        flagged_for_review=True,
        current_layer="layer1"
    )

    return state


# ============================================================================
# MarkdownGenerator Tests
# ============================================================================

class TestMarkdownGeneratorInitialization:
    """Test MarkdownGenerator initialization."""

    def test_default_initialization(self):
        """Test generator initializes with default settings."""
        generator = MarkdownGenerator()
        assert generator.include_metadata is True
        assert generator.include_toc is True

    def test_custom_initialization(self):
        """Test generator initializes with custom settings."""
        generator = MarkdownGenerator(include_metadata=False, include_toc=False)
        assert generator.include_metadata is False
        assert generator.include_toc is False


class TestMarkdownGeneratorOutput:
    """Test markdown generation."""

    def test_generate_complete_document(self, sample_file_state):
        """Test generating complete documentation with all layers."""
        generator = MarkdownGenerator()
        markdown = generator.generate(sample_file_state)

        # Check title
        assert "# UserService.cs" in markdown

        # Check metadata section
        assert "## Metadata" in markdown
        assert "Services/UserService.cs" in markdown
        assert "✅ Passed" in markdown

        # Check TOC
        assert "## Table of Contents" in markdown
        assert "[Overview](#overview)" in markdown
        assert "[Detailed Documentation](#detailed-documentation)" in markdown
        assert "[Relationships](#relationships)" in markdown

        # Check Layer 1 content
        assert "## Overview" in markdown
        assert "Manages user account operations" in markdown
        assert "Service" in markdown
        assert "`UserService`" in markdown

        # Check Layer 2 content
        assert "## Detailed Documentation" in markdown
        assert "CreateUser" in markdown
        assert "GetUserById" in markdown
        assert "email: User's email address" in markdown

        # Check Layer 3 content
        assert "## Relationships" in markdown
        assert "### Dependencies" in markdown
        assert "IUserRepository" in markdown
        assert "Service Layer" in markdown

    def test_generate_without_metadata(self, sample_file_state):
        """Test generating without metadata section."""
        generator = MarkdownGenerator(include_metadata=False)
        markdown = generator.generate(sample_file_state)

        assert "## Metadata" not in markdown
        assert "# UserService.cs" in markdown
        assert "## Overview" in markdown

    def test_generate_without_toc(self, sample_file_state):
        """Test generating without table of contents."""
        generator = MarkdownGenerator(include_toc=False)
        markdown = generator.generate(sample_file_state)

        assert "## Table of Contents" not in markdown
        assert "## Overview" in markdown

    def test_generate_incomplete_state(self, incomplete_file_state):
        """Test generating documentation with only Layer 1."""
        generator = MarkdownGenerator()
        markdown = generator.generate(incomplete_file_state)

        assert "# Test.cs" in markdown
        assert "## Overview" in markdown
        assert "## Detailed Documentation" not in markdown
        assert "## Relationships" not in markdown

    def test_generate_failed_state(self, failed_validation_state):
        """Test generating documentation with validation failures."""
        generator = MarkdownGenerator()
        markdown = generator.generate(failed_validation_state)

        assert "# Failed.cs" in markdown
        assert "## Status" in markdown
        assert "⚠️ **Flagged for Manual Review**" in markdown
        assert "❌ Failed" in markdown


class TestMarkdownGeneratorLayers:
    """Test individual layer generation."""

    def test_layer1_section(self, sample_file_state):
        """Test Layer 1 section generation."""
        generator = MarkdownGenerator()
        section = generator._generate_layer1_section(sample_file_state)

        assert "## Overview" in section
        assert "Manages user account operations" in section
        assert "Service" in section
        assert "`UserService`" in section
        assert "`UserValidator`" in section

    def test_layer2_section_with_classes(self, sample_file_state):
        """Test Layer 2 section with classes."""
        generator = MarkdownGenerator()
        section = generator._generate_layer2_section(sample_file_state)

        assert "## Detailed Documentation" in section
        assert "### Classes" in section
        assert "`UserService`" in section
        assert "CreateUser" in section
        assert "email: User's email address" in section

    def test_layer2_section_empty(self):
        """Test Layer 2 section when no details available."""
        generator = MarkdownGenerator()
        state = FileState(
            file_path=Path("Test.cs"),
            file_content="test",
            layer2_details=None
        )
        section = generator._generate_layer2_section(state)
        assert section == ""

    def test_layer3_section_with_relationships(self, sample_file_state):
        """Test Layer 3 section generation."""
        generator = MarkdownGenerator()
        section = generator._generate_layer3_section(sample_file_state)

        assert "## Relationships" in section
        assert "### Dependencies" in section
        assert "IUserRepository" in section
        assert "### Dependents" in section
        assert "UserController.cs" in section
        assert "### Architectural Role" in section
        assert "Service Layer" in section

    def test_layer3_section_no_dependencies(self):
        """Test Layer 3 section with no dependencies."""
        generator = MarkdownGenerator()
        relationships = RelationshipMap(
            dependencies=[],
            dependents=[],
            architectural_role="Utility"
        )
        state = FileState(
            file_path=Path("Utils.cs"),
            file_content="utils",
            layer3_relationships=relationships
        )

        section = generator._generate_layer3_section(state)
        assert "*No external dependencies*" in section
        assert "*No known dependents*" in section
        assert "Utility" in section


# ============================================================================
# OutputManager Tests
# ============================================================================

class TestOutputManagerInitialization:
    """Test OutputManager initialization."""

    def test_initialization_with_source_root(self, tmp_path):
        """Test initialization with source root."""
        output_dir = tmp_path / "docs"
        source_root = tmp_path / "src"

        manager = OutputManager(output_dir, source_root)
        assert manager.base_output_dir == output_dir
        assert manager.source_root == source_root
        assert len(manager.generated_files) == 0

    def test_initialization_without_source_root(self, tmp_path):
        """Test initialization without source root (flat structure)."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)
        assert manager.source_root is None


class TestOutputManagerDirectories:
    """Test directory management."""

    def test_ensure_output_directory(self, tmp_path):
        """Test creating output directory."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        assert not output_dir.exists()
        manager.ensure_output_directory()
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_ensure_output_directory_idempotent(self, tmp_path):
        """Test ensure_output_directory is idempotent."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        manager.ensure_output_directory()
        manager.ensure_output_directory()  # Should not raise
        assert output_dir.exists()


class TestOutputManagerPaths:
    """Test path generation."""

    def test_get_output_path_flat_structure(self, tmp_path):
        """Test output path generation without source root."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        source_file = Path("/some/path/UserService.cs")
        output_path = manager.get_output_path(source_file)

        assert output_path == output_dir / "UserService.md"

    def test_get_output_path_mirrored_structure(self, tmp_path):
        """Test output path generation with mirrored directory structure."""
        output_dir = tmp_path / "docs"
        source_root = tmp_path / "src"
        manager = OutputManager(output_dir, source_root)

        source_file = source_root / "Services" / "UserService.cs"
        output_path = manager.get_output_path(source_file)

        assert output_path == output_dir / "Services" / "UserService.md"

    def test_get_output_path_extension_conversion(self, tmp_path):
        """Test that .cs extension is converted to .md."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        source_file = Path("Test.cs")
        output_path = manager.get_output_path(source_file)

        assert output_path.suffix == ".md"
        assert output_path.stem == "Test"


class TestOutputManagerFileWriting:
    """Test file writing operations."""

    def test_write_documentation(self, tmp_path):
        """Test writing documentation file."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        source_file = Path("Test.cs")
        content = "# Test\n\nThis is test documentation."

        output_path = manager.write_documentation(source_file, content)

        assert output_path.exists()
        assert output_path.read_text(encoding='utf-8') == content
        assert len(manager.generated_files) == 1

    def test_write_documentation_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created automatically."""
        output_dir = tmp_path / "docs"
        source_root = tmp_path / "src"
        manager = OutputManager(output_dir, source_root)

        source_file = source_root / "Services" / "Data" / "UserRepo.cs"
        content = "# UserRepo"

        output_path = manager.write_documentation(source_file, content)

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_write_documentation_atomic_operation(self, tmp_path):
        """Test that write is atomic (uses temp file + rename)."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        source_file = Path("Test.cs")
        content = "# Test Documentation"

        # Write once
        output_path = manager.write_documentation(source_file, content)
        assert output_path.read_text(encoding='utf-8') == content

        # Overwrite
        new_content = "# Updated Documentation"
        output_path = manager.write_documentation(source_file, new_content)
        assert output_path.read_text(encoding='utf-8') == new_content

    def test_write_documentation_tracks_files(self, tmp_path):
        """Test that generated files are tracked."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        manager.write_documentation(Path("File1.cs"), "# File 1")
        manager.write_documentation(Path("File2.cs"), "# File 2")

        assert len(manager.generated_files) == 2
        assert manager.generated_files[0]["source"] == str(Path("File1.cs"))
        assert manager.generated_files[1]["source"] == str(Path("File2.cs"))


class TestOutputManagerIndex:
    """Test index generation."""

    def test_generate_index_empty(self, tmp_path):
        """Test generating index with no files."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)
        manager.ensure_output_directory()

        index_path = manager.generate_index()

        assert index_path.exists()
        content = index_path.read_text(encoding='utf-8')
        assert "# Documentation Index" in content
        assert "Total Files: 0" in content

    def test_generate_index_with_files(self, tmp_path):
        """Test generating index with generated files."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        manager.write_documentation(Path("Service1.cs"), "# Service 1")
        manager.write_documentation(Path("Service2.cs"), "# Service 2")

        index_path = manager.generate_index()

        content = index_path.read_text(encoding='utf-8')
        assert "Total Files: 2" in content
        assert "Service1.cs" in content
        assert "Service2.cs" in content

    def test_generate_index_custom_title(self, tmp_path):
        """Test generating index with custom title."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        index_path = manager.generate_index(title="Custom Title")

        content = index_path.read_text(encoding='utf-8')
        assert "# Custom Title" in content


class TestOutputManagerStatistics:
    """Test statistics methods."""

    def test_get_statistics_empty(self, tmp_path):
        """Test statistics with no files."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        stats = manager.get_statistics()
        assert stats["total_files"] == 0
        assert stats["total_size_bytes"] == 0

    def test_get_statistics_with_files(self, tmp_path):
        """Test statistics with generated files."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        manager.write_documentation(Path("Test.cs"), "# Test Content")

        stats = manager.get_statistics()
        assert stats["total_files"] == 1
        assert stats["total_size_bytes"] > 0

    def test_clear_output_directory(self, tmp_path):
        """Test clearing output directory."""
        output_dir = tmp_path / "docs"
        manager = OutputManager(output_dir)

        # Write some files
        manager.write_documentation(Path("File1.cs"), "# File 1")
        manager.write_documentation(Path("File2.cs"), "# File 2")

        assert len(list(output_dir.glob("*.md"))) == 2

        # Clear
        manager.clear_output_directory()

        assert len(list(output_dir.glob("*.md"))) == 0
        assert len(manager.generated_files) == 0


# ============================================================================
# MetricsCollector Tests
# ============================================================================

class TestMetricsCollectorInitialization:
    """Test MetricsCollector initialization."""

    def test_initialization(self):
        """Test collector initializes correctly."""
        collector = MetricsCollector()
        assert collector.metrics.total_files == 0
        assert collector.pipeline_start_time is None


class TestMetricsCollectorPipelineTracking:
    """Test pipeline-level tracking."""

    def test_start_pipeline(self):
        """Test starting pipeline tracking."""
        collector = MetricsCollector()
        config = {"model": "codellama:13b", "max_iterations": 3}

        collector.start_pipeline(config)

        assert collector.pipeline_start_time is not None
        assert collector.metrics.start_time is not None
        assert collector.metrics.config_used == config

    def test_end_pipeline(self):
        """Test ending pipeline and calculating duration."""
        collector = MetricsCollector()
        collector.start_pipeline()

        # Simulate some processing time
        import time
        time.sleep(0.1)

        collector.end_pipeline()

        assert collector.metrics.end_time is not None
        assert collector.metrics.total_duration_seconds > 0


class TestMetricsCollectorFileTracking:
    """Test file-level tracking."""

    def test_record_file_completion_basic(self, sample_file_state):
        """Test recording file completion."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)

        assert collector.metrics.total_files == 1
        assert collector.metrics.layer1_completed == 1
        assert collector.metrics.layer2_completed == 1
        assert collector.metrics.layer3_completed == 1
        assert collector.metrics.fully_documented == 1

    def test_record_file_completion_incomplete(self, incomplete_file_state):
        """Test recording incomplete file."""
        collector = MetricsCollector()
        collector.record_file_completion(incomplete_file_state)

        assert collector.metrics.total_files == 1
        assert collector.metrics.layer1_completed == 1
        assert collector.metrics.layer2_completed == 0
        assert collector.metrics.layer3_completed == 0
        assert collector.metrics.fully_documented == 0

    def test_record_validation_results(self, sample_file_state):
        """Test recording validation results."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)

        assert collector.metrics.layer1_validation_passed == 1
        assert collector.metrics.layer2_validation_passed == 1
        assert collector.metrics.layer3_validation_passed == 1
        assert collector.metrics.layer1_validation_failed == 0

    def test_record_iterations(self, sample_file_state):
        """Test recording iteration counts."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)

        assert collector.metrics.total_layer1_iterations == 0
        assert collector.metrics.total_layer2_iterations == 1
        assert collector.metrics.max_layer2_iterations == 1

    def test_record_flags_and_errors(self, failed_validation_state):
        """Test recording flags and errors."""
        collector = MetricsCollector()
        collector.record_file_completion(failed_validation_state)

        assert collector.metrics.flagged_for_review == 1


class TestMetricsCollectorCalculations:
    """Test metric calculations."""

    def test_coverage_percentage(self, sample_file_state, incomplete_file_state):
        """Test coverage percentage calculation."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)
        collector.record_file_completion(incomplete_file_state)

        coverage = collector.get_coverage_percentage()

        assert coverage["layer1"] == 100.0  # 2/2
        assert coverage["layer2"] == 50.0   # 1/2
        assert coverage["layer3"] == 50.0   # 1/2
        assert coverage["fully_documented"] == 50.0  # 1/2

    def test_validation_pass_rate(self, sample_file_state, failed_validation_state):
        """Test validation pass rate calculation."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)
        collector.record_file_completion(failed_validation_state)

        pass_rates = collector.get_validation_pass_rate()

        assert pass_rates["layer1"] == 50.0  # 1 passed, 1 failed

    def test_average_iterations(self, sample_file_state):
        """Test average iterations calculation."""
        collector = MetricsCollector()
        collector.record_file_completion(sample_file_state)

        avg_iterations = collector.get_average_iterations()

        assert avg_iterations["layer1"] == 0.0
        assert avg_iterations["layer2"] == 1.0
        assert avg_iterations["layer3"] == 0.0


class TestMetricsCollectorExport:
    """Test metrics export."""

    def test_export_json(self, tmp_path, sample_file_state):
        """Test exporting metrics to JSON."""
        collector = MetricsCollector()
        collector.start_pipeline({"model": "test"})
        collector.record_file_completion(sample_file_state)
        collector.end_pipeline()

        output_path = tmp_path / "metrics.json"
        collector.export_json(output_path)

        assert output_path.exists()

        with open(output_path) as f:
            data = json.load(f)

        assert data["total_files"] == 1
        assert "coverage_percentage" in data
        assert "validation_pass_rate" in data

    def test_export_markdown(self, tmp_path, sample_file_state):
        """Test exporting metrics to markdown."""
        collector = MetricsCollector()
        collector.start_pipeline()
        collector.record_file_completion(sample_file_state)
        collector.end_pipeline()

        output_path = tmp_path / "metrics.md"
        collector.export_markdown(output_path)

        assert output_path.exists()
        content = output_path.read_text(encoding='utf-8')

        assert "# Documentation Pipeline Metrics Report" in content
        assert "Total Files Processed" in content
        assert "Coverage Metrics" in content
        assert "Quality Metrics" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
