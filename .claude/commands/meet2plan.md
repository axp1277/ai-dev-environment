# Meeting Transcript to Report Command

## Command
`/meet2plan <meeting_number>`

## Description
Converts meeting transcripts into structured meeting reports with action items and key decisions.

## Arguments
- `meeting_number`: The meeting transcript number (e.g., 001, 002, etc.)

## Instructions for Claude Code Agent

Review the meeting transcript transcript<meeting_number>.md from the ai-docs/0-meetings/ folder and create a comprehensive meeting report minutes<meeting_number>.md in the ai-docs/2-meeting-minutes/ folder following the guidelines provided by the ai-docs/1-prompts/transcript2minutes.md.

Meeting number is $ARGUMENTS