# 비디오 다운로더 웹 애플리케이션

TikTok, Douyin, YouTube, Threads에서 비디오를 다운로드할 수 있는 다국어 지원 웹 애플리케이션입니다.

Made by WITHYM

## 🌟 주요 기능

### ✨ 다국어 지원 (20개 언어)
- 🇰🇷 한국어
- 🇺🇸 English
- 🇯🇵 日本語
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇮🇹 Italiano
- 🇵🇹 Português
- 🇷🇺 Русский
- 🇸🇦 العربية
- 🇮🇳 हिन्दी
- 🇹🇭 ไทย
- 🇻🇳 Tiếng Việt
- 🇮🇩 Indonesia
- 🇹🇷 Türkçe
- 🇵🇱 Polski
- 🇳🇱 Nederlands
- 🇸🇪 Svenska

### 📹 지원 플랫폼
- **YouTube** (일반 영상 + Shorts)
- **TikTok**
- **Douyin** (抖音)
- **Threads**

### 🎨 모던한 UI/UX
- **반응형 디자인** - 모바일/태블릿/데스크톱 완벽 지원
- **다크 모드** - 눈의 피로를 줄이는 다크 테마
- **애니메이션 효과** - 부드러운 사용자 경험
- **직관적인 인터페이스** - 누구나 쉽게 사용 가능

### 💰 수익화 기능
- **구글 애드센스 통합** - 광고 수익 창출 가능
- 광고 위치 커스터마이즈 가능

### 🔒 보안
- **접속 암호 제거** - 자유로운 접근
- **안전한 다운로드** - 악성코드 없음
- **개인정보 보호** - 사용자 데이터 저장 안 함

## 🚀 빠른 시작

### 로컬 개발 환경

```bash
# 1. 의존성 설치
pip install -r web/requirements.txt

# 2. 서버 실행
python web/app.py
```

브라우저에서 접속: `http://localhost:8080`

### Docker로 실행

```bash
# Docker 컨테이너 빌드 및 실행
docker-compose up --build
```

브라우저에서 접속: `http://localhost:8080`

## 📁 프로젝트 구조

```
tiktok-douyin-youtube-web-version/
├── web/                          # 웹 애플리케이션
│   ├── app.py                    # Flask 메인 애플리케이션
│   ├── templates/
│   │   └── index.html            # 메인 페이지 (다국어/다크모드 지원)
│   ├── locales/                  # 언어 파일 폴더
│   │   ├── ko.json              # 한국어
│   │   ├── en.json              # 영어
│   │   ├── ja.json              # 일본어
│   │   ├── zh-CN.json           # 중국어 간체
│   │   ├── zh-TW.json           # 중국어 번체
│   │   ├── es.json              # 스페인어
│   │   ├── fr.json              # 프랑스어
│   │   ├── de.json              # 독일어
│   │   ├── it.json              # 이탈리아어
│   │   ├── pt.json              # 포르투갈어
│   │   ├── ru.json              # 러시아어
│   │   ├── ar.json              # 아랍어
│   │   ├── hi.json              # 힌디어
│   │   ├── th.json              # 태국어
│   │   ├── vi.json              # 베트남어
│   │   ├── id.json              # 인도네시아어
│   │   ├── tr.json              # 터키어
│   │   ├── pl.json              # 폴란드어
│   │   ├── nl.json              # 네덜란드어
│   │   └── sv.json              # 스웨덴어
│   ├── requirements.txt         # Python 의존성
│   └── README.md               # 웹 앱 문서
├── controller/                  # 다운로드 로직
│   ├── DouyinExtract.py        # TikTok/Douyin 다운로더
│   ├── ThreadsExtract.py       # Threads 다운로더
│   └── VideoExtract.py         # 비디오 추출 유틸
├── common/                      # 공통 유틸리티
│   ├── DriverConfig.py
│   └── Tool.py
├── Dockerfile                   # Docker 설정
├── docker-compose.yml          # Docker Compose 설정
└── README.md                   # 프로젝트 메인 문서
```

## 🌐 언어 파일 관리

언어 파일은 `web/locales/` 폴더에서 개별적으로 관리됩니다.

### 언어 파일 수정하기

1. `web/locales/` 폴더로 이동
2. 수정하고 싶은 언어 파일 열기 (예: `ko.json`)
3. JSON 형식으로 번역 수정:

```json
{
  "title": "Video Downloader",
  "subtitle": "TikTok · Douyin · YouTube · Threads",
  "download_button": "다운로드",
  ...
}
```

4. 파일 저장 후 서버 재시작

### 새로운 언어 추가하기

1. `web/locales/` 폴더에 새 언어 파일 생성 (예: `ko.json` 복사)
2. `web/app.py`의 `SUPPORTED_LANGUAGES` 리스트에 새 언어 추가:

```python
SUPPORTED_LANGUAGES = [
    # ... 기존 언어들
    {'code': 'new-lang', 'name': '언어이름', 'flag': '🏳️'},
]
```

3. 서버 재시작

## 💰 구글 애드센스 설정

### 1. 애드센스 계정 생성
1. [Google AdSense](https://www.google.com/adsense/) 가입
2. 웹사이트 등록 및 승인 대기

### 2. 광고 코드 삽입
`web/templates/index.html` 파일 수정:

```html
<!-- 'ca-pub-XXXXXXXXXXXXXXXX' 부분을 본인의 애드센스 ID로 교체 -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

### 3. 광고 슬롯 ID 설정
```html
<!-- data-ad-slot 값을 본인의 광고 슬롯 ID로 교체 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

## 🔧 환경 변수 설정

`.env` 파일 생성 (선택사항):

```env
# Flask 설정
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# 포트 설정 (기본값: 8080)
PORT=8080

# 구글 애드센스
ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
```

## 📡 API 엔드포인트

### GET `/`
메인 웹 페이지

### POST `/api/download`
비디오 다운로드

**요청:**
```json
{
  "url": "https://youtube.com/watch?v=..."
}
```

**응답:**
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
파일 다운로드

### POST `/api/set-language`
언어 설정

**요청:**
```json
{
  "lang": "ko"
}
```

### GET `/api/translations/<lang_code>`
특정 언어의 번역 가져오기

### GET `/api/languages`
지원하는 언어 목록

### GET `/api/platforms`
지원하는 플랫폼 목록

### GET `/api/health`
서버 상태 확인

## 🐛 문제 해결

### yt-dlp 설치 오류
```bash
pip install --upgrade yt-dlp
```

### Chrome/Chromium 없음 (Threads 다운로드)
```bash
# Windows
choco install googlechrome

# Ubuntu/Debian
sudo apt-get install chromium-browser chromium-chromedriver

# macOS
brew install --cask google-chrome
```

### 포트 충돌
```bash
# 다른 포트로 변경
export PORT=8081
python web/app.py
```

## 🌍 배포

### Google Cloud Run
[DEPLOYMENT.md](DEPLOYMENT.md) 참조

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### AWS / Azure
Docker 이미지 사용 권장

## 📝 라이선스

Made by WITHYM

개인 사용 및 학습 목적으로 제공됩니다.

## ⚠️ 주의사항

- 개인적 용도로만 사용하세요
- 저작권법을 준수하세요
- 상업적 용도로 사용 시 플랫폼의 이용약관을 확인하세요
- 다운로드한 콘텐츠의 재배포는 원작자의 권리를 침해할 수 있습니다

## 🤝 기여하기

버그 리포트, 기능 제안, Pull Request 환영합니다!

---

© 2024 WITHYM. All rights reserved.
