# File: `FileHandlers/ContentExtractors/PdfContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `PdfContentExtractor`

A class responsible for extracting content from PDF files. It implements the IContentExtractor interface and supports only PDF file extensions.

**Purpose:** To extract textual content, metadata, and line-by-line structure from PDF documents.

### Methods

  ### `CanExtract`

  Checks if the given input file can be extracted by this content extractor.

  **Parameters:**
  - `input`: The path to the file being checked for extraction

  **Returns:** void (This method does not return a value)

  ### `ExtractContent`

  Extracts and returns the textual content from a PDF file located at the provided input path.

  **Parameters:**
  - `input`: The file path of the PDF document to extract text from

  **Returns:** void (This method does not return any value)

  ### `ExtractTextFromPdf`

  Extracts and concatenates textual content from a PDF file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path of the PDF document to extract text from

  **Returns:** null (void method)

### Fields

  ### `_supportedExtensions`

  A list of file extensions that this content extractor supports, currently only '.pdf'

