# Product Requirements Document

## Executive Summary
This project aims to create a universal AI development framework that provides a standardized, "plug-and-play" architecture for AI coding tools across different platforms (Claude Code, Codex, etc.). The framework establishes consistent folder structures, workflow definitions, and conversion capabilities to enable seamless project initialization and development regardless of the specific AI coding tool being used.

## Vision Statement
To create a universal adapter framework that eliminates fragmentation across AI coding tools by providing standardized project structures and workflows that work consistently across any AI agentic coding environment.

## Objectives
- Establish a standardized folder structure that works across all AI coding frameworks
- Create reusable workflow templates that can be applied to any project
- Develop automated conversion capabilities between different document types (brainstorming to PRD, PRD to specs, transcripts to meeting notes)
- Enable rapid project scaffolding through template repository functionality
- Reduce context switching and learning curves when moving between different AI coding tools
- Provide a consistent development methodology that scales across teams and projects

## Target Users
- **Developers using AI coding tools**: Software engineers who work with multiple AI coding assistants and need consistent project structures and workflows
- **Technical teams transitioning between AI tools**: Development teams that want to maintain consistency when switching between different AI coding platforms
- **Project managers and technical leads**: Leadership roles that need standardized documentation and workflow processes for AI-assisted development projects

## Key Features

### Core Features (Must-Have)
1. **Standardized Folder Structure**: Implementation of a seven-part hierarchy with the following order:
   - 0-brainstorming/ (Initial idea sessions and transcripts)
   - 1-prompts/ (Central prompts repository with `core/`, `roles/`, and `utilities/` subfolders)
   - 2-workflows/ (Workflow definitions and orchestration notes)
   - 3-specs/ (Detailed specification documents with atomic tasks)
   - 4-prds/ (High-level product requirement documents)
   - 5-meeting-notes/ (Summaries of general meetings or transcripts)
   - 6-resources/ (Reference documents, examples, guidelines)

2. **Document Conversion System**: Automated prompts to convert:
   - Brainstorming sessions to PRDs using session-to-prd prompt
   - PRDs to technical specifications using prd-to-specs prompt
   - General transcripts to meeting notes using session-to-meeting-notes prompt
   - Brainstorming sessions directly to specs using brain2specs prompt

3. **Sequential Numbering System**: Consistent file naming convention (session1.md → prd1.md → specs1.md) that maintains traceability between related documents

4. **Multi-Agent Workflow Support**: Sequential agent execution including:
   - Initial conversion agent (brainstorm to PRD/specs)
   - Simplification/review agent to prevent over-engineering
   - Specification refinement to ensure atomic and subatomic task definition

5. **Template Repository**: GitHub template repository functionality enabling one-click project initialization with complete folder structure

6. **Flexible Session Handling**: Support for both brainstorming sessions and general meeting transcripts in the same 0-brainstorming folder with different conversion workflows

### Secondary Features (Should-Have)
1. **Rust-Based Scaffolding Tool**: Standalone executable for rapid project initialization without requiring development environment setup
2. **Markdown-Driven Workflows**: Simple workflow definitions that can be executed by AI agents without complex orchestration tools
3. **Private Template Support**: Ability to maintain private template repositories for team-specific or proprietary workflows
4. **Cross-Platform Compatibility**: Framework design that works with Claude Code, Codex, and other AI coding tools without modification
5. **Command Integration**: Support for custom commands (like brain2-specs 1) that trigger specific workflow sequences

### Future Features (Could-Have)
1. **Advanced Workflow Orchestration**: Integration with tools like LangGraph for complex multi-agent workflows when simple markdown workflows become insufficient
2. **Integrated Tool Support**: Built-in support for CLI tools and MCP servers within the framework structure
3. **Cross-Language Support**: Framework adaptation for Rust, C#, Python, and other programming languages
4. **Team Collaboration Features**: Enhanced template sharing and version control for distributed teams
5. **Analytics and Metrics**: Tracking of workflow efficiency and document conversion success rates

## Technical Considerations
- **GitHub Template Repository**: Utilizes GitHub's native template functionality for easy project replication, with support for private templates
- **Rust Implementation**: Scaffolding tool implemented in Rust for cross-platform binary distribution and easy team sharing
- **Markdown-Based Configuration**: All workflows and prompts defined in markdown for human readability and AI parseability
- **Tool Agnostic Design**: Framework structure independent of specific AI coding tool implementations
- **File System Organization**: Hierarchical folder structure optimized for AI agent navigation and logical development flow
- **Simple Workflow Engine**: Initial implementation using markdown instructions rather than complex orchestration to validate agent capability

## Success Criteria
- Successful conversion of existing ai-dev-environment repository to GitHub template
- Complete implementation of 7-folder structure with appropriate numbering conventions and logical ordering
- Functional document conversion workflows supporting multiple output types (PRD, specs, meeting notes)
- Working multi-agent workflows with simplification/review capabilities
- Rust-based scaffolding tool that generates complete project structure
- Zero-configuration deployment on new projects using template repository
- Consistent workflow execution across different AI coding platforms
- Reduction in project setup time from hours to minutes
- Successful testing with both brainstorming sessions and meeting transcripts

## Out of Scope
- Integration with specific AI model APIs or services
- Development of new AI coding tools or frameworks
- Custom UI or web-based interfaces for workflow management
- Advanced project management features beyond basic documentation workflows
- Real-time collaboration features or live editing capabilities
- Integration with external project management tools (Jira, Asana, etc.)
- Complex orchestration tools (LangGraph) in initial implementation

## Dependencies
- GitHub repository access for template functionality
- Rust development environment for scaffolding tool creation
- Existing ai-dev-environment repository as foundation
- Access to AI coding tools (Claude Code, Codex) for testing and validation
- Markdown processing capabilities in target AI coding environments
- File system access for folder structure creation and management
