"""
File Summarizer Agent - Layer 1

Generates high-level summaries of C# files by directly analyzing source code
and inferring structure, purpose, and key classes.

Four Pillars:
1. Model: Ollama LLM (configurable, default: codellama:7b)
2. Prompt: External markdown file (prompts/file_summarizer.md)
3. Context: File content and metadata
4. Tools: None (LLM analyzes code directly)
"""

import json
from pathlib import Path
from typing import Dict, Any
import ollama
from loguru import logger

from ..state import FileState, FileSummary, GraphConfig


class FileSummarizerAgent:
    """
    Layer 1 Agent: Analyzes C# files and generates high-level summaries.

    Simple, focused responsibility: Take file content, return structured summary.
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the File Summarizer Agent.

        Args:
            config: Graph configuration containing model name and prompt path
        """
        self.model_name = config.summarizer_model
        self.prompt_path = config.summarizer_prompt_path
        self.system_prompt = self._load_prompt()

        # Create Ollama client with configurable base URL
        self.client = ollama.Client(host=config.ollama_base_url)

        logger.info(
            f"FileSummarizerAgent initialized",
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
        Execute the File Summarizer Agent.

        Args:
            state: Current file state containing file_path and file_content

        Returns:
            Updated state with layer1_summary populated
        """
        logger.info(f"FileSummarizerAgent invoked", file=str(state.file_path))

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
                format=FileSummary.model_json_schema()  # Pydantic structured output
            )

            # Parse response directly into Pydantic model
            summary = self._parse_response(response)

            # Update state
            state.layer1_summary = summary
            state.layer1_iterations += 1

            logger.success(
                f"FileSummarizerAgent completed",
                file=str(state.file_path),
                summary_length=len(summary.summary)
            )

            return state

        except Exception as e:
            logger.exception(f"FileSummarizerAgent failed: {e}")
            state.error_message = f"Layer 1 failed: {str(e)}"
            return state

    def _prepare_context(self, state: FileState) -> str:
        """
        Prepare the user message with file content and metadata.

        Args:
            state: Current file state

        Returns:
            Formatted message for the LLM
        """
        return f"""Analyze this C# file and generate a high-level summary.

**File:** {state.file_path.name}
**Full Path:** {str(state.file_path)}

**Code:**
```csharp
{state.file_content}
```

Respond with valid JSON matching the required schema.
"""

    def _parse_response(self, response: Dict[str, Any]) -> FileSummary:
        """
        Parse LLM response into structured FileSummary.

        With Pydantic structured output, Ollama returns valid JSON matching the schema.

        Args:
            response: Ollama chat response

        Returns:
            Validated FileSummary object
        """
        try:
            # Extract content from response (already JSON due to format parameter)
            content = response['message']['content']

            # Parse JSON directly (Ollama structured output guarantees valid JSON)
            data = json.loads(content)

            # Validate and create FileSummary (Pydantic validation)
            summary = FileSummary(**data)

            logger.debug("Successfully parsed structured output into FileSummary")
            return summary

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.debug(f"Raw response: {content}")
            raise ValueError(f"Invalid JSON from LLM: {e}")

        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise


# Node function for LangGraph
def summarize_file(state: FileState, config: GraphConfig) -> FileState:
    """
    LangGraph node function for file summarization.

    Args:
        state: Current file state
        config: Graph configuration

    Returns:
        Updated state with layer1_summary
    """
    agent = FileSummarizerAgent(config)
    return agent.invoke(state)
