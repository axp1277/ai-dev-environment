# File: `Database/Entities/ContentItemEntity.cs`

**Namespace:** `RepoScribe.Core.Database.Entities`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 11
- **Documented:** 11

---

## Class: `ContentItemEntity`

Represents an entity for content items in the database, serving as a base class for specific content types. Stores metadata and content data.

**Purpose:** Defines common properties and behavior for all content entities

### Properties

  ### `Content`

  The content of the item represented as a string.

  ### `ContextSource`

  The source of contextual input for this content item.

  ### `Domain`

  The domain to which this content item belongs.

  ### `Id`

  Unique identifier for the content item entity.

  ### `Language`

  The language of the content represented by this entity, e.g., 'en' for English.

  ### `LastModified`

  The date and time when the content item was last modified.

  ### `Lines`

  A collection of line content entities associated with this content item.

  ### `Owner`

  The username or identifier of the owner of this content item.

  ### `Path`

  The file path of the content item.

  ### `SizeMB`

  The size of the content item in megabytes.

