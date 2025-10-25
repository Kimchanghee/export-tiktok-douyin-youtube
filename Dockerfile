# Use Python 3.12 (more stable with dependencies)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    chromium \
    chromium-driver \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better caching
COPY web/requirements.txt /app/web/requirements.txt
RUN pip install --no-cache-dir -r /app/web/requirements.txt

# Install yt-dlp
RUN pip install --no-cache-dir yt-dlp

# Copy application code
COPY web/ /app/web/
COPY controller/ /app/controller/
COPY common/ /app/common/

# Create downloads directory
RUN mkdir -p /tmp/downloads

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=/app/web/app.py
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["python", "/app/web/app.py"]
