# Video Downloader - TikTok / Douyin / Threads / Twitter / Instagram

멀티 플랫폼 비디오 다운로더입니다.  
TikTok, Douyin(抖音), Threads, Twitter/X, Instagram 링크만 붙여 넣으면 고화질 영상과 이미지를 빠르게 저장할 수 있습니다.

**Made by WITHYM**

## Supported Platforms

- TikTok (`https://www.tiktok.com/@user/video/...`)
- Douyin (`https://v.douyin.com/...`)
- Threads (`https://www.threads.net/@user/post/...`)
- Twitter/X (`https://twitter.com/...` 또는 `https://x.com/...`)
- Instagram (`https://www.instagram.com/reel/...`)

YouTube 지원은 제거되었습니다. 대신 Twitter/X와 Instagram 다운로드 기능이 추가되었습니다.

## Key Features

- 완전 무료 사용
- 빠른 다운로드 속도
- 워터마크 제거(가능한 경우)
- 고화질 영상 및 이미지 저장
- 다국어 UI 지원 (한국어, 영어, 일본어, 중국어, 스페인어 등)
- Cloud Run 기반 서버리스 배포 스크립트 포함

## Running Locally

```bash
cd web
pip install -r requirements.txt
python app.py
```

## Deploy to Cloud Run

```bash
gcloud run deploy export-tiktok-douyin-youtube \
  --source . \
  --region=asia-northeast3 \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=900s
```

## Project Structure

```
export-tiktok-douyin-youtube/
├── controller/           # 플랫폼별 다운로드 로직
├── web/                  # Flask 웹 애플리케이션
│   ├── app.py
│   ├── locales/          # 다국어 번역 JSON
│   ├── templates/        # Jinja2 템플릿
│   └── static/           # 정적 자원
└── deploy.sh             # Cloud Run 배포 스크립트
```

## Notes

- 모든 다운로드 기능은 개인 학습용으로만 사용하세요.
- 각 플랫폼의 이용약관과 저작권 정책을 준수해야 합니다.

---

© 2025 WITHYM. All rights reserved.
