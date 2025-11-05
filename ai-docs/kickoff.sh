#!/bin/bash

# Kickoff Script - Initialize a new project
# This script resets the project to a clean state while preserving resources and prompts

set -e  # Exit on error

echo "🚀 Starting project kickoff..."

# Get the project root directory (parent of ai-docs)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 Project root: $PROJECT_ROOT"

# Step 1: Initialize UV at project root
echo ""
echo "📦 Initializing UV..."
cd "$PROJECT_ROOT"

if [ -f "pyproject.toml" ]; then
    echo "⚠️  pyproject.toml already exists. Skipping uv init."
else
    uv init
fi

echo "🔄 Running uv sync..."
uv sync

# Step 2: Clean ai-docs directories (except 3-resources and 4-prompts)
echo ""
echo "🧹 Cleaning ai-docs directories..."
cd "$SCRIPT_DIR"

# List of directories to clean (empty their contents)
DIRS_TO_CLEAN=(
    "0-brainstorming"
    "0-emails"
    "0-meetings"
    "0-voice"
    "1-meeting-minutes"
    "2-bugs"
    "2-chores"
    "2-diagrams"
    "2-features"
    "2-prds"
    "2-specs"
    "2-user-stories"
    "2-validation"
    "3-analysis"
    "4-misc"
    "5-issues"
    "5-workflows"
)

for dir in "${DIRS_TO_CLEAN[@]}"; do
    if [ -d "$dir" ]; then
        echo "  Cleaning $dir..."
        rm -rf "$dir"/*
    fi
done

echo "✓ Directories cleaned (3-resources and 4-prompts preserved)"

# Step 3: Create new directory structure at project root
echo ""
echo "📂 Creating project directories..."
cd "$PROJECT_ROOT"

mkdir -p src
echo "  ✓ Created src/"

mkdir -p tests
echo "  ✓ Created tests/"

mkdir -p docs
echo "  ✓ Created docs/"

# Step 4: Create configuration files at project root
echo ""
echo "📝 Creating configuration files..."

# Create .env.example (empty)
if [ ! -f ".env.example" ]; then
    touch .env.example
    echo "  ✓ Created .env.example"
else
    echo "  ⚠️  .env.example already exists, skipping"
fi

# Create .env (empty)
if [ ! -f ".env" ]; then
    touch .env
    echo "  ✓ Created .env"
else
    echo "  ⚠️  .env already exists, skipping"
fi

# Create .gitignore with comprehensive patterns
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
*.cover
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
ENV/
env/

# UV specific
.uv/

# Environment files
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
EOF
    echo "  ✓ Created .gitignore"
else
    echo "  ⚠️  .gitignore already exists, skipping"
fi

echo ""
echo "✅ Project kickoff complete!"
echo ""
echo "📋 Summary:"
echo "  • UV initialized and synced"
echo "  • ai-docs directories cleaned (3-resources & 4-prompts preserved)"
echo "  • Created: src/, tests/, docs/"
echo "  • Created: .env.example, .env, .gitignore"
echo ""
echo "🎯 Ready to start your new project!"
