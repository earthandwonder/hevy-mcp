# Hevy MCP

An MCP (Model Context Protocol) server for [Hevy](https://hevy.com) — the workout tracking app. Connects any MCP-compatible AI client (Claude, Cursor, etc.) to your Hevy account, letting it read your workouts, routines, and exercises, or log new ones on your behalf.

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk) and async [httpx](https://www.python-httpx.org/).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Hevy Pro subscription (for API access)
- Hevy API key (Settings > API in the Hevy app)

## Setup

```bash
# Clone and install
git clone https://github.com/zachsai/hevy-mcp.git
cd hevy-mcp
uv sync

# Configure
cp env.example .env
# Edit .env and add your HEVY_API_KEY

# Run locally
./run.sh
```

The server starts on `http://localhost:8000` with streamable-HTTP transport.

## Tools

### Read
| Tool | Description |
|------|-------------|
| `get_workout_count` | Total number of logged workouts |
| `list_workouts` | List workouts with pagination |
| `get_workout` | Full workout details (exercises, sets, weights) |
| `list_routines` | List saved routines |
| `get_routine` | Full routine details |
| `search_exercises` | Search exercise templates by name |

### Write
| Tool | Description |
|------|-------------|
| `create_workout` | Log a new workout |
| `update_workout` | Update an existing workout |
| `create_routine` | Create a new routine |
| `update_routine` | Update an existing routine |

## Architecture

```
hevy_mcp/
├── server.py           # FastMCP server, Pydantic models, tool definitions
└── utils/
    ├── auth.py         # API key from environment
    └── hevy.py         # Async HTTP client for Hevy API v1
```

- **Auth:** Static API key via `api-key` header (no OAuth complexity)
- **HTTP client:** async httpx with pagination support
- **Models:** Pydantic BaseModel for all tool inputs/outputs

## Deployment

### Docker (any platform)

Includes a `Dockerfile` for container deployment. The server reads `PORT` from the environment and exposes a `/health_check` endpoint.

```bash
docker build -t hevy-mcp .
docker run -e HEVY_API_KEY=your_key -e PORT=8080 hevy-mcp
```

### Railway

This project is set up for one-click deployment on [Railway](https://railway.com). See [`RAILWAY_DEPLOY.md`](RAILWAY_DEPLOY.md) for the full step-by-step playbook covering:

1. Creating the Railway project
2. Deploying the Docker container
3. Setting environment variables (`HEVY_API_KEY`, `ENVIRONMENT`)
4. Generating a public domain
5. Verifying the deployment (health check + MCP handshake)

The playbook documents the exact Railway MCP tool calls and parameters, so it can be followed manually or used as a reference for building an automated deployment skill with the [Railway MCP server](https://docs.railway.com/guides/mcp).

## Development

```bash
uv run ruff check --fix   # Lint
uv run ruff format         # Format
uv run python tests/test_http.py   # Integration test (HTTP)
uv run python tests/test_stdio.py  # Integration test (stdio)
```
