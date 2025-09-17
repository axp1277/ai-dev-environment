# Workflow Creation Guidelines and Best Practices

## Overview
This document provides comprehensive guidelines for creating effective workflows within the ai-docs framework, ensuring consistency, reliability, and maintainability across all workflow implementations.

## Workflow Creation Process

### 1. Planning Phase
Before creating a workflow:
- **Define clear purpose**: What specific outcome does this workflow achieve?
- **Identify inputs and outputs**: What files are required and what will be generated?
- **Map dependencies**: Which steps must happen in sequence vs. parallel?
- **Consider reusability**: How can this workflow be parameterized for different sessions?

### 2. Structure Design
Follow the standard workflow template:
```markdown
# Workflow N: [Descriptive Name]

## Variables
- `$SESSION_NUMBER` - Session identifier
- `$CUSTOM_VAR` - Any additional variables

## Overview
[Clear, concise description]

## Prerequisites
[Required files, agents, conditions]

## Workflow Steps
[Detailed step descriptions with variables]

## Execution Sequence
[YAML format with variable usage]

## Expected Outputs
[Complete list of generated files]

## Success Criteria
[Validation checkboxes]
```

### 3. Variable Strategy
**Always use variables for**:
- Session numbers (`$SESSION_NUMBER`)
- File paths and filenames
- Command arguments
- Output destinations

**Variable naming conventions**:
- Use UPPERCASE with underscores: `$SESSION_NUMBER`
- Be descriptive: `$TARGET_LANGUAGE` not `$LANG`
- Include type hints in documentation: `$SESSION_NUMBER` - The session number to process (e.g., 2)

## Step Design Patterns

### Pattern 1: Command Execution
```yaml
generate_spec:
  command: "/brain2specs $SESSION_NUMBER"
  creates: "2-specs/specs$SESSION_NUMBER.md"
```

### Pattern 2: Agent Invocation
```yaml
simplify_spec:
  agent: "spec-simplification-agent"
  input:
    - "0-brainstorming/session$SESSION_NUMBER.md"
    - "2-specs/specs$SESSION_NUMBER.md"
  output: "2-specs/specs$SESSION_NUMBER-simplified.md"
```

### Pattern 3: Tool Execution
```yaml
update_status:
  tool: "update_completion"
  args: "$SESSION_NUMBER"
```

## Best Practices

### Workflow Design
1. **Single Responsibility Principle**
   - Each workflow should have one clear, focused purpose
   - Avoid creating "mega-workflows" that try to do everything
   - Split complex processes into multiple related workflows

2. **Modular Architecture**
   - Design steps to be independently executable
   - Each step should have clear inputs and outputs
   - Avoid hidden dependencies between steps

3. **Clear Naming**
   - Use descriptive workflow names: `complete-session-processing` not `workflow1`
   - Step names should indicate action: `generate_spec`, `validate_output`
   - File outputs should follow naming conventions: `specs$SESSION_NUMBER-simplified.md`

4. **Variable Usage**
   - Use variables for ALL file paths to ensure reusability
   - Include variable definitions section at the top
   - Provide examples of variable substitution
   - Document variable types and expected formats

### Error Prevention
1. **Input Validation**
   - Always validate required files exist before starting
   - Check for proper file formats and structure
   - Verify agent availability before execution

2. **Dependency Management**
   - Make step dependencies explicit in YAML
   - Use `depends_on` for sequential requirements
   - Consider `parallel: true` for independent steps

3. **Output Verification**
   - Include success criteria for each step
   - Validate output files are created correctly
   - Check file content quality where possible

### Documentation Standards
1. **Comprehensive Descriptions**
   - Explain what each step accomplishes
   - Document why the step is necessary
   - Include context about when to use this workflow

2. **Usage Examples**
   - Provide concrete examples: `/workflow 1 3`
   - Show expected file outputs
   - Document common error scenarios

3. **Prerequisites**
   - List all required files and their locations
   - Specify agent dependencies
   - Document any environmental requirements

