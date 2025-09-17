# Command: spec-task-review.md
# Description: Reviews a specific task in a spec document and provides implementation understanding and options
# Usage: spec-task-review <spec_number> <task_number>

SPEC_FILE="ai-docs/3-specs/specs-$1.md"
TASK_NUMBER="$2"

echo "Reviewing task $TASK_NUMBER from specification document $SPEC_FILE..."

Review the specified task (task number $TASK_NUMBER) from the specification document located at $SPEC_FILE.

Your task is to:
1. Find and extract the task with the specified number in the spec document
2. Provide a concise summary of what the task entails, showing your understanding
3. Present 3 distinct options for how to implement the task, considering:
   - Technical approach
   - Required technologies/frameworks
   - Implementation complexity
   - Advantages and disadvantages
4. Recommend the best option out of the 3, with clear justification
5. Outline high-level steps needed to implement the recommended option

Do NOT write any code or begin implementation. Focus exclusively on demonstrating your understanding of the task and presenting implementation strategies.

If the task is not found in the spec document, clearly state this and suggest possible reasons why.