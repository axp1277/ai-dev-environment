# File: `Utilities/HashUtility.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `HashUtility`

A utility class for generating hashes and unique IDs from content using SHA256 algorithm.

**Purpose:** Provides methods to hash content securely and generate unique IDs.

### Methods

  ### `GetContentHash`

  Calculates the SHA-256 hash of the provided content string and returns it as a lowercase hexadecimal string without hyphens.

  **Parameters:**
  - `content`: The input string for which to calculate the hash

  **Returns:** null (void method)

  ### `GetUniqueId`

  Generates a unique identifier by taking the first 32 characters of the SHA-256 hash of the provided content.

  **Parameters:**
  - `content`: The input string to generate the unique ID from

  **Returns:** null (void method)

