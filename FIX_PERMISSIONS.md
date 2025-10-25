# Cloud Build 권한 오류 해결 가이드

## ❌ 발생한 오류

```
실패: Cloud Build 트리거를 만들 수 없습니다.
지속적 배포 파이프라인이 설정되지 않았습니다.
기본 Compute 서비스 계정에 필요한 역할을 설정하는 중에 오류가 발생했습니다.
roles/run.admin, roles/iam.serviceAccountUser 역할이 필요합니다.
```

이 오류는 Cloud Build 서비스 계정에 Cloud Run을 배포할 권한이 없어서 발생합니다.

---

## ✅ 해결 방법

### 방법 1: 자동 권한 설정 스크립트 (권장)

**Windows:**
```cmd
setup-permissions.bat
```

**Linux/macOS:**
```bash
chmod +x setup-permissions.sh
./setup-permissions.sh
```

스크립트가 자동으로:
- ✓ 필요한 API 활성화
- ✓ Cloud Build 서비스 계정 확인
- ✓ 필요한 권한 부여

완료 후 다시 배포:
```bash
./deploy.sh  # 또는 deploy.bat
```

---

### 방법 2: 수동 권한 설정

#### 1단계: 프로젝트 정보 확인

```bash
# 프로젝트 ID 확인
gcloud config get-value project

# 프로젝트 번호 확인
gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)'
```

출력 예시:
```
프로젝트 ID: my-project-id
프로젝트 번호: 123456789012
```

#### 2단계: Cloud Build 서비스 계정 확인

Cloud Build 서비스 계정 형식:
```
[프로젝트_번호]@cloudbuild.gserviceaccount.com
```

예: `123456789012@cloudbuild.gserviceaccount.com`

#### 3단계: 필요한 API 활성화

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable iam.googleapis.com
```

#### 4단계: 권한 부여

**roles/run.admin (Cloud Run 관리 권한)**
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"
```

**roles/iam.serviceAccountUser (서비스 계정 사용 권한)**
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

**roles/storage.admin (Container Registry 접근 권한)**
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"
```

#### 5단계: 권한 확인

```bash
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --format="table(bindings.role)"
```

다음 역할들이 표시되어야 합니다:
```
roles/run.admin
roles/iam.serviceAccountUser
roles/storage.admin
```

---

### 방법 3: Google Cloud Console에서 설정

#### 1. IAM 페이지로 이동
[https://console.cloud.google.com/iam-admin/iam](https://console.cloud.google.com/iam-admin/iam)

#### 2. Cloud Build 서비스 계정 찾기
`@cloudbuild.gserviceaccount.com`으로 끝나는 계정 찾기

#### 3. 권한 추가
연필 아이콘 클릭 → "역할 추가" 클릭

다음 역할들을 추가:
- ✓ Cloud Run 관리자 (`roles/run.admin`)
- ✓ 서비스 계정 사용자 (`roles/iam.serviceAccountUser`)
- ✓ Storage 관리자 (`roles/storage.admin`)

#### 4. 저장

---

## 🧪 권한 설정 확인

설정이 완료되었으면 테스트:

```bash
# 권한 확인
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com"

# 배포 테스트
gcloud builds submit --config cloudbuild.yaml
```

---

## 📋 필요한 권한 설명

| 역할 | 이름 | 필요한 이유 |
|------|------|------------|
| `roles/run.admin` | Cloud Run 관리자 | Cloud Run 서비스 생성, 업데이트, 배포 |
| `roles/iam.serviceAccountUser` | 서비스 계정 사용자 | Cloud Run 서비스에서 서비스 계정 사용 |
| `roles/storage.admin` | Storage 관리자 | Container Registry에 Docker 이미지 업로드 |

---

## 🔐 최소 권한 원칙 (선택사항)

보안을 더 강화하려면 커스텀 역할 생성:

```bash
# 커스텀 역할 생성
gcloud iam roles create cloudrun_deployer \
    --project=YOUR_PROJECT_ID \
    --title="Cloud Run Deployer" \
    --description="Custom role for Cloud Run deployment" \
    --permissions=run.services.create,run.services.update,run.services.get,run.services.list,run.operations.get,iam.serviceaccounts.actAs

# 권한 부여
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="projects/YOUR_PROJECT_ID/roles/cloudrun_deployer"
```

---

## 🐛 추가 문제 해결

### 여전히 권한 오류가 발생하는 경우

#### 1. 프로젝트 소유자인지 확인
```bash
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:user:YOUR_EMAIL"
```

`roles/owner` 또는 `roles/editor`가 있어야 합니다.

#### 2. Cloud Build API가 활성화되었는지 재확인
```bash
gcloud services list --enabled | grep cloudbuild
```

#### 3. 조직 정책 확인 (기업 계정)
조직에서 제한을 걸었을 수 있습니다. 관리자에게 문의하세요.

#### 4. 권한 적용 대기
권한 설정 후 몇 분 정도 기다린 후 다시 시도:
```bash
sleep 60
gcloud builds submit --config cloudbuild.yaml
```

---

## 📚 관련 문서

- [Cloud Build IAM 역할](https://cloud.google.com/build/docs/iam-roles-permissions)
- [Cloud Run IAM 역할](https://cloud.google.com/run/docs/reference/iam/roles)
- [서비스 계정 관리](https://cloud.google.com/iam/docs/service-accounts)

---

## 🎯 빠른 해결 체크리스트

권한 설정 전:
- [ ] `gcloud auth login` 실행
- [ ] 프로젝트 ID 확인
- [ ] 프로젝트에 소유자/편집자 권한 있음

권한 설정:
- [ ] `setup-permissions.sh` (또는 `.bat`) 실행
- [ ] 또는 수동으로 3개 역할 부여
- [ ] 권한 확인 명령어 실행

배포:
- [ ] `./deploy.sh` 실행
- [ ] 또는 `gcloud builds submit --config cloudbuild.yaml`
- [ ] 배포 성공 확인

---

## 💡 팁

1. **한 번만 설정하면 됩니다**
   - 권한은 프로젝트별로 한 번만 설정하면 됩니다
   - 이후 배포는 `deploy.sh`만 실행하면 됩니다

2. **다른 프로젝트에서도 사용**
   - 새 프로젝트에서도 똑같이 권한 설정 필요

3. **권한 제거** (필요한 경우)
   ```bash
   gcloud projects remove-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
       --role="roles/run.admin"
   ```

---

Made by WITHYM | 권한 문제 해결 완료! 🔐
