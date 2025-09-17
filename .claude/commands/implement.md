# Command: implement.md
# Description: Implements a specific task from a specification document and updates completion status
# Usage: implement <task_number>

TASK_NUMBER="$1"

if [ -z "$TASK_NUMBER" ]; then
    echo "Error: Please provide a task number"
    echo "Usage: implement <task_number>"
    exit 1
fi

echo "Implementing Task $TASK_NUMBER..."

## Instructions for Claude Code Agent

You are tasked with implementing a specific task from a specification document. Follow these steps:

### 1. Locate and Analyze the Task
- Find the specification document containing Task $TASK_NUMBER
- Identify the atomic task and all its sub-atomic tasks
- Understand the requirements and acceptance criteria
- Note any dependencies or prerequisites

### 2. Implementation Process
- Implement each sub-atomic task within the atomic task group
- Follow best practices for code quality and documentation
- Ensure all requirements are met according to the specification
- Test functionality as you implement each sub-atomic task

### 3. Task Completion Criteria
- Complete ALL sub-atomic tasks within the specified task number
- Verify that each sub-atomic task meets its acceptance criteria
- Ensure proper integration with existing codebase
- Validate that no existing functionality is broken

### 4. Status Update Requirements
- Once ALL sub-atomic tasks are completed, update the specification document
- Change all sub-atomic task statuses to ✅ (completed)
- Change the atomic task status to ✅ (completed)
- Update any related task dependencies if applicable

### 5. Completion Rules
- **STOP** only when all atomic and sub-atomic tasks for Task $TASK_NUMBER are 100% completed
- Do not proceed to other tasks unless explicitly instructed
- Provide a summary of what was implemented
- Confirm all status updates have been applied

### 6. Output Requirements
Provide a completion report including:
- List of all sub-atomic tasks completed
- Files created or modified during implementation
- Any issues encountered and how they were resolved
- Confirmation that Task $TASK_NUMBER is fully completed
- Updated completion status in the specification document

### Error Handling
- If Task $TASK_NUMBER doesn't exist, report the error clearly
- If dependencies are missing, identify and request clarification
- If implementation cannot be completed, document the blockers

echo "Task $TASK_NUMBER implementation completed successfully"