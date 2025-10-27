# Task 3.0: Transcript Parsing and Segmentation Logic

This document provides comprehensive specifications for parsing Google Meet transcripts and segmenting conversations into actionable items.

## 3.1: Transcript Input Format Specifications

### Supported File Formats
- **Location**: `ai-docs/0-meetings/`
- **Extensions**: `.md` (Markdown)
- **Encoding**: UTF-8

### Naming Conventions
- **Required**: `transcript<number>.md` (e.g., `transcript7.md`, `transcript12.md`)
- **Pattern**: `transcript` prefix followed by number, no hyphens or spaces
- **Number**: Corresponds to session/meeting number

### Format Variants

#### Variant 1: Plain Text with Speaker Labels
```
Client: The login page is broken. Users can't sign in.
Developer: What error are they seeing?
Client: It just shows a blank screen after they submit credentials.
```

#### Variant 2: Timestamped Format
```
[00:03] Client: The login page is broken. Users can't sign in.
[00:08] Developer: What error are they seeing?
[00:12] Client: It just shows a blank screen after they submit credentials.
```

#### Variant 3: Detailed Format with Names
```
2025-01-15 14:32:15 - Andrea (Client): The login page is broken. Users can't sign in.
2025-01-15 14:32:23 - John (Developer): What error are they seeing?
2025-01-15 14:32:35 - Andrea (Client): It just shows a blank screen after they submit credentials.
```

#### Variant 4: Google Meet Native Export
```
Andrea Palladino
The login page is broken. Users can't sign in.
14:32

John Developer
What error are they seeing?
14:32

Andrea Palladino
It just shows a blank screen after they submit credentials.
14:32
```

### Required Elements
- ✓ Speaker identification (name, role, or label)
- ✓ Conversation content (what was said)
- ✓ Chronological order (temporal sequence preserved)

### Optional Elements
- Timestamps (absolute or relative)
- Speaker roles (Client, Developer, etc.)
- System messages (joins, leaves, screen sharing)
- Meeting metadata (date, attendees, duration)

### Parsing Strategy

**Step 1: Detect Format**
- Scan first 10 lines to identify format variant
- Look for patterns: speaker labels (`:` or `-`), timestamps (`[`, `]`), line structure

**Step 2: Extract Speaker-Content Pairs**
- Identify speaker delimiter (`:`, `-`, or line breaks)
- Extract speaker name/role
- Extract content (what was said)
- Preserve chronological order

**Step 3: Normalize Structure**
- Convert all variants to: `[Speaker]: [Content]`
- Remove timestamps (preserve in metadata if needed)
- Merge multi-line statements from same speaker
- Filter system messages

## 3.2: Identifying Conversation Segments Related to Issues

### Topic Boundary Markers

**Explicit Markers**
- "Another thing..."
- "Also, ..."
- "Next, ..."
- "Moving on, ..."
- "One more issue..."
- "Separate from that, ..."

**Implicit Markers**
- Long pause (3+ speaker turns on different topic)
- Return to agenda ("Let's talk about...")
- Question-answer completion
- Topic closure ("That's all for that")

### Segment Types

**Type 1: Single-Turn Segment**
```
Client: The dashboard export is broken.
```
- Complete issue in one statement
- No follow-up needed
- Clear and self-contained

**Type 2: Multi-Turn Segment (Q&A)**
```
Client: The login page is broken.
Developer: What error are they seeing?
Client: It shows a blank screen after credentials.
Developer: Is this in production or staging?
Client: Production.
```
- Initial statement + clarifying questions
- Capture all turns until topic complete
- Preserve full context

**Type 3: Multi-Turn Segment (Discussion)**
```
Client: We need better reporting.
Developer: What kind of reports do you need?
Client: Sales data and user analytics.
Developer: Should they be exportable?
Client: Yes, PDF and CSV formats.
```
- Evolving discussion of a feature
- Multiple speakers building on idea
- Capture entire discussion arc

### Issue Identification Heuristics

