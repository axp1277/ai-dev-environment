# File: `Services/FlattenAllService.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 7
- **Documented:** 7

---

## Class: `FlattenAllService`

Manages and coordinates the Flatten-All process for generating markdown files from Git repositories.

**Purpose:** Coordinates the execution of CodeFlattener.exe on all Git repositories found in the current directory hierarchy.

### Methods

  ### `FlattenAllAsync`

  Asynchronously processes all Git repositories in the current directory and its subdirectories using CodeFlattener.exe, saving output Markdown files to a specified directory.

  ### `FlattenAllService`

  Runs a process to flatten all Git repositories in the current directory and its subdirectories using CodeFlattener.exe.

  **Parameters:**
  - `codeFlattenerPath`: The path to the CodeFlattener.exe file
  - `outputDirectory`: The directory where the output markdown files will be saved
  - `inputProcessor`: An instance of InputProcessor used for processing input data
  - `renderer`: An implementation of IRenderer interface for rendering output

### Fields

  ### `_codeFlattenerPath`

  The file path to the CodeFlattener.exe executable

  ### `_inputProcessor`

  Stores the instance of InputProcessor used for processing input

  ### `_outputDirectory`

  The directory where flattened markdown files are saved

  ### `_renderer`

  The renderer used to generate markdown files from processed directories

