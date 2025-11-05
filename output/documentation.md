================================================================================
CODE DOCUMENTATION
================================================================================
Generated: 2025-10-29 10:24:56
Source Directory: data/sample_codebase/RepoScribe-master/RepoScribe.Core

================================================================================
Section 1
================================================================================
5.1 RepoScribe

Module containing 56 file(s) with related functionality.

5.1.1 Dependencies

No external dependencies.

5.1.2 Classes

5.1.2.1 IContentExtractor

Namespace: RepoScribe.Core.Abstractions

Defines an interface for extracting content items from a given string input.

Methods:

- void CanExtract(object param): Checks if the given input can be extracted as content.
    input: The string to check for extraction
- void ExtractContent(object param): Extracts content from a given string input.
    input: The string containing the content to extract

5.1.2.2 IInputSource

Namespace: RepoScribe.Core.Abstractions

Defines an input source for retrieving content items.

Methods:

- void GetContentItem(): Retrieves a content item from the input source.

5.1.2.3 IRenderer

Namespace: RepoScribe.Core.Abstractions

Defines an interface for rendering a ContentItem into a string representation.

Methods:

- void Render(object param): Renders a ContentItem into its string representation.
    contentItem: The ContentItem to render

5.1.2.4 ITemplateRenderer

Namespace: RepoScribe.Core.Abstractions
Interfaces: IRenderer

Defines an interface for rendering content items using a specified template.

Methods:

- void Render(object param, object param): Renders a ContentItem using the specified template.
    contentItem: The content item to render
    template: The name of the template to use for rendering

5.1.2.5 CodeContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents a content item of type code with associated lines.

Properties:

- List<LineContent> Lines: A list of LineContent objects representing the individual lines of code in this content item.

Methods:

- void Ingest(): Marks the start of code ingestion process for this content item.
- void SaveAsync(): Saves the current instance of CodeContentItem to both local database and ChromaDB asynchronously.

5.1.2.6 ContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: Metadata

An abstract base class representing a content item with metadata, ingestion, saving, and rendering capabilities.

Properties:

- ContextualInputSource ContextSource: The source of contextual input for this content item
- Domain Domain: The domain to which this content item belongs
- Guid Id: Unique identifier for this content item

Methods:

- void GetSummary(): Retrieves a summary representation of this content item.
- void Ingest(): Default implementation of Ingest method that throws a NotImplementedException.
- void RenderAs(object param): Renders this content item using the provided IRenderer implementation.
    renderer: An instance of IRenderer to use for rendering
- void Save(): Saves the current state of the content item to its underlying data store.
- void SaveAsync(): Asynchronously saves the current state of the content item to its underlying data store.

5.1.2.7 ImageContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents an image content item with metadata and binary data.

Properties:

- byte[] ImageData: Stores the binary data of the image
- string ImageMetadata: Represents metadata associated with an image content item

Methods:

- void Ingest(): Implements image ingestion logic for the current ImageContentItem instance.
- void SaveAsync(): Saves the current instance of ImageContentItem asynchronously to both LocalDatabaseService and ChromaDbService.

5.1.2.8 PdfContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

A specialized content item representing a PDF file with its extracted line contents.

Properties:

- List<LineContent> Lines: A list of LineContent objects representing the lines in the PDF content item.

Methods:

- void Ingest(): Marks the start of PDF ingestion process by implementing specific PDF ingestion logic.
- void SaveAsync(): Saves the PDF content item asynchronously to both local database and ChromaDB.

5.1.2.9 RepositoryContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents a content item from a repository, containing details like URL, author, readme, and nested files.

Properties:

- string Author: The author of the repository associated with this content item.
- List<ContentItem> Files: A list of content items representing files associated with this repository
- string Readme: The markdown content of the repository's README file
- string Url: The URL of the repository associated with this content item.

Methods:

- void Ingest(): Implements repository ingestion logic such as cloning the repo and parsing files.
- void SaveAsync(): Saves the current content item and its nested files asynchronously to both local database and ChromaDB.

5.1.2.10 CacheEntry

Namespace: RepoScribe.Core.DataModels

Represents a cache entry containing cluster indices and keywords associated with a specific keyword embedding.

Properties:

