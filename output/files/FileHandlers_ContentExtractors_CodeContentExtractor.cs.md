# File: `FileHandlers/ContentExtractors/CodeContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `CodeContentExtractor`

Extracts content from code files based on their extensions and language mappings.

**Purpose:** Provides a way to retrieve structured information about code files

### Methods

  ### `CanExtract`

  Checks if the extractor can handle a given input file based on its extension.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** null (void)

  ### `CodeContentExtractor`

  Extracts code content from a file based on its extension and language mapping.

  **Parameters:**
  - `languageMap`: A dictionary containing file extensions as keys and their corresponding programming languages as values

  **Returns:** An instance of CodeContentExtractor that can extract content from files matching the provided language map

  ### `ExtractContent`

  Extracts content from a file and returns it as a CodeContentItem.

  **Parameters:**
  - `input`: The path to the file containing the content

### Fields

  ### `_languageMap`

  Stores a mapping of file extensions to programming languages for content extraction

