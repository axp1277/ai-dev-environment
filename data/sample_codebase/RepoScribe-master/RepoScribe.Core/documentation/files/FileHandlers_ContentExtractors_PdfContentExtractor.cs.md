# File: `FileHandlers/ContentExtractors/PdfContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `PdfContentExtractor`

A class responsible for extracting content from PDF files and converting it into a structured format.

**Purpose:** Provides functionality to extract textual content from PDF documents.

### Methods

  ### `CanExtract`

  Checks if the given input file can be extracted by this content extractor.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (no return value)

  ### `ExtractContent`

  Extracts content from a PDF file and returns it as a string.

  **Parameters:**
  - `input`: The path to the PDF file

  ### `ExtractTextFromPdf`

  Extracts and concatenates text from all pages of a PDF file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path to the PDF document

### Fields

  ### `_supportedExtensions`

  List of file extensions that this content extractor supports

