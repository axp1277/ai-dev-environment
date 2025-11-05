"""
Documentation Agent - Layer 1 (Element Documentation)

Documents each code element identified by the parser using LLM.
Takes parsed structure and generates human-readable documentation.

Responsibilities:
- Iterate through each class in StructureSnapshot
- For each element (class, method, property, field), generate documentation
- Maintain full file context in each LLM prompt
- Parse and validate LLM responses
- Aggregate all documented elements per file
- Handle LLM errors gracefully
"""

import json
import time
import re
from pathlib import Path
from typing import Optional, Dict
from loguru import logger

from ..state import (
    ParserLedState,
    FileDocumentation,
    DocumentedClass,
    DocumentedMethod,
    DocumentedProperty,
    DocumentedField
)
from ....shared.parsers.csharp_structure_parser import (
    StructureSnapshot,
    ClassInfo,
    MethodInfo,
    PropertyInfo,
    AttributeInfo
)
from ....shared.core import create_chat_model


def load_prompt_template() -> str:
    """Load the element documentation prompt template."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "element_documenter.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def call_llm_with_retry(llm_model, prompt: str, element_type: str, element_name: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Call LLM with retry logic for robustness.

    Args:
        llm_model: LLM model instance
        prompt: The prompt to send
        element_type: Type of element being documented (for logging)
        element_name: Name of element being documented (for logging)
        max_retries: Maximum number of retry attempts

    Returns:
        Parsed JSON dict or None if all retries fail
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Make LLM call
            llm_start = time.time()
            response = llm_model.invoke(prompt)
            llm_duration = time.time() - llm_start

            # Extract content
            content = response.content if hasattr(response, 'content') else str(response)

            # Log response
            logger.info(
                f"  [LLM RESPONSE] {element_type} - {element_name} | "
                f"Attempt: {attempt}/{max_retries} | Duration: {llm_duration:.2f}s | Response: {len(content)} chars"
            )

            # Extract and parse JSON
            json_content = extract_json_from_response(content)
            doc_data = json.loads(json_content)

            # Success!
            if attempt > 1:
                logger.info(f"  [RETRY SUCCESS] {element_type} - {element_name} succeeded on attempt {attempt}")
            return doc_data

        except json.JSONDecodeError as e:
            logger.warning(
                f"  [JSON PARSE ERROR] {element_type} - {element_name} | Attempt {attempt}/{max_retries}",
                error=str(e),
                error_line=e.lineno if hasattr(e, 'lineno') else None,
                error_col=e.colno if hasattr(e, 'colno') else None
            )

            if attempt < max_retries:
                logger.info(f"  [RETRY] Retrying {element_type} - {element_name} (attempt {attempt + 1}/{max_retries})")
                # For retry, we could enhance the prompt to be more explicit about JSON format
                # but for now we'll just retry with the same prompt
                continue
            else:
                # Final attempt failed - log full content
                logger.error(
                    f"  [ALL RETRIES FAILED] {element_type} - {element_name} | All {max_retries} attempts failed",
                    error=str(e),
                    content_preview=content[:500],
                    full_content=content
                )
                return None

        except Exception as e:
            logger.error(
                f"  [LLM ERROR] {element_type} - {element_name} | Attempt {attempt}/{max_retries}",
                error=str(e)
            )
            if attempt < max_retries:
                logger.info(f"  [RETRY] Retrying {element_type} - {element_name} due to error")
                continue
            else:
                logger.error(f"  [ALL RETRIES FAILED] {element_type} - {element_name} | Error: {e}")
                return None

    return None


def extract_json_from_response(content: str) -> str:
    """
    Robustly extract JSON from LLM response.

    Handles:
    - Markdown code blocks (```json or ```)
    - Plain JSON with surrounding text
    - Common prefixes like "Here is the JSON:"
    - JSON objects anywhere in the text

    Args:
        content: Raw LLM response content

    Returns:
        Extracted JSON string

    Raises:
        ValueError: If no JSON can be extracted
    """
    # Strategy 1: Try markdown code blocks first
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

    # Strategy 2: Strip common prefixes and try parsing
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

    # Strategy 3: Try to find JSON object using regex
    # Look for { ... } pattern (handles nested braces)
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, cleaned_content, re.DOTALL)

    if matches:
        # Try each match, starting with the longest (likely most complete)
        for match in sorted(matches, key=len, reverse=True):
            try:
                # Validate it's actually JSON
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue

    # Strategy 4: If content looks like it starts with {, try using it directly
    if cleaned_content.startswith('{'):
        # Find the matching closing brace
        brace_count = 0
        for i, char in enumerate(cleaned_content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return cleaned_content[:i+1]

    # Strategy 5: Return original content and let json.loads fail with a clear error
    return content.strip()


def document_method(
    method: MethodInfo,
    file_content: str,
    llm_model,
    class_name: str
) -> Optional[DocumentedMethod]:
    """
    Generate documentation for a method using LLM.

    Args:
        method: MethodInfo from parser
        file_content: Full file source code
        llm_model: LLM model instance
        class_name: Name of the containing class

    Returns:
        DocumentedMethod or None if LLM fails
    """
    try:
        # Build method signature
        params_str = ", ".join(method.parameters) if method.parameters else ""
        signature = f"{method.return_type} {method.name}({params_str})"

        # Load and format prompt
        template = load_prompt_template()
        prompt = template.format(
            element_type="Method",
            element_name=method.name,
            element_signature=signature,
            file_content=file_content
        )

        # Call LLM with retry
        logger.info(f"  [LLM CALL] Method - {class_name}.{method.name} | Prompt: {len(prompt)} chars")

        doc_data = call_llm_with_retry(llm_model, prompt, "Method", f"{class_name}.{method.name}")

        if doc_data is None:
            return None

        return DocumentedMethod(
            name=method.name,
            description=doc_data.get("description", ""),
            parameters=doc_data.get("parameters", {}),
            returns=doc_data.get("returns")
        )

    except Exception as e:
        logger.error(
            f"Failed to document method {class_name}.{method.name}: {e}",
            method=method.name,
            error=str(e)
        )
        return None


def document_property(
    prop: PropertyInfo,
    file_content: str,
    llm_model,
    class_name: str
) -> Optional[DocumentedProperty]:
    """
    Generate documentation for a property using LLM.

    Args:
        prop: PropertyInfo from parser
        file_content: Full file source code
        llm_model: LLM model instance
        class_name: Name of the containing class

    Returns:
        DocumentedProperty or None if LLM fails
    """
    try:
        signature = f"{prop.type} {prop.name}"

        template = load_prompt_template()
        prompt = template.format(
            element_type="Property",
            element_name=prop.name,
            element_signature=signature,
            file_content=file_content
        )

        logger.info(f"  [LLM CALL] Property - {class_name}.{prop.name} | Prompt: {len(prompt)} chars")

        doc_data = call_llm_with_retry(llm_model, prompt, "Property", f"{class_name}.{prop.name}")

        if doc_data is None:
            return None

        return DocumentedProperty(
            name=prop.name,
            description=doc_data.get("description", "")
        )

    except Exception as e:
        logger.error(
            f"Failed to document property {class_name}.{prop.name}: {e}",
            property=prop.name,
            error=str(e)
        )
        return None


def document_field(
    field: AttributeInfo,
    file_content: str,
    llm_model,
    class_name: str
) -> Optional[DocumentedField]:
    """
    Generate documentation for a field using LLM.

    Args:
        field: AttributeInfo from parser
        file_content: Full file source code
        llm_model: LLM model instance
        class_name: Name of the containing class

    Returns:
        DocumentedField or None if LLM fails
    """
    try:
        signature = f"{field.type} {field.name}"

        template = load_prompt_template()
        prompt = template.format(
            element_type="Field",
            element_name=field.name,
            element_signature=signature,
            file_content=file_content
        )

        logger.info(f"  [LLM CALL] Field - {class_name}.{field.name} | Prompt: {len(prompt)} chars")

        doc_data = call_llm_with_retry(llm_model, prompt, "Field", f"{class_name}.{field.name}")

        if doc_data is None:
            return None

        return DocumentedField(
            name=field.name,
            description=doc_data.get("description", "")
        )

    except Exception as e:
        logger.error(
            f"Failed to document field {class_name}.{field.name}: {e}",
            field=field.name,
            error=str(e)
        )
        return None


def document_class(
    class_info: ClassInfo,
    file_content: str,
    llm_model,
    include_private: bool = True
) -> Optional[DocumentedClass]:
    """
    Generate complete documentation for a class and all its members.

    Args:
        class_info: ClassInfo from parser
        file_content: Full file source code
        llm_model: LLM model instance
        include_private: Whether to document private members

    Returns:
        DocumentedClass with all member documentation
    """
    try:
        # Document class itself
        logger.info(f"Documenting class: {class_info.name}")

        base_str = f" : {class_info.base_class}" if class_info.base_class else ""
        interfaces_str = f", {', '.join(class_info.interfaces)}" if class_info.interfaces else ""
        signature = f"class {class_info.name}{base_str}{interfaces_str}"

        template = load_prompt_template()
        prompt = template.format(
            element_type="Class",
            element_name=class_info.name,
            element_signature=signature,
            file_content=file_content
        )

        logger.info(f"  [LLM CALL] Class - {class_info.name} | Prompt: {len(prompt)} chars")

        class_doc_data = call_llm_with_retry(llm_model, prompt, "Class", class_info.name)

        if class_doc_data is None:
            return None

        documented_class = DocumentedClass(
            name=class_info.name,
            description=class_doc_data.get("description", ""),
            purpose=class_doc_data.get("purpose", "")
        )

        # Document methods
        for method in class_info.methods:
            # Skip private methods if not included
            if not include_private and 'private' in method.modifiers:
                continue

            doc_method = document_method(method, file_content, llm_model, class_info.name)
            if doc_method:
                documented_class.methods[method.name] = doc_method

        # Document properties
        for prop in class_info.properties:
            if not include_private and 'private' in prop.modifiers:
                continue

            doc_prop = document_property(prop, file_content, llm_model, class_info.name)
            if doc_prop:
                documented_class.properties[prop.name] = doc_prop

        # Document fields
        for field in class_info.attributes:
            if not include_private and 'private' in field.modifiers:
                continue

            doc_field = document_field(field, file_content, llm_model, class_info.name)
            if doc_field:
                documented_class.fields[field.name] = doc_field

        logger.info(
            f"Completed documentation for {class_info.name}",
            class_name=class_info.name,
            methods=len(documented_class.methods),
            properties=len(documented_class.properties),
            fields=len(documented_class.fields)
        )

        return documented_class

    except Exception as e:
        logger.error(
            f"Failed to document class {class_info.name}: {e}",
            class_name=class_info.name,
            error=str(e)
        )
        return None


def documentation_agent_node(state: ParserLedState) -> ParserLedState:
    """
    Documentation Agent LangGraph Node - Layer 1 (Element Documentation).

    Takes parser output and generates LLM documentation for each element.

    Args:
        state: Current workflow state with structure_snapshots populated

    Returns:
        Updated state with documented_files populated
    """
    agent_start_time = time.time()
    llm_call_count = 0
    logger.info(
        f"[AGENT START] Documentation Agent | Files: {len(state.structure_snapshots)} | Model: {state.config.llm_model}"
    )

    if not state.structure_snapshots:
        logger.warning("No structure snapshots to document")
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

    # Process each file
    total_files = len(state.structure_snapshots)
    for idx, (file_path, snapshot) in enumerate(state.structure_snapshots.items(), start=1):
        try:
            file_start_time = time.time()
            file_llm_calls = 0
            logger.info(f"[FILE] Processing {file_path} ({idx}/{total_files})")

            # Read file content for context
            full_path = Path(state.directory_path) / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # Create file documentation
            file_doc = FileDocumentation(
                file_path=file_path,
                namespace=snapshot.namespace
            )

            # Document each class
            for class_info in snapshot.classes:
                doc_class = document_class(
                    class_info=class_info,
                    file_content=file_content,
                    llm_model=llm_model,
                    include_private=state.config.include_private_members
                )

                if doc_class:
                    file_doc.classes[class_info.name] = doc_class
                    # Count LLM calls: 1 for class + 1 for each method/property/field
                    file_llm_calls += 1 + len(doc_class.methods) + len(doc_class.properties) + len(doc_class.fields)

            # Store file documentation
            state.documented_files[file_path] = file_doc

            file_duration = time.time() - file_start_time
            llm_call_count += file_llm_calls
            logger.info(
                f"[FILE] Completed {file_path} | Classes: {len(file_doc.classes)} | LLM Calls: {file_llm_calls} | Duration: {file_duration:.2f}s"
            )

        except Exception as e:
            logger.error(
                f"Failed to document file {file_path}: {e}",
                file=file_path,
                error=str(e)
            )

    # Log summary
    agent_duration = time.time() - agent_start_time
    total_classes = sum(len(doc.classes) for doc in state.documented_files.values())
    logger.info(
        f"[AGENT END] Documentation Agent | Duration: {agent_duration:.2f}s | Files: {len(state.documented_files)} | Classes: {total_classes} | LLM Calls: {llm_call_count}"
    )

    return state


# Export for LangGraph graph construction
__all__ = [
    "documentation_agent_node",
    "document_class",
    "document_method",
    "document_property",
    "document_field"
]
