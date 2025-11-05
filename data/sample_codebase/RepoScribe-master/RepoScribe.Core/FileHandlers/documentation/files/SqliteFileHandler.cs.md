# File: `SqliteFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `SqliteFileHandler`

Handles file processing for SQLite databases. It checks if the file can be handled based on its extension, extracts table information from the database, and generates a FileMetadata object.

**Purpose:** Provides functionality to process SQLite files within the RepoScribe application

### Methods

  ### `CanHandle`

  Checks if the file handler can process files with the given extension by verifying if it's included in the list of supported extensions.

  **Parameters:**
  - `extension`: The file extension to check for support

  **Returns:** void (no return value)

  ### `GetTables`

  Extracts the names of all tables from a SQLite database file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path to the SQLite database (.sqlite, .db, or .sqlite3)

  **Returns:** void (This method does not return any value. It populates the 'tables' list with table names.)

  ### `ProcessFile`

  Processes a SQLite database file located at the given path, extracts table names, and returns metadata about the file.

  **Parameters:**
  - `filePath`: The full file path of the SQLite database to process

  **Returns:** void (This method does not return any value)

### Fields

  ### `_supportedExtensions`

  A list of supported file extensions for SQLite databases that this handler can process.

