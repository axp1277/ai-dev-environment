# Chore Planning (Test-Driven Development)

Create a new plan in ai-docs/2-chores/*.md to resolve the `Chore` using Test-Driven Development following Dave Farley's refactoring methodology. Use the exact specified markdown `Plan Format` below.

## Refactoring and Test Coverage Principles (Dave Farley)

Chores (refactoring, cleanup, maintenance) MUST maintain test coverage and code quality:

1. **BASELINE** - Establish test baseline BEFORE making changes
   - Run all tests and record results (all must be GREEN)
   - Run coverage report and record percentage
   - This is your safety net

2. **SMALL STEPS** - Make changes in tiny, reversible increments
   - ONE change at a time (extract method, rename variable, etc.)
   - Run tests after EACH change
   - Tests MUST stay green - if red, undo the change

3. **COMMIT FREQUENTLY** - Use Git tactically
   - Commit after each small refactoring that keeps tests green
   - Each commit is a safe rollback point
   - Message: "refactor: <what changed>"

4. **VALIDATE COVERAGE** - Ensure tests still cover behavior
   - Coverage should be maintained or improved
   - If coverage drops, add tests before continuing
   - Tests prevent regressions during refactoring

**Critical Rule**: NEVER refactor when tests are red. Only refactor from green tests.

## Test Pain as Design Signal (Dave Farley)

If tests are hard to write or maintain, the design needs improvement:
- **Complex test setup** → Poor separation of concerns (split responsibilities)
- **Brittle tests** → Testing implementation details instead of behavior
- **Slow tests** → External dependencies not mocked/stubbed
- **Duplicate test code** → Missing test utilities or fixtures

Listen to test pain and fix the design, don't work around it.

## Instructions

- IMPORTANT: You're writing a **TDD-based plan** to resolve a chore that will add value to the application.
- IMPORTANT: The `Chore` describes the chore, but we're creating the PLAN showing how to do it safely with tests, not doing it yet.
- You're writing a plan to resolve a chore, it should be simple but we need to be thorough and precise so we don't miss anything or waste time with any second round of changes.
- Create the plan in the `ai-docs/2-chores/*.md` file. Name it appropriately based on the `Chore`.
- Use the plan format below to create the plan.
- Research the codebase and put together a plan to accomplish the chore.
- **IMPORTANT**: Plan must include test baseline, small refactoring steps, and coverage validation.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to accomplish the chore.
- Use your reasoning model: THINK HARD about the plan and the steps to accomplish the chore.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.
- `adws/*.py` contain astral uv single file python scripts. So if you want to run them use `uv run <script_name>`.
- When you finish creating the plan for the chore, follow the `Report` section to properly report the results of your work.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/**` - Contains the codebase client/server.
- `scripts/**` - Contains the scripts to start and stop the server + client.
- `adws/**` - Contains the AI Developer Workflow (ADW) scripts.

Ignore all other files in the codebase.

## Plan Format

```md
# Chore: <chore name>

## Chore Description
<describe the chore in detail>

**Type of Chore**: <refactoring | cleanup | dependency update | documentation | etc.>

**Why this matters**: <value this chore provides>

## Test Coverage Baseline

Before starting the chore, establish baseline:

**Current State**:
- Total tests: <run pytest and count>
- Passing tests: <should be 100%>
- Test coverage: <run pytest --cov to get percentage>
- Coverage gaps: <areas with low/no coverage>

**Baseline Commands**:
```bash
# Record current test state
uv run pytest tests/ -v > baseline_tests.txt

# Record current coverage
uv run pytest --cov=<module> tests/ --cov-report=term > baseline_coverage.txt
```

**Requirement**: ALL tests must be GREEN before refactoring begins. If any tests fail, fix them first.

## Relevant Files
Use these files to resolve the chore:

<find and list the files that are relevant to the chore describe why they are relevant in bullet points. If there are new files that need to be created to accomplish the chore, list them in an h3 'New Files' section.>

## Design Improvements (If Refactoring)

If this chore involves refactoring, identify design improvements to make:

**Single Responsibility Violations**:
- <components doing multiple things to split>

**Duplication (DRY)**:
- <duplicated code to extract to shared utilities>

**Separation of Concerns**:
- <mixed concerns to separate (business logic, infrastructure, etc.)>

**Naming Clarity**:
- <unclear names to improve>

**Test Pain Points**:
- <complex test setup indicating design issues>
- <brittle tests testing implementation details>

## Step by Step Tasks (Small Steps Refactoring)
IMPORTANT: Execute every step in order, top to bottom. Follow Dave Farley's small-step methodology.

### Phase 1: Establish Safety Net
☐ **Task 1.0: Verify Test Baseline**
* ☐ 1.1: Run full test suite: `uv run pytest tests/ -v`
  - ALL tests must be GREEN before proceeding
  - If any fail, fix them before refactoring
* ☐ 1.2: Run coverage report: `uv run pytest --cov=<module> tests/`
  - Record current coverage percentage
  - Identify areas with low coverage
* ☐ 1.3: Save baseline to files
  - `uv run pytest tests/ -v > baseline_tests.txt`
  - `uv run pytest --cov=<module> tests/ > baseline_coverage.txt`
* ☐ 1.4: Create feature branch for chore
  - `git checkout -b chore/<chore-name>`

### Phase 2: Add Missing Tests (If Needed)
☐ **Task 2.0: Improve Test Coverage Before Refactoring**
* ☐ 2.1: Identify untested behaviors in code to be refactored
* ☐ 2.2: Write tests for uncovered behavior
  - These tests should pass with current implementation
  - Ensures current behavior is captured before changes
* ☐ 2.3: Run tests to verify new tests pass
* ☐ 2.4: Commit new tests
  - Message: "test: add coverage before refactoring <component>"

### Phase 3: Small Refactoring Steps

**CRITICAL RULE**: After EACH step:
1. Make the small change
2. Run tests: `uv run pytest tests/ -v`
3. Verify ALL tests are GREEN
4. Commit: `git commit -am "refactor: <what changed>"`

<list each refactoring step as a small, atomic change>

☐ **Refactor Step 1**: <Extract method/class/function>
* ☐ 1.1: <Specific small change to make>
* ☐ 1.2: Run tests - MUST be GREEN
* ☐ 1.3: Commit with message: "refactor: <description>"

☐ **Refactor Step 2**: <Eliminate duplication>
* ☐ 2.1: <Specific small change to make>
* ☐ 2.2: Run tests - MUST be GREEN
* ☐ 2.3: Commit with message: "refactor: <description>"

☐ **Refactor Step 3**: <Improve naming>
* ☐ 3.1: <Specific small change to make>
* ☐ 3.2: Run tests - MUST be GREEN
* ☐ 3.3: Commit with message: "refactor: <description>"

☐ **Refactor Step 4**: <Split responsibilities>
* ☐ 4.1: <Specific small change to make>
* ☐ 4.2: Run tests - MUST be GREEN
* ☐ 4.3: Commit with message: "refactor: <description>"

<continue for each refactoring step>

### Phase 4: Validate Final State
☐ **Task N.0: Validate Chore Complete**
* ☐ N.1: Run full test suite - ALL tests MUST pass
  - `uv run pytest tests/ -v`
* ☐ N.2: Run coverage report - Coverage maintained or improved
  - `uv run pytest --cov=<module> tests/ --cov-report=term-missing`
  - Compare to baseline coverage
* ☐ N.3: Compare baseline to final state
  - `diff baseline_tests.txt current_tests.txt`
  - Should show same number of passing tests (or more)
* ☐ N.4: Run validation commands (see below)
* ☐ N.5: Merge chore branch
  - Review git log to see progression of small commits

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

```bash
# Run all tests - must all pass
uv run pytest tests/ -v

# Run with fail-fast to catch issues immediately
uv run pytest tests/ -x

# Run coverage - should match or exceed baseline
uv run pytest --cov=<module> tests/ --cov-report=term-missing

# Compare test results to baseline
diff baseline_tests.txt <(uv run pytest tests/ -v)
# Should show no new failures

# Run linting to ensure code quality improved
uv run ruff check .
uv run ruff format --check .

# Verify imports still work after refactoring
uv run python -c "from <module> import <refactored_component>; print('OK')"

# Run integration tests if applicable
<any integration or end-to-end test commands>
```

## Design Principles Applied (Dave Farley)

### Single Responsibility Principle
**Applied when**:
- Component was doing X AND Y (split into two)
- Each component now has one reason to change

### DRY (Don't Repeat Yourself)
**Applied when**:
- Duplicated code extracted to shared utility
- Copy-paste eliminated through abstraction

### Separation of Concerns
**Applied when**:
- Business logic separated from infrastructure (DB, API calls)
- Pure functions separated from side effects

### Clear Intent
**Applied when**:
- Renamed variables/functions to express WHAT not HOW
- Names now self-document the code

## Anti-Patterns to Avoid (Dave Farley)

**DON'T make big refactoring changes**
- ❌ Refactor entire file/module at once
- ✅ Make tiny changes, one at a time

**DON'T refactor when tests are red**
- ❌ "I'll fix the tests after the refactoring"
- ✅ Stop, undo the change, figure out why tests failed

**DON'T skip running tests**
- ❌ Make several changes before running tests
- ✅ Run tests after EVERY small change

**DON'T ignore test coverage drops**
- ❌ "Coverage went from 90% to 75%, but the refactoring is done"
- ✅ Add tests to restore coverage before finishing

## Notes

### Small Steps Refactoring Workflow
1. Establish test baseline (all green)
2. Make ONE small change
3. Run tests (must stay green)
4. Commit
5. Repeat steps 2-4 for each refactoring

### Dave Farley's Refactoring Principles
- **Always from green tests**: Non-negotiable safety requirement
- **Small steps**: One change at a time, not a dozen
- **Frequent commits**: Each successful refactoring gets committed
- **Listen to tests**: Test pain signals design problems
- **Design improvement**: Not just cleanup, but strategic enhancement

### Rollback Strategy
- Each commit is a safe rollback point
- If a refactoring causes test failures, undo it: `git checkout -- <file>`
- Feature branch can be discarded if chore goes wrong
- No harm done because tests caught the problem

<optionally list any additional notes or context that are relevant to the chore that will be helpful to the developer>
```

## Chore
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- Include a path to the plan you created in the `2-chores/*.md` file.
- Note the number of small refactoring steps planned.
- Note the test coverage baseline and target.
- Highlight the design principles that will be applied.
