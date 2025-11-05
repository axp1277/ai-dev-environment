# File: `FileHandlers/ContentExtractors/ImageContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `ImageContentExtractor`

Extracts and encapsulates relevant information from image files such as PNG, JPG, JPEG, GIF, BMP.

**Purpose:** Provides image content extraction functionality for RepoScribe

### Methods

  ### `CanExtract`

  Checks if the given input file can be extracted by this content extractor.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (no return value)

  ### `ExtractContent`

  Extracts image content from a file and returns it as an ImageContentItem.

  **Parameters:**
  - `input`: The path to the image file

  **Returns:** null (void)

### Fields

  ### `_supportedExtensions`

  List of supported image file extensions

