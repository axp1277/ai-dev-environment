"""
Tests for docugen core module.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from ..shared.core import (
    DocuGenConfig,
    ModelConfig,
    ValidationConfig,
    OutputConfig,
    ProcessingConfig,
    validate_config_path,
    validate_input_path,
    create_default_config,
)


class TestDocuGenConfig:
    """Tests for DocuGenConfig class."""

    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = DocuGenConfig()

        assert config.models.default == "codellama:13b"
        assert config.models.summarizer == "codellama:7b"
        assert config.validation.max_iterations == 3
        assert config.processing.parallel_files == 4

    def test_config_from_yaml(self, tmp_path):
        """Test loading config from YAML file."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "models": {
                "default": "llama2:13b",
                "summarizer": "llama2:7b"
            },
            "validation": {
                "max_iterations": 5
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = DocuGenConfig.from_yaml(config_file)

        assert config.models.default == "llama2:13b"
        assert config.models.summarizer == "llama2:7b"
        assert config.validation.max_iterations == 5

    def test_config_to_yaml(self, tmp_path):
        """Test saving config to YAML file."""
        config = DocuGenConfig()
        config.models.default = "custom:model"

        output_file = tmp_path / "output_config.yaml"
        config.to_yaml(output_file)

        assert output_file.exists()

        # Reload and verify
        loaded_config = DocuGenConfig.from_yaml(output_file)
        assert loaded_config.models.default == "custom:model"

    def test_config_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            DocuGenConfig.from_yaml(Path("/nonexistent/config.yaml"))

    def test_config_validation_constraints(self):
        """Test Pydantic validation constraints."""
        config = DocuGenConfig()

        # max_iterations should be between 1 and 10
        with pytest.raises(ValueError):
            config.validation.max_iterations = 0

        with pytest.raises(ValueError):
            config.validation.max_iterations = 11

    def test_output_path_property(self):
        """Test output_path property getter and setter."""
        config = DocuGenConfig()

        # Test getter
        assert config.output_path == Path("./docs_output")

        # Test setter
        new_path = Path("/custom/output")
        config.output_path = new_path
        assert config.output_path == new_path
        assert config.output.base_path == new_path


class TestValidationFunctions:
    """Tests for validation utility functions."""

    def test_validate_config_path_success(self, tmp_path):
        """Test validating existing config file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("models:\n  default: test")

        result = validate_config_path(str(config_file))

        assert result == config_file
        assert result.exists()

    def test_validate_config_path_not_found(self):
        """Test validation fails for non-existent file."""
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            validate_config_path("/nonexistent/config.yaml")

    def test_validate_config_path_not_file(self, tmp_path):
        """Test validation fails if path is a directory."""
        with pytest.raises(ValueError, match="not a file"):
            validate_config_path(str(tmp_path))

    def test_validate_input_path_success(self, tmp_path):
        """Test validating existing input directory."""
        result = validate_input_path(str(tmp_path))

        assert result == tmp_path
        assert result.is_dir()

    def test_validate_input_path_not_found(self):
        """Test validation fails for non-existent directory."""
        with pytest.raises(FileNotFoundError, match="Input directory not found"):
            validate_input_path("/nonexistent/directory")

    def test_validate_input_path_not_directory(self, tmp_path):
        """Test validation fails if path is a file."""
        test_file = tmp_path / "file.txt"
        test_file.write_text("content")

        with pytest.raises(ValueError, match="not a directory"):
            validate_input_path(str(test_file))


class TestCreateDefaultConfig:
    """Tests for create_default_config function."""

    def test_create_default_config(self, tmp_path):
        """Test creating default configuration file."""
        config_file = tmp_path / "default_config.yaml"

        config = create_default_config(config_file)

        assert config_file.exists()
        assert isinstance(config, DocuGenConfig)
        assert config.models.default == "codellama:13b"

        # Verify file is valid YAML
        loaded = DocuGenConfig.from_yaml(config_file)
        assert loaded.models.default == config.models.default


class TestModelConfig:
    """Tests for ModelConfig class."""

    def test_default_models(self):
        """Test default model values."""
        model_config = ModelConfig()

        assert model_config.default == "codellama:13b"
        assert model_config.summarizer == "codellama:7b"
        assert model_config.detailing == "codellama:13b"
        assert model_config.relationship_mapper == "codellama:7b"

    def test_custom_models(self):
        """Test creating config with custom models."""
        model_config = ModelConfig(
            default="llama2:13b",
            summarizer="llama2:7b"
        )

        assert model_config.default == "llama2:13b"
        assert model_config.summarizer == "llama2:7b"


class TestValidationConfig:
    """Tests for ValidationConfig class."""

    def test_default_validation(self):
        """Test default validation values."""
        validation_config = ValidationConfig()

        assert validation_config.max_iterations == 3
        assert validation_config.min_summary_length == 50
        assert validation_config.require_all_public_methods is True

    def test_validation_constraints(self):
        """Test Pydantic validation constraints."""
        # Valid values
        validation_config = ValidationConfig(
            max_iterations=5,
            min_summary_length=100
        )
        assert validation_config.max_iterations == 5

        # Invalid values should raise
        with pytest.raises(ValueError):
            ValidationConfig(max_iterations=0)  # Below minimum

        with pytest.raises(ValueError):
            ValidationConfig(max_iterations=11)  # Above maximum

        with pytest.raises(ValueError):
            ValidationConfig(min_summary_length=5)  # Below minimum


class TestProcessingConfig:
    """Tests for ProcessingConfig class."""

    def test_default_processing(self):
        """Test default processing values."""
        processing_config = ProcessingConfig()

        assert processing_config.parallel_files == 4
        assert processing_config.enable_incremental is True
        assert "csharp" in processing_config.supported_languages

    def test_parallel_files_constraints(self):
        """Test parallel_files validation constraints."""
        # Valid values
        processing_config = ProcessingConfig(parallel_files=8)
        assert processing_config.parallel_files == 8

        # Invalid values
        with pytest.raises(ValueError):
            ProcessingConfig(parallel_files=0)  # Below minimum

        with pytest.raises(ValueError):
            ProcessingConfig(parallel_files=17)  # Above maximum


# COMMENTED OUT: ParserConfig not yet implemented
# class TestParserConfig:
#     """Tests for ParserConfig class."""

#     def test_default_parsers(self):
#         """Test default parser values."""
#         parser_config = ParserConfig()

#         assert parser_config.csharp == "csast"
#         assert parser_config.java is None
#         assert parser_config.python is None

#     def test_custom_parsers(self):
#         """Test creating config with custom parsers."""
#         parser_config = ParserConfig(
#             csharp="roslyn",
#             java="javaparser"
#         )

#         assert parser_config.csharp == "roslyn"
#         assert parser_config.java == "javaparser"
