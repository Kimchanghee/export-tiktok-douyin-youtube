# Google Cloud Run 배포 가이드

Google Cloud Run에서 Video Downloader 웹 애플리케이션을 배포하는 방법입니다.

## 📋 사전 요구사항

1. Google Cloud 계정
2. Google Cloud SDK (gcloud CLI) 설치
3. 프로젝트 생성
4. 결제 계정 연결

---

## 🚀 빠른 배포 (Cloud Build 사용)

### 1. Google Cloud SDK 설치 및 초기 설정

```bash
# gcloud CLI 설치 (이미 설치되어 있다면 생략)
# Windows: https://cloud.google.com/sdk/docs/install
# macOS: brew install --cask google-cloud-sdk
# Linux: curl https://sdk.cloud.google.com | bash

# 로그인
gcloud auth login

# 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# 리전 설정 (서울)
gcloud config set run/region asia-northeast3
```

### 2. 필요한 API 활성화

```bash
# Cloud Run API 활성화
gcloud services enable run.googleapis.com

# Cloud Build API 활성화
gcloud services enable cloudbuild.googleapis.com

# Container Registry API 활성화
gcloud services enable containerregistry.googleapis.com
```

### 3. Cloud Build로 배포

```bash
# 프로젝트 루트 디렉토리에서 실행
gcloud builds submit --config cloudbuild.yaml
```

**완료!** Cloud Build가 자동으로:
- Docker 이미지 빌드
- Container Registry에 푸시
- Cloud Run에 배포

배포가 완료되면 URL이 출력됩니다:
```
Service [video-downloader] revision [video-downloader-xxxxx] has been deployed
Service URL: https://video-downloader-xxxxx-an.a.run.app
```

---

## 🔧 수동 배포 방법

Cloud Build 없이 수동으로 배포하려면:

### 1. Docker 이미지 빌드

```bash
# Artifact Registry 사용 (권장)
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/video-downloader

# 또는 로컬에서 빌드
docker build -t gcr.io/YOUR_PROJECT_ID/video-downloader .
docker push gcr.io/YOUR_PROJECT_ID/video-downloader
```

### 2. Cloud Run에 배포

```bash
gcloud run deploy video-downloader \
  --image gcr.io/YOUR_PROJECT_ID/video-downloader \
  --region asia-northeast3 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300s \
  --max-instances 10 \
  --min-instances 0 \
  --concurrency 80 \
  --set-env-vars FLASK_ENV=production,PORT=8080
```

---

## ⚙️ Cloud Run 설정 상세

### 리소스 할당

```yaml
메모리: 2Gi       # 비디오 다운로드를 위한 충분한 메모리
CPU: 2           # 2개 vCPU
타임아웃: 300초   # 5분 (긴 다운로드 대응)
동시성: 80       # 인스턴스당 최대 80개 동시 요청
```

### 자동 스케일링

```yaml
최소 인스턴스: 0   # 비용 절감 (요청 없을 때 0으로)
최대 인스턴스: 10  # 트래픽 급증 대응
```

### 환경 변수 설정

```bash
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --set-env-vars \
    FLASK_ENV=production,\
    SECRET_KEY=your-super-secret-key-here,\
    PORT=8080
```

---

## 🌍 리전 선택

### 권장 리전

```bash
# 한국 사용자 대상
asia-northeast3  # 서울 (권장)

# 일본 사용자 대상
asia-northeast1  # 도쿄

# 글로벌 사용자 대상
us-central1      # 미국 중부 (저렴)
```

리전 변경:
```bash
gcloud config set run/region asia-northeast3
```

---

## 💰 비용 최적화

### 1. 최소 인스턴스 0으로 설정
```bash
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --min-instances 0
```

### 2. 메모리 조정
비용을 줄이려면 메모리를 1Gi로 줄이기:
```bash
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --memory 1Gi
```

### 3. CPU 할당 모드
```bash
# CPU always allocated (항상 할당) - 빠른 응답
--cpu-throttling

# CPU allocated only during request (요청 시만) - 비용 절감
--no-cpu-throttling
```

---

## 🔒 보안 설정

### 1. 인증 요구 (필요한 경우)

```bash
# 인증 필요하도록 변경
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --no-allow-unauthenticated

# 특정 서비스 계정에만 접근 허용
gcloud run services add-iam-policy-binding video-downloader \
  --region asia-northeast3 \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### 2. 커스텀 도메인 연결

```bash
# 도메인 매핑
gcloud run domain-mappings create \
  --service video-downloader \
  --domain your-domain.com \
  --region asia-northeast3
```

### 3. HTTPS 강제 (기본값)
Cloud Run은 자동으로 HTTPS를 제공하고 HTTP 요청을 리다이렉트합니다.

---

## 📊 모니터링 및 로그

### 로그 확인

```bash
# 실시간 로그
gcloud run services logs tail video-downloader \
  --region asia-northeast3

