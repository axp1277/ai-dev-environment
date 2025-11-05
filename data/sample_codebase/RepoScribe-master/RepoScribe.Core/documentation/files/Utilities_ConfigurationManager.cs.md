# File: `Utilities/ConfigurationManager.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 10
- **Documented:** 10

---

## Class: `ConfigurationManager`

Manages application configuration by loading and providing access to configuration data from various sources such as environment variables, user's home directory, or default application directory.

**Purpose:** Centralizes configuration management for RepoScribe application

### Methods

  ### `ConfigurationManager`

  Initializes a new ConfigurationManager instance with the specified configuration path.

  **Parameters:**
  - `configPath`: The file path to the configuration file

  ### `GetExtractChunksInputDirectory`

  Retrieves the directory path for input files used in chunk extraction process.

  ### `GetIgnoredPaths`

  Retrieves a list of paths to ignore during processing.

  **Returns:** A List<string> containing the ignored paths

  ### `GetLanguageMap`

  Retrieves a dictionary mapping language identifiers to their corresponding display names from the configuration.

### Fields

  ### `_configuration`

  Stores the configuration settings loaded from appsettings.json files or environment variables.

  ### `_defaultConfigPath`

  The default file path for the application's configuration file if none other is specified.

  ### `_envVarConfigPath`

  Stores the configuration path specified via the REPOSCRIBE_CONFIG environment variable

  ### `_homeDirConfigPath`

  The default configuration path for the application if a user has a configuration file in their home directory

