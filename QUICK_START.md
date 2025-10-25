# 빠른 시작 가이드

## 웹 애플리케이션 실행하기

### 1. 의존성 설치

```bash
# 웹 앱 의존성 설치
pip install -r web/requirements.txt

# YouTube 다운로드용 (필수)
pip install yt-dlp
```

### 2. 웹 서버 실행

```bash
# 기본 포트 (8080)
python web/app.py

# 다른 포트 사용
PORT=8081 python web/app.py
```

### 3. 브라우저에서 접속

```
http://localhost:8080
```

또는 포트를 변경한 경우:
```
http://localhost:8081
```

## 주요 기능

### ✨ 지원 플랫폼
- YouTube (일반 영상 + Shorts)
- TikTok
- Douyin (抖音)
- Threads

### 🌍 20개 언어 지원
한국어, English, 日本語, 简体中文, 繁體中文, Español, Français, Deutsch, Italiano, Português, Русский, العربية, हिन्दी, ไทย, Tiếng Việt, Indonesia, Türkçe, Polski, Nederlands, Svenska

### 🎨 UI 기능
- 다크 모드 토글
- 반응형 디자인
- 언어 선택 드롭다운
- 구글 애드센스 통합 준비

## 테스트된 URL

다음 URL로 테스트가 완료되었습니다:

```
YouTube Shorts: https://www.youtube.com/shorts/HQZ1P0tUXck
YouTube: https://www.youtube.com/watch?v=wgMxQ15PX6U
Threads: https://www.threads.com/@fig080/post/DQGf4IQEomg
Douyin: https://v.douyin.com/V6MEi1KHNh8/
```

## 언어 파일 수정

언어 번역을 수정하려면:

1. `web/locales/` 폴더 열기
2. 원하는 언어 파일 수정 (예: `ko.json`, `en.json`)
3. 서버 재시작

## 구글 애드센스 설정

`web/templates/index.html` 파일에서:

```html
<!-- 본인의 애드센스 ID로 교체 -->
data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
data-ad-slot="XXXXXXXXXX"
```

## API 엔드포인트

### 다운로드
```bash
POST /api/download
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=..."
}
```

### 언어 변경
```bash
POST /api/set-language
Content-Type: application/json

{
  "lang": "ko"
}
```

### 언어 목록
```bash
GET /api/languages
```

### 번역 가져오기
```bash
GET /api/translations/ko
```

## 문제 해결

### 포트가 이미 사용 중
```bash
PORT=8081 python web/app.py
```

### yt-dlp 없음
```bash
pip install yt-dlp
```

### Flask 없음
```bash
pip install -r web/requirements.txt
```

## 더 많은 정보

- [웹 앱 가이드 (한국어)](WEB_APP_GUIDE_KO.md)
- [Web App Guide (English)](WEB_APP_GUIDE_EN.md)
- [배포 가이드](DEPLOYMENT.md)

---

Made by WITHYM
