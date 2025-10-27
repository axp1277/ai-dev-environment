# Task 6.0: Command Generation Logic

This document specifies the logic for generating /bug and /feature commands from processed transcript segments.

## 6.1: Output Structure for Multiple Command Lines

### Basic Structure

```
/bug [description]
/feature [description]
/bug [description]
/feature [description]
```

### Formatting Rules

**Rule 1: One Command Per Line**
- Each command on a separate line
- No blank lines between commands
- No line numbers or bullets

**Rule 2: Command Prefix**
- Start each line with `/bug` or `/feature`
- Single space after command prefix
- Command and description on same line

**Rule 3: No Additional Commentary**
- Only output the commands
- No explanatory text between commands
- No "Command List:" header or similar

**Rule 4: Clean Output**
- No markdown formatting around commands
- No code blocks
- Raw command list only

### Valid Output Examples

**Example 1: Multiple Commands**
```
/bug Login page displays blank screen after credential submission preventing user access.
/feature Add OAuth authentication support for Google and GitHub to improve sign-in experience.
/bug CSV export times out with database error when generating large reports.
```

**Example 2: Single Command**
```
/feature Implement dark mode toggle in application settings for improved accessibility.
```

**Example 3: No Commands**
```
No actionable bugs or features were identified in the meeting transcript. The discussion focused on project status updates and timeline planning.
```

### Invalid Output Examples

**❌ Example 1: Extra Formatting**
```
Command List:
1. /bug Login is broken
2. /feature Add dark mode
```

**❌ Example 2: Blank Lines**
```
/bug Login is broken

/feature Add dark mode
```

**❌ Example 3: Commentary**
```
/bug Login is broken
(This is urgent according to the client)
/feature Add dark mode
```

## 6.2: Formatting Template for /bug Commands

### Template

```
/bug [Component] [Problem] [Error/Symptom]. [User Impact]. [Priority if mentioned].
```

### Components

1. **Component**: What part of the system (e.g., "Login page", "CSV export", "API endpoint")
2. **Problem**: What's wrong (e.g., "fails", "crashes", "returns error")
3. **Error/Symptom**: Observable issue (e.g., "'timeout' error", "blank screen", "incorrect data")
4. **User Impact**: Who/what is affected (e.g., "preventing user access", "blocking reports")
5. **Priority**: Urgency if mentioned (e.g., "Client reported as critical")

### Examples by Complexity

**Simple Bug**
```
/bug Search functionality returns no results when queries are entered.
```

**Bug with Error**
```
/bug User export fails with 'Database connection timeout' error when generating CSV files.
```

**Bug with Context**
```
/bug Payment processing returns 'Transaction declined' for valid credit cards in production. Blocking customer transactions. Client reported as critical.
```

**Performance Bug**
```
/bug Analytics dashboard load time increased from 2 seconds to 45 seconds after last deployment. Performance regression.
```

## 6.3: Formatting Template for /feature Commands

### Template

```
/feature [Action Verb] [Feature/Capability] [for/to Purpose]. [User Value]. [Additional Context].
```

### Components

1. **Action Verb**: Start with "Add", "Implement", "Create", "Enable", "Integrate"
2. **Feature/Capability**: What's being requested
3. **Purpose**: "for [users]" or "to [accomplish]"
4. **User Value**: Why it matters, benefit delivered
5. **Additional Context**: Technical preferences, constraints, requirements

### Examples by Complexity

**Simple Feature**
```
/feature Add dark mode option to application settings for improved user experience and accessibility.
```

**Feature with User Story**
```
/feature Enable users to save and share custom filter preferences to streamline repeated searches and improve workflow efficiency.
```

**Integration Feature**
```
/feature Integrate Slack notifications for system alerts and user activity with configurable user preferences to improve team communication and awareness.
```

**Complex Feature**
```
/feature Create customizable reporting module supporting user-defined columns, filters, grouping, and multiple export formats with template saving and team sharing capabilities.
```

## 6.4: Command Ordering Logic

### Primary Ordering: Chronological

**Default Rule**: Preserve the order issues were discussed in the meeting

**Rationale**:
- Maintains meeting context
- Preserves discussion flow
- Client priority often correlates with mention order
- Most natural for review

