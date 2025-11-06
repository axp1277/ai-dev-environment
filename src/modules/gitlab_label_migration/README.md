# GitLab Label Migration Utility

A minimalistic, single-file Python utility for seamlessly migrating labels from one GitLab repository to another. This tool fetches all labels (names, colors, descriptions) from a source project and replicates them to a destination project.

## Features

- Simple single-file implementation
- Pydantic-based configuration validation
- Automatic label creation and updates
- Handles duplicate labels intelligently (creates new, updates changed, skips unchanged)
- Rate limit handling with exponential backoff
- Comprehensive logging with loguru
- Full test coverage with pytest

## Requirements

- Python 3.13+
- uv package manager
- GitLab personal access token with API scope

## Installation

1. Clone or navigate to this directory:
```bash
cd src/modules/gitlab_label_migration
```

2. Install dependencies using uv:
```bash
uv sync
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your actual values:
```env
# GitLab Personal Access Token (required)
# Generate at: https://gitlab.com/-/user_settings/personal_access_tokens
# Required scopes: api, read_api
GITLAB_TOKEN=your_personal_access_token_here

# Source Project ID (required)
# Find in project settings or URL
SOURCE_PROJECT_ID=12345

# Destination Project ID (required)
# Find in project settings or URL
DESTINATION_PROJECT_ID=67890

# GitLab Instance URL (optional)
# Defaults to https://gitlab.com
# For self-hosted GitLab, specify your instance URL:
# GITLAB_URL=https://gitlab.example.com
```

### Finding Project IDs

You can find your project ID in several ways:

1. **From Project Settings**: Navigate to Settings > General in your GitLab project
2. **From URL**: The project ID is often visible in the project URL
3. **From API**: Visit `https://gitlab.com/api/v4/projects?search=your-project-name`

### Required GitLab Permissions

Your personal access token must have:
- **Read access** to source project (at least Reporter role)
- **Write access** to destination project (at least Developer role)
- **API scope** enabled when generating the token

## Usage

### Basic Usage

Run the utility using uv:
```bash
uv run python main.py
```

### With Virtual Environment

Alternatively, activate the virtual environment first:
```bash
# Mac/Linux
source .venv/bin/activate

# Windows
.venv\scripts\activate

# Then run
python main.py
```

## How It Works

The utility follows this workflow:

1. **Load Configuration**: Reads and validates configuration from `.env` file
2. **Authenticate**: Connects to GitLab and verifies authentication
3. **Fetch Labels**: Retrieves all labels from the source project
4. **Parse Labels**: Validates label data using Pydantic models
5. **Replicate Labels**: For each label in the destination project:
   - **Create** if label doesn't exist
   - **Update** if label exists but color differs
   - **Skip** if label is unchanged
6. **Display Summary**: Shows counts of created, updated, skipped, and failed labels

### Label Comparison Logic

- Labels are matched by **name** (case-sensitive)
- If a label with the same name exists, colors are compared
- Color comparison is case-insensitive (e.g., `#ff0000` matches `#FF0000`)
- If colors differ, the existing label is updated
- If colors match, the label is skipped (no API call made)

## Output Example

```
2025-11-06 15:30:45 | INFO     | Starting GitLab Label Migration Utility
2025-11-06 15:30:45 | INFO     | Loading configuration from environment
2025-11-06 15:30:45 | INFO     | Connecting to GitLab at https://gitlab.com
2025-11-06 15:30:46 | INFO     | Successfully authenticated as: johndoe
2025-11-06 15:30:46 | INFO     | Fetching labels from source project 12345
2025-11-06 15:30:47 | INFO     | Successfully fetched 8 labels from source project
2025-11-06 15:30:47 | INFO     | Replicating labels to destination project 67890
2025-11-06 15:30:48 | INFO     | Created label: bug → #FF0000
2025-11-06 15:30:48 | INFO     | Created label: feature → #00FF00
2025-11-06 15:30:48 | INFO     | Updated label: enhancement → #FFFF00
2025-11-06 15:30:49 | INFO     | Skipped label (unchanged): documentation
...
2025-11-06 15:30:52 | INFO     | ============================================================
2025-11-06 15:30:52 | INFO     | Migration Summary:
2025-11-06 15:30:52 | INFO     |   Total labels processed: 8
2025-11-06 15:30:52 | INFO     |   Created: 5
2025-11-06 15:30:52 | INFO     |   Updated: 1
2025-11-06 15:30:52 | INFO     |   Skipped: 2
2025-11-06 15:30:52 | INFO     |   Failed: 0
2025-11-06 15:30:52 | INFO     | ============================================================
2025-11-06 15:30:52 | INFO     | Label migration completed successfully!
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest tests/ --cov=main --cov-report=term-missing

# Run specific test class
uv run pytest tests/test_label_migration.py::TestGitLabLabel

# Run with verbose output
uv run pytest tests/ -v
```

