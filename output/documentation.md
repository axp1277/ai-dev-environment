================================================================================
CODE DOCUMENTATION
================================================================================
Generated: 2025-10-28 20:26:16
Source Directory: data/sample_codebase/RepoScribe-master/RepoScribe.Core

================================================================================
Section 1
================================================================================
5.1 RepoScribe

Module containing 56 file(s) with related functionality.

5.1.1 Dependencies

No external dependencies.

5.1.2 Classes

5.1.2.1 CodeContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents a content item of type code, containing lines of code and implementing methods for ingestion and saving.

Properties:

- List<LineContent> Lines: A list of LineContent objects representing the individual lines of code within this content item.

Methods:

- void Ingest(): Initializes the ingestion process for this CodeContentItem. This method should contain logic to parse code, analyze dependencies, etc.
- void SaveAsync(): Saves the current instance of CodeContentItem to both local database and ChromaDB asynchronously.

5.1.2.2 ContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: Metadata

An abstract base class representing a content item with metadata, ingestion, saving, and rendering capabilities. It serves as the foundation for specific content types like articles or videos.

Properties:

- ContextualInputSource ContextSource: The source of contextual input for this content item.
- Domain Domain: The domain to which this content item belongs.
- Guid Id: Unique identifier for the content item.

Methods:

- void GetSummary(): Generates a summary representation of the content item. The default implementation throws a NotImplementedException.
- void Ingest(): Marks the content item for ingestion. This method is intended to be overridden by derived classes with actual ingestion logic.
- void RenderAs(object param): Renders the content item using the provided IRenderer instance.
    renderer: An implementation of IRenderer to use for rendering
    Returns: void (This method does not return a value)
- void Save(): Saves the current state of the content item. This method is intended to be overridden by concrete implementations.
- void SaveAsync(): Asynchronously saves the current state of the content item. The default implementation throws a NotImplementedException.

5.1.2.3 ImageContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents an image content item with metadata and binary data, extending the base ContentItem class.

Properties:

- byte[] ImageData: Stores the raw byte array representing the image data.
- string ImageMetadata: Represents the metadata associated with the image content item.

Methods:

- void Ingest(): Implements the ingestion logic for an image content item. This method should contain the necessary code to process and store the image data.
- void SaveAsync(): Saves the current instance of ImageContentItem to both local database and ChromaDB asynchronously.

5.1.2.4 PdfContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents a PDF content item within the RepoScribe system. It inherits from ContentItem and contains a list of LineContent objects representing the lines of text extracted from the PDF.

Properties:

- List<LineContent> Lines: A list of LineContent objects representing the lines of text extracted from the PDF content item.

Methods:

- void Ingest(): Initializes the ingestion process for a PDF content item. This method should contain logic to extract text, index pages, and other relevant data from the PDF.
- void SaveAsync(): Saves the current instance of PdfContentItem to both local database and ChromaDB asynchronously.

5.1.2.5 RepositoryContentItem

Namespace: RepoScribe.Core.ContentItems
Base class: ContentItem

Represents a content item from a repository, containing details like URL, author, readme, and associated files. It also implements ingestion and saving functionality.

Properties:

- string Author: The author of the repository associated with this content item.
- List<ContentItem> Files: A list of content items representing the files within this repository.
- string Readme: The markdown content of the repository's README file.
- string Url: The URL of the repository associated with this content item.

Methods:

- void Ingest(): Initializes the ingestion process for a repository content item. This method should contain logic to clone the repository, parse its files, and populate the internal 'Files' list.
- void SaveAsync(): Saves the current content item and its associated files to both local database and ChromaDB.

5.1.2.6 CacheEntry

Namespace: RepoScribe.Core.DataModels

Represents a single entry in the cache, containing metadata and associated cluster indices.

Properties:

- Guid CacheEntryId: Unique identifier for the cache entry.
- List<ClusterIndex> ClusterIndices: A list of cluster indices associated with this cache entry.
- Guid KeyWordEmbeddingId: Unique identifier for the keyword embedding associated with this cache entry.
- string[] KeyWords: An array of keywords associated with this cache entry.

5.1.2.7 FileMetadata

Namespace: RepoScribe.Core.DataModels

Represents metadata associated with a file, including its path, owner, modification details, size, language, content, and line contents.

