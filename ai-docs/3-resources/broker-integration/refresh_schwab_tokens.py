#!/usr/bin/env python
"""
Schwab Token Refresh Utility

This script automates the process of refreshing Schwab API tokens when they expire.
It directly constructs and opens the authorization URL in a browser, then handles
the token exchange process.

Usage:
    python refresh_schwab_tokens.py
"""
import os
import base64
import urllib.parse
import webbrowser
import requests
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.theme import Theme
from dotenv import load_dotenv

# Custom theme for rich console
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red bold",
    "step": "magenta bold",
    "url": "blue underline",
    "code": "green",
    "highlight": "yellow bold",
})

# Initialize Rich console with custom theme
console = Console(theme=custom_theme)

class SchwabTokenRefresher:
    """Class to handle Schwab API token refresh process"""
    
    def __init__(self):
        """Initialize the token refresher with credentials from .env file"""
        self._load_credentials()
        self._initialize_api_urls()
        console.print("[info]Schwab Token Refresher initialized[/info]")

    def _load_credentials(self) -> None:
        """Load credentials from .env file"""
        # Load from project root directory
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            console.print(f"[error]No .env file found at {env_path}[/error]")
            raise EnvironmentError("No .env file found in project root directory")
            
        load_dotenv(env_path)
        self.app_key = os.getenv('APP_KEY')
        self.app_secret = os.getenv('APP_SECRET')
        self.callback_url = os.getenv('CALLBACK_URL', 'https://127.0.0.1')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        
        if not all([self.app_key, self.app_secret]):
            console.print("[error]Missing required APP_KEY or APP_SECRET in .env file[/error]")
            raise EnvironmentError("Missing required APP_KEY or APP_SECRET in .env file")

    def _initialize_api_urls(self) -> None:
        """Initialize API URLs"""
        self.base_url = "https://api.schwabapi.com"
        self.auth_url = f"{self.base_url}/v1/oauth"

    def _get_encoded_credentials(self) -> str:
        """Get Base64 encoded client credentials"""
        credentials = f"{self.app_key}:{self.app_secret}"
        return base64.b64encode(credentials.encode()).decode('utf-8')

    def _update_env_tokens(self) -> None:
        """Update tokens in .env file"""
        try:
            # Get the project root directory (where .env is located)
            env_path = os.path.join(os.getcwd(), '.env')
            
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('ACCESS_TOKEN='):
                        f.write(f'ACCESS_TOKEN={self.access_token}\n')
                    elif line.startswith('REFRESH_TOKEN='):
                        f.write(f'REFRESH_TOKEN={self.refresh_token}\n')
                    else:
                        f.write(line)
            console.print("[success]Updated tokens in .env file[/success]")
        except Exception as e:
            console.print(f"[error]Failed to update tokens in .env file: {e}[/error]")
            raise

    def extract_and_decode_code(self, url: str) -> str:
        """
        Extracts the authorization code from the provided URL.
        
        Args:
            url (str): The URL containing the authorization code.
        
        Returns:
            str: The decoded authorization code.
        
        Raises:
            ValueError: If the authorization code is not found in the URL.
        """
        console.print("[info]Extracting authorization code from URL...[/info]")
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            encoded_code = query_params['code'][0]
            decoded_code = urllib.parse.unquote(encoded_code)
            console.print("[success]Authorization code extracted and decoded successfully.[/success]")
            return decoded_code
        else:
            console.print("[error]Authorization code not found in the URL.[/error]")
            raise ValueError("Authorization code not found in the URL.")

    def exchange_code_for_tokens(self, auth_code: str) -> tuple:
        """
        Exchanges the authorization code for an access token and a refresh token.
        
        Args:
            auth_code (str): The authorization code to be exchanged.
        
        Returns:
            tuple: A tuple containing the access token and refresh token.
        
        Raises:
            Exception: If the token exchange fails.
        """
        console.print("[info]Exchanging authorization code for access and refresh tokens...[/info]")
        url = f"{self.auth_url}/token"
        encoded_credentials = self._get_encoded_credentials()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.callback_url
        }
        
        try:
            with console.status("[info]Sending token exchange request...[/info]"):
                response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
            
            if response.status_code == 200:
                self.access_token = response_data['access_token']
                self.refresh_token = response_data['refresh_token']
                self._update_env_tokens()
                console.print("[success]Successfully exchanged code for tokens[/success]")
                return self.access_token, self.refresh_token
            else:
                console.print(f"[error]Failed to exchange code for tokens: {response_data}[/error]")
                raise Exception(f"Failed to exchange code for tokens: {response_data}")
                
        except requests.exceptions.RequestException as e:
            console.print(f"[error]Network error during token exchange: {e}[/error]")
            raise

    def launch_auth_server(self) -> str:
        """
        Launch the authorization flow by opening the authorization URL in a browser.
        
        Returns:
            str: The authorization URL that was opened in the browser
        """
        # Construct authorization URL
        auth_url = f"{self.auth_url}/authorize?client_id={self.app_key}&redirect_uri={self.callback_url}"
        
        console.print(Panel.fit(
            Markdown(f"# Opening Authorization URL\n\nYour default web browser will open to the Schwab authorization URL.\n\nURL: `{auth_url}`"),
            title="Browser Opening",
            border_style="blue"
        ))
        
        try:
            # Open URL in default web browser
            webbrowser.open(auth_url)
            console.print("[success]Browser opened successfully with authorization URL[/success]")
        except Exception as e:
            console.print(f"[error]Failed to open browser: {e}[/error]")
            console.print(f"[info]Please manually navigate to: [url]{auth_url}[/url][/info]")
        
        return auth_url

    def guide_user(self) -> None:
        """Guide the user through the authorization process"""
        console.print(Panel.fit(
            Markdown("""# Schwab Authorization Process

## Follow these steps:

1. **Log in** to your Schwab account if prompted
2. **Authorize** the application when prompted
3. **Copy** the entire callback URL from your browser
4. **Paste** it below when prompted

The callback URL should contain a 'code' parameter that will be used to obtain new tokens.
"""),
            title="Authorization Instructions",
            border_style="green"
        ))

    def get_callback_url(self) -> str:
        """Prompt the user to enter the callback URL"""
        while True:
            callback_url = Prompt.ask("[step]Enter the callback URL from your browser[/step]")
            
            # Basic validation
            if "code=" in callback_url:
                return callback_url
            else:
                console.print("[warning]The URL you entered doesn't appear to contain an authorization code.[/warning]")
                retry = Prompt.ask("[step]Would you like to try again?[/step]", choices=["yes", "no"], default="yes")
                if retry.lower() != "yes":
                    raise ValueError("Valid callback URL not provided")

    def refresh_tokens(self) -> None:
        """Main method to refresh tokens"""
        try:
            # Display welcome message
            console.print(Panel.fit(
                "[highlight]Schwab API Token Refresh Utility[/highlight]\n\n"
                "This utility will help you refresh your Schwab API tokens when they expire.",
                title="Welcome",
                border_style="cyan"
            ))
            
            # Launch the authorization flow
            self.launch_auth_server()
            
            # Guide the user
            self.guide_user()
            
            # Get the callback URL
            callback_url = self.get_callback_url()
            
            # Extract the authorization code
            auth_code = self.extract_and_decode_code(callback_url)
            
            # Exchange the code for tokens
            access_token, refresh_token = self.exchange_code_for_tokens(auth_code)
            
            # Display success message
            console.print(Panel.fit(
                "[success]✓ Tokens refreshed successfully![/success]\n\n"
                f"Access Token: {access_token[:10]}...{access_token[-10:]}\n"
                f"Refresh Token: {refresh_token[:10]}...{refresh_token[-10:]}\n\n"
                "The tokens have been updated in your .env file.",
                title="Success",
                border_style="green"
            ))
            
            # Display timestamp
            console.print(f"[info]Tokens refreshed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/info]")
            
        except Exception as e:
            console.print(Panel.fit(
                f"[error]An error occurred during the token refresh process:[/error]\n\n{str(e)}",
                title="Error",
                border_style="red"
            ))
            raise

def main():
    """Main function"""
    try:
        refresher = SchwabTokenRefresher()
        refresher.refresh_tokens()
    except KeyboardInterrupt:
        console.print("\n[warning]Process interrupted by user[/warning]")
    except Exception as e:
        console.print(f"[error]Error: {str(e)}[/error]")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
