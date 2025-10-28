# Multi-stage build for smaller image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY web/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --no-cache-dir --user yt-dlp

# Final production stage
FROM python:3.11-slim

# Install runtime dependencies and Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    procps \
    ffmpeg \
    curl \
    unzip \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver
RUN wget -q https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json -O /tmp/versions.json && \
    CHROMEDRIVER_URL=$(grep -o 'https://[^"]*chromedriver-linux64.zip' /tmp/versions.json | head -1) && \
    if [ -n "$CHROMEDRIVER_URL" ]; then \
        wget -q "$CHROMEDRIVER_URL" -O /tmp/chromedriver.zip && \
        unzip -o /tmp/chromedriver.zip -d /tmp/ && \
        mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
        chmod +x /usr/bin/chromedriver; \
    fi && \
    rm -rf /tmp/chromedriver* /tmp/versions.json

# Set up Chromium to work in containers
ENV CHROME_BIN=/usr/bin/chromium

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY web ./web
COPY controller ./controller
COPY common ./common

# Create necessary directories with proper permissions
RUN mkdir -p /tmp/downloads && \
    chown -R appuser:appuser /app /tmp/downloads

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    FLASK_ENV=production \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/health', timeout=5)" || exit 1

# Run with gunicorn for production
CMD exec gunicorn \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 4 \
    --timeout 300 \
    --worker-class gthread \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --chdir web \
    app:app