Properties:

- string Content: The textual content of the file.
- string Language: The primary language used in the file, if applicable.
- DateTime LastModified: The date and time when the file was last modified.
- List<LineContent> Lines: A list of LineContent objects representing the individual lines of content within the file.
- string Owner: The username or identifier of the user who owns this file.
- string Path: The file path of the metadata.
- double SizeMB: The size of the file in megabytes.

5.1.2.8 LineContent

Namespace: RepoScribe.Core.DataModels

Represents a single line of content with its number and text.

Properties:

- string Content: The textual content of the line.
- int Number: Represents the line number of this content.

5.1.2.9 CodeBlock

Namespace: RepoScribe.Core.DataModels.Markdown
Base class: MarkdownContent

A class representing a block of code in Markdown format. It includes the programming language and the actual code content.

Properties:

- string Content: The content of the code block represented as a string.
- string Language: The programming language associated with the code block.

Methods:

- void ApplyTemplate(object param): Applies a given markdown template to the code block's content and returns the result.
    template: The markdown template to apply. It should contain placeholders (e.g., '{0}') where the code block's content will be inserted.
    Returns: A string representing the applied markdown template with the code block's content inserted into the placeholder(s).
-  CodeBlock(object param, object param): Creates a new CodeBlock instance with the specified programming language and content.
    language: The programming language for the code block (e.g., 'csharp', 'python').
    content: The actual code to be displayed within the block.
- void ToMarkdown(): Converts the CodeBlock instance to its Markdown representation.
    Returns: A string containing the Markdown representation of the CodeBlock.

5.1.2.10 Header

Namespace: RepoScribe.Core.DataModels.Markdown
Base class: MarkdownContent

A class representing a markdown header with customizable level and text.

Properties:

- int Level: The level of the header (1-6), indicating its importance and hierarchy.
- string Text: The textual content of the header

Methods:

- void ApplyTemplate(object param): Applies a given Markdown template to the current Header instance and returns the result.
    template: The Markdown template string to apply. It should contain placeholders (e.g., '{0}') where the Header's content will be inserted.
    Returns: A formatted string that represents the applied template with the current Header's content.
-  Header(object param, object param): Creates a new Header instance with the specified level and text.
    level: The header level (1-6)
    text: The header text
- void ToMarkdown(): Converts the Header object to its Markdown representation and returns it as a string.
    Returns: A string representing the Header in Markdown format

5.1.2.11 MarkdownContent

Namespace: RepoScribe.Core.DataModels.Markdown
Interfaces: IOutputTemplating

An abstract base class for generating Markdown content with templating capabilities.

Methods:

- void ApplyTemplate(object param): Applies a given template string to the Markdown content represented by this instance.
    template: A string containing placeholders (e.g., '{0}') where Markdown content will be inserted
- void ToMarkdown(): Converts the MarkdownContent object into its Markdown representation.
- void ToString(): Overrides the default ToString() method to return the Markdown representation of this content.

5.1.2.12 MarkdownDocument

Namespace: RepoScribe.Core.DataModels.Markdown

A class representing a Markdown document composed of multiple MarkdownContent sections.

Attributes:

- List<MarkdownContent> _contents (public): A private, mutable list storing the individual MarkdownContent items that make up this document.

Methods:

- void AddContent(object param): Appends the provided MarkdownContent to the internal list of contents.
    content: The MarkdownContent to add
- void ToString(): Converts the MarkdownDocument object to its string representation by concatenating all contained MarkdownContent objects.

5.1.2.13 Metadata

Namespace: RepoScribe.Core.DataModels

Represents metadata information for a file or document, including path, owner details, size, language, and content.

Properties:

- string Content: The textual content of the metadata item.
- string Language: The primary language used in the content represented by this metadata.
- DateTime LastModified: The date and time when the associated resource was last modified.
- string Owner: The owner of the metadata resource represented by this instance.
- string Path: The file path of the metadata.
- double SizeMB: Represents the size of the metadata in megabytes.

5.1.2.14 RepositoryMetadata

Namespace: RepoScribe.Core.DataModels

Represents metadata associated with a Git repository, including its URL, author, readme content, and list of files.

Properties:

- string Author: The author of the repository.
- List<FileMetadata> Files: A list of FileMetadata objects representing the files within the repository.
- string Readme: The markdown content of the repository's README file.
- string Url: The URL of the repository.

