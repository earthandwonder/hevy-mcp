#!/usr/bin/env python3
"""Test the MCP server using stdio transport."""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PACKAGE_NAME = "hevy_mcp"


def get_project_root() -> Path:
    """Find project root by looking for pyproject.toml."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find project root (no pyproject.toml found)")


def load_env():
    """Load .env from project root, raise if not found."""
    root = get_project_root()
    env_file = root / ".env"
    if not env_file.exists():
        raise FileNotFoundError(
            f".env file not found at {env_file}\nCopy env.example to .env and fill in your API key."
        )
    load_dotenv(env_file)
    return root


async def test_stdio():
    """Connect to the server via stdio and test its tools."""
    root = load_env()

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", f"{PACKAGE_NAME}.server", "--transport", "stdio"],
        env={
            **os.environ,
            "PYTHONPATH": str(root),
            "ENVIRONMENT": "local",
        },
    )

    print("Connecting to server via stdio...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected and initialized\n")

            tools_response = await session.list_tools()
            print("Available tools:")
            for tool in tools_response.tools:
                print(f"   - {tool.name}: {tool.description}")
            print()

            print("Testing get_workout_count...")
            result = await session.call_tool("get_workout_count", {})
            print(f"   Result: {result.content}")
            print()

            print("All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_stdio())
