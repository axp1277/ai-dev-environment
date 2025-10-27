# Task 5.0: Feature Classification and Extraction Workflow

This document provides comprehensive specifications for identifying, classifying, and extracting feature requests from meeting transcripts.

## 5.1: Feature Identification Criteria

### Primary Feature Categories

#### Category 1: Enhancement Requests
Requests to improve or extend existing functionality.

**Keywords**:
- "enhance", "enhancement", "improve", "better"
- "add", "include", "extend", "expand"
- "upgrade", "update", "modernize"
- "make it", "could it", "can we"

**Examples**:
- "We'd like to enhance the reporting dashboard with more filters"
- "Can we improve the search to include fuzzy matching"
- "Add the ability to export to PDF in addition to CSV"

#### Category 2: New Functionality
Requests for completely new features that don't currently exist.

**Keywords**:
- "new feature", "add feature", "build", "create"
- "implement", "develop", "introduce"
- "we need", "we want", "would like"
- "support for", "capability to"

**Examples**:
- "We need a new notification system for user alerts"
- "Add dark mode support to the application"
- "Implement two-factor authentication for user accounts"

#### Category 3: User Stories and Needs
Descriptions from the user perspective of what they want to accomplish.

**Patterns**:
- "Users want to...", "Users need to..."
- "As a user, I want to...", "As a [role], I need to..."
- "It would be great if users could..."
- "Users are asking for..."

**Examples**:
- "Users want to be able to customize their dashboard layout"
- "As an admin, I need to see all user activity logs"
- "Users are asking for the ability to save filter preferences"

#### Category 4: Capability Additions
Adding functionality that extends what the system can do.

**Keywords**:
- "capability", "ability to", "enable", "allow"
- "support for", "compatible with", "work with"
- "handle", "process", "manage"

**Examples**:
- "Add the capability to import from Excel files"
- "Enable users to share reports with external stakeholders"
- "Support for multi-language translations"

#### Category 5: Optimization Requests (Non-Regression)
Making existing features better, faster, or easier (without fixing bugs).

**Keywords**:
- "optimize", "faster", "more efficient"
- "streamline", "simplify", "easier"
- "automate", "reduce steps", "one-click"

**Distinguishing from Bugs**:
- Future-looking: "would be nice", "could be faster"
- No regression language: NOT "used to be", "was faster"
- Enhancement language: "make it better", "improve"

**Examples**:
- "Optimize the dashboard to load under 3 seconds"
- "Streamline the checkout process from 5 steps to 3"
- "Make the report generation more efficient"

#### Category 6: Integration Requests
Connecting to external systems, services, or tools.

**Keywords**:
- "integrate", "integration with", "connect to"
- "sync with", "import from", "export to"
- "API", "webhook", "plugin", "extension"
- "support for [service name]"

**Examples**:
- "Integrate with Salesforce for CRM data sync"
- "Add Slack notifications for system events"
- "Support OAuth login with Google and GitHub"

### Secondary Feature Indicators

#### Indicator 1: Future Tense
- "will need", "going to need", "planning to"
- "would like", "would be nice", "could we"
- "in the future", "down the road"

#### Indicator 2: Positive Language
- "great", "awesome", "helpful", "valuable"
- "benefit", "improve", "enhance", "better"
- "nice to have", "would love"

#### Indicator 3: Business Value Statements
- "increase revenue", "save time", "improve efficiency"
- "better user experience", "competitive advantage"
- "customer request", "market demand"

### Classification Decision Tree

```
Does segment mention:
├─ "Broken", "not working", "error"? → Check BUG criteria
├─ "Used to work", "regression"? → BUG (not feature)
├─ "Would like", "could we", "add"? → FEATURE
├─ "Improve", "enhance", "better" (no regression)? → FEATURE
├─ "New", "build", "create"? → FEATURE
├─ User story pattern ("users want to")? → FEATURE
└─ Default if unclear → FEATURE
```

## 5.2: Feature Description Extraction Template

### Template Structure

```
[Action Verb] [Feature/Capability] [for/to Purpose]. [User Value/Benefit]. [Additional Context if mentioned].
```

### Component Breakdown

**1. Action Verb**
- Start with action: "Add", "Implement", "Create", "Enable", "Integrate"
- Avoid passive: "There should be" → "Add"

**2. Feature/Capability**
- What is being requested
- Be specific: Not "better reports" but "customizable report templates"

