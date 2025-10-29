# File: `Utilities/Logger.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `Logger`

A static utility class responsible for initializing and managing Serilog logger instances.

**Purpose:** Centralizes logging setup and teardown operations.

### Methods

  ### `CloseAndFlush`

  Closes the current log stream and flushes all buffered logs to their destinations.

  **Returns:** No return value (void)

  ### `Initialize`

  Initializes the logger with console and file output destinations. The log file will be rolled daily.

