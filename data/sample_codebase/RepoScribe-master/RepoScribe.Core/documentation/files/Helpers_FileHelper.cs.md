# File: `Helpers/FileHelper.cs`

**Namespace:** `RepoScribe.Core.Helpers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `FileHelper`

A deprecated class that handles file processing using a list of IFileHandler implementations. It determines the appropriate handler based on the file's extension and processes the file if a matching handler is found.

**Purpose:** Provides functionality to process files based on their extensions

### Methods

  ### `FileHelper`

  Processes a file using registered handlers and returns its metadata if handled successfully.

  **Parameters:**
  - `filePath`: The path of the file to process

  **Returns:** FileMetadata object containing details about the processed file, or null if no handler could handle it

  ### `ProcessFile`

  Processes a file using appropriate handlers based on its extension.

  **Parameters:**
  - `filePath`: The path to the file being processed

  **Returns:** null if no handler can process the file

### Fields

  ### `_fileHandlers`

  A list of file handlers used to process files