5.1.2.15 AppDbContext

Namespace: RepoScribe.Core.Database
Base class: DbContext

The AppDbContext class is responsible for managing the database context and configurations for RepoScribe's content items. It inherits from DbContext and provides DbSets for each type of content item entity.

Properties:

- DbSet<CodeContentItemEntity> CodeContentItems: A DbSet property representing the collection of CodeContentItemEntity objects tracked by the AppDbContext.
- DbSet<ContentItemEntity> ContentItems: A DbSet property that represents the collection of ContentItem entities tracked by this AppDbContext instance.
- DbSet<ImageContentItemEntity> ImageContentItems: A DbSet property that represents the collection of ImageContentItemEntity objects tracked by the AppDbContext.
- DbSet<LineContentEntity> LineContents: A DbSet property that represents the collection of LineContentEntity objects tracked by the AppDbContext.
- DbSet<PdfContentItemEntity> PdfContentItems: A DbSet property that represents the collection of PdfContentItemEntity objects tracked by the AppDbContext.
- DbSet<RepositoryContentItemEntity> RepositoryContentItems: A DbSet property that represents the collection of RepositoryContentItemEntity objects tracked by the AppDbContext.

Methods:

-  AppDbContext(object param): Initializes a new instance of the AppDbContext class with the provided DbContextOptions.
    options: The DbContextOptions to use for this context.
- void OnModelCreating(object param): Configures the model for the database using Fluent API. This includes setting up inheritance and relationships between entities.
    modelBuilder: The ModelBuilder instance used to configure the model

5.1.2.16 ClusterIndex

Namespace: RepoScribe.Core.DataModels

Represents a cluster index used for managing and retrieving member embeddings within a specific cluster.

Properties:

- string ClusterId: Unique identifier for the cluster.
- Guid ClusterIndexId: Unique identifier for the cluster index.
- List<Guid> MemberEmbeddings: A list of unique identifiers (GUIDs) representing the embeddings of members within this cluster.

5.1.2.17 CodeContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents an entity for code content items in the database, inheriting from the base ContentItemEntity.

5.1.2.18 ContentItemEntity

Namespace: RepoScribe.Core.Database.Entities

Represents an entity for content items in the database, serving as a base class for specific content types. Stores metadata and content data.

Properties:

- string Content: The content of the item represented as a string.
- ContextualInputSource ContextSource: The source of contextual input for this content item.
- Domain Domain: The domain to which this content item belongs.
- Guid Id: Unique identifier for the content item entity.
- string Language: The language of the content represented by this entity, e.g., 'en' for English.
- DateTime LastModified: The date and time when the content item was last modified.
- ICollection<LineContentEntity> Lines: A collection of line content entities associated with this content item.
- string Owner: The username or identifier of the owner of this content item.
- string Path: The file path of the content item.
- double SizeMB: The size of the content item in megabytes.

5.1.2.19 ConversationEntity

Namespace: RepoScribe.Core.Database.Entities

Represents a conversation entity containing queries, metadata and related information.

Properties:

- Guid ConversationId: Unique identifier for the conversation.
- string ConversationName: The name or title of the conversation.
- List<string> ConversationTopics: A list of strings representing the topics discussed during this conversation.
- string ConversationUrl: The URL associated with the conversation.
- string Provider: The name or identifier of the provider associated with this conversation.
- List<QueryEntity> Queries: A collection of query entities associated with this conversation.
- DateTime TimeStamp: The date and time when the conversation was created or last updated.

5.1.2.20 ImageContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents an image content item entity, extending the base ContentItemEntity class. Stores metadata and binary data for an image.

Properties:

- byte[] ImageData: Stores the binary data of the image.
- string ImageMetadata: Represents the metadata associated with an image, stored as a string.

5.1.2.21 LineContentEntity

Namespace: RepoScribe.Core.Database.Entities

Represents a line of content within a larger content item, storing its number and text. Also maintains a reference to its parent content item.

Properties:

- string Content: The textual content of the line entity.
- ContentItemEntity ContentItem: The associated ContentItemEntity instance that this LineContentEntity belongs to.
- int ContentItemEntityId: The unique identifier of the associated ContentItemEntity.
- int Id: Unique identifier for the LineContentEntity instance
- int Number: The sequence number of this line content within its parent content item.

