# Video Downloader - 실행 가이드

## ⚠️ PyInstaller 이슈

현재 Python 3.13과 PyInstaller 간 호환성 문제로 인해 EXE 빌드가 불가능합니다.

### 해결 방법

#### 옵션 1: Python으로 직접 실행 (권장)

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 프로그램 실행:
```bash
python main.py
```

#### 옵션 2: 배치 파일 사용

제공된 `run.bat` 파일을 더블클릭하여 실행

#### 옵션 3: Python 3.12로 다운그레이드 후 EXE 빌드

1. Python 3.12 설치
2. 패키지 재설치
3. PyInstaller로 빌드:
```bash
pyinstaller VideoDownloader.spec --clean --noconfirm
```

## 프로그램 기능

✅ **지원 플랫폼:**
- YouTube (일반 영상 + Shorts)
- Threads
- TikTok
- Douyin

✅ **주요 기능:**
- 고품질 비디오 다운로드
- Selenium 기반 Threads 추출
- 자동 재시도 및 fallback
- 다국어 지원 (한국어, 영어, 일본어)

## 시스템 요구사항

- Windows 10 이상
- Python 3.12 이상
- Chrome 브라우저 (Threads 다운로드용)
- yt-dlp (YouTube 다운로드용)

## 문제 해결

### yt-dlp 설치
```bash
pip install yt-dlp
```

### Selenium 설치
```bash
pip install selenium
```

### Chrome WebDriver
Selenium이 자동으로 ChromeDriver를 관리합니다.
