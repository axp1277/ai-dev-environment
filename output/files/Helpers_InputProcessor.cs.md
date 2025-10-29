# File: `Helpers/InputProcessor.cs`

**Namespace:** `RepoScribe.Core.Helpers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `InputProcessor`

A class responsible for processing input files and extracting content using appropriate extractors.

**Purpose:** Facilitates content extraction from various file types by utilizing registered IContentExtractor implementations.

### Methods

  ### `InputProcessor`

  Initializes an InputProcessor with a list of content extractors.

  **Parameters:**
  - `extractors`: A list of IContentExtractor implementations used to process input files

  **Returns:** null (void)

  ### `ProcessInput`

  Processes the given input string and attempts to extract content using registered IContentExtractor instances.

  **Parameters:**
  - `input`: The input string to process

  **Returns:** null if no extractor can handle the input, otherwise the extracted ContentItem

### Fields

  ### `_extractors`

  A private, readonly list of content extractors used to determine which extractor can process a given input.

