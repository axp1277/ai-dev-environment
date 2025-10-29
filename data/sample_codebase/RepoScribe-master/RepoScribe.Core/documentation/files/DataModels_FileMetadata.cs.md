# File: `DataModels/FileMetadata.cs`

**Namespace:** `RepoScribe.Core.DataModels`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 8
- **Documented:** 8

---

## Class: `FileMetadata`

Represents metadata associated with a file, including its path, owner, modification details, size, language, content, and line contents.

**Purpose:** Used to store and manage comprehensive information about files within the application.

### Properties

  ### `Content`

  The textual content of the file.

  ### `Language`

  The primary language used in the file, if applicable.

  ### `LastModified`

  The date and time when the file was last modified.

  ### `Lines`

  A list of LineContent objects representing the individual lines of content within the file.

  ### `Owner`

  The username or identifier of the user who owns this file.

  ### `Path`

  The file path of the metadata.

  ### `SizeMB`

  The size of the file in megabytes.

