# Meet-to-Issues: Extract Bugs and Features from Meeting Transcripts

This is a Higher-Order Prompt (HOP) that processes Google Meet transcripts from client-developer meetings and automatically classifies conversation segments into actionable bugs and features. The workflow generates individual `/bug` and `/feature` commands for each identified item, enabling systematic implementation through a command-driven approach.

## Purpose

Transform unstructured meeting transcripts into structured, actionable commands that can be executed by AI coders to:
- Document bugs that need to be fixed
- Document features that need to be implemented
- Maintain chronological order of discussion
- Preserve full context from the meeting

## Input Requirements

### Transcript Location
- Transcripts must be stored in: `ai-docs/0-meetings/`
- File format: `.md`
- Naming convention: `transcript<number>.md` (e.g., `transcript7.md`, `transcript12.md`)

### Expected Transcript Format
The transcript should contain:
- **Plain text** or **formatted text** with timestamps
- **Speaker labels** (e.g., "Client:", "Developer:", "Andrea:", etc.)
- **Chronological conversation flow**
- May include system messages (joins, leaves) - these will be filtered out

### Example Input Format
```
Client: The login page is broken. Users can't sign in.
Developer: What error are they seeing?
Client: It just shows a blank screen after they submit credentials.

Client: Also, we'd like to add OAuth support for Google and GitHub.
Developer: That makes sense. Anything else?
Client: Yes, the dashboard loads too slowly. It used to be faster.
```

## Classification Logic

### Bug Identification Criteria
Classify a conversation segment as a **BUG** if it contains:

1. **Error Reports**: Mentions of errors, exceptions, crashes, or failures
   - Keywords: "error", "broken", "not working", "fails", "crash", "exception", "blank screen"

2. **Unexpected Behavior**: Descriptions of actual vs expected behavior mismatch
   - Keywords: "should be", "expected", "instead", "wrong", "incorrect", "doesn't work"

3. **Defects**: Issues with existing functionality
   - Keywords: "regression", "used to work", "stopped working", "defect", "bug"

4. **Performance Regressions**: Slow response times that were previously faster
   - Keywords: "slow", "used to be faster", "hanging", "timeout", "slower than before"

5. **Data Issues**: Lost data, corrupted files, inconsistent state
   - Keywords: "lost data", "corrupted", "missing data", "inconsistent"

### Feature Identification Criteria
Classify a conversation segment as a **FEATURE** if it contains:

1. **Enhancement Requests**: Requests for new functionality or improvements
   - Keywords: "add", "new feature", "enhancement", "improve", "could we", "would like to"

2. **User Stories**: Descriptions of user needs and desired outcomes
   - Patterns: "users want to", "we need to", "it would be nice if", "can we"

3. **Capability Additions**: Requests to add something that doesn't exist
   - Keywords: "implement", "create", "build", "develop", "integrate", "support for"

4. **Optimization Requests**: Making existing functionality better (not fixing regressions)
   - Keywords: "optimize", "better", "make it faster", "easier", "streamline", "improve"

5. **New Integrations**: Connecting to external systems or services
   - Keywords: "integrate with", "connect to", "support for", "compatibility with"

### Classification Decision Rules

1. **Priority Rule**: If a segment explicitly mentions "broken", "error", or "not working" → classify as Bug
2. **Default Rule**: If unclear whether bug or feature → classify as Feature
3. **Split Rule**: If segment contains BOTH bug and feature aspects → create separate commands
4. **Context Rule**: Use surrounding conversation for classification hints
5. **Regression Rule**: If mentions "used to work" or "was faster before" → classify as Bug

## Command Generation Format

### Output Structure
Generate one command per line in the following format:

```
/bug [Complete bug description with full context from transcript]
/feature [Complete feature description with full context from transcript]
```

### Description Requirements
Each command description must include:
- **Clear statement** of the issue or feature
- **Relevant context** from the meeting (who mentioned it, why it matters)
- **User impact** or value proposition (if mentioned)
- **Any priorities or constraints** mentioned in the discussion
- **Enough detail** for the /bug or /feature command to create a complete plan

### Example Output
```
/bug Login page shows blank screen after users submit credentials. Users cannot sign in. Client reported this is blocking production use.
/feature Add OAuth support for Google and GitHub authentication. Client requested this to improve user sign-in experience and reduce password management.
/bug Dashboard loads too slowly, performance has regressed from previous versions. Client noticed significant slowdown affecting user experience.
```

## Line-by-Line Command Structure

### Execution Order
Commands should be output in **chronological order** as discussed in the meeting, with the following structure:

1. **One command per line** - Each `/bug` or `/feature` on a separate line
2. **No blank lines** between commands - Ensures clean sequential execution
3. **No additional commentary** - Only the commands themselves
4. **Preserve discussion order** - Maintain the sequence from the transcript

### Multiple Issues Handling
- If transcript contains 3 bugs and 2 features, output exactly 5 command lines
- Order: As discussed in meeting (e.g., bug1, feature1, bug2, bug3, feature2)
- Each command is completely independent and self-contained

## Edge Case Handling

### Case 1: No Issues Found
If the transcript contains **no actionable bugs or features**:
```
No actionable bugs or features were identified in the meeting transcript. The discussion focused on [brief summary of what was discussed].
```

### Case 2: Ambiguous Classification
If a segment could be **either** bug or feature:
- Check for temporal language: "used to", "was", "before" → Bug
- Check for aspirational language: "would like", "could we", "want to" → Feature
- Default to **Feature** if still unclear

