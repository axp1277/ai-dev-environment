# Command: gacp
# Description: Git Add, Commit, and Push with intelligent version bumping - AI reviews changes and handles git operations
# Usage: gacp

# Instruct the AI to review changes and perform git operations
Review the changes you've just made to the codebase:

1. **Check for version file**: Look for `pyproject.toml` in the project root directory.

2. **Analyze changes**: 
   - Run `git status` to see what files have been modified
   - Run `git diff` to analyze the specific changes across all modified files

3. **Determine version bump** (if `pyproject.toml` exists):
   Based on the changes made, determine the appropriate semantic version bump:
   
   **MAJOR version** (X.y.z → (X+1).0.0) - Breaking changes:
   - Removed public APIs, functions, or classes
   - Changed function signatures that would break existing code
   - Removed or renamed configuration options
   - Changed database schema in incompatible ways
   - Modified public interfaces in non-backward-compatible ways
   - Removed dependencies that user code might rely on

   **MINOR version** (x.Y.z → x.(Y+1).0) - New features (backward compatible):
   - Added new public functions, classes, or modules
   - Added new configuration options (with sensible defaults)
   - Added new dependencies
   - Enhanced existing functionality without breaking changes
   - Added new API endpoints
   - Introduced new optional parameters to existing functions

   **PATCH version** (x.y.Z → x.y.(Z+1)) - Bug fixes and small improvements:
   - Fixed bugs without changing public APIs
   - Updated documentation
   - Refactored internal code without affecting public interface
   - Updated dependencies to patch versions
   - Performance improvements that don't change behavior
   - Code style/formatting changes
   - Updated tests without changing functionality
   - Fixed typos in code comments or docstrings

4. **Update version** (if version bump is needed):
   - Parse the current version from `pyproject.toml`
   - Apply the determined version bump
   - Update the version field in `pyproject.toml`
   - Include the version update in the staged changes

5. **Generate commit message**:
   Create a descriptive and concise commit message that captures:
   - The version bump (if applicable): e.g., "bump: v1.2.3 → v1.3.0"
   - The main updates or additions to the codebase
   - What sections or files were modified  
   - What new features, fixes, or tasks were added or improved
   
   Format: Use conventional commit format with summary line (50-72 chars) and optional bullet points
   
   Examples:
   - `feat: add user authentication system (v1.2.0 → v1.3.0)`
   - `fix: resolve database connection timeout issue (v1.2.3 → v1.2.4)`
   - `BREAKING: remove deprecated API endpoints (v1.2.3 → v2.0.0)`

6. **Execute git operations**:
   - `git add .`
   - `git commit -m "YOUR_GENERATED_COMMIT_MESSAGE"`
   - `git push`

7. **Provide summary**:
   After completing these actions, provide a brief summary including:
   - What changes were committed
   - Version bump applied (if any): old version → new version
   - Reasoning for the version bump decision

## Version Bump Decision Framework

When analyzing changes, consider this hierarchy:

1. **Scan for breaking changes first** → MAJOR
2. **Look for new features/additions** → MINOR  
3. **Default to patches for everything else** → PATCH

**Special cases**:
- If no functional code changes (only docs, tests, comments): Consider PATCH or no bump
- If multiple types of changes: Use the highest level (MAJOR > MINOR > PATCH)
- If unsure between MINOR and PATCH: Choose PATCH (safer)
- Pre-release versions (0.x.y): Different rules may apply (breaking changes can be MINOR)

**No version bump scenarios**:
- Only changes to README, documentation files
- Only changes to .gitignore, CI/CD configuration  
- Only formatting or linting changes with no functional impact