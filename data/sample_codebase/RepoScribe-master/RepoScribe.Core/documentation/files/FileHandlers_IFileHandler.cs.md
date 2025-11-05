# File: `FileHandlers/IFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `IFileHandler`

Defines an interface for handling files based on their extensions and extracting metadata.

**Purpose:** Provides a standard way to process files in RepoScribe

### Methods

  ### `CanHandle`

  Checks if the file handler can process files with the specified extension.

  **Parameters:**
  - `extension`: The file extension to check for

  ### `ProcessFile`

  Processes a file located at the specified path and returns its metadata.

  **Parameters:**
  - `filePath`: The full path to the file being processed

