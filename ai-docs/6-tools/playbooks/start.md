# Playbook: Combined Brainstorming Conversion

## Purpose
Quickly generate both the PRD and the technical specification for a single brainstorming session by running the PRD and spec playbooks back to back.

## Inputs
- `ai-docs/0-brainstorming/session<session_number>.md`
- PRD prompt: `ai-docs/4-prompts/session-to-prd.md`
- Spec prompt: `ai-docs/4-prompts/brain2specs.md`

## Steps
1. Follow the Product Requirements Document playbook to create `ai-docs/1-prds/prd<session_number>.md`.
2. Follow the Technical Specification playbook to create `ai-docs/2-specs/specs<session_number>.md`.
3. Optional: if a simplification review is required, queue the `spec-simplification` playbook once the spec exists.
4. Confirm both output files link back to the same session number in their metadata.

## Outputs
- `ai-docs/1-prds/prd<session_number>.md`
- `ai-docs/2-specs/specs<session_number>.md`
