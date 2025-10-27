# Task 1.0: System Prompt Infrastructure Analysis

This document provides a comprehensive analysis of the existing /bug and /feature commands to support the Meet-to-Issues workflow implementation.

## 1. Bug Command Analysis

### Input Format
- **Command**: `/bug $ARGUMENTS`
- **Arguments**: Free-form text describing the bug
- **Expected Content**: Bug description including symptoms, expected vs actual behavior

### Output Format
- **File Location**: `ai-docs/2-bugs/*.md` (dynamically named based on bug description)
- **File Structure**:
  ```markdown
  # Bug: <bug name>

  ## Bug Description
  ## Problem Statement
  ## Solution Statement
  ## Steps to Reproduce
  ## Root Cause Analysis
  ## Relevant Files
  ## Step by Step Tasks
  ## Validation Commands
  ## Notes
  ```

### Key Characteristics
- **Focus**: Root cause analysis and minimal surgical fixes
- **Approach**: Research-based, thorough understanding before planning
- **Validation**: Includes commands to verify zero regressions
- **Scope**: Relevant files in app/**, scripts/**, adws/**

## 2. Feature Command Analysis

### Input Format
- **Command**: `/feature $ARGUMENTS`
- **Arguments**: Free-form text describing the feature
- **Expected Content**: Feature description including purpose and value to users

### Output Format
- **File Location**: `ai-docs/2-features/<feature_name>.md`
- **File Structure**:
  ```markdown
  # Feature: <feature name>

  ## Feature Description
  ## User Story
  ## Problem Statement
  ## Solution Statement
  ## Relevant Files
  ## Implementation Plan (Phase 1, 2, 3)
  ## Step by Step Tasks (with =4/=�/=� status)
  ## Testing Strategy
  ## Acceptance Criteria
  ## Validation Commands
  ## Notes
  ```

### Key Characteristics
- **Focus**: Net new functionality with user value
- **Approach**: Phased implementation (Foundation → Core → Integration)
- **Task Format**: Incremental numbering with status indicators (=4, =�, =�)
- **Scope**: Relevant files in app/server/**, app/client/**, scripts/**, adws/**

## 3. Classification Criteria

### Bug Identification Criteria
A conversation segment should be classified as a **BUG** if it contains:

1. **Error Reports**: Mentions of errors, exceptions, crashes, or failures
   - Keywords: "error", "broken", "not working", "fails", "crash", "exception"

2. **Unexpected Behavior**: Descriptions of actual vs expected behavior mismatch
   - Keywords: "should be", "expected", "instead", "wrong", "incorrect"

3. **Defects**: Issues with existing functionality that worked before or should work
   - Keywords: "regression", "used to work", "stopped working", "defect"

4. **Performance Issues**: Slow response times, memory leaks, resource problems
   - Keywords: "slow", "hanging", "timeout", "memory leak", "performance"

5. **Data Corruption**: Lost data, corrupted files, inconsistent state
   - Keywords: "lost data", "corrupted", "missing", "inconsistent"

### Feature Identification Criteria
A conversation segment should be classified as a **FEATURE** if it contains:

1. **Enhancement Requests**: Requests for new functionality or improvements
   - Keywords: "add", "new feature", "enhancement", "improve", "could we"

2. **User Stories**: Descriptions of user needs and desired outcomes
   - Patterns: "as a user", "I want to", "it would be nice if", "can we"

3. **Capability Additions**: Requests to add something that doesn't exist
   - Keywords: "implement", "create", "build", "develop", "integrate"

4. **Optimization Requests**: Making existing functionality better (not fixing bugs)
   - Keywords: "optimize", "better", "faster", "easier", "streamline"

5. **New Integrations**: Connecting to external systems or services
   - Keywords: "integrate", "connect to", "support for", "compatibility with"

### Ambiguity Resolution Rules

1. **Default to Feature**: If unclear whether bug or feature, classify as feature
2. **Bug Priority**: If explicitly mentions "broken", "error", or "not working" → Bug
3. **Split if Needed**: If segment contains both bug and feature aspects, create separate items
4. **Context Matters**: Consider surrounding conversation for classification hints

## 4. Conversation Segment Extraction Strategy

### Context Window Definition
- **Minimum Segment**: Single speaker turn with complete thought
- **Maximum Segment**: Multi-turn exchange that completes a single topic
- **Optimal Size**: 2-5 speaker turns that capture full context of issue

### Sentence Boundary Rules
1. **Start Boundary**: Begin with the first mention of the issue/feature
2. **End Boundary**: End when topic changes or issue is fully described
3. **Include Context**: Capture clarifying questions and answers
4. **Preserve Completeness**: Don't cut off mid-explanation

### Extraction Process
1. **Identify Topic Markers**: Look for phrases like "another thing", "also", "next issue"
2. **Track Speaker Transitions**: Note when client vs developer is speaking
3. **Capture Complete Exchanges**: Include follow-up questions and clarifications
4. **Maintain Chronological Order**: Process segments in order of discussion

### Segment Validation Criteria
A valid segment must contain:
- [ ] Clear description of the issue or feature
- [ ] Enough context to understand the problem/request
- [ ] No incomplete thoughts or cut-off sentences
- [ ] Speaker attribution (if relevant for understanding)

### Filtering Rules (Non-Actionable Content)
Exclude segments that are:
- Greetings and pleasantries ("Hi", "How are you", "Thanks for joining")
- Off-topic discussions (weather, personal chat, unrelated topics)
- Meeting logistics ("Can you hear me?", "Let me share my screen")
- Acknowledgments without content ("Okay", "Got it", "Makes sense")
- Agenda setting without actionable items ("Let's discuss...", "Today we'll cover...")

### Edge Cases

#### Case 1: Overlapping Bug and Feature
**Example**: "The login is broken (bug), and we also need to add OAuth support (feature)"
**Strategy**: Split into two segments:
- Segment 1: "The login is broken" → /bug
- Segment 2: "add OAuth support" → /feature

#### Case 2: Ambiguous Classification
**Example**: "The dashboard is too slow"
**Analysis**: Could be bug (performance regression) or feature (optimization request)
**Strategy**: Check for temporal context:
- If "used to be faster" → Bug (regression)
- If "would be nice if faster" → Feature (enhancement)
- If unclear → Default to Feature

#### Case 3: Multiple Related Issues
**Example**: "The user table doesn't sort correctly, and it also doesn't filter properly"
**Strategy**: Keep as single segment if root cause is likely shared, otherwise split

#### Case 4: Incomplete Information
**Example**: "Something is wrong with the API"
**Strategy**: Mark as needs-clarification in description, but still classify as bug

## 5. Input/Output Format Summary

### For Meet-to-Issues Workflow

#### Input (from ai-docs/0-meetings/)
```
Google Meet Transcript Format:
- Plain text or formatted with timestamps
- Speaker labels (Client:, Developer:, etc.)
- Chronological conversation flow
- May include system messages (joins, leaves, etc.)
```

#### Output (to AI Coder)
```
Command List Format:
/bug [Bug description with full context from transcript]
/bug [Another bug description if multiple bugs identified]
/feature [Feature description with user value and context]
/feature [Another feature description if multiple features identified]
```

#### Resulting Files
- **Bugs**: `ai-docs/2-bugs/<bug-name>.md` (as per bug.md command)
- **Features**: `ai-docs/2-features/<feature-name>.md` (as per feature.md command)

## 6. Integration Points

### From Transcript to Commands
1. Parse transcript from `ai-docs/0-meetings/`
2. Apply segmentation strategy (Section 4)
3. Apply classification criteria (Section 3)
4. Generate `/bug` or `/feature` commands with extracted descriptions
5. Output one command per line for AI coder to execute sequentially

### Command Execution Flow
1. AI coder receives command list from meet2issues HOP
2. For each `/bug [description]`:
   - Executes bug.md prompt with description as $ARGUMENTS
   - Creates plan in ai-docs/2-bugs/*.md
3. For each `/feature [description]`:
   - Executes feature.md prompt with description as $ARGUMENTS
   - Creates plan in ai-docs/2-features/*.md

## 7. Quality Assurance Guidelines

### Description Quality Checklist
For each generated command, ensure description includes:
- [ ] Clear statement of the issue/feature
- [ ] Relevant context from the meeting
- [ ] User impact or value proposition
- [ ] Any mentioned priorities or constraints
- [ ] Enough detail for the command to create a complete plan

### Validation Strategy
Before outputting command list:
- Verify all actionable items from transcript are captured
- Check for duplicate or overlapping issues
- Ensure descriptions are concise but complete
- Confirm chronological ordering is preserved
- Validate that classification makes sense for each item

## Implementation Notes

- Both bug.md and feature.md commands start with research (reading README.md)
- Both use uv package manager and pytest for testing
- Bug command focuses on surgical fixes with zero regressions
- Feature command uses phased approach with incremental tasks
- Both commands generate plans that AI coders can execute systematically
- The meet2issues HOP orchestrates these commands based on transcript analysis
