You are tasked with setting up a Python project environment using uv.

Follow these steps in order:

1. **Initialize the project with uv** if pyproject.toml does not exist:
   - Check if `pyproject.toml` exists in the project root
   - If it does not exist, run: `uv init`

2. **Run uv sync** to synchronize the project dependencies:
   - Execute: `uv sync`

3. **Add required packages** using uv:
   - Execute: `uv add loguru pydantic python-dotenv`

4. **Create .env.example file** if it does not exist:
   - Check if `.env.example` exists in the project root
   - If it does not exist, create an empty `.env.example` file
   - DO NOT overwrite if it already exists

5. **Create .env file** if it does not exist:
   - Check if `.env` exists in the project root
   - If it does not exist, create an empty `.env` file
   - DO NOT overwrite if it already exists
   - Inform the user they need to add their actual configuration

6. **Create .gitignore file** if it does not exist:
   - Check if `.gitignore` exists in the project root
   - If it does not exist, create it with common Python ignore patterns
   - DO NOT overwrite if it already exists

After completing all steps, provide a summary of what was created/updated.
