# File: `DataModels/Markdown/Header.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `Header`

A class representing a markdown header with customizable level and text.

**Purpose:** Used to create headers for markdown content.

### Methods

  ### `ApplyTemplate`

  Applies a given Markdown template to the current Header instance and returns the result.

  **Parameters:**
  - `template`: The Markdown template string to apply. It should contain placeholders (e.g., '{0}') where the Header's content will be inserted.

  **Returns:** A formatted string that represents the applied template with the current Header's content.

  ### `Header`

  Creates a new Header instance with the specified level and text.

  **Parameters:**
  - `level`: The header level (1-6)
  - `text`: The header text

  ### `ToMarkdown`

  Converts the Header object to its Markdown representation and returns it as a string.

  **Returns:** A string representing the Header in Markdown format

### Properties

  ### `Level`

  The level of the header (1-6), indicating its importance and hierarchy.

  ### `Text`

  The textual content of the header

