"""
Parser-Led Workflow State Models

State management for the parser-led documentation generation workflow.
Uses Pydantic for validation and LangGraph compatibility.
"""

from typing import Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field

from ...shared.parsers.csharp_structure_parser import StructureSnapshot


class ParserLedConfig(BaseModel):
    """Configuration for parser-led workflow."""
    include_private_members: bool = True
    max_validation_iterations: int = 3

    # LLM configuration (follows existing DocuGen pattern)
    llm_base_url: str = "http://localhost:11434/v1"  # Default to Ollama
    llm_model: str = "mistral-nemo:latest"  # Model for documentation
    llm_api_key_env: Optional[str] = None  # Environment variable name for API key
    llm_timeout: int = 300

    # Output configuration
    output_format: str = "hierarchical"  # "hierarchical" or "markdown"

    class Config:
        """Pydantic configuration."""
        frozen = False


class DocumentedMethod(BaseModel):
    """LLM-generated documentation for a method."""
    name: str
    description: str
    parameters: Dict[str, str] = Field(default_factory=dict)  # param_name: description
    returns: Optional[str] = None

    class Config:
        frozen = False


class DocumentedProperty(BaseModel):
    """LLM-generated documentation for a property."""
    name: str
    description: str

    class Config:
        frozen = False


class DocumentedField(BaseModel):
    """LLM-generated documentation for a field."""
    name: str
    description: str

    class Config:
        frozen = False


class DocumentedClass(BaseModel):
    """Complete documentation for a class with all its members."""
    name: str
    description: str
    purpose: str  # High-level purpose of the class
    methods: Dict[str, DocumentedMethod] = Field(default_factory=dict)  # method_name: documentation
    properties: Dict[str, DocumentedProperty] = Field(default_factory=dict)
    fields: Dict[str, DocumentedField] = Field(default_factory=dict)

    class Config:
        frozen = False


class FileDocumentation(BaseModel):
    """Complete documentation for a single file."""
    file_path: str
    namespace: Optional[str] = None
    classes: Dict[str, DocumentedClass] = Field(default_factory=dict)  # class_name: documentation

    class Config:
        frozen = False


class ValidationGap(BaseModel):
    """Represents a missing or incomplete documentation element."""
    element_type: str  # "class", "method", "property", "field"
    element_name: str
    parent_class: Optional[str] = None  # For methods, properties, fields
    reason: str  # Why it's considered a gap

    class Config:
        frozen = False


class ValidationResult(BaseModel):
    """Result of validating a file's documentation against its structure."""
    file_path: str
    iteration: int
    coverage_percentage: float
    total_elements: int
    documented_elements: int
    missing_elements: int
    gaps: List[ValidationGap] = Field(default_factory=list)
    is_complete: bool = False

    class Config:
        frozen = False


class ParserLedState(BaseModel):
    """
    State for parser-led documentation workflow.

    This state tracks the entire pipeline from file discovery through
    parsing, documentation, validation, and final output generation.
    """

    # Input configuration
    directory_path: str
    config: ParserLedConfig = Field(default_factory=ParserLedConfig)

    # File discovery
    discovered_files: List[str] = Field(default_factory=list)
    current_file_index: int = 0

    # Parsing phase (Phase 1)
    structure_snapshots: Dict[str, StructureSnapshot] = Field(default_factory=dict)
    parsing_errors: Dict[str, str] = Field(default_factory=dict)

    # Documentation phase (Phase 2)
    documented_files: Dict[str, FileDocumentation] = Field(default_factory=dict)
    current_file_path: Optional[str] = None

    # Validation phase (Phase 3)
    validation_results: Dict[str, ValidationResult] = Field(default_factory=dict)
    validation_iteration: int = 0

    # Final output (Phase 4) - To be implemented
    # final_documentation: Optional[str] = None

    class Config:
        """Pydantic configuration."""
        frozen = False
        arbitrary_types_allowed = True  # Allow Path and other types


class FileDiscoveryResult(BaseModel):
    """Result of file discovery operation."""
    total_files: int
    cs_files: List[str]
    csproj_files: List[str]

    class Config:
        """Pydantic configuration."""
        frozen = False
