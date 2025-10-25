@echo off
REM Video Downloader - Google Cloud Run 배포 스크립트 (Windows)
REM Made by WITHYM

echo ========================================
echo 🚀 Video Downloader - Cloud Run 배포
echo ========================================
echo.

REM 프로젝트 ID 확인
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i

if "%PROJECT_ID%"=="" (
    echo ❌ Google Cloud 프로젝트가 설정되지 않았습니다.
    echo.
    echo 다음 명령어로 프로젝트를 설정하세요:
    echo   gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo ✓ 프로젝트 ID: %PROJECT_ID%

REM 리전 확인
for /f "tokens=*" %%i in ('gcloud config get-value run/region 2^>nul') do set REGION=%%i

if "%REGION%"=="" (
    echo ⚠ 리전이 설정되지 않았습니다. 서울(asia-northeast3)로 설정합니다.
    gcloud config set run/region asia-northeast3
    set REGION=asia-northeast3
)

echo ✓ 리전: %REGION%
echo.

REM 필요한 API 활성화
echo 📦 필요한 API 활성화 중...
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
echo.

REM 배포 확인
echo 🔍 배포 정보:
echo   프로젝트: %PROJECT_ID%
echo   리전: %REGION%
echo   서비스명: video-downloader
echo.

set /p CONFIRM="배포를 계속하시겠습니까? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo 배포가 취소되었습니다.
    pause
    exit /b 0
)

REM Cloud Build로 배포
echo.
echo 🏗️  Cloud Build 시작...
gcloud builds submit --config cloudbuild.yaml

echo.
echo ==========================================
echo ✅ 배포가 완료되었습니다!
echo ==========================================

REM 서비스 URL 가져오기
for /f "tokens=*" %%i in ('gcloud run services describe video-downloader --region=%REGION% --format="value(status.url)" 2^>nul') do set SERVICE_URL=%%i

if not "%SERVICE_URL%"=="" (
    echo.
    echo 🌐 서비스 URL: %SERVICE_URL%
    echo.
    echo 브라우저에서 위 URL로 접속하세요!
) else (
    echo.
    echo 서비스 URL을 확인하려면 다음 명령어를 실행하세요:
    echo   gcloud run services describe video-downloader --region=%REGION% --format="value(status.url)"
)

echo.
echo 📊 로그 확인:
echo   gcloud run services logs tail video-downloader --region=%REGION%
echo.
echo 🔧 서비스 업데이트:
echo   gcloud run services update video-downloader --region=%REGION% [옵션]
echo.

pause
