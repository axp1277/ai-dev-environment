Create a new Python project with standard directory structure and uv package management

# Project Setup

Initialize a new Python project with the following structure and configurations:

## Steps

1. Initialize the project with uv if pyproject.toml doesn't exist
2. Sync dependencies to create .venv
3. Create standard directory structure

## Directory Structure

```
.
├── .claude/
│   └── commands/
├── ai-docs/
│   ├── 0-brainstorming/
│   ├── 1-prompts/
│   ├── 2-specs/
│   └── 3-resources/
├── docs/
│   └── wiki/
├── src/
├── tests/
├── output/
├── examples/
├── logs/
├── .venv/
└── pyproject.toml
```

## Implementation

```bash
# Check if pyproject.toml exists, if not initialize with uv
if [ ! -f "pyproject.toml" ]; then
    echo "Initializing project with uv..."
    uv init
fi

# Sync dependencies to create .venv
echo "Syncing dependencies..."
uv sync

# Create directory structure
echo "Creating directory structure..."

# Create main directories
directories=(
    ".claude/commands"
    "ai-docs/0-brainstorming"
    "ai-docs/1-prompts"
    "ai-docs/2-specs"
    "ai-docs/3-resources"
    "docs/wiki"
    "src"
    "tests"
    "examples"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "Created $dir"
    else
        echo "Skipping $dir - already exists"
    fi
done

# Create CLAUDE.md if it doesn't exist
if [ ! -f "CLAUDE.md" ]; then
    cat > CLAUDE.md << 'EOF'
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project managed with `uv` package manager.

- Python version: >=3.12
- Package manager: `uv`

## High-Level Architecture

The project follows a structured approach with:
- `/ai-docs/0-brainstorming/` - Initial ideas and brainstorming sessions
- `/ai-docs/1-prompts/` - AI prompts for development tasks
- `/ai-docs/2-specs/` - Technical specifications derived from brainstorming
- `/ai-docs/3-resources/` - Additional resources and references
- `/src/` - Main source code
- `/tests/` - Test files
- `/examples/` - Example usage and demos
- `/docs/` - Documentation
- `/docs/wiki/` - Wiki-style documentation

## Common Commands

### Environment Setup
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
.venv\scripts\activate     # Windows

# Install dependencies
uv pip sync
```

### Running the Application
```bash
uv run main.py
```

### Testing and Linting
No test framework or linting configuration is currently set up. These will be added as the project develops.

## Development Conventions

### Python Standards
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Write clear docstrings for all functions, classes, and modules
- Implement appropriate validation for data structures

### Package Management
- Use `uv` as the Python package manager
- Dependencies are managed through `pyproject.toml`
- Document all dependencies and their purpose
EOF
    echo "Created CLAUDE.md"
else
    echo "CLAUDE.md already exists"
fi

# Create a basic main.py if it doesn't exist
if [ ! -f "src/main.py" ]; then
    cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""Main entry point for the application."""


def main():
    """Run the main application."""
    print("Hello, World!")


if __name__ == "__main__":
    main()
EOF
    echo "Created src/main.py"
fi

# Create a basic __init__.py in src
if [ ! -f "src/__init__.py" ]; then
    touch src/__init__.py
    echo "Created src/__init__.py"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.coverage
.pytest_cache/
htmlcov/

# Distribution
dist/
build/
*.egg-info/

# Environment
.env
.env.*

# OS
.DS_Store
Thumbs.db
EOF
    echo "Created .gitignore"
fi

echo "Project setup complete!"
```