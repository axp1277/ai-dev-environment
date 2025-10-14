# Brain2Stories Guide

This document serves as a comprehensive guide for analyzing brainstorming sessions and PRDs to generate user-focused user story documents. This guide is designed to bridge the gap between technical requirements and user-centric perspectives, ensuring features are understood from the end-user's point of view.

## Purpose

The Brain2Stories process transforms technical discussions and product requirements into user stories that:
- Focus on user value and outcomes rather than technical implementation
- Provide context for why features are being built
- Help align development with user needs and expectations
- Enable better validation and acceptance testing
- Create empathy for the end user throughout the development process

## Process Overview

1. **Input**: Brainstorming session transcript + PRD document
2. **Analysis**: Extract user-facing features and understand user personas
3. **Translation**: Convert technical requirements into user-centric stories
4. **Output**: A structured user story document organized by epics with clear acceptance criteria

## User Story Document Structure

When creating a user story document, follow this structure:

### 1. User Personas Section

```markdown
# User Personas

## Primary Persona: [Persona Name]
**Role**: [User role or job title]
**Goals**:
- [Primary goal 1]
- [Primary goal 2]

**Pain Points**:
- [Current challenge 1]
- [Current challenge 2]

**Technical Proficiency**: [Beginner/Intermediate/Advanced]

## Secondary Persona: [Persona Name]
[Repeat structure for additional personas as needed]
```

### 2. Epics and User Stories Section

Structure stories using epic groupings with clear user story format:

```markdown
# Epic 1: [Epic Name]

**Epic Goal**: [High-level goal this epic achieves]

## User Story 1.1: [Story Title]

**As a** [user persona]
**I want to** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [expected outcome]
- [ ] Given [context], when [action], then [expected outcome]
- [ ] Given [context], when [action], then [expected outcome]

**Priority**: [High/Medium/Low]
**Story Points**: [Estimated effort: 1, 2, 3, 5, 8, 13]

---

## User Story 1.2: [Story Title]
[Repeat structure]

# Epic 2: [Epic Name]
[Continue pattern]
```

### 3. Story Map (Optional)

```markdown
# Story Map

## Release 1 - MVP
- Epic 1: [Epic Name]
  - Story 1.1: [Title]
  - Story 1.2: [Title]
- Epic 2: [Epic Name]
  - Story 2.1: [Title]

## Release 2 - Enhanced Features
- Epic 3: [Epic Name]
  - Story 3.1: [Title]
```

## Story Writing Guidelines

### User Story Format

Always use the standard format:
- **As a** [persona/role]
- **I want to** [action/feature]
- **So that** [benefit/outcome]

### Quality Criteria (INVEST)

Stories should be:
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers user value
- **E**stimable: Can be sized
- **S**mall: Completable in one iteration
- **T**estable: Has clear acceptance criteria

### Acceptance Criteria Guidelines

Use Given-When-Then format:
- **Given** [initial context/state]
- **When** [action is performed]
- **Then** [expected result]

Example:
- Given I am logged in as an administrator
- When I click the "Generate Report" button
- Then a PDF report should download within 5 seconds

### Priority Levels

- **High**: Critical for MVP, blocks other work, or high user value
- **Medium**: Important but not blocking, good user value
- **Low**: Nice to have, future enhancement, or edge case

### Story Points

Estimate relative effort using Fibonacci sequence:
- **1**: Trivial change, well-understood
- **2**: Simple feature, minimal risk
- **3**: Standard feature, some complexity
- **5**: Complex feature, some unknowns
- **8**: Very complex, significant unknowns
- **13**: Epic-level, needs breakdown

## Analysis Guidelines

When analyzing inputs to create user stories:

### 1. Identify User Personas

- Look for mentions of user types, roles, or audiences
- Consider who will use each feature
- Create distinct personas if multiple user types exist
- Define goals and pain points for each persona

### 2. Extract User-Facing Features

- Focus on capabilities that users directly interact with
- Distinguish between user features and technical requirements
- Identify the "why" behind each feature
- Consider the user journey and workflow

### 3. Group into Epics

- Organize related stories into logical epics
- Each epic should represent a cohesive user goal
- Epics should align with product phases or releases
- Keep epics focused and bounded

### 4. Write from User Perspective

- Use user language, not technical jargon
- Focus on outcomes and benefits
- Avoid implementation details
- Make the value clear

### 5. Define Clear Acceptance Criteria

- Cover happy path and edge cases
- Make criteria specific and measurable
- Include UI/UX expectations where relevant
- Consider non-functional requirements (performance, security)

## Common Patterns

### Feature Story Pattern
```markdown
**As a** [user]
**I want to** [use specific feature]
**So that** [achieve specific outcome]
```

### Configuration Story Pattern
```markdown
**As a** [admin/power user]
**I want to** [configure/customize setting]
**So that** [adapt system to my needs]
```

### Integration Story Pattern
```markdown
**As a** [user]
**I want to** [integrate with external system]
**So that** [avoid manual work/sync data]
```

