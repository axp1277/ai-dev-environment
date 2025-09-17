# Utility Prompt: Bootstrap a Python Project (uv)

## Purpose
Initialize a Python project that aligns with the centralised ai-docs structure while remaining tooling agnostic.

## Steps
1. Run `uv init` (or your preferred bootstrap) so `pyproject.toml` and `.venv/` exist.
2. Create the ai-docs scaffold:
   - `ai-docs/0-brainstorming`
   - `ai-docs/1-prompts/core`
   - `ai-docs/1-prompts/roles`
   - `ai-docs/1-prompts/utilities`
   - `ai-docs/2-workflows`
   - `ai-docs/3-specs`
   - `ai-docs/4-prds`
   - `ai-docs/5-meeting-notes`
   - `ai-docs/6-resources`
3. Add supporting project directories as needed (for example `docs/wiki`, `src/`, `tests/`, `examples/`).
4. Seed helper files such as `README.md`, `src/main.py`, and `src/__init__.py` to make the package importable.
5. Document assistant usage or development conventions inside `ai-docs/6-resources` or the main README.

## Sample Commands
```bash
uv init
uv sync
mkdir -p ai-docs/0-brainstorming \
         ai-docs/1-prompts/core ai-docs/1-prompts/roles ai-docs/1-prompts/utilities \
         ai-docs/2-workflows ai-docs/3-specs ai-docs/4-prds ai-docs/5-meeting-notes ai-docs/6-resources
mkdir -p docs/wiki src tests examples
cat > src/main.py <<'PY'
#!/usr/bin/env python3
"""Main entry point for the application."""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
PY
```

## Outcome
A Python project scaffold that matches the refactored ai-docs directory layout and is ready for AI-assisted workflows.
