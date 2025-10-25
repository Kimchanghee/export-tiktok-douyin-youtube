# Video Downloader Web Application

A Flask-based web application for downloading videos from multiple platforms.

## 🌟 Features

- ✅ **Multi-Platform Support**
  - YouTube (regular videos + Shorts)
  - TikTok
  - Douyin
  - Threads

- ✅ **Modern Web Interface**
  - Responsive design
  - Real-time download status
  - One-click download

- ✅ **Cloud-Ready**
  - Docker support
  - Google Cloud Run compatible
  - Auto-scaling
  - Health checks

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r web/requirements.txt

# Run server
python web/app.py
```

Access at: http://localhost:8080

### Docker

```bash
# Build and run
docker-compose up --build
```

### Google Cloud Run

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

## 📡 API Endpoints

### GET `/`
Main web interface

### POST `/api/download`
Download video

**Request:**
```json
{
  "url": "https://youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "success": true,
  "platform": "youtube",
  "filename": "video.mp4",
  "size": 12345678,
  "download_id": "uuid",
  "download_url": "/api/file/uuid/video.mp4"
}
```

### GET `/api/file/<download_id>/<filename>`
Download file

### GET `/api/health`
Health check

**Response:**
```json
{
  "status": "healthy",
  "service": "video-downloader"
}
```

### GET `/api/platforms`
List supported platforms

**Response:**
```json
{
  "platforms": [
    {"id": "youtube", "name": "YouTube", "types": ["videos", "shorts"]},
    ...
  ]
}
```

## 🏗️ Architecture

```
web/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Web interface
├── requirements.txt    # Python dependencies
└── README.md          # This file

controller/             # Download logic (shared)
├── ThreadsExtract.py
├── DouyinExtract.py
└── ...

common/                # Common utilities (shared)
```

## 🔧 Configuration

Environment variables:

- `PORT`: Server port (default: 8080)
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Flask secret key (required in production)

## 📦 Dependencies

- Flask 3.1+
- Selenium 4.0+ (for Threads)
- yt-dlp (for YouTube)
- requests (for HTTP)
- gunicorn (production server)

## 🐛 Troubleshooting

### yt-dlp not found
```bash
pip install yt-dlp
```

### Chrome/Chromium not found (Threads)
```bash
# Install Chrome
sudo apt-get install chromium chromium-driver
```

### Port already in use
```bash
# Change port
export PORT=8081
python web/app.py
```

## 📝 License

Made by WITHYM

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.
