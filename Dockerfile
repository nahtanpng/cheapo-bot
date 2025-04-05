# Use official Python runtime as base image
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Remove unnecessary files
RUN find . -type d -name '__pycache__' -exec rm -rf {} + && \
    find . -type f -name '*.pyc' -delete

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m botuser && \
    chown -R botuser:botuser /app
USER botuser

# Copy application files
COPY --chown=botuser:botuser . .

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    BOT_ENV=production


# Run the bot
CMD ["python", "-m", "main.py"]