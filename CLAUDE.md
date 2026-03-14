# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Overview

This is a Hevy workout tracking MCP (Model Context Protocol) server, built with FastMCP. It runs locally via streamable-HTTP and deploys to Railway via Docker.

## Commands

- **Install deps:** `uv sync`
- **Run server:** `uv run hevy-mcp` (or `./run.sh` which loads `.env` first)
- **Run tests:** `uv run python tests/test_http.py` or `uv run python tests/test_stdio.py`
- **Lint:** `uv run ruff check --fix`
- **Format:** `uv run ruff format`
- **Add package:** `uv add <package>`

## Architecture

- **`hevy_mcp/server.py`** — FastMCP server instance, Pydantic models, tool definitions, health check endpoint, and `main()` entrypoint.
- **`hevy_mcp/utils/auth.py`** — `get_credentials()` returns `{"api_key": ...}` from env vars.
- **`hevy_mcp/utils/hevy.py`** — `HevyClient` async httpx client. Base URL: `https://api.hevyapp.com/v1`. Auth via `api-key` header.
- **`tests/`** — Integration tests that spin up the server and connect via MCP client.

## Key Conventions

- All tools must return type annotations (BaseModel preferred).
- Use `Field(description=...)` for all tool parameters.
- Use `get_credentials()` for any credentials — never hardcode.
- Use `httpx` (not `requests`) for async HTTP calls.
- Ruff line length: 100 chars. Pre-commit runs ruff check + format.

## Setup

Requires `.env` file (copy from `env.example`). Set `ENVIRONMENT=local` for local development.
Only need `HEVY_API_KEY` — get from Hevy app settings (requires Hevy Pro).

## Deployment

Deployed on Railway via Docker. Railway provides `PORT` env var dynamically.
