# Refactor Planning (Dave Farley's Methodology)

Create a new plan in ai-docs/2-refactors/<refactor_name>.md to refactor code using Dave Farley's Test-Driven Refactoring methodology. Use the exact specified markdown `Plan Format` below.

## Dave Farley's Refactoring Principles

Refactoring MUST follow these non-negotiable principles:

### 1. Always Start from Green Tests
**Rule**: ALL tests must pass before any refactoring begins.
- If tests are failing, fix them first
- Refactoring changes internal structure, not external behavior
- Tests prove behavior is preserved during refactoring

### 2. Small Steps, One at a Time
**Rule**: Make ONE tiny change, run tests, commit.
- Extract a single method
- Rename one variable
- Move one function
- Don't batch multiple refactorings

### 3. Tests Must Stay Green
**Rule**: If tests fail after a refactoring, UNDO it immediately.
- Failed tests mean behavior changed (not refactoring, that's a bug)
- Git makes undoing easy: `git checkout -- <file>`
- Never proceed with red tests

### 4. Commit After Each Successful Refactoring
**Rule**: Use Git tactically for safety.
- Each commit is a rollback point
- Small commits = easy to revert if needed
- Message format: "refactor: <what changed>"

### 5. Listen to Test Pain
**Rule**: Hard-to-test code signals design problems.
- Complex test setup → Poor separation of concerns
- Brittle tests → Testing implementation details
- Slow tests → External dependencies not mocked
- Fix the design, don't work around it

## Instructions

- IMPORTANT: You're writing a **refactoring plan** to improve code internal structure WITHOUT changing external behavior.
- IMPORTANT: The `Code` describes what needs refactoring, but we're creating the PLAN, not refactoring yet.
- Refactoring MUST be done with passing tests - this is non-negotiable.
- Create the plan in `ai-docs/2-refactors/<refactor_name>.md` file.
- Use the `Plan Format` below to create the plan.
- Research the codebase to understand current structure and test coverage.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value.
- Use your reasoning model: THINK HARD about design improvements needed.
- Follow Dave Farley's methodology: small steps, always green tests, frequent commits.
- Start your research by reading the `README.md` file.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview
- Files mentioned in the refactoring request
- Related test files
- Any files importing the code to be refactored

## Plan Format

```md
# Refactor: <component/module name> - <design improvement>

## Refactoring Description

**Current State**: <describe what's wrong with the current design>

**Target State**: <describe what the design should look like after refactoring>

**Why This Matters**: <explain the value this refactoring provides>

## Design Problems Being Fixed

Identify specific design issues (check all that apply):

- [ ] **Duplication (DRY violation)**: <describe duplicated code>
- [ ] **Single Responsibility violations**: <components doing X AND Y>
- [ ] **Tight Coupling**: <dependencies that should be broken>
- [ ] **Poor Naming**: <unclear or misleading names>
- [ ] **Mixed Concerns**: <business logic mixed with infrastructure>
- [ ] **Complex Test Setup**: <test pain indicating design issues>
- [ ] **Long Functions/Classes**: <components that are too large>
- [ ] **Feature Envy**: <code that uses more of another class than its own>

## Test Coverage Analysis

### Current Test State
**Before refactoring, establish baseline**:

```bash
# Count tests
uv run pytest tests/ --collect-only | grep "test session starts"

# Check all tests pass
uv run pytest tests/ -v

# Measure coverage
uv run pytest --cov=<module> tests/ --cov-report=term-missing
```

**Baseline Results**:
- Total tests: <number>
- All passing: <yes/no - MUST be yes>
- Coverage: <percentage>
- Uncovered lines: <specific line numbers/functions>

### Test Quality Assessment

**Are tests focused on behavior or implementation?**
- [ ] Tests use public APIs (good - enables refactoring)
- [ ] Tests verify behavior, not internal state (good)
- [ ] Tests check implementation details (bad - will break during refactoring)

**Test pain points**:
- <Complex setup indicating design issues>
- <Brittle tests that break easily>
- <Slow tests indicating external dependencies>

### Tests to Add Before Refactoring

If test coverage is insufficient, add tests FIRST:

☐ **Missing Test 1**: <behavior not currently tested>
☐ **Missing Test 2**: <edge case not covered>
☐ **Missing Test 3**: <error condition not tested>

**Why add tests first**: These tests will pass with current code, proving they capture current behavior before we change it.

## Relevant Files

Use these files to perform the refactoring:

- **`path/to/file.py`** (<X> lines) - <why it needs refactoring>
  - Current issues: <specific design problems>
  - Will be refactored to: <target structure>
  - Tests: `tests/path/to/test_file.py` (<Y>% coverage)

- **`path/to/another_file.py`** (<X> lines) - <relationship to main refactoring>
  - Dependencies: <what imports this>
  - Will change: <how it will be affected>

### New Files (if needed)

- **`path/to/new_file.py`** - <purpose after extraction>
  - Created by: Extracting <responsibility> from <current file>
  - Will contain: <specific components>

## Refactoring Techniques to Apply

<Specify which Martin Fowler refactoring patterns to use>:

### Extract Method
**Where**: <function name, lines X-Y>
**Why**: Function is too long / does multiple things
**Result**: <new method name with single responsibility>

### Extract Class
**Where**: <current class name>
**Why**: Class has multiple responsibilities
**Result**: <new class name> handling <specific responsibility>

### Rename Method/Variable/Class
**From**: <current confusing name>
**To**: <clearer name expressing intent>
**Why**: <current name is unclear/misleading>

### Introduce Parameter Object
**Where**: <function with many parameters>
**Why**: Related parameters should be grouped
**Result**: <parameter object class>

### Replace Conditional with Polymorphism
**Where**: <switch/if-else chain>
**Why**: Violates Open-Closed principle
**Result**: <interface/base class with implementations>

### Move Method/Field
**From**: <class A>
**To**: <class B>
**Why**: Feature envy / better cohesion in B

## Step by Step Refactoring Plan

CRITICAL: Follow Dave Farley's small-step methodology. After EACH step:
1. Make the small change
2. Run tests: `uv run pytest tests/ -v`
3. Verify ALL tests are GREEN
4. Commit: `git commit -am "refactor: <what changed>"`

If tests fail, UNDO the change immediately.

### Phase 1: Establish Safety Net

☐ **Step 1.0: Verify Test Baseline**
* ☐ 1.1: Run full test suite - ALL must be GREEN
  - `uv run pytest tests/ -v`
  - Record count: <number> tests passing
* ☐ 1.2: Run coverage and save baseline
  - `uv run pytest --cov=<module> tests/ > baseline_coverage.txt`
  - Record coverage: <percentage>
* ☐ 1.3: Create feature branch
  - `git checkout -b refactor/<refactor-name>`
* ☐ 1.4: Commit baseline
  - `git commit --allow-empty -m "refactor: baseline for <refactor-name>"`

### Phase 2: Add Missing Tests (if needed)

☐ **Step 2.0: Improve Test Coverage**
* ☐ 2.1: Write test for <uncovered behavior 1>
  - Test should PASS with current code
  - Captures current behavior before refactoring
* ☐ 2.2: Write test for <uncovered behavior 2>
* ☐ 2.3: Run tests to verify new tests pass
* ☐ 2.4: Commit new tests
  - `git commit -am "test: add coverage before refactoring"`

### Phase 3: Small Refactoring Steps

**Each step is ONE atomic refactoring. Tests must stay GREEN.**

☐ **Step 3.1: <First small refactoring>**
Example: Extract method `_validate_email()` from `register_user()`
* Make the change (extract method)
* Run tests: `uv run pytest tests/ -v` - MUST be GREEN
* Commit: `git commit -am "refactor: extract email validation to separate method"`

☐ **Step 3.2: <Second small refactoring>**
Example: Rename `data` to `user_registration_data` for clarity
* Make the change (rename variable)
* Run tests: `uv run pytest tests/ -v` - MUST be GREEN
* Commit: `git commit -am "refactor: clarify user_registration_data naming"`

☐ **Step 3.3: <Third small refactoring>**
Example: Extract class `EmailValidator` from extracted method
* Make the change (extract class)
* Run tests: `uv run pytest tests/ -v` - MUST be GREEN
* Commit: `git commit -am "refactor: extract EmailValidator class (SRP)"`

☐ **Step 3.4: <Fourth small refactoring>**
Example: Move `EmailValidator` to `validators.py` module
* Make the change (move class to new file)
* Update imports
* Run tests: `uv run pytest tests/ -v` - MUST be GREEN
* Commit: `git commit -am "refactor: move EmailValidator to validators module"`

<Continue with each small refactoring step>

**Template for each step**:
```
☐ **Step X.Y: <Specific refactoring>**
* Make change: <exactly what to change>
* Run tests: `uv run pytest tests/ -v` - MUST be GREEN
* Commit: `git commit -am "refactor: <description>"`
```

### Phase 4: Validate Final State

☐ **Step 4.0: Final Validation**
* ☐ 4.1: Run full test suite - ALL tests MUST pass
  - `uv run pytest tests/ -v`
* ☐ 4.2: Verify coverage maintained or improved
  - `uv run pytest --cov=<module> tests/ --cov-report=term-missing`
  - Compare to baseline
* ☐ 4.3: Run linting - code quality should improve
  - `uv run ruff check .`
  - `uv run ruff format --check .`
* ☐ 4.4: Review git log to see progression
  - `git log --oneline`
  - Should show many small commits
* ☐ 4.5: Merge refactoring branch
  - `git checkout main && git merge refactor/<refactor-name>`

## Design Principles Applied

### Before → After Transformation

**Single Responsibility Principle**:
- **Before**: <Component> does X, Y, and Z
- **After**: <Component> does only X, <NewComponent1> does Y, <NewComponent2> does Z

**DRY (Don't Repeat Yourself)**:
- **Before**: Same code in <locations>
- **After**: Extracted to <shared utility/method>

**Separation of Concerns**:
- **Before**: Business logic mixed with <infrastructure concern>
- **After**: Business logic in <domain module>, infrastructure in <infrastructure module>

**Open-Closed Principle** (if applicable):
- **Before**: Switch statement / if-else chain requiring modification
- **After**: Polymorphic design allowing extension without modification

## Risk Assessment

### What Could Go Wrong

**Risk 1: Breaking changes to public API**
- **Mitigation**: Tests verify API behavior stays same
- **Detection**: Integration tests would fail
- **Rollback**: Each commit is revertable

**Risk 2: Performance regression**
- **Mitigation**: <benchmark before/after if applicable>
- **Detection**: Performance tests / profiling
- **Rollback**: Revert specific commit causing slowdown

**Risk 3: Introducing subtle bugs**
- **Mitigation**: Comprehensive test coverage
- **Detection**: Tests fail after refactoring
- **Rollback**: Undo the change that broke tests

### Rollback Strategy

Dave Farley's small-step approach makes rollback trivial:

1. **Each commit is a safe state** (all tests green)
2. **Undo last refactoring**: `git reset --hard HEAD~1`
3. **Undo specific file**: `git checkout HEAD~1 -- <file>`
4. **Abandon entire refactoring**: `git checkout main && git branch -D refactor/<name>`

No harm done because tests caught the problem before it went further.

## Validation Commands

Execute every command to validate refactoring maintains behavior with zero regressions.

```bash
# 1. All tests must pass (100% green)
uv run pytest tests/ -v

# 2. Run with fail-fast to catch issues immediately
uv run pytest tests/ -x

# 3. Coverage maintained or improved
uv run pytest --cov=<module> tests/ --cov-report=term-missing

# 4. Compare to baseline
diff baseline_coverage.txt <(uv run pytest --cov=<module> tests/ --cov-report=term)

# 5. No behavior changes detected
# (test count same or higher, all passing)

# 6. Code quality improved
uv run ruff check .
uv run ruff format --check .

# 7. Imports still work
uv run python -c "from <module> import <refactored_component>; print('OK')"

# 8. Performance maintained (if applicable)
<benchmark commands>

# 9. Integration tests pass (if applicable)
<integration test commands>
```

## Success Criteria

Refactoring is successful when ALL criteria are met:

- [ ] **All tests pass** (100% green)
- [ ] **Test coverage maintained** or improved (compare to baseline)
- [ ] **Code is more readable** and maintainable
- [ ] **Design principles applied** (SRP, DRY, Separation of Concerns)
- [ ] **No behavioral changes** (external API unchanged)
- [ ] **Performance maintained** or improved
- [ ] **Documentation updated** (if API changed)
- [ ] **All commits have green tests** (verified by reviewing git log)
- [ ] **Code quality metrics improved** (linting, complexity)

## Anti-Patterns to Avoid (Dave Farley)

**DON'T make big changes**
- ❌ Refactor entire module at once
- ✅ One small change at a time

**DON'T refactor when tests are red**
- ❌ "I'll fix the tests after refactoring"
- ✅ Stop, undo, figure out why tests failed

**DON'T skip running tests**
- ❌ Make several changes, then run tests
- ✅ Run tests after EVERY change

**DON'T change behavior while refactoring**
- ❌ "While I'm here, let me add this feature"
- ✅ Refactoring = preserve behavior, improve structure

**DON'T ignore test coverage drops**
- ❌ "Coverage dropped but refactoring is done"
- ✅ Add tests to restore/exceed coverage

## Notes

### Dave Farley's Refactoring Workflow Summary

1. **Verify all tests green** (baseline)
2. **Make ONE small change**
3. **Run tests** (must stay green)
4. **Commit** (safe rollback point)
5. **Repeat** steps 2-4 for next change

### Key Insights from Dave Farley

**"Refactoring is not optional"**
- Technical debt accumulates if skipped
- Makes future changes harder and slower
- Regular refactoring maintains velocity

**"Small steps, fast feedback"**
- Many tiny changes > few big changes
- Faster to find problems when they occur
- Each commit is a safety checkpoint

**"Listen to test pain"**
- Hard-to-test code = poorly designed code
- Fix the design, tests become easy
- Test-first thinking prevents design problems

**"Always from green tests"**
- Non-negotiable safety requirement
- Red tests mean behavior changed (bug!)
- Green tests prove behavior preserved

### Before/After Comparison

**Before Refactoring**:
<Describe current design with problems>

**After Refactoring**:
<Describe target design with improvements>

### Future Improvements

<Optionally note further refactoring opportunities for later>
- Potential next refactoring: <description>
- Areas still needing attention: <list>
- Tech debt to address later: <items>

```

## Code to Refactor
$ARGUMENTS

## Report

After creating the refactoring plan, provide:

- Summary of refactoring goals and design improvements
- Path to the plan in `ai-docs/2-refactors/<refactor_name>.md`
- Number of small refactoring steps planned
- Design principles that will be applied
- Risk assessment summary
- Baseline test coverage and target coverage
