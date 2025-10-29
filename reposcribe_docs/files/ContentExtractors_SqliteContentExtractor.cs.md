# File: `ContentExtractors/SqliteContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `SqliteContentExtractor`

A class responsible for extracting content from SQLite database files. It implements the IContentExtractor interface and supports file extensions like .sqlite, .db, and .sqlite3.

**Purpose:** To extract table names and other relevant information from SQLite databases

### Methods

  ### `CanExtract`

  Checks if the input file has a supported SQLite extension (.sqlite, .db, or .sqlite3) and returns true if it does, false otherwise.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (no return value)

  ### `ExtractContent`

  Extracts content from a SQLite database file located at the provided input path.

  **Parameters:**
  - `input`: The file path of the SQLite database to extract content from.

  ### `GetTables`

  Extracts table names from a SQLite database file located at the given path.

  **Parameters:**
  - `filePath`: The full file path of the SQLite database (.sqlite, .db, or .sqlite3)

  **Returns:** void (This method does not return any value. It populates the 'tables' list with table names.)

### Fields

  ### `_supportedExtensions`

  A list of supported file extensions for SQLite databases that this content extractor can handle.