**3. Purpose**
- Why it's needed or what it enables
- "for [user group]", "to [accomplish goal]"

**4. User Value/Benefit**
- How it helps users or the business
- What improvement it brings

**5. Additional Context**
- Priority if mentioned
- Technical preferences if specified
- Constraints or requirements

### Extraction Examples

**Example 1: Simple Feature**
```
Transcript: "We'd like to add dark mode to the settings."

Extracted Description:
"Add dark mode option to application settings to improve user experience and accessibility."
```

**Example 2: Feature with User Value**
```
Transcript:
Client: "Can we add PDF export?"
Developer: "In addition to CSV?"
Client: "Yes, some users need PDF format for reports."

Extracted Description:
"Add PDF export capability in addition to existing CSV export to provide users more format options for reports."
```

**Example 3: Feature with Business Context**
```
Transcript:
Client: "We need OAuth integration for Google and GitHub."
Developer: "Why those two specifically?"
Client: "Most of our users have Google accounts, and developers use GitHub. It'll improve sign-up conversion."

Extracted Description:
"Implement OAuth authentication for Google and GitHub to improve user sign-up conversion, as most users have accounts on these platforms."
```

**Example 4: User Story Format**
```
Transcript:
Client: "Users want to be able to save their filter preferences."
Developer: "So they don't have to re-enter them each time?"
Client: "Exactly. It's a common request from power users."

Extracted Description:
"Add ability to save filter preferences so users don't need to re-enter them each session. Requested by power users for improved workflow efficiency."
```

## 5.3: Feature Description Formatting Standards

### Standard 1: Clear Scope
- Define what the feature includes
- Specify boundaries if mentioned
- Note any limitations discussed

**Bad**: "Make the dashboard better."

**Good**: "Add customizable widgets to the dashboard allowing users to rearrange and resize components."

### Standard 2: User Benefit Explicit
- Always include why it matters
- State the value proposition
- Mention user impact or business value

**Bad**: "Add export feature."

**Good**: "Add bulk export feature to allow users to download multiple reports simultaneously, saving time for data analysts."

### Standard 3: Acceptance Criteria (If Mentioned)
- Include specific requirements from conversation
- Note success criteria if discussed
- Mention constraints or preferences

**Bad**: "Add notifications."

**Good**: "Add email and in-app notifications for user activity, with user preference controls to manage notification frequency."

### Formatting Guidelines

**DO**:
- ✓ Start with strong action verb (Add, Implement, Create, Enable)
- ✓ Be specific about what's being added
- ✓ Include user benefit or business value
- ✓ Mention technical preferences if specified (e.g., "using React")
- ✓ Note any mentioned constraints or requirements
- ✓ Use positive, forward-looking language

**DON'T**:
- ✗ Be vague: "improve things", "make it better"
- ✗ Use negative framing: "fix the lack of"
- ✗ Omit the "why" (user value)
- ✗ Include bug language: "broken", "not working"
- ✗ Mix multiple unrelated features in one description
- ✗ Add speculation not from the transcript

## 5.4: Feature Complexity Inference Logic

### Explicit Complexity Mentions

If transcript contains these phrases, include in description:

**Simple/Quick Win**:
- "simple", "quick win", "easy", "straightforward"
- "small feature", "minor addition"
- "should be quick", "won't take long"

**Medium Complexity**:
- "medium complexity", "moderate effort"
- "few weeks", "next sprint", "reasonable timeline"

**Complex/Large**:
- "complex", "big project", "major feature"
- "multi-phase", "long term", "several months"
- "significant effort", "large undertaking"

### Implicit Complexity Signals

**Likely Simple** if:
- Single component change
- UI-only modification
- Configuration/settings addition
- Minor integration

**Likely Medium** if:
- Multiple components affected
- New database schema needed
- Moderate integration work
- New user workflows

**Likely Complex** if:
- System-wide changes
- New architecture components
- Complex integrations
- Security/compliance requirements
- Multiple teams involved

### Complexity Formatting

**If Explicit**: Include verbatim
```
"Add real-time collaboration feature to document editor. Client noted this is a complex, multi-phase project."
```

**If Implicit and Relevant**: Can note
```
"Implement single sign-on (SSO) integration with SAML support across all applications."
(Implies complexity through scope)
```

**If Unclear**: Omit, let /feature command assess
```
"Add export to Excel functionality for user reports."
```

## 5.5: /feature Command Generation Template

### Command Format

