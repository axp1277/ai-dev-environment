# Utility Prompt: Generate a Client Update Report

## Purpose
Summarise recent work into a client-friendly changelog that highlights features, improvements, fixes, and other notable updates.

## Inputs
- Repository with recent commits or staged changes
- Optional current version sourced from `pyproject.toml`

## Steps
1. Determine the current version (if applicable) to include in the report header.
2. Review recent work using `git status` and `git diff` against the previous commit; include uncommitted work if it should be communicated.
3. Categorise changes into: New Features, Improvements, Bug Fixes, Configuration & Settings, Security & Stability.
4. Draft `UPDATE_REPORT.md` with sections for Summary and each applicable category, keeping explanations client-focused and outcome-oriented.
5. Note any dependencies, environment changes, or follow-up actions clients should know about.
6. Save `UPDATE_REPORT.md` at the repository root.

## Output
- `UPDATE_REPORT.md` summarising recent progress for stakeholders.