5.1.2.22 PdfContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents a PDF content item entity, inheriting from the base ContentItemEntity class.

5.1.2.23 QueryEntity

Namespace: RepoScribe.Core.Database.Entities

An abstract class representing a query entity within the conversation context, containing properties for query details and related entities.

Properties:

- ConversationEntity Conversation: The conversation entity associated with this query entity.
- Guid ConversationId: The unique identifier of the conversation associated with this query entity.
- bool HasResponse: Indicates whether this query entity has a response associated with it.
- bool IsBestResponse: Indicates whether this response is considered the best among all responses for its corresponding query.
- bool IsBot: Indicates whether the entity represents a bot or not.
- bool IsQuery: Indicates whether the entity represents a query (true) or not (false).
- bool IsResponse: Indicates whether this entity represents a response to another query.
- bool IsUser: Indicates whether the entity represents a user's query.
- string Provider: The name of the provider associated with this query entity.
- Guid QueryId: Unique identifier for the query entity, generated using Guid.NewGuid().
- string QueryString: The raw query string entered by the user or bot.
- string Response: The response text generated by the bot or retrieved from a knowledge base for this query.
- List<QueryEntity> Responses: A list of QueryEntity objects representing the responses to this query.
- string Source: The source of the query, indicating where it originated from.
- DateTime TimeStamp: The date and time when the query entity was created or last updated.

5.1.2.24 RepositoryContentItemEntity

Namespace: RepoScribe.Core.Database.Entities
Base class: ContentItemEntity

Represents a content item entity within the repository, extending the base ContentItemEntity class.

Properties:

- string Author: The author of the repository content item.
- ICollection<ContentItemEntity> Files: A collection of content item entities representing the files associated with this repository.
- string Readme: The markdown content of the README file associated with this repository.
- string Url: The URL associated with this repository content item.

5.1.2.25 CodeFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

A deprecated class for handling code files and extracting metadata. It maps file extensions to programming languages and retrieves file details such as owner, last modified time, size, language, content, and line contents.

Attributes:

- Dictionary<string, string> _languageMap (public): A dictionary that maps file extensions to their corresponding programming languages for identification of the language used in a given file.

Methods:

- void CanHandle(object param): Checks if the CodeFileHandler can handle files with the given extension by looking up the extension in its language map.
    extension: The file extension to check for (e.g., '.cs', '.js')
    Returns: void (no return value)
-  CodeFileHandler(object param): Initializes a CodeFileHandler instance with a language map for file processing.
    languageMap: A dictionary mapping file extensions to their respective programming languages
- void ProcessFile(object param): Reads a file from the specified path and returns its metadata including owner, last modified time, size, language (if mapped), content, and line contents.
    filePath: The full path of the file to process
    Returns: null (void method)

5.1.2.26 CodeContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

A class responsible for extracting content from code files. It implements the IContentExtractor interface and uses a language map to determine if it can extract content based on file extension.

Attributes:

- Dictionary<string, string> _languageMap (public): A dictionary that maps file extensions to their corresponding programming languages for content extraction.

Methods:

- void CanExtract(object param): Checks if the extractor can process a given input file based on its extension.
    input: The path to the file being checked
    Returns: void (This method does not return any value)
-  CodeContentExtractor(object param): Extracts content from a code file based on its language and returns it as a CodeContentItem.
    languageMap: A dictionary mapping file extensions to their respective programming languages
    Returns: An instance of CodeContentExtractor initialized with the provided language map
- void ExtractContent(object param): Extracts content from the given input file and returns a CodeContentItem object.
    input: The path to the file containing the content to extract

5.1.2.27 ImageContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

A class responsible for extracting relevant information from image files. It supports various image formats and retrieves metadata such as owner, last modified time, size, and image-specific metadata.

Attributes:

- List<string> _supportedExtensions (public): A list of supported image file extensions that this extractor can handle.

Methods:

- void CanExtract(object param): Checks if the given input file can be extracted by this content extractor based on its extension.
    input: The path to the file being checked
    Returns: void (This method does not return a value)
- void ExtractContent(object param): Extracts image content from the given input file path and returns an ImageContentItem object.
    input: The file path of the image to extract content from
    Returns: null (void method)

