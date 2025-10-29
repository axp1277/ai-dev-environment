# File: `Services/OllamaService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `OllamaService`

A service class responsible for communicating with the Ollama API to retrieve data.

**Purpose:** Facilitates asynchronous HTTP requests to interact with the Ollama API.

### Methods

  ### `GetAsync`

  Asynchronously retrieves data from the Ollama API using the provided URL and request parameters.

  **Parameters:**
  - `url`: The endpoint URL to retrieve data from
  - `req`: A dictionary containing request parameters

  **Returns:** null (void method)

  ### `OllamaService`

  Initializes a new instance of the OllamaService class with a default HttpClient and base URL.

### Fields

  ### `_baseUrl`

  The base URL for the Ollama API, used to construct full URLs when making requests.

  ### `_httpClient`

  An HttpClient instance used for making HTTP requests to the Ollama API.

