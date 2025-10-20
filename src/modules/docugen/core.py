"""
DocuGen Core - Core utilities and configuration management.

This module contains the core functionality for the DocuGen system,
including configuration management, validation, and utility functions.
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from loguru import logger
from pydantic import BaseModel, Field, field_validator


class ModelConfig(BaseModel):
    """Configuration for LLM models."""

    default: str = Field(default="codellama:13b", description="Default model for general tasks")
    summarizer: str = Field(default="codellama:7b", description="Model for file summarization (Layer 1)")
    detailing: str = Field(default="codellama:13b", description="Model for detailed documentation (Layer 2)")
    relationship_mapper: str = Field(default="codellama:7b", description="Model for relationship mapping (Layer 3)")
    validation: Optional[str] = Field(default=None, description="Model for validation (defaults to detailing model if not specified)")


class ValidationConfig(BaseModel):
    """Configuration for validation rules."""

    max_iterations: int = Field(default=3, ge=1, le=10, description="Maximum refinement iterations per layer")
    min_summary_length: int = Field(default=50, ge=10, description="Minimum summary length in characters")
    require_all_public_methods: bool = Field(default=True, description="Require documentation for all public methods")


class OutputConfig(BaseModel):
    """Configuration for output generation."""

    base_path: Path = Field(default=Path("./docs_output"), description="Base output directory")
    format: str = Field(default="markdown", description="Output format (currently only markdown)")
    include_metadata: bool = Field(default=True, description="Include generation metadata in output")

    @field_validator("base_path", mode="before")
    @classmethod
    def validate_base_path(cls, v):
        """Convert string paths to Path objects."""
        return Path(v) if isinstance(v, str) else v


class ProcessingConfig(BaseModel):
    """Configuration for processing options."""

    parallel_files: int = Field(default=4, ge=1, le=16, description="Number of files to process in parallel")
    enable_incremental: bool = Field(default=True, description="Enable incremental documentation updates")
    supported_languages: list[str] = Field(
        default=["csharp"],
        description="Supported programming languages (csharp, java, python, etc.)"
    )


class OllamaConfig(BaseModel):
    """Configuration for Ollama/LLM connection."""

    base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for Ollama API or OpenAI-compatible endpoint"
    )
    timeout: int = Field(default=300, ge=1, description="Request timeout in seconds")


class DocuGenConfig(BaseModel):
    """Main configuration for DocuGen system."""

    models: ModelConfig = Field(default_factory=ModelConfig)
    validation: ValidationConfig = Field(default_factory=ValidationConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)

    @property
    def output_path(self) -> Path:
        """Get the output path."""
        return self.output.base_path

    @output_path.setter
    def output_path(self, value: Path):
        """Set the output path."""
        self.output.base_path = value

    @classmethod
    def from_yaml(cls, path: Path) -> "DocuGenConfig":
        """
        Load configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            DocuGenConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)

            if data is None:
                data = {}

            return cls(**data)

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")

    def to_yaml(self, path: Path) -> None:
        """
        Save configuration to YAML file.

        Args:
            path: Path where to save configuration
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            # Convert Pydantic model to dict, excluding defaults
            data = self.model_dump(exclude_defaults=False)
            # Convert Path objects to strings for YAML serialization
            data = self._convert_paths_to_str(data)
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def _convert_paths_to_str(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively convert Path objects to strings in nested dict."""
        if isinstance(data, dict):
            return {k: DocuGenConfig._convert_paths_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DocuGenConfig._convert_paths_to_str(item) for item in data]
        elif isinstance(data, Path):
            return str(data)
        return data


def validate_config_path(config_path: str) -> Path:
    """
    Validate that config file exists and is readable.

    Args:
        config_path: Path to configuration file

    Returns:
        Path object for valid config file

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n\n"
            "Create a configuration file using the example:\n"
            "  cp src/modules/docugen/config/config.example.yaml config.yaml"
        )

    if not path.is_file():
        raise ValueError(f"Configuration path is not a file: {config_path}")

    logger.debug(f"Configuration file validated: {path}")
    return path


def validate_input_path(input_path: str) -> Path:
    """
    Validate that input directory exists and is accessible.

    Args:
        input_path: Path to source code directory

    Returns:
        Path object for valid input directory

    Raises:
        FileNotFoundError: If directory doesn't exist
        ValueError: If path is not a directory
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    if not path.is_dir():
        raise ValueError(f"Input path is not a directory: {input_path}")

    logger.debug(f"Input directory validated: {path}")
    return path


def verify_ollama_running() -> bool:
    """
    Verify that Ollama service is running and accessible.

    Returns:
        True if Ollama is running, False otherwise
    """
    try:
        # Try to run ollama list command
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            logger.debug("Ollama service is running")
            return True
        else:
            logger.warning(f"Ollama command failed: {result.stderr}")
            return False

    except FileNotFoundError:
        logger.error("Ollama command not found - is Ollama installed?")
        return False
    except subprocess.TimeoutExpired:
        logger.error("Ollama command timed out")
        return False
    except Exception as e:
        logger.error(f"Error checking Ollama status: {e}")
        return False


def get_project_root() -> Path:
    """
    Get the project root directory (where pyproject.toml is located).

    Returns:
        Path to project root
    """
    current = Path(__file__).resolve()

    # Walk up the directory tree looking for pyproject.toml
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    # Fallback to current working directory
    return Path.cwd()


def create_default_config(output_path: Path) -> DocuGenConfig:
    """
    Create and save a default configuration file.

    Args:
        output_path: Where to save the configuration

    Returns:
        DocuGenConfig instance with default values
    """
    config = DocuGenConfig()
    config.to_yaml(output_path)
    logger.info(f"Created default configuration: {output_path}")
    return config
