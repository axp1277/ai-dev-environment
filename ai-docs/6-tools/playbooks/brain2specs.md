# Playbook: Brainstorming Session → Technical Specification

## Purpose
Convert a numbered brainstorming transcript into a structured specification document that follows the guidance in `ai-docs/4-prompts/brain2specs.md`.

## Inputs
- `ai-docs/0-brainstorming/session<session_number>.md`
- Prompt reference: `ai-docs/4-prompts/brain2specs.md`

## Steps
1. Open the session file that matches the requested `<session_number>`.
2. Review the `brain2specs` prompt to ensure the agent understands formatting expectations.
3. Provide the agent with the transcript plus the prompt instructions and request a specification titled `specs<session_number>.md`.
4. Save the generated document to `ai-docs/2-specs/specs<session_number>.md`.
5. Verify the new file includes Vision, Tasks with status glyphs, and Development Conventions sections.

## Outputs
- `ai-docs/2-specs/specs<session_number>.md`
