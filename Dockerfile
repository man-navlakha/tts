# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies (espeak-ng is required for Kokoro TTS)
RUN apt-get update && \
    apt-get install -y espeak-ng curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Railway provides the PORT environment variable dynamically.
# We use 'sh -c' to ensure the environment variable is evaluated.
CMD sh -c "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"
