# File: `Services/FlattenAllService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 7
- **Documented:** 7

---

## Class: `FlattenAllService`

Manages the Flatten-All process, which involves finding Git repositories, running CodeFlattener.exe on them, and saving the output to a specified directory. It tracks progress and logs results.

**Purpose:** Coordinates the Flatten-All operation for generating markdown files from code directories

### Methods

  ### `FlattenAllAsync`

  Asynchronously processes all Git repositories found within the current directory and its subdirectories, using CodeFlattener.exe to generate markdown files for each repository's code. The generated markdown files are saved to the specified output directory.

  ### `FlattenAllService`

  Runs the Flatten-All process to generate markdown files for all Git repositories found within the current directory and its subdirectories.

  **Parameters:**
  - `codeFlattenerPath`: The path to the CodeFlattener.exe file
  - `outputDirectory`: The directory where generated markdown files will be saved
  - `inputProcessor`: An instance of InputProcessor used for processing input data
  - `renderer`: An implementation of IRenderer interface for rendering output

### Fields

  ### `_codeFlattenerPath`

  The file path to the CodeFlattener.exe used for processing directories.

  ### `_inputProcessor`

  Stores the instance of InputProcessor used for processing input files.

  ### `_outputDirectory`

  The output directory where the flattened markdown files will be saved.

  ### `_renderer`

  Stores the instance of IRenderer used for rendering markdown files.

