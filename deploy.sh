#!/bin/bash

# Video Downloader - Google Cloud Run 배포 스크립트
# Made by WITHYM

set -e

echo "🚀 Video Downloader - Cloud Run 배포 시작"
echo "=========================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 리전 확인
REGION=$(gcloud config get-value run/region 2>/dev/null)

if [ -z "$REGION" ]; then
    echo -e "${YELLOW}⚠ 리전이 설정되지 않았습니다. 서울(asia-northeast3)로 설정합니다.${NC}"
    gcloud config set run/region asia-northeast3
    REGION="asia-northeast3"
fi

echo -e "${GREEN}✓ 리전: $REGION${NC}"

# 필요한 API 확인 및 활성화
echo ""
echo "📦 필요한 API 확인 중..."

APIS=("run.googleapis.com" "cloudbuild.googleapis.com" "containerregistry.googleapis.com")

for API in "${APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$API" --format="value(name)" | grep -q "$API"; then
        echo -e "${GREEN}✓ $API 활성화됨${NC}"
    else
        echo -e "${YELLOW}⚠ $API 활성화 중...${NC}"
        gcloud services enable "$API"
        echo -e "${GREEN}✓ $API 활성화 완료${NC}"
    fi
done

# 배포 확인
echo ""
echo "🔍 배포 정보:"
echo "  프로젝트: $PROJECT_ID"
echo "  리전: $REGION"
echo "  서비스명: video-downloader"
echo ""
read -p "배포를 계속하시겠습니까? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "배포가 취소되었습니다."
    exit 0
fi

# Cloud Build로 배포
echo ""
echo "🏗️  Cloud Build 시작..."
gcloud builds submit --config cloudbuild.yaml

echo ""
echo -e "${GREEN}=========================================="
echo "✅ 배포가 완료되었습니다!"
echo "==========================================${NC}"

# 서비스 URL 가져오기
SERVICE_URL=$(gcloud run services describe video-downloader --region="$REGION" --format="value(status.url)" 2>/dev/null)

if [ -n "$SERVICE_URL" ]; then
    echo ""
    echo -e "${GREEN}🌐 서비스 URL: $SERVICE_URL${NC}"
    echo ""
    echo "브라우저에서 위 URL로 접속하세요!"
else
    echo ""
    echo "서비스 URL을 확인하려면 다음 명령어를 실행하세요:"
    echo "  gcloud run services describe video-downloader --region=$REGION --format='value(status.url)'"
fi

echo ""
echo "📊 로그 확인:"
echo "  gcloud run services logs tail video-downloader --region=$REGION"
echo ""
echo "🔧 서비스 업데이트:"
echo "  gcloud run services update video-downloader --region=$REGION [옵션]"
echo ""
