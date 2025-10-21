## RepoScribe Project Documentation

### Layer 1 Data (File Summaries)

1. **Program.cs**
   - **Summary**: This tool flattens a codebase into a Markdown file, processing files within a specified root directory. It extracts information like file paths and content, and outputs a Markdown document with relative paths and code blocks.
   - **Purpose**: Codebase flattening and Markdown generation
   - **Category**: Utility
   - **Key Classes**: Program, RootCommand, FileHelper, CodeFileHandler, FileMetadata

2. **AssemblyInfo.cs**
   - **Summary**: This file is an assembly information file, specifying visibility for internal types. It allows the 'Flattener.Tests' project to access internal components of the current assembly for testing purposes.
   - **Purpose**: Specifies internal assembly visibility for testing
   - **Category**: Build Metadata
   - **Key Classes**: AssemblyInfo

### Layer 2 Data (Detailed Documentation)

#### Program.cs
- **Classes**
  - **Program**: The entry point of the RepoScribe tool, responsible for parsing command-line arguments, initializing logging, and orchestrating the codebase flattening process.
    - Methods:
      - `Main`: Initializes logging, sets up command-line options, and invokes the root command handler to start processing the codebase.
  - **RootCommand**: A command object representing the root command for the RepoScribe tool, which encapsulates options and handlers.
    - Methods:
      - `AddOption`: Adds a specified option to this command.
      - `SetHandler`: Sets the command handler that will be invoked when this root command is executed.
  - **ConfigurationManager**: Manages configuration settings, such as language mappings and ignored paths, loaded from an appsettings.json file.
    - Methods:
      - `GetLanguageMap`: Retrieves the language mapping configuration.
      - `GetIgnoredPaths`: Retrieves a list of paths to ignore during processing.
  - **FileHelper**: Handles file operations, including processing files with registered handlers.
    - Method:
      - `ProcessFile`: Processes a given file path and returns metadata about the file.
  - **CodeFileHandler**: Handles processing of code files, extracting metadata and content.
    - Method:
      - `ProcessFile`: Processes a code file, extracting metadata and content.
  - **FileMetadata**: Represents metadata about a processed file, including its path and content.

#### AssemblyInfo.cs
- **Class**
  - **AssemblyInfo**: This file is an assembly information file, specifying visibility for internal types. It allows the 'Flattener.Tests' project to access internal components of the current assembly for testing purposes.

### Layer 3 Data (Relationships and Architecture)

1. **Program.cs**
   - **Architectural Role**: Utility Application (Command-Line Tool)
   - **Dependencies**:
     - Uses `RootCommand`, `Option`, `ConfigurationManager`, `FileHelper`, `CodeFileHandler`, `FileMetadata` for command-line interface setup and file processing logic.
   - **Dependent Files**: Invoked from the command line for codebase flattening and Markdown generation.

2. **AssemblyInfo.cs**
   - **Architectural Role**: Build Metadata Configuration File
   - **Dependencies**: None
   - **Dependent Files**: Used by `Flattener.Tests/Program.cs` via InternalsVisibleTo attribute to grant access to internal types for testing purposes.