# 최근 로그 조회
gcloud run services logs read video-downloader \
  --region asia-northeast3 \
  --limit 100
```

### Cloud Console에서 확인

1. [Cloud Run Console](https://console.cloud.google.com/run)
2. 서비스 선택
3. "로그" 탭 또는 "측정항목" 탭

---

## 🔄 업데이트 및 롤백

### 새 버전 배포

```bash
# 코드 수정 후
gcloud builds submit --config cloudbuild.yaml
```

### 롤백

```bash
# 리비전 목록 확인
gcloud run revisions list --service video-downloader --region asia-northeast3

# 특정 리비전으로 롤백
gcloud run services update-traffic video-downloader \
  --region asia-northeast3 \
  --to-revisions REVISION_NAME=100
```

### 트래픽 분할 (카나리 배포)

```bash
# 50%씩 분할
gcloud run services update-traffic video-downloader \
  --region asia-northeast3 \
  --to-revisions REVISION_1=50,REVISION_2=50
```

---

## 🧪 로컬에서 Docker 테스트

배포 전에 로컬에서 Docker 이미지 테스트:

```bash
# 이미지 빌드
docker build -t video-downloader .

# 컨테이너 실행
docker run -p 8080:8080 \
  -e FLASK_ENV=production \
  -e PORT=8080 \
  video-downloader

# 브라우저에서 확인
# http://localhost:8080
```

Docker Compose로 테스트:
```bash
docker-compose up --build
```

---

## 🐛 문제 해결

### 1. 빌드 실패

```bash
# 상세 로그 확인
gcloud builds log BUILD_ID

# Cloud Build 히스토리
gcloud builds list --limit 10
```

### 2. 메모리 부족

증상: 503 오류, "Memory limit exceeded"
```bash
# 메모리 증가
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --memory 4Gi
```

### 3. 타임아웃 오류

증상: 504 Gateway Timeout
```bash
# 타임아웃 증가
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --timeout 600s
```

### 4. 헬스체크 실패

```bash
# 로그 확인
gcloud run services logs read video-downloader \
  --region asia-northeast3 | grep health
```

---

## 📈 성능 최적화

### 1. Cold Start 최소화

```bash
# 최소 인스턴스 1로 설정 (항상 1개 웜 인스턴스 유지)
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --min-instances 1
```

⚠️ 주의: 비용이 증가합니다

### 2. 동시성 조정

```bash
# 인스턴스당 동시 요청 수 증가
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --concurrency 100
```

### 3. CPU 부스트

```bash
# Startup CPU boost 활성화
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --cpu-boost
```

---

## 💡 팁

### cloudbuild.yaml 커스터마이징

리전, 메모리, CPU 등을 변경하려면 `cloudbuild.yaml` 파일 수정:

```yaml
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: gcloud
  args:
    - 'run'
    - 'deploy'
    - 'video-downloader'
    - '--region'
    - 'asia-northeast3'  # 여기 수정
    - '--memory'
    - '2Gi'              # 여기 수정
    - '--cpu'
    - '2'                # 여기 수정
```

### 환경 변수 관리

중요한 비밀 정보는 Secret Manager 사용:

```bash
# Secret 생성
echo -n "your-secret-key" | gcloud secrets create app-secret-key --data-file=-

# Cloud Run에서 사용
gcloud run services update video-downloader \
  --region asia-northeast3 \
  --update-secrets SECRET_KEY=app-secret-key:latest
```

---

## 📚 추가 리소스

- [Cloud Run 문서](https://cloud.google.com/run/docs)
- [Cloud Build 문서](https://cloud.google.com/build/docs)
- [가격 계산기](https://cloud.google.com/products/calculator)
- [Cloud Run 모범 사례](https://cloud.google.com/run/docs/tips)

---

## 🎯 체크리스트

배포 전 확인사항:

- [ ] Google Cloud 프로젝트 생성
- [ ] 결제 계정 연결
- [ ] gcloud CLI 설치 및 인증
- [ ] 필요한 API 활성화
- [ ] `cloudbuild.yaml`에서 리전 확인
- [ ] 로컬에서 Docker 테스트
- [ ] 환경 변수 설정
- [ ] 애드센스 ID 교체 (`web/templates/index.html`)

배포 후 확인사항:

- [ ] 서비스 URL 접속 테스트
- [ ] 다운로드 기능 테스트 (YouTube, TikTok 등)
- [ ] 다국어 전환 테스트
- [ ] 모바일 반응형 확인
- [ ] 로그 확인
- [ ] 비용 모니터링 설정

---

Made by WITHYM | Google Cloud Run 배포 준비 완료! ☁️
