"""
Relationship Mapper Agent - Layer 3

Analyzes cross-file dependencies and relationships by directly inferring
from source code without external AST parsers.

Four Pillars:
1. Model: Ollama LLM (configurable, default: codellama:7b)
2. Prompt: External markdown file (prompts/relationship_mapper.md)
3. Context: File content + Layer 1 & 2 outputs
4. Tools: None (LLM infers relationships from code)
"""

import json
from pathlib import Path
from typing import Dict, Any
import ollama
from loguru import logger

from ..state import FileState, RelationshipMap, GraphConfig


class RelationshipMapperAgent:
    """
    Layer 3 Agent: Maps cross-file dependencies and architectural relationships.

    Simple, focused responsibility: Analyze dependencies, return relationship map.
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the Relationship Mapper Agent.

        Args:
            config: Graph configuration containing model name and prompt path
        """
        self.model_name = config.relationship_model
        self.prompt_path = config.relationship_prompt_path
        self.system_prompt = self._load_prompt()

        # Create Ollama client with configurable base URL
        self.client = ollama.Client(host=config.ollama_base_url)

        logger.info(
            f"RelationshipMapperAgent initialized",
            model=self.model_name,
            prompt=str(self.prompt_path),
            base_url=config.ollama_base_url
        )

    def _load_prompt(self) -> str:
        """Load system prompt from markdown file."""
        try:
            with open(self.prompt_path, 'r') as f:
                prompt = f.read()
            logger.debug(f"Loaded prompt from {self.prompt_path}")
            return prompt
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {self.prompt_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading prompt: {e}")
            raise

    def invoke(self, state: FileState) -> FileState:
        """
        Execute the Relationship Mapper Agent.

        Args:
            state: Current file state with file_content, layer1_summary, layer2_details

        Returns:
            Updated state with layer3_relationships populated
        """
        logger.info(f"RelationshipMapperAgent invoked", file=str(state.file_path))

        try:
            # Prepare context for LLM
            user_message = self._prepare_context(state)

            # Call Ollama with Pydantic structured output
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                format=RelationshipMap.model_json_schema()  # Pydantic structured output
            )

            # Parse response
            relationships = self._parse_response(response)

            # Update state
            state.layer3_relationships = relationships
            state.layer3_iterations += 1

            logger.success(
                f"RelationshipMapperAgent completed",
                file=str(state.file_path),
                dependencies=len(relationships.dependencies),
                role=relationships.architectural_role
            )

            return state

        except Exception as e:
            logger.exception(f"RelationshipMapperAgent failed: {e}")
            state.error_message = f"Layer 3 failed: {str(e)}"
            return state

    def _prepare_context(self, state: FileState) -> str:
        """
        Prepare the user message with all previous layer outputs.

        Args:
            state: Current file state

        Returns:
            Formatted message for the LLM
        """
        summary_context = ""
        if state.layer1_summary:
            summary_context = f"""
**Layer 1 Summary:**
- Purpose: {state.layer1_summary.purpose}
- Category: {state.layer1_summary.category}
- Key Classes: {', '.join(state.layer1_summary.key_classes)}
"""

        details_context = ""
        if state.layer2_details:
            class_names = [c.name for c in state.layer2_details.classes]
            details_context = f"""
**Layer 2 Details:**
- Classes Documented: {', '.join(class_names) if class_names else 'None'}
- Standalone Methods: {len(state.layer2_details.standalone_methods)}
"""

        return f"""Analyze cross-file dependencies and relationships for this C# file.

**File:** {state.file_path.name}
**Full Path:** {str(state.file_path)}

{summary_context}
{details_context}

**Code:**
```csharp
{state.file_content}
```

Identify:
1. Dependencies (what this file uses)
2. Dependents (what uses this file - infer from usage patterns)
3. Architectural role (Repository, Service, Controller, etc.)
4. Data flow patterns

Respond with valid JSON matching the required schema.
"""

    def _parse_response(self, response: Dict[str, Any]) -> RelationshipMap:
        """
        Parse LLM response into structured RelationshipMap.

        With Pydantic structured output, Ollama returns valid JSON matching the schema.

        Args:
            response: Ollama chat response

        Returns:
            Validated RelationshipMap object
        """
        try:
            # Extract content from response (already JSON due to format parameter)
            content = response['message']['content']

            # Parse JSON directly (Ollama structured output guarantees valid JSON)
            data = json.loads(content)

            # Validate and create RelationshipMap (Pydantic validation)
            relationships = RelationshipMap(**data)

            logger.debug("Successfully parsed structured output into RelationshipMap")
            return relationships

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.debug(f"Raw response: {content}")
            raise ValueError(f"Invalid JSON from LLM: {e}")

        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise


# Node function for LangGraph
def map_relationships(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for relationship mapping.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer3_relationships
    """
    agent = RelationshipMapperAgent(config)
    return agent.invoke(state)
