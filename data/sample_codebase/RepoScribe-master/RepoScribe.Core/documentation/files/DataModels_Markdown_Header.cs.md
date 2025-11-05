# File: `DataModels/Markdown/Header.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `Header`

A class representing a header in Markdown format with specified level and text.

**Purpose:** Used to create headers for Markdown content

### Methods

  ### `ApplyTemplate`

  Applies a given Markdown template to the current Header instance.

  **Parameters:**
  - `template`: The Markdown template string to apply

  ### `Header`

  Creates a new Header instance with specified level and text.

  **Parameters:**
  - `level`: The header level (1-6)
  - `text`: The header text

  ### `ToMarkdown`

  Converts this Header instance to Markdown format.

### Properties

  ### `Level`

  The level of heading for this header (1-6)

  ### `Text`

  The textual content of the header

