# File: `FileHandlers/SqliteFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `SqliteFileHandler`

Handles SQLite file processing and metadata extraction.

**Purpose:** Provides functionality to process SQLite files and retrieve their table names.

### Methods

  ### `CanHandle`

  Checks if the file handler can process files with the given extension by comparing it to a list of supported extensions.

  **Parameters:**
  - `extension`: The file extension (including dot) to check for support

  ### `GetTables`

  Extracts and returns a list of table names from an SQLite database file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path to the SQLite database (.sqlite or .db extension)

  **Returns:** null (void method)

  ### `ProcessFile`

  Processes a SQLite file located at the specified path and returns metadata about it.

  **Parameters:**
  - `filePath`: The full file path of the SQLite database to process

### Fields

  ### `_supportedExtensions`

  List of supported file extensions for SQLite databases

