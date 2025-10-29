# File: `FileHandlers/ImageFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `ImageFileHandler`

Handles the processing of image files by checking if they are supported and extracting relevant metadata.

**Purpose:** Provides functionality to process image files within the RepoScribe system.

### Methods

  ### `CanHandle`

  Checks if the given file extension is supported by this handler.

  **Parameters:**
  - `extension`: The file extension to check for support (e.g., '.png', '.jpg')

  **Returns:** void (This method does not return a value)

  ### `ProcessFile`

  Processes an image file located at the given path, extracts metadata using SixLabors.ImageSharp library, and returns a FileMetadata object.

  **Parameters:**
  - `filePath`: The full path of the image file to process

### Fields

  ### `_supportedExtensions`

  A list of file extensions that this handler supports for image processing.

