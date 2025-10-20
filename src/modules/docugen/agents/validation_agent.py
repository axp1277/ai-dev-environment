"""
Validation Agent - Quality Checks for All Layers

Performs hybrid validation on Layer 1, 2, and 3 outputs:
- Phase 1: Fast programmatic pre-checks (structure, required fields)
- Phase 2: LLM-driven semantic validation (accuracy, quality, usefulness)

Generates structured feedback for refinement when validation fails.

Four Pillars:
1. Model: Ollama LLM (configurable, defaults to detailing_model)
2. Prompt: External files (validation_layer1/2/3.md)
3. Context: Layer outputs + original file content
4. Tools: Pydantic validation, Ollama structured output
"""

import json
from typing import Optional
from pathlib import Path
import ollama
from loguru import logger

from ..state import (
    FileState,
    ValidationResult,
    FileSummary,
    DetailedDocs,
    RelationshipMap,
    GraphConfig
)


class ValidationAgent:
    """
    Validation Agent: Performs hybrid quality checks on documentation layers.

    Phase 1: Fast programmatic pre-checks
    Phase 2: LLM-driven semantic validation
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the Validation Agent.

        Args:
            config: Graph configuration containing validation settings
        """
        self.config = config
        self.model_name = config.get_validation_model()
        self.min_summary_length = config.min_summary_length
        self.require_all_public_methods = config.require_all_public_methods

        # Create Ollama client with configurable base URL
        self.client = ollama.Client(host=config.ollama_base_url)

        # Load validation prompts
        self.layer1_prompt = self._load_prompt(config.validation_layer1_prompt_path)
        self.layer2_prompt = self._load_prompt(config.validation_layer2_prompt_path)
        self.layer3_prompt = self._load_prompt(config.validation_layer3_prompt_path)

        logger.info(
            "ValidationAgent initialized",
            model=self.model_name,
            min_summary_length=self.min_summary_length,
            require_all_methods=self.require_all_public_methods,
            base_url=config.ollama_base_url
        )

    def _load_prompt(self, prompt_path: Path) -> str:
        """
        Load validation prompt from file.

        Args:
            prompt_path: Path to prompt file

        Returns:
            Prompt content as string
        """
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt file not found: {prompt_path}, using minimal prompt")
            return "Evaluate the documentation quality and return valid JSON with passed, issues, and refinement_instructions."

    def _call_llm_validator(self, prompt: str, context: str) -> ValidationResult:
        """
        Call LLM to perform semantic validation.

        Args:
            prompt: System prompt for validation
            context: User context (code + documentation)

        Returns:
            ValidationResult from LLM
        """
        try:
            logger.debug("Calling LLM validator", model=self.model_name)

            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": context}
                ],
                format=ValidationResult.model_json_schema(),
                options={"temperature": 0.1}  # Low temperature for consistent validation
            )

            # Parse response into ValidationResult
            result_dict = json.loads(response['message']['content'])
            return ValidationResult(**result_dict)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM validation response: {e}")
            return ValidationResult(
                passed=False,
                issues=["LLM validation failed - could not parse response"],
                refinement_instructions="Internal error - validation response was invalid"
            )
        except Exception as e:
            logger.exception(f"LLM validation error: {e}")
            return ValidationResult(
                passed=False,
                issues=[f"LLM validation error: {str(e)}"],
                refinement_instructions="Internal error during validation"
            )

    def validate_layer1(self, summary: Optional[FileSummary], file_content: str) -> ValidationResult:
        """
        Hybrid validation for Layer 1 output (FileSummary).

        Phase 1: Fast programmatic pre-checks
        Phase 2: LLM semantic validation

        Args:
            summary: Layer 1 FileSummary output
            file_content: Original source code

        Returns:
            ValidationResult with pass/fail and issues
        """
        # Phase 1: Fast programmatic pre-checks
        if not summary:
            return ValidationResult(
                passed=False,
                issues=["Layer 1 output missing - no summary generated"],
                refinement_instructions="Generate a complete FileSummary with all required fields"
            )

        # Check basic structure
        precheck_issues = []
        if len(summary.summary) < self.min_summary_length:
            precheck_issues.append(f"Summary too short ({len(summary.summary)} chars, minimum {self.min_summary_length})")
        if not summary.purpose or summary.purpose.strip() == "":
            precheck_issues.append("Purpose field is empty")
        if not summary.category or summary.category.strip() == "":
            precheck_issues.append("Category field is empty")
        if summary.key_classes is None:
            precheck_issues.append("Key classes list is missing")

        if precheck_issues:
            logger.warning("Layer 1 pre-check failed", issues=precheck_issues)
            return ValidationResult(
                passed=False,
                issues=precheck_issues,
                refinement_instructions="Fix structural issues: " + "; ".join(precheck_issues)
            )

        # Phase 2: LLM semantic validation
        logger.info("Running LLM semantic validation for Layer 1")

        context = f"""# Original Source Code
```
{file_content}
```

# Generated FileSummary
- **Summary**: {summary.summary}
- **Purpose**: {summary.purpose}
- **Category**: {summary.category}
- **Key Classes**: {', '.join(summary.key_classes) if summary.key_classes else 'None'}

Evaluate the quality and accuracy of this FileSummary."""

        result = self._call_llm_validator(self.layer1_prompt, context)

        if result.passed:
            logger.success("Layer 1 validation passed (LLM)")
        else:
            logger.warning("Layer 1 validation failed (LLM)", issues=result.issues)

        return result

    def validate_layer2(self, details: Optional[DetailedDocs], file_content: str, layer1_summary: Optional[FileSummary] = None) -> ValidationResult:
        """
        Hybrid validation for Layer 2 output (DetailedDocs).

        Phase 1: Fast programmatic pre-checks
        Phase 2: LLM semantic validation

        Args:
            details: Layer 2 DetailedDocs output
            file_content: Original source code
            layer1_summary: Layer 1 summary for context (optional)

        Returns:
            ValidationResult with pass/fail and issues
        """
        # Phase 1: Fast programmatic pre-checks
        if not details:
            return ValidationResult(
                passed=False,
                issues=["Layer 2 output missing - no detailed docs generated"],
                refinement_instructions="Generate complete DetailedDocs with class and method documentation"
            )

        # Check basic structure
        precheck_issues = []
        for class_doc in details.classes:
            if not class_doc.name or class_doc.name.strip() == "":
                precheck_issues.append("Found class with empty name")
            if not class_doc.description or class_doc.description.strip() == "":
                precheck_issues.append(f"Class '{class_doc.name}' has no description")
            for method in class_doc.methods:
                if not method.name or method.name.strip() == "":
                    precheck_issues.append(f"Class '{class_doc.name}' has method with empty name")
                if not method.description or method.description.strip() == "":
                    precheck_issues.append(f"Method '{method.name}' in '{class_doc.name}' has no description")

        for method in details.standalone_methods:
            if not method.name or method.name.strip() == "":
                precheck_issues.append("Found standalone method with empty name")
            if not method.description or method.description.strip() == "":
                precheck_issues.append(f"Standalone method '{method.name}' has no description")

        if precheck_issues:
            logger.warning("Layer 2 pre-check failed", issues=precheck_issues)
            return ValidationResult(
                passed=False,
                issues=precheck_issues,
                refinement_instructions="Fix structural issues: " + "; ".join(precheck_issues[:3])  # Limit to first 3
            )

        # Phase 2: LLM semantic validation
        logger.info("Running LLM semantic validation for Layer 2")

        # Prepare detailed docs summary for context
        docs_summary = f"**Classes**: {len(details.classes)}\n"
        for cls in details.classes[:3]:  # Sample first 3 classes
            docs_summary += f"  - {cls.name}: {len(cls.methods)} methods\n"
        docs_summary += f"**Standalone Methods**: {len(details.standalone_methods)}"

        context = f"""# Original Source Code
```
{file_content}
```

# Layer 1 Summary (for context)
{json.dumps(layer1_summary.model_dump() if layer1_summary else {}, indent=2)}

# Layer 2 Detailed Documentation
{json.dumps(details.model_dump(), indent=2)}

Evaluate the quality, accuracy, and completeness of this detailed documentation."""

        result = self._call_llm_validator(self.layer2_prompt, context)

        if result.passed:
            logger.success("Layer 2 validation passed (LLM)")
        else:
            logger.warning("Layer 2 validation failed (LLM)", issues=result.issues)

        return result

    def validate_layer3(
        self,
        relationships: Optional[RelationshipMap],
        file_content: str,
        layer1_summary: Optional[FileSummary] = None,
        layer2_details: Optional[DetailedDocs] = None
    ) -> ValidationResult:
        """
        Hybrid validation for Layer 3 output (RelationshipMap).

        Phase 1: Fast programmatic pre-checks
        Phase 2: LLM semantic validation

        Args:
            relationships: Layer 3 RelationshipMap output
            file_content: Original source code
            layer1_summary: Layer 1 summary for context (optional)
            layer2_details: Layer 2 details for context (optional)

        Returns:
            ValidationResult with pass/fail and issues
        """
        # Phase 1: Fast programmatic pre-checks
        if not relationships:
            return ValidationResult(
                passed=False,
                issues=["Layer 3 output missing - no relationship map generated"],
                refinement_instructions="Generate complete RelationshipMap with dependencies and architectural role"
            )

        # Check basic structure
        precheck_issues = []
        if not relationships.architectural_role or relationships.architectural_role.strip() == "":
            precheck_issues.append("Architectural role is not specified")

        valid_types = ["Composition", "Inheritance", "Usage", "Injection", "Association"]
        for dep in relationships.dependencies:
            if not dep.file or dep.file.strip() == "":
                precheck_issues.append("Found dependency with empty file path")
            if not dep.purpose or dep.purpose.strip() == "":
                precheck_issues.append(f"Dependency on '{dep.file}' has no purpose description")
            if dep.relationship_type and dep.relationship_type not in valid_types:
                precheck_issues.append(f"Invalid relationship type '{dep.relationship_type}'")

        if precheck_issues:
            logger.warning("Layer 3 pre-check failed", issues=precheck_issues)
            return ValidationResult(
                passed=False,
                issues=precheck_issues,
                refinement_instructions="Fix structural issues: " + "; ".join(precheck_issues[:3])
            )

        # Phase 2: LLM semantic validation
        logger.info("Running LLM semantic validation for Layer 3")

        context = f"""# Original Source Code
```
{file_content}
```

# Layer 1 Summary (for context)
{json.dumps(layer1_summary.model_dump() if layer1_summary else {}, indent=2)}

# Layer 2 Detailed Documentation (for context)
{json.dumps(layer2_details.model_dump() if layer2_details else {}, indent=2)}

# Layer 3 Relationship Mapping
{json.dumps(relationships.model_dump(), indent=2)}

Evaluate the accuracy and completeness of this relationship mapping."""

        result = self._call_llm_validator(self.layer3_prompt, context)

        if result.passed:
            logger.success("Layer 3 validation passed (LLM)")
        else:
            logger.warning("Layer 3 validation failed (LLM)", issues=result.issues)

        return result

    def validate(self, state: FileState, layer: str) -> FileState:
        """
        Validate a specific layer based on current state.

        Args:
            state: Current file state
            layer: Which layer to validate ("layer1", "layer2", or "layer3")

        Returns:
            Updated state with validation result
        """
        logger.info(f"Validating {layer}", file=str(state.file_path))

        try:
            if layer == "layer1":
                result = self.validate_layer1(state.layer1_summary, state.file_content)
                state.layer1_validation = result
            elif layer == "layer2":
                result = self.validate_layer2(
                    state.layer2_details,
                    state.file_content,
                    state.layer1_summary
                )
                state.layer2_validation = result
            elif layer == "layer3":
                result = self.validate_layer3(
                    state.layer3_relationships,
                    state.file_content,
                    state.layer1_summary,
                    state.layer2_details
                )
                state.layer3_validation = result
            else:
                raise ValueError(f"Unknown layer: {layer}")

            if result.passed:
                logger.success(f"{layer} validation passed", file=str(state.file_path))
            else:
                logger.warning(
                    f"{layer} validation failed",
                    file=str(state.file_path),
                    issues=len(result.issues)
                )

            return state

        except Exception as e:
            logger.exception(f"Validation failed for {layer}: {e}")
            state.error_message = f"{layer} validation error: {str(e)}"
            return state


# Node functions for LangGraph
def validate_layer1(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for Layer 1 validation.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer1_validation
    """
    agent = ValidationAgent(config)
    return agent.validate(state, "layer1")


def validate_layer2(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for Layer 2 validation.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer2_validation
    """
    agent = ValidationAgent(config)
    return agent.validate(state, "layer2")


def validate_layer3(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for Layer 3 validation.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer3_validation
    """
    agent = ValidationAgent(config)
    return agent.validate(state, "layer3")
