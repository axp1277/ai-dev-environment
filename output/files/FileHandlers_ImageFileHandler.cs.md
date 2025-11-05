# File: `FileHandlers/ImageFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `ImageFileHandler`

Handles processing and metadata extraction for image files with supported extensions.

**Purpose:** Provides file handling capabilities specifically for image files.

### Methods

  ### `CanHandle`

  Checks if the specified file extension is supported by this handler.

  **Parameters:**
  - `extension`: The file extension to check for support

  ### `ProcessFile`

  Processes a file by loading its image data and extracting metadata.

  **Parameters:**
  - `filePath`: The path to the file being processed

### Fields

  ### `_supportedExtensions`

  List of file extensions that this handler supports

