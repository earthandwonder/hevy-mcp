"""Authentication utilities for Hevy MCP."""

import os


def get_credentials() -> dict[str, str]:
    """Get Hevy credentials from environment variables."""
    return {
        "api_key": os.environ.get("HEVY_API_KEY", ""),
    }
