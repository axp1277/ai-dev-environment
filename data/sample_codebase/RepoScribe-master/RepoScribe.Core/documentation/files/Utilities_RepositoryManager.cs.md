# File: `Utilities/RepositoryManager.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 5
- **Documented:** 5

---

## Class: `RepositoryManager`

Manages a list of repositories by loading them from a config file and providing methods to save changes.

**Purpose:** Centralizes repository management for RepoScribe application

### Methods

  ### `RepositoryManager`

  Initializes a new instance of RepositoryManager with the specified configuration path and loads repositories from the config file if it exists.

  **Parameters:**
  - `configPath`: The file path to the configuration file containing serialized repository data

  ### `Save`

  Saves the current list of repositories to the configuration file located at _configPath.

### Properties

  ### `Repositories`

  A list of repository URLs managed by this instance

### Fields

  ### `_configPath`

  The file path to the configuration file used by RepositoryManager

