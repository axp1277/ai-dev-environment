# File: `Services/OllamaService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `OllamaService`

A service class responsible for communicating with Ollama API to fetch data.

**Purpose:** Provides methods to interact with Ollama API endpoints

### Methods

  ### `GetAsync`

  Asynchronously retrieves data from a specified URL with optional request parameters.

  **Parameters:**
  - `url`: The endpoint URL to retrieve data from
  - `req`: A dictionary of key-value pairs representing request parameters

  ### `OllamaService`

  Initializes a new instance of OllamaService with default HttpClient and base URL.

### Fields

  ### `_baseUrl`

  The base URL for Ollama API requests

  ### `_httpClient`

  An HttpClient instance used for making HTTP requests

