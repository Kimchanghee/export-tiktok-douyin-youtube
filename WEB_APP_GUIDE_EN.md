# Video Downloader Web Application

A multilingual web application for downloading videos from TikTok, Douyin, YouTube, and Threads.

Made by WITHYM

## 🌟 Key Features

### ✨ Multilingual Support (20 Languages)
- 🇰🇷 한국어 (Korean)
- 🇺🇸 English
- 🇯🇵 日本語 (Japanese)
- 🇨🇳 简体中文 (Simplified Chinese)
- 🇹🇼 繁體中文 (Traditional Chinese)
- 🇪🇸 Español (Spanish)
- 🇫🇷 Français (French)
- 🇩🇪 Deutsch (German)
- 🇮🇹 Italiano (Italian)
- 🇵🇹 Português (Portuguese)
- 🇷🇺 Русский (Russian)
- 🇸🇦 العربية (Arabic)
- 🇮🇳 हिन्दी (Hindi)
- 🇹🇭 ไทย (Thai)
- 🇻🇳 Tiếng Việt (Vietnamese)
- 🇮🇩 Indonesia (Indonesian)
- 🇹🇷 Türkçe (Turkish)
- 🇵🇱 Polski (Polish)
- 🇳🇱 Nederlands (Dutch)
- 🇸🇪 Svenska (Swedish)

### 📹 Supported Platforms
- **YouTube** (Regular videos + Shorts)
- **TikTok**
- **Douyin** (抖音)
- **Threads**

### 🎨 Modern UI/UX
- **Responsive Design** - Perfect support for mobile/tablet/desktop
- **Dark Mode** - Eye-friendly dark theme
- **Smooth Animations** - Enhanced user experience
- **Intuitive Interface** - Easy to use for everyone

### 💰 Monetization Features
- **Google AdSense Integration** - Generate ad revenue
- Customizable ad placement

### 🔒 Security
- **No Access Password** - Free access
- **Safe Downloads** - No malware
- **Privacy Protection** - No user data storage

## 🚀 Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r web/requirements.txt

# 2. Run server
python web/app.py
```

Access in browser: `http://localhost:8080`

### Run with Docker

```bash
# Build and run Docker container
docker-compose up --build
```

Access in browser: `http://localhost:8080`

## 📁 Project Structure

```
tiktok-douyin-youtube-web-version/
├── web/                          # Web application
│   ├── app.py                    # Flask main application
│   ├── templates/
│   │   └── index.html            # Main page (i18n/dark mode)
│   ├── locales/                  # Language files folder
│   │   ├── ko.json              # Korean
│   │   ├── en.json              # English
│   │   ├── ja.json              # Japanese
│   │   ├── zh-CN.json           # Simplified Chinese
│   │   ├── zh-TW.json           # Traditional Chinese
│   │   ├── es.json              # Spanish
│   │   ├── fr.json              # French
│   │   ├── de.json              # German
│   │   ├── it.json              # Italian
│   │   ├── pt.json              # Portuguese
│   │   ├── ru.json              # Russian
│   │   ├── ar.json              # Arabic
│   │   ├── hi.json              # Hindi
│   │   ├── th.json              # Thai
│   │   ├── vi.json              # Vietnamese
│   │   ├── id.json              # Indonesian
│   │   ├── tr.json              # Turkish
│   │   ├── pl.json              # Polish
│   │   ├── nl.json              # Dutch
│   │   └── sv.json              # Swedish
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # Web app documentation
├── controller/                  # Download logic
│   ├── DouyinExtract.py        # TikTok/Douyin downloader
│   ├── ThreadsExtract.py       # Threads downloader
│   └── VideoExtract.py         # Video extraction utils
├── common/                      # Common utilities
│   ├── DriverConfig.py
│   └── Tool.py
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # Main project documentation
```

## 🌐 Language File Management

Language files are individually managed in the `web/locales/` folder.

### Editing Language Files

1. Navigate to `web/locales/` folder
2. Open the language file you want to edit (e.g., `en.json`)
3. Edit translations in JSON format:

```json
{
  "title": "Video Downloader",
  "subtitle": "TikTok · Douyin · YouTube · Threads",
  "download_button": "Download",
  ...
}
```

4. Save file and restart server

### Adding a New Language

1. Create a new language file in `web/locales/` (e.g., copy `en.json`)
2. Add the new language to `SUPPORTED_LANGUAGES` list in `web/app.py`:

```python
SUPPORTED_LANGUAGES = [
    # ... existing languages
    {'code': 'new-lang', 'name': 'Language Name', 'flag': '🏳️'},
]
```

3. Restart server

## 💰 Google AdSense Setup

### 1. Create AdSense Account
1. Sign up at [Google AdSense](https://www.google.com/adsense/)
2. Register your website and wait for approval

### 2. Insert Ad Code
Edit `web/templates/index.html`:

```html
<!-- Replace 'ca-pub-XXXXXXXXXXXXXXXX' with your AdSense ID -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

### 3. Set Ad Slot IDs
```html
<!-- Replace data-ad-slot value with your ad slot ID -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

## 🔧 Environment Variables

Create `.env` file (optional):

```env
# Flask settings
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# Port settings (default: 8080)
PORT=8080

# Google AdSense
ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
```

## 📡 API Endpoints

### GET `/`
Main web page

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

### POST `/api/set-language`
Set language preference

**Request:**
```json
{
  "lang": "en"
}
```

### GET `/api/translations/<lang_code>`
Get translations for a specific language

### GET `/api/languages`
List of supported languages

### GET `/api/platforms`
List of supported platforms

### GET `/api/health`
Server health check

## 🐛 Troubleshooting

### yt-dlp Installation Error
```bash
pip install --upgrade yt-dlp
```

### Chrome/Chromium Not Found (Threads download)
```bash
# Windows
choco install googlechrome

# Ubuntu/Debian
sudo apt-get install chromium-browser chromium-chromedriver

# macOS
brew install --cask google-chrome
```

### Port Conflict
```bash
# Change to a different port
export PORT=8081
python web/app.py
```

## 🌍 Deployment

### Google Cloud Run
See [DEPLOYMENT.md](DEPLOYMENT.md)

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### AWS / Azure
Docker image recommended

## 📝 License

Made by WITHYM

Provided for personal use and educational purposes.

## ⚠️ Disclaimer

- Use for personal purposes only
- Respect copyright laws
- Check platform terms of service for commercial use
- Redistribution of downloaded content may infringe on creator rights

## 🤝 Contributing

Bug reports, feature requests, and Pull Requests are welcome!

---

© 2024 WITHYM. All rights reserved.
