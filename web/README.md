#
 Video Downloader Web Application

Flask 기반의 다국어 비디오 다운로드 웹 서비스입니다.  
TikTok, Douyin(抖音), Threads, Twitter/X, Instagram 링크를 감지하여 서버 측에서 파일을 생성한 뒤 바로 내려받을 수 있게 합니다.

## ✅ Features

- **Multi-Platform Support**  
  - TikTok (동영상, 이미지)  
  - Douyin (抖音)  
  - Threads  
  - Twitter/X  
  - Instagram (Reels 포함)
- **Modern Web Interface**  
  - 반응형 UI  
  - 실시간 상태 메시지  
  - 다크 모드 & 다국어 전환
- **Cloud Ready**  
  - Docker 기반 빌드  
  - Google Cloud Run 배포 스크립트  
  - 헬스체크 및 로깅 지원

## 🚀 Quick Start

### Local Development

```bash
cd web
pip install -r requirements.txt
python app.py
```

브라우저에서 `http://localhost:8080` 접속

### Docker

```bash
docker-compose up --build
```

### Google Cloud Run

```bash
gcloud run deploy export-tiktok-douyin-youtube \
  --source . \
  --region=asia-northeast1 \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=900s
```

## 🔌 API Endpoints

### `GET /`
메인 웹 UI

### `POST /api/download`
플랫폼을 자동 감지하고 다운로드를 트리거합니다.

**Request**
```json
{
  "url": "https://www.instagram.com/reel/..."
}
```

**Response**
```json
{
  "success": true,
  "platform": "instagram",
  "filename": "video.mp4",
  "size": 12345678,
  "download_id": "uuid",
  "download_url": "/api/file/uuid/video.mp4"
}
```

### `GET /api/file/<download_id>/<filename>`
생성된 파일 다운로드

### `GET /api/platforms`
지원 플랫폼 목록 반환

```json
{
  "platforms": [
    {"id": "tiktok", "name": "TikTok"},
    {"id": "threads", "name": "Threads"},
    {"id": "twitter", "name": "Twitter/X"},
    {"id": "instagram", "name": "Instagram"}
  ]
}
```

### `GET /api/health`
헬스 체크

## 🛠️ Tech Stack

- Flask 3.x
- Requests, httpx
- Selenium (Threads 지원용)
- yt-dlp (백업 다운로드 로직)
- Google Cloud Run / Cloud Build

## 📁 Directory Overview

```
web/
├── app.py               # Flask 엔트리포인트
├── templates/           # Jinja2 템플릿
├── static/              # 정적 자원
├── locales/             # 다국어 JSON
└── config/              # 광고/애널리틱스 설정
```

## ⚙️ Configuration

환경 변수:
- `PORT` (기본: 8080)
- `SECRET_KEY`
- `GOOGLE_APPLICATION_CREDENTIALS` (필요 시)

## 🧪 Testing

`test_new_platforms.py`는 Threads/Twitter/Instagram을 포함한 통합 다운로드 테스트를 수행합니다.

```bash
python test_new_platforms.py
```

## 📄 License

Made by WITHYM.  
비상업적/개인 학습용도로만 사용하세요.
