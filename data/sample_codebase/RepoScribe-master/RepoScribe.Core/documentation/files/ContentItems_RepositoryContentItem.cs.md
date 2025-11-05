# File: `ContentItems/RepositoryContentItem.cs`

**Namespace:** `RepoScribe.Core.ContentItems`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 7
- **Documented:** 7

---

## Class: `RepositoryContentItem`

Represents a content item from a repository, containing details like URL, author, readme, and nested files.

**Purpose:** Provides structure for ingesting and saving repository content items

### Methods

  ### `Ingest`

  Implements repository ingestion logic such as cloning the repo and parsing files.

  ### `SaveAsync`

  Saves the current content item and its nested files asynchronously to both local database and ChromaDB.

### Properties

  ### `Author`

  The author of the repository associated with this content item.

  ### `Files`

  A list of content items representing files associated with this repository

  ### `Readme`

  The markdown content of the repository's README file

  ### `Url`

  The URL of the repository associated with this content item.

