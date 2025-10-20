﻿//using System;
//using System.IO;
//using System.Text;
//using Xunit;
//using Moq;
//using Microsoft.Extensions.Configuration;

//namespace RepoScribe.Tests
//{
//    public class RepoScribeTests : IDisposable
//    {
//        private readonly string testDir;
//        private readonly string outputFile;

//        public RepoScribeTests()
//        {
//            testDir = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());
//            Directory.CreateDirectory(testDir);
//            outputFile = Path.Combine(testDir, "output.md");

//            // Create test files and directories
//            Directory.CreateDirectory(Path.Combine(testDir, "subfolder"));
//            Directory.CreateDirectory(Path.Combine(testDir, ".git"));
//            File.WriteAllText(Path.Combine(testDir, "test.cs"), "Console.WriteLine(\"Hello, World!\");");
//            File.WriteAllText(Path.Combine(testDir, "subfolder", "test.js"), "console.log(\"Hello, World!\");");
//            File.WriteAllText(Path.Combine(testDir, ".git", "config"), "# Git config file");
//        }

//        void IDisposable.Dispose()
//        {
//            Directory.Delete(testDir, true);
//        }

//        [Fact]
//        public void FlattenCodebase_CreatesCorrectMarkdownContent()
//        {
//            // Arrange
//            string[] acceptedFileTypes = [".cs", ".js"];
//            string[] ignoredPaths = [".git"];

//            // Act
//            Flattener.FlattenCodebase(testDir, outputFile, acceptedFileTypes, ignoredPaths, false);

//            // Assert
//            string content = File.ReadAllText(outputFile);
//            Assert.Contains("# test.cs", content);
//            Assert.Contains("```csharp", content);
//            Assert.Contains("Console.WriteLine(\"Hello, World!\");", content);
//            Assert.Contains("# subfolder/test.js", content);
//            Assert.Contains("```javascript", content);
//            Assert.Contains("console.log(\"Hello, World!\");", content);
//            Assert.DoesNotContain("# .git/config", content);
//        }

//        [Fact]
//        public void FlattenCodebase_WithCompression_CompressesContent()
//        {
//            // Arrange
//            string[] acceptedFileTypes = [".cs"];
//            string[] ignoredPaths = [];

//            // Act
//            Flattener.FlattenCodebase(testDir, outputFile, acceptedFileTypes, ignoredPaths, true);

//            // Assert
//            string content = File.ReadAllText(outputFile);
//            Assert.Contains("Console.WriteLine(\"Hello,World!\");", content);
//            Assert.DoesNotContain("Console.WriteLine(\"Hello, World!\");", content);
//        }

//        [Fact]
//        public void FlattenCodebase_WithIgnoredPaths_ExcludesIgnoredFiles()
//        {
//            // Arrange
//            string[] acceptedFileTypes = [".cs", ".js"];
//            string[] ignoredPaths = ["subfolder"];

//            // Act
//            Flattener.FlattenCodebase(testDir, outputFile, acceptedFileTypes, ignoredPaths, false);

//            // Assert
//            string content = File.ReadAllText(outputFile);
//            Assert.Contains("# test.cs", content);
//            Assert.DoesNotContain("# subfolder/test.js", content);
//        }

//        [Theory]
//        [InlineData("test.cs", "csharp")]
//        [InlineData("test.js", "javascript")]
//        [InlineData("test.txt", "plaintext")]
//        [InlineData("unknown.xyz", "")]
//        public void GetLanguageIdentifier_ReturnsCorrectIdentifier(string fileName, string expectedIdentifier)
//        {
//            // Act
//            string result = FileHelper.GetLanguageIdentifier(fileName);

//            // Assert
//            Assert.Equal(expectedIdentifier, result);
//        }

//        [Fact]
//        public void RunRepoScribe_WithValidArguments_FlattensCodabase()
//        {
//            // Arrange
//            string[] args = [testDir, outputFile];
//            var mockConfiguration = new Mock<IConfiguration>();
//            mockConfiguration.Setup(c => c.GetSection("AcceptedFileTypes").Value).Returns(".cs,.js");
//            mockConfiguration.Setup(c => c.GetSection("IgnoredPaths").Value).Returns(".git");

//            // Act
//            Program.RunRepoScribe(args, mockConfiguration.Object);

//            // Assert
//            Assert.True(File.Exists(outputFile));
//            string content = File.ReadAllText(outputFile);
//            Assert.Contains("# test.cs", content);
//            Assert.Contains("# subfolder/test.js", content);
//            Assert.DoesNotContain("# .git/config", content);
//        }

//        [Fact]
//        public void RunRepoScribe_WithInvalidArguments_DoesNotFlattenCodebase()
//        {
//            // Arrange
//            string[] args = ["invalid_path", outputFile];
//            var mockConfiguration = new Mock<IConfiguration>();
//            mockConfiguration.Setup(c => c.GetSection("AcceptedFileTypes").Value).Returns(".cs,.js");
//            mockConfiguration.Setup(c => c.GetSection("IgnoredPaths").Value).Returns(".git");

//            // Act & Assert
//            var exception = Assert.Throws<DirectoryNotFoundException>(() => Program.RunRepoScribe(args, mockConfiguration.Object));
//            Assert.Contains("Directory not found: invalid_path", exception.Message);
//        }

//        [Fact]
//        public void RunRepoScribe_WithCompressionFlag_CompressesOutput()
//        {
//            // Arrange
//            string[] args = [testDir, outputFile, "-c"];
//            var mockConfiguration = new Mock<IConfiguration>();
//            mockConfiguration.Setup(c => c.GetSection("AcceptedFileTypes").Value).Returns(".cs");
//            mockConfiguration.Setup(c => c.GetSection("IgnoredPaths").Value).Returns(".git");

//            // Act
//            Program.RunRepoScribe(args, mockConfiguration.Object);

//            // Assert
//            Assert.True(File.Exists(outputFile));
//            string content = File.ReadAllText(outputFile);
//            Assert.Contains("Console.WriteLine(\"Hello,World!\");", content);
//            Assert.DoesNotContain("Console.WriteLine(\"Hello, World!\");", content);
//        }
//    }
//}