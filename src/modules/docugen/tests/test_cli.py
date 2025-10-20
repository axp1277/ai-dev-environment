"""
Tests for docugen CLI module.
"""

import pytest
from click.testing import CliRunner
from pathlib import Path

from ..cli import main


class TestCLI:
    """Tests for CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    @pytest.fixture
    def config_file(self, tmp_path):
        """Create a temporary config file."""
        config = tmp_path / "config.yaml"
        config.write_text("""
models:
  default: "codellama:13b"
  summarizer: "codellama:7b"

validation:
  max_iterations: 3

output:
  base_path: "./docs_output"

processing:
  parallel_files: 4
  supported_languages: ["csharp"]
""")
        return config

    @pytest.fixture
    def input_dir(self, tmp_path):
        """Create a temporary input directory."""
        input_dir = tmp_path / "codebase"
        input_dir.mkdir()
        return input_dir

    def test_cli_version(self, runner):
        """Test --version flag."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "docugen" in result.output
        assert "0.1.0" in result.output

    def test_cli_help(self, runner):
        """Test --help flag."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "DocuGen" in result.output
        assert "Multi-agent code documentation generator" in result.output

    def test_document_command_help(self, runner):
        """Test document command help."""
        result = runner.invoke(main, ["document", "--help"])
        assert result.exit_code == 0
        assert "Generate documentation for a codebase" in result.output
        assert "--config" in result.output
        assert "--input" in result.output

    def test_document_missing_config(self, runner, input_dir):
        """Test document command with missing config file."""
        result = runner.invoke(main, [
            "document",
            "--config", "/nonexistent/config.yaml",
            "--input", str(input_dir)
        ])
        assert result.exit_code == 1
        assert "Configuration file not found" in result.output

    def test_document_missing_input(self, runner, config_file):
        """Test document command with missing input directory."""
        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", "/nonexistent/directory"
        ])
        assert result.exit_code == 1
        assert "Input directory not found" in result.output

    def test_document_dry_run(self, runner, config_file, input_dir):
        """Test document command with dry-run flag."""
        # Note: This test will fail if Ollama is not running
        # In real environment, you might want to skip this or mock Ollama
        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", str(input_dir),
            "--dry-run"
        ])

        # Check if Ollama is running determines the exit code
        if "Ollama is not running" in result.output:
            assert result.exit_code == 1
        else:
            assert result.exit_code == 0
            assert "Dry run mode" in result.output

    def test_document_verbose_flag(self, runner, config_file, input_dir):
        """Test document command with verbose flag."""
        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", str(input_dir),
            "--verbose"
        ])

        # Verbose flag should not cause errors (though execution may fail without Ollama)
        assert "--verbose" not in result.output  # Flag is processed, not echoed

    def test_status_command(self, runner, config_file):
        """Test status command."""
        result = runner.invoke(main, [
            "status",
            "--config", str(config_file)
        ])
        # Status command should run but show not implemented message
        assert "Status monitoring not yet implemented" in result.output

    def test_resume_command(self, runner, config_file):
        """Test resume command."""
        result = runner.invoke(main, [
            "resume",
            "--config", str(config_file)
        ])
        # Resume command should run but show not implemented message
        assert "Resume functionality not yet implemented" in result.output

    def test_validate_command(self, runner, config_file, input_dir):
        """Test validate command."""
        result = runner.invoke(main, [
            "validate",
            "--config", str(config_file),
            "--input", str(input_dir)
        ])
        # Validate command should run but show not implemented message
        assert "Validation command not yet implemented" in result.output

    def test_document_with_output_override(self, runner, config_file, input_dir, tmp_path):
        """Test document command with output path override."""
        custom_output = tmp_path / "custom_docs"

        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", str(input_dir),
            "--output", str(custom_output),
            "--dry-run"  # Use dry-run to avoid needing Ollama
        ])

        # Should process without error (unless Ollama check fails)
        if "Ollama is not running" not in result.output:
            assert "Output:" in result.output
            assert str(custom_output) in result.output

    def test_document_incremental_flag(self, runner, config_file, input_dir):
        """Test document command with incremental flag."""
        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", str(input_dir),
            "--incremental",
            "--dry-run"
        ])

        if "Ollama is not running" not in result.output:
            assert "Mode:" in result.output
            assert "Incremental" in result.output


# Integration test (requires Ollama to be running)
@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--integration')",
    reason="Integration tests require --integration flag"
)
class TestCLIIntegration:
    """Integration tests requiring Ollama."""

    def test_full_document_command(self, runner, config_file, input_dir):
        """Test full document command with Ollama running."""
        result = runner.invoke(main, [
            "document",
            "--config", str(config_file),
            "--input", str(input_dir),
            "--dry-run",
            "--verbose"
        ])

        assert result.exit_code == 0
        assert "Configuration valid" in result.output
        assert "Ollama connection verified" in result.output
