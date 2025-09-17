# Utility Prompt: Git Add, Commit & Push (AI-Assisted)

## Purpose
Stage changes, determine semantic versioning impact, generate a clear commit message, and push the result to the remote repository.

## Inputs
- Optional issue numbers for closure annotations
- Repository with pending changes and configured remote

## Steps
1. Review modifications via `git status` and `git diff` to understand scope.
2. Assess whether the change requires a semantic version bump in `pyproject.toml`; update the version when necessary.
3. Craft a detailed commit message using conventional commits, noting version transitions if they occurred.
4. Include `Closes #<issue>` annotations for any supplied issues.
5. Stage files with `git add .` and create the commit.
6. Push changes to the default remote/branch (`git push`).
7. Summarise the work performed, version adjustments, and closed issues.

## Output
- Remote branch updated with the committed changes.
- Recap of version movement and issue closures.
