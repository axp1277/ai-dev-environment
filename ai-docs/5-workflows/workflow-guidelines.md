# Workflow Creation Guidelines and Best Practices

## Overview
Use these guidelines to design workflows that remain portable across AI assistants, automation scripts, or manual execution. The goal is to produce checklists that are explicit, parameterised, and easy to follow without tool-specific commands.

## Creation Process

### 1. Planning
- Define the single outcome the workflow achieves.
- List required inputs, expected outputs, and validation steps.
- Identify which tasks depend on others and which can happen in parallel.
- Choose variables (e.g., `$SESSION_NUMBER`, `$TARGET_LANG`) to keep the workflow reusable.

### 2. Structure
Follow the template described in `workflow-conventions.md` and ensure each section is present:
- Variables
- Overview
- Prerequisites
- Workflow Steps
- Execution Checklist (optional)
- Expected Outputs
- Success Criteria

### 3. Detailing Steps
- Start each step with an imperative verb (“Generate”, “Review”, “Validate”).
- Name the responsible role or agent and link to its definition where relevant.
- Reference prompts or playbooks by file path.
- Indicate the exact input files and where outputs should be stored.
- Note if the step can run in parallel with others.

### 4. Variable Strategy
- Use uppercase snake case for variables.
- Explain each variable in the Variables section, including examples.
- Replace all mutable values (paths, filenames, parameters) with variables.
- Remind users to substitute variables before asking an assistant to act.

## Reusable Step Patterns

### Agent-Guided Step
```
Step N: Review Specification Scope
- Role: spec-simplification-agent (see agents/spec-simplification-agent.md)
- Inputs: 0-brainstorming/session$SESSION_NUMBER.md, 2-specs/specs$SESSION_NUMBER.md
- Output: 2-specs/specs$SESSION_NUMBER-simplified.md
```

### Prompt-Driven Conversion
```
Step N: Create PRD
- Reference: ai-docs/4-prompts/session-to-prd.md
- Inputs: 0-brainstorming/session$SESSION_NUMBER.md
- Output: 1-prds/prd$SESSION_NUMBER.md
```

### Local Tool Invocation
```
Step N: Update Spec Progress
- Tool: ai-docs/6-tools/playbooks/update_completion.md
- Inputs: Session number, current spec file
- Output: Updated progress notes in the spec
```

## Best Practices
1. **Single Responsibility** — keep workflows focused; chain them if needed.
2. **Explicit Dependencies** — state when a step must wait for another to finish.
3. **Parallelisation Notes** — flag steps that may run concurrently after prerequisites.
4. **Validation Hooks** — add checkpoints (“Confirm file exists”, “Review accuracy”).
5. **Error Guidance** — note common failure modes and recovery suggestions.
6. **Plain Language** — avoid platform-specific jargon so any assistant can interpret the instructions.

## Quality Checklist
- [ ] Variables documented with purpose and examples.
- [ ] Every step lists required inputs and expected outputs.
- [ ] References to prompts, playbooks, or tools use canonical repository paths.
- [ ] Success criteria are measurable and tied to generated artifacts.
- [ ] Notes cover parallel execution or manual review requirements where applicable.
- [ ] No hard-coded session numbers, usernames, or environment-specific commands remain.

## Common Pitfalls
- **Hard-coded values** — always parameterise.
- **Implied dependencies** — be explicit with ordering.
- **Vague steps** — “Process file” is insufficient; describe the action and outcome.
- **Missing validation** — ensure every workflow has a way to confirm completion.

## Documentation Tips
- Include a “Last Updated” note when workflows change materially.
- Link related workflows or playbooks so assistants discover adjacent processes easily.
- Capture lessons learned in a notes section to improve future iterations.