**Bug Signals**
- Negative language: "broken", "not working", "error", "fails"
- Problem statement: "can't", "unable to", "doesn't"
- User impact: "blocking", "urgent", "users are complaining"

**Feature Signals**
- Positive language: "would like", "could we", "want to"
- Future tense: "will need", "planning to", "going to"
- Enhancement language: "improve", "add", "better", "new"

**Non-Issue Signals**
- Status updates: "we've completed", "already done"
- Acknowledgments: "got it", "makes sense", "understood"
- Questions without context: "how's it going?", "any updates?"

## 3.3: Context Preservation Strategy

### What Context to Preserve

**Essential Context**
1. **Problem/Feature Statement**: Core description of the issue
2. **User Impact**: Who is affected and how
3. **Urgency/Priority**: When it needs to be addressed
4. **Technical Details**: Error messages, specific components affected
5. **Success Criteria**: What "fixed" or "implemented" looks like

**Supporting Context**
1. **Speaker Roles**: Who requested it (client, developer, PM)
2. **Related Systems**: What parts of the application are involved
3. **Dependencies**: Prerequisites or related issues
4. **Constraints**: Time, budget, technical limitations

### Context Extraction Rules

**Rule 1: Include Clarifications**
```
Client: The export is broken.
Developer: What format?
Client: CSV export specifically.
```
→ Context: "CSV export is broken" (not just "export is broken")

**Rule 2: Include Impact Statements**
```
Client: The dashboard loads slowly.
Developer: How slow?
Client: Takes 30 seconds. Users are complaining.
```
→ Context: "Dashboard loads slowly (30 seconds), users are complaining"

**Rule 3: Include Technical Details**
```
Client: We get an error on login.
Developer: What's the error message?
Client: Says 'Database connection timeout'.
```
→ Context: "Login fails with 'Database connection timeout' error"

**Rule 4: Preserve Priority/Urgency**
```
Client: The payment processing is failing. This is blocking production.
```
→ Context: "Payment processing is failing. Client reported as blocking production."

### Context Formatting in Commands

**Format**: `[Issue/Feature Description]. [User Impact]. [Priority/Urgency if mentioned].`

**Examples**:
- Bug: "Login page shows blank screen after users submit credentials. Users cannot sign in. Client reported this is blocking production use."
- Feature: "Add OAuth support for Google and GitHub authentication. Client requested this to improve user sign-in experience and reduce password management."

## 3.4: Filtering Rules for Non-Actionable Discussion

### Category 1: Greetings and Pleasantries
**Filter Out**:
- "Hi", "Hello", "Good morning", "How are you"
- "Thanks for joining", "Good to see you"
- "Have a great day", "Talk soon", "Bye"

**Keep**:
- Substantive thank-yous that include context: "Thanks for fixing that bug last week"

### Category 2: Meeting Logistics
**Filter Out**:
- "Can you hear me?", "Is my screen visible?"
- "Let me share my screen", "Can everyone see this?"
- "I'll send the link in chat", "Let me record this"
- "We have 30 minutes", "Let's start"

**Keep**:
- Logistics that affect scope: "We have limited time, so let's prioritize the login bug"

### Category 3: Simple Acknowledgments
**Filter Out**:
- "Okay", "Got it", "Makes sense", "Understood"
- "Yeah", "Yep", "Sure", "Right"
- "Mm-hmm", "Uh-huh", "I see"

**Keep**:
- Acknowledgments with decisions: "Okay, let's do that", "Got it, I'll make that high priority"

### Category 4: Off-Topic Discussion
**Filter Out**:
- Personal conversations (weather, weekend plans, family)
- Company gossip or news unrelated to project
- Technical discussions not related to this project

**Keep**:
- Contextual information: "Since we're launching next month, we need this feature prioritized"

### Category 5: Agenda Setting Without Details
**Filter Out**:
- "Let's talk about bugs today"
- "We'll discuss new features"
- "Shall we review the issues?"

