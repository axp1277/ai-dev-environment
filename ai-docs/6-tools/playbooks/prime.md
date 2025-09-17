# Playbook: Prime a Codebase for AI Assistance

## Purpose
Analyze a file or directory to produce an `assistant-context.md` document summarising structure, patterns, and conventions so any AI helper can work productively in the codebase.

## Inputs
- Path to a file or directory (relative or absolute).

## Steps
1. Review the target path to understand modules, entry points, and dependencies.
2. Capture implementation patterns: coding conventions, configuration handling, error/logging approaches, and core algorithms.
3. Document domain concepts, business rules, and rationale behind major decisions.
4. Record improvement opportunities or technical debt worth noting.
5. Write the findings to `<target>/assistant-context.md` (adjacent to the analysed file or within the directory) with the sections below.

### Recommended Document Structure
- **Overview** — purpose, technology stack, and responsibilities.
- **Architecture** — component breakdown and data or control flow.
- **Implementation Notes** — key classes/functions, configuration, external integrations.
- **Usage** — typical workflows, CLI/API examples, integration tips.
- **Development Guidelines** — coding standards, testing approach, extension patterns.
- **Troubleshooting / Risks** — known issues, technical debt, edge cases.

## Output
- `assistant-context.md` containing the analysed insights, stored alongside the inspected code.

## Notes
- This playbook is read-only with respect to source files; only the documentation file is created or updated.
- Use a consistent tone and formatting so future assistants immediately understand the codebase.
- If an `assistant-context.md` already exists, update sections in place rather than duplicating information.
