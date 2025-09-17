# Command: document.md
# Description: Automatically generates comprehensive documentation for a module directory
# Usage: document <module_directory>

MODULE_DIR="$1"

if [ -z "$MODULE_DIR" ]; then
    echo "Error: Please provide a module directory path"
    echo "Usage: document <module_directory>"
    exit 1
fi

if [ ! -d "$MODULE_DIR" ]; then
    echo "Error: Directory '$MODULE_DIR' does not exist"
    exit 1
fi

README_FILE="$MODULE_DIR/README.md"

echo "Analyzing module directory: $MODULE_DIR..."
echo "Generating documentation..."

Analyze all files in the directory "$MODULE_DIR" including:
- All source code files (*.js, *.ts, *.py, *.java, *.cpp, *.go, *.rs, etc.)
- Configuration files (package.json, pom.xml, Cargo.toml, go.mod, etc.)
- Existing documentation files
- Test files
- Any other relevant files

Your task is to create a comprehensive README.md file that includes:

1. **Module Overview**
   - Clear, concise description of what this module does
   - Primary purpose and key features
   - Technology stack used

2. **Installation & Setup**
   - Prerequisites required
   - Step-by-step installation instructions
   - Configuration requirements

3. **Usage Guide**
   - Basic usage examples with code snippets
   - Common use cases
   - API documentation (if applicable)
   - Command-line interface documentation (if applicable)

4. **Architecture Overview**
   - Create a Mermaid diagram that clearly illustrates:
     - Main components and their relationships
     - Data flow between components
     - External dependencies
     - Key classes/modules and their interactions
   - The diagram should be simple, clear, and easy to understand

5. **Project Structure**
   - Directory layout explanation
   - Purpose of key files and folders

6. **Development**
   - How to contribute
   - Testing instructions
   - Build instructions

7. **Additional Information**
   - License information (if found)
   - Author/maintainer information
   - Links to additional resources

Format the README.md using proper Markdown syntax with:
- Clear section headers
- Code blocks with appropriate syntax highlighting
- The Mermaid diagram in a code block with ```mermaid notation
- Bullet points and numbered lists where appropriate
- Tables if needed for structured information

Ensure the documentation is:
- Concise but comprehensive
- Written for developers who are new to the codebase
- Technically accurate based on the actual code analysis
- Professional and well-organized

Write the complete README.md content to "$README_FILE".

echo "Documentation generated successfully at $README_FILE"