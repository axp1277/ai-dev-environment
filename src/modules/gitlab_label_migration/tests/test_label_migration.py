"""Comprehensive test suite for GitLab Label Migration utility.

Tests cover:
- Pydantic model validation
- Configuration loading
- GitLab client authentication
- Label fetching
- Label replication
- Edge cases and error handling
"""

import os
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import ValidationError

# Import modules from parent directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import (
    GitLabConfig,
    GitLabLabel,
    create_gitlab_client,
    fetch_labels_from_source,
    load_configuration,
    replicate_labels_to_destination,
)


# ============================================================================
# Pydantic Model Tests
# ============================================================================


class TestGitLabLabel:
    """Test suite for GitLabLabel Pydantic model."""

    def test_valid_label_creation(self):
        """Test creating a valid label."""
        label = GitLabLabel(
            name="bug",
            color="#FF0000",
            description="Bug reports"
        )
        assert label.name == "bug"
        assert label.color == "#FF0000"
        assert label.description == "Bug reports"

    def test_label_without_description(self):
        """Test creating a label without description."""
        label = GitLabLabel(name="feature", color="#00FF00")
        assert label.name == "feature"
        assert label.color == "#00FF00"
        assert label.description is None

    def test_color_format_validation(self):
        """Test color format validation and normalization."""
        # Without hash prefix
        label = GitLabLabel(name="test", color="FF0000")
        assert label.color == "#FF0000"

        # Lowercase hex
        label = GitLabLabel(name="test", color="#ff0000")
        assert label.color == "#FF0000"

    def test_invalid_color_format(self):
        """Test invalid color format raises validation error."""
        with pytest.raises(ValidationError):
            GitLabLabel(name="test", color="invalid")

        with pytest.raises(ValidationError):
            GitLabLabel(name="test", color="#FFF")  # Too short

        with pytest.raises(ValidationError):
            GitLabLabel(name="test", color="#GGGGGG")  # Invalid hex

    def test_empty_name_validation(self):
        """Test empty name raises validation error."""
        with pytest.raises(ValidationError):
            GitLabLabel(name="", color="#FF0000")


