FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Use public PyPI directly (skip university mirror)
ENV UV_INDEX_URL="https://pypi.org/simple"
ENV UV_INDEX_STRATEGY=unsafe-best-match

# Install dependencies with uv
RUN uv sync --no-dev

# Final stage
FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy the bot code
COPY . .

# Make sure we use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "-m", "bot"]
