# Use a stable Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory and set permissions
RUN mkdir -p uploads && chmod 777 uploads

# Expose the port Flask/Gunicorn will run on
EXPOSE 7860

# Command to run the application
# Note: Hugging Face uses port 7860 by default
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]
