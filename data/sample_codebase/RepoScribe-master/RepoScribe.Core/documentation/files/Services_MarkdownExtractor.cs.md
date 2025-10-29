# File: `Services/MarkdownExtractor.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `MarkdownExtractor`

MarkdownExtractor is a class responsible for extracting code blocks from markdown files located within a specified directory.

**Purpose:** This class exists to facilitate the retrieval of code snippets embedded within markdown files.

### Methods

  ### `ExtractCodeBlocks`

  Extracts code blocks from markdown files located within the input directory, using regular expressions to match and extract code block sections.

  ### `MarkdownExtractor`

  Extracts code blocks from markdown files located within the specified input directory.

  **Parameters:**
  - `inputDirectory`: The directory containing the markdown files to extract code blocks from.

  **Returns:** An enumerable of JSON strings, each string representing a code block object with properties Id (unique identifier), Path (relative path to the code block), and Content (the actual code content).

### Fields

  ### `_inputDirectory`

  Stores the input directory path where markdown files are located

