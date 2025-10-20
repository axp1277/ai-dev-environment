"""
DocumentationAgent - Layer 4

LLM-driven agent that reads JSON outputs from Layers 1-3 and generates
comprehensive markdown documentation for the entire codebase.
"""

import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from loguru import logger

from ..state import GraphConfig
from ..core import create_chat_model


class DocumentationOutput(BaseModel):
    """Output from DocumentationAgent."""
    markdown_content: str = Field(..., description="Complete markdown documentation")
    title: str = Field(..., description="Documentation title")


class DocumentationAgent:
    """
    Agent that synthesizes all layer outputs into comprehensive documentation.

    This agent reads the JSON files created by Layers 1-3 and uses an LLM
    to generate a cohesive, well-structured markdown documentation report.
    """

    def __init__(self, config: GraphConfig):
        """
        Initialize the DocumentationAgent.

        Args:
            config: Graph configuration with model and prompt settings
        """
        self.config = config
        self.model_name = config.detailing_model  # Use detailing model for quality
        self.prompt_path = Path("src/modules/docugen/prompts/documentation_agent.md")

        # Create LangChain chat model
        self.model = create_chat_model(
            config.llm_base_url,
            self.model_name,
            config.llm_api_key_env,
            config.llm_timeout
        )

        logger.info(
            "DocumentationAgent initialized",
            model=self.model_name,
            base_url=config.llm_base_url
        )

    def invoke(
        self,
        layer1_path: Path,
        layer2_path: Path,
        layer3_path: Path,
        output_path: Path,
        project_name: Optional[str] = None
    ) -> Path:
        """
        Generate comprehensive markdown documentation from layer JSON files.

        Args:
            layer1_path: Path to layer1_summaries.json
            layer2_path: Path to layer2_details.json
            layer3_path: Path to layer3_relationships.json
            output_path: Path where markdown file should be written
            project_name: Optional project name for documentation title

        Returns:
            Path to generated markdown documentation
        """
        logger.info("DocumentationAgent invoked")

        try:
            # Load JSON data
            with open(layer1_path, 'r', encoding='utf-8') as f:
                layer1_data = json.load(f)

            with open(layer2_path, 'r', encoding='utf-8') as f:
                layer2_data = json.load(f)

            with open(layer3_path, 'r', encoding='utf-8') as f:
                layer3_data = json.load(f)

            # Load prompt template
            system_prompt = self._load_prompt()

            # Prepare context
            context = self._prepare_context(
                layer1_data,
                layer2_data,
                layer3_data,
                project_name or "Codebase"
            )

            # Invoke LLM
            logger.info("Calling LLM to generate documentation")
            from langchain_core.messages import SystemMessage, HumanMessage

            response = self.model.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=context)
            ])

            markdown_content = response.content

            # Write to output file
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            logger.success(f"Documentation generated: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"DocumentationAgent failed: {e}")
            raise

    def _load_prompt(self) -> str:
        """Load the system prompt from file."""
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt file not found: {self.prompt_path}, using default")
            return self._get_default_prompt()

    def _get_default_prompt(self) -> str:
        """Default system prompt if file not found."""
        return """You are a technical documentation expert. Your task is to create comprehensive,
well-structured markdown documentation for a codebase.

You will receive JSON data containing:
- Layer 1: High-level file summaries and categorization
- Layer 2: Detailed class and method documentation
- Layer 3: Architectural relationships and dependencies

Generate markdown documentation that:
1. Provides a clear overview of the codebase architecture
2. Documents each component thoroughly
3. Explains relationships and dependencies
4. Uses proper markdown formatting (headings, code blocks, lists)
5. Is organized logically and easy to navigate

Output ONLY the markdown content, no preamble or explanation."""

    def _prepare_context(
        self,
        layer1_data: list,
        layer2_data: list,
        layer3_data: list,
        project_name: str
    ) -> str:
        """
        Prepare the context prompt for the LLM.

        Args:
            layer1_data: List of file summaries
            layer2_data: List of detailed documentation
            layer3_data: List of relationships
            project_name: Name of the project

        Returns:
            Formatted context string
        """
        return f"""Generate comprehensive markdown documentation for the {project_name} project.

# Layer 1: File Summaries
{json.dumps(layer1_data, indent=2)}

# Layer 2: Detailed Documentation
{json.dumps(layer2_data, indent=2)}

# Layer 3: Relationships and Architecture
{json.dumps(layer3_data, indent=2)}

Please create a well-structured, comprehensive markdown documentation that synthesizes
all this information into a cohesive technical document."""