5.1.2.28 PdfContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

A class responsible for extracting content from PDF files. It implements the IContentExtractor interface and supports only PDF file extensions.

Attributes:

- List<string> _supportedExtensions (public): A list of file extensions that this content extractor supports, currently only '.pdf'

Methods:

- void CanExtract(object param): Checks if the given input file can be extracted by this content extractor.
    input: The path to the file being checked for extraction
    Returns: void (This method does not return a value)
- void ExtractContent(object param): Extracts and returns the textual content from a PDF file located at the provided input path.
    input: The file path of the PDF document to extract text from
    Returns: void (This method does not return any value)
- void ExtractTextFromPdf(object param): Extracts and concatenates textual content from a PDF file located at the specified path.
    filePath: The full file path of the PDF document to extract text from
    Returns: null (void method)

5.1.2.29 SqliteContentExtractor

Namespace: RepoScribe.Core.FileHandlers.ContentExtractors
Interfaces: IContentExtractor

A class responsible for extracting content from SQLite database files. It implements the IContentExtractor interface and supports file extensions like .sqlite, .db, and .sqlite3.

Attributes:

- List<string> _supportedExtensions (public): A list of supported file extensions for SQLite databases that this content extractor can handle.

Methods:

- void CanExtract(object param): Checks if the input file has a supported SQLite extension (.sqlite, .db, or .sqlite3) and returns true if it does, false otherwise.
    input: The path to the file being checked
    Returns: void (no return value)
- void ExtractContent(object param): Extracts content from a SQLite database file located at the provided input path.
    input: The file path of the SQLite database to extract content from.
- void GetTables(object param): Extracts table names from a SQLite database file located at the given path.
    filePath: The full file path of the SQLite database (.sqlite, .db, or .sqlite3)
    Returns: void (This method does not return any value. It populates the 'tables' list with table names.)

5.1.2.30 ImageFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles the processing of image files by checking if they are supported and extracting relevant metadata.

Attributes:

- List<string> _supportedExtensions (public): A list of file extensions that this handler supports for image processing.

Methods:

- void CanHandle(object param): Checks if the given file extension is supported by this handler.
    extension: The file extension to check for support (e.g., '.png', '.jpg')
    Returns: void (This method does not return a value)
- void ProcessFile(object param): Processes an image file located at the given path, extracts metadata using SixLabors.ImageSharp library, and returns a FileMetadata object.
    filePath: The full path of the image file to process

5.1.2.31 PdfFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles processing of PDF files, extracting text content and metadata.

Attributes:

- List<string> _supportedExtensions (public): A list of file extensions that this handler can process, currently only supports PDF files.

Methods:

- void CanHandle(object param): Checks if the file handler can process files with the given extension by comparing it to the list of supported extensions.
    extension: The file extension (e.g., '.pdf') to check for
    Returns: void (no return value)
- void ExtractTextFromPdf(object param): Extracts and appends the textual content from a PDF file located at the specified path.
    filePath: The full file path of the PDF document to extract text from
    Returns: void (This method does not return any value)
- void ProcessFile(object param): Processes a PDF file located at the given path, extracting its textual content and creating a FileMetadata object.
    filePath: The full file path of the PDF document to process
    Returns: null (void method)

5.1.2.32 SqliteFileHandler

Namespace: RepoScribe.Core.FileHandlers
Interfaces: IFileHandler

Handles file processing for SQLite databases. It checks if the file can be handled based on its extension, extracts table information from the database, and generates a FileMetadata object.

Attributes:

- List<string> _supportedExtensions (public): A list of supported file extensions for SQLite databases that this handler can process.

Methods:

- void CanHandle(object param): Checks if the file handler can process files with the given extension by verifying if it's included in the list of supported extensions.
    extension: The file extension to check for support
    Returns: void (no return value)
- void GetTables(object param): Extracts the names of all tables from a SQLite database file located at the specified path.
    filePath: The full file path to the SQLite database (.sqlite, .db, or .sqlite3)
    Returns: void (This method does not return any value. It populates the 'tables' list with table names.)
- void ProcessFile(object param): Processes a SQLite database file located at the given path, extracts table names, and returns metadata about the file.
    filePath: The full file path of the SQLite database to process
    Returns: void (This method does not return any value)

