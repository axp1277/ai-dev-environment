# File: `Services/ChromaDbService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 7
- **Documented:** 7

---

## Class: `ChromaDbService`

A service class responsible for interacting with a ChromaDB instance to perform CRUD operations on ContentItems. It provides a singleton instance for easy access and uses HttpClient for communication.

**Purpose:** Facilitates seamless integration between RepoScribe's ContentItem management and ChromaDB for persistent storage.

### Methods

  ### `ChromaDbService`

  Initializes an instance of ChromaDbService with a new HttpClient and sets the base URL to communicate with ChromaDB.

  **Returns:** An instance of ChromaDbService

  ### `UpsertAsync`

  Asynchronously sends a POST request to upsert (insert or update) the provided ContentItem into ChromaDB.

  **Parameters:**
  - `contentItem`: The ContentItem object containing data to be inserted or updated

  **Returns:** void

### Properties

  ### `Instance`

  The singleton instance of the ChromaDbService class, providing access to shared HttpClient and baseUrl.

### Fields

  ### `_baseUrl`

  The base URL of the ChromaDB service, used to construct API endpoints.

  ### `_httpClient`

  An instance of HttpClient used for making HTTP requests to communicate with the ChromaDB service.

  ### `_instance`

  Lazy-loaded singleton instance of ChromaDbService, ensuring thread safety and efficient initialization.

