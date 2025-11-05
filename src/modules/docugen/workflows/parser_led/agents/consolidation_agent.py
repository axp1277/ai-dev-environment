"""
Consolidation Agent - Post-Processing Layer (Duplicate Element Consolidation)

Identifies elements that appear in multiple files (inherited/interface members)
and consolidates their documentation using LLM review.

Responsibilities:
- Scan all documented files for duplicate element names
- Group duplicate definitions by element signature
- Use LLM to review and consolidate multiple definitions
- Store consolidated documentation in state
- Preserve source file tracking for transparency

This agent operates after documentation and validation, before compilation.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger

from ..state import (
    ParserLedState,
    FileDocumentation,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField,
    ConsolidatedElement
)
from ....shared.core import create_chat_model


@dataclass
class ElementReference:
    """Reference to a documented element in a specific file."""
    file_path: str
    class_name: str
    element_name: str
    element_type: str  # "method", "property", "field"
    element_doc: object  # DocumentedMethod, DocumentedProperty, or DocumentedField
    signature: str  # For identification


def load_consolidation_prompt() -> str:
    """Load the consolidation prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "consolidation_prompt.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_json_from_response(content: str) -> str:
    """
    Extract JSON from LLM response (reused from documentation_agent).

    Handles markdown code blocks, plain JSON, and common prefixes.
    """
    import re

    # Strategy 1: Markdown code blocks
    if "```json" in content:
        try:
            extracted = content.split("```json")[1].split("```")[0].strip()
            if extracted:
                return extracted
        except IndexError:
            pass

    if "```" in content:
        try:
            extracted = content.split("```")[1].split("```")[0].strip()
            if extracted:
                return extracted
        except IndexError:
            pass

    # Strategy 2: Strip common prefixes
    common_prefixes = [
        "Here is the JSON:",
        "Here's the JSON:",
        "The JSON is:",
        "JSON:",
        "Output:",
        "Result:",
    ]

    cleaned_content = content.strip()
    for prefix in common_prefixes:
        if cleaned_content.lower().startswith(prefix.lower()):
            cleaned_content = cleaned_content[len(prefix):].strip()
            break

    # Strategy 3: Regex for JSON object
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, cleaned_content, re.DOTALL)

    if matches:
        for match in sorted(matches, key=len, reverse=True):
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue

    # Strategy 4: Direct content starting with {
    if cleaned_content.startswith('{'):
        brace_count = 0
        for i, char in enumerate(cleaned_content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return cleaned_content[:i+1]

    return content.strip()


def call_llm_with_retry(llm_model, prompt: str, element_key: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Call LLM with retry logic for consolidation.

    Args:
        llm_model: LLM model instance
        prompt: The prompt to send
        element_key: Identifier for the element being consolidated (for logging)
        max_retries: Maximum number of retry attempts

    Returns:
        Parsed JSON dict or None if all retries fail
    """
    for attempt in range(1, max_retries + 1):
        try:
            llm_start = time.time()
            response = llm_model.invoke(prompt)
            llm_duration = time.time() - llm_start

            content = response.content if hasattr(response, 'content') else str(response)

            logger.info(
                f"  [LLM RESPONSE] Consolidation - {element_key} | "
                f"Attempt: {attempt}/{max_retries} | Duration: {llm_duration:.2f}s | Response: {len(content)} chars"
            )

            # Extract and parse JSON
            json_content = extract_json_from_response(content)
            consolidated_data = json.loads(json_content)

            if attempt > 1:
                logger.info(f"  [RETRY SUCCESS] {element_key} succeeded on attempt {attempt}")
            return consolidated_data

        except json.JSONDecodeError as e:
            logger.warning(
                f"  [JSON PARSE ERROR] Consolidation - {element_key} | Attempt {attempt}/{max_retries}",
                error=str(e)
            )

            if attempt < max_retries:
                logger.info(f"  [RETRY] Retrying {element_key} (attempt {attempt + 1}/{max_retries})")
                continue
            else:
                logger.error(
                    f"  [ALL RETRIES FAILED] {element_key} | All {max_retries} attempts failed",
                    error=str(e),
                    content_preview=content[:500]
                )
                return None

        except Exception as e:
            logger.error(
                f"  [LLM ERROR] Consolidation - {element_key} | Attempt {attempt}/{max_retries}",
                error=str(e)
            )
            if attempt < max_retries:
                continue
            else:
                return None

    return None


def identify_duplicate_elements(documented_files: Dict[str, FileDocumentation]) -> Dict[str, List[ElementReference]]:
    """
    Scan all documented files and identify elements that appear multiple times.

    Focus on inherited/interface members that appear in multiple classes.
    An element is considered duplicate if it has the same name across different files.

    Args:
        documented_files: Dictionary of file_path -> FileDocumentation

    Returns:
        Dictionary mapping element_key -> list of ElementReference
        Only includes elements that appear 2+ times
    """
    # Map: element_key -> list of ElementReference
    element_map: Dict[str, List[ElementReference]] = {}

    for file_path, file_doc in documented_files.items():
        for class_name, doc_class in file_doc.classes.items():
            # Process methods
            for method_name, method_doc in doc_class.methods.items():
                # Create signature (simple version: just name for now)
                signature = f"{method_name}"
                element_key = f"method:{signature}"

                ref = ElementReference(
                    file_path=file_path,
                    class_name=class_name,
                    element_name=method_name,
                    element_type="method",
                    element_doc=method_doc,
                    signature=signature
                )

                if element_key not in element_map:
                    element_map[element_key] = []
                element_map[element_key].append(ref)

            # Process properties
            for prop_name, prop_doc in doc_class.properties.items():
                signature = f"{prop_name}"
                element_key = f"property:{signature}"

                ref = ElementReference(
                    file_path=file_path,
                    class_name=class_name,
                    element_name=prop_name,
                    element_type="property",
                    element_doc=prop_doc,
                    signature=signature
                )

                if element_key not in element_map:
                    element_map[element_key] = []
                element_map[element_key].append(ref)

            # Process fields
            for field_name, field_doc in doc_class.fields.items():
                signature = f"{field_name}"
                element_key = f"field:{signature}"

                ref = ElementReference(
                    file_path=file_path,
                    class_name=class_name,
                    element_name=field_name,
                    element_type="field",
                    element_doc=field_doc,
                    signature=signature
                )

                if element_key not in element_map:
                    element_map[element_key] = []
                element_map[element_key].append(ref)

    # Filter to only duplicates (2+ occurrences)
    duplicates = {k: v for k, v in element_map.items() if len(v) >= 2}

    logger.info(f"Identified {len(duplicates)} duplicate elements across files")
    for element_key, refs in duplicates.items():
        logger.info(f"  - {element_key}: {len(refs)} occurrences")

    return duplicates


def consolidate_element_definitions(
    element_key: str,
    references: List[ElementReference],
    llm_model
) -> Optional[ConsolidatedElement]:
    """
    Use LLM to consolidate multiple definitions of the same element.

    Args:
        element_key: Unique identifier for the element
        references: List of ElementReference for this element
        llm_model: LLM model instance

    Returns:
        ConsolidatedElement or None if consolidation fails
    """
    try:
        # Prepare definitions for LLM
        definitions = []
        for i, ref in enumerate(references, start=1):
            if ref.element_type == "method":
                method_doc: DocumentedMethod = ref.element_doc
                definitions.append({
                    "source": f"{ref.file_path} ({ref.class_name}.{ref.element_name})",
                    "description": method_doc.description,
                    "parameters": method_doc.parameters if method_doc.parameters else {},
                    "returns": method_doc.returns
                })
            elif ref.element_type == "property":
                prop_doc: DocumentedProperty = ref.element_doc
                definitions.append({
                    "source": f"{ref.file_path} ({ref.class_name}.{ref.element_name})",
                    "description": prop_doc.description
                })
            elif ref.element_type == "field":
                field_doc: DocumentedField = ref.element_doc
                definitions.append({
                    "source": f"{ref.file_path} ({ref.class_name}.{ref.element_name})",
                    "description": field_doc.description
                })

        # Load prompt template
        template = load_consolidation_prompt()

        # Format prompt
        first_ref = references[0]
        prompt = template.format(
            element_type=first_ref.element_type.capitalize(),
            element_name=first_ref.element_name,
            element_signature=first_ref.signature,
            definition_count=len(definitions),
            definitions_json=json.dumps(definitions, indent=2)
        )

        logger.info(f"  [LLM CALL] Consolidating {element_key} | Definitions: {len(definitions)} | Prompt: {len(prompt)} chars")

        # Call LLM
        consolidated_data = call_llm_with_retry(llm_model, prompt, element_key)

        if consolidated_data is None:
            logger.warning(f"Failed to consolidate {element_key}")
            return None

        # Create ConsolidatedElement
        source_files = [ref.file_path for ref in references]

        consolidated = ConsolidatedElement(
            element_name=first_ref.element_name,
            element_type=first_ref.element_type,
            signature=first_ref.signature,
            consolidated_description=consolidated_data.get("description", ""),
            consolidated_parameters=consolidated_data.get("parameters") if first_ref.element_type == "method" else None,
            consolidated_returns=consolidated_data.get("returns") if first_ref.element_type == "method" else None,
            source_files=source_files,
            original_count=len(references)
        )

        logger.info(f"  [SUCCESS] Consolidated {element_key} from {len(references)} definitions")
        return consolidated

    except Exception as e:
        logger.error(f"Failed to consolidate {element_key}: {e}", error=str(e))
        return None


def consolidation_agent_node(state: ParserLedState) -> ParserLedState:
    """
    Consolidation Agent LangGraph Node - Post-Processing Layer.

    Identifies duplicate elements across files and consolidates their documentation.

    Args:
        state: Current workflow state with documented_files populated

    Returns:
        Updated state with consolidated_elements populated
    """
    agent_start_time = time.time()
    logger.info(
        f"[AGENT START] Consolidation Agent | Files: {len(state.documented_files)} | Model: {state.config.llm_model}"
    )

    if not state.documented_files:
        logger.warning("No documented files to consolidate")
        return state

    # Create LLM model
    try:
        llm_model = create_chat_model(
            base_url=state.config.llm_base_url,
            model_name=state.config.llm_model,
            api_key_env=state.config.llm_api_key_env,
            timeout=state.config.llm_timeout
        )
    except Exception as e:
        logger.error(f"Failed to create LLM model: {e}")
        raise

    # Identify duplicates
    duplicates = identify_duplicate_elements(state.documented_files)

    if not duplicates:
        logger.info("No duplicate elements found - skipping consolidation")
        return state

    # Consolidate each duplicate
    consolidated_map: Dict[str, ConsolidatedElement] = {}
    llm_call_count = 0
    success_count = 0

    for element_key, references in duplicates.items():
        consolidated = consolidate_element_definitions(element_key, references, llm_model)

        if consolidated:
            consolidated_map[element_key] = consolidated
            success_count += 1

        llm_call_count += 1

    # Store in state
    state.consolidated_elements = consolidated_map

    # Log summary
    agent_duration = time.time() - agent_start_time
    logger.info(
        f"[AGENT END] Consolidation Agent | Duration: {agent_duration:.2f}s | "
        f"Duplicates: {len(duplicates)} | Consolidated: {success_count} | LLM Calls: {llm_call_count}"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "consolidation_agent_node",
    "identify_duplicate_elements",
    "consolidate_element_definitions"
]
