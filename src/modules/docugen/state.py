"""
State Management for DocuGen LangGraph Orchestrator

Defines Pydantic models for state management across the documentation pipeline.
Each state is passed through the graph nodes and persists between layers.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path


class FileSummary(BaseModel):
    """Layer 1 output: High-level file summary."""
    summary: str = Field(..., description="2-4 sentence high-level description")
    key_classes: List[str] = Field(default_factory=list, description="Main classes in file")
    purpose: str = Field(..., description="Primary responsibility of this file")
    category: str = Field(..., description="Type of file (e.g., Service, Repository, Controller)")

    # Module context fields (for enhanced Layer 4 synthesis)
    primary_namespace: str = Field(
        default="",
        description="Module name from first 2 namespace parts (e.g., MyApp.Services)"
    )
    module_contribution: str = Field(
        default="",
        description="What this file contributes to the module (one sentence)"
    )
    key_technologies: List[str] = Field(
        default_factory=list,
        description="Main frameworks/libraries used in this file (max 3)"
    )


class MethodDoc(BaseModel):
    """Documentation for a single method."""
    name: str
    signature: str
    description: str
    parameters: List[str] = Field(default_factory=list)
    returns: Optional[str] = None


class AttributeDoc(BaseModel):
    """Documentation for a class field/attribute."""
    name: str = Field(..., description="Name of the attribute/field")
    data_type: str = Field(..., description="Data type of the attribute")
    visibility: str = Field(..., description="Visibility modifier (public, private, protected, internal)")
    description: str = Field(..., description="One sentence description of what this attribute is used for")


class PropertyDoc(BaseModel):
    """Documentation for a class property."""
    name: str = Field(..., description="Name of the property")
    data_type: str = Field(..., description="Data type of the property")
    description: str = Field(..., description="One sentence description of what this property represents")
    is_readonly: bool = Field(default=False, description="Whether the property is read-only")


class ClassDoc(BaseModel):
    """Documentation for a single class."""
    name: str
    namespace: str = Field(default="", description="Full namespace path (e.g., MyApp.Services)")
    base_classes: List[str] = Field(default_factory=list, description="Base classes and interfaces this class derives from")
    description: str
    attributes: List[AttributeDoc] = Field(default_factory=list, description="Class fields/attributes")
    properties: List[PropertyDoc] = Field(default_factory=list, description="Class properties")
    methods: List[MethodDoc] = Field(default_factory=list)


class DetailedDocs(BaseModel):
    """Layer 2 output: Detailed function/class documentation."""
    classes: List[ClassDoc] = Field(default_factory=list)
    standalone_methods: List[MethodDoc] = Field(default_factory=list)


class DependencyInfo(BaseModel):
    """Information about a file-level dependency."""
    file: str
    classes_used: List[str] = Field(default_factory=list)
    purpose: str
    relationship_type: str  # Composition, Inheritance, Usage, Injection


class NamespaceDependency(BaseModel):
    """Namespace-level dependency inferred from using statements."""
    namespace: str = Field(..., description="Full namespace (e.g., MyApp.Services or System.Linq)")
    inferred_module: str = Field(..., description="Inferred module name (e.g., MyApp.Services)")
    purpose: str = Field(..., description="Inferred purpose of this dependency")
    dependency_type: str = Field(..., description="Internal, Framework, or ThirdParty")


class RelationshipMap(BaseModel):
    """Layer 3 output: Cross-file relationships."""
    namespace_dependencies: List[NamespaceDependency] = Field(default_factory=list, description="Namespace-level dependencies from using statements")
    dependencies: List[DependencyInfo] = Field(default_factory=list, description="File-level dependencies (classes this file depends on)")
    dependents: List[Dict[str, str]] = Field(default_factory=list, description="What depends on this file")
    architectural_role: str = Field(default="", description="Design pattern or architectural layer")


class ValidationResult(BaseModel):
    """Validation output for any layer."""
    passed: bool
    issues: List[str] = Field(default_factory=list)
    refinement_instructions: Optional[str] = None


class FileState(BaseModel):
    """
    Main state object passed through the LangGraph pipeline.

    This state persists across all nodes and contains the file being processed,
    outputs from each layer, validation results, and iteration tracking.
    """
    # Input
    file_path: Path = Field(..., description="Path to the C# file being processed")
    file_content: str = Field(..., description="Content of the file")

    # Layer 1: File Summary
    layer1_summary: Optional[FileSummary] = None
    layer1_validation: Optional[ValidationResult] = None
    layer1_iterations: int = Field(default=0, description="Refinement iteration count for Layer 1")

    # Layer 2: Detailed Documentation
    layer2_details: Optional[DetailedDocs] = None
    layer2_validation: Optional[ValidationResult] = None
    layer2_iterations: int = Field(default=0, description="Refinement iteration count for Layer 2")

    # Layer 3: Relationship Mapping
    layer3_relationships: Optional[RelationshipMap] = None
    layer3_validation: Optional[ValidationResult] = None
    layer3_iterations: int = Field(default=0, description="Refinement iteration count for Layer 3")

    # Metadata
    current_layer: str = Field(default="layer1", description="Current processing layer")
    flagged_for_review: bool = Field(default=False, description="Flagged for manual review")
    error_message: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)  # Allow Path type


class GraphConfig(BaseModel):
    """Configuration for the LangGraph orchestrator."""
    max_iterations: int = Field(default=3, description="Maximum refinement iterations per layer")

    # Model configuration per agent
    summarizer_model: str = Field(default="codellama:7b")
    detailing_model: str = Field(default="codellama:13b")
    relationship_model: str = Field(default="codellama:7b")
    validation_model: Optional[str] = Field(default=None, description="Model for validation (defaults to detailing_model)")

    # LLM connection (OpenAI-compatible endpoint)
    llm_base_url: str = Field(
        default="http://localhost:11434/v1",
        description="Base URL for OpenAI-compatible API endpoint (Ollama, OpenRouter, Together AI, OpenAI, etc.)"
    )
    llm_api_key_env: Optional[str] = Field(
        default=None,
        description="Environment variable name for API key (e.g., 'OPENAI_API_KEY', 'OPENROUTER_API_KEY'). Leave None for local Ollama."
    )
    llm_timeout: int = Field(
        default=300,
        ge=1,
        description="Request timeout in seconds"
    )

    # Prompt paths
    summarizer_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/file_summarizer.md"))
    detailing_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/detailing_agent.md"))
    relationship_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/relationship_mapper.md"))
    validation_layer1_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/validation_layer1.md"))
    validation_layer2_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/validation_layer2.md"))
    validation_layer3_prompt_path: Path = Field(default=Path("src/modules/docugen/prompts/validation_layer3.md"))

    # Validation settings
    min_summary_length: int = Field(default=50)
    require_all_public_methods: bool = Field(default=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_validation_model(self) -> str:
        """Get the model to use for validation (defaults to detailing_model)."""
        return self.validation_model if self.validation_model else self.detailing_model
