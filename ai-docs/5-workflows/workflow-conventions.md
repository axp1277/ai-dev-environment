# Workflow Syntax and Conventions for Agent Coordination

## Overview
This document defines the standardized syntax and conventions for creating workflows that coordinate multiple AI agents, prompts, and tools within the ai-docs framework.

## Workflow File Structure

### Basic Template
```markdown
# Workflow N: [Workflow Name]

## Variables
- `$SESSION_NUMBER` - The session number to process (e.g., 2 for session2.md)
- `$WORKFLOW_NUMBER` - The current workflow number (auto-set)
- `$CUSTOM_VAR` - Any additional custom variables needed

## Overview
[Brief description of what this workflow accomplishes]

## Prerequisites
- [Required files, agents, or conditions]

## Workflow Steps
[Detailed step-by-step process using variables]

## Execution Sequence
[YAML or structured format showing the flow with variables]

## Expected Outputs
[List of all files and artifacts created using variable notation]

## Success Criteria
[Checkboxes for validation using variable references]
```

## Workflow Syntax Conventions

### Step Definition Format
```yaml
step_name:
  agent: "agent-name"
  input: "file-path-with-variables" | ["file1", "file2"]
  output: "output-path-with-variables"
  command: "/command-name $VARIABLE" (optional)
  depends_on: "previous_step_name" (optional)
  parallel: true|false (default: false)
```

### Variable Usage Standards
- **$SESSION_NUMBER**: Primary session identifier (e.g., 2 for session2.md)
- **$WORKFLOW_NUMBER**: Current workflow number (auto-set by executor)
- **File path patterns**: Use variables in all file paths for reusability
- **Command patterns**: Include variables in command arguments
- **Custom variables**: Define additional variables as needed

### Variable Substitution Examples
```yaml
# Original with variables
input: "0-brainstorming/session$SESSION_NUMBER.md"
command: "/brain2specs $SESSION_NUMBER"
output: "2-specs/specs$SESSION_NUMBER-simplified.md"

# After substitution with SESSION_NUMBER=3
input: "0-brainstorming/session3.md"
command: "/brain2specs 3"
output: "2-specs/specs3-simplified.md"
```

### Agent Types
- **Command Agents**: Triggered via slash commands (`/brain2specs`, `/session2prd`)
- **Direct Agents**: Called directly (`spec-simplifier-agent`, `session2notes-agent`)
- **Tool Agents**: Execute tools or scripts
- **Human Agents**: Require human intervention

### Input/Output Conventions
- Use relative paths from project root
- Follow naming convention: `folder/typeN.md` (e.g., `0-brainstorming/session2.md`)
- Multiple inputs as array: `["file1.md", "file2.md"]`
- Optional outputs marked with `(optional)`

### Dependency Management
- `depends_on`: Sequential execution (step waits for dependency)
- `parallel: true`: Steps can run concurrently
- No dependency specified: Can run at any time

## Standard Workflow Patterns

### Pattern 1: Linear Sequential
```yaml
steps:
  1. step_a:
     agent: "agent-1"
     input: "source.md"
     output: "intermediate.md"

  2. step_b:
     agent: "agent-2"
     input: "intermediate.md"
     output: "final.md"
     depends_on: "step_a"
```

### Pattern 2: Parallel Processing
```yaml
steps:
  1. step_a:
     agent: "agent-1"
     input: "source.md"
     output: "output-a.md"
     parallel: true

  2. step_b:
     agent: "agent-2"
     input: "source.md"
     output: "output-b.md"
     parallel: true
```

### Pattern 3: Fan-Out then Merge
```yaml
steps:
  1. generate_specs:
     agent: "brain2specs-agent"
     input: "session.md"
     output: "specs.md"

  2. generate_prd:
     agent: "brain2prd-agent"
     input: "session.md"
     output: "prd.md"
     parallel: true
     depends_on: "generate_specs"

  3. validate:
     agent: "spec-simplifier-agent"
     input: ["session.md", "specs.md"]
     output: "specs-simplified.md"
     depends_on: ["generate_specs", "generate_prd"]
```

## Naming Conventions

### Workflow Files
- `workflow1.md`, `workflow2.md`, etc.
- Use descriptive names: `workflow-complete-processing.md`
- Special workflows: `workflow-conventions.md`, `workflow-templates.md`

### Step Names
- Use lowercase with underscores: `generate_spec`, `simplify_output`
- Be descriptive: `review_for_scope_creep`, `validate_against_original`
- Avoid abbreviations unless widely understood

### Agent References
- Use exact agent names: `brain2specs-agent`, `spec-simplifier-agent`
- Command format: `/command-name arguments`
- Tool format: `tool-name --options`

## Error Handling and Validation

### Required Validation Checks
```yaml
validation:
  pre_execution:
    - check_input_files_exist
    - verify_agent_availability
    - validate_output_paths

  post_execution:
    - verify_all_outputs_created
    - check_output_file_validity
    - validate_against_success_criteria
```

### Error Recovery Patterns
- **Retry**: Attempt step again with same inputs
- **Fallback**: Use alternative agent or approach
- **Skip**: Continue workflow without this step (if marked optional)
- **Abort**: Stop entire workflow execution

## Best Practices

### Workflow Design
1. **Single Responsibility**: Each workflow should have one clear purpose
2. **Modular Steps**: Each step should be independently executable
3. **Clear Dependencies**: Make step relationships explicit
4. **Descriptive Naming**: Use self-documenting names for steps and outputs
5. **Validation Points**: Include success criteria for each step
6. **Variable Usage**: Use variables for all file paths and commands to ensure reusability
7. **Input Validation**: Always validate required files exist before execution

### Performance Optimization
1. **Parallel Execution**: Use `parallel: true` when steps are independent
2. **Minimal Dependencies**: Only specify dependencies when truly required
3. **Efficient Ordering**: Place quick steps early, expensive steps late
4. **Resource Management**: Consider agent capacity and tool limitations

### Documentation Requirements
1. **Overview**: Clear description of workflow purpose
2. **Prerequisites**: All requirements for execution
3. **Expected Outputs**: Complete list of generated artifacts
4. **Success Criteria**: Measurable validation checkpoints
5. **Usage Examples**: Real-world execution scenarios

## Workflow Execution Models

### Manual Execution
Human executes each step manually following the workflow document.

### Semi-Automated
Some steps automated (slash commands), others manual (agent calls).

### Future: Fully Automated
Workflow engine reads YAML and executes all steps automatically.

## Version Control
- Include version number in workflow metadata
- Track changes to workflow logic
- Maintain backwards compatibility when possible
- Document breaking changes clearly