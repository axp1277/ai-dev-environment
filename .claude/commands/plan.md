# /plan - Master Planning Command

## Usage
`/plan <session_number>`

## Description
Master command that orchestrates the complete document generation pipeline from brainstorming session to final diagrams. Sequentially invokes all planning commands with context passing and progress reporting.

## Examples
- `/plan 2` - Generates complete planning suite from session2.md
- `/plan 4` - Generates complete planning suite from session4.md

## Pipeline Overview

This command executes the following sequence:

```
Brainstorming Session (input)
       ↓
1. /session2prd     → generates prd{N}.md
       ↓
2. /brain2stories   → generates stories-{N}.md
       ↓
3. /brain2specs     → generates specs-{N}.md
       ↓
4. /brain2validation → generates validation-{N}.md
       ↓
5. /graph           → generates workflow-{N}.mmd + architecture-{N}.mmd
       ↓
Complete Planning Documentation (output)
```

## Task Instructions

When this command is invoked with a session number:

### Phase 0: Pre-flight Validation

1. **Verify input file exists**:
   - Check for `ai-docs/0-brainstorming/session{N}.md` OR `session-{N}.md`
   - If not found, report error: "❌ Error: Brainstorming session {N} not found. Please create ai-docs/0-brainstorming/session{N}.md first."
   - Exit if missing

2. **Check output directories exist**:
   - `ai-docs/2-prds/`
   - `ai-docs/2-user-stories/`
   - `ai-docs/2-specs/`
   - `ai-docs/2-validation/`
   - `ai-docs/2-diagrams/`
   - If any missing, report error with list of missing directories

3. **Display pipeline overview**:
   ```
   🎯 Starting Planning Pipeline for Session {N}

   Pipeline Steps:
   1️⃣ Generate PRD (Product Requirements Document)
   2️⃣ Generate User Stories with Epics and Acceptance Criteria
   3️⃣ Generate Technical Specifications
   4️⃣ Generate Validation and Test Scenarios
   5️⃣ Generate Visual Diagrams (Workflow + Architecture)

   Input: ai-docs/0-brainstorming/session{N}.md

   Expected Outputs:
   - ai-docs/2-prds/prd{N}.md
   - ai-docs/2-user-stories/stories-{N}.md
   - ai-docs/2-specs/specs-{N}.md
   - ai-docs/2-validation/validation-{N}.md
   - ai-docs/2-diagrams/workflow-{N}.mmd
   - ai-docs/2-diagrams/architecture-{N}.mmd

   Press Enter to continue or Ctrl+C to cancel...
   ```

### Phase 1: Generate PRD

4. **Invoke /session2prd**:
   ```
   ═══════════════════════════════════════════════════════════
   📄 Step 1/5: Generating Product Requirements Document (PRD)
   ═══════════════════════════════════════════════════════════
   ```
   - Execute: `/session2prd {N}`
   - Wait for completion
   - Verify output file exists: `ai-docs/2-prds/prd{N}.md`
   - If failed, report error and exit
   - If successful: `✅ PRD generated: ai-docs/2-prds/prd{N}.md`

### Phase 2: Generate User Stories

5. **Invoke /brain2stories**:
   ```
   ═══════════════════════════════════════════════════════════
   👥 Step 2/5: Generating User Stories
   ═══════════════════════════════════════════════════════════
   Context: Using session{N}.md + prd{N}.md
   ```
   - Execute: `/brain2stories {N}`
   - Wait for completion
   - Verify output file exists: `ai-docs/2-user-stories/stories-{N}.md`
   - If failed, report error and exit
   - If successful: `✅ User Stories generated: ai-docs/2-user-stories/stories-{N}.md`

### Phase 3: Generate Technical Specs

6. **Invoke /brain2specs**:
   ```
   ═══════════════════════════════════════════════════════════
   🔧 Step 3/5: Generating Technical Specifications
   ═══════════════════════════════════════════════════════════
   Context: Using session{N}.md + prd{N}.md + stories-{N}.md
   ```
   - Execute: `/brain2specs {N}`
   - Wait for completion
   - Verify output file exists: `ai-docs/2-specs/specs-{N}.md`
   - If failed, report error and exit
   - If successful: `✅ Technical Specs generated: ai-docs/2-specs/specs-{N}.md`

### Phase 4: Generate Validation Criteria

7. **Invoke /brain2validation**:
   ```
   ═══════════════════════════════════════════════════════════
   ✓ Step 4/5: Generating Validation and Test Scenarios
   ═══════════════════════════════════════════════════════════
   Context: Using all previous documents
   ```
   - Execute: `/brain2validation {N}`
   - Wait for completion
   - Verify output file exists: `ai-docs/2-validation/validation-{N}.md`
   - If failed, report error and exit
   - If successful: `✅ Validation generated: ai-docs/2-validation/validation-{N}.md`

### Phase 5: Generate Visual Diagrams

