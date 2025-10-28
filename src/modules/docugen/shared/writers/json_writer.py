"""
JSON Writer

Saves documentation layer outputs as JSON files for the DocumentationAgent.
"""

import json
from pathlib import Path
from typing import Dict
from loguru import logger

from ...workflows.llm_first.state import FileState


def save_layer_outputs(results: Dict[Path, FileState], output_dir: Path) -> Dict[str, Path]:
    """
    Save all layer outputs as JSON files.

    Creates three JSON files:
    - layer1_summaries.json: All file summaries
    - layer2_details.json: All detailed documentation
    - layer3_relationships.json: All relationship mappings

    Args:
        results: Dictionary mapping file paths to their FileState
        output_dir: Directory to save JSON files

    Returns:
        Dictionary with paths to created JSON files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare Layer 1 data
    layer1_data = []
    for file_path, state in results.items():
        if state.layer1_summary:
            layer1_data.append({
                "file": str(file_path),
                "summary": state.layer1_summary.summary,
                "purpose": state.layer1_summary.purpose,
                "category": state.layer1_summary.category,
                "key_classes": state.layer1_summary.key_classes,
            })

    # Prepare Layer 2 data
    layer2_data = []
    for file_path, state in results.items():
        if state.layer2_details:
            layer2_data.append({
                "file": str(file_path),
                "classes": [
                    {
                        "name": cls.name,
                        "description": cls.description,
                        "methods": [
                            {
                                "name": m.name,
                                "signature": m.signature,
                                "description": m.description,
                                "parameters": m.parameters,
                                "returns": m.returns
                            } for m in cls.methods
                        ]
                    } for cls in state.layer2_details.classes
                ],
                "standalone_methods": [
                    {
                        "name": m.name,
                        "signature": m.signature,
                        "description": m.description,
                        "parameters": m.parameters,
                        "returns": m.returns
                    } for m in state.layer2_details.standalone_methods
                ]
            })

    # Prepare Layer 3 data
    layer3_data = []
    for file_path, state in results.items():
        if state.layer3_relationships:
            layer3_data.append({
                "file": str(file_path),
                "architectural_role": state.layer3_relationships.architectural_role,
                "dependencies": [
                    {
                        "file": dep.file,
                        "classes_used": dep.classes_used,
                        "purpose": dep.purpose,
                        "relationship_type": dep.relationship_type
                    } for dep in state.layer3_relationships.dependencies
                ],
                "dependents": state.layer3_relationships.dependents
            })

    # Save to files
    output_files = {}

    layer1_path = output_dir / "layer1_summaries.json"
    with open(layer1_path, 'w', encoding='utf-8') as f:
        json.dump(layer1_data, f, indent=2)
    output_files['layer1'] = layer1_path
    logger.info(f"Saved Layer 1 summaries to {layer1_path}")

    layer2_path = output_dir / "layer2_details.json"
    with open(layer2_path, 'w', encoding='utf-8') as f:
        json.dump(layer2_data, f, indent=2)
    output_files['layer2'] = layer2_path
    logger.info(f"Saved Layer 2 details to {layer2_path}")

    layer3_path = output_dir / "layer3_relationships.json"
    with open(layer3_path, 'w', encoding='utf-8') as f:
        json.dump(layer3_data, f, indent=2)
    output_files['layer3'] = layer3_path
    logger.info(f"Saved Layer 3 relationships to {layer3_path}")

    return output_files
