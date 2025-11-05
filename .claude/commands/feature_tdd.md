# Feature Planning (Test-Driven Development)

Create a new plan in ai-docs/2-features/<feature_name>.md to implement the `Feature` using Test-Driven Development following Dave Farley's methodology. Use the exact specified markdown `Plan Format` below.

## TDD Workflow Principles (Dave Farley)

This command enforces Test-Driven Development using the Red-Green-Refactor cycle:

1. **RED Phase** - Write a failing test that specifies desired behavior
   - Think from the caller's perspective (API design)
   - Focus on WHAT the code should do, NOT HOW it works internally
   - Run the test to verify it fails (proves it's testing something)

2. **GREEN Phase** - Write the simplest code to make the test pass
   - Do the minimum required to satisfy the test
   - Don't anticipate future requirements or generalize prematurely
   - Hard-code values if it makes the test pass

3. **REFACTOR Phase** - Improve the design while keeping tests green
   - Eliminate duplication (DRY principle)
   - Apply Single Responsibility (if code does X and Y, split it)
   - Improve names for clarity
   - Run tests after EACH small refactoring

4. **COMMIT** - Commit after each complete Red-Green-Refactor cycle

**Core Principle**: Tests drive design. TDD is about designing better software, not just testing it.

## Instructions

- IMPORTANT: You're writing a **TDD-based plan** to implement a net new feature that will add value to the application.
- IMPORTANT: The `Feature` describes what to build, but we're creating the PLAN showing HOW to TDD it, not implementing yet.
- Create the plan in the `ai-docs/2-features/<feature_name>.md` file. Name it appropriately based on the `Feature`.
- Use the `Plan Format` below to create the plan.
- Research the codebase to understand existing patterns, architecture, and conventions before planning the feature.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to implement the feature successfully.
- Use your reasoning model: THINK HARD about the feature requirements, design, and implementation approach.
- **Plan the feature as a series of Red-Green-Refactor cycles**, not just sequential implementation steps.
- Follow existing patterns and conventions in the codebase. Don't reinvent the wheel.
- Design for extensibility and maintainability.
- If you need a new library, use `uv add` and be sure to report it in the `Notes` section of the `Plan Format`.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/server/**` - Contains the codebase server.
- `app/client/**` - Contains the codebase client.
- `scripts/**` - Contains the scripts to start and stop the server + client.
- `adws/**` - Contains the AI Developer Workflow (ADW) scripts.

Ignore all other files in the codebase.

## Plan Format

```md
# Feature: <feature name>

## Feature Description
<describe the feature in detail, including its purpose and value to users>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<clearly define the specific problem or opportunity this feature addresses>

## Solution Statement
<describe the proposed solution approach and how it solves the problem>

## Relevant Files
Use these files to implement the feature:

<find and list the files that are relevant to the feature describe why they are relevant in bullet points. If there are new files that need to be created to implement the feature, list them in an h3 'New Files' section.>

## Implementation Plan
### Phase 1: Foundation
<describe the foundational work needed before implementing the main feature>

### Phase 2: Core Implementation
<describe the main implementation work for the feature>

### Phase 3: Integration
<describe how the feature will integrate with existing functionality>

## Step by Step Tasks (TDD Cycles)
IMPORTANT: Execute every step in order, top to bottom. Each task follows the Red-Green-Refactor cycle.

<list step by step tasks using TDD cycle format below. Order matters, start with the foundational shared changes required then move on to the specific implementation. Each cycle includes: write failing test, make it pass, refactor. Your last step should be running the `Validation Commands` to validate the feature works correctly with zero regressions.>

### Task Format (Red-Green-Refactor Cycles)
Use TDD cycle format with completion status indicators:

```
☐ Cycle 1.0: [Specific behavior/feature to implement]
* ☐ 1.0-RED: Write failing test for [specific behavior]
  - Test should specify WHAT the code should do (from caller's perspective)
  - Run test to verify it fails
* ☐ 1.0-GREEN: Implement minimal code to make test pass
  - Simplest thing that could possibly work
  - Don't anticipate future requirements
* ☐ 1.0-REFACTOR: Improve design while keeping tests green
  - Eliminate duplication
  - Apply Single Responsibility principle
  - Improve naming for clarity
  - Run tests after each small refactoring
* ☐ 1.0-COMMIT: Commit with message "feat: [description]"

☐ Cycle 2.0: [Next behavior/feature to implement]
* ☐ 2.0-RED: Write failing test for [specific behavior]
* ☐ 2.0-GREEN: Implement minimal code to make test pass
* ☐ 2.0-REFACTOR: Improve design while keeping tests green
* ☐ 2.0-COMMIT: Commit with message "feat: [description]"
```

Status Indicators:
- ☐ Not started
- 🚧 Partially completed
- ✅ Completed

Initially mark ALL tasks with ☐ (needs implementation). Update status as implementation progresses.

**IMPORTANT**: Each cycle must be SMALL. If you find yourself writing lots of implementation code in the GREEN phase, break it into smaller cycles with simpler tests.

## Testing Strategy (Test-First Requirements)

### Test-First Discipline
For EVERY piece of functionality:
1. **Write the test BEFORE implementation** (Red phase)
2. **Run the test to see it fail** (verify it's actually testing something)
3. **Focus on behavior**, not implementation details
4. **Keep tests small and focused** (one behavior per test)
5. **Tests should be easy to understand** (they document what the code does)

### Unit Tests (Red-Green-Refactor Cycles)
<For each cycle, specify:>
- **What failing test to write** (Red): <specific behavior being tested>
- **Expected behavior**: <what should happen when the test passes>
- **Minimal implementation approach** (Green): <simplest code to make it pass>
- **Design improvements to apply** (Refactor): <duplication to remove, responsibilities to split, names to clarify>

Example:
```
Cycle: User email validation
- RED: Test that invalid email raises InvalidEmailError
- GREEN: Simple regex check, raise error if doesn't match
- REFACTOR: Extract to EmailValidator class (Single Responsibility)
```

### Integration Tests
<High-level tests to validate units work together>
- Write these AFTER unit tests are green
- Test realistic scenarios in production-like environment
- Should be fewer than unit tests
- Focus on end-to-end workflows

### Edge Cases
<Each edge case gets its own Red-Green-Refactor cycle>
- Empty/null inputs
- Boundary conditions
- Error scenarios
- Concurrent access (if applicable)

### Anti-Patterns to Avoid (Dave Farley)

**DON'T write tests that are too big**
- ❌ One test requiring 100 lines of implementation
- ✅ Ten tests each requiring 10 lines of implementation

**DON'T skip the refactoring step**
- ❌ "It works, move on to next feature"
- ✅ "It works, now make it clean and maintainable"

**DON'T test implementation details**
- ❌ `assert obj._internal_state == expected` (testing internals)
- ✅ `assert obj.public_method() == expected` (testing behavior)

**DON'T write implementation before tests**
- ❌ Write code first, then add tests to verify it
- ✅ Write test first, then write code to make it pass

**DON'T stay red too long**
- ❌ Write test, write lots of code, finally run test
- ✅ Write test, write minimal code, run test immediately (repeat)

## Refactoring Checkpoints (Design Principles)

After each GREEN phase, apply these design principles during REFACTOR:

### Single Responsibility Principle
**Check**: Does any class/function do more than one thing?
- If code does X AND Y, split it into two components
- Each component should have one reason to change

### DRY (Don't Repeat Yourself)
**Check**: Is there duplication?
- Extract duplicated code to shared functions/utilities
- Eliminate copy-paste code through abstraction

### Clear Intent
**Check**: Are names expressive and clear?
- Rename variables/functions to express WHAT, not HOW
- Good names make code self-documenting

### Separation of Concerns
**Check**: Are different concerns mixed together?
- Business logic separate from infrastructure (database, API calls)
- Pure functions separate from side effects
- Domain models separate from data access

### Test Pain as Design Signal
**Listen to test pain** - if tests are hard to write, the design needs improvement:
- Complex test setup → Poor separation of concerns
- Brittle tests → Testing implementation details instead of behavior
- Slow tests → External dependencies not mocked/stubbed

## Acceptance Criteria
<list specific, measurable criteria that must be met for the feature to be considered complete>

Include test coverage requirements:
- [ ] All Red-Green-Refactor cycles completed
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Test coverage: [specify percentage, e.g., >90%]
- [ ] No tests testing implementation details (only public APIs)
- [ ] Code refactored after each Green phase

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

```bash
# Run all tests in verbose mode
uv run pytest tests/ -v

# Run with fail-fast to catch issues immediately
uv run pytest tests/ -x

# Run with coverage to verify completeness
uv run pytest tests/ --cov=<module> --cov-report=term-missing

# Verify coverage meets requirements (e.g., >90%)
uv run pytest tests/ --cov=<module> --cov-fail-under=90

# Run specific test file as you implement each cycle
uv run pytest tests/path/to/test_file.py -v

# Run linting to ensure code quality
uv run ruff check .
uv run ruff format --check .

# Integration tests (if applicable)
<specific integration test commands>
```

## Notes

### TDD Workflow Summary
1. Start with failing test (RED)
2. Make test pass with minimal code (GREEN)
3. Improve design while tests are green (REFACTOR)
4. Commit after each complete cycle
5. Repeat for next behavior

### Dave Farley's Key Insights
- **TDD is about design**: Tests force you to think from the caller's perspective
- **Small steps**: Many small cycles > few large cycles
- **Refactoring is not optional**: Technical debt accumulates if skipped
- **Fast feedback**: Run tests constantly, don't stay red too long

<optionally list any additional notes, future considerations, or context that are relevant to the feature that will be helpful to the developer>
```

## Feature
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- Include a path to the plan you created in the `ai-docs/2-features/<feature_name>.md` file.
- Note the number of Red-Green-Refactor cycles planned.
- Highlight any design principles emphasized in the refactoring phases.
