# File: `FileHandlers/ContentExtractors/SqliteContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `SqliteContentExtractor`

Extracts content from SQLite databases by retrieving table names and storing them in a PdfContentItem.

**Purpose:** Provides content extraction functionality for SQLite files

### Methods

  ### `CanExtract`

  Checks if the input file has a supported extension for SQLite databases.

  **Parameters:**
  - `input`: The path to the file being checked

  ### `ExtractContent`

  Extracts content from a SQLite database file by retrieving table names and storing them in a PdfContentItem.

  **Parameters:**
  - `input`: Path to the SQLite database file

  ### `GetTables`

  Extracts table names from a SQLite database file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path of the SQLite database

  **Returns:** null (void method)

### Fields

  ### `_supportedExtensions`

  List of supported file extensions for SQLite databases

