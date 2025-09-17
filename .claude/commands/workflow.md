# /workflow - Execute AI-Docs Workflow

## Usage
`/workflow <workflow_number> <session_number>`

## Description
Executes a parameterized workflow from the ai-docs/5-workflows/ directory, substituting variables and running all workflow steps in sequence.

## Arguments
- `workflow_number`: The workflow file number (e.g., 1 for workflow1.md)
- `session_number`: The session number to process (substitutes $SESSION_NUMBER variable)

## Examples
- `/workflow 1 3` - Executes workflow1.md on session 3
- `/workflow 2 5` - Executes workflow2.md on session 5

## Task Instructions

When this command is invoked:

1. **Locate the workflow file**: Look for `ai-docs/5-workflows/workflow{workflow_number}.md`

2. **Parse workflow structure**:
   - Read the workflow file completely
   - Identify the Variables section and variable definitions
   - Parse the Workflow Steps section for execution sequence
   - Extract the YAML execution sequence if present

3. **Substitute variables**:
   - Replace `$SESSION_NUMBER` with the provided session number
   - Apply substitutions to all file paths, commands, and references
   - Validate that all input files exist before proceeding

4. **Execute workflow steps in sequence**:
   - For each step in the workflow:
     - **Slash commands**: Execute directly (e.g., `/brain2specs 3`)
     - **Agent calls**: Use the Task tool to invoke the specified agent
     - **Tool execution**: Run specified tools or scripts
   - Respect step dependencies and execution order
   - Provide progress updates for each step

5. **Variable substitution examples**:
   ```
   Original: 0-brainstorming/session$SESSION_NUMBER.md
   With session_number=3: 0-brainstorming/session3.md

   Original: /brain2specs $SESSION_NUMBER
   With session_number=3: /brain2specs 3

   Original: 2-specs/specs$SESSION_NUMBER-simplified.md
   With session_number=3: 2-specs/specs3-simplified.md
   ```

6. **Step execution logic**:
   ```
   For step with command: Execute the slash command directly
   For step with agent: Use Task tool to invoke the agent with proper inputs
   For step with tool: Execute the specified tool with arguments
   ```

7. **Error handling**:
   - If input files don't exist, report error and abort
   - If a step fails, provide clear error message and stop execution
   - If workflow file doesn't exist, report error clearly

8. **Success reporting**:
   - Report completion of each step
   - List all generated output files
   - Confirm workflow execution completion
   - Provide summary of created artifacts

## Workflow Step Execution Patterns

### Pattern 1: Slash Command Execution
```yaml
steps:
  1. generate_spec:
     - Run: /brain2specs $SESSION_NUMBER
```
**Action**: Execute the slash command directly

### Pattern 2: Agent Invocation
```yaml
steps:
  2. simplify_spec:
     - Agent: spec-simplification-agent
     - Input: ["session$SESSION_NUMBER.md", "specs$SESSION_NUMBER.md"]
```
**Action**: Use Task tool to invoke the agent with specified inputs

### Pattern 3: Tool Execution
```yaml
steps:
  3. validate:
     - Tool: update_completion
     - Args: $SESSION_NUMBER
```
**Action**: Execute the specified tool with provided arguments

## Important Notes

- Always validate input files exist before starting execution
- Maintain execution order as specified in workflow
- Provide clear progress updates for each step
- Report all generated artifacts upon completion
- Handle errors gracefully with clear messaging
- Respect the Variables section for proper substitution

## Example Execution Flow

For `/workflow 1 3`:

1. **Load**: Read `ai-docs/5-workflows/workflow1.md`
2. **Parse**: Extract steps and variable definitions
3. **Substitute**: Replace `$SESSION_NUMBER` with `3` throughout
4. **Validate**: Ensure `ai-docs/0-brainstorming/session3.md` exists
5. **Execute Step 1**: Run `/brain2specs 3`
6. **Execute Step 2**: Invoke spec-simplification-agent with session3.md and specs3.md
7. **Execute Step 3**: Run `/session2prd 3`
8. **Report**: List all created files and confirm completion