# Utility Prompt: Merge Brainstorming Updates into a Specification

## Purpose
Bring fresh ideas from a new brainstorming session into an existing specification without losing structure, numbering, or prior context.

## Inputs
- Brainstorming transcript: `ai-docs/0-brainstorming/session<session_number>.md`
- Target specification: `ai-docs/3-specs/specs<spec_number>.md`

## Steps
1. Review both documents and list any features, tasks, or constraints in the session that do not appear in the spec.
2. Decide where each new item belongs within the spec's Vision, Tasks, or Development Conventions sections.
3. Integrate the updates directly into the spec, keeping numbering, emoji status, and formatting consistent.
4. When enhancing an existing item, merge details instead of duplicating tasks.
5. Annotate impacted sections with a short note such as "Updated using session<session_number>.md" to preserve traceability.
6. Return the revised specification document.

## Output
- Updated `ai-docs/3-specs/specs<spec_number>.md` incorporating the new brainstorming insights.
