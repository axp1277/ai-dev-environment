# File: `Utilities/PathUtility.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `PathUtility`

A utility class for converting between dotted path notation and standard file system paths.

**Purpose:** Provides helper methods to convert between '.'-separated paths and OS-specific directory separators.

### Methods

  ### `ConvertDottedPathToFilePath`

  Converts a dotted path string (e.g., 'a.b.c') into a file system compatible path by replacing dots with the directory separator character.

  **Parameters:**
  - `dottedPath`: The input path string where dots represent directories

  **Returns:** null (void method)

  ### `ConvertFilePathToDottedPath`

  Converts a standard file path to a dotted path representation.

  **Parameters:**
  - `filePath`: The input file path to convert

  **Returns:** null (void method)