**Keep**:
- Specific agenda with actionable items: "Let's discuss the login bug that's blocking users"

### Category 6: Incomplete Statements
**Filter Out**:
- "So, um...", "Well, actually...", "You know..."
- False starts that lead nowhere
- Interrupted thoughts without completion

**Keep**:
- Completed thoughts even if across multiple turns

### Filtering Algorithm

```
FOR each conversation segment:
  IF contains_actionable_issue(segment):
    IF has_sufficient_context(segment):
      INCLUDE segment
    ELSE:
      MERGE with adjacent segments for context
  ELSE IF is_greeting_or_logistics(segment):
    FILTER OUT
  ELSE IF is_simple_acknowledgment(segment):
    FILTER OUT unless contains_decision
  ELSE IF is_off_topic(segment):
    FILTER OUT
  END IF
END FOR
```

## 3.5: Segment Validation Criteria

### Completeness Checklist

For each segment to be considered valid and complete, verify:

- [ ] **Clear Subject**: What is being discussed (specific feature/bug)
- [ ] **Complete Description**: Enough detail to understand the issue
- [ ] **No Dangling References**: All pronouns and references are clear ("it", "that", "the thing")
- [ ] **Context Included**: Supporting details from Q&A preserved
- [ ] **Actionable**: Can be turned into a /bug or /feature command
- [ ] **Self-Contained**: Understandable without reading the full transcript

### Quality Metrics

**Minimum Length**
- At least 1 complete sentence (10+ words)
- Describes specific issue or feature
- Not just a fragment or acknowledgment

**Maximum Length**
- No more than 5-7 speaker turns per segment
- If longer, likely multiple issues combined
- Should split into separate segments

**Clarity Test**
- Can someone unfamiliar with the meeting understand the issue?
- Are all technical terms explained or clear from context?
- Is the desired outcome clear?

### Validation Questions

Ask these questions for each segment:

1. **What?** - What is the issue or feature being discussed?
2. **Why?** - Why does it matter (user impact, business value)?
3. **Who?** - Who is affected or requesting this?
4. **When?** - Is there urgency or priority mentioned?
5. **Where?** - What part of the system is involved?

If you can't answer questions 1 and 2, the segment is incomplete.

### Segment Merge Rules

**Merge segments when**:
- Same issue discussed across non-contiguous turns
- Initial mention + later clarification
- Related issues that share root cause

**Keep segments separate when**:
- Clearly different issues (login vs dashboard)
- Different types (bug vs feature)
- Different urgency levels
- Different systems/components

### Invalid Segment Examples

**Example 1: Incomplete**
```
Client: The thing is broken.
```
❌ What "thing"? No context.

**Example 2: Too Vague**
```
Client: We should improve the UI.
```
❌ What part of UI? How to improve?

**Example 3: Acknowledgment Only**
```
Developer: Got it, I'll look into that.
```
❌ No actionable content, just acknowledgment.

### Valid Segment Examples

**Example 1: Complete Bug**
```
Client: The CSV export feature is failing with a timeout error. Users can't download their data. This is urgent.
```
✓ Clear issue, impact, and urgency.

**Example 2: Complete Feature**
```
Client: We'd like to add dark mode to the settings. Users have been requesting this for accessibility.
```
✓ Clear feature, reason, and user value.

**Example 3: Complete Multi-Turn**
```
Client: The dashboard is slow.
Developer: How slow?
Client: Takes 30 seconds to load. It used to be instant.
Developer: Which dashboard page?
Client: The main analytics dashboard.
```
✓ Clear issue with context and specifics.

## Implementation in meet2issues.md

All of these specifications are implemented in the meet2issues.md Higher-Order Prompt through:

1. **Input Requirements** section - Covers format specifications
2. **Conversation Segment Extraction** section - Covers segmentation strategy
3. **Classification Logic** section - Covers issue identification
4. **Edge Case Handling** section - Covers filtering and validation
5. **Quality Checklist** section - Covers completeness validation

The prompt guides Claude to apply these rules when processing transcripts.
