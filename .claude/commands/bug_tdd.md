# Bug Planning (Test-Driven Development)

Create a new plan in ai-docs/2-bugs/<bug_name>.md to resolve the `Bug` using Test-Driven Development following Dave Farley's methodology. Use the exact specified markdown `Plan Format` below.

## Test-First Bug Fix Workflow (Dave Farley)

Bug fixes are the PERFECT use case for TDD. Every bug fix MUST follow this workflow:

1. **RED Phase** - Write a failing test that reproduces the bug
   - Test should fail in the same way the bug manifests
   - This proves you understand the bug
   - Serves as permanent regression prevention
   - Run test to verify it actually fails

2. **GREEN Phase** - Fix the bug with minimal changes
   - Change ONLY what's necessary to make the test pass
   - Don't refactor while fixing (tests are red!)
   - Keep the fix surgical and focused

3. **REFACTOR Phase** - Improve the code that contained the bug
   - Now that tests are green, clean up the area
   - Look for patterns that allowed the bug
   - Apply design principles to prevent similar bugs

4. **VERIFY** - Validate no regressions
   - The new test should pass
   - ALL existing tests should still pass
   - Confirms fix doesn't break anything else

**Critical Rule**: If you can't write a failing test that reproduces the bug, you don't understand the bug well enough to fix it.

## Instructions

