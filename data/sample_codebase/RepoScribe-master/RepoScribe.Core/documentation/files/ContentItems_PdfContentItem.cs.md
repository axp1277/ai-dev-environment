# File: `ContentItems/PdfContentItem.cs`

**Namespace:** `RepoScribe.Core.ContentItems`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 4
- **Documented:** 4

---

## Class: `PdfContentItem`

A specialized content item representing a PDF file with its extracted line contents.

**Purpose:** Stores and manages PDF files along with their textual content for indexing.

### Methods

  ### `Ingest`

  Marks the start of PDF ingestion process by implementing specific PDF ingestion logic.

  ### `SaveAsync`

  Saves the PDF content item asynchronously to both local database and ChromaDB.

### Properties

  ### `Lines`

  A list of LineContent objects representing the lines in the PDF content item.