class TestGitLabConfig:
    """Test suite for GitLabConfig Pydantic model."""

    def test_valid_config_creation(self):
        """Test creating a valid configuration."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
            source_project_id=100,
            destination_project_id=200,
        )
        assert config.gitlab_url == "https://gitlab.example.com"
        assert config.gitlab_token == "test-token-123"
        assert config.source_project_id == 100
        assert config.destination_project_id == 200

    def test_default_gitlab_url(self):
        """Test default GitLab URL."""
        config = GitLabConfig(
            gitlab_token="token",
            source_project_id=1,
            destination_project_id=2,
        )
        assert config.gitlab_url == "https://gitlab.com"

    def test_invalid_project_ids(self):
        """Test invalid project IDs raise validation error."""
        with pytest.raises(ValidationError):
            GitLabConfig(
                gitlab_token="token",
                source_project_id=0,  # Must be > 0
                destination_project_id=1,
            )

        with pytest.raises(ValidationError):
            GitLabConfig(
                gitlab_token="token",
                source_project_id=-1,  # Must be > 0
                destination_project_id=1,
            )

    def test_empty_token_validation(self):
        """Test empty token raises validation error."""
        with pytest.raises(ValidationError):
            GitLabConfig(
                gitlab_token="",
                source_project_id=1,
                destination_project_id=2,
            )

        with pytest.raises(ValidationError):
            GitLabConfig(
                gitlab_token="   ",  # Whitespace only
                source_project_id=1,
                destination_project_id=2,
            )


# ============================================================================
# Configuration Loading Tests
# ============================================================================


class TestLoadConfiguration:
    """Test suite for configuration loading."""

    @patch.dict(os.environ, {
        "GITLAB_TOKEN": "test-token",
        "SOURCE_PROJECT_ID": "100",
        "DESTINATION_PROJECT_ID": "200",
    }, clear=True)
    def test_load_valid_configuration(self):
        """Test loading valid configuration from environment."""
        config = load_configuration()
        assert config.gitlab_token == "test-token"
        assert config.source_project_id == 100
        assert config.destination_project_id == 200
        assert config.gitlab_url == "https://gitlab.com"

    @patch.dict(os.environ, {
        "GITLAB_URL": "https://gitlab.example.com",
        "GITLAB_TOKEN": "test-token",
        "SOURCE_PROJECT_ID": "100",
        "DESTINATION_PROJECT_ID": "200",
    }, clear=True)
    def test_load_configuration_with_custom_url(self):
        """Test loading configuration with custom GitLab URL."""
        config = load_configuration()
        assert config.gitlab_url == "https://gitlab.example.com"

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_token_raises_error(self):
        """Test missing token raises ValueError."""
        with pytest.raises(ValueError, match="GITLAB_TOKEN"):
            load_configuration()

    @patch.dict(os.environ, {"GITLAB_TOKEN": "token"}, clear=True)
    def test_missing_source_project_id_raises_error(self):
        """Test missing source project ID raises ValueError."""
        with pytest.raises(ValueError, match="SOURCE_PROJECT_ID"):
            load_configuration()

    @patch.dict(os.environ, {
        "GITLAB_TOKEN": "token",
        "SOURCE_PROJECT_ID": "invalid",
        "DESTINATION_PROJECT_ID": "200",
    }, clear=True)
    def test_invalid_project_id_format(self):
        """Test invalid project ID format raises error."""
        with pytest.raises(ValueError):
            load_configuration()


# ============================================================================
# GitLab Client Tests
# ============================================================================


class TestCreateGitLabClient:
    """Test suite for GitLab client creation."""

    @patch("main.gitlab.Gitlab")
    def test_successful_authentication(self, mock_gitlab_class):
        """Test successful GitLab client authentication."""
        # Setup mock
        mock_client = MagicMock()
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_client.user = mock_user
        mock_gitlab_class.return_value = mock_client

        config = GitLabConfig(
            gitlab_token="token",
            source_project_id=1,
            destination_project_id=2,
        )

        client = create_gitlab_client(config)

        # Verify
        mock_gitlab_class.assert_called_once_with(
            url="https://gitlab.com",
            private_token="token"
        )
        mock_client.auth.assert_called_once()
        assert client == mock_client

    @patch("main.gitlab.Gitlab")
    def test_authentication_failure(self, mock_gitlab_class):
        """Test authentication failure raises error."""
        import gitlab as gitlab_module

        mock_client = MagicMock()
        mock_client.auth.side_effect = gitlab_module.exceptions.GitlabAuthenticationError()
        mock_gitlab_class.return_value = mock_client

        config = GitLabConfig(
            gitlab_token="invalid",
            source_project_id=1,
            destination_project_id=2,
        )

        with pytest.raises(gitlab_module.exceptions.GitlabAuthenticationError):
            create_gitlab_client(config)


# ============================================================================
# Label Fetching Tests
# ============================================================================


class TestFetchLabelsFromSource:
    """Test suite for fetching labels from source project."""

    @patch("main.gitlab.Gitlab")
    def test_fetch_labels_success(self, mock_gitlab_class):
        """Test successfully fetching labels from source project."""
        # Setup mock
        mock_label1 = MagicMock()
        mock_label1.name = "bug"
        mock_label1.color = "#FF0000"
        mock_label1.description = "Bug reports"

        mock_label2 = MagicMock()
        mock_label2.name = "feature"
        mock_label2.color = "#00FF00"
        mock_label2.description = None

        mock_project = MagicMock()
        mock_project.labels.list.return_value = [mock_label1, mock_label2]

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = fetch_labels_from_source(mock_client, 100)

        assert len(labels) == 2
        assert labels[0].name == "bug"
        assert labels[0].color == "#FF0000"
        assert labels[1].name == "feature"
        assert labels[1].color == "#00FF00"

    @patch("main.gitlab.Gitlab")
    def test_fetch_empty_labels(self, mock_gitlab_class):
        """Test fetching from project with no labels."""
        mock_project = MagicMock()
        mock_project.labels.list.return_value = []

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = fetch_labels_from_source(mock_client, 100)

        assert labels == []

    @patch("main.gitlab.Gitlab")
    def test_fetch_labels_invalid_label_skipped(self, mock_gitlab_class):
        """Test that invalid labels are skipped."""
        mock_valid_label = MagicMock()
        mock_valid_label.name = "valid"
        mock_valid_label.color = "#FF0000"
        mock_valid_label.description = None

        mock_invalid_label = MagicMock()
        mock_invalid_label.name = "invalid"
        mock_invalid_label.color = "not-a-color"
        mock_invalid_label.description = None

        mock_project = MagicMock()
        mock_project.labels.list.return_value = [mock_valid_label, mock_invalid_label]

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = fetch_labels_from_source(mock_client, 100)

        assert len(labels) == 1
        assert labels[0].name == "valid"


# ============================================================================
# Label Replication Tests
# ============================================================================


class TestReplicateLabelsToDestination:
    """Test suite for replicating labels to destination project."""

    @patch("main.gitlab.Gitlab")
    def test_create_new_labels(self, mock_gitlab_class):
        """Test creating new labels in destination project."""
        mock_project = MagicMock()
        mock_project.labels.list.return_value = []  # No existing labels

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = [
            GitLabLabel(name="bug", color="#FF0000", description="Bugs"),
            GitLabLabel(name="feature", color="#00FF00"),
        ]

        summary = replicate_labels_to_destination(mock_client, 200, labels)

        assert summary["created"] == 2
        assert summary["updated"] == 0
        assert summary["skipped"] == 0
        assert summary["failed"] == 0
        assert mock_project.labels.create.call_count == 2

    @patch("main.gitlab.Gitlab")
    def test_update_existing_labels(self, mock_gitlab_class):
        """Test updating existing labels with different colors."""
        mock_existing = MagicMock()
        mock_existing.name = "bug"
        mock_existing.color = "#0000FF"  # Different color

        mock_project = MagicMock()
        mock_project.labels.list.return_value = [mock_existing]

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = [GitLabLabel(name="bug", color="#FF0000")]

        summary = replicate_labels_to_destination(mock_client, 200, labels)

        assert summary["created"] == 0
        assert summary["updated"] == 1
        assert summary["skipped"] == 0
        assert summary["failed"] == 0
        assert mock_existing.color == "#FF0000"
        mock_existing.save.assert_called_once()

    @patch("main.gitlab.Gitlab")
    def test_skip_unchanged_labels(self, mock_gitlab_class):
        """Test skipping labels that haven't changed."""
        mock_existing = MagicMock()
        mock_existing.name = "bug"
        mock_existing.color = "#FF0000"  # Same color

        mock_project = MagicMock()
        mock_project.labels.list.return_value = [mock_existing]

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = [GitLabLabel(name="bug", color="#FF0000")]

        summary = replicate_labels_to_destination(mock_client, 200, labels)

        assert summary["created"] == 0
        assert summary["updated"] == 0
        assert summary["skipped"] == 1
        assert summary["failed"] == 0
        mock_existing.save.assert_not_called()

    @patch("main.gitlab.Gitlab")
    def test_mixed_operations(self, mock_gitlab_class):
        """Test mixed create, update, and skip operations."""
        mock_existing1 = MagicMock()
        mock_existing1.name = "bug"
        mock_existing1.color = "#0000FF"  # Will be updated

        mock_existing2 = MagicMock()
        mock_existing2.name = "feature"
        mock_existing2.color = "#00FF00"  # Will be skipped

        mock_project = MagicMock()
        mock_project.labels.list.return_value = [mock_existing1, mock_existing2]

        mock_client = MagicMock()
        mock_client.projects.get.return_value = mock_project

        labels = [
            GitLabLabel(name="bug", color="#FF0000"),  # Update
            GitLabLabel(name="feature", color="#00FF00"),  # Skip
            GitLabLabel(name="enhancement", color="#FFFF00"),  # Create
        ]

        summary = replicate_labels_to_destination(mock_client, 200, labels)

        assert summary["created"] == 1
        assert summary["updated"] == 1
        assert summary["skipped"] == 1
        assert summary["failed"] == 0


