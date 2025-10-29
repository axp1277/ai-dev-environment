# File: `FileHandlers/ContentExtractors/ImageContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `ImageContentExtractor`

A class responsible for extracting relevant information from image files. It supports various image formats and retrieves metadata such as owner, last modified time, size, and image-specific metadata.

**Purpose:** To extract structured content from image files for processing within the RepoScribe system.

### Methods

  ### `CanExtract`

  Checks if the given input file can be extracted by this content extractor based on its extension.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (This method does not return a value)

  ### `ExtractContent`

  Extracts image content from the given input file path and returns an ImageContentItem object.

  **Parameters:**
  - `input`: The file path of the image to extract content from

  **Returns:** null (void method)

### Fields

  ### `_supportedExtensions`

  A list of supported image file extensions that this extractor can handle.

