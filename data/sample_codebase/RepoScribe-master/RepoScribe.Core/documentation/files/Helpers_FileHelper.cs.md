# File: `Helpers/FileHelper.cs`

**Namespace:** `RepoScribe.Core.Helpers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `FileHelper`

A deprecated class that provides functionality to process files using a list of file handlers. It determines the appropriate handler based on the file's extension and processes the file if a matching handler is found.

**Purpose:** To facilitate file processing by delegating tasks to specialized file handlers.

### Methods

  ### `FileHelper`

  Processes a file using the appropriate IFileHandler based on its extension, returning FileMetadata if successful or null otherwise.

  **Parameters:**
  - `filePath`: The path to the file being processed

  **Returns:** FileMetadata containing information about the processed file, or null if no handler could process the file

  ### `ProcessFile`

  Processes a file using the appropriate file handler based on its extension, returning the extracted metadata if successful.

  **Parameters:**
  - `filePath`: The path to the file being processed

  **Returns:** null (void)

### Fields

  ### `_fileHandlers`

  A list of file handlers used to process files based on their extensions.

