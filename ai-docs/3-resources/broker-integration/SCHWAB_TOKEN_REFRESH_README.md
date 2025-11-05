# Schwab API Token Refresh Utilities

This document provides information about the utilities created to automate the Schwab API token refresh process.

## Overview

The Schwab API integration requires OAuth tokens that expire periodically. When the refresh token expires, a new authorization URL must be generated from the Schwab developer portal. These utilities streamline this process by:

1. Automatically opening the Schwab developer portal in a browser
2. Guiding the user through generating a new authorization URL
3. Handling the token exchange process
4. Updating the `.env` file with the new tokens

## Components

### 1. `refresh_schwab_tokens.py`

A standalone script that handles the token refresh process. This script can be run directly when you need to refresh your tokens:

```bash
python refresh_schwab_tokens.py
```

The script will:
- Open the Schwab developer portal in your default browser
- Guide you through generating a new authorization URL
- Prompt you to paste the URL
- Extract the authorization code from the URL
- Exchange the code for new access and refresh tokens
- Update your `.env` file with the new tokens

### 2. `auto_refresh_test_schwab.py`

An enhanced version of the original test script that automatically handles token refresh when needed:

```bash
python auto_refresh_test_schwab.py
```

This script:
- Tests the SchwabDataProvider by fetching historical data
- Automatically detects when tokens have expired
- Runs the token refresh utility when needed
- Continues with the test after tokens are refreshed

### 3. `src/utils/schwab_token_manager.py`

A utility module that provides a decorator for automatically refreshing tokens in any function that uses the Schwab API:

```python
from src.utils.schwab_token_manager import with_token_refresh

@with_token_refresh
def my_function_that_uses_schwab_api():
    # Function that uses the Schwab API
    ...
```

The decorator:
- Wraps a function that uses the Schwab API
- Catches token expiration errors
- Runs the token refresh utility when needed
- Retries the original function with the new tokens

## Integration with SchwabDataProvider

The `SchwabDataProvider` class has been updated to use the token refresh decorator on its methods that interact with the Schwab API. This means that any code that uses the `SchwabDataProvider` will automatically benefit from token refresh capabilities without any additional changes.

## Usage Scenarios

### Scenario 1: Manual Token Refresh

If you know your tokens have expired or you want to refresh them proactively:

```bash
python refresh_schwab_tokens.py
```

### Scenario 2: Running Tests with Automatic Token Refresh

To run tests with automatic token refresh:

```bash
python auto_refresh_test_schwab.py
```

### Scenario 3: Using the Token Refresh Decorator in Custom Code

If you're writing custom code that directly uses the Schwab API:

```python
from src.utils.schwab_token_manager import with_token_refresh

@with_token_refresh
def my_custom_function():
    from src.data_providers.schwab import SchwabApi
    
    api = SchwabApi()
    # Use the API...
```

## Schwab Authorization Process

When the token refresh process is initiated, the script will:

1. Directly construct the authorization URL using your APP_KEY and CALLBACK_URL
2. Open this URL in your default web browser
3. Guide you through logging in and authorizing the application
4. Prompt you to copy and paste the callback URL
5. Extract the authorization code from the callback URL
6. Exchange the code for new tokens

## Environment Variables

The script requires the following environment variables in your `.env` file:

```
APP_KEY=your_app_key
APP_SECRET=your_app_secret
CALLBACK_URL=your_callback_url (defaults to https://127.0.0.1 if not provided)
ACCESS_TOKEN=your_current_access_token (will be updated)
REFRESH_TOKEN=your_current_refresh_token (will be updated)
```

## Troubleshooting

If you encounter issues with the token refresh process:

1. **Browser doesn't open**: The script will display the authorization URL that you can manually copy and paste into your browser.

2. **Invalid callback URL**: Make sure you're copying the entire callback URL from your browser after authorization. The URL should contain a `code` parameter.

3. **Token exchange fails**: Check that your APP_KEY and APP_SECRET in the `.env` file are correct.

4. **Script not found**: Make sure you're running the scripts from the project root directory.

## Future Improvements

Potential future improvements for the token refresh utilities:

1. Implement a scheduled token refresh that runs before tokens expire
2. Add support for multiple Schwab API accounts
3. Create a GUI for the token refresh process
4. Add more detailed logging for troubleshooting
