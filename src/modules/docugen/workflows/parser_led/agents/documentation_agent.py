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

        # Call LLM
        logger.debug(f"Documenting method: {class_name}.{method.name}")
        response = llm_model.invoke(prompt)

        # Parse JSON response
        content = response.content if hasattr(response, 'content') else str(response)

        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Try to parse JSON
        try:
            doc_data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse JSON for method {class_name}.{method.name}",
                error=str(e),
                content_preview=content[:200]
            )
            raise

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

        logger.debug(f"Documenting property: {class_name}.{prop.name}")
        response = llm_model.invoke(prompt)

        content = response.content if hasattr(response, 'content') else str(response)

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        doc_data = json.loads(content)

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

        logger.debug(f"Documenting field: {class_name}.{field.name}")
        response = llm_model.invoke(prompt)

        content = response.content if hasattr(response, 'content') else str(response)

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        doc_data = json.loads(content)

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

        logger.debug(f"Calling LLM for class {class_info.name} with prompt length: {len(prompt)}")
        response = llm_model.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        logger.debug(f"Received LLM response for class {class_info.name}, content length: {len(content)}, content preview: {content[:100]}")

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Try to parse JSON
        try:
            class_doc_data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse JSON for class {class_info.name}",
                error=str(e),
                content_preview=content[:200],
                full_content=content
            )
            raise

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
    logger.info(
        "Starting Documentation Agent",
        total_files=len(state.structure_snapshots),
        llm_model=state.config.llm_model
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
            logger.info(
                f"Documenting file {idx}/{total_files}",
                file=file_path,
                progress=f"{idx}/{total_files}"
            )

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

            # Store file documentation
            state.documented_files[file_path] = file_doc

        except Exception as e:
            logger.error(
                f"Failed to document file {file_path}: {e}",
                file=file_path,
                error=str(e)
            )

    # Log summary
    total_classes = sum(len(doc.classes) for doc in state.documented_files.values())
    logger.info(
        "Documentation Agent complete",
        documented_files=len(state.documented_files),
        total_classes=total_classes
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
