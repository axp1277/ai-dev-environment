### 5.1.1.1 RepoScribe

This module contains the core functionality of the RepoScribe tool, which flattens a codebase into a Markdown file by processing files within a specified root directory. It extracts information like file paths and content, and outputs a Markdown document with relative paths and code blocks.

#### 5.1.1.1.1 Dependencies

**Internal Modules:**
- **RepoScribe.Program**: Command-line interface setup and file processing logic
- **RepoScribe.ConfigurationManager**: Manages configuration settings like language mappings and ignored paths
- **RepoScribe.FileHelper**: Handles file operations, including processing files with registered handlers
- **RepoScribe.CodeFileHandler**: Handles processing of code files, extracting metadata and content

**Standalone Methods:**
- **Logger.Initialize**: Initializes the logging system.
- **Path.GetFullPath**: Resolves a path to its full form, handling relative paths.
- **Path.GetFileName**: Extracts the file name from a given path.
- **Directory.EnumerateFiles**: Enumerates files in a directory matching a specified pattern.
- **Directory.Exists**: Checks if a directory exists.
- **Environment.ExpandEnvironmentVariables**: Expands environment variables in a given path string.
- **File.WriteAllText**: Writes all text to a specified file.
- **Log.Information**, **Log.Error**, **Log.Warning**: Log messages with different severity levels.
- **Log.CloseAndFlush**: Closes and flushes the logging system.

#### 5.1.1.1.2 Classes

**5.1.1.1.2.1 Program**

The entry point of the RepoScribe tool, responsible for parsing command-line arguments, initializing logging, and orchestrating the codebase flattening process.

- **Main (int Main(string[] args))**: The main method that initializes logging, sets up command-line options, and invokes the root command handler to start processing the codebase.
  - Parameters: `args` (string[])
  - Returns: int

**5.1.1.1.2.2 RootCommand**

A command object representing the root command for the RepoScribe tool, which encapsulates options and handlers.

- **AddOption (void AddOption(Option<T> option))**: Adds a specified option to this command.
  - Parameters: `option` (Option<T>)
  - Returns: void

- **SetHandler (void SetHandler(Action<string[], string?, bool> handler))**: Sets the command handler that will be invoked when this root command is executed.
  - Parameters: `handler` (Action<string[], string?, bool>)
  - Returns: void

**5.1.1.1.2.3 Option**

Represents an option that can be specified when invoking a command.

- **No methods**

**5.1.1.1.2.4 ConfigurationManager**

Manages configuration settings, such as language mappings and ignored paths, loaded from an appsettings.json file.

- **GetLanguageMap (Dictionary<string, string> GetLanguageMap())**: Retrieves the language mapping configuration.
  - Parameters: None
  - Returns: Dictionary<string, string>

- **GetIgnoredPaths (List<string> GetIgnoredPaths())**: Retrieves a list of paths to ignore during processing.
  - Parameters: None
  - Returns: List<string>

**5.1.1.1.2.5 FileHelper**

Handles file operations, including processing files with registered handlers.

- **ProcessFile (FileMetadata ProcessFile(string filePath))**: Processes a given file path and returns metadata about the file.
  - Parameters: `filePath` (string)
  - Returns: FileMetadata

**5.1.1.1.2.6 CodeFileHandler**

Handles processing of code files, extracting metadata and content.

- **ProcessFile (FileMetadata ProcessFile(string filePath))**: Processes a code file, extracting metadata and content.
  - Parameters: `filePath` (string)
  - Returns: FileMetadata

**5.1.1.1.2.7 FileMetadata**

Represents metadata about a processed file, including its path and content.

- **No methods**

### 5.1.1.2 RepoScribe.AssemblyInfo

This module contains the AssemblyInfo.cs file, which is an assembly information file specifying visibility for internal types. It allows the 'Flattener.Tests' project to access internal components of the current assembly for testing purposes.

#### 5.1.1.2.1 Dependencies

**5.1.1.2.1.1 Flattener.Tests**

The 'Flattener.Tests' project uses the AssemblyInfo.cs file to grant visibility to its internal types and members for testing purposes.

- **How Used**: The InternalsVisibleTo attribute grants internal types and members visibility to Flattener.Tests for testing purposes.
  - Relationship Type: Used by