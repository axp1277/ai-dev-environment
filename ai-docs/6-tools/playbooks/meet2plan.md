# Playbook: Meeting Transcript → Action Report

## Purpose
Turn a numbered meeting transcript into structured minutes with action items, decisions, and follow-ups.

## Inputs
- `ai-docs/0-brainstorming/transcript<meeting_number>.md` (or the applicable transcript folder if you maintain a dedicated meetings directory)
- Prompt reference: `ai-docs/4-prompts/transcript2minutes.md`

## Steps
1. Open the transcript that matches `<meeting_number>`.
2. Load the `transcript2minutes` prompt to understand the required sections and tone.
3. Feed the transcript and prompt to your assistant, asking for an output named `minutes<meeting_number>.md`.
4. Save the generated report to `ai-docs/3-meeting-notes/minutes<meeting_number>.md` (update the folder path if your structure differs).
5. Review the output to ensure decisions, action items, and participants are captured accurately.

## Output
- `ai-docs/3-meeting-notes/minutes<meeting_number>.md`
