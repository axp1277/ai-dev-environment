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

from pathlib import Path
from loguru import logger

from ..state import FileState, FileSummary, GraphConfig
from docugen.shared.core import create_chat_model


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

        # Create LangChain chat model with structured output support
        base_model = create_chat_model(
            config.llm_base_url,
            self.model_name,
            config.llm_api_key_env,
            config.llm_timeout
        )

        # Configure model to output structured FileSummary
        self.model = base_model.with_structured_output(FileSummary)

        logger.info(
            f"FileSummarizerAgent initialized",
            model=self.model_name,
            prompt=str(self.prompt_path),
            base_url=config.llm_base_url
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

            # Call LangChain model with structured output (returns FileSummary directly)
            from langchain_core.messages import SystemMessage, HumanMessage

            summary = self.model.invoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ])

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
