# File: `Services/ChromaDbService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 7
- **Documented:** 7

---

## Class: `ChromaDbService`

A service class responsible for interacting with a ChromaDB instance to perform CRUD operations on content items.

**Purpose:** Provides methods to upsert (insert or update), query, and delete content items in ChromaDB.

### Methods

  ### `ChromaDbService`

  Initializes a new instance of the ChromaDbService class with an HttpClient and base URL for communicating with ChromaDB.

  ### `UpsertAsync`

  Asynchronously sends a POST request to upsert (insert or update) the provided ContentItem into ChromaDB.

  **Parameters:**
  - `contentItem`: The ContentItem object containing data to be inserted or updated

### Properties

  ### `Instance`

  The singleton instance of the ChromaDbService class

### Fields

  ### `_baseUrl`

  The base URL of the ChromaDB service

  ### `_httpClient`

  An instance of HttpClient used to make HTTP requests to communicate with ChromaDB

  ### `_instance`

  Lazy-loaded singleton instance of ChromaDbService

