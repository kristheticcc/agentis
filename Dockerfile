# Base image
FROM python:3.12-slim

# Working directory inside container
WORKDIR /app

# Copy uv and uvx binaries
COPY --from=ghcr.io/astral-sh/uv:0.11.16 /uv /uvx /bin/

# Copy dependencies local -> container
COPY pyproject.toml uv.lock ./

# uv sync
RUN uv sync --frozen --no-dev

# Copy all local files to container
COPY . .

# Expose port for cloud run
EXPOSE 8080

# Procuction command (--host 0.0.0.0 for app access from outside container)
CMD ["uv", "run", "uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8080"]




