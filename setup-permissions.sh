#!/bin/bash

# Google Cloud Build 권한 설정 스크립트
# Made by WITHYM

set -e

echo "🔐 Cloud Build 권한 설정"
echo "=========================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# 프로젝트 ID 확인
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Google Cloud 프로젝트가 설정되지 않았습니다.${NC}"
    echo "다음 명령어로 프로젝트를 설정하세요:"
    echo "  gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}✓ 프로젝트 ID: $PROJECT_ID${NC}"

# 프로젝트 번호 가져오기
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
echo -e "${GREEN}✓ 프로젝트 번호: $PROJECT_NUMBER${NC}"

# Cloud Build 서비스 계정
CLOUDBUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
echo -e "${BLUE}Cloud Build 서비스 계정: $CLOUDBUILD_SA${NC}"

echo ""
echo "📦 필요한 API 활성화 중..."

# 필요한 API 활성화
APIS=(
    "run.googleapis.com"
    "cloudbuild.googleapis.com"
    "containerregistry.googleapis.com"
    "iam.googleapis.com"
)

for API in "${APIS[@]}"; do
    echo -n "  - $API ... "
    if gcloud services list --enabled --filter="name:$API" --format="value(name)" 2>/dev/null | grep -q "$API"; then
        echo -e "${GREEN}✓${NC}"
    else
        gcloud services enable "$API" --quiet
        echo -e "${GREEN}✓ (활성화됨)${NC}"
    fi
done

echo ""
echo "🔑 Cloud Build 서비스 계정에 권한 부여 중..."

# 필요한 역할
ROLES=(
    "roles/run.admin"
    "roles/iam.serviceAccountUser"
    "roles/storage.admin"
)

for ROLE in "${ROLES[@]}"; do
    echo -n "  - $ROLE ... "

    # 이미 권한이 있는지 확인
    if gcloud projects get-iam-policy $PROJECT_ID \
        --flatten="bindings[].members" \
        --format="table(bindings.role)" \
        --filter="bindings.members:serviceAccount:$CLOUDBUILD_SA AND bindings.role:$ROLE" 2>/dev/null | grep -q "$ROLE"; then
        echo -e "${YELLOW}이미 있음${NC}"
    else
        # 권한 부여
        gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:$CLOUDBUILD_SA" \
            --role="$ROLE" \
            --quiet > /dev/null 2>&1
        echo -e "${GREEN}✓ (부여됨)${NC}"
    fi
done

echo ""
echo -e "${GREEN}=========================================="
echo "✅ 권한 설정이 완료되었습니다!"
echo "==========================================${NC}"
echo ""
echo "이제 배포를 진행할 수 있습니다:"
echo "  ./deploy.sh"
echo ""
echo "또는:"
echo "  gcloud builds submit --config cloudbuild.yaml"
echo ""