## Quality Checklist

Before finalizing a workflow, verify:

### Structure
- [ ] Variables section includes all parameterized values
- [ ] Overview clearly explains workflow purpose
- [ ] Prerequisites list all requirements
- [ ] Steps are numbered and well-described
- [ ] YAML execution sequence is valid and complete
- [ ] Expected outputs list all generated files
- [ ] Success criteria are measurable and specific

### Variables
- [ ] All file paths use variables where appropriate
- [ ] Variable names follow naming conventions
- [ ] Variable documentation includes examples
- [ ] Commands use variables for arguments
- [ ] No hard-coded session numbers or file names

### Dependencies
- [ ] Step execution order is logical
- [ ] Dependencies are explicitly declared
- [ ] No circular dependencies exist
- [ ] Parallel steps are properly identified

### Documentation
- [ ] Clear, jargon-free language
- [ ] Complete prerequisite listing
- [ ] Concrete usage examples provided
- [ ] Error scenarios documented
- [ ] Integration with other workflows explained

## Common Pitfalls to Avoid

### 1. Hard-coded Values
```yaml
# BAD - Hard-coded session number
input: "0-brainstorming/session2.md"

# GOOD - Parameterized with variable
input: "0-brainstorming/session$SESSION_NUMBER.md"
```

### 2. Missing Dependencies
```yaml
# BAD - No dependency specified when order matters
steps:
  1. generate_spec: ...
  2. simplify_spec: ...  # Needs spec from step 1

# GOOD - Explicit dependency
steps:
  1. generate_spec: ...
  2. simplify_spec:
     depends_on: "generate_spec"
```

### 3. Unclear Step Names
```yaml
# BAD - Vague names
steps:
  1. step1: ...
  2. process: ...

# GOOD - Descriptive names
steps:
  1. generate_specification: ...
  2. review_for_scope_creep: ...
```

### 4. Missing Validation
```yaml
# BAD - No validation
steps:
  1. generate_spec:
     command: "/brain2specs $SESSION_NUMBER"

# GOOD - Input validation included
prerequisites:
  - "File 0-brainstorming/session$SESSION_NUMBER.md must exist"
```

## Integration Guidelines

### With Existing Systems
- **Commands**: Workflows should integrate with existing slash commands
- **Agents**: Use established agent names and calling conventions
- **File Structure**: Follow ai-docs directory organization
- **Naming**: Maintain consistency with existing patterns

### Version Control
- **Workflow Files**: Track changes to workflow logic
- **Backwards Compatibility**: Maintain compatibility when possible
- **Breaking Changes**: Document clearly with migration guidance
- **Testing**: Validate workflows before committing changes

### Team Collaboration
- **Documentation**: Keep workflows well-documented for team usage
- **Standardization**: Follow established conventions consistently
- **Knowledge Sharing**: Include rationale for design decisions
- **Maintenance**: Plan for ongoing workflow updates and improvements

## Advanced Patterns

### Conditional Execution
```yaml
validate_prd:
  condition: "file_exists(1-prds/prd$SESSION_NUMBER.md)"
  agent: "prd-validator"
  input: "1-prds/prd$SESSION_NUMBER.md"
```

### Loop Constructs
```yaml
process_all_sessions:
  for_each: "$SESSION_LIST"
  steps:
    - generate_spec: "/brain2specs $CURRENT_SESSION"
```

### Error Recovery
```yaml
generate_spec:
  command: "/brain2specs $SESSION_NUMBER"
  retry: 3
  fallback: "manual_spec_creation"
```

## Conclusion

Well-designed workflows are the backbone of the ai-docs framework. By following these guidelines, you'll create reliable, maintainable, and reusable workflows that enhance productivity and ensure consistent results across all AI-assisted development tasks.

Remember: workflows should make complex processes simple, not add unnecessary complexity. Focus on clarity, reliability, and user experience in every workflow you create.