### Reporting Story Pattern
```markdown
**As a** [manager/analyst]
**I want to** [view/generate report]
**So that** [make informed decisions]
```

## Examples

### Example 1: Authentication Feature

```markdown
# Epic 1: User Authentication and Authorization

**Epic Goal**: Enable secure access control so only authorized users can access the system

## User Story 1.1: User Login

**As a** registered user
**I want to** log in with my email and password
**So that** I can securely access my account

**Acceptance Criteria**:
- [ ] Given I am on the login page, when I enter valid credentials and click "Login", then I am redirected to my dashboard
- [ ] Given I am on the login page, when I enter invalid credentials, then I see an error message "Invalid email or password"
- [ ] Given I have entered my password, when I view the password field, then the password is masked with dots
- [ ] Given I have failed login 5 times, when I attempt the 6th login, then my account is temporarily locked for 15 minutes

**Priority**: High
**Story Points**: 3

---

## User Story 1.2: Password Reset

**As a** user who forgot my password
**I want to** reset my password via email
**So that** I can regain access to my account

**Acceptance Criteria**:
- [ ] Given I click "Forgot Password", when I enter my email, then I receive a password reset link via email within 2 minutes
- [ ] Given I click the reset link, when I enter a new password meeting requirements, then my password is updated
- [ ] Given the reset link is more than 1 hour old, when I click it, then I see "Link expired" message

**Priority**: High
**Story Points**: 3
```

### Example 2: Data Visualization Feature

```markdown
# Epic 2: Analytics Dashboard

**Epic Goal**: Provide visual insights into user activity and system performance

## User Story 2.1: View Activity Chart

**As a** business analyst
**I want to** see a line chart of user activity over time
**So that** I can identify trends and patterns

**Acceptance Criteria**:
- [ ] Given I am on the dashboard, when the page loads, then I see a line chart showing last 30 days of activity
- [ ] Given I hover over a data point, when I pause for 1 second, then I see a tooltip with exact values
- [ ] Given I want to see a different time range, when I select "Last 90 days", then the chart updates accordingly
- [ ] Given there is no data for a date, when viewing the chart, then that point shows as zero with a dotted line

**Priority**: Medium
**Story Points**: 5

---

## User Story 2.2: Export Dashboard Data

**As a** data analyst
**I want to** export dashboard data to CSV
**So that** I can perform custom analysis in Excel

**Acceptance Criteria**:
- [ ] Given I am viewing the dashboard, when I click "Export to CSV", then a CSV file downloads within 3 seconds
- [ ] Given the CSV is downloaded, when I open it, then all visible data is included with proper headers
- [ ] Given I have applied filters, when I export, then only filtered data is included

**Priority**: Low
**Story Points**: 2
```

## Integration with Development Process

### From PRD to User Stories

The PRD provides:
- Product vision and objectives
- Feature list and requirements
- Technical constraints

User Stories add:
- User perspective and context
- Specific acceptance criteria
- Implementation priority
- Effort estimation

### From User Stories to Technical Specs

User stories inform technical specs by:
- Defining what success looks like (acceptance criteria)
- Providing context for technical decisions
- Identifying user-facing vs. backend requirements
- Clarifying scope and boundaries

### From User Stories to Validation

User stories enable validation by:
- Providing testable acceptance criteria
- Defining expected user journeys
- Specifying edge cases and error handling
- Setting quality standards

## Best Practices

### DO:
- ✓ Write from the user's perspective
- ✓ Focus on the value and outcome
- ✓ Keep stories small and focused
- ✓ Include clear acceptance criteria
- ✓ Consider different user personas
- ✓ Use consistent story format
- ✓ Group related stories into epics
- ✓ Prioritize based on user value

### DON'T:
- ✗ Include implementation details
- ✗ Write technical specifications
- ✗ Make stories too large or complex
- ✗ Use technical jargon
- ✗ Skip acceptance criteria
- ✗ Ignore edge cases
- ✗ Write from developer perspective
- ✗ Mix multiple features in one story

## Practical Tips

1. **Start with Personas**: Understand who you're building for before writing stories
2. **Think User Journey**: Consider the complete user workflow, not just isolated features
3. **Ask "Why"**: Always include the "so that" clause - if you can't articulate the value, reconsider the story
4. **Collaborate**: User stories benefit from input from product owners, developers, and users
5. **Iterate**: Stories will evolve during development - that's expected and healthy
6. **Estimate Together**: Story pointing works best as a team activity
7. **Reference Specs**: Stories should align with but not duplicate technical specifications

## Document Metadata

When creating the user stories document, include:

```markdown
---
Session: [Session number]
Created: [Date]
Inputs:
  - Brainstorming: session-[N].md
  - PRD: prd[N].md
Status: [Draft/Review/Approved]
---
```

## Conclusion

This Brain2Stories guide provides a standardized approach to transform brainstorming sessions and PRDs into user-centric story documents. Following this guide ensures that development stays focused on delivering user value, provides clear acceptance criteria for validation, and maintains empathy for end users throughout the development process.

Remember: Good user stories are conversations, not contracts. They should spark discussion and collaboration, not replace it.
