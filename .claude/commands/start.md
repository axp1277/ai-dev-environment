Execute a comprehensive workflow to transform a brainstorming session into both PRD and technical specification documents.

**Usage**: `/start <session_number>`

**Process**:
1. **Step 1 - PRD Generation**: Use the brain2prd-agent to analyze brainstorming session$ARGUMENTS.md from ai-docs/0-brainstorming/ and create a Product Requirements Document (PRD) in ai-docs/2-prds/prd-$ARGUMENTS.md

2. **Step 2 - Technical Specs Generation**: Use the brain2specs-agent to analyze the same brainstorming session$ARGUMENTS.md and create a technical specification document in ai-docs/2-specs/specs-$ARGUMENTS.md

**Input**: `ai-docs/0-brainstorming/session$ARGUMENTS.md`
**Outputs**: 
- `ai-docs/2-prds/prd-$ARGUMENTS.md` (PRD document)
- `ai-docs/2-specs/specs-$ARGUMENTS.md` (Technical specifications)

**Example**: `/start 1` will process session1.md and generate both prd-1.md and specs-1.md

This command replaces the manual two-step process with a single automated workflow that ensures consistency and completeness in document generation from brainstorming to implementation-ready specifications.