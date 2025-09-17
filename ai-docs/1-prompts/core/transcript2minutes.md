# Meeting Transcript to Minutes Guidelines

## Purpose
Convert meeting transcripts between programmer (Andrea) and clients into structured, actionable meeting reports that capture all critical information and next steps.

## Analysis Framework

### Meeting Context
- Identify all participants and their roles
- Extract meeting date, duration, and purpose
- Understand the overall meeting objectives

### Content Extraction Priorities
1. **Decisions Made** - Firm commitments and agreed directions
2. **Action Items** - Specific tasks with ownership and deadlines
3. **Technical Requirements** - New features, changes, or technical decisions
4. **Issues & Blockers** - Problems identified and proposed solutions
5. **Timeline & Deadlines** - All mentioned dates and milestones
6. **Open Questions** - Unresolved items requiring follow-up

## Output Structure

Create a markdown report with these sections:

### Header
```markdown
# Meeting Minutes - Meeting [number]
**Date:** [date or "Not specified"]
**Participants:** Andrea (Programmer), [Client name/role]
**Duration:** [duration or "Not specified"]
```

### Executive Summary
- 2-3 sentences summarizing the main outcomes
- Focus on what was accomplished and decided

### Key Decisions
- List important decisions made during the meeting
- Include the reasoning behind decisions when discussed
- Note any changes to project scope, timeline, or approach

### Action Items
Organize tasks by assignee:

**Andrea's Tasks:**
- [ ] Task description [Deadline: date/TBD] [Priority: High/Medium/Low]

**Client's Tasks:**
- [ ] Task description [Deadline: date/TBD] [Priority: High/Medium/Low]

**Shared/Discussion Items:**
- [ ] Task description [Deadline: date/TBD] [Priority: High/Medium/Low]

### Technical Items

**New Features/Requirements:**
- Feature description and current status (approved/under consideration)

**Issues Reported:**
- Issue description, severity, and proposed solution

**Technical Decisions:**
- Technology choices, architecture decisions, implementation approaches

### Project Status
- Work completed since last meeting
- Current progress on ongoing tasks
- Upcoming milestones and their status

### Open Questions
- Unresolved items that need clarification
- Who should provide answers or make decisions
- Target date for resolution

### Next Steps
- Immediate actions before next meeting
- Next meeting date and agenda items (if discussed)
- Any preparation needed by participants

## Extraction Guidelines

### For Action Items:
- Be specific about what needs to be done
- Clearly identify who is responsible
- Extract deadlines even if tentative
- Infer priority from discussion tone and urgency
- Include dependencies between tasks

### For Technical Content:
- Capture exact feature requirements as discussed
- Note any technical constraints or considerations
- Record technology decisions and alternatives considered
- Flag any technical risks or concerns raised

### For Decisions:
- Distinguish between firm decisions and tentative discussions
- Include the context that led to decisions
- Note any dissenting opinions or concerns raised

### For Deadlines:
- Extract all mentioned dates, even if approximate
- Note milestone dependencies
- Flag any timeline concerns or risks discussed

## Quality Standards

- **Accuracy**: Ensure all critical information is captured
- **Clarity**: Use clear, actionable language
- **Completeness**: Don't miss implicit action items or decisions
- **Organization**: Group related items logically
- **Actionability**: Focus on what needs to happen next

## Common Pitfalls to Avoid

- Don't assume unstated details
- Don't editorialize or add opinions not expressed
- Don't miss follow-up items that weren't explicitly called "action items"
- Don't overlook technical details that might impact implementation
- Don't ignore budget, timeline, or resource constraints mentioned

## Tone and Style

- Professional but accessible
- Focus on outcomes and next steps
- Use present tense for current status, future tense for planned actions
- Be concise but thorough
- Emphasize actionable information over discussion details