5.1.2.33 FileHelper

Namespace: RepoScribe.Core.Helpers

A deprecated class that provides functionality to process files using a list of file handlers. It determines the appropriate handler based on the file's extension and processes the file if a matching handler is found.

Attributes:

- List<IFileHandler> _fileHandlers (public): A list of file handlers used to process files based on their extensions.

Methods:

-  FileHelper(object param): Processes a file using the appropriate IFileHandler based on its extension, returning FileMetadata if successful or null otherwise.
    filePath: The path to the file being processed
    Returns: FileMetadata containing information about the processed file, or null if no handler could process the file
- void ProcessFile(object param): Processes a file using the appropriate file handler based on its extension, returning the extracted metadata if successful.
    filePath: The path to the file being processed
    Returns: null (void)

5.1.2.34 GitHelper

Namespace: RepoScribe.Core.Helpers

A helper class designed to interact with Git repositories and retrieve relevant metadata.

Methods:

- void GetReadmeContent(object param): Retrieves the content of the README file from the specified repository path.
    repoPath: The full path to the Git repository
    Returns: null (void method)
- void GetRepositoryMetadata(object param): Retrieves metadata for a given Git repository, including its URL, author of the first commit, and content of the README file.
    repoPath: The local path to the Git repository
    Returns: void (This method does not return any value)

5.1.2.35 InputProcessor

Namespace: RepoScribe.Core.Helpers

A class responsible for processing input files and extracting content using appropriate extractors.

Attributes:

- List<IContentExtractor> _extractors (public): A private, readonly list of content extractors used to determine which extractor can process a given input.

Methods:

-  InputProcessor(object param): Initializes an InputProcessor with a list of content extractors.
    extractors: A list of IContentExtractor implementations used to process input files
    Returns: null (void)
- void ProcessInput(object param): Processes the given input string and attempts to extract content using registered IContentExtractor instances.
    input: The input string to process
    Returns: null if no extractor can handle the input, otherwise the extracted ContentItem

5.1.2.36 MarkdownRenderer

Namespace: RepoScribe.Core.Renderers
Interfaces: ITemplateRenderer

A class responsible for converting various content items into Markdown format. It supports rendering CodeContentItem, with plans to extend support for ImageContentItem, PdfContentItem, and RepositoryContentItem.

Methods:

- void Render(object param, object param): Renders a given ContentItem into Markdown format based on the provided template. If no template is provided, it uses a default structure.
    contentItem: The content item to render. It can be of type CodeContentItem, ImageContentItem, PdfContentItem, or RepositoryContentItem.
    template: An optional Markdown template to apply to the rendered content.
    Returns: A string representing the rendered Markdown content

5.1.2.37 ChromaDbService

Namespace: RepoScribe.Core.Services

A service class responsible for interacting with a ChromaDB instance to perform CRUD operations on ContentItems. It provides a singleton instance for easy access and uses HttpClient for communication.

Attributes:

- string _baseUrl (public): The base URL of the ChromaDB service, used to construct API endpoints.
- HttpClient _httpClient (public): An instance of HttpClient used for making HTTP requests to communicate with the ChromaDB service.
- Lazy<ChromaDbService> _instance (public): Lazy-loaded singleton instance of ChromaDbService, ensuring thread safety and efficient initialization.

Properties:

- ChromaDbService Instance: The singleton instance of the ChromaDbService class, providing access to shared HttpClient and baseUrl.

Methods:

-  ChromaDbService(): Initializes an instance of ChromaDbService with a new HttpClient and sets the base URL to communicate with ChromaDB.
    Returns: An instance of ChromaDbService
- void UpsertAsync(object param): Asynchronously sends a POST request to upsert (insert or update) the provided ContentItem into ChromaDB.
    contentItem: The ContentItem object containing data to be inserted or updated
    Returns: void

5.1.2.38 FlattenAllService

Namespace: RepoScribe.Core.Services

Manages the Flatten-All process, which involves finding Git repositories, running CodeFlattener.exe on them, and saving the output to a specified directory. It tracks progress and logs results.

Attributes:

- string _codeFlattenerPath (public): The file path to the CodeFlattener.exe used for processing directories.
- InputProcessor _inputProcessor (public): Stores the instance of InputProcessor used for processing input files.
- string _outputDirectory (public): The output directory where the flattened markdown files will be saved.
- IRenderer _renderer (public): Stores the instance of IRenderer used for rendering markdown files.

