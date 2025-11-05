# File: `Utilities/HashUtility.cs`

**Namespace:** `RepoScribe.Core.Utilities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `HashUtility`

A utility class for generating SHA-256 hashes and unique IDs from content.

**Purpose:** Provides methods to hash and generate unique IDs from input strings

### Methods

  ### `GetContentHash`

  Calculates and returns a SHA-256 hash of the provided content as a lowercase string without hyphens.

  **Parameters:**
  - `content`: The input string to be hashed

  **Returns:** null (void method)

  ### `GetUniqueId`

  Generates a unique identifier by taking the first 32 characters of the SHA-256 hash of the provided content.

  **Parameters:**
  - `content`: The input string to generate a unique ID from

