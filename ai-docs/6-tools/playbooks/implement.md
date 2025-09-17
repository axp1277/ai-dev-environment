# Playbook: Implement a Specification Task

## Purpose
Execute all subtasks within a target specification task and update the document to reflect completion.

## Inputs
- Target task number (e.g., `Task 3.0`)
- Specification file containing the task (typically `ai-docs/2-specs/specs<session_number>.md`)

## Steps
1. Locate the specification that includes the chosen task number and review its atomic and sub-atomic items.
2. Identify dependencies, acceptance criteria, and related tasks before coding.
3. Implement each sub-atomic item, committing changes or notes as necessary.
4. Test and validate the work to ensure nothing else regresses.
5. Update status emojis in the spec: mark subtasks ✅ and elevate the parent task to ✅ once everything is done.
6. Produce a brief completion note summarizing work performed, modified files, and any follow-up items.

## Output
- Implementation changes applied to the codebase or project.
- Updated specification reflecting the completed task.
