# Video Downloader - Cloud Run Edition

Google Cloud Run에서 실행 가능한 다국어 비디오 다운로더 웹 애플리케이션

Made by WITHYM

---

## 🚀 빠른 배포

### 방법 1: 자동 배포 스크립트 (권장)

**Windows:**
```cmd
deploy.bat
```

**Linux/macOS:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### 방법 2: 수동 배포

```bash
# 1. Google Cloud 로그인
gcloud auth login

# 2. 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# 3. 리전 설정 (서울)
gcloud config set run/region asia-northeast3

# 4. 필요한 API 활성화
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com

# 5. 배포
gcloud builds submit --config cloudbuild.yaml
```

배포가 완료되면 서비스 URL이 출력됩니다:
```
Service URL: https://video-downloader-xxxxx-an.a.run.app
```

---

## 📁 프로젝트 구조

```
tiktok-douyin-youtube-web-version/
├── 📄 Dockerfile                    # Multi-stage Docker 빌드
├── 📄 cloudbuild.yaml               # Cloud Build 설정
├── 📄 .dockerignore                 # Docker 빌드 제외 파일
├── 📄 .gcloudignore                 # Cloud 업로드 제외 파일
├── 📄 docker-compose.yml            # 로컬 테스트용
├── 📄 .env.example                  # 환경 변수 예제
│
├── 📜 deploy.sh                     # 배포 스크립트 (Linux/macOS)
├── 📜 deploy.bat                    # 배포 스크립트 (Windows)
│
├── 📚 GOOGLE_CLOUD_RUN_DEPLOYMENT.md   # 상세 배포 가이드
├── 📚 QUICK_START.md                   # 빠른 시작 가이드
├── 📚 WEB_APP_GUIDE_KO.md              # 웹앱 가이드 (한국어)
├── 📚 WEB_APP_GUIDE_EN.md              # 웹앱 가이드 (영어)
│
└── web/                             # 웹 애플리케이션
    ├── app.py                       # Flask 앱
    ├── templates/
    │   └── index.html              # 프론트엔드 (다크모드, 20개 언어)
    ├── locales/                    # 언어 파일 (20개)
    │   ├── ko.json
    │   ├── en.json
    │   ├── ja.json
    │   └── ... (17개 더)
    └── requirements.txt
```

---

## ✨ 주요 기능

### 🌍 20개 언어 지원
🇰🇷 한국어 | 🇺🇸 English | 🇯🇵 日本語 | 🇨🇳 简体中文 | 🇹🇼 繁體中文
🇪🇸 Español | 🇫🇷 Français | 🇩🇪 Deutsch | 🇮🇹 Italiano | 🇵🇹 Português
🇷🇺 Русский | 🇸🇦 العربية | 🇮🇳 हिन्दी | 🇹🇭 ไทย | 🇻🇳 Tiếng Việt
🇮🇩 Indonesia | 🇹🇷 Türkçe | 🇵🇱 Polski | 🇳🇱 Nederlands | 🇸🇪 Svenska

### 📹 지원 플랫폼
- **YouTube** (일반 영상 + Shorts)
- **TikTok**
- **Douyin** (抖音)
- **Threads**

### 🎨 모던 UI
- 다크 모드 지원
- 반응형 디자인 (모바일/태블릿/데스크톱)
- 부드러운 애니메이션
- 언어 선택 드롭다운

### 💰 수익화
- 구글 애드센스 통합 준비 완료
- 2개 광고 슬롯 (상단/하단)

### 🔒 보안
- Non-root 컨테이너 실행
- Multi-stage Docker 빌드
- 최소 권한 원칙

---

## 🔧 Cloud Run 설정

### 현재 설정 (cloudbuild.yaml)

```yaml
리전: asia-northeast3 (서울)
메모리: 2Gi
CPU: 2 vCPU
타임아웃: 300초 (5분)
동시성: 80
최소 인스턴스: 0
최대 인스턴스: 10
인증: 불필요 (public)
```

### 설정 변경

`cloudbuild.yaml` 파일에서 수정:

```yaml
- '--memory'
- '2Gi'              # 1Gi, 2Gi, 4Gi 등

- '--cpu'
- '2'                # 1, 2, 4 등

- '--region'
- 'asia-northeast3'  # 서울, tokyo: asia-northeast1
```

---

## 💰 예상 비용

### Cloud Run 가격 (서울 리전)

**요청당:**
- vCPU: $0.00002400 per vCPU-second
- 메모리: $0.00000250 per GiB-second
- 요청: $0.40 per million requests

**무료 등급 (매월):**
- 2 million requests
- 360,000 vCPU-seconds
- 180,000 GiB-seconds

