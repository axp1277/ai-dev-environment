# Task 4.0: Bug Classification and Extraction Workflow

This document provides comprehensive specifications for identifying, classifying, and extracting bug information from meeting transcripts.

## 4.1: Bug Identification Criteria

### Primary Bug Categories

#### Category 1: Error Reports
Explicit mentions of errors, exceptions, or failures in the system.

**Keywords**:
- "error", "exception", "crash", "fails", "failed"
- "throws error", "error message", "error code"
- "500 error", "404 error", "timeout error"
- "stack trace", "exception thrown"

**Examples**:
- "Users are getting a 500 error when they try to submit the form"
- "The application crashes when we upload large files"
- "There's an exception thrown in the payment processing module"

#### Category 2: Unexpected Behavior
Descriptions of the system behaving differently than expected.

**Keywords**:
- "not working", "doesn't work", "broken"
- "should be", "expected", "supposed to"
- "instead", "but", "however"
- "wrong", "incorrect", "inaccurate"

**Patterns**:
- "X should do Y but does Z instead"
- "Expected X but got Y"
- "It's supposed to X but it doesn't"

**Examples**:
- "The sort button should arrange items alphabetically but it's random"
- "Expected the user to stay logged in but they get logged out"
- "The total should be $100 but it shows $95"

#### Category 3: Defects and Regressions
Issues with existing functionality, especially things that worked before.

**Keywords**:
- "regression", "broke", "stopped working"
- "used to work", "worked before", "was working"
- "no longer", "doesn't anymore"
- "defect", "bug", "issue"

**Examples**:
- "The export feature used to work but stopped working after the update"
- "This was functioning properly last week but is broken now"
- "We have a regression in the login flow from the last deployment"

#### Category 4: Performance Regressions
System slowness or degraded performance compared to previous state.

**Keywords**:
- "slow", "slower than before", "used to be faster"
- "takes too long", "hanging", "freezing"
- "timeout", "times out", "waiting forever"
- "performance degraded", "worse performance"

**Temporal Indicators** (key for classification):
- "was fast", "used to load instantly"
- "slower since", "after the update"
- "before it was X, now it's Y"

**Examples**:
- "The dashboard loads in 30 seconds now, it used to be instant"
- "Search has gotten really slow since last week"
- "The API response time has tripled after the deployment"

#### Category 5: Data Corruption/Loss
Issues with data integrity, missing information, or corrupted files.

**Keywords**:
- "lost data", "missing data", "data disappeared"
- "corrupted", "corrupt files", "can't open"
- "inconsistent", "out of sync", "doesn't match"
- "deleted", "removed", "vanished"

**Examples**:
- "User profiles are missing the email addresses they had before"
- "Exported CSV files are corrupted and won't open"
- "The database shows different numbers than the UI"

### Secondary Bug Indicators

#### Indicator 1: User Impact Statements
- "users can't", "blocking users", "users are complaining"
- "production is down", "affecting customers"
- "urgent", "critical", "high priority"

#### Indicator 2: Reproducibility Statements
- "every time", "always", "consistently"
- "happens when", "if you do X then Y occurs"
- "steps to reproduce", "here's how to trigger it"

#### Indicator 3: Negative User Experience
- "frustrating", "annoying users", "confusing"
- "poor experience", "users are upset"
- "can't complete", "blocks workflow"

### Classification Decision Tree

```
Does segment mention:
├─ Explicit error/exception? → BUG (Category 1)
├─ "Broken", "not working", "fails"? → BUG (Category 2)
├─ "Used to work", "regression"? → BUG (Category 3)
├─ "Slower than before", "used to be fast"? → BUG (Category 4)
├─ "Lost data", "corrupted", "missing"? → BUG (Category 5)
└─ None of the above → Check Feature Criteria
```

## 4.2: Bug Description Extraction Template

### Template Structure

```
[Component/Feature] [Problem] [Error/Symptom]. [User Impact]. [Priority/Urgency if mentioned].
```

### Component Breakdown

**1. Component/Feature**
- What part of the system is affected
- Examples: "Login page", "CSV export", "User dashboard", "API endpoint"

**2. Problem**
- What is going wrong
- Use strong verbs: "fails", "crashes", "shows error", "returns incorrect data"