- Guid CacheEntryId: Unique identifier for this cache entry
- List<ClusterIndex> ClusterIndices: A list of ClusterIndex objects associated with this CacheEntry.
- Guid KeyWordEmbeddingId: Unique identifier for the keyword embedding associated with this cache entry
- string[] KeyWords: An array of keywords associated with this cache entry

5.1.2.11 FileMetadata

Namespace: RepoScribe.Core.DataModels

Represents metadata associated with a file including its path, owner, modification details, size, language, content, and line contents.

Properties:

- string Content: The content of the file as a string
- string Language: The programming language of the file's content
- DateTime LastModified: The date and time when the file was last modified
- List<LineContent> Lines: A list of LineContent objects representing each line in the file
- string Owner: The user or entity that owns this file
- string Path: The file path of this metadata
- double SizeMB: The size of the file in megabytes

5.1.2.12 LineContent

Namespace: RepoScribe.Core.DataModels

Represents a single line of content with its number and textual content.

Properties:

- string Content: The textual content of the line
- int Number: The sequence number of this line content.

5.1.2.13 CodeBlock

Namespace: RepoScribe.Core.DataModels.Markdown
Base class: MarkdownContent

A class representing a block of code in Markdown format with a specified language.

Properties:

- string Content: The content of the code block as a string
- string Language: The programming language of the code block

Methods:

- void ApplyTemplate(object param): Applies a given Markdown template to the current CodeBlock's content and returns the result.
    template: The Markdown template string to apply
-  CodeBlock(object param, object param): Creates a new CodeBlock instance with specified language and content.
    language: The programming language for the code block
    content: The actual code to be displayed
- void ToMarkdown(): Converts this CodeBlock instance to Markdown format.

5.1.2.14 Header

Namespace: RepoScribe.Core.DataModels.Markdown
Base class: MarkdownContent

A class representing a header in Markdown format with specified level and text.

Properties:

- int Level: The level of heading for this header (1-6)
- string Text: The textual content of the header

Methods:

- void ApplyTemplate(object param): Applies a given Markdown template to the current Header instance.
    template: The Markdown template string to apply
-  Header(object param, object param): Creates a new Header instance with specified level and text.
    level: The header level (1-6)
    text: The header text
- void ToMarkdown(): Converts this Header instance to Markdown format.

5.1.2.15 IOutputTemplating

Namespace: RepoScribe.Core.DataModels.Markdown

Defines an interface for applying templates to strings.

Methods:

- void ApplyTemplate(object param): Applies a given Markdown template to the current output.
    template: The Markdown template to apply

5.1.2.16 MarkdownContent

Namespace: RepoScribe.Core.DataModels.Markdown
Interfaces: IOutputTemplating

An abstract base class for generating Markdown content with templating capabilities.

Methods:

- void ApplyTemplate(object param): Applies a given template string to the Markdown content represented by this instance.
    template: A string containing placeholders (e.g., '{0}') where Markdown content will be inserted
- void ToMarkdown(): Converts the MarkdownContent instance into its Markdown representation.
- void ToString(): Overrides the ToString() method to return the Markdown representation of this content.

5.1.2.17 MarkdownDocument

Namespace: RepoScribe.Core.DataModels.Markdown

A class representing a Markdown document composed of multiple MarkdownContent sections.

Attributes:

- List<MarkdownContent> _contents (public): Stores the list of MarkdownContent items that make up this document

Methods:

- void AddContent(object param): Appends the provided MarkdownContent to the internal list of contents.
    content: The MarkdownContent to add
- void ToString(): Converts the MarkdownDocument to a string by concatenating all its contents.

5.1.2.18 Metadata

Namespace: RepoScribe.Core.DataModels

Represents metadata for a file or document, including path, owner, modification details, size, language, and content.

Properties:

- string Content: The content of the metadata as a string
- string Language: The primary language used in the content
- DateTime LastModified: The date and time when this metadata was last modified.
- string Owner: The owner of the metadata resource
- string Path: The file path of this metadata
- double SizeMB: The size of the metadata in megabytes

5.1.2.19 RepositoryMetadata

Namespace: RepoScribe.Core.DataModels

Represents metadata for a GitHub repository, including its URL, author, readme content, and list of files.

Properties:

- string Author: The author of the repository
- List<FileMetadata> Files: A list of FileMetadata objects representing all files in the repository.
- string Readme: The content of the README file for this repository.
- string Url: The URL of the repository

5.1.2.20 AppDbContext

Namespace: RepoScribe.Core.Database
Base class: DbContext

