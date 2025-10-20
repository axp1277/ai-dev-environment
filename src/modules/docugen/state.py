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


class MethodDoc(BaseModel):
    """Documentation for a single method."""
    name: str
    signature: str
    description: str
    parameters: List[str] = Field(default_factory=list)
    returns: Optional[str] = None


class ClassDoc(BaseModel):
    """Documentation for a single class."""
    name: str
    description: str
    methods: List[MethodDoc] = Field(default_factory=list)


class DetailedDocs(BaseModel):
    """Layer 2 output: Detailed function/class documentation."""
    classes: List[ClassDoc] = Field(default_factory=list)
    standalone_methods: List[MethodDoc] = Field(default_factory=list)


class DependencyInfo(BaseModel):
    """Information about a dependency."""
    file: str
    classes_used: List[str] = Field(default_factory=list)
    purpose: str
    relationship_type: str  # Composition, Inheritance, Usage, Injection


class RelationshipMap(BaseModel):
    """Layer 3 output: Cross-file relationships."""
    dependencies: List[DependencyInfo] = Field(default_factory=list, description="What this file depends on")
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

    # Ollama/LLM connection
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for Ollama API or OpenAI-compatible endpoint"
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
