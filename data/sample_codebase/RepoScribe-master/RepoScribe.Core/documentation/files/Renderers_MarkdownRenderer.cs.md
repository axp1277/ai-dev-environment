# File: `Renderers/MarkdownRenderer.cs`

**Namespace:** `RepoScribe.Core.Renderers`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 3
- **Documented:** 3

---

## Class: `MarkdownRenderer`

A class responsible for converting various content items into Markdown format. It supports rendering CodeContentItem, with plans to extend support for ImageContentItem, PdfContentItem, and RepositoryContentItem.

**Purpose:** To facilitate the conversion of diverse content types into a standardized Markdown format for easier integration with other systems.

### Methods

  ### `Render`

  Renders a given ContentItem into Markdown format based on the provided template. If no template is provided, it uses a default structure.

  **Parameters:**
  - `contentItem`: The content item to render. It can be of type CodeContentItem, ImageContentItem, PdfContentItem, or RepositoryContentItem.
  - `template`: An optional Markdown template to apply to the rendered content.

  **Returns:** A string representing the rendered Markdown content

