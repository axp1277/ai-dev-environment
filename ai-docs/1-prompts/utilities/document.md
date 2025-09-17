# Utility Prompt: Document a Module Directory

## Purpose
Generate a comprehensive `README.md` for a given module by analysing its source, configuration, tests, and existing docs.

## Inputs
- Target directory path (relative to the repository root unless otherwise specified)

## Steps
1. Inspect the directory structure, including source files, configuration files, tests, and existing documentation.
2. Summarise the module overview: purpose, key features, and primary technology choices.
3. Describe installation and setup requirements, including prerequisites and configuration.
4. Document usage patterns with code examples or CLI instructions as appropriate.
5. Outline the internal architecture and include a Mermaid diagram that highlights major components and their interactions.
6. Provide a project structure reference that explains important files and folders.
7. Detail development practices: testing approach, coding standards, deployment steps, troubleshooting tips, and contribution guidelines.
8. Save the generated documentation as `README.md` in the target directory, overwriting or updating the file in place.

## Output
- `<module_directory>/README.md` containing the full documentation for the module.
