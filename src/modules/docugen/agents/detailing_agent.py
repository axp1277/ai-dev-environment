"""
Detailing Agent - Layer 2

Generates detailed function/class documentation with docstrings,
parameter descriptions, and return type analysis.

Four Pillars:
1. Model: Ollama LLM (configurable, default: codellama:13b)
2. Prompt: External markdown file (prompts/detailing_agent.md)
3. Context: File content + Layer 1 summary
4. Tools: None (LLM analyzes code directly)
"""

import json
from pathlib import Path
from typing import Dict, Any
import ollama
from loguru import logger

from ..state import FileState, DetailedDocs, GraphConfig


class DetailingAgent:
    """
    Layer 2 Agent: Generates detailed documentation for classes and methods.

    Simple, focused responsibility: Take file + summary, return detailed docs.
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the Detailing Agent.

        Args:
            config: Graph configuration containing model name and prompt path
        """
        self.model_name = config.detailing_model
        self.prompt_path = config.detailing_prompt_path
        self.system_prompt = self._load_prompt()

        logger.info(
            f"DetailingAgent initialized",
            model=self.model_name,
            prompt=str(self.prompt_path)
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
        Execute the Detailing Agent.

        Args:
            state: Current file state with file_content and layer1_summary

        Returns:
            Updated state with layer2_details populated
        """
        logger.info(f"DetailingAgent invoked", file=str(state.file_path))

        try:
            # Prepare context for LLM
            user_message = self._prepare_context(state)

            # Call Ollama with Pydantic structured output
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                format=DetailedDocs.model_json_schema()  # Pydantic structured output
            )

            # Parse response
            details = self._parse_response(response)

            # Update state
            state.layer2_details = details
            state.layer2_iterations += 1

            logger.success(
                f"DetailingAgent completed",
                file=str(state.file_path),
                classes=len(details.classes),
                methods=len(details.standalone_methods)
            )

            return state

        except Exception as e:
            logger.exception(f"DetailingAgent failed: {e}")
            state.error_message = f"Layer 2 failed: {str(e)}"
            return state

    def _prepare_context(self, state: FileState) -> str:
        """
        Prepare the user message with file content, Layer 1 summary, and metadata.

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
- Summary: {state.layer1_summary.summary}
"""

        return f"""Generate detailed documentation for this C# file.

**File:** {state.file_path.name}
**Full Path:** {str(state.file_path)}

{summary_context}

**Code:**
```csharp
{state.file_content}
```

Provide comprehensive docstrings for all classes and public methods.
Respond with valid JSON matching the required schema.
"""

    def _parse_response(self, response: Dict[str, Any]) -> DetailedDocs:
        """
        Parse LLM response into structured DetailedDocs.

        With Pydantic structured output, Ollama returns valid JSON matching the schema.

        Args:
            response: Ollama chat response

        Returns:
            Validated DetailedDocs object
        """
        try:
            # Extract content from response (already JSON due to format parameter)
            content = response['message']['content']

            # Parse JSON directly (Ollama structured output guarantees valid JSON)
            data = json.loads(content)

            # Validate and create DetailedDocs (Pydantic validation)
            details = DetailedDocs(**data)

            logger.debug("Successfully parsed structured output into DetailedDocs")
            return details

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.debug(f"Raw response: {content}")
            raise ValueError(f"Invalid JSON from LLM: {e}")

        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise


# Node function for LangGraph
def generate_details(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for detailed documentation.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer2_details
    """
    agent = DetailingAgent(config)
    return agent.invoke(state)
