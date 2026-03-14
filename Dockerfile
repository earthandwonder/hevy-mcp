# Dockerfile for Hevy MCP
# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv sync

# Copy application code
COPY . .

# Railway sets PORT dynamically
EXPOSE ${PORT:-8080}

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Health check endpoint
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8080}/health_check || exit 1

# Run the MCP server
CMD ["uv", "run", "hevy-mcp"]
