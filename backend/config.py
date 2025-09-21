"""
Configuration management for the Daily Wellness Tracker application.
"""

import json
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def get_env_str(var_name: str, description: str = "") -> str:
    """Get a required string environment variable."""
    value = os.getenv(var_name)
    if not value:
        desc_text = f" ({description})" if description else ""
        raise ValueError(f"{var_name} environment variable is required{desc_text}")
    return value


def get_env_int(var_name: str, description: str = "") -> int:
    """Get a required integer environment variable."""
    value = os.getenv(var_name)
    if not value:
        desc_text = f" ({description})" if description else ""
        raise ValueError(f"{var_name} environment variable is required{desc_text}")

    try:
        return int(value)
    except ValueError as err:
        raise ValueError(f"{var_name} must be a valid integer") from err


def get_env_bool(var_name: str, description: str = "") -> bool:
    """Get a required boolean environment variable."""
    value = os.getenv(var_name)
    if not value:
        desc_text = f" ({description})" if description else ""
        raise ValueError(f"{var_name} environment variable is required{desc_text}")
    return value.lower() == "true"


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        """Initializes the settings object by loading environment variables."""

        self.database_url = get_env_str("DATABASE_URL", "database connection string")
        self.host = get_env_str("HOST", "server host address")
        self.port = get_env_int("PORT", "server port number")
        self.debug = get_env_bool("DEBUG", "debug mode (true/false)")

        cors_origins_str = get_env_str("CORS_ORIGINS", "allowed frontend origins")
        try:
            # Try parsing as JSON array first, fall back to comma-separated string
            self.cors_origins = json.loads(cors_origins_str)
        except (json.JSONDecodeError, TypeError, ValueError):
            self.cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

        self.secret_key = get_env_str("SECRET_KEY", "application secret key")
        self.default_user_id = get_env_str("DEFAULT_USER_ID", "default user identifier")
        self.gemini_api_key = get_env_str("GEMINI_API_KEY", "Google Gemini API key")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the application settings instance (cached singleton)."""
    return Settings()
