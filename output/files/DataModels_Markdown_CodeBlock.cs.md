# File: `DataModels/Markdown/CodeBlock.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `CodeBlock`

A class representing a block of code in Markdown format with a specified language.

**Purpose:** Used to display formatted code blocks within Markdown content.

### Methods

  ### `ApplyTemplate`

  Applies a given Markdown template to the current CodeBlock's content and returns the result.

  **Parameters:**
  - `template`: The Markdown template string to apply

  ### `CodeBlock`

  Creates a new CodeBlock instance with specified language and content.

  **Parameters:**
  - `language`: The programming language for the code block
  - `content`: The actual code to be displayed

  ### `ToMarkdown`

  Converts this CodeBlock instance to Markdown format.

### Properties

  ### `Content`

  The content of the code block as a string

  ### `Language`

  The programming language of the code block