```
/feature [Action Verb] [Feature/Capability] [for/to Purpose]. [User Value/Benefit]. [Additional Context].
```

### Generation Rules

**Rule 1: One Feature Per Command**
- Each distinct feature gets its own command line
- Don't combine multiple features into one command
- Split related features if they're separately implementable

**Rule 2: Self-Contained Description**
- Description must be understandable without transcript
- Include all necessary context
- No pronouns without antecedents

**Rule 3: Focus on Value**
- Always include user benefit or business value
- Explain why it matters
- Connect to user needs or business goals

**Rule 4: Include Technical Preferences**
- If specific technologies mentioned, include them
- Note integration requirements
- Specify platform if discussed (web, mobile, API)

**Rule 5: Chronological Order**
- Output features in order discussed in meeting
- Don't reorder by complexity or priority

### Complete Examples

**Example 1: Basic Feature**
```
Transcript:
Client: "We'd like to add dark mode to the settings."

Generated Command:
/feature Add dark mode option to application settings to improve user experience and accessibility.
```

**Example 2: Feature with User Story**
```
Transcript:
Client: "Users want to customize their dashboard layout."
Developer: "Like drag and drop widgets?"
Client: "Exactly, so they can arrange it how they want."

Generated Command:
/feature Add customizable dashboard with drag-and-drop widgets allowing users to arrange components according to their preferences and workflow needs.
```

**Example 3: Integration Feature**
```
Transcript:
Client: "We need Slack integration for notifications."
Developer: "What kind of notifications?"
Client: "System alerts and user activity updates."
Developer: "Should users be able to configure which notifications they get?"
Client: "Yes, definitely."

Generated Command:
/feature Integrate Slack notifications for system alerts and user activity updates with user-configurable preferences to control which notifications are sent.
```

**Example 4: Feature with Business Value**
```
Transcript:
Client: "We want to add bulk actions for user management."
Developer: "What actions?"
Client: "Bulk delete, bulk role assignment, bulk export."
Client: "Our admins waste hours doing these one by one."

Generated Command:
/feature Add bulk action capabilities for user management including bulk delete, role assignment, and export to save administrator time currently spent on individual user operations.
```

**Example 5: Complex Feature**
```
Transcript:
Client: "We need a reporting module with custom templates."
Developer: "What should users be able to customize?"
Client: "Columns, filters, grouping, and export formats."
Client: "They should be able to save templates and share them with their team."

Generated Command:
/feature Create reporting module with customizable templates supporting column selection, filters, grouping, and multiple export formats. Users should be able to save and share templates with team members.
```

### Multi-Feature Example

```
Transcript:
Client: "We have several feature requests. First, add OAuth for Google."
Developer: "Okay."
Client: "Second, we need PDF export for reports."
Developer: "Got it."
Client: "Third, add a user activity timeline."

Generated Commands:
/feature Implement OAuth authentication for Google to improve user sign-in experience and reduce password management.
/feature Add PDF export capability for reports to provide users additional format options beyond CSV.
/feature Add user activity timeline displaying chronological history of user actions for audit and tracking purposes.
```

### Optimization vs Bug Example

```
Transcript Example 1 (BUG - Regression):
Client: "The dashboard is slow now. It used to load in 2 seconds."

Classification: BUG
Command: /bug Dashboard performance degraded from 2 seconds to current slow load time. Performance regression.

Transcript Example 2 (FEATURE - Optimization):
Client: "The dashboard loads in 10 seconds. Could we optimize it to under 5?"

Classification: FEATURE
Command: /feature Optimize dashboard load performance to achieve under 5 second load times for improved user experience.
```

## Integration with meet2issues.md

All feature classification logic is implemented in meet2issues.md through:

1. **Classification Logic** section - Feature Identification Criteria
2. **Command Generation Format** section - Description Requirements
3. **Classification Decision Rules** - Bug vs Feature distinction
4. **Example Complete Workflow** - Full feature extraction example

The prompt applies these specifications automatically when processing transcripts.

## Validation Checklist

Before generating a `/feature` command, verify:

- [ ] Clearly identified as a feature (not a bug fix)
- [ ] Action verb starts the description
- [ ] Feature/capability is clearly specified
- [ ] User value or business benefit is included
- [ ] Description is self-contained and complete
- [ ] Technical preferences included if mentioned
- [ ] No duplicate of another feature in the command list
- [ ] No bug language present ("broken", "not working", "regression")
