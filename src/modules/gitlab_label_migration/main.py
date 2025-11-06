"""GitLab Label Migration Utility.

This module provides a minimalistic utility for migrating labels from one GitLab
project to another. It fetches all labels (names, colors, descriptions) from a
source project and replicates them to a destination project.

Usage:
    uv run python main.py

Configuration:
    Create a .env file with the following variables:
    - GITLAB_TOKEN: Personal access token with API access
    - SOURCE_PROJECT_ID: ID of the source GitLab project
    - DESTINATION_PROJECT_ID: ID of the destination GitLab project
    - GITLAB_URL: (Optional) GitLab instance URL, defaults to https://gitlab.com
"""

import os
import sys
import time
from typing import Optional

import gitlab
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field, ValidationError, field_validator


# ============================================================================
# Pydantic Models
# ============================================================================


class GitLabLabel(BaseModel):
    """Model representing a GitLab label.

    Attributes:
        name: The label name
        color: Hex color code (e.g., #FF0000)
        description: Optional label description
    """

    name: str = Field(..., min_length=1, description="Label name")
    color: str = Field(..., description="Hex color code")
    description: Optional[str] = Field(None, description="Label description")

    @field_validator("color", mode="before")
    @classmethod
    def validate_color_format(cls, v: str) -> str:
        """Ensure color is in proper hex format."""
        if not v.startswith("#"):
            v = f"#{v}"
        v = v.upper()
        # Validate format
        if len(v) != 7 or not all(c in "0123456789ABCDEF" for c in v[1:]):
            raise ValueError(f"Invalid hex color format: {v}")
        return v


class GitLabConfig(BaseModel):
    """Configuration model for GitLab label migration.

    Attributes:
        gitlab_url: GitLab instance URL
        gitlab_token: Personal access token with API scope
        source_project_id: Source project ID to fetch labels from
        destination_project_id: Destination project ID to create labels in
    """

    gitlab_url: str = Field(
        default="https://gitlab.com",
        description="GitLab instance URL"
    )
    gitlab_token: str = Field(..., min_length=1, description="GitLab API token")
    source_project_id: int = Field(..., gt=0, description="Source project ID")
    destination_project_id: int = Field(..., gt=0, description="Destination project ID")

    @field_validator("gitlab_token")
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate token is not empty."""
        if not v or v.isspace():
            raise ValueError("GitLab token cannot be empty or whitespace")
        return v


# ============================================================================
# Configuration Loading
# ============================================================================


def load_configuration() -> GitLabConfig:
    """Load and validate configuration from environment variables.

    Returns:
        GitLabConfig: Validated configuration object

    Raises:
        ValidationError: If configuration is invalid
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
    gitlab_token = os.getenv("GITLAB_TOKEN")
    source_project_id = os.getenv("SOURCE_PROJECT_ID")
    destination_project_id = os.getenv("DESTINATION_PROJECT_ID")

    if not gitlab_token:
        raise ValueError("GITLAB_TOKEN environment variable is required")
    if not source_project_id:
        raise ValueError("SOURCE_PROJECT_ID environment variable is required")
    if not destination_project_id:
        raise ValueError("DESTINATION_PROJECT_ID environment variable is required")

    try:
        config = GitLabConfig(
            gitlab_url=gitlab_url,
            gitlab_token=gitlab_token,
            source_project_id=int(source_project_id),
            destination_project_id=int(destination_project_id),
        )
        logger.debug(f"Configuration loaded: URL={config.gitlab_url}, "
                    f"Source={config.source_project_id}, "
                    f"Destination={config.destination_project_id}")
        return config
    except (ValueError, ValidationError) as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


# ============================================================================
# GitLab Client Authentication
# ============================================================================


def create_gitlab_client(config: GitLabConfig) -> gitlab.Gitlab:
    """Create and authenticate GitLab client.

    Args:
        config: GitLab configuration

    Returns:
        gitlab.Gitlab: Authenticated GitLab client

    Raises:
        gitlab.exceptions.GitlabAuthenticationError: If authentication fails
        gitlab.exceptions.GitlabError: If connection fails
    """
    try:
        logger.info(f"Connecting to GitLab at {config.gitlab_url}")
        gl = gitlab.Gitlab(url=config.gitlab_url, private_token=config.gitlab_token)

        # Verify authentication by fetching current user
        gl.auth()
        user = gl.user
        logger.info(f"Successfully authenticated as: {user.username}")
        return gl

    except gitlab.exceptions.GitlabAuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        raise
    except gitlab.exceptions.GitlabError as e:
        logger.error(f"Failed to connect to GitLab: {e}")
        raise


# ============================================================================
# Label Operations
# ============================================================================


