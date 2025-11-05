# /brain2validation - Generate Validation and Acceptance Criteria

## Usage
`/brain2validation <session_number>`

## Description
Generates comprehensive validation document with test scenarios, acceptance criteria, and quality assurance requirements from all planning documents.

## Examples
- `/brain2validation 2` - Generates validation-2.md from session2.md, prd2.md, stories-2.md, and specs-2.md
- `/brain2validation 4` - Generates validation-4.md from all session 4 planning documents

## Task Instructions

When this command is invoked with a session number:

1. **Locate input files**:
   - Brainstorming: `ai-docs/0-brainstorming/session{N}.md` or `session-{N}.md`
   - PRD: `ai-docs/2-prds/prd{N}.md`
   - User Stories: `ai-docs/2-user-stories/stories-{N}.md`
   - Specifications: `ai-docs/2-specs/specs-{N}.md`

2. **Read the brain2validation prompt**: `ai-docs/4-prompts/brain2validation.md` for comprehensive guidelines

3. **Analyze inputs** to extract:
   - All testable requirements and features
   - User acceptance criteria from stories
   - Technical requirements from specs
   - Success metrics from PRD
   - Edge cases and error scenarios
   - Non-functional requirements (performance, security, usability)

4. **Generate validation document** following the structure defined in brain2validation.md prompt:

### Document Structure

```markdown
---
Session: {N}
Created: [Date]
Inputs:
  - Brainstorming: session-{N}.md
  - PRD: prd{N}.md
  - User Stories: stories-{N}.md
  - Specs: specs-{N}.md
Test Coverage Goal: 90%
Status: Draft
---

# [Project Name] - Validation and Acceptance Criteria

## Testing Overview

### Test Strategy
**Approach**: [Manual/Automated/Mixed]
**Coverage Goals**:
- Unit Tests: [X%]
- Integration Tests: [Y%]
- E2E Tests: [Z%]

### Test Environments
- Development: [Description]
- Staging: [Description]
- Production: [Description]

### Testing Tools
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

## Feature 1: [Feature Name]

**Feature Description**: [Brief description from specs/stories]
**Related User Stories**: [Story 1.1, Story 1.2, etc.]
**Priority**: [Critical/High/Medium/Low]

### Test Scenario 1.1: [Scenario Name]

**Objective**: [What this test validates]
**Preconditions**:
- [Required state or setup 1]
- [Required state or setup 2]

**Test Steps**:
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]

**Expected Results**:
- ✓ [Expected outcome 1]
- ✓ [Expected outcome 2]

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

**Test Type**: [Unit/Integration/E2E/Manual]
**Automation**: [Yes/No/Partial]
**Priority**: [P0/P1/P2/P3]

---

[Continue with additional test scenarios...]

## Non-Functional Requirements

### Performance Validation
- [ ] Response time under [X]ms for [scenario]
- [ ] System handles [N] concurrent users
- [ ] Page load time under [X] seconds

### Security Validation
- [ ] Authentication properly validates credentials
- [ ] Authorization restricts access appropriately
- [ ] Sensitive data is encrypted
- [ ] SQL injection prevention verified

### Usability Validation
- [ ] UI follows design specifications
- [ ] Error messages are clear and helpful
- [ ] Accessibility standards met (WCAG 2.1 Level AA)

## Edge Cases and Error Scenarios

### Feature: [Feature Name]

#### Edge Case 1: [Description]
**Test**: [What to test]
**Expected**: [How system should handle it]
**Priority**: [High/Medium/Low]

#### Error Scenario 1: [Description]
**Trigger**: [How to cause the error]
**Expected Error Handling**:
- Display: [Error message shown to user]
- Logging: [What gets logged]
- Recovery: [How system recovers]

## Traceability Matrix

| User Story | Technical Spec | Test Scenario | Status |
|------------|----------------|---------------|---------|
| Story 1.1  | Task 3.2      | TS 1.1, 1.2   | Pending |
| Story 1.2  | Task 3.3      | TS 1.3, 1.4   | Pending |

## Test Execution Summary

**Test Run Date**: [Date]
**Environment**: [Dev/Staging/Prod]
**Build Version**: [Version]

| Feature | Total Tests | Passed | Failed | Blocked | Pass Rate |
|---------|-------------|--------|--------|---------|-----------|
| Auth    | 0          | 0      | 0      | 0       | N/A       |
| API     | 0          | 0      | 0      | 0       | N/A       |

**Overall Pass Rate**: 0% (Not yet executed)
```

5. **Save the output** as `ai-docs/2-validation/validation-{N}.md`

## Key Guidelines

- **Comprehensive Coverage**: Cover happy path, alternate paths, error paths, edge cases
- **Given-When-Then**: Use this format for all acceptance criteria
- **Measurable Outcomes**: Use specific values, not vague terms
- **Test Types**: Classify as Unit, Integration, E2E, Manual, Performance, Security
- **Priority Levels**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **Automation Ready**: Write scenarios that can be automated
- **Traceability**: Link test scenarios back to requirements
- **Non-Functional**: Don't forget performance, security, usability
- **Edge Cases**: Actively identify boundary conditions and error scenarios

## Context Passing

This command receives context from:
- **Brainstorming Session**: Original requirements and discussions
- **PRD**: Business objectives and success metrics
- **User Stories**: User acceptance criteria and workflows
- **Technical Specs**: Implementation requirements and constraints

This is the final document in the planning pipeline and provides complete validation coverage.

## Important Notes

- If input files don't exist, report error with clear message
- Maintain traceability with metadata and matrix
- Include test execution tracking tables (initially empty)
- Focus on testability - every requirement should have test scenarios
- Include both positive and negative test cases
- Consider security implications for all features
- Specify exact expected values, not ranges or vague terms
- Link test scenarios to user stories and specs for traceability
