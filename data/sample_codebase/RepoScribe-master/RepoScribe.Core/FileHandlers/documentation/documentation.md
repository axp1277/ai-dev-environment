# Code Documentation

**Generated:** 2025-10-28 16:10:29
**Source Directory:** `data/sample_codebase/RepoScribe-master/RepoScribe.Core/FileHandlers`

---

# Documentation Summary

## Overall Metrics

- **Total Files:** 9
- **Complete Files:** 9
- **Average Coverage:** 88.9%
- **Total Elements:** 38
- **Documented Elements:** 38

## Per-File Coverage

| File | Coverage | Elements | Status |
|------|----------|----------|--------|
| `CodeFileHandler.cs` | 100.0% | 5/5 | ✓ Complete |
| `ContentExtractors/CodeContentExtractor.cs` | 100.0% | 5/5 | ✓ Complete |
| `ContentExtractors/ImageContentExtractor.cs` | 100.0% | 4/4 | ✓ Complete |
| `ContentExtractors/PdfContentExtractor.cs` | 100.0% | 5/5 | ✓ Complete |
| `ContentExtractors/SqliteContentExtractor.cs` | 100.0% | 5/5 | ✓ Complete |
| `IFileHandler.cs` | 0.0% | 0/0 | ✓ Complete |
| `ImageFileHandler.cs` | 100.0% | 4/4 | ✓ Complete |
| `PdfFileHandler.cs` | 100.0% | 5/5 | ✓ Complete |
| `SqliteFileHandler.cs` | 100.0% | 5/5 | ✓ Complete |

---

# Table of Contents

## ContentExtractors

