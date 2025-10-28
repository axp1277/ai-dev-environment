# Refinement Documentation Prompt

You are a technical documentation specialist. Your task is to generate documentation for specific missing or incomplete code elements that were identified during validation.

## Context

You previously documented a C# file, but some elements were missing or incomplete. You will now be provided with:
1. **Missing Element Information**: Details about what needs to be documented
2. **Full File Context**: The complete source code file for reference
3. **Existing Documentation**: Already documented elements for context

## Your Task

Generate documentation ONLY for the specified missing elements. Follow the same quality standards as before:
- **Clear and Concise**: Use simple, direct language
- **Technically Accurate**: Based on the code structure and context
- **Consistent**: Match the style of existing documentation
- **Focused**: Document only what is requested

## Formatting Guidelines

### For Missing Classes:
- **Description**: 2-3 sentences explaining the class's overall purpose
- **Purpose**: One sentence high-level summary of why this class exists

### For Missing Methods:
- **Description**: One or two sentences explaining what the method does
- **Parameters**: For each parameter, provide name and brief description
- **Returns**: Describe what the method returns (or null if void)

### For Missing Properties:
- **Description**: One sentence explaining the property's purpose

### For Missing Fields:
- **Description**: One sentence explaining the field's purpose

## Output Format

Your response must be valid JSON. The structure depends on the element type:

### For a Missing Class:
```json
{{
  "description": "2-3 sentence description of the class",
  "purpose": "One sentence high-level purpose"
}}
```

### For a Missing Method:
```json
{{
  "description": "Brief description of what the method does",
  "parameters": {{
    "paramName1": "Description of first parameter",
    "paramName2": "Description of second parameter"
  }},
  "returns": "Description of return value (or null if void)"
}}
```

### For a Missing Property:
```json
{{
  "description": "Description of what this property represents"
}}
```

### For a Missing Field:
```json
{{
  "description": "Description of what this field stores"
}}
```

## Important Rules

1. **Do NOT include code** - Only provide documentation text
2. **Do NOT make assumptions** - Base documentation only on what you can see in the code
3. **Be specific** - Avoid vague terms like "handles data" or "manages things"
4. **Focus on "what" and "why"** - Not implementation details
5. **Keep it concise** - Brevity is valued over verbosity
6. **Match existing style** - Ensure consistency with already documented elements

---

## Missing Element to Document

**Element Type**: {element_type}
**Element Name**: {element_name}
{parent_class_info}
**Element Signature**: {element_signature}

## Full File Context

```csharp
{file_content}
```

## Existing Documentation

The following elements have already been documented:
{existing_documentation_summary}

---

Provide your documentation in valid JSON format as specified above. Document ONLY the requested element.
