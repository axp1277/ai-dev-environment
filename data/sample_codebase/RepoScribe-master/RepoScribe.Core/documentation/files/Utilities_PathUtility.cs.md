# File: `Utilities/PathUtility.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `PathUtility`

A utility class for converting between dotted paths and file system paths.

**Purpose:** Provides methods to convert between dotted path notation used in RepoScribe and standard file system paths.

### Methods

  ### `ConvertDottedPathToFilePath`

  Converts a dotted path string into a file system compatible path by replacing dots with directory separators.

  **Parameters:**
  - `dottedPath`: The input path as a string of components separated by dots

  **Returns:** null (void method)

  ### `ConvertFilePathToDottedPath`

  Converts a file path to a dotted path representation by replacing directory separators with dots.

  **Parameters:**
  - `filePath`: The file path to convert

  **Returns:** null (void method)

