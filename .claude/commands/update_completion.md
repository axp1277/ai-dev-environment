# Update Completion Status Command

## Command
`/update_completion <spec_number>`

## Description
Updates the completion statuses of tasks in a specification document with appropriate emoji indicators based on task completion levels.

## Arguments
- `spec_number`: The specification document number (e.g., 001, 002, etc.)

## Target File
`ai-docs/specs/spec-<spec_number>.md`

## Instructions for Claude Code Agent

You are tasked with updating the completion statuses in a specification document. Follow these rules:

### Task Classification
- **Sub-atomic tasks**: The smallest, indivisible units of work
- **Atomic tasks**: Groups of related sub-atomic tasks

### Status Update Rules

#### For Sub-atomic Tasks:
- ✅ **Completed**: Use green checkmark emoji for finished tasks
- 🔄 **In Progress**: Use cycle emoji for tasks currently being worked on  
- ⭕ **Not Started**: Use red circle emoji for tasks not yet begun

#### For Atomic Tasks:
- ✅ **All Complete**: Use green checkmark emoji when ALL sub-atomic tasks within the atomic task are completed
- 🚧 **Partially Complete**: Use construction emoji when SOME but not all sub-atomic tasks are completed
- ⭕ **Not Started**: Use red circle emoji when NO sub-atomic tasks have been started

### Process Steps:

1. **Read the specification document** at `ai-docs/specs/spec-$ARGUMENTS.md`

2. **Analyze task hierarchy**:
   - Identify atomic tasks (main task groups)
   - Identify sub-atomic tasks within each atomic task
   - Determine current completion status of each task

3. **Update sub-atomic task statuses**:
   - Review each sub-atomic task
   - Update with appropriate emoji based on completion level
   - Ensure consistency in formatting

4. **Update atomic task statuses**:
   - Count completed vs total sub-atomic tasks for each atomic task
   - Apply the appropriate emoji:
     - If 100% of sub-atomic tasks complete → ✅
     - If 0% of sub-atomic tasks complete → ⭕
     - If between 1-99% of sub-atomic tasks complete → 🚧

5. **Preserve document structure**:
   - Maintain all existing formatting
   - Keep all content intact except for status emojis
   - Ensure proper markdown formatting

6. **Save the updated document** back to the same location

### Example Status Patterns:

```markdown
## ✅ Atomic Task: Database Setup
- ✅ Sub-atomic: Create database schema
- ✅ Sub-atomic: Set up connection pooling
- ✅ Sub-atomic: Configure backup procedures

## 🚧 Atomic Task: API Development  
- ✅ Sub-atomic: Design REST endpoints
- 🔄 Sub-atomic: Implement authentication
- ⭕ Sub-atomic: Add rate limiting
- ⭕ Sub-atomic: Write API documentation

## ⭕ Atomic Task: Frontend Implementation
- ⭕ Sub-atomic: Create component library
- ⭕ Sub-atomic: Build user interface
- ⭕ Sub-atomic: Implement state management
```

### Error Handling:
- If the specification file doesn't exist, report the error clearly
- If the file format is unexpected, document the issues found
- If unable to determine task hierarchy, ask for clarification

### Output:
Provide a summary of changes made, including:
- Number of atomic tasks updated
- Number of sub-atomic tasks updated  
- Overall completion percentage of the specification
- Any issues or ambiguities encountered