def fetch_labels_from_source(
    gl: gitlab.Gitlab,
    project_id: int
) -> list[GitLabLabel]:
    """Fetch all labels from source project.

    Args:
        gl: Authenticated GitLab client
        project_id: Source project ID

    Returns:
        list[GitLabLabel]: List of labels from source project

    Raises:
        gitlab.exceptions.GitlabError: If project access fails
    """
    try:
        logger.info(f"Fetching labels from source project {project_id}")
        project = gl.projects.get(project_id)

        # Fetch all labels
        labels = project.labels.list(get_all=True)

        if not labels:
            logger.warning(f"No labels found in source project {project_id}")
            return []

        # Parse into Pydantic models
        parsed_labels = []
        for label in labels:
            try:
                gitlab_label = GitLabLabel(
                    name=label.name,
                    color=label.color,
                    description=getattr(label, "description", None) or None,
                )
                parsed_labels.append(gitlab_label)
                logger.debug(f"Fetched label: {gitlab_label.name} ({gitlab_label.color})")
            except ValidationError as e:
                logger.warning(f"Skipping invalid label {label.name}: {e}")
                continue

        logger.info(f"Successfully fetched {len(parsed_labels)} labels from source project")
        return parsed_labels

    except gitlab.exceptions.GitlabGetError as e:
        logger.error(f"Failed to access source project {project_id}: {e}")
        raise
    except gitlab.exceptions.GitlabError as e:
        logger.error(f"Error fetching labels from project {project_id}: {e}")
        raise


def replicate_labels_to_destination(
    gl: gitlab.Gitlab,
    project_id: int,
    labels: list[GitLabLabel],
    retry_attempts: int = 3,
    retry_delay: float = 1.0,
) -> dict[str, int]:
    """Replicate labels to destination project.

    Args:
        gl: Authenticated GitLab client
        project_id: Destination project ID
        labels: List of labels to replicate
        retry_attempts: Number of retry attempts for rate limiting
        retry_delay: Delay between retries in seconds

    Returns:
        dict: Summary with 'created', 'updated', 'skipped', 'failed' counts

    Raises:
        gitlab.exceptions.GitlabError: If project access fails
    """
    try:
        logger.info(f"Replicating labels to destination project {project_id}")
        project = gl.projects.get(project_id)

        # Fetch existing labels to check for duplicates
        existing_labels = {label.name: label for label in project.labels.list(get_all=True)}

        summary = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}

        for label in labels:
            attempt = 0
            while attempt < retry_attempts:
                try:
                    if label.name in existing_labels:
                        existing = existing_labels[label.name]
                        # Check if color differs
                        if existing.color.upper() != label.color.upper():
                            existing.color = label.color
                            if label.description:
                                existing.description = label.description
                            existing.save()
                            logger.info(f"Updated label: {label.name} -> {label.color}")
                            summary["updated"] += 1
                        else:
                            logger.debug(f"Skipped label (unchanged): {label.name}")
                            summary["skipped"] += 1
                    else:
                        # Create new label
                        project.labels.create({
                            "name": label.name,
                            "color": label.color,
                            "description": label.description or "",
                        })
                        logger.info(f"Created label: {label.name} -> {label.color}")
                        summary["created"] += 1

                    break  # Success, exit retry loop

                except gitlab.exceptions.GitlabCreateError as e:
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        attempt += 1
                        if attempt < retry_attempts:
                            wait_time = retry_delay * (2 ** (attempt - 1))
                            logger.warning(f"Rate limit hit, retrying in {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            logger.error(f"Failed to create label {label.name} after "
                                       f"{retry_attempts} attempts: {e}")
                            summary["failed"] += 1
                            break
                    else:
                        logger.error(f"Failed to create label {label.name}: {e}")
                        summary["failed"] += 1
                        break

                except gitlab.exceptions.GitlabError as e:
                    logger.error(f"Error processing label {label.name}: {e}")
                    summary["failed"] += 1
                    break

        logger.info(f"Label replication complete: {summary}")
        return summary

    except gitlab.exceptions.GitlabGetError as e:
        logger.error(f"Failed to access destination project {project_id}: {e}")
        raise
    except gitlab.exceptions.GitlabError as e:
        logger.error(f"Error replicating labels to project {project_id}: {e}")
        raise


# ============================================================================
# Main Orchestration
# ============================================================================


def main() -> int:
    """Main entry point for GitLab label migration utility.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<level>{message}</level>",
        level="INFO",
    )

    try:
        logger.info("Starting GitLab Label Migration Utility")

        # Load configuration
        logger.info("Loading configuration from environment")
        config = load_configuration()

        # Create GitLab client
        gl = create_gitlab_client(config)

        # Fetch labels from source
        labels = fetch_labels_from_source(gl, config.source_project_id)

        if not labels:
            logger.warning("No labels to migrate. Exiting.")
            return 0

        # Replicate to destination
        summary = replicate_labels_to_destination(
            gl,
            config.destination_project_id,
            labels,
        )

        # Display final summary
        logger.info("=" * 60)
        logger.info("Migration Summary:")
        logger.info(f"  Total labels processed: {len(labels)}")
        logger.info(f"  Created: {summary['created']}")
        logger.info(f"  Updated: {summary['updated']}")
        logger.info(f"  Skipped: {summary['skipped']}")
        logger.info(f"  Failed: {summary['failed']}")
        logger.info("=" * 60)

        if summary["failed"] > 0:
            logger.warning("Some labels failed to migrate. Check logs above.")
            return 1

        logger.info("Label migration completed successfully!")
        return 0

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except gitlab.exceptions.GitlabAuthenticationError:
        logger.error("Authentication failed. Check your GITLAB_TOKEN.")
        return 1
    except gitlab.exceptions.GitlabError as e:
        logger.error(f"GitLab API error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.warning("Migration interrupted by user")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