- [ContentExtractors/CodeContentExtractor.cs](#contentextractors-codecontentextractor-cs)
  - [`CodeContentExtractor`](#contentextractors-codecontentextractor-cs-class-codecontentextractor)
- [ContentExtractors/ImageContentExtractor.cs](#contentextractors-imagecontentextractor-cs)
  - [`ImageContentExtractor`](#contentextractors-imagecontentextractor-cs-class-imagecontentextractor)
- [ContentExtractors/PdfContentExtractor.cs](#contentextractors-pdfcontentextractor-cs)
  - [`PdfContentExtractor`](#contentextractors-pdfcontentextractor-cs-class-pdfcontentextractor)
- [ContentExtractors/SqliteContentExtractor.cs](#contentextractors-sqlitecontentextractor-cs)
  - [`SqliteContentExtractor`](#contentextractors-sqlitecontentextractor-cs-class-sqlitecontentextractor)

## Root

- [CodeFileHandler.cs](#codefilehandler-cs)
  - [`CodeFileHandler`](#codefilehandler-cs-class-codefilehandler)
- [IFileHandler.cs](#ifilehandler-cs)
- [ImageFileHandler.cs](#imagefilehandler-cs)
  - [`ImageFileHandler`](#imagefilehandler-cs-class-imagefilehandler)
- [PdfFileHandler.cs](#pdffilehandler-cs)
  - [`PdfFileHandler`](#pdffilehandler-cs-class-pdffilehandler)
- [SqliteFileHandler.cs](#sqlitefilehandler-cs)
  - [`SqliteFileHandler`](#sqlitefilehandler-cs-class-sqlitefilehandler)

---

# Detailed Documentation

# File: `CodeFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `CodeFileHandler`

A deprecated class for handling code files and extracting metadata. It maps file extensions to programming languages and retrieves file details such as owner, last modified time, size, language, content, and line contents.

**Purpose:** To handle and process code files by retrieving relevant metadata

### Methods

  ### `CanHandle`

  Checks if the CodeFileHandler can handle files with the given extension by looking up the extension in its language map.

  **Parameters:**
  - `extension`: The file extension to check for (e.g., '.cs', '.js')

  **Returns:** void (no return value)

  ### `CodeFileHandler`

  Initializes a CodeFileHandler instance with a language map for file processing.

  **Parameters:**
  - `languageMap`: A dictionary mapping file extensions to their respective programming languages

  ### `ProcessFile`

  Reads a file from the specified path and returns its metadata including owner, last modified time, size, language (if mapped), content, and line contents.

  **Parameters:**
  - `filePath`: The full path of the file to process

  **Returns:** null (void method)

### Fields

  ### `_languageMap`

  A dictionary that maps file extensions to their corresponding programming languages for identification of the language used in a given file.



---

# File: `ContentExtractors/CodeContentExtractor.cs`

**Namespace:** `RepoScribe.Core.FileHandlers.ContentExtractors`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `CodeContentExtractor`

A class responsible for extracting content from code files. It implements the IContentExtractor interface and uses a language map to determine if it can extract content based on file extension.

**Purpose:** To provide functionality for extracting structured content (like lines of code) from source files, specifically focusing on code files.

### Methods

  ### `CanExtract`

  Checks if the extractor can process a given input file based on its extension.

  **Parameters:**
  - `input`: The path to the file being checked

  **Returns:** void (This method does not return any value)

  ### `CodeContentExtractor`

  Extracts content from a code file based on its language and returns it as a CodeContentItem.

  **Parameters:**
  - `languageMap`: A dictionary mapping file extensions to their respective programming languages

  **Returns:** An instance of CodeContentExtractor initialized with the provided language map

  ### `ExtractContent`

  Extracts content from the given input file and returns a CodeContentItem object.

  **Parameters:**
  - `input`: The path to the file containing the content to extract

### Fields

  ### `_languageMap`

  A dictionary that maps file extensions to their corresponding programming languages for content extraction.



---

# File: `ContentExtractors/ImageContentExtractor.cs`

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



---

# File: `ContentExtractors/PdfContentExtractor.cs`

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



---

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



---

# File: `IFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 0.0%
- **Total Elements:** 0
- **Documented:** 0


---

# File: `ImageFileHandler.cs`

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



---

# File: `PdfFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `PdfFileHandler`

Handles processing of PDF files, extracting text content and metadata.

**Purpose:** Implements the IFileHandler interface to process PDF files specifically.

### Methods

  ### `CanHandle`

  Checks if the file handler can process files with the given extension by comparing it to the list of supported extensions.

  **Parameters:**
  - `extension`: The file extension (e.g., '.pdf') to check for

  **Returns:** void (no return value)

  ### `ExtractTextFromPdf`

  Extracts and appends the textual content from a PDF file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path of the PDF document to extract text from

  **Returns:** void (This method does not return any value)

  ### `ProcessFile`

  Processes a PDF file located at the given path, extracting its textual content and creating a FileMetadata object.

  **Parameters:**
  - `filePath`: The full file path of the PDF document to process

  **Returns:** null (void method)

### Fields

  ### `_supportedExtensions`

  A list of file extensions that this handler can process, currently only supports PDF files.



---

# File: `SqliteFileHandler.cs`

**Namespace:** `RepoScribe.Core.FileHandlers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `SqliteFileHandler`

Handles file processing for SQLite databases. It checks if the file can be handled based on its extension, extracts table information from the database, and generates a FileMetadata object.

**Purpose:** Provides functionality to process SQLite files within the RepoScribe application

### Methods

  ### `CanHandle`

  Checks if the file handler can process files with the given extension by verifying if it's included in the list of supported extensions.

  **Parameters:**
  - `extension`: The file extension to check for support

  **Returns:** void (no return value)

  ### `GetTables`

  Extracts the names of all tables from a SQLite database file located at the specified path.

  **Parameters:**
  - `filePath`: The full file path to the SQLite database (.sqlite, .db, or .sqlite3)

  **Returns:** void (This method does not return any value. It populates the 'tables' list with table names.)

  ### `ProcessFile`

  Processes a SQLite database file located at the given path, extracts table names, and returns metadata about the file.

  **Parameters:**
  - `filePath`: The full file path of the SQLite database to process

  **Returns:** void (This method does not return any value)

### Fields

  ### `_supportedExtensions`

  A list of supported file extensions for SQLite databases that this handler can process.



---