Represents the main database context for RepoScribe application, managing various content item entities and their relationships.

Properties:

- DbSet<CodeContentItemEntity> CodeContentItems: A DbSet property representing the set of CodeContentItemEntity objects tracked by the AppDbContext
- DbSet<ContentItemEntity> ContentItems: A DbSet property representing the set of ContentItem entities tracked by this AppDbContext instance.
- DbSet<ImageContentItemEntity> ImageContentItems: A DbSet property representing the set of ImageContentItemEntity objects tracked by the AppDbContext
- DbSet<LineContentEntity> LineContents: A DbSet property representing the collection of LineContentEntity objects tracked by the AppDbContext.
- DbSet<PdfContentItemEntity> PdfContentItems: A DbSet property representing the collection of PdfContentItemEntity objects in the database
- DbSet<RepositoryContentItemEntity> RepositoryContentItems: A DbSet property representing the set of RepositoryContentItemEntity objects in the database

Methods:

-  AppDbContext(object param): Initializes a new instance of AppDbContext with the specified DbContextOptions.
    options: The DbContextOptions to use for this context
- void OnModelCreating(object param): Configures the model for the database using Fluent API.
    modelBuilder: The ModelBuilder instance used to configure the model

5.1.2.21 ClusterIndex

Namespace: RepoScribe.Core.DataModels

Represents a cluster index containing cluster ID, unique identifier, and list of member embeddings.

Properties:

- string ClusterId: Unique identifier for the cluster
- Guid ClusterIndexId: Unique identifier for this cluster index
- List<Guid> MemberEmbeddings: A list of unique identifiers (GUIDs) representing member embeddings associated with this cluster index.

5.1.2.22 CodeContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents a code content item entity in the database, inheriting from ContentItemEntity.

5.1.2.23 ContentItemEntity

Namespace: RepoScribe.Core.Database.Entities

Represents an entity for content items in the database, serving as a base class for specific content types.

Properties:

- string Content: The content of the item as a string
- ContextualInputSource ContextSource: The source of contextual input for this content item
- Domain Domain: The domain to which this content item belongs
- Guid Id: Unique identifier for this content item entity
- string Language: The language of the content represented by this entity
- DateTime LastModified: The date and time when this content item was last modified.
- ICollection<LineContentEntity> Lines: A collection of line content entities associated with this content item.
- string Owner: The username or identifier of the owner of this content item
- string Path: The file path of the content item
- double SizeMB: The size of the content item in megabytes

5.1.2.24 ConversationEntity

Namespace: RepoScribe.Core.Database.Entities

Represents a conversation entity in the database with its associated queries and metadata.

Properties:

- Guid ConversationId: Unique identifier for the conversation
- string ConversationName: The name or title of the conversation.
- List<string> ConversationTopics: A list of strings representing the topics discussed in the conversation.
- string ConversationUrl: The URL associated with this conversation.
- string Provider: The name or identifier of the provider associated with this conversation
- List<QueryEntity> Queries: A collection of QueryEntity objects associated with this conversation.
- DateTime TimeStamp: The date and time when this conversation entity was created or last updated.

5.1.2.25 ImageContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents an image content item entity with metadata and binary data.

Properties:

- byte[] ImageData: Stores the binary data of an image
- string ImageMetadata: Stores metadata associated with an image

5.1.2.26 LineContentEntity

Namespace: RepoScribe.Core.Database.Entities

Represents a line of content within a content item in the database.

Properties:

- string Content: The textual content of the line
- ContentItemEntity ContentItem: The associated ContentItemEntity for this LineContentEntity
- int ContentItemEntityId: The identifier of the associated ContentItemEntity
- int Id: Unique identifier for this LineContentEntity instance
- int Number: The sequence number of this line content

5.1.2.27 PdfContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents a PDF content item entity, inheriting from ContentItemEntity.

5.1.2.28 QueryEntity

Namespace: RepoScribe.Core.Database.Entities

An abstract class representing a query entity in the conversation history, containing details about each query and its responses.

Properties:

