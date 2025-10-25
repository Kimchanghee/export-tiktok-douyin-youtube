# 🌐 Video Downloader - Web Application Guide

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [로컬 실행](#로컬-실행)
3. [Docker 실행](#docker-실행)
4. [Google Cloud Run 배포](#google-cloud-run-배포)
5. [API 사용법](#api-사용법)
6. [문제 해결](#문제-해결)

---

## 🎯 프로젝트 개요

### 지원 플랫폼
- ✅ YouTube (일반 영상 + Shorts)
- ✅ TikTok
- ✅ Douyin
- ✅ Threads

### 기술 스택
- **Backend**: Flask (Python 3.12)
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Download**: yt-dlp, Selenium, Requests
- **Container**: Docker
- **Cloud**: Google Cloud Run

### 파일 구조
```
export-tiktok-douyin-youtube/
│
├── web/                        # 웹 애플리케이션
│   ├── app.py                 # Flask 서버
│   ├── templates/
│   │   └── index.html         # 웹 인터페이스
│   ├── requirements.txt       # Python 패키지
│   └── README.md
│
├── controller/                 # 다운로드 로직 (공유)
│   ├── ThreadsExtract.py
│   ├── DouyinExtract.py
│   └── ...
│
├── common/                     # 공통 유틸리티 (공유)
│
├── Dockerfile                  # Docker 이미지 정의
├── docker-compose.yml         # Docker Compose 설정
├── .dockerignore              # Docker 빌드 제외 파일
├── .gcloudignore              # GCP 배포 제외 파일
├── DEPLOYMENT.md              # 배포 가이드
└── WEB_APP_GUIDE.md          # 이 파일
```

---

## 🏠 로컬 실행

### 방법 1: Python 직접 실행

```bash
# 1. 의존성 설치
cd export-tiktok-douyin-youtube
pip install -r web/requirements.txt
pip install yt-dlp  # YouTube 다운로드용

# 2. 서버 실행
python web/app.py

# 3. 브라우저에서 접속
# http://localhost:8080
```

### 방법 2: 개발 모드 실행

```bash
# 개발 모드 (자동 리로드)
export FLASK_ENV=development
export PORT=8080
python web/app.py
```

---

## 🐳 Docker 실행

### 빠른 시작

```bash
# Docker Compose로 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build

# 접속
# http://localhost:8080

# 종료
docker-compose down
```

### Docker 명령어로 실행

```bash
# 1. 이미지 빌드
docker build -t video-downloader .

# 2. 컨테이너 실행
docker run -p 8080:8080 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  video-downloader

# 3. 접속
# http://localhost:8080

# 4. 종료
docker stop <container_id>
```

---

## ☁️ Google Cloud Run 배포

### 사전 준비

1. **Google Cloud 계정 생성**
   - https://cloud.google.com
   - 청구 계정 활성화

2. **Google Cloud SDK 설치**
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Windows
   # https://cloud.google.com/sdk/docs/install 에서 다운로드

   # Linux
   curl https://sdk.cloud.google.com | bash
   ```

3. **로그인 및 프로젝트 설정**
   ```bash
   gcloud init
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

### 배포 단계

#### 1단계: API 활성화

```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### 2단계: 프로젝트 ID 설정

```bash
export PROJECT_ID="your-project-id"
export SERVICE_NAME="video-downloader"
export REGION="us-central1"
```

#### 3단계: 빌드 및 배포

```bash
# Cloud에서 빌드 및 배포 (한 번에)
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars "FLASK_ENV=production"
```

또는 분리하여:

```bash
# 1. 빌드
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 2. 배포
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

#### 4단계: URL 확인

```bash
gcloud run services describe $SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)'
```

배포 완료! URL: `https://video-downloader-xxxxx-uc.a.run.app`

### 배포 후 확인

```bash
# Health check
curl https://your-service-url/api/health

# 응답:
# {"status":"healthy","service":"video-downloader"}
```

---

## 📡 API 사용법

### 1. 비디오 다운로드

```bash
curl -X POST https://your-url/api/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=..."}'
```

**응답:**
```json
{
  "success": true,
  "platform": "youtube",
  "filename": "video_abc123.mp4",
  "size": 12345678,
  "download_id": "uuid-here",
  "download_url": "/api/file/uuid-here/video_abc123.mp4"
}
```

### 2. 파일 다운로드

```bash
curl -O https://your-url/api/file/uuid-here/video.mp4
```

### 3. Health Check

```bash
curl https://your-url/api/health
```

### 4. 지원 플랫폼 목록

```bash
curl https://your-url/api/platforms
```

---

## 🔧 설정

### 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `PORT` | 서버 포트 | `8080` |
| `FLASK_ENV` | 환경 (development/production) | `production` |
| `SECRET_KEY` | Flask 시크릿 키 | 필수 (프로덕션) |

### Cloud Run 권장 설정

- **메모리**: 2 GiB (비디오 처리용)
- **CPU**: 2 vCPU
- **타임아웃**: 300초 (5분)
- **최대 인스턴스**: 10개
- **최소 인스턴스**: 0개 (비용 절감)

---

## 🐛 문제 해결

### 문제: 빌드 실패

```bash
# 로그 확인
docker build -t test . 2>&1 | tee build.log

# Docker Compose 로그
docker-compose logs
```

### 문제: 서비스 시작 안 됨

```bash
# Cloud Run 로그 확인
gcloud run services logs tail $SERVICE_NAME --region $REGION

# 로컬 Docker 로그
docker logs <container_id>
```

### 문제: yt-dlp 없음

```bash
# 컨테이너 내부 확인
docker exec -it <container_id> bash
which yt-dlp
yt-dlp --version
```

### 문제: 타임아웃

```bash
# Cloud Run 타임아웃 증가
gcloud run services update $SERVICE_NAME \
  --timeout 600 \
  --region $REGION
```

### 문제: 메모리 부족

```bash
# 메모리 증가
gcloud run services update $SERVICE_NAME \
  --memory 4Gi \
  --region $REGION
```

### 문제: Threads 다운로드 실패

```bash
# Chrome/Chromium 확인
docker exec -it <container_id> bash
chromium --version
chromedriver --version
```

---

## 💰 비용 예측

### Cloud Run 무료 할당량 (월간)
- 요청: 2백만 건
- CPU 시간: 180,000 vCPU-초
- 메모리: 360,000 GiB-초
- 네트워크 송신: 1 GiB (북미)

### 비용 계산 예시

**시나리오**: 월 10,000건의 비디오 다운로드
- 평균 다운로드 시간: 30초
- 메모리: 2 GiB
- CPU: 2 vCPU

**비용**:
- CPU: 10,000 × 30 × 2 × $0.000024 = $14.40
- 메모리: 10,000 × 30 × 2 × $0.0000025 = $1.50
- 요청: 10,000 × $0.40 / 1,000,000 = $0.004
- **총 월 비용**: 약 $16

### 비용 절감 팁

1. **최소 인스턴스 0으로 설정**
2. **불필요한 리비전 삭제**
3. **타임아웃 최적화**
4. **캐싱 활용** (향후 개선)

---

## 🔄 업데이트

### 코드 업데이트 후 재배포

```bash
# 코드 수정 후
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION
```

### 롤백

```bash
# 리비전 목록 확인
gcloud run revisions list --service $SERVICE_NAME --region $REGION

# 이전 리비전으로 롤백
gcloud run services update-traffic $SERVICE_NAME \
  --to-revisions REVISION_NAME=100 \
  --region $REGION
```

---

## 📚 추가 리소스

- [DEPLOYMENT.md](DEPLOYMENT.md) - 상세 배포 가이드
- [web/README.md](web/README.md) - 웹 앱 README
- [Cloud Run 문서](https://cloud.google.com/run/docs)
- [Flask 문서](https://flask.palletsprojects.com/)
- [Docker 문서](https://docs.docker.com/)

---

## 🎉 완료!

웹 애플리케이션이 준비되었습니다!

### 테스트해보기

1. **로컬**: http://localhost:8080
2. **Docker**: `docker-compose up`
3. **Cloud**: `gcloud run deploy`

### 지원

문제가 있으면 Issue를 열어주세요!

---

Made by WITHYM | Powered by Flask + Google Cloud Run
