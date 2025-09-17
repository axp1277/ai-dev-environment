# Repository Guidelines

## Project Structure & Module Organization
- `ai-docs/` holds the knowledge base: brainstorming transcripts, PRDs, specs, prompts, workflows, and playbooks.
- `agents/` stores role definitions and operating instructions for specialized assistants.
- When adding new documentation, mirror the numbering pattern (`0-brainstorming`, `1-prds`, `2-specs`, etc.) so agents resolve related files quickly.

## Command-to-Prompt Rules
Use these shortcuts in conversations; agents should resolve each command to the indicated assets:
- `brain2specs <n>` → Read `ai-docs/0-brainstorming/session<n>.md` and apply `ai-docs/4-prompts/brain2specs.md`, saving to `ai-docs/2-specs/specs<n>.md`.
- `session2prd <n>` → Transform the same session file using `ai-docs/4-prompts/session-to-prd.md`, output `ai-docs/1-prds/prd<n>.md`.
- `start <n>` → Run both commands above sequentially; reference `ai-docs/5-workflows/workflow1.md` for orchestration.
- `workflow <id> <n>` → Follow `ai-docs/5-workflows/workflow<id>.md`; consult `agents/workflow-executor-agent.md` for execution procedure.
- `update_completion <n>` → Refresh task emojis in `ai-docs/2-specs/specs<n>.md` using `ai-docs/6-tools/playbooks/update_completion.md`.
- `implement <task>` → Implement the specified task and update its spec per `ai-docs/6-tools/playbooks/implement.md`.
- Add new commands only if their prompts/workflows live in `ai-docs/` and are documented here.

## Development Workflow
- Maintain documentation changes beside their source prompts/workflows; no Python CLI is required.
- Regenerate specs or PRDs by invoking the commands above directly with the corresponding prompts.
- When extending workflows, update both the workflow file and this rules section.

## Coding Style & Naming Conventions
- Keep Markdown sections concise: Vision → Tasks → Development Conventions for specs.
- Name workflows `workflowN.md`; playbooks in lowercase snake case (e.g., `brain2specs.md`).
- Use plain ASCII; add comments only where logic would be ambiguous to agents.

## Testing & Validation
- Manual validation: ensure generated documents include required sections and correct numbering.
- For new workflows or prompts, run a dry run with sample session numbers and verify outputs land in the right folders.
- Record deviations or manual adjustments inside workflow files under “Notes”.

## Commit & Pull Request Guidelines
- Use short, imperative messages (e.g., “Document workflow shortcuts in AGENTS.md”).
- Include updated prompts/workflows/specs when behaviour changes.
- PR descriptions should mention affected commands and any manual verifications performed.

## Agent Authoring Tips
- Store new agent definitions in `agents/` with examples illustrating when to invoke them.
- Align prompts (`ai-docs/4-prompts/`) with their playbooks (`ai-docs/6-tools/playbooks/`) and update the command mapping if invocation keywords change.
