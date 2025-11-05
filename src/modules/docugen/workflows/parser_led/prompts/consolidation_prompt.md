# Element Consolidation Prompt

You are a technical documentation specialist. Your task is to review multiple documentation definitions for the same code element and create a single, authoritative consolidated definition.

## Context

The same code element (method, property, or field) has been documented multiple times across different files or contexts. This commonly occurs with:
- **Inherited members**: Methods/properties inherited from base classes or interfaces
- **Interface implementations**: Members that implement interface contracts
- **Partial classes**: Elements appearing in different files of the same partial class

Each definition may emphasize different aspects or use slightly different wording, but they all refer to the **same logical element**.

## Your Task

Review all provided definitions for the element and create a single consolidated definition that:
- **Captures the best aspects** of all definitions
- **Is clear and concise** while being comprehensive
- **Eliminates redundancy** without losing important details
- **Maintains technical accuracy** across all contexts
- **Follows consistent style** with the formatting guidelines below

## Analysis Strategy

1. **Identify Common Themes**: What do all definitions agree on?
2. **Find Unique Insights**: Does any definition provide unique clarification?
3. **Detect Conflicts**: If definitions conflict, prefer the most specific and accurate one
4. **Synthesize**: Combine the best elements into a single, authoritative definition

## Formatting Guidelines

### For Methods:
- **Description**: One or two clear sentences explaining what the method does
- **Parameters**: Consolidated descriptions for each parameter (merge insights from all definitions)
- **Returns**: Consolidated description of the return value

### For Properties:
- **Description**: One clear sentence explaining the property's purpose

### For Fields:
- **Description**: One clear sentence explaining the field's purpose

## Important Rules

1. **Do NOT simply pick one definition** - Synthesize a better consolidated version
2. **Preserve technical accuracy** - Do not add information not present in the originals
3. **Prefer specificity** - Choose more specific explanations over vague ones
4. **Maintain brevity** - The consolidated version should not be longer than necessary
5. **Be consistent** - Use consistent terminology across all elements

## Output Format

**CRITICAL**: Your response must contain ONLY valid JSON. Do not include:
- Explanatory text before or after the JSON
- Markdown code blocks (no ``` markers)
- Comments or justifications for your choices
- Any text that is not part of the JSON object

Return ONLY the JSON object matching this structure:

### For Methods:
```json
{{
  "description": "Consolidated description of what the method does",
  "parameters": {{
    "paramName1": "Consolidated description of first parameter",
    "paramName2": "Consolidated description of second parameter"
  }},
  "returns": "Consolidated description of return value (or null if void)"
}}
```

### For Properties:
```json
{{
  "description": "Consolidated description of what this property represents"
}}
```

### For Fields:
```json
{{
  "description": "Consolidated description of what this field stores"
}}
```

## Example

**Element Type**: Method
**Element Name**: `Save`
**Signature**: `bool Save()`

**Definition 1** (from UserRepository.cs):
```json
{{
  "description": "Saves the current user to the database.",
  "returns": "True if save was successful"
}}
```

**Definition 2** (from IRepository.cs interface):
```json
{{
  "description": "Persists changes to the underlying data store.",
  "returns": "Boolean indicating success or failure"
}}
```

**Definition 3** (from EntityBase.cs):
```json
{{
  "description": "Commits all pending changes to storage.",
  "returns": "Success flag"
}}
```

**Good Consolidated Documentation:**
```json
{{
  "description": "Persists all pending changes for the current entity to the underlying data store.",
  "returns": "True if the save operation completed successfully, false otherwise"
}}
```

**Analysis**: The consolidated version:
- Uses "persists" (most technical term from Definition 2)
- Clarifies "current entity" (synthesized from Definitions 1 and 3)
- Provides complete return value explanation (combines insights from all three)

---

Now consolidate the following element:

**Element Type**: {element_type}
**Element Name**: {element_name}
**Element Signature**: {element_signature}
**Number of Definitions**: {definition_count}

**All Definitions**:

{definitions_json}

**IMPORTANT**: Return ONLY the JSON object with your consolidated documentation. No explanations, no markdown formatting, no additional text. Just the raw JSON.
