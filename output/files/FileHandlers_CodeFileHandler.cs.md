# File: `FileHandlers/CodeFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `CodeFileHandler`

Handles file processing for code files, providing metadata including language, content, and line details.

**Purpose:** Extracts relevant information from code files

### Methods

  ### `CanHandle`

  Checks if this handler can process files with the given extension by looking up the extension in the language map.

  **Parameters:**
  - `extension`: File extension to check for

  **Returns:** null (void method)

  ### `CodeFileHandler`

  Initializes a CodeFileHandler instance with a language map for file processing.

  **Parameters:**
  - `languageMap`: A dictionary mapping file extensions to their respective programming languages

  ### `ProcessFile`

  Reads a file at the specified path and returns its metadata.

  **Parameters:**
  - `filePath`: The full path to the file

### Fields

  ### `_languageMap`

  A dictionary mapping file extensions to their corresponding programming languages

