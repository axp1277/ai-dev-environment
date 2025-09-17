# Playbook: Bootstrap a Python Project (uv)

## Purpose
Initialize a Python project that follows the ai-docs scaffolding pattern while remaining tool-agnostic.

## Steps
1. **Create `pyproject.toml`** (if absent) using `uv init` and sync dependencies with `uv sync` to generate `.venv`.
2. **Establish directories**:
   - `ai-docs/0-brainstorming`
   - `ai-docs/1-prds`
   - `ai-docs/2-specs`
   - `ai-docs/3-meeting-notes`
   - `ai-docs/4-prompts`
   - `ai-docs/5-workflows`
   - `ai-docs/6-tools/playbooks`
   - `ai-docs/7-resources`
   - `agents/`
   - `docs/wiki`
   - `src/`
   - `tests/`
   - `examples/`
3. **Add helper files** as needed:
   - `README.md` describing the project.
   - `src/main.py` with a starter entry point.
   - `src/__init__.py` to make the package importable.
4. **Document assistant usage** in a neutral `AI_ASSISTANT.md` file summarising prompts, workflows, and expectations (optional but recommended).
5. **Record conventions** (type hints, logging, testing) either in `ai-docs/7-resources` or the project README.

## Sample Commands
```bash
uv init
uv sync
mkdir -p ai-docs/{0-brainstorming,1-prds,2-specs,3-meeting-notes,4-prompts,5-workflows,6-tools/playbooks,7-resources}
mkdir -p agents docs/wiki src tests examples
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
A Python project ready for any AI assistant, complete with the ai-docs scaffold and space for prompts, workflows, and agent profiles.