- ConversationEntity Conversation: The conversation entity associated with this query entity
- Guid ConversationId: Unique identifier of the conversation associated with this query entity
- bool HasResponse: Indicates whether this query entity has a response
- bool IsBestResponse: Indicates whether this query entity is considered the best response among its related responses.
- bool IsBot: Indicates whether this query entity represents a bot (true) or not (false)
- bool IsQuery: Indicates whether this entity represents a query (true if it's a query, false otherwise)
- bool IsResponse: Indicates whether this entity represents a response to another query
- bool IsUser: Indicates whether this entity represents a user query
- string Provider: The name of the provider associated with this query entity
- Guid QueryId: Unique identifier for each query entity
- string QueryString: The raw query string entered by the user or bot
- string Response: The response message generated by the bot or retrieved from a provider.
- List<QueryEntity> Responses: A list of QueryEntity objects representing responses to this query
- string Source: The source of the query entity
- DateTime TimeStamp: The date and time when this query entity was created or last updated.

5.1.2.29 RepositoryContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents a content item entity in the repository database with additional properties like URL, author, readme, and associated files.

Properties:

- string Author: The author of the repository content item
- ICollection<ContentItemEntity> Files: A collection of ContentItemEntity objects representing the files associated with this repository content item.
- string Readme: The markdown content of the repository's README file.
- string Url: The URL associated with this repository content item.

5.1.2.30 CodeFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles file processing for code files, providing metadata including language, content, and line details.

Attributes:

- Dictionary<string, string> _languageMap (public): A dictionary mapping file extensions to their corresponding programming languages

Methods:

- void CanHandle(object param): Checks if this handler can process files with the given extension by looking up the extension in the language map.
    extension: File extension to check for
    Returns: null (void method)
-  CodeFileHandler(object param): Initializes a CodeFileHandler instance with a language map for file processing.
    languageMap: A dictionary mapping file extensions to their respective programming languages
- void ProcessFile(object param): Reads a file at the specified path and returns its metadata.
    filePath: The full path to the file

5.1.2.31 CodeContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

Extracts content from code files based on their extensions and language mappings.

Attributes:

- Dictionary<string, string> _languageMap (public): Stores a mapping of file extensions to programming languages for content extraction

Methods:

- void CanExtract(object param): Checks if the extractor can handle a given input file based on its extension.
    input: The path to the file being checked
    Returns: null (void)
-  CodeContentExtractor(object param): Extracts code content from a file based on its extension and language mapping.
    languageMap: A dictionary containing file extensions as keys and their corresponding programming languages as values
    Returns: An instance of CodeContentExtractor that can extract content from files matching the provided language map
- void ExtractContent(object param): Extracts content from a file and returns it as a CodeContentItem.
    input: The path to the file containing the content

5.1.2.32 ImageContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

Extracts and encapsulates relevant information from image files such as PNG, JPG, JPEG, GIF, BMP.

Attributes:

- List<string> _supportedExtensions (public): List of supported image file extensions

Methods:

- void CanExtract(object param): Checks if the given input file can be extracted by this content extractor.
    input: The path to the file being checked
    Returns: void (no return value)
- void ExtractContent(object param): Extracts image content from a file and returns it as an ImageContentItem.
    input: The path to the image file
    Returns: null (void)

5.1.2.33 PdfContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

A class responsible for extracting content from PDF files and converting it into a structured format.

Attributes:

- List<string> _supportedExtensions (public): List of file extensions that this content extractor supports

Methods:

- void CanExtract(object param): Checks if the given input file can be extracted by this content extractor.
    input: The path to the file being checked
    Returns: void (no return value)
- void ExtractContent(object param): Extracts content from a PDF file and returns it as a string.
    input: The path to the PDF file
- void ExtractTextFromPdf(object param): Extracts and concatenates text from all pages of a PDF file located at the specified path.
    filePath: The full file path to the PDF document

5.1.2.34 SqliteContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

Extracts content from SQLite databases by retrieving table names and storing them in a PdfContentItem.

Attributes:

- List<string> _supportedExtensions (public): List of supported file extensions for SQLite databases

Methods:

- void CanExtract(object param): Checks if the input file has a supported extension for SQLite databases.
    input: The path to the file being checked
- void ExtractContent(object param): Extracts content from a SQLite database file by retrieving table names and storing them in a PdfContentItem.
    input: Path to the SQLite database file
- void GetTables(object param): Extracts table names from a SQLite database file located at the specified path.
    filePath: The full file path of the SQLite database
    Returns: null (void method)

5.1.2.35 IFileHandler

Namespace: RepoScribe.Core.FileHandlers

Defines an interface for handling files based on their extensions and extracting metadata.

Methods:

- void CanHandle(object param): Checks if the file handler can process files with the specified extension.
    extension: The file extension to check for
- void ProcessFile(object param): Processes a file located at the specified path and returns its metadata.
    filePath: The full path to the file being processed

5.1.2.36 ImageFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles processing and metadata extraction for image files with supported extensions.

Attributes:

- List<string> _supportedExtensions (public): List of file extensions that this handler supports

Methods:

- void CanHandle(object param): Checks if the specified file extension is supported by this handler.
    extension: The file extension to check for support
- void ProcessFile(object param): Processes a file by loading its image data and extracting metadata.
    filePath: The path to the file being processed

5.1.2.37 PdfFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles processing of PDF files by extracting text content and generating metadata.

Attributes:

- List<string> _supportedExtensions (public): List of file extensions that this handler can process

Methods:

- void CanHandle(object param): Checks if the file handler can process files with the given extension.
    extension: The file extension to check for (e.g., '.pdf')
- void ExtractTextFromPdf(object param): Extracts and appends text from a PDF file located at the specified path.
    filePath: The full file path of the PDF document
    Returns: null (void method)
- void ProcessFile(object param): Processes a PDF file located at the specified path and returns its metadata.
    filePath: The full file path of the PDF document to process
    Returns: null (void method)

5.1.2.38 SqliteFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles SQLite file processing and metadata extraction.

Attributes:

- List<string> _supportedExtensions (public): List of supported file extensions for SQLite databases

Methods:

- void CanHandle(object param): Checks if the file handler can process files with the given extension by comparing it to a list of supported extensions.
    extension: The file extension (including dot) to check for support
- void GetTables(object param): Extracts and returns a list of table names from an SQLite database file located at the specified path.
    filePath: The full file path to the SQLite database (.sqlite or .db extension)
    Returns: null (void method)
- void ProcessFile(object param): Processes a SQLite file located at the specified path and returns metadata about it.
    filePath: The full file path of the SQLite database to process

5.1.2.39 FileHelper

Namespace: RepoScribe.Core.Helpers

A deprecated class that handles file processing using a list of IFileHandler implementations. It determines the appropriate handler based on the file's extension and processes the file if a matching handler is found.

Attributes:

- List<IFileHandler> _fileHandlers (public): A list of file handlers used to process files

Methods:

-  FileHelper(object param): Processes a file using registered handlers and returns its metadata if handled successfully.
    filePath: The path of the file to process
    Returns: FileMetadata object containing details about the processed file, or null if no handler could handle it
- void ProcessFile(object param): Processes a file using appropriate handlers based on its extension.
    filePath: The path to the file being processed
    Returns: null if no handler can process the file

5.1.2.40 GitHelper

Namespace: RepoScribe.Core.Helpers

A helper class designed to interact with Git repositories and retrieve relevant metadata.

Methods:

- void GetReadmeContent(object param): Retrieves the content of the README file from the specified repository path.
    repoPath: The path to the Git repository
    Returns: null (void method)
- void GetRepositoryMetadata(object param): Retrieves metadata for a Git repository located at the specified path.
    repoPath: The file system path to the root of the Git repository
    Returns: void (This method does not return any value)

5.1.2.41 InputProcessor

Namespace: RepoScribe.Core.Helpers

A class responsible for processing input files and extracting content using appropriate extractors.

Attributes:

- List<IContentExtractor> _extractors (public): Stores a list of content extractors used for processing input

Methods:

-  InputProcessor(object param): Initializes an InputProcessor with a list of content extractors.
    extractors: A list of IContentExtractor implementations used to process input files
- void ProcessInput(object param): Processes a given input string and attempts to extract content using registered extractors.
    input: The input string to process
    Returns: null

5.1.2.42 MarkdownRenderer

Namespace: RepoScribe.Core.Renderers
Interfaces: ITemplateRenderer

A class responsible for rendering various content items into Markdown format.

Methods:

- void Render(object param, object param): Renders a ContentItem as Markdown string based on its type and optionally applies a template.
    contentItem: The content item to render
    template: Optional template to apply to the rendered content
    Returns: Markdown string representation of the content item

5.1.2.43 ChromaDbService

Namespace: RepoScribe.Core.Services

A service class responsible for interacting with a ChromaDB instance to perform CRUD operations on content items.

Attributes:

- string _baseUrl (public): The base URL of the ChromaDB service
- HttpClient _httpClient (public): An instance of HttpClient used to make HTTP requests to communicate with ChromaDB
- Lazy<ChromaDbService> _instance (public): Lazy-loaded singleton instance of ChromaDbService

Properties:

- ChromaDbService Instance: The singleton instance of the ChromaDbService class

Methods:

-  ChromaDbService(): Initializes a new instance of the ChromaDbService class with an HttpClient and base URL for communicating with ChromaDB.
- void UpsertAsync(object param): Asynchronously sends a POST request to upsert (insert or update) the provided ContentItem into ChromaDB.
    contentItem: The ContentItem object containing data to be inserted or updated

5.1.2.44 FlattenAllService

Namespace: RepoScribe.Core.Services

Manages and coordinates the Flatten-All process for generating markdown files from Git repositories.

Attributes:

- string _codeFlattenerPath (public): The file path to the CodeFlattener.exe executable
- InputProcessor _inputProcessor (public): Stores the instance of InputProcessor used for processing input
- string _outputDirectory (public): The directory where flattened markdown files are saved
- IRenderer _renderer (public): The renderer used to generate markdown files from processed directories

Methods:

- void FlattenAllAsync(): Asynchronously processes all Git repositories in the current directory and its subdirectories using CodeFlattener.exe, saving output Markdown files to a specified directory.
-  FlattenAllService(object param, object param, object param, object param): Runs a process to flatten all Git repositories in the current directory and its subdirectories using CodeFlattener.exe.
    codeFlattenerPath: The path to the CodeFlattener.exe file
    outputDirectory: The directory where the output markdown files will be saved
    inputProcessor: An instance of InputProcessor used for processing input data
    renderer: An implementation of IRenderer interface for rendering output

5.1.2.45 HttpService

Namespace: RepoScribe.Core.Services

A service class for making HTTP requests using the HttpClient class.

Attributes:

- HttpClient _httpClient (public): An instance of HttpClient used for making HTTP requests

Methods:

- void GetAsync(object param): Asynchronously retrieves data from the specified URL using an HTTP GET request.
    url: The Uniform Resource Locator (URL) to retrieve data from
    Returns: null (void)
-  HttpService(): Initializes a new instance of HttpService with an HttpClient for making HTTP requests.
- void PostAsync(object param, object param): Sends an asynchronous POST request to the specified URL with the provided content.
    url: The URI to send the POST request to
    content: The HttpContent containing data to be sent in the POST request

5.1.2.46 LocalDatabaseService

Namespace: RepoScribe.Core.Services

Manages local database operations using Npgsql or Sqlite connections based on environment configuration.

Attributes:

- IConfiguration _config (public): Stores the configuration settings for the application
- string _connectionString (public): Stores the connection string used to connect to the database
- ILogger _logger (public): Stores an instance of ILogger for logging purposes

Methods:

- void InitializeDatabase(): Initializes the database by opening a connection and performing necessary operations such as creating tables or running migrations.
-  LocalDatabaseService(object param, object param): Initializes a new instance of LocalDatabaseService with configuration and logger.
    config: The IConfiguration object containing connection strings for different environments
    logger: The ILogger object used for logging information, errors, etc.
- void OpenConnection(): Opens a database connection using either Sqlite or Npgsql based on the connection string.
- void TestConnection(): Tests the connection to the database using the configured connection string.
    Returns: True if the connection is successful, false otherwise

5.1.2.47 MarkdownExtractor

Namespace: RepoScribe.Core.Services

A deprecated class that extracts code blocks from Markdown files in a specified directory and returns them as serialized JSON objects.

Attributes:

- string _inputDirectory (public): The input directory path where Markdown files are located

Methods:

- void ExtractCodeBlocks(): Extracts code blocks from Markdown files in the specified directory and yields them as serialized JSON objects.
    Returns: IEnumerable<string> containing serialized JSON objects representing extracted code blocks
-  MarkdownExtractor(object param): Extracts code blocks from Markdown files in a specified directory and returns them as serialized JSON objects.
    inputDirectory: The directory containing the Markdown files to extract code blocks from
    Returns: IEnumerable<string> representing the extracted code blocks serialized as JSON

5.1.2.48 OllamaService

Namespace: RepoScribe.Core.Services

A service class responsible for communicating with Ollama API to fetch data.

Attributes:

- string _baseUrl (public): The base URL for Ollama API requests
- HttpClient _httpClient (public): An HttpClient instance used for making HTTP requests

Methods:

- void GetAsync(object param, object param): Asynchronously retrieves data from a specified URL with optional request parameters.
    url: The endpoint URL to retrieve data from
    req: A dictionary of key-value pairs representing request parameters
-  OllamaService(): Initializes a new instance of OllamaService with default HttpClient and base URL.

5.1.2.49 WorkerPool

Namespace: RepoScribe.Core.Services

A pool of worker threads that process tasks in a queue. Tasks are added via EnqueueTask and workers will execute them concurrently.

Attributes:

- CancellationTokenSource _cts (public): Cancellation token source used to signal worker tasks to stop
- BlockingCollection<Func<Task>> _taskQueue (public): A blocking collection used to queue tasks for worker threads

Methods:

- void EnqueueTask(object param): Adds a new task to be processed by the worker pool.
    task: A function that returns a Task representing the work to be done
- void Stop(): Cancels all tasks in the worker pool and stops accepting new ones.
-  WorkerPool(object param): Initializes a worker pool with specified number of workers.
    workerCount: Number of worker threads to create

5.1.2.50 ConfigurationManager

Namespace: RepoScribe.Core.Utilities

Manages application configuration by loading and providing access to configuration data from various sources such as environment variables, user's home directory, or default application directory.

Attributes:

- IConfiguration _configuration (public): Stores the configuration settings loaded from appsettings.json files or environment variables.
- string _defaultConfigPath (public): The default file path for the application's configuration file if none other is specified.
- string _envVarConfigPath (public): Stores the configuration path specified via the REPOSCRIBE_CONFIG environment variable
- string _homeDirConfigPath (public): The default configuration path for the application if a user has a configuration file in their home directory

Methods:

-  ConfigurationManager(object param): Initializes a new ConfigurationManager instance with the specified configuration path.
    configPath: The file path to the configuration file
- void GetExtractChunksInputDirectory(): Retrieves the directory path for input files used in chunk extraction process.
- void GetIgnoredPaths(): Retrieves a list of paths to ignore during processing.
    Returns: A List<string> containing the ignored paths
- void GetLanguageMap(): Retrieves a dictionary mapping language identifiers to their corresponding display names from the configuration.

5.1.2.51 HashUtility

Namespace: RepoScribe.Core.Utilities

A utility class for generating SHA-256 hashes and unique IDs from content.

Methods:

- void GetContentHash(object param): Calculates and returns a SHA-256 hash of the provided content as a lowercase string without hyphens.
    content: The input string to be hashed
    Returns: null (void method)
- void GetUniqueId(object param): Generates a unique identifier by taking the first 32 characters of the SHA-256 hash of the provided content.
    content: The input string to generate a unique ID from

5.1.2.52 Logger

Namespace: RepoScribe.Core.Utilities

A static utility class for initializing and managing Serilog logger with console and file output.

Methods:

- void CloseAndFlush(): Closes and flushes the current log stream.
- void Initialize(): Initializes the logger with console and file output destinations.

5.1.2.53 PathUtility

Namespace: RepoScribe.Core.Utilities

A utility class for converting between dotted paths and file system paths.

Methods:

- void ConvertDottedPathToFilePath(object param): Converts a dotted path string into a file system compatible path by replacing dots with directory separators.
    dottedPath: The input path as a string of components separated by dots
    Returns: null (void method)
- void ConvertFilePathToDottedPath(object param): Converts a file path to a dotted path representation by replacing directory separators with dots.
    filePath: The file path to convert
    Returns: null (void method)

5.1.2.54 RepositoryManager

Namespace: RepoScribe.Core.Utilities

Manages a list of repositories by loading them from a config file and providing methods to save changes.

Attributes:

- string _configPath (public): The file path to the configuration file used by RepositoryManager

Properties:

- List<string> Repositories: A list of repository URLs managed by this instance

Methods:

-  RepositoryManager(object param): Initializes a new instance of RepositoryManager with the specified configuration path and loads repositories from the config file if it exists.
    configPath: The file path to the configuration file containing serialized repository data
- void Save(): Saves the current list of repositories to the configuration file located at _configPath.


================================================================================
Section 2
================================================================================
5.2 Unknown

Module containing 1 file(s) with related functionality.

5.2.1 Dependencies

No external dependencies.

5.2.2 Classes

