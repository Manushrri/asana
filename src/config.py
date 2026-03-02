"""
Configuration settings for Asana MCP Server
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env from project root (parent of src/) so vars are set even when CWD is different
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")


@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    
    # Asana OAuth2 settings
    client_id: str = os.getenv("ASANA_CLIENT_ID", "")
    client_secret: str = os.getenv("ASANA_CLIENT_SECRET", "")
    redirect_uri: str = os.getenv("ASANA_REDIRECT_URI", "http://localhost:8338/callback")
    
    # Asana REST API settings
    api_base_url: str = os.getenv("ASANA_API_BASE_URL", "https://app.asana.com/api/1.0")
    
    # Asana OAuth2 endpoints
    authorization_url: str = "https://app.asana.com/-/oauth_authorize"
    token_url: str = "https://app.asana.com/-/oauth_token"
    
    # Scopes (Asana uses 'default' for full access)
    scopes: str = os.getenv("ASANA_SCOPES", "default")

    # Workspace path for secure file access (attachments). Optional; when set,
    # CREATE_ATTACHMENT_FOR_TASK can accept a workspace-relative file path.
    workspace_path: Optional[str] = os.getenv("WORKSPACE_PATH")


# Singleton settings instance
settings = Settings()
