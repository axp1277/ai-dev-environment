# Workflow 1: Complete Session Processing Pipeline

## Variables
- `$SESSION_NUMBER` — session number to process (e.g., `2` maps to `session2.md`)

## Overview
Process a brainstorming session through the full documentation pipeline: generate the initial specification, run a simplification review, and produce the companion PRD.

## Workflow Steps

### Step 1: Generate Technical Specification
- **Role**: `brain2specs-agent`
- **Inputs**: `0-brainstorming/session$SESSION_NUMBER.md`
- **Playbook**: `ai-docs/6-tools/playbooks/brain2specs.md`
- **Output**: `2-specs/specs$SESSION_NUMBER.md`

### Step 2: Review and Simplify Specification
- **Role**: `spec-simplification-agent`
- **Inputs**:
  - `0-brainstorming/session$SESSION_NUMBER.md`
  - `2-specs/specs$SESSION_NUMBER.md`
- **Guidance**: `agents/spec-simplification-agent.md`
- **Output**: `2-specs/specs$SESSION_NUMBER-simplified.md`

### Step 3: Generate Product Requirements Document
- **Role**: `brain2prd-agent`
- **Inputs**: `0-brainstorming/session$SESSION_NUMBER.md`
- **Playbook**: `ai-docs/6-tools/playbooks/session2prd.md`
- **Output**: `1-prds/prd$SESSION_NUMBER.md`

## Execution Checklist
- Substitute `$SESSION_NUMBER` with the target value before sharing file paths with an assistant.
- Run each step in order; pause between steps if human review is required.
- Capture notes about decisions or deviations directly in the workflow file if helpful for future runs.

## Expected Outputs
- `2-specs/specs$SESSION_NUMBER.md`
- `2-specs/specs$SESSION_NUMBER-simplified.md`
- `1-prds/prd$SESSION_NUMBER.md`

## Success Criteria
- [ ] Specification reflects the session content for `$SESSION_NUMBER`
- [ ] Simplified specification aligns with original intent and flags removed scope
- [ ] PRD captures business context and requirements from the same session
- [ ] All artifacts reference the source session number for traceability
