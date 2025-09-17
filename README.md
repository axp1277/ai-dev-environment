# ai-docs Universal Scaffold

This repository is a template for running AI-assisted software projects with a consistent "ai-docs" knowledge base. It standardises how brainstorming sessions, PRDs, specs, workflows, and agent prompts live together so any coding assistant (Claude Code, Cursor, Copilot CLI, etc.) can step in without custom setup.

## Folder Overview

```
.
├── README.md                     # This guide
├── agents/                       # Assistant role definitions (Markdown)
└── ai-docs/                      # Project knowledge base
    ├── 0-brainstorming/          # Raw transcripts and ideation sessions
    ├── 1-prds/                   # Product requirement documents
    ├── 2-specs/                  # Technical specifications with task tracking
    ├── 3-meeting-notes/          # Meeting minutes and action reports
    ├── 4-prompts/                # Conversion prompts & coding standards
    ├── 5-workflows/              # Multi-step process guides
    ├── 6-tools/playbooks/        # Assistant-agnostic runbooks (ex-commands)
    └── 7-resources/              # Reference material & supporting docs
```

### Agents (`agents/`)
Each Markdown file defines a specialised assistant profile (persona, responsibilities, outputs). Use these to brief any AI model before handing over a task. Examples:
- `agents/agent-architect.md`: designs new assistant configs.
- `agents/spec-simplification-agent.md`: keeps specs aligned with original brainstorming intent.
- `agents/workflow-executor-agent.md`: walks through workflow files and reports progress.

### Prompts & Playbooks
- Prompts in `ai-docs/4-prompts/` describe the formatting and expectations for conversions (brainstorm→spec, session→PRD, transcript→minutes, coding standards, etc.).
- Playbooks in `ai-docs/6-tools/playbooks/` replace former slash-commands. Each file lists Inputs → Steps → Outputs so any assistant or human can execute the routine. Start with `ai-docs/6-tools/README.md` for a quick index.
- Command mappings live in `AGENTS.md`; use those shortcuts to pick the correct prompt/workflow when chatting with an assistant.

### Workflows (`ai-docs/5-workflows/`)
Workflow files capture end-to-end processes. `workflow1.md` shows the full session pipeline (brainstorm → spec → simplification → PRD) using playbooks and agent roles. `workflow-conventions.md` and `workflow-guidelines.md` explain how to write new workflows in a platform-neutral way.

## Getting Started

1. **Capture a brainstorming session** in `ai-docs/0-brainstorming/sessionN.md`.
2. **Generate documentation** using the command rules or playbooks:
   - Consult `AGENTS.md` to translate shortcuts (e.g., `brain2specs 2`) into the correct prompt + output file.
   - Alternatively, open the relevant playbook (`ai-docs/6-tools/playbooks/brain2specs.md`, `session2prd.md`) and execute the checklist manually.
   - For multi-step automation, follow `ai-docs/5-workflows/workflow1.md` and associated playbooks.
3. **Track progress** inside specs by updating task glyphs (see `ai-docs/6-tools/playbooks/update_completion.md`).
4. **Review scope** with `agents/spec-simplification-agent.md` whenever specs drift.

Any assistant that can read Markdown can follow the steps; platform-specific commands are no longer required.

## Creating New Workflows or Playbooks

1. Draft a playbook when a task is a single conversion or small checklist. Follow the Inputs/Steps/Outputs template.
2. Create a workflow when multiple playbooks must be chained. Reference the relevant playbooks/agents and include validation notes.
3. Store supporting prompts in `ai-docs/4-prompts/` so future runs stay consistent.

## Maintaining the Knowledge Base

- **Version control**: Commit generated specs/PRDs/notes alongside code so documentation evolves with the project.
- **Status updates**: Keep emojis in specs current (⏳/🔄/✅/🚧) using the update playbook.
- **Agent refresh**: When the team invents new helper roles, add them to `agents/` with examples.
- **Context docs**: Use the `prime` playbook (`ai-docs/6-tools/playbooks/prime.md`) to produce `assistant-context.md` files summarising code modules for AIs.

## Adapting for Your Stack

- Extend playbooks with language- or framework-specific steps (e.g., run tests, build docs).
- Add scripts to `ai-docs/6-tools/` if a task benefits from automation; reference them from playbooks.
- Mirror this structure in new repos by copying `ai-docs/` and `agents/`, then tailoring prompts to your domain.

## Additional Resources

- `ai-docs/6-tools/README.md`: index of available playbooks/runbooks.
- `AGENTS.md`: command-to-prompt rules and contributor guidance.
- `ai-docs/5-workflows/workflow-conventions.md`: formatting rules for workflow authors.
- `agents/` directory: ready-to-use assistant personas.
- `ai-docs/2-specs/specs-2.md`: a meta-spec describing the universal ai-docs vision.

With this layout, any AI coding assistant—or a human teammate—can onboard quickly, run the right playbook, and produce consistent artifacts.
