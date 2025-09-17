# Utility Prompt: Update Specification Task Status

## Purpose
Apply progress emojis to tasks within a specification so the document reflects the latest completion state.

## Inputs
- Specification file: `ai-docs/3-specs/specs<spec_number>.md`

## Status Rules
- **Sub-atomic tasks** (bullet list entries under a task):
  - ✅ Completed
  - 🔄 In progress
  - ⭕ Not started
- **Atomic tasks** (e.g., `Task 1.0` headings):
  - ✅ All subtasks complete
  - 🚧 Some subtasks complete
  - ⭕ No subtasks started

## Steps
1. Open `ai-docs/3-specs/specs<spec_number>.md` and review the task hierarchy.
2. For each sub-atomic task, assign the emoji that matches its real-world status.
3. For each atomic task, evaluate all subtasks and set the status emoji according to the rules above.
4. Preserve existing formatting and numbering while updating emojis.
5. Save the file in place and document the update in a short summary (for example in commit notes or a changelog section).

## Output
- Updated `ai-docs/3-specs/specs<spec_number>.md` with refreshed status indicators.
