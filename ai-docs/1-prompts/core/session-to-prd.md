# Session to PRD (Product Requirements Document) Guide

This document serves as a comprehensive guide for analyzing brainstorming sessions or meeting transcripts and converting them into structured Product Requirements Documents. This guide is designed to work with any project and can be used by AI assistants to create clear, business-focused requirement documents.

## Purpose

The Session-to-PRD process transforms brainstorming conversations and meeting transcripts into high-level product requirement documents that define what needs to be built before diving into technical specifications. PRDs bridge the gap between business vision and technical implementation.

## Process Overview

1. **Input**: A brainstorming session transcript, meeting notes, or product discussion
2. **Analysis**: Review the transcript to identify business objectives, user needs, and requirements
3. **Extraction**: Identify problem statements, target users, functional requirements, and success criteria
4. **Output**: A well-structured PRD document that can later be converted into technical specifications

## Quick Execution Checklist

1. Open the source transcript at `ai-docs/0-brainstorming/session<session_number>.md`.
2. Refresh on this prompt stored at `ai-docs/1-prompts/core/session-to-prd.md` to align on tone and structure.
3. Summarize objectives, personas, functional scope, and risks directly from the transcript.
4. Draft the PRD and save it to `ai-docs/4-prds/prd<session_number>.md`.
5. Confirm metadata references the correct session and that every section in the template is populated.

## PRD Document Structure

When creating a PRD from a session, follow this structure:

### 1. Executive Summary

```markdown
# [Product/Feature Name] - Product Requirements Document

## Executive Summary
[2-3 paragraph overview of what is being built and why]

## Document Version
- Version: 1.0
- Date: [Creation date]
- Source Session: sessionN.md
```

### 2. Problem Statement

```markdown
## Problem Statement

### Current State
[Description of the current situation and pain points]

### Desired State
[Vision of how things should work after implementation]

### Value Proposition
[Why this solution is worth building]
```

### 3. User Personas & Use Cases

```markdown
## Target Users

### Primary User Personas
1. **[Persona Name]**
   - Role: [User role/title]
   - Goals: [What they want to achieve]
   - Pain Points: [Current challenges]
   - Success Criteria: [What success looks like for them]

### Use Cases
1. **[Use Case Name]**
   - Actor: [Which persona]
   - Scenario: [Description of the use case]
   - Expected Outcome: [What happens when successful]
```

### 4. Requirements

```markdown
## Requirements

### Functional Requirements
1. **[Requirement Category]**
   - FR1.1: [Specific requirement]
   - FR1.2: [Specific requirement]

2. **[Requirement Category]**
   - FR2.1: [Specific requirement]
   - FR2.2: [Specific requirement]

### Non-Functional Requirements
1. **Performance**
   - [Performance requirements]

2. **Security**
   - [Security requirements]

3. **Usability**
   - [Usability requirements]

4. **Compatibility**
   - [Compatibility requirements]
```

### 5. Scope & Constraints

```markdown
## Scope & Constraints

### In Scope
- [What is included in this version]
- [Core features to be built]

### Out of Scope
- [What is explicitly not included]
- [Features for future versions]

### Constraints
- Technical: [Technical limitations]
- Business: [Business constraints]
- Timeline: [Time constraints]
- Resources: [Resource limitations]
```

### 6. Success Metrics

```markdown
## Success Metrics

### Key Performance Indicators (KPIs)
1. [Metric 1]: [Target value and measurement method]
2. [Metric 2]: [Target value and measurement method]

### Acceptance Criteria
1. [Criteria for considering the product complete]
2. [Quality standards that must be met]
```

### 7. Dependencies & Risks

```markdown
## Dependencies & Risks

### Dependencies
- External Systems: [Systems this depends on]
- Teams: [Other teams involved]
- Prerequisites: [What must be in place first]

### Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
```

### 8. Timeline & Phases

```markdown
## Timeline & Phases

### Proposed Phases
**Phase 1: [Name]** (Timeline)
- [Key deliverables]
- [Success criteria]

**Phase 2: [Name]** (Timeline)
- [Key deliverables]
- [Success criteria]

### Milestones
- [Date]: [Milestone description]
- [Date]: [Milestone description]
```

## Analysis Guidelines

When analyzing a session transcript for PRD creation:

1. **Focus on Business Value**: Extract the "why" behind requests, not just the "what"

2. **Identify Stakeholders**: Determine who will use the product and who will be affected

3. **Clarify Objectives**:
   - What problem are we solving?
   - Who experiences this problem?
   - What is the impact of solving it?

4. **Extract Requirements, Not Solutions**: Focus on what needs to be accomplished, not how

5. **Prioritize Features**: Identify must-haves vs nice-to-haves based on discussion emphasis

6. **Note Constraints Early**: Identify mentioned limitations, deadlines, or resource constraints

## Key Differences from Technical Specifications

| Aspect | PRD (This Document) | Technical Specification |
|--------|-------------------|------------------------|
| Audience | Stakeholders, Product Managers, Business | Developers, Technical Teams |
| Focus | What & Why | How |
| Language | Business terminology | Technical terminology |
| Detail Level | High-level requirements | Implementation details |
| Output | Requirements & objectives | Tasks & technical design |

## Important Considerations

1. **Business Language**: Use terminology that non-technical stakeholders can understand

2. **User-Centric**: Frame requirements from the user's perspective

3. **Measurable Success**: Define clear, quantifiable success metrics

4. **Flexibility**: Leave room for technical teams to determine implementation approaches

5. **Traceability**: Maintain clear references to source sessions and discussions

6. **Living Document**: Structure the PRD to support updates as requirements evolve

## Template for Quick Reference

When creating a PRD, ensure you cover:
- ✅ Executive Summary
- ✅ Problem Statement
- ✅ Target Users
- ✅ Functional Requirements
- ✅ Non-Functional Requirements
- ✅ Scope (In/Out)
- ✅ Success Metrics
- ✅ Dependencies & Risks
- ✅ Timeline

## Practical Tips

1. **First Pass**: Read the entire transcript to understand the context and vision
2. **Business Extraction**: Focus on business goals, user needs, and value propositions
3. **Requirement Mining**: List all mentioned features and capabilities
4. **Prioritization**: Organize requirements by importance and dependency
5. **Validation**: Ensure the PRD answers "What are we building and why?"

## Output File Naming

PRDs should be saved as:
- Location: `ai-docs/4-prds/`
- Naming: `prdN.md` where N matches the session number
- Example: Session 3 → prd3.md

## Conclusion

This Session-to-PRD guide provides a standardized approach to transform brainstorming sessions and meeting transcripts into comprehensive Product Requirements Documents. Following this guide ensures that business objectives are clearly captured before technical implementation begins, creating a solid foundation for subsequent technical specification development.
