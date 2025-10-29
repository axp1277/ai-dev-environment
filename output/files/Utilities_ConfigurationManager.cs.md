# File: `Utilities/ConfigurationManager.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 10
- **Documented:** 10

---

## Class: `ConfigurationManager`

Manages application configuration by loading and providing access to configuration data. It supports multiple sources including environment variables, user's home directory, and the default application directory.

**Purpose:** Centralizes configuration management for RepoScribe application

### Methods

  ### `ConfigurationManager`

  Initializes a new instance of ConfigurationManager with the specified configuration path.

  **Parameters:**
  - `configPath`: The file path to the configuration file

  ### `GetExtractChunksInputDirectory`

  Retrieves the directory path for input files used in the ExtractChunks process.

  **Returns:** The directory path as a string, or the default path if not configured.

  ### `GetIgnoredPaths`

  Retrieves a list of paths that should be ignored during processing.

  **Returns:** A List<string> containing the paths to ignore

  ### `GetLanguageMap`

  Retrieves a dictionary mapping language identifiers to their corresponding display names from the configuration.

  **Returns:** A Dictionary<string, string> where keys are language identifiers and values are their display names

### Fields

  ### `_configuration`

  Stores the configuration settings loaded from appsettings.json files or environment variables.

  ### `_defaultConfigPath`

  The default file path for the application's configuration file if no other paths are specified or found.

  ### `_envVarConfigPath`

  Stores the path to the configuration file if set as an environment variable with the key 'REPOSCRIBE_CONFIG'. If not set, it defaults to an empty string.

  ### `_homeDirConfigPath`

  The default configuration path for the application, looking for a user-specific appsettings.json file in the MyDocuments folder.

