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

from pathlib import Path
from loguru import logger

from ..state import FileState, DetailedDocs, GraphConfig
from ..core import create_chat_model


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

        # Create LangChain chat model with structured output support
        base_model = create_chat_model(
            config.llm_base_url,
            self.model_name,
            config.llm_api_key_env,
            config.llm_timeout
        )

        # Configure model to output structured DetailedDocs
        self.model = base_model.with_structured_output(DetailedDocs)

        logger.info(
            f"DetailingAgent initialized",
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

            # Call LangChain model with structured output (returns DetailedDocs directly)
            from langchain_core.messages import SystemMessage, HumanMessage

            details = self.model.invoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ])

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
