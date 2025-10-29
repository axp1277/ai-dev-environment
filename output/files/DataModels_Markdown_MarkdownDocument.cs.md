# File: `DataModels/Markdown/MarkdownDocument.cs`

**Namespace:** `RepoScribe.Core.DataModels.Markdown`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `MarkdownDocument`

A class representing a Markdown document composed of multiple MarkdownContent sections.

**Purpose:** Used to aggregate and manage MarkdownContent sections for generating a complete Markdown string.

### Methods

  ### `AddContent`

  Appends the provided MarkdownContent to the internal list of contents.

  **Parameters:**
  - `content`: The MarkdownContent to add

  ### `ToString`

  Converts the MarkdownDocument object to its string representation by concatenating all contained MarkdownContent objects.

### Fields

  ### `_contents`

  A private, mutable list storing the individual MarkdownContent items that make up this document.

