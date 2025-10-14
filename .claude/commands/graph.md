# /graph - Generate Visual Mermaid Diagrams

## Usage
`/graph <session_number>`

## Description
Analyzes all project documentation and generates two complementary Mermaid diagrams: a workflow diagram showing user journeys and process flows, and an architecture diagram showing system components and technical infrastructure.

## Examples
- `/graph 2` - Generates workflow-2.mmd and architecture-2.mmd from session2.md, prd2.md, stories-2.md, specs-2.md, and validation-2.md
- `/graph 4` - Generates workflow-4.mmd and architecture-4.mmd from all session 4 planning documents

## Task Instructions

When this command is invoked with a session number:

1. **Locate input files**:
   - Brainstorming: `ai-docs/0-brainstorming/session{N}.md` or `session-{N}.md`
   - PRD: `ai-docs/2-prds/prd{N}.md`
   - User Stories: `ai-docs/2-user-stories/stories-{N}.md`
   - Specifications: `ai-docs/2-specs/specs-{N}.md`
   - Validation: `ai-docs/2-validation/validation-{N}.md`

2. **Read the brain2graph prompt**: `ai-docs/4-prompts/brain2graph.md` for comprehensive guidelines

3. **Analyze all inputs** to extract:
   - User journeys and process flows (from Stories and Specs)
   - System components and architecture (from Specs and PRD)
   - Integration points and data flow (from Specs)
   - State transitions and decision points (from Stories and Validation)
   - Technology stack and infrastructure (from Specs)

4. **Generate TWO separate Mermaid diagram files**:

### Workflow Diagram (workflow-{N}.mmd)

Focus on user perspective and process flow:
- User journeys from start to end
- Process sequences and decision points
- Data flow through the system
- User interactions and touchpoints
- State transitions
- Business process flow

Use Mermaid diagram types:
- `graph TD` or `graph LR` for flowcharts
- `journey` for user journey maps
- `stateDiagram-v2` for state machines
- `sequenceDiagram` for interaction flows

### Architecture Diagram (architecture-{N}.mmd)

Focus on system structure and technical components:
- System components and modules
- Data storage and databases
- External integrations
- API endpoints and services
- Technology stack
- Component dependencies
- Communication patterns

Use Mermaid diagram types:
- `graph TD` or `graph LR` for component relationships
- `C4Context` for system context
- `flowchart` for detailed component interactions

5. **File Format**:

Each `.mmd` file should contain:

```markdown
---
title: [Descriptive Title]
session: {N}
created: [Date]
description: [Brief 1-2 sentence description]
---

```mermaid
[Mermaid diagram code]
```
```

6. **Save the outputs**:
   - `ai-docs/2-diagrams/workflow-{N}.mmd`
   - `ai-docs/2-diagrams/architecture-{N}.mmd`

## Key Guidelines

- **Clarity First**: Maximum 15-20 nodes per diagram
- **Use Hierarchy**: Group related components with subgraphs
- **Label Clearly**: Descriptive names, not abbreviations
- **Show Flow**: Clear direction of data/process flow
- **Consistent Style**: Use same shapes for similar concepts
- **Color Coding**: Use consistent colors for component types
- **Test Rendering**: Verify diagrams render correctly in Mermaid live editor

### Simplification Strategies

If diagram is too complex:
- Break into multiple focused diagrams
- Use subgraphs to create hierarchy
- Abstract details into higher-level components
- Merge similar components

## Diagram Quality Checklist

Before finalizing, verify:
1. **Renders Correctly**: Test in Mermaid live editor (https://mermaid.live/)
2. **Readable**: Text is legible, not cramped
3. **Complete**: All major flows/components shown
4. **Accurate**: Reflects actual system design
5. **Consistent**: Matches other project documentation
6. **Valuable**: Adds clarity, not confusion

## Context Passing

This command receives context from:
- **Brainstorming Session**: Original requirements and discussions
- **PRD**: Business objectives and product vision
- **User Stories**: User workflows and acceptance criteria
- **Technical Specs**: Implementation details and architecture
- **Validation**: Test scenarios and validation flows

This is the final visual documentation in the planning pipeline.

## Important Notes

- If input files don't exist, report error with clear message
- Include metadata in each .mmd file for traceability
- Focus on clarity - simplify complex flows
- Use consistent visual language across both diagrams
- Test diagrams before finalizing
- Keep workflow diagram user-centric
- Keep architecture diagram technically accurate
