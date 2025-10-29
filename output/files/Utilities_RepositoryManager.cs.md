# File: `Utilities/RepositoryManager.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `RepositoryManager`

Manages a list of repositories by loading them from a config file and providing methods to save changes back to the file. Uses Newtonsoft.Json for serialization.

**Purpose:** Centralizes repository management within the application

### Methods

  ### `RepositoryManager`

  Initializes a new instance of the RepositoryManager class with the given configuration path.

  **Parameters:**
  - `configPath`: The file path to the JSON configuration file containing repository URLs.

  ### `Save`

  Saves the current list of repositories to the configuration file located at _configPath.

### Properties

  ### `Repositories`

  A list of repository URLs managed by the RepositoryManager.

### Fields

  ### `_configPath`

  The file path to the configuration file used by this instance of RepositoryManager.