**3. Error/Symptom**
- Specific error message or observable symptom
- Include exact error text in quotes if available
- Describe what users see

**4. User Impact**
- Who is affected and how
- What they cannot do
- Business/workflow impact

**5. Priority/Urgency**
- If explicitly mentioned in transcript
- Examples: "blocking production", "urgent", "critical", "affecting all users"

### Extraction Examples

**Example 1: Simple Bug**
```
Transcript: "The login page is broken. Users can't sign in."

Extracted Description:
"Login page is broken and users cannot sign in."
```

**Example 2: Bug with Error Details**
```
Transcript:
Client: "The CSV export fails with an error."
Developer: "What error?"
Client: "Says 'Database timeout' and nothing downloads."

Extracted Description:
"CSV export fails with 'Database timeout' error and files do not download."
```

**Example 3: Bug with Context and Urgency**
```
Transcript:
Client: "The payment processing is failing. This is blocking our customers. Very urgent."
Developer: "What's the failure?"
Client: "It shows 'Transaction declined' even for valid cards."

Extracted Description:
"Payment processing fails showing 'Transaction declined' error even for valid cards. Blocking customers. Client reported as very urgent."
```

**Example 4: Performance Regression**
```
Transcript:
Client: "The dashboard is super slow now."
Developer: "How slow?"
Client: "Takes 30 seconds. It used to load instantly."

Extracted Description:
"Dashboard loads slowly (30 seconds) compared to previous instant loading. Performance regression."
```

## 4.3: Bug Description Formatting Standards

### Standard 1: Concise
- Target: 1-3 sentences
- Avoid unnecessary words: "basically", "kind of", "sort of"
- Get to the point immediately

**Bad**: "So basically what's happening is that when users are trying to use the login feature, it kind of doesn't work properly."

**Good**: "Login feature fails when users attempt to sign in."

### Standard 2: Actionable
- Use specific technical terms
- Include component names, not vague references
- Provide enough detail to start investigation

**Bad**: "The thing is broken."

**Good**: "User profile export feature returns 404 error."

### Standard 3: Context-Aware
- Include relevant details from the conversation
- Preserve error messages verbatim (in quotes)
- Note user impact and urgency
- Mention environment if specified (production, staging)

**Bad**: "Export doesn't work."

**Good**: "Production CSV export fails with 'Database connection timeout' error, blocking daily reports workflow."

### Formatting Guidelines

**DO**:
- ✓ Start with the component/feature name
- ✓ Use present tense: "fails", "shows", "returns"
- ✓ Include exact error messages in quotes
- ✓ Mention user impact in second sentence
- ✓ Add priority if explicitly stated
- ✓ Be specific about what's wrong

**DON'T**:
- ✗ Use passive voice: "is broken by"
- ✗ Add speculation: "might be", "probably"
- ✗ Include meeting logistics: "the client mentioned"
- ✗ Paraphrase error messages
- ✗ Omit important context
- ✗ Make it too verbose

## 4.4: Bug Priority Inference Logic

### Explicit Priority Mentions

If transcript contains these phrases, include in description:

**Critical/Urgent**:
- "critical", "urgent", "ASAP", "immediately"
- "blocking", "blocker", "blocks", "preventing"
- "production down", "customers affected", "revenue impact"

**High Priority**:
- "high priority", "important", "needs attention"
- "many users affected", "frequently occurring"
- "should fix soon", "next sprint"

**Medium Priority**:
- "medium priority", "moderate", "when you can"
- "some users", "occasionally", "sometimes"

**Low Priority**:
- "low priority", "nice to fix", "eventually"
- "minor", "cosmetic", "aesthetic"
- "edge case", "rare", "uncommon"

### Implicit Priority Signals

Even without explicit priority mention, infer from context:

**Likely Critical** if:
- Mentions "production", "all users", "no workaround"
- Mentions "revenue", "payment", "security"
- Mentions "data loss", "corruption"

**Likely High** if:
- Mentions "many users", "important feature"
- Mentions "regression" (previously worked)
- Mentions "customer complaints"

**Likely Medium** if:
- Mentions "some users", "specific scenario"
- No urgency language used
- Has workaround mentioned

