import os
import base64
import urllib.parse
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from typing import Tuple

console = Console()

class SchwabAuth:
    def __init__(self):
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path): raise EnvironmentError("No .env file found")
        load_dotenv(env_path)
        self.app_key, self.app_secret, self.access_token, self.refresh_token = [os.getenv(k) for k in ['APP_KEY', 'APP_SECRET', 'ACCESS_TOKEN', 'REFRESH_TOKEN']]
        if not all([self.app_key, self.app_secret, self.access_token, self.refresh_token]): raise EnvironmentError("Missing required environment variables")
        self.auth_url = "https://api.schwabapi.com/v1/oauth"

    def get_encoded_credentials(self) -> str: return base64.b64encode(f"{self.app_key}:{self.app_secret}".encode()).decode('utf-8')

    def update_env_tokens(self) -> None:
        env_path = os.path.join(os.getcwd(), '.env')
        with open(env_path, 'r') as f: lines = f.readlines()
        with open(env_path, 'w') as f:
            for line in lines: f.write(f'ACCESS_TOKEN={self.access_token}\n' if line.startswith('ACCESS_TOKEN=') else f'REFRESH_TOKEN={self.refresh_token}\n' if line.startswith('REFRESH_TOKEN=') else line)

    def refresh_tokens(self) -> Tuple[str, str]:
        response = requests.post(f"{self.auth_url}/token", headers={'Authorization': f'Basic {self.get_encoded_credentials()}', 'Content-Type': 'application/x-www-form-urlencoded'}, data={'grant_type': 'refresh_token', 'refresh_token': self.refresh_token})
        if response.status_code == 200:
            data = response.json()
            self.access_token, self.refresh_token = data['access_token'], data['refresh_token']
            self.update_env_tokens()
            return self.access_token, self.refresh_token
        error = response.json().get('error', '')
        if error in ['unsupported_token_type', 'refresh_token_authentication_error']: return self.get_new_tokens()
        raise Exception(f"Failed to refresh tokens: {response.json()}")

    def extract_and_decode_code(self, url: str) -> str:
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        if 'code' not in query_params: raise ValueError("Authorization code not found in the URL")
        return urllib.parse.unquote(query_params['code'][0])

    def exchange_code_for_tokens(self, auth_code: str) -> Tuple[str, str]:
        response = requests.post(f"{self.auth_url}/token", headers={'Authorization': f'Basic {self.get_encoded_credentials()}', 'Content-Type': 'application/x-www-form-urlencoded'}, data={'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': 'https://127.0.0.1'})
        if response.status_code == 200:
            data = response.json()
            self.access_token, self.refresh_token = data['access_token'], data['refresh_token']
            self.update_env_tokens()
            return self.access_token, self.refresh_token
        raise Exception(f"Failed to exchange code for tokens: {response.json()}")

    def get_new_tokens(self) -> Tuple[str, str]:
        console.print(Panel.fit("[yellow]Authorization Required[/yellow]\n\nPlease follow these steps:\n1. Go to your Schwab developer portal\n2. Generate a new authorization URL\n3. Paste it below"))
        auth_url = console.input("[cyan]Enter the authorization URL: [/cyan]")
        auth_code = self.extract_and_decode_code(auth_url)
        with console.status("[cyan]Exchanging code for tokens...[/cyan]"): access_token, refresh_token = self.exchange_code_for_tokens(auth_code)
        self.access_token, self.refresh_token = access_token, refresh_token
        self.update_env_tokens()
        return access_token, refresh_token

    def get_auth_headers(self) -> dict: return {'Authorization': f'Bearer {self.access_token}', 'Accept': 'application/json'}