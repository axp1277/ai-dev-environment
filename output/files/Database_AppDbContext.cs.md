# File: `Database/AppDbContext.cs`

**Namespace:** `RepoScribe.Core.Database`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 9
- **Documented:** 9

---

## Class: `AppDbContext`

Represents the main database context for RepoScribe application, managing various content item entities and their relationships.

**Purpose:** Provides DbSet properties for each entity type to enable querying and manipulation of data in the database.

### Methods

  ### `AppDbContext`

  Initializes a new instance of AppDbContext with the specified DbContextOptions.

  **Parameters:**
  - `options`: The DbContextOptions to use for this context

  ### `OnModelCreating`

  Configures the model for the database using Fluent API.

  **Parameters:**
  - `modelBuilder`: The ModelBuilder instance used to configure the model

### Properties

  ### `CodeContentItems`

  A DbSet property representing the set of CodeContentItemEntity objects tracked by the AppDbContext

  ### `ContentItems`

  A DbSet property representing the set of ContentItem entities tracked by this AppDbContext instance.

  ### `ImageContentItems`

  A DbSet property representing the set of ImageContentItemEntity objects tracked by the AppDbContext

  ### `LineContents`

  A DbSet property representing the collection of LineContentEntity objects tracked by the AppDbContext.

  ### `PdfContentItems`

  A DbSet property representing the collection of PdfContentItemEntity objects in the database

  ### `RepositoryContentItems`

  A DbSet property representing the set of RepositoryContentItemEntity objects in the database

