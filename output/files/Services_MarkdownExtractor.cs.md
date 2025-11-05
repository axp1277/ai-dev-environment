# File: `Services/MarkdownExtractor.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `MarkdownExtractor`

A deprecated class that extracts code blocks from Markdown files in a specified directory and returns them as serialized JSON objects.

**Purpose:** Used for extracting and processing code snippets embedded within Markdown files.

### Methods

  ### `ExtractCodeBlocks`

  Extracts code blocks from Markdown files in the specified directory and yields them as serialized JSON objects.

  **Returns:** IEnumerable<string> containing serialized JSON objects representing extracted code blocks

  ### `MarkdownExtractor`

  Extracts code blocks from Markdown files in a specified directory and returns them as serialized JSON objects.

  **Parameters:**
  - `inputDirectory`: The directory containing the Markdown files to extract code blocks from

  **Returns:** IEnumerable<string> representing the extracted code blocks serialized as JSON

### Fields

  ### `_inputDirectory`

  The input directory path where Markdown files are located