**Example**:
```
Transcript order: Bug A, Feature X, Bug B, Feature Y
Output order: /bug A, /feature X, /bug B, /feature Y
```

### Alternative Ordering (NOT USED)

**Not by Type**: Don't group all bugs then all features
```
❌ Wrong: /bug A, /bug B, /feature X, /feature Y
✓ Correct: /bug A, /feature X, /bug B, /feature Y (chronological)
```

**Not by Priority**: Don't reorder by urgency
```
❌ Wrong: Critical bugs first, then high, then features
✓ Correct: Order discussed in meeting
```

**Not Alphabetically**: Don't sort by component name
```
❌ Wrong: Alphabetical by feature name
✓ Correct: Order discussed in meeting
```

### Edge Cases

**Case 1: Related Issues Discussed Non-Contiguously**

```
Transcript:
- Login bug mentioned (minute 5)
- Feature discussion (minutes 6-10)
- More login bug details (minute 11)

Output:
Merge login bug context into single command at first mention position
```

**Case 2: Same Issue Mentioned Multiple Times**

```
Transcript:
- Export bug mentioned briefly (minute 3)
- Other discussions (minutes 4-8)
- Export bug discussed in detail (minute 9)

Output:
Single /bug command with complete context at first mention position
```

**Case 3: Clarification Adds Classification Info**

```
Transcript:
Client: "The dashboard is slow" (could be bug or feature)
Developer: "How slow?"
Client: "It used to be instant, now takes 30 seconds" (regression → bug)

Output:
/bug at the position of first mention, with clarification context
```

## 6.5: AI Coder Execution Instructions

### Instruction Format

Included in meet2issues.md as guidance for the AI coder receiving the command list.

### Execution Sequence

```
1. Receive command list from meet2issues HOP
2. For each line in order (top to bottom):
   a. If line starts with /bug:
      - Execute bug.md command with description as $ARGUMENTS
      - Bug command creates plan in specs/*.md
      - Wait for completion
   b. If line starts with /feature:
      - Execute feature.md command with description as $ARGUMENTS
      - Feature command creates plan in ai-docs/2-features/*.md
      - Wait for completion
3. Report completion of all commands
```

### Execution Rules

**Rule 1: Sequential Execution**
- Execute commands in order (don't parallelize)
- Complete each command before starting next
- Maintain order for dependency management

**Rule 2: No Skipping**
- Execute every command in the list
- Don't skip commands that seem similar
- Don't combine multiple commands

**Rule 3: Error Handling**
- If a command fails, report the error
- Don't silently skip failed commands
- Ask for guidance if command is unclear

**Rule 4: Verification**
- After all commands executed, verify all output files created
- Check specs/*.md for bug plans
- Check ai-docs/2-features/*.md for feature plans
- Report count: "Executed X bugs and Y features"

### Example Execution Flow

**Input Command List**:
```
/bug Login page shows blank screen after credential submission.
/feature Add OAuth support for Google and GitHub.
/bug CSV export times out with database error.
```

**AI Coder Actions**:
```
Step 1: Execute /bug command
  → Creates specs/fix-login-blank-screen.md
  → Status: ✓ Complete

Step 2: Execute /feature command
  → Creates ai-docs/2-features/oauth-authentication.md
  → Status: ✓ Complete

Step 3: Execute /bug command
  → Creates specs/fix-csv-export-timeout.md
  → Status: ✓ Complete

Report: Successfully executed 2 bugs and 1 feature. Created 3 plan documents.
```

## Integration with meet2issues.md

All command generation logic is implemented in meet2issues.md through:

1. **Command Generation Format** section - Templates and formatting
2. **Line-by-Line Command Structure** section - Output structure and ordering
3. **Instructions for AI Coder** section - Execution sequence
4. **Example Complete Workflow** section - End-to-end demonstration

## Output Quality Checklist

Before outputting final command list, verify:

- [ ] One command per line (no blank lines)
- [ ] No additional commentary or formatting
- [ ] Commands in chronological order from transcript
- [ ] Each command is complete and self-contained
- [ ] /bug commands follow bug template
- [ ] /feature commands follow feature template
- [ ] No duplicate commands for same issue
- [ ] All actionable items from transcript represented
- [ ] Descriptions include sufficient context
- [ ] Commands are ready for immediate execution by AI coder
