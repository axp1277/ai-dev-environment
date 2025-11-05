# File: `ContentExtractors/CodeContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `CodeContentExtractor`

A class responsible for extracting content from code files. It implements the IContentExtractor interface and uses a language map to determine if it can extract content based on file extension.

**Purpose:** To provide functionality for extracting structured content (like lines of code) from source files, specifically focusing on code files.

### Methods

  ### `CanExtract`

  Checks if the extractor can process a given input file based on its extension.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (This method does not return any value)

  ### `CodeContentExtractor`

  Extracts content from a code file based on its language and returns it as a CodeContentItem.

  **Parameters:**
  - `languageMap`: A dictionary mapping file extensions to their respective programming languages

  **Returns:** An instance of CodeContentExtractor initialized with the provided language map

  ### `ExtractContent`

  Extracts content from the given input file and returns a CodeContentItem object.

  **Parameters:**
  - `input`: The path to the file containing the content to extract

### Fields

  ### `_languageMap`

  A dictionary that maps file extensions to their corresponding programming languages for content extraction.

