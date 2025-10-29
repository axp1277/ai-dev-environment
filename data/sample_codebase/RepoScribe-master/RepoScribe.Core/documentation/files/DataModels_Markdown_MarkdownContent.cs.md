# File: `DataModels/Markdown/MarkdownContent.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `MarkdownContent`

An abstract base class for generating Markdown content with templating capabilities.

**Purpose:** Provides a common interface for converting content to Markdown and applying templates.

### Methods

  ### `ApplyTemplate`

  Applies a given template string to the Markdown content represented by this instance.

  **Parameters:**
  - `template`: A string containing placeholders (e.g., '{0}') where Markdown content will be inserted

  ### `ToMarkdown`

  Converts the MarkdownContent object into its Markdown representation.

  ### `ToString`

  Overrides the default ToString() method to return the Markdown representation of this content.

