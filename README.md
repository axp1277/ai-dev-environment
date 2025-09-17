# ai-docs Universal Scaffold

The repository standardises how AI-assisted software projects store brainstorming transcripts, prompts, workflows, and delivery artifacts. With a predictable `ai-docs/` layout any coding assistant (Claude Code, Cursor, Copilot CLI, etc.) can load the context and work productively without custom setup.

## Folder Overview

```
.
├── README.md                 # This guide
└── ai-docs/                  # Project knowledge base
    ├── 0-brainstorming/      # Raw transcripts and ideation sessions
    ├── 1-prompts/            # Central prompts repository
    │   ├── core/             # Conversion prompts & shared guidance
    │   ├── roles/            # Assistant role definitions
    │   └── utilities/        # Operational/maintenance prompts
    ├── 2-workflows/          # Multi-step process guides
    ├── 3-specs/              # Technical specifications with task tracking
    ├── 4-prds/               # Product requirements documents
    ├── 5-meeting-notes/      # Meeting minutes and action reports
    └── 6-resources/          # Additional reference material
```

### Prompts (`ai-docs/1-prompts/`)
- **Core** prompts capture source-to-output conversions such as brain2specs, session-to-prd, meeting transcripts to minutes, and coding standards.
- **Roles** store assistant personas (formerly under `agents/`) so any model can adopt the right behaviour before executing a task.
- **Utilities** house operational prompts: updating spec status, generating reports, running git commits, bootstrapping projects, etc.

### Workflows (`ai-docs/2-workflows/`)
Workflow files orchestrate multiple prompts. `workflow1.md` shows the complete session pipeline (brainstorm → spec → simplification → PRD). `workflow-conventions.md` and `workflow-guidelines.md` explain how to author new workflows in a platform-neutral format.

### Delivery Artifacts
- `3-specs/` keeps implementation-ready specifications with task emojis.
- `4-prds/` stores product requirements distilled from the same sessions.
- `5-meeting-notes/` collects meeting minutes written via the transcript-to-minutes prompt.

## Getting Started

1. Capture a brainstorming session in `ai-docs/0-brainstorming/session<id>.md`.
2. Convert the session into documentation:
   - Run the spec conversion with `ai-docs/1-prompts/core/brain2specs.md` (output to `ai-docs/3-specs/`).
   - Run the PRD conversion with `ai-docs/1-prompts/core/session-to-prd.md` (output to `ai-docs/4-prds/`).
   - Use `ai-docs/2-workflows/workflow1.md` when you want the pipeline executed end to end, including the simplification step.
3. Maintain specs by updating task glyphs via `ai-docs/1-prompts/utilities/update_completion.md` and logging progress notes as needed.
4. For scope control, brief the assistant with `ai-docs/1-prompts/roles/spec-simplification-agent.md` before reviewing a spec.

## Creating New Prompts or Workflows

- Place any new conversion or system prompt under `ai-docs/1-prompts/core/`.
- Store new assistant personas in `ai-docs/1-prompts/roles/` with usage examples.
- Add operational checklists or maintenance routines to `ai-docs/1-prompts/utilities/`.
- When tasks require sequencing multiple prompts, draft a workflow in `ai-docs/2-workflows/` following the conventions file.

## Maintaining the Knowledge Base

- Commit generated specs, PRDs, and meeting notes alongside code so history remains traceable.
- Keep emoji statuses in specs current (⭕/🔄/✅) using the update utility prompt.
- Produce `assistant-context.md` files for complex code areas via `ai-docs/1-prompts/utilities/prime.md` so future assistants ramp quickly.
- Use `ai-docs/6-resources/` for reference material that does not fit prompts or workflows.

## Additional References

- `AGENTS.md`: command-to-prompt mappings, repository conventions, and workflow shortcuts.
- `ai-docs/2-workflows/workflow-conventions.md`: formatting rules for workflow authors.
- `ai-docs/3-specs/specs-2.md`: meta-spec describing the ai-docs vision.
- `ai-docs/1-prompts/utilities/setup.md`: bootstrapping checklist for new repositories.

With the centralised prompts directory and dedicated workflows, any assistant or teammate can locate the right instructions instantly and follow repeatable processes across projects.