Methods:

- void FlattenAllAsync(): Asynchronously processes all Git repositories found within the current directory and its subdirectories, using CodeFlattener.exe to generate markdown files for each repository's code. The generated markdown files are saved to the specified output directory.
-  FlattenAllService(object param, object param, object param, object param): Runs the Flatten-All process to generate markdown files for all Git repositories found within the current directory and its subdirectories.
    codeFlattenerPath: The path to the CodeFlattener.exe file
    outputDirectory: The directory where generated markdown files will be saved
    inputProcessor: An instance of InputProcessor used for processing input data
    renderer: An implementation of IRenderer interface for rendering output

5.1.2.39 HttpService

Namespace: RepoScribe.Core.Services

A class responsible for handling HTTP requests and responses using the HttpClient class. It provides asynchronous methods for GET and POST operations.

Attributes:

- HttpClient _httpClient (public): An instance of HttpClient used to send HTTP requests.

Methods:

- void GetAsync(object param): Asynchronously retrieves the content of a webpage at the specified URL.
    url: The Uniform Resource Locator (URL) of the webpage to retrieve.
    Returns: null
-  HttpService(): Initializes a new instance of the HttpService class with an internal HttpClient for making HTTP requests.
- void PostAsync(object param, object param): Sends an asynchronous POST request to the specified URL with the provided HttpContent.
    url: The URI of the resource to send the POST request to
    content: The content to send in the body of the POST request

5.1.2.40 LocalDatabaseService

Namespace: RepoScribe.Core.Services

Manages local database operations, handling connections and initialization for SQLite or PostgreSQL databases based on the current environment.

Attributes:

- IConfiguration _config (public): Stores the application's configuration settings.
- string _connectionString (public): Stores the connection string used to connect to the database, determined based on the current environment.
- ILogger _logger (public): Stores the logger instance used for logging information, errors, and other messages within the LocalDatabaseService class.

Methods:

- void InitializeDatabase(): Initializes the database connection and performs setup operations such as creating tables if they do not exist, running migrations, etc.
-  LocalDatabaseService(object param, object param): Initializes a new instance of the LocalDatabaseService class with the provided configuration and logger.
    config: An IConfiguration object containing connection strings for different environments
    logger: An ILogger object to log information, errors, and warnings
- void OpenConnection(): Opens a database connection using the configured connection string.
- void TestConnection(): Tests the connection to the database using the configured connection string.
    Returns: True if the connection is successful, false otherwise

5.1.2.41 MarkdownExtractor

Namespace: RepoScribe.Core.Services

MarkdownExtractor is a class responsible for extracting code blocks from markdown files located within a specified directory.

Attributes:

- string _inputDirectory (public): Stores the input directory path where markdown files are located

Methods:

- void ExtractCodeBlocks(): Extracts code blocks from markdown files located within the input directory, using regular expressions to match and extract code block sections.
-  MarkdownExtractor(object param): Extracts code blocks from markdown files located within the specified input directory.
    inputDirectory: The directory containing the markdown files to extract code blocks from.
    Returns: An enumerable of JSON strings, each string representing a code block object with properties Id (unique identifier), Path (relative path to the code block), and Content (the actual code content).

5.1.2.42 OllamaService

Namespace: RepoScribe.Core.Services

A service class responsible for communicating with the Ollama API to retrieve data.

Attributes:

- string _baseUrl (public): The base URL for the Ollama API, used to construct full URLs when making requests.
- HttpClient _httpClient (public): An HttpClient instance used for making HTTP requests to the Ollama API.

Methods:

- void GetAsync(object param, object param): Asynchronously retrieves data from the Ollama API using the provided URL and request parameters.
    url: The endpoint URL to retrieve data from
    req: A dictionary containing request parameters
    Returns: null (void method)
-  OllamaService(): Initializes a new instance of the OllamaService class with a default HttpClient and base URL.

5.1.2.43 WorkerPool

Namespace: RepoScribe.Core.Services

A class that manages a pool of worker threads for executing tasks concurrently.

Attributes:

