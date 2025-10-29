# File: `Database/AppDbContext.cs`

**Namespace:** `RepoScribe.Core.Database`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 9
- **Documented:** 9

---

## Class: `AppDbContext`

The AppDbContext class is responsible for managing the database context and configurations for RepoScribe's content items. It inherits from DbContext and provides DbSets for each type of content item entity.

**Purpose:** To manage the database context and provide access to various content item entities

### Methods

  ### `AppDbContext`

  Initializes a new instance of the AppDbContext class with the provided DbContextOptions.

  **Parameters:**
  - `options`: The DbContextOptions to use for this context.

  ### `OnModelCreating`

  Configures the model for the database using Fluent API. This includes setting up inheritance and relationships between entities.

  **Parameters:**
  - `modelBuilder`: The ModelBuilder instance used to configure the model

### Properties

  ### `CodeContentItems`

  A DbSet property representing the collection of CodeContentItemEntity objects tracked by the AppDbContext.

  ### `ContentItems`

  A DbSet property that represents the collection of ContentItem entities tracked by this AppDbContext instance.

  ### `ImageContentItems`

  A DbSet property that represents the collection of ImageContentItemEntity objects tracked by the AppDbContext.

  ### `LineContents`

  A DbSet property that represents the collection of LineContentEntity objects tracked by the AppDbContext.

  ### `PdfContentItems`

  A DbSet property that represents the collection of PdfContentItemEntity objects tracked by the AppDbContext.

  ### `RepositoryContentItems`

  A DbSet property that represents the collection of RepositoryContentItemEntity objects tracked by the AppDbContext.

