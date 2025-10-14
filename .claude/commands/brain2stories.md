# /brain2stories - Convert Brainstorming to User Stories

## Usage
`/brain2stories <session_number>`

## Description
Converts a brainstorming session and PRD into user-centric user story documents with epics, stories, and acceptance criteria.

## Examples
- `/brain2stories 2` - Generates stories-2.md from session2.md and prd2.md
- `/brain2stories 4` - Generates stories-4.md from session4.md and prd4.md

## Task Instructions

When this command is invoked with a session number:

1. **Locate input files**:
   - Brainstorming: `ai-docs/0-brainstorming/session{N}.md` or `session-{N}.md`
   - PRD: `ai-docs/2-prds/prd{N}.md`

2. **Read the brain2stories prompt**: `ai-docs/4-prompts/brain2stories.md` for comprehensive guidelines

3. **Analyze inputs** to extract:
   - User personas and roles
   - User-facing features and capabilities
   - User goals and motivations
   - Expected user workflows
   - Success criteria from user perspective

4. **Generate user stories document** following the structure defined in brain2stories.md prompt:

### Document Structure

```markdown
---
Session: {N}
Created: [Date]
Inputs:
  - Brainstorming: session-{N}.md
  - PRD: prd{N}.md
Status: Draft
---

# [Project Name] - User Stories

## User Personas

### Primary Persona: [Persona Name]
**Role**: [User role or job title]
**Goals**:
- [Primary goal 1]
- [Primary goal 2]

**Pain Points**:
- [Current challenge 1]
- [Current challenge 2]

**Technical Proficiency**: [Beginner/Intermediate/Advanced]

## Epic 1: [Epic Name]

**Epic Goal**: [High-level goal this epic achieves]

### User Story 1.1: [Story Title]

**As a** [user persona]
**I want to** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [expected outcome]
- [ ] Given [context], when [action], then [expected outcome]

**Priority**: [High/Medium/Low]
**Story Points**: [1, 2, 3, 5, 8, 13]

---

[Continue with additional stories...]

## Story Map

### Release 1 - MVP
- Epic 1: [Epic Name]
  - Story 1.1: [Title]
  - Story 1.2: [Title]

### Release 2 - Enhanced Features
- Epic 2: [Epic Name]
  - Story 2.1: [Title]
```

5. **Save the output** as `ai-docs/2-user-stories/stories-{N}.md`

## Key Guidelines

- **User Perspective**: Write from the user's point of view, not technical implementation
- **Focus on Value**: Every story should clearly state the user benefit
- **INVEST Criteria**: Stories should be Independent, Negotiable, Valuable, Estimable, Small, Testable
- **Given-When-Then**: Use this format for acceptance criteria
- **Personas First**: Define clear user personas before writing stories
- **Epic Organization**: Group related stories into logical epics
- **Priority Levels**: High (MVP), Medium (important), Low (nice-to-have)
- **Story Points**: Use Fibonacci sequence for relative effort estimation

## Context Passing

This command receives context from:
- **Brainstorming Session**: Original ideas and discussions
- **PRD**: Business requirements and product vision

And provides context to:
- **brain2specs**: Technical specifications will reference these user stories
- **brain2validation**: Test scenarios will validate these stories

## Important Notes

- If input files don't exist, report error with clear message
- Maintain traceability with metadata section
- Focus on user-facing features, not backend implementation
- Use consistent terminology across all stories
- Include both happy path and edge cases in acceptance criteria
- Prioritize based on PRD requirements and brainstorming emphasis
