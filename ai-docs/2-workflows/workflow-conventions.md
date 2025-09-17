# Workflow Syntax and Conventions for Agent Coordination

## Purpose
Define a consistent way to write workflow instructions that any AI coding assistant—or a human following a checklist—can execute without relying on platform-specific commands.

## Workflow Template
```markdown
# Workflow N: [Workflow Name]

## Variables
- `$SESSION_NUMBER` — explain purpose
- `$CUSTOM_VAR` — document additional variables

## Overview
[High-level summary of what the workflow delivers]

## Prerequisites
- [Files, prompts, agents, or tools required before starting]

## Workflow Steps
[Sequential steps referencing prompts, utility guides, or tools]

## Execution Checklist
[Optional structured list that mirrors the steps for quick validation]

## Expected Outputs
[List all artifacts with variable notation]

## Success Criteria
[Checkbox list to confirm completion]
```

## Writing Steps
- Use descriptive headings such as "Step 1: Generate Technical Specification".
- Reference supporting material explicitly: core prompts (`ai-docs/1-prompts/core/...`), utility prompts (`ai-docs/1-prompts/utilities/...`), or role guides (`ai-docs/1-prompts/roles/...`).
- Include exact file paths with variables so assistants can substitute values reliably.
- If a step can be parallelised, note it inline (e.g., “Steps 2 and 3 may run in parallel once Step 1 finishes”).

## Variable Conventions
- Prefix variables with `$` and explain them in the Variables section.
- Use variables in every path or filename that changes between runs (`3-specs/specs$SESSION_NUMBER.md`).
- Before sharing paths with an assistant, replace variables with concrete values to prevent mistakes.

## Referencing Agents and Tools
- **Agent roles**: link to the agent definition file and outline the expected input/output at that step.
- **Prompts**: cite the file containing the system instructions so assistants can load them.
- **Local tools/scripts**: include the command to run and note any required parameters.
- **Manual reviews**: call out when a human check is required before the workflow continues.

## Validation Patterns
- Add pre- and post-step checks (e.g., “Confirm `specs$SESSION_NUMBER.md` exists before continuing”).
- Encourage logging progress in a Notes section when workflows are long-running.
- Provide fallback guidance for common errors (missing files, prompt failures, etc.).

## Naming Guidelines
- Workflow files: `workflow1.md`, `workflow2.md`, or descriptive names like `workflow-complete-processing.md`.
- Step identifiers: lowercase with underscores if referenced programmatically (`generate_spec`).
- Output files: maintain the ai-docs numbering system (`prd$SESSION_NUMBER.md`).

## Best Practices
1. **Single Responsibility** — keep each workflow focused.
2. **Modularity** — design steps that are reusable in other workflows.
3. **Clarity** — prefer plain-language instructions over platform-specific syntax.
4. **Traceability** — ensure outputs reference their originating session or input.
5. **Adaptability** — note where alternative prompts or tools could be substituted if an assistant lacks capabilities.
