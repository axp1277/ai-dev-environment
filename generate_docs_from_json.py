#!/usr/bin/env python3
"""
Quick script to generate final documentation from existing JSON layer outputs.
Use this when Layer 1-3 processing completed but Layer 4 timed out.
"""

from pathlib import Path
from src.modules.docugen.agents.documentation_agent import DocumentationAgent
from src.modules.docugen.state import GraphConfig
from src.modules.docugen.core import DocuGenConfig
from loguru import logger

# Configure paths
output_dir = Path("docs_output/test_enhanced")
layer1_json = output_dir / "layer1_summaries.json"
layer2_json = output_dir / "layer2_details.json"
layer3_json = output_dir / "layer3_relationships.json"
final_doc = output_dir / "DOCUMENTATION.md"

# Load configuration
config_file = Path("config.yaml")
docugen_config = DocuGenConfig.from_yaml(config_file)

# Create GraphConfig from DocuGenConfig
graph_config = GraphConfig(
    max_iterations=docugen_config.validation.max_iterations,
    summarizer_model=docugen_config.models.summarizer,
    detailing_model=docugen_config.models.detailing,
    relationship_model=docugen_config.models.relationship_mapper,
    documentation_model=docugen_config.models.documentation,
    validation_model=docugen_config.models.validation,
    llm_base_url=docugen_config.llm.base_url,
    llm_api_key_env=docugen_config.llm.api_key_env,
    llm_timeout=docugen_config.llm.timeout,
)

logger.info(f"Using timeout: {graph_config.llm_timeout} seconds")
logger.info(f"Using Layer 4 model: {graph_config.get_documentation_model()}")

# Create documentation agent
agent = DocumentationAgent(graph_config)

# Generate documentation
logger.info("Generating comprehensive documentation from layer JSON files...")
logger.info(f"  Layer 1: {layer1_json}")
logger.info(f"  Layer 2: {layer2_json}")
logger.info(f"  Layer 3: {layer3_json}")

result_path = agent.invoke(
    layer1_path=layer1_json,
    layer2_path=layer2_json,
    layer3_path=layer3_json,
    output_path=final_doc,
    project_name="RepoScribe.Core"
)

logger.success(f"✓ Documentation generated: {result_path}")
print(f"\n✓ Success! Documentation saved to: {result_path}")
