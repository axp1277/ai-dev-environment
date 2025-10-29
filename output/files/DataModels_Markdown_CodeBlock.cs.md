# File: `DataModels/Markdown/CodeBlock.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `CodeBlock`

A class representing a block of code in Markdown format. It includes the programming language and the actual code content.

**Purpose:** Used to embed code snippets within Markdown text

### Methods

  ### `ApplyTemplate`

  Applies a given markdown template to the code block's content and returns the result.

  **Parameters:**
  - `template`: The markdown template to apply. It should contain placeholders (e.g., '{0}') where the code block's content will be inserted.

  **Returns:** A string representing the applied markdown template with the code block's content inserted into the placeholder(s).

  ### `CodeBlock`

  Creates a new CodeBlock instance with the specified programming language and content.

  **Parameters:**
  - `language`: The programming language for the code block (e.g., 'csharp', 'python').
  - `content`: The actual code to be displayed within the block.

  ### `ToMarkdown`

  Converts the CodeBlock instance to its Markdown representation.

  **Returns:** A string containing the Markdown representation of the CodeBlock.

### Properties

  ### `Content`

  The content of the code block represented as a string.

  ### `Language`

  The programming language associated with the code block.