# ============================================================================
# Integration Tests
# ============================================================================


class TestIntegration:
    """Integration tests with mocked GitLab API."""

    @patch("main.gitlab.Gitlab")
    @patch.dict(os.environ, {
        "GITLAB_TOKEN": "test-token",
        "SOURCE_PROJECT_ID": "100",
        "DESTINATION_PROJECT_ID": "200",
    }, clear=True)
    def test_end_to_end_migration(self, mock_gitlab_class):
        """Test complete end-to-end label migration."""
        # Setup source project
        mock_source_label = MagicMock()
        mock_source_label.name = "bug"
        mock_source_label.color = "#FF0000"
        mock_source_label.description = "Bug reports"

        mock_source_project = MagicMock()
        mock_source_project.labels.list.return_value = [mock_source_label]

        # Setup destination project
        mock_dest_project = MagicMock()
        mock_dest_project.labels.list.return_value = []

        # Setup client
        mock_client = MagicMock()
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_client.user = mock_user

        def get_project(project_id):
            if project_id == 100:
                return mock_source_project
            return mock_dest_project

        mock_client.projects.get.side_effect = get_project
        mock_gitlab_class.return_value = mock_client

        # Execute
        config = load_configuration()
        client = create_gitlab_client(config)
        labels = fetch_labels_from_source(client, config.source_project_id)
        summary = replicate_labels_to_destination(
            client,
            config.destination_project_id,
            labels
        )

        # Verify
        assert len(labels) == 1
        assert summary["created"] == 1
        assert summary["failed"] == 0