- IMPORTANT: You're writing a **TDD-based plan** to resolve a bug that will add value to the application.
- IMPORTANT: The `Bug` describes the bug, but we're creating the PLAN showing how to TDD-fix it, not fixing yet.
- You're writing a plan to resolve a bug, it should be thorough and precise so we fix the root cause and prevent regressions.
- Create the plan in the `ai-docs/2-bugs/<bug_name>.md` file. Name it appropriately based on the `Bug`.
- If the `ai-docs/2-bugs/` directory does not exist, create it before writing the file.
- Use the plan format below to create the plan.
- Research the codebase to understand the bug, reproduce it, and put together a plan to fix it.
- **IMPORTANT**: First step MUST be writing a failing test. Fix comes second, never first.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to fix the bug.
- Use your reasoning model: THINK HARD about the bug, its root cause, and the steps to fix it properly.
- IMPORTANT: Be surgical with your bug fix, solve the bug at hand and don't fall off track.
- IMPORTANT: We want the minimal number of changes that will fix and address the bug.
- Don't use decorators. Keep it simple.
- If you need a new library, use `uv add` and be sure to report it in the `Notes` section of the `Plan Format`.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/**` - Contains the codebase client/server.
- `scripts/**` - Contains the scripts to start and stop the server + client.
- `adws/**` - Contains the AI Developer Workflow (ADW) scripts.

Ignore all other files in the codebase.

## Plan Format

```md
# Bug: <bug name>

## Bug Description
<describe the bug in detail, including symptoms and expected vs actual behavior>

## Problem Statement
<clearly define the specific problem that needs to be solved>

## Solution Statement
<describe the proposed solution approach to fix the bug>

## Steps to Reproduce
<list exact steps to reproduce the bug>

1. <step 1>
2. <step 2>
3. <observe buggy behavior>

Expected: <what should happen>
Actual: <what actually happens>

## Root Cause Analysis
<analyze and explain the root cause of the bug>

**Why it happens**: <technical explanation>
**Where it happens**: <specific file:line or component>
**Pattern that allowed it**: <design issue, missing validation, etc.>

## Relevant Files
Use these files to fix the bug:

<find and list the files that are relevant to the bug describe why they are relevant in bullet points. If there are new files that need to be created to fix the bug, list them in an h3 'New Files' section.>

## Step by Step Tasks (Test-First Bug Fix)
IMPORTANT: Execute every step in order, top to bottom. Follow the TDD workflow for bug fixes.

### Phase 1: Reproduce Bug with Test (RED)
☐ **Task 1.0: Write Failing Test**
* ☐ 1.1: Create test file: `tests/path/to/test_bug_<bug_name>.py`
* ☐ 1.2: Write test that reproduces the bug
  - Test should demonstrate the buggy behavior
  - Use the same inputs/conditions that trigger the bug
  - Assert the CORRECT behavior (test will fail because bug exists)
* ☐ 1.3: Run test to verify it FAILS
  - Command: `uv run pytest tests/path/to/test_bug_<bug_name>.py -v`
  - Confirm failure message matches bug symptoms
* ☐ 1.4: Document the failing test output
  - This proves we understand the bug

### Phase 2: Fix Bug (GREEN)
☐ **Task 2.0: Implement Minimal Fix**
* ☐ 2.1: Make minimal changes to fix the bug
  - Change ONLY what's necessary to pass the test
  - Don't refactor yet (tests are still red/transitioning)
  - Focus on making the test green
* ☐ 2.2: Run the failing test again
  - Command: `uv run pytest tests/path/to/test_bug_<bug_name>.py -v`
  - Verify test now PASSES
* ☐ 2.3: Run ALL tests to check for regressions
  - Command: `uv run pytest tests/ -v`
  - ALL tests must pass (no regressions introduced)
* ☐ 2.4: Commit the fix
  - Message: "fix: <bug description>"
  - Include the test and the fix in same commit

### Phase 3: Refactor (Prevent Future Bugs)
☐ **Task 3.0: Improve Code Quality**
* ☐ 3.1: Analyze the area that contained the bug
  - Look for code doing multiple things (Single Responsibility violation)
  - Look for missing validation or error handling
  - Look for similar patterns elsewhere in codebase
* ☐ 3.2: Apply design improvements
  - Extract methods if functions are too long
  - Add validation if missing
  - Clarify names if confusing
  - Run tests after EACH small refactoring
* ☐ 3.3: Add tests for related edge cases
  - If bug was null pointer, test other null scenarios
  - If bug was validation, test boundary conditions
  - Prevent similar bugs in the future
* ☐ 3.4: Commit refactoring
  - Message: "refactor: improve <component> to prevent similar bugs"

### Phase 4: Validate and Document
☐ **Task 4.0: Final Validation**
* ☐ 4.1: Run validation commands (see below)
* ☐ 4.2: Verify bug is fixed in actual usage
  - Manually test the original bug scenario
  - Confirm expected behavior now occurs
* ☐ 4.3: Update documentation if needed
  - Note any API changes
  - Document the fix for future reference

## Root Cause Prevention

After fixing the bug, ask these questions to prevent similar bugs:

**Design Questions**:
- Does this component have too many responsibilities?
- Is validation missing or incomplete?
- Are error conditions handled properly?
- Are dependencies too tightly coupled?

**Pattern Recognition**:
- Are there similar code patterns elsewhere that might have the same bug?
- Should we add linting rules to catch this pattern?
- Should we add validation in multiple places?

**Test Coverage**:
- What edge cases were missing tests?
- What assumptions were untested?
- Should we add more property-based tests?

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

```bash
# 1. Run the specific bug test (should now PASS)
uv run pytest tests/path/to/test_bug_<bug_name>.py -v

# 2. Run all tests to verify no regressions
uv run pytest tests/ -v

# 3. Run with fail-fast to catch issues immediately
uv run pytest tests/ -x

# 4. Verify test coverage (ensure bug area is covered)
uv run pytest tests/ --cov=<module_with_bug> --cov-report=term-missing

# 5. Run linting to ensure code quality
uv run ruff check .
uv run ruff format --check .

# 6. Manually reproduce original bug scenario
<specific commands to reproduce the bug>
# Should now show CORRECT behavior instead of buggy behavior

# 7. Integration tests (if applicable)
<any integration tests that exercise the bug scenario>
```

## Regression Prevention

**Test Documentation**:
- The failing test is now permanent regression protection
- Future changes that reintroduce the bug will immediately fail this test
- Test name should clearly indicate what bug it prevents

**Example Test Naming**:
```python
def test_bug_<bug_name>_<specific_scenario>():
    """
    Regression test for bug: <bug description>

    Previously, <what used to happen>
    Now, <correct behavior>
    """
```

## Anti-Patterns to Avoid (Dave Farley)

**DON'T fix the bug before writing the test**
- ❌ "I know what's wrong, let me just fix it"
- ✅ "Let me prove I understand the bug with a failing test"

**DON'T refactor while the test is red**
- ❌ Fix the bug and improve the design at the same time
- ✅ Fix first (GREEN), then refactor

**DON'T write tests that pass immediately**
- ❌ Test that passes even before the fix (not testing the bug)
- ✅ Test that fails reproducing the bug, then passes after the fix

**DON'T skip regression testing**
- ❌ Only run the new test, assume others still pass
- ✅ Run full test suite to verify no regressions

## Notes

### TDD Bug Fix Workflow Summary
1. Write failing test that reproduces bug (RED)
2. Verify test actually fails
3. Fix bug with minimal changes (GREEN)
4. Verify test now passes
5. Refactor to prevent similar bugs (REFACTOR)
6. Run all tests to check for regressions (VERIFY)

### Dave Farley's Key Insight
"A bug is a missing test. Once you write the test that exposes the bug, fixing it becomes straightforward."

**Benefits of Test-First Bug Fixing**:
- Proves you understand the bug before attempting to fix it
- Provides permanent regression protection
- Faster debugging (test clearly demonstrates the problem)
- Higher confidence in the fix (test proves it works)

<optionally list any additional notes or context that are relevant to the bug that will be helpful to the developer>
```

## Bug
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- Include a path to the plan you created in the `ai-docs/2-bugs/<bug_name>.md` file.
- Note that the plan enforces test-first bug fixing (failing test → fix → refactor).
- Highlight the regression prevention measures included.