- CancellationTokenSource _cts (public): A CancellationTokenSource used to signal the worker tasks to stop processing new items when the pool is shut down.
- BlockingCollection<Func<Task>> _taskQueue (public): A blocking collection used to queue tasks for worker threads to process.

Methods:

- void EnqueueTask(object param): Adds a new task to the worker pool's task queue for asynchronous processing.
    task: A function that returns a Task, representing the work to be done
- void Stop(): Cancels the cancellation token source and completes adding tasks to the blocking collection, effectively stopping all worker threads.
-  WorkerPool(object param): Initializes a new instance of WorkerPool with the specified number of workers.
    workerCount: The number of worker threads to create.

5.1.2.44 ConfigurationManager

Namespace: RepoScribe.Core.Utilities

Manages application configuration by loading and providing access to configuration data. It supports multiple sources including environment variables, user's home directory, and the default application directory.

Attributes:

- IConfiguration _configuration (public): Stores the configuration settings loaded from appsettings.json files or environment variables.
- string _defaultConfigPath (public): The default file path for the application's configuration file if no other paths are specified or found.
- string _envVarConfigPath (public): Stores the path to the configuration file if set as an environment variable with the key 'REPOSCRIBE_CONFIG'. If not set, it defaults to an empty string.
- string _homeDirConfigPath (public): The default configuration path for the application, looking for a user-specific appsettings.json file in the MyDocuments folder.

Methods:

-  ConfigurationManager(object param): Initializes a new instance of ConfigurationManager with the specified configuration path.
    configPath: The file path to the configuration file
- void GetExtractChunksInputDirectory(): Retrieves the directory path for input files used in the ExtractChunks process.
    Returns: The directory path as a string, or the default path if not configured.
- void GetIgnoredPaths(): Retrieves a list of paths that should be ignored during processing.
    Returns: A List<string> containing the paths to ignore
- void GetLanguageMap(): Retrieves a dictionary mapping language identifiers to their corresponding display names from the configuration.
    Returns: A Dictionary<string, string> where keys are language identifiers and values are their display names

5.1.2.45 HashUtility

Namespace: RepoScribe.Core.Utilities

A utility class for generating hashes and unique IDs from content using SHA256 algorithm.

Methods:

- void GetContentHash(object param): Calculates the SHA-256 hash of the provided content string and returns it as a lowercase hexadecimal string without hyphens.
    content: The input string for which to calculate the hash
    Returns: null (void method)
- void GetUniqueId(object param): Generates a unique identifier by taking the first 32 characters of the SHA-256 hash of the provided content.
    content: The input string to generate the unique ID from
    Returns: null (void method)

5.1.2.46 Logger

Namespace: RepoScribe.Core.Utilities

A static utility class responsible for initializing and managing Serilog logger instances.

Methods:

- void CloseAndFlush(): Closes the current log stream and flushes all buffered logs to their destinations.
    Returns: No return value (void)
- void Initialize(): Initializes the logger with console and file output destinations. The log file will be rolled daily.

5.1.2.47 PathUtility

Namespace: RepoScribe.Core.Utilities

A utility class for converting between dotted path notation and standard file system paths.

Methods:

- void ConvertDottedPathToFilePath(object param): Converts a dotted path string (e.g., 'a.b.c') into a file system compatible path by replacing dots with the directory separator character.
    dottedPath: The input path string where dots represent directories
    Returns: null (void method)
- void ConvertFilePathToDottedPath(object param): Converts a standard file path to a dotted path representation.
    filePath: The input file path to convert
    Returns: null (void method)

5.1.2.48 RepositoryManager

Namespace: RepoScribe.Core.Utilities

Manages a list of repositories by loading them from a config file and providing methods to save changes back to the file. Uses Newtonsoft.Json for serialization.

Attributes:

- string _configPath (public): The file path to the configuration file used by this instance of RepositoryManager.

Properties:

- List<string> Repositories: A list of repository URLs managed by the RepositoryManager.

Methods:

-  RepositoryManager(object param): Initializes a new instance of the RepositoryManager class with the given configuration path.
    configPath: The file path to the JSON configuration file containing repository URLs.
- void Save(): Saves the current list of repositories to the configuration file located at _configPath.


================================================================================
Section 2
================================================================================
5.2 Unknown

Module containing 1 file(s) with related functionality.

5.2.1 Dependencies

No external dependencies.

5.2.2 Classes

