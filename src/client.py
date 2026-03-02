"""
Asana Client - OAuth2 Authentication with Asana REST API
"""

import os
import json
import time
import threading
import webbrowser
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs
from pathlib import Path
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("asana-mcp.client")


class AsanaClient:
    """Client for Asana using REST API with OAuth2 Authentication."""
    
    API_BASE_URL = "https://app.asana.com/api/1.0"
    AUTHORIZATION_URL = "https://app.asana.com/-/oauth_authorize"
    TOKEN_URL = "https://app.asana.com/-/oauth_token"
    
    def __init__(self):
        self.client_id = os.getenv("ASANA_CLIENT_ID", "")
        self.client_secret = os.getenv("ASANA_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("ASANA_REDIRECT_URI", "http://localhost:8338/callback")

        # Allow overriding token cache location via ASANA_TOKEN_PATH; default to project/.token_cache.json
        token_path_env = os.getenv("ASANA_TOKEN_PATH")
        if token_path_env:
            self.token_cache_path = Path(token_path_env).expanduser()
        else:
            self.token_cache_path = Path(__file__).parent.parent / ".token_cache.json"
        
        if not self.client_id:
            raise ValueError(
                "ASANA_CLIENT_ID environment variable is required. "
                "Create an OAuth app at https://app.asana.com/0/my-apps"
            )
        if not self.client_secret:
            raise ValueError(
                "ASANA_CLIENT_SECRET environment variable is required. "
                "Get it from your app at https://app.asana.com/0/my-apps"
            )
        
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[float] = None
        # Cached from /users/me so user doesn't have to pass workspace/user every time
        self._current_user_gid: Optional[str] = None
        self._default_workspace_gid: Optional[str] = None

        # Try to load cached token (and cached user/workspace if present)
        self._load_cached_token()

    def _save_token_cache(self):
        """Save token data and user/workspace context to cache file."""
        token_data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.token_expires_at,
        }
        if self._current_user_gid:
            token_data["current_user_gid"] = self._current_user_gid
        if self._default_workspace_gid:
            token_data["default_workspace_gid"] = self._default_workspace_gid
        try:
            self.token_cache_path.write_text(json.dumps(token_data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save token cache: {e}")

    def _load_cached_token(self) -> bool:
        """Try to load token and user/workspace context from cache file."""
        if not self.token_cache_path.exists():
            return False

        try:
            token_data = json.loads(self.token_cache_path.read_text())
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            self.token_expires_at = token_data.get("expires_at")
            self._current_user_gid = token_data.get("current_user_gid")
            self._default_workspace_gid = token_data.get("default_workspace_gid")

            # Check if token is expired and try to refresh
            if self.access_token and self._is_token_expired():
                if self.refresh_token:
                    logger.info("Token expired, attempting refresh...")
                    return self._refresh_access_token()
                else:
                    logger.info("Token expired and no refresh token available.")
                    self.access_token = None
                    return False

            return self.access_token is not None
        except Exception as e:
            logger.error(f"Failed to load token cache: {e}")
            return False

    def _ensure_user_context(self) -> None:
        """Fetch current user and default workspace from API if not cached."""
        if self._current_user_gid and self._default_workspace_gid:
            return
        if not self.is_authenticated():
            return
        try:
            result = self.get_me()
            data = result.get("data", {})
            if data:
                self._current_user_gid = data.get("gid")
                workspaces = data.get("workspaces") or []
                if workspaces:
                    self._default_workspace_gid = workspaces[0].get("gid")
                self._save_token_cache()
        except Exception as e:
            logger.debug(f"Could not fetch user context: {e}")

    @property
    def current_user_gid(self) -> Optional[str]:
        """Current user GID from session; no need for user to enter it."""
        self._ensure_user_context()
        return self._current_user_gid

    @property
    def default_workspace_gid(self) -> Optional[str]:
        """Default workspace GID (first workspace); no need for user to enter it."""
        self._ensure_user_context()
        return self._default_workspace_gid
    
    def _is_token_expired(self) -> bool:
        """Check if the access token is expired."""
        if not self.token_expires_at:
            return False
        # Add 60-second buffer
        return time.time() >= (self.token_expires_at - 60)
    
    def _refresh_access_token(self) -> bool:
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            return False
        
        try:
            response = requests.post(self.TOKEN_URL, data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token
            })
            
            if response.ok:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token", self.refresh_token)
                expires_in = token_data.get("expires_in", 3600)
                self.token_expires_at = time.time() + expires_in
                self._save_token_cache()
                logger.info("Token refreshed successfully.")
                return True
            else:
                logger.error(f"Token refresh failed: {response.status_code} {response.text}")
                self.access_token = None
                return False
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return False
    
    def _exchange_code_for_token(self, auth_code: str) -> bool:
        """Exchange authorization code for access token."""
        try:
            response = requests.post(self.TOKEN_URL, data={
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "code": auth_code
            })
            
            if response.ok:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                expires_in = token_data.get("expires_in", 3600)
                self.token_expires_at = time.time() + expires_in
                self._save_token_cache()
                return True
            else:
                logger.error(f"Token exchange failed: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"Token exchange error: {e}")
            return False
    
    def authenticate_interactive(self) -> bool:
        """
        Authenticate using OAuth2 authorization code flow.
        Opens browser for user to authorize, then captures the callback.
        """
        print("Starting Asana OAuth2 authentication...")
        
        # Build the authorization URL
        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": "asana_mcp_auth"
        }
        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(auth_params)}"
        
        # Parse redirect URI to get host and port for the callback server
        parsed = urlparse(self.redirect_uri)
        callback_host = parsed.hostname or "localhost"
        callback_port = parsed.port or 8338
        callback_path = parsed.path or "/callback"
        
        # Store for the callback handler
        auth_result = {"code": None, "error": None}
        
        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urlparse(self.path)
                query_params = parse_qs(parsed_path.query)
                
                if "code" in query_params:
                    auth_result["code"] = query_params["code"][0]
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"""
                    <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #6d6e6f;">&#10004; Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    <script>setTimeout(function(){window.close();}, 3000);</script>
                    </body></html>
                    """)
                elif "error" in query_params:
                    auth_result["error"] = query_params.get("error", ["Unknown error"])[0]
                    self.send_response(400)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    error_msg = auth_result["error"]
                    self.wfile.write(f"""
                    <html><body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #e53935;">&#10008; Authentication Failed</h1>
                    <p>Error: {error_msg}</p>
                    <p>Please close this window and try again.</p>
                    </body></html>
                    """.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # Suppress HTTP server logs
                pass
        
        # Start local callback server in a thread
        server = HTTPServer((callback_host, callback_port), CallbackHandler)
        server_thread = threading.Thread(target=server.handle_request, daemon=True)
        server_thread.start()
        
        print()
        print("=" * 60)
        print("ASANA AUTHENTICATION REQUIRED")
        print("=" * 60)
        print()
        print("1. A browser window will open for Asana authorization.")
        print("2. Sign in with your Asana account and click 'Allow'.")
        print("3. You will be redirected back automatically.")
        print()
        print(f"   Authorization URL: {auth_url}")
        print()
        print("=" * 60)
        print("Opening browser...")
        
        # Open the browser
        try:
            webbrowser.open(auth_url)
        except Exception:
            print("\n[WARNING] Could not open browser automatically.")
            print(f"Please open this URL manually:\n{auth_url}")
        
        print("Waiting for authorization (this may take a minute)...")
        
        # Wait for the callback
        server_thread.join(timeout=120)
        server.server_close()
        
        if auth_result["code"]:
            print("\nExchanging authorization code for token...")
            if self._exchange_code_for_token(auth_result["code"]):
                print()
                print("[OK] Authentication successful!")
                return True
            else:
                print("[FAILED] Token exchange failed.")
                return False
        elif auth_result["error"]:
            print(f"\n[FAILED] Authorization error: {auth_result['error']}")
            return False
        else:
            print("\n[FAILED] Authorization timed out. Please try again.")
            return False
    
    def is_authenticated(self) -> bool:
        """Check if client has valid authentication."""
        if not self.access_token:
            return False
        
        # Auto-refresh if expired
        if self._is_token_expired():
            if self.refresh_token:
                return self._refresh_access_token()
            return False
        
        return True
    
    def get_headers(self) -> dict:
        """Get headers for API requests."""
        if not self.access_token:
            raise Exception("Not authenticated. Call authenticate_interactive() first.")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make authenticated request to Asana REST API."""
        url = f"{self.API_BASE_URL}{endpoint}"
        headers = self.get_headers()
        
        # Merge custom headers if provided
        if "headers" in kwargs:
            custom_headers = kwargs.pop("headers")
            if custom_headers:
                headers.update(custom_headers)
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        if response.status_code == 401:
            # Token expired, try to refresh
            if self._refresh_access_token():
                headers = self.get_headers()
                response = requests.request(method, url, headers=headers, **kwargs)
            else:
                raise Exception("Authentication expired. Please re-authenticate.")
        
        if not response.ok:
            error_msg = f"{response.status_code} Error: {response.reason}"
            try:
                error_data = response.json()
                if "errors" in error_data:
                    errors = error_data["errors"]
                    if isinstance(errors, list) and errors:
                        error_msg += f" for url: {url}"
                        for err in errors:
                            if isinstance(err, dict) and "message" in err:
                                error_msg += f"\nError: {err['message']}"
                            if isinstance(err, dict) and "help" in err:
                                error_msg += f"\nHelp: {err['help']}"
                elif "error" in error_data:
                    error_msg += f" for url: {url}\nError: {error_data['error']}"
            except:
                error_msg += f" for url: {url}"
            raise requests.exceptions.HTTPError(error_msg, response=response)
        
        # DELETE often returns empty body
        if response.status_code == 204 or not response.content:
            return {"data": {}}
        
        return response.json()
    
    def get(self, endpoint: str, **kwargs) -> dict:
        """GET request to Asana API."""
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> dict:
        """POST request to Asana API."""
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> dict:
        """PUT request to Asana API."""
        return self.request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> dict:
        """DELETE request to Asana API."""
        return self.request("DELETE", endpoint, **kwargs)
    
    # Basic test method
    def get_me(self) -> dict:
        """Get current user profile."""
        return self.get("/users/me")


# Singleton instance
_client: Optional[AsanaClient] = None


def get_client() -> AsanaClient:
    """Get or create Asana client instance."""
    global _client
    if _client is None:
        _client = AsanaClient()
    return _client
