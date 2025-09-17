# Playbook: Execute an AI-Docs Workflow

## Purpose
Coordinate multi-step workflows defined in `ai-docs/5-workflows/` by substituting variables and running each step with any AI assistant or automation tool.

## Inputs
- Workflow definition: `ai-docs/5-workflows/workflow<workflow_number>.md`
- Optional variables declared at the top of the workflow file (e.g., `$SESSION_NUMBER`).

## Steps
1. Open the workflow file that matches `<workflow_number>` and read the Variables, Workflow Steps, and Execution Sequence sections.
2. Capture the variable values you intend to use (for example, set `$SESSION_NUMBER = 3`).
3. For each step, perform the described action manually or via your assistant:
   - When a step references a prompt, open the cited prompt file and feed the indicated inputs.
   - When a step references a tool or script, run the command locally if available, or replicate the behaviour within your assistant.
   - When a step references another playbook, follow that playbook before proceeding.
4. Record outputs as you go, storing files at the paths listed in the workflow.
5. After completing all steps, verify that every expected output listed in the workflow exists and satisfies the success criteria.

## Tips
- Use find/replace for variables such as `$SESSION_NUMBER` to avoid mistakes when copying file paths.
- If a workflow references a capability your assistant cannot run automatically, treat the instruction as a manual checklist.
- Document any deviations or errors in a notes section at the end of the workflow file for future runs.

## Outputs
- Artifacts enumerated in the workflow’s “Expected Outputs” section.