The test suite includes:
- Pydantic model validation tests
- Configuration loading tests
- GitLab client authentication tests
- Label fetching and replication tests
- Edge case handling (empty labels, duplicates, rate limits)
- Integration tests with mocked API

## Error Handling

The utility handles various error scenarios:

### Authentication Errors
```
ERROR | Authentication failed. Check your GITLAB_TOKEN.
```
**Solution**: Verify your token is correct and has API scope enabled.

### Missing Configuration
```
ERROR | Configuration error: SOURCE_PROJECT_ID environment variable is required
```
**Solution**: Ensure all required variables are set in `.env` file.

### Project Access Errors
```
ERROR | Failed to access source project 12345: 404 Project Not Found
```
**Solution**: Verify project ID is correct and your token has access to the project.

### Rate Limiting
```
WARNING | Rate limit hit, retrying in 2.0s...
```
The utility automatically retries with exponential backoff. If rate limits persist, wait a few minutes before retrying.

## Troubleshooting

### Issue: "Authentication failed"
- Verify your `GITLAB_TOKEN` is correct
- Ensure token has `api` scope enabled
- Check token hasn't expired

### Issue: "Project Not Found"
- Confirm project IDs are correct
- Verify your account has access to both projects
- For private projects, ensure token has sufficient permissions

### Issue: "Permission denied"
- Source project: Ensure you have at least Reporter role
- Destination project: Ensure you have at least Developer role

### Issue: Rate limit errors persist
- Wait a few minutes between migration attempts
- Consider migrating during off-peak hours
- For large label sets, GitLab may temporarily throttle requests

## Project Structure

```
gitlab_label_migration/
├── main.py              # Main implementation (single file)
├── .env                 # Configuration (create from .env.example)
├── .env.example         # Example configuration template
├── README.md            # This file
└── tests/
    └── test_label_migration.py  # Comprehensive test suite
```

## Development

### Code Quality Standards

- Type hints for all function parameters and return values
- Google-style docstrings for all public functions
- PEP 8 compliance
- Pydantic for all data validation
- loguru for structured logging
- Under 700 lines of code (single file)

### Running Quality Checks

```bash
# Run linting
uv run ruff check main.py

# Run type checking
uv run mypy main.py

# Run tests with coverage
uv run pytest tests/ --cov=main
```

## Technical Details

### Dependencies

- `python-gitlab`: GitLab API client
- `pydantic`: Data validation and settings management
- `python-dotenv`: Environment variable loading
- `loguru`: Structured logging
- `pytest`: Testing framework (dev dependency)

### API Considerations

- Uses GitLab REST API v4
- Supports both GitLab.com and self-hosted instances
- Implements exponential backoff for rate limiting
- Validates hex color codes before API calls
- Handles pagination automatically with `get_all=True`

### Label Color Format

GitLab uses hex color codes in the format `#RRGGBB`:
- Valid: `#FF0000`, `#00FF00`, `#0000FF`
- Invalid: `#FFF` (too short), `red` (not hex), `FFFF00` (missing #)

The utility automatically:
- Adds `#` prefix if missing
- Converts to uppercase for consistency
- Validates format before API calls

## License

This utility is part of the ai-dev-environment project.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitLab API documentation: https://docs.gitlab.com/ee/api/
3. Verify your token permissions and project access

## Version History

- **v1.0.0**: Initial release with core functionality
  - Single-file implementation
  - Pydantic-based validation
  - Comprehensive error handling
  - Full test coverage
