# Use Python 3.14 as the base image
FROM python:3.14

# Copy the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory in container
WORKDIR /app

# Copy dependency metadata and lock files
COPY pyproject.toml uv.lock .python-version /app/

# Install dependencies using uv (will include pydantic, requests, etc.)
RUN uv sync --locked

# Copy your application and test files
COPY ISS_OEM_J2K_EPH.xml main.py iss_tracker.py test_iss_tracker.py /app/

# Command to run FastAPI app
CMD ["uv", "run", "--", "fastapi", "dev", "--host", "0.0.0.0", "main.py"]
