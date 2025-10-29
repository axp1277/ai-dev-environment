# File: `Services/HttpService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `HttpService`

A class responsible for handling HTTP requests and responses using the HttpClient class. It provides asynchronous methods for GET and POST operations.

**Purpose:** To facilitate communication with external APIs or services via HTTP

### Methods

  ### `GetAsync`

  Asynchronously retrieves the content of a webpage at the specified URL.

  **Parameters:**
  - `url`: The Uniform Resource Locator (URL) of the webpage to retrieve.

  **Returns:** null

  ### `HttpService`

  Initializes a new instance of the HttpService class with an internal HttpClient for making HTTP requests.

  ### `PostAsync`

  Sends an asynchronous POST request to the specified URL with the provided HttpContent.

  **Parameters:**
  - `url`: The URI of the resource to send the POST request to
  - `content`: The content to send in the body of the POST request

### Fields

  ### `_httpClient`

  An instance of HttpClient used to send HTTP requests.

