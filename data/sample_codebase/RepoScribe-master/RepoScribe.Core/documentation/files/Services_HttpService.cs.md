# File: `Services/HttpService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `HttpService`

A service class for making HTTP requests using the HttpClient class.

**Purpose:** Provides methods to perform GET and POST operations.

### Methods

  ### `GetAsync`

  Asynchronously retrieves data from the specified URL using an HTTP GET request.

  **Parameters:**
  - `url`: The Uniform Resource Locator (URL) to retrieve data from

  **Returns:** null (void)

  ### `HttpService`

  Initializes a new instance of HttpService with an HttpClient for making HTTP requests.

  ### `PostAsync`

  Sends an asynchronous POST request to the specified URL with the provided content.

  **Parameters:**
  - `url`: The URI to send the POST request to
  - `content`: The HttpContent containing data to be sent in the POST request

### Fields

  ### `_httpClient`

  An instance of HttpClient used for making HTTP requests

