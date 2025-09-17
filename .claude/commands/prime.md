# Prime - Code Review and Documentation Command

## Description

Analyzes a specified file or directory to understand its current implementation and generates comprehensive documentation in a claude.md file. This command prepares codebases for new feature development by providing AI agents with complete context about existing code structure, patterns, and functionality.

## Usage

```
@prime <file_or_directory_path>
```

## Parameters

- `file_or_directory_path`: Path to the file or directory to analyze (required)
  - Can be relative (e.g., `src/modules/`) or absolute path
  - If file: analyzes the single file and creates claude.md in its directory
  - If directory: recursively analyzes all files and creates claude.md in the target directory

## Examples

```bash
# Analyze a specific module directory
@prime src/modules/

# Analyze the entire source directory
@prime src/

# Analyze a specific file
@prime src/app.py

# Analyze current directory
@prime .

# Analyze a subdirectory with relative path
@prime ./pipelines/
```

## What It Does

1. **Code Structure Analysis**:
   - Surveys directory structure and file organization
   - Identifies entry points, main components, and dependencies
   - Maps component relationships and data flow

2. **Implementation Pattern Discovery**:
   - Analyzes coding conventions and design patterns
   - Documents configuration management approaches
   - Identifies error handling and logging strategies
   - Extracts API endpoints, database schemas, or key algorithms

3. **Context Documentation**:
   - Captures business logic and domain concepts
   - Documents the "why" behind implementation decisions
   - Identifies technical debt and improvement opportunities
   - Preserves institutional knowledge from comments and docstrings

4. **claude.md Generation**:
   - Creates comprehensive documentation in the target directory
   - Includes overview, architecture, implementation details, and usage examples
   - Provides development guidelines and troubleshooting information
   - Structures content for easy AI agent consumption

## Generated claude.md Structure

The generated documentation includes:

- **Overview**: Purpose, key technologies, and what the code accomplishes
- **Architecture**: Component breakdown, design decisions, and interaction patterns
- **Implementation**: Key classes/functions, configuration requirements, schemas
- **Usage**: Common workflows, code examples, and integration points
- **Development**: Coding conventions, testing approaches, extension guidelines

## Use Cases

- **Pre-Development Analysis**: Before adding new features to unfamiliar code
- **Onboarding**: Quickly understand existing codebase structure and patterns
- **Legacy Documentation**: Create documentation for undocumented legacy code
- **Refactoring Preparation**: Understand current implementation before major changes
- **AI Context Creation**: Provide comprehensive context for AI-assisted development

## Output

Creates a `claude.md` file in the analyzed directory containing:
- Complete codebase documentation
- Implementation patterns and conventions
- Usage examples and common workflows
- Development guidelines and best practices
- Troubleshooting and extension guidance

## Notes

- The command performs read-only analysis - no code modifications are made
- Generated claude.md files follow a consistent, structured format
- Analysis depth scales with codebase complexity
- Focuses on providing actionable information for future development work
- Designed to work seamlessly with AI coding assistants for enhanced productivity