### 예상 비용 계산

월 10,000회 다운로드 기준:
- 평균 처리 시간: 30초
- 메모리: 2GB
- CPU: 2 vCPU

```
vCPU: 10,000 × 30초 × 2 vCPU × $0.000024 = $14.40
메모리: 10,000 × 30초 × 2 GB × $0.0000025 = $1.50
요청: 10,000 × $0.0000004 = $0.004

월 예상 비용: 약 $16
```

💡 **팁:** 최소 인스턴스를 0으로 설정하면 사용하지 않을 때 비용이 발생하지 않습니다!

---

## 🧪 로컬에서 테스트

### Docker로 테스트

```bash
# 이미지 빌드
docker build -t video-downloader .

# 컨테이너 실행
docker run -p 8080:8080 video-downloader

# 브라우저에서 접속
# http://localhost:8080
```

### Docker Compose로 테스트

```bash
# 빌드 및 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 중지
docker-compose down
```

### Python으로 직접 실행

```bash
# 의존성 설치
pip install -r web/requirements.txt
pip install yt-dlp

# 개발 서버 실행
python web/app.py
```

---

## 📊 모니터링

### 로그 확인

```bash
# 실시간 로그
gcloud run services logs tail video-downloader --region asia-northeast3

# 최근 100줄
gcloud run services logs read video-downloader --region asia-northeast3 --limit 100
```

### 서비스 상태

```bash
# 서비스 정보
gcloud run services describe video-downloader --region asia-northeast3

# 리비전 목록
gcloud run revisions list --service video-downloader --region asia-northeast3
```

### Cloud Console

[Google Cloud Run Console](https://console.cloud.google.com/run) → 서비스 선택 → 측정항목/로그

---

## 🔄 업데이트

### 코드 수정 후 재배포

```bash
# 방법 1: 배포 스크립트
./deploy.sh  # 또는 deploy.bat

# 방법 2: 수동
gcloud builds submit --config cloudbuild.yaml
```

### 환경 변수 업데이트

```bash
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --set-env-vars SECRET_KEY=new-secret-key
```

### 롤백

```bash
# 리비전 확인
gcloud run revisions list --service video-downloader --region asia-northeast3

# 이전 리비전으로 롤백
gcloud run services update-traffic video-downloader \
  --region asia-northeast3 \
  --to-revisions REVISION_NAME=100
```

---

## 💡 유용한 명령어

### 서비스 삭제

```bash
gcloud run services delete video-downloader --region asia-northeast3
```

### 트래픽 100% 특정 리비전으로

```bash
gcloud run services update-traffic video-downloader \
  --region asia-northeast3 \
  --to-latest
```

### 커스텀 도메인 연결

```bash
gcloud run domain-mappings create \
  --service video-downloader \
  --domain your-domain.com \
  --region asia-northeast3
```

---

## 🐛 문제 해결

### 빌드 실패

```bash
# 빌드 로그 확인
gcloud builds log [BUILD_ID]

# 로컬에서 Docker 빌드 테스트
docker build -t test .
```

### 메모리 부족 (503)

```bash
# 메모리 증가
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --memory 4Gi
```

### 타임아웃 (504)

```bash
# 타임아웃 증가
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --timeout 600s
```

---

## 📚 문서

- [상세 배포 가이드](GOOGLE_CLOUD_RUN_DEPLOYMENT.md)
- [빠른 시작](QUICK_START.md)
- [웹앱 가이드 (한국어)](WEB_APP_GUIDE_KO.md)
- [웹앱 가이드 (영어)](WEB_APP_GUIDE_EN.md)

---

## 🎯 배포 체크리스트

### 배포 전

- [ ] Google Cloud 계정 생성
- [ ] 프로젝트 생성 및 결제 설정
- [ ] gcloud CLI 설치
- [ ] `cloudbuild.yaml`에서 리전 확인
- [ ] 애드센스 ID 교체 (`web/templates/index.html`)
- [ ] 로컬 Docker 테스트

### 배포 후

- [ ] 서비스 URL 접속 확인
- [ ] 다운로드 기능 테스트
- [ ] 다국어 전환 테스트
- [ ] 모바일 반응형 확인
- [ ] 로그 모니터링 설정
- [ ] 비용 알림 설정

---

## 📞 지원

문제가 발생하면:
1. [문제 해결 섹션](#-문제-해결) 확인
2. [Cloud Run 문서](https://cloud.google.com/run/docs) 참조
3. 로그 확인: `gcloud run services logs read video-downloader`

---

Made by WITHYM | Cloud Run Ready ☁️

**배포 완료 후 접속하세요!** 🚀