8. **Invoke /graph**:
   ```
   ═══════════════════════════════════════════════════════════
   📊 Step 5/5: Generating Visual Diagrams
   ═══════════════════════════════════════════════════════════
   Context: Using all previous documents
   Creating: Workflow + Architecture diagrams
   ```
   - Execute: `/graph {N}`
   - Wait for completion
   - Verify output files exist:
     - `ai-docs/2-diagrams/workflow-{N}.mmd`
     - `ai-docs/2-diagrams/architecture-{N}.mmd`
   - If failed, report error and exit
   - If successful:
     ```
     ✅ Workflow diagram: ai-docs/2-diagrams/workflow-{N}.mmd
     ✅ Architecture diagram: ai-docs/2-diagrams/architecture-{N}.mmd
     ```

### Phase 6: Pipeline Completion

9. **Display completion summary**:
   ```
   ═══════════════════════════════════════════════════════════
   🎉 Planning Pipeline Complete for Session {N}
   ═══════════════════════════════════════════════════════════

   Generated Files:
   ✅ ai-docs/2-prds/prd{N}.md
   ✅ ai-docs/2-user-stories/stories-{N}.md
   ✅ ai-docs/2-specs/specs-{N}.md
   ✅ ai-docs/2-validation/validation-{N}.md
   ✅ ai-docs/2-diagrams/workflow-{N}.mmd
   ✅ ai-docs/2-diagrams/architecture-{N}.mmd

   Next Steps:
   1. Review all generated documents for accuracy
   2. Test Mermaid diagrams at https://mermaid.live/
   3. Begin implementation using specs-{N}.md as guide
   4. Use validation-{N}.md for test-driven development

   Pipeline Duration: [X minutes Y seconds]
   ```

## Error Handling

### Missing Input File
```
❌ Error: Brainstorming session {N} not found

Expected location: ai-docs/0-brainstorming/session{N}.md

Please create the brainstorming session file first, then run:
/plan {N}
```

### Missing Output Directory
```
❌ Error: Required directories missing

Missing:
- ai-docs/2-prds/
- ai-docs/2-validation/

Please create these directories first:
mkdir -p ai-docs/2-prds ai-docs/2-validation
```

### Step Failure
```
❌ Error: Step 3/5 failed

Command: /brain2specs {N}
Error: [Error message from command]

Pipeline halted. Please fix the error and re-run:
/plan {N}

Note: Already completed steps (1-2) can be skipped by manually running remaining steps:
/brain2specs {N}
/brain2validation {N}
/graph {N}
```

### Partial Completion
```
⚠️  Warning: Some files already exist

Existing files will be OVERWRITTEN:
- ai-docs/2-prds/prd{N}.md (modified 2 hours ago)
- ai-docs/2-specs/specs-{N}.md (modified 1 hour ago)

Continue? (y/N): _
```

## Progress Reporting

Throughout execution, display:
- Current step number and description
- Context being used (which files are inputs)
- Real-time status updates
- File verification after each step
- Estimated time remaining (if possible)

## Implementation Notes

### Sequential Execution
- Each command must complete before starting next
- Use command results to verify success
- Pass context forward (each step builds on previous)
- Halt pipeline if any step fails

### Context Passing
Each command receives cumulative context:
- Step 1 (PRD): session{N}.md
- Step 2 (Stories): session{N}.md + prd{N}.md
- Step 3 (Specs): session{N}.md + prd{N}.md + stories-{N}.md
- Step 4 (Validation): All previous documents
- Step 5 (Diagrams): All previous documents

### File Verification
After each step:
1. Check file exists
2. Check file is not empty (> 1KB)
3. Check file has valid markdown structure
4. Report file size for reference

### Error Recovery
If pipeline fails:
- Report which step failed
- Show error message
- Indicate which files were successfully created
- Provide instructions for manual completion
- Allow resuming from failed step

## Best Practices

- **Review Before Running**: Ensure brainstorming session is complete
- **Clean Slate**: Consider backing up existing files before overwriting
- **Iterative Refinement**: Run pipeline, review, improve brainstorming, re-run
- **Context Quality**: Better brainstorming sessions produce better outputs
- **Manual Review**: Always review generated documents for accuracy
- **Version Control**: Commit generated files to git for tracking changes

## Expected Duration

Approximate time per step (varies by complexity):
- Step 1 (PRD): 2-3 minutes
- Step 2 (Stories): 3-5 minutes
- Step 3 (Specs): 5-8 minutes
- Step 4 (Validation): 4-6 minutes
- Step 5 (Diagrams): 3-4 minutes

**Total Pipeline Duration**: ~17-26 minutes

## Success Criteria

Pipeline is successful when:
1. All 6 files are generated
2. Each file has valid markdown structure
3. Files have appropriate metadata headers
4. Content is comprehensive and detailed
5. Diagrams render correctly in Mermaid
6. Traceability maintained across documents
7. No errors reported during execution

## Related Commands

- `/session2prd <N>` - Generate PRD only
- `/brain2stories <N>` - Generate User Stories only
- `/brain2specs <N>` - Generate Technical Specs only
- `/brain2validation <N>` - Generate Validation only
- `/graph <N>` - Generate Diagrams only
- `/update_completion <N>` - Update task completion status

## Important Notes

- This is a long-running command (15-30 minutes)
- Do not interrupt execution mid-pipeline
- Each step overwrites existing files
- Review all outputs after completion
- Consider running individual commands for iteration
- Use this for initial generation or full regeneration
- For updates to specific documents, use individual commands
