@echo off
REM Google Cloud Build 권한 설정 스크립트 (Windows)
REM Made by WITHYM

echo ==========================================
echo 🔐 Cloud Build 권한 설정
echo ==========================================
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

REM 프로젝트 번호 가져오기
for /f "tokens=*" %%i in ('gcloud projects describe %PROJECT_ID% --format="value(projectNumber)"') do set PROJECT_NUMBER=%%i
echo ✓ 프로젝트 번호: %PROJECT_NUMBER%

REM Cloud Build 서비스 계정
set CLOUDBUILD_SA=%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com
echo Cloud Build 서비스 계정: %CLOUDBUILD_SA%
echo.

echo 📦 필요한 API 활성화 중...
gcloud services enable run.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet
gcloud services enable iam.googleapis.com --quiet
echo ✓ API 활성화 완료
echo.

echo 🔑 Cloud Build 서비스 계정에 권한 부여 중...

REM roles/run.admin 권한 부여
echo   - roles/run.admin
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%CLOUDBUILD_SA%" --role="roles/run.admin" --quiet >nul 2>&1
echo     ✓ 부여됨

REM roles/iam.serviceAccountUser 권한 부여
echo   - roles/iam.serviceAccountUser
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%CLOUDBUILD_SA%" --role="roles/iam.serviceAccountUser" --quiet >nul 2>&1
echo     ✓ 부여됨

REM roles/storage.admin 권한 부여
echo   - roles/storage.admin
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%CLOUDBUILD_SA%" --role="roles/storage.admin" --quiet >nul 2>&1
echo     ✓ 부여됨

echo.
echo ==========================================
echo ✅ 권한 설정이 완료되었습니다!
echo ==========================================
echo.
echo 이제 배포를 진행할 수 있습니다:
echo   deploy.bat
echo.
echo 또는:
echo   gcloud builds submit --config cloudbuild.yaml
echo.

pause