**Likely Low** if:
- Mentions "minor", "cosmetic", "edge case"
- Mentions "rare", "unlikely scenario"

### Priority Formatting

**If Explicit**: Include verbatim
```
"Login fails with 500 error. Client reported as critical and urgent."
```

**If Implicit and Strong**: Include inference
```
"Payment processing fails in production affecting all customers. Blocking revenue."
```

**If Unclear**: Omit priority, let /bug command determine
```
"Search results display incorrect sorting order."
```

## 4.5: /bug Command Generation Template

### Command Format

```
/bug [Component] [Problem] [Error/Symptom]. [User Impact]. [Priority if mentioned].
```

### Generation Rules

**Rule 1: One Bug Per Command**
- Each distinct bug gets its own command line
- Don't combine multiple bugs into one command

**Rule 2: Self-Contained Description**
- Description must be understandable without transcript
- Include all necessary context
- No pronouns without antecedents

**Rule 3: Preserve Technical Details**
- Exact error messages in quotes
- Specific component names
- Version numbers if mentioned
- Environment if specified (production, staging)

**Rule 4: Include User Impact**
- What users cannot do
- How it affects workflow
- Business impact if mentioned

**Rule 5: Chronological Order**
- Output bugs in order discussed in meeting
- Don't reorder by priority

### Complete Examples

**Example 1: Basic Bug**
```
Transcript:
Client: "The login page is broken. Users can't access their accounts."

Generated Command:
/bug Login page is broken and users cannot access their accounts.
```

**Example 2: Bug with Error Details**
```
Transcript:
Client: "When users export data, they get an error."
Developer: "What error?"
Client: "It says 'Export failed - database timeout'."

Generated Command:
/bug Data export fails with 'Export failed - database timeout' error when users attempt to download.
```

**Example 3: Bug with Full Context**
```
Transcript:
Client: "The payment processing module is failing in production."
Developer: "What's happening?"
Client: "Transactions show 'declined' even for valid cards. This is blocking our revenue. Critical."
Developer: "What error code?"
Client: "Error code 5001."

Generated Command:
/bug Payment processing module fails in production with error code 5001, showing 'declined' status for valid credit cards. Blocking revenue. Client reported as critical.
```

**Example 4: Performance Regression**
```
Transcript:
Client: "The analytics dashboard is loading very slowly now."
Developer: "How slow?"
Client: "About 45 seconds. It used to be 2-3 seconds."
Client: "This happened after last week's deployment."

Generated Command:
/bug Analytics dashboard performance degraded from 2-3 seconds to 45 seconds load time after last week's deployment. Performance regression.
```

**Example 5: Data Issue**
```
Transcript:
Client: "User profiles are missing email addresses that were there before."
Developer: "When did this start?"
Client: "We noticed it yesterday. About 200 users affected."

Generated Command:
/bug User profiles missing email addresses that were previously stored. Approximately 200 users affected. Started yesterday.
```

### Multi-Bug Example

```
Transcript:
Client: "We have three issues. First, login is broken."
Developer: "What's the error?"
Client: "Blank screen. Second, the export times out."
Developer: "Okay."
Client: "Third, user search doesn't return results."

Generated Commands:
/bug Login shows blank screen after credentials are submitted and users cannot sign in.
/bug Export feature times out and fails to generate downloadable files.
/bug User search returns no results when queries are entered.
```

## Integration with meet2issues.md

All bug classification logic is implemented in meet2issues.md through:

1. **Classification Logic** section - Bug Identification Criteria
2. **Command Generation Format** section - Description Requirements
3. **Edge Case Handling** section - Ambiguous classification
4. **Example Complete Workflow** - Full bug extraction example

The prompt applies these specifications automatically when processing transcripts.

## Validation Checklist

Before generating a `/bug` command, verify:

- [ ] Clearly identified as a bug (not a feature request)
- [ ] Component/feature is specified
- [ ] Problem is clearly stated
- [ ] Error message included if available (in quotes)
- [ ] User impact is mentioned
- [ ] Priority included if explicitly mentioned
- [ ] Description is self-contained and complete
- [ ] No duplicate of another bug in the command list
