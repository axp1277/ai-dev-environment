# File: `DataModels/FileMetadata.cs`

**Namespace:** `RepoScribe.Core.DataModels`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 8
- **Documented:** 8

---

## Class: `FileMetadata`

Represents metadata associated with a file including its path, owner, modification details, size, language, content, and line contents.

**Purpose:** Stores comprehensive information about a file for processing within RepoScribe

### Properties

  ### `Content`

  The content of the file as a string

  ### `Language`

  The programming language of the file's content

  ### `LastModified`

  The date and time when the file was last modified

  ### `Lines`

  A list of LineContent objects representing each line in the file

  ### `Owner`

  The user or entity that owns this file

  ### `Path`

  The file path of this metadata

  ### `SizeMB`

  The size of the file in megabytes

