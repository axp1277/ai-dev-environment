# /session2prd - Convert Session to Product Requirements Document

## Usage
`/session2prd <session_number>`

## Description
Converts a brainstorming session or transcript into a structured Product Requirements Document (PRD).

## Examples
- `/session2prd 2` - Converts session2.md to prd2.md
- `/session2prd 5` - Converts session5.md or session-5.md to prd5.md

## Task Instructions

When this command is invoked with a session number:

1. **Locate the session file**: Look for `ai-docs/0-brainstorming/session{N}.md` or `session-{N}.md`

2. **Analyze the session** using the comprehensive PRD structure to extract:
   - Business objectives and vision
   - Problem statements and value propositions
   - Target users and personas
   - Functional and non-functional requirements
   - Scope, constraints, and timelines
   - Success metrics and acceptance criteria

3. **Generate the PRD** following this structure:

### PRD Structure

```markdown
# [Product/Feature Name] - Product Requirements Document

## Executive Summary
[2-3 paragraph overview of what is being built and why]

## Document Version
- Version: 1.0
- Date: [Current date]
- Source Session: session{N}.md

## Problem Statement

### Current State
[Description of current situation and pain points]

### Desired State
[Vision of how things should work after implementation]

### Value Proposition
[Why this solution is worth building]

## Target Users

### Primary User Personas
1. **[Persona Name]**
   - Role: [User role/title]
   - Goals: [What they want to achieve]
   - Pain Points: [Current challenges]
   - Success Criteria: [What success looks like]

### Use Cases
1. **[Use Case Name]**
   - Actor: [Which persona]
   - Scenario: [Description]
   - Expected Outcome: [Success criteria]

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
   - [Requirements]

2. **Security**
   - [Requirements]

3. **Usability**
   - [Requirements]

## Scope & Constraints

### In Scope
- [What is included in this version]

### Out of Scope
- [What is explicitly not included]

### Constraints
- Technical: [Limitations]
- Business: [Constraints]
- Timeline: [Time constraints]

## Success Metrics

### Key Performance Indicators (KPIs)
1. [Metric]: [Target and measurement method]
2. [Metric]: [Target and measurement method]

### Acceptance Criteria
1. [Criteria for completion]
2. [Quality standards]

## Dependencies & Risks

### Dependencies
- External Systems: [Systems]
- Teams: [Teams involved]
- Prerequisites: [Requirements]

### Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Strategy] |
```

4. **Save the output** as `ai-docs/1-prds/prd{N}.md`

## Key Guidelines

- **Focus on Business Value**: Extract the "why" behind requests, not just the "what"
- **User-Centric Language**: Frame requirements from the user's perspective
- **Measurable Success**: Define clear, quantifiable success metrics
- **High-Level Focus**: Business requirements, not technical implementation details
- **Stakeholder Friendly**: Use terminology that non-technical stakeholders can understand
- **Prioritize Features**: Identify must-haves vs nice-to-haves based on discussion emphasis

## Important Notes

- If the session file doesn't exist, report an error
- Maintain traceability by referencing the source session
- Structure the PRD to support future conversion to technical specifications
- Give more weight to conclusions reached near the end of brainstorming sessions
- Resolve any contradictions by prioritizing the most recent or consensus views