### Case 3: Overlapping Concerns
If a segment discusses **both** bug and feature:
```
Example: "The search is broken (bug) and we should add filters (feature)"
Output:
/bug Search functionality is broken and not returning results
/feature Add filter capabilities to search functionality to improve user experience
```

### Case 4: Incomplete Information
If segment lacks sufficient detail:
- Include what is known from the transcript
- Note in description: "Client mentioned [issue] but additional details may be needed"
- Still generate the command - the /bug or /feature prompt will handle research

### Case 5: Duplicate or Related Issues
If multiple segments discuss the **same** issue:
- Consolidate into a **single** command with combined context
- Merge all relevant details from different parts of the transcript
- Avoid creating duplicate commands

### Case 6: Non-Actionable Discussion
**Filter out** these types of segments:
- Greetings and pleasantries ("Hi", "How are you", "Thanks")
- Meeting logistics ("Can you hear me?", "Let me share screen")
- Off-topic discussions (personal chat, unrelated topics)
- Simple acknowledgments ("Okay", "Got it", "Makes sense")
- Agenda setting without details ("Let's discuss features today")

## Conversation Segment Extraction

### Segmentation Strategy
1. **Identify topic boundaries**: Look for phrases like "another thing", "also", "next issue"
2. **Capture complete context**: Include follow-up questions and clarifications
3. **Maintain speaker flow**: Note transitions between client and developer
4. **Preserve completeness**: Don't cut off mid-explanation

### Context Window
- **Minimum**: Single speaker turn with complete thought
- **Optimal**: 2-5 speaker turns that fully explain the issue/feature
- **Maximum**: All related turns until topic changes

### Validation Before Output
Each generated command must pass these checks:
- [ ] Description is complete and understandable without the transcript
- [ ] Classification (bug vs feature) is appropriate
- [ ] No duplicate commands for the same issue
- [ ] Context from meeting is preserved
- [ ] Description is concise but comprehensive (1-3 sentences ideal)

## Instructions for AI Coder

After generating the command list, the AI coder should:

1. **Execute each command sequentially** from top to bottom
2. For each `/bug [description]`:
   - The bug.md command will create a detailed fix plan in `ai-docs/2-bugs/*.md`
   - Research the codebase to understand root cause
   - Create surgical fix plan with validation commands

3. For each `/feature [description]`:
   - The feature.md command will create a detailed implementation plan in `ai-docs/2-features/*.md`
   - Research the codebase to understand existing patterns
   - Create phased implementation plan with testing strategy

4. **Do not skip any commands** - Each line must be executed
5. **Maintain order** - Execute in the sequence provided
6. **Report completion** - Confirm all commands have been executed

## Transcript File Selection

The command accepts a transcript number as an argument:

```
/meet2issues 7
```

This will analyze the transcript at: `ai-docs/0-meetings/transcript7.md`

If no transcript number is provided, prompt the user:
```
Please specify the transcript number:
Usage: /meet2issues <transcript_number>
Example: /meet2issues 7
```

## Workflow Summary

```
1. Read transcript from ai-docs/0-meetings/
2. Parse and segment conversation into topics
3. Apply classification logic (bug vs feature criteria)
4. Generate command for each actionable item
5. Output commands one per line in chronological order
6. AI coder executes each command sequentially
7. Result: Complete documentation in ai-docs/2-bugs/ and ai-docs/2-features/
```

## Quality Checklist

Before outputting the command list, verify:
- [ ] All actionable items from transcript are captured
- [ ] No duplicate or overlapping commands
- [ ] Descriptions include sufficient context
- [ ] Classification makes sense for each item
- [ ] Commands are in chronological order
- [ ] Non-actionable content has been filtered out
- [ ] Each description is self-contained and complete

## Example Complete Workflow

**Command**: `/meet2issues 7`

**Input Transcript** (ai-docs/0-meetings/transcript7.md):
```
Client: The user export feature is completely broken. We get an error when trying to export.
Developer: What's the error message?
Client: It says "Export failed - database timeout". This is urgent.
Client: Also, we'd like to add a dark mode option to the settings.
Developer: That makes sense. Any other requests?
Client: Yes, can we add PDF export in addition to CSV?
```

**Generated Output**:
```
/bug User export feature fails with "Export failed - database timeout" error. Client reported this as urgent and blocking user workflows.
/feature Add dark mode option to application settings to improve user experience and accessibility.
/feature Add PDF export capability in addition to existing CSV export to provide users more format options.
```

**AI Coder Actions**:
1. Execute `/bug User export feature fails...` → Creates `ai-docs/2-bugs/fix-user-export-timeout.md`
2. Execute `/feature Add dark mode option...` → Creates `ai-docs/2-features/dark-mode-settings.md`
3. Execute `/feature Add PDF export capability...` → Creates `ai-docs/2-features/pdf-export-option.md`

---

## Transcript Number

$ARGUMENTS

## Instructions

1. Extract the transcript number from the argument above
2. Construct the file path: `ai-docs/0-meetings/transcript<number>.md`
3. Read the transcript file from that location
4. Process the transcript following all instructions, classification logic, and edge case handling
5. Output the command list in the specified format, one command per line

If the file does not exist, inform the user:
```
Error: Transcript file not found at ai-docs/0-meetings/transcript<number>.md
Please verify the transcript number and ensure the file exists.
```
