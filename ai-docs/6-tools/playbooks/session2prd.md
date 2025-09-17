# Playbook: Brainstorming Session → Product Requirements Document

## Purpose
Transform a brainstorming session transcript into a PRD that captures the business context, requirements, and success metrics discussed during the session.

## Inputs
- `ai-docs/0-brainstorming/session<session_number>.md`
- Prompt reference: `ai-docs/4-prompts/session-to-prd.md`

## Steps
1. Open the relevant session file (`session<session_number>.md` or `session-<session_number>.md`).
2. Review the session-to-PRD prompt to align on structure, tone, and required sections.
3. Extract the session's business objectives, user personas, functional scope, constraints, and risks.
4. Draft the PRD using the template below, tying each section back to explicit statements in the transcript.
5. Save the finished document to `ai-docs/1-prds/prd<session_number>.md`.
6. Verify all sections are complete and the Source Session metadata references the correct file.

### PRD Template

```markdown
# [Product/Feature Name] - Product Requirements Document

## Executive Summary
[2-3 paragraph overview of what is being built and why]

## Document Version
- Version: 1.0
- Date: [Creation date]
- Source Session: session<session_number>.md

## Problem Statement

### Current State
[Description of current situation and pain points]

### Desired State
[Vision for the future state after implementation]

### Value Proposition
[Why this initiative is worth the investment]

## Target Users

### Primary User Personas
1. **[Persona Name]**
   - Role: [User role/title]
   - Goals: [What they aim to achieve]
   - Pain Points: [Current challenges]
   - Success Criteria: [How they define success]

### Use Cases
1. **[Use Case Name]**
   - Actor: [Persona]
   - Scenario: [Description]
   - Expected Outcome: [Result when successful]

## Requirements

### Functional Requirements
1. **[Category]**
   - FR1.1: [Requirement]
   - FR1.2: [Requirement]

2. **[Category]**
   - FR2.1: [Requirement]
   - FR2.2: [Requirement]

### Non-Functional Requirements
1. **Performance**
   - [Requirement]

2. **Security**
   - [Requirement]

3. **Usability**
   - [Requirement]

4. **Compatibility**
   - [Requirement]

## Scope & Constraints

### In Scope
- [Capabilities included in this iteration]

### Out of Scope
- [Explicit exclusions]

### Constraints
- Technical: [Limitations]
- Business: [Constraints]
- Timeline: [Deadlines or milestones]
- Resources: [Resourcing considerations]

## Success Metrics

### Key Performance Indicators (KPIs)
1. [Metric]: [Target & measurement method]
2. [Metric]: [Target & measurement method]

### Acceptance Criteria
1. [Criteria for considering the initiative complete]
2. [Quality standards that must be met]

## Dependencies & Risks

### Dependencies
- External Systems: [Systems or data feeds]
- Teams: [Partner teams]
- Prerequisites: [Conditions that must be true]

### Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | High/Medium/Low | High/Medium/Low | [Mitigation plan] |

## Timeline & Phases

### Proposed Phases
**Phase 1: [Name]** (Timeline)
- [Key deliverables]
- [Success criteria]

**Phase 2: [Name]** (Timeline)
- [Key deliverables]
- [Success criteria]

### Milestones
- [Milestone 1]
- [Milestone 2]
```

## Outputs
- `ai-docs/1-prds/prd<session_number>.md`
