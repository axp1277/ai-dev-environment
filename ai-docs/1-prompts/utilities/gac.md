# Utility Prompt: Git Add & Commit (AI-Assisted)

## Purpose
Review staged changes, determine the appropriate semantic version bump (if applicable), craft a high-quality commit message, and perform `git add`/`git commit` in one sequence.

## Inputs
- Optional list of issue numbers to close (comma-separated)
- Repository root with pending changes

## Steps
1. Inspect the repository state with `git status` and `git diff` to understand the modifications.
2. If `pyproject.toml` exists, evaluate the scope of changes and decide on a semantic version bump (major, minor, or patch). Update the version field accordingly.
3. Summarise the changes, highlighting affected components and rationale for the version decision.
4. Compose a concise commit message following conventional commits (include the version bump when applicable).
5. Append `Closes #<issue>` syntax using provided issue numbers.
6. Stage all modifications with `git add .`.
7. Commit using the generated message.
8. Provide a short report covering the new version (if changed), closed issues, and the nature of the updates.

## Output
- Local commit with an accurate message and optional version bump.
- Summary of committed work and issue closures.
