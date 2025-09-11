# Unified Coding Standards Prompt (UCSP) for Claude Code

## Objective
Ensure consistent, well-structured code architecture across all development projects, with clear separation between agents and tools.

## Project Structure Guidelines

### 1. Directory Organization
- **Agents** (`src/agents/`): Modules using LLMs (e.g., LangGraph implementations)
- **Tools** (`src/tools/`): Pure Python modules without LLM dependencies
- Each agent/tool must have its own subdirectory named after its primary function

### 2. Subdirectory Structure
Each agent/tool subdirectory must contain:
```
tool_name/
├── cli.py          # CLI entry point (imports from core)
├── core.py         # Main functionality
├── README.md       # Documentation
├── tests/          # Unit tests
│   ├── test_cli.py
│   └── test_core.py
└── *.py           # Additional modules only when needed
```

### 3. Code Organization Principles
- **Start simple**: Begin with just `cli.py` and `core.py`
- **Split when needed**: Only create additional modules when files exceed ~1000 lines
- **Clear separation**: 
  - `cli.py`: CLI interface only, delegates to core
  - `core.py`: All business logic, classes, and utilities
- **Natural growth**: Let additional modules emerge organically from refactoring

### 4. Entry Points
- `cli.py` serves as the CLI interface, importing from `core.py`
- Configure shortcuts in `pyproject.toml` at root level
- Example: `tool-name = "src.tools.tool_name.cli:main"`

### 5. Documentation Requirements
Each `README.md` must include:
- Tool/agent purpose and functionality
- Installation instructions
- Usage examples with CLI commands
- API documentation if applicable

### 6. Code Standards
- **Logging**: Use `loguru` for all logging
- **Output Display**: Use `rich` for formatted terminal output
- **Error Handling**: Implement comprehensive error handling with clear messages
- **Type Hints**: Use type hints for all function signatures

### 7. Testing Requirements
- Create `tests/` folder in each subdirectory
- Write simple, synchronous unit tests
- Aim for maximum coverage with minimal complexity
- **Avoid**: async testing, mocks (unless absolutely necessary)
- Use `pytest` for test framework

### 8. Implementation Example

#### CLI Module (cli.py)
```python
# src/tools/document_extractor/cli.py
import click
from loguru import logger
from rich.console import Console

from .core import extract_document, validate_path

console = Console()

@click.command()
@click.option('--input', '-i', required=True, help='Input file path')
@click.option('--output', '-o', help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(input, output, verbose):
    """Document extraction tool."""
    if verbose:
        logger.add(sys.stderr, level="DEBUG")
    
    try:
        # Validate and process
        input_path = validate_path(input)
        result = extract_document(input_path, output)
        
        console.print(f"[green]✓ Extracted {result['count']} documents[/green]")
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        return 1

if __name__ == "__main__":
    exit(main())
```

#### Core Module (core.py)
```python
# src/tools/document_extractor/core.py
from pathlib import Path
from typing import Dict, Any
from loguru import logger

def validate_path(path: str) -> Path:
    """Validate input path exists and is readable."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p

def extract_document(input_path: Path, output_path: str = None) -> Dict[str, Any]:
    """Extract content from document."""
    logger.info(f"Processing {input_path}")
    
    # Main extraction logic here
    content = input_path.read_text()
    
    # Process content...
    
    if output_path:
        Path(output_path).write_text(processed_content)
    
    return {"count": 1, "status": "success"}

class DocumentProcessor:
    """More complex processing logic when needed."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    # Additional methods...
```

### pyproject.toml Entry Example
```toml
[project.scripts]
document-extractor = "src.tools.document_extractor.cli:main"
```

## Summary
This unified coding standard ensures all tools and agents follow a consistent, maintainable structure. Start with the minimal `cli.py` and `core.py` setup, and expand only when complexity demands it. Always prioritize clarity, testability, and user-friendly CLI interfaces.
