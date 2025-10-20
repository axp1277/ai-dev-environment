#!/usr/bin/env bash
# DocuGen Environment Setup Script
# Activates Python UV virtual environment and verifies dependencies

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

echo "=== DocuGen Environment Setup ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    echo "Please run 'uv venv' from the project root first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✓ Virtual environment activated (Linux/Mac)"
elif [ -f "$VENV_PATH/Scripts/activate" ]; then
    source "$VENV_PATH/Scripts/activate"
    echo "✓ Virtual environment activated (Windows/Git Bash)"
else
    echo "ERROR: Could not find activation script"
    exit 1
fi

# Verify Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo ""
echo "Python version: $PYTHON_VERSION"

# Check required Python version (3.11+)
REQUIRED_VERSION="3.11"
if python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "✓ Python version meets requirements (>= $REQUIRED_VERSION)"
else
    echo "ERROR: Python $REQUIRED_VERSION or higher is required"
    exit 1
fi

# Verify key dependencies
echo ""
echo "Checking dependencies..."
MISSING_DEPS=()

# Check for required packages
for package in "langgraph" "pydantic" "ollama" "click" "rich" "loguru"; do
    if python -c "import $package" 2>/dev/null; then
        echo "✓ $package installed"
    else
        echo "✗ $package missing"
        MISSING_DEPS+=("$package")
    fi
done

# Report missing dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "WARNING: Missing dependencies detected:"
    for dep in "${MISSING_DEPS[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "Run 'uv add ${MISSING_DEPS[*]}' to install missing packages"
fi

echo ""
echo "=== Environment Ready ==="
echo "To use this environment in future shells, run:"
echo "  source .venv/bin/activate  # Linux/Mac"
echo "  .venv\\Scripts\\activate     # Windows"
echo ""
