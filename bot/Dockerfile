FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY bot/pyproject.toml bot/uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy bot code
COPY bot/ .

# Run bot
CMD ["uv", "run", "bot.py"]
