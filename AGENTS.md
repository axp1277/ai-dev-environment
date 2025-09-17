# Repository Guidelines

## Project Structure & Module Organization
- `ai-docs/` holds the full knowledge base: brainstorming transcripts, prompts, workflows, specs, PRDs, and resources.
- Prompts now live in a single location (`ai-docs/1-prompts/`) with subfolders for core conversions, role definitions, and utilities.
- When adding new documentation, follow the numbering pattern (`0-brainstorming`, `1-prompts`, `2-workflows`, `3-specs`, `4-prds`, `5-meeting-notes`, `6-resources`).

## Command-to-Prompt Rules
Use these shortcuts in conversations; resolve each command to the indicated assets:
- `brain2specs <n>` → Read `ai-docs/0-brainstorming/session<n>.md` and apply `ai-docs/1-prompts/core/brain2specs.md`, saving to `ai-docs/3-specs/specs<n>.md`.
- `session2prd <n>` → Transform the same session using `ai-docs/1-prompts/core/session-to-prd.md`, output `ai-docs/4-prds/prd<n>.md`.
- `start <n>` → Execute `ai-docs/2-workflows/workflow1.md` (full pipeline: spec, simplification, PRD).
- `workflow <id> <n>` → Follow `ai-docs/2-workflows/workflow<id>.md`; consult `ai-docs/1-prompts/roles/workflow-executor-agent.md` for execution procedure.
- `update_completion <n>` → Refresh task emojis in `ai-docs/3-specs/specs<n>.md` using `ai-docs/1-prompts/utilities/update_completion.md`.
- `implement <task>` → Implement the specified task and update its spec per `ai-docs/1-prompts/utilities/implement.md`.
- `report_updates` → Summarise recent work using `ai-docs/1-prompts/utilities/report_updates.md`.
- Add new commands only if their prompts/workflows live inside `ai-docs/` and are documented here.

## Development Workflow
- Maintain documentation changes beside their source prompts or workflows; no specialised CLI is required.
- Regenerate specs or PRDs by invoking the command mappings above with the corresponding prompts.
- When extending workflows, update both the workflow file and this rules section so shortcuts stay accurate.

## Coding Style & Naming Conventions
- Specs remain structured as Vision → Tasks → Development Conventions.
- Name workflows `workflowN.md`; utility prompts use lowercase snake case.
- Keep Markdown ASCII-friendly; add clarifying comments only when an instruction would otherwise be ambiguous.

## Testing & Validation
- Validate generated documents manually to ensure required sections exist and numbering is correct.
- For new workflows or prompts, run a dry run with sample session numbers and confirm outputs land in the right folders.
- Record deviations or manual adjustments inside workflow files under “Notes”.

## Commit & Pull Request Guidelines
- Use short, imperative messages (e.g., “Refactor prompts directory layout”).
- Include updated prompts/workflows/specs whenever behaviour changes.
- PR descriptions should mention affected commands and any validation performed.

## Prompt Authoring Tips
- Store new role definitions in `ai-docs/1-prompts/roles/` with examples showing when to invoke them.
- Keep conversion prompts under `ai-docs/1-prompts/core/`, and operational checklists in `ai-docs/1-prompts/utilities/`.
- Update this file whenever a new shortcut or workflow is introduced so assistants can route requests correctly.
