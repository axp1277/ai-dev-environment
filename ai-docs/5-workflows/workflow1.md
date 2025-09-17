# Workflow 1: Complete Session Processing Pipeline

## Variables
- `$SESSION_NUMBER` - The session number to process (e.g., 2 for session2.md)

## Overview
This workflow processes a brainstorming session through the complete document generation pipeline: specification creation, simplification review, and PRD generation.

## Workflow Steps

### Step 1: Generate Technical Specification
**Agent**: `brain2specs-agent`
**Input**: `0-brainstorming/session$SESSION_NUMBER.md`
**Output**: `2-specs/specs$SESSION_NUMBER.md`
**Command**: `/brain2specs $SESSION_NUMBER`

### Step 2: Review and Simplify Specification
**Agent**: `spec-simplification-agent`
**Input**:
- `0-brainstorming/session$SESSION_NUMBER.md` (original)
- `2-specs/specs$SESSION_NUMBER.md` (generated spec)
**Output**: `2-specs/specs$SESSION_NUMBER-simplified.md`

### Step 3: Generate Product Requirements Document
**Agent**: `brain2prd-agent`
**Input**: `0-brainstorming/session$SESSION_NUMBER.md`
**Output**: `1-prds/prd$SESSION_NUMBER.md`
**Command**: `/session2prd $SESSION_NUMBER`

## Execution Sequence

```yaml
workflow_name: "complete-session-processing"
session: $SESSION_NUMBER
steps:
  1. brain2specs_conversion:
     - Run: /brain2specs $SESSION_NUMBER
     - Creates: 2-specs/specs$SESSION_NUMBER.md

  2. spec_simplification:
     - Agent: spec-simplification-agent
     - Compare: session$SESSION_NUMBER.md vs specs$SESSION_NUMBER.md
     - Creates: 2-specs/specs$SESSION_NUMBER-simplified.md

  3. prd_generation:
     - Run: /session2prd $SESSION_NUMBER
     - Creates: 1-prds/prd$SESSION_NUMBER.md
```

## Expected Outputs
- `2-specs/specs$SESSION_NUMBER.md` - Initial technical specification
- `2-specs/specs$SESSION_NUMBER-simplified.md` - Reviewed and simplified specification
- `1-prds/prd$SESSION_NUMBER.md` - Product requirements document

## Success Criteria
- [ ] Technical specification generated from session $SESSION_NUMBER
- [ ] Specification reviewed for scope creep and over-engineering
- [ ] Simplified specification maintains original session intent
- [ ] PRD captures business requirements from session $SESSION_NUMBER
- [ ] All three documents are consistent and traceable to original session