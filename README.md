# Video Downloader - TikTok / Douyin / YouTube

간단한 비디오 다운로더입니다. TikTok, Douyin(抖音), YouTube 영상을 로컬에 다운로드할 수 있습니다.

**Made by WITHYM**

## 주요 기능

✅ **TikTok 비디오 다운로드**
✅ **Douyin(抖音) 비디오 다운로드**
✅ **Threads (베타) 비디오/이미지 다운로드 (GraphQL + Jina fallback)**
✅ **YouTube 비디오 다운로드**
✅ **심플한 GUI**
✅ **다국어 지원** (한국어, English, 日本語)
✅ **자동 플랫폼 감지**
✅ **커스텀 아이콘**

## 설치 방법

### 1. 필수 패키지 설치

```bash
pip install yt-dlp
```

### 2. 프로그램 실행

```bash
python main.py
```

또는 Windows에서 `run.bat` 파일을 더블클릭하세요.

## 사용 방법

1. **언어 선택**: 우측 상단에서 원하는 언어 선택 (한국어/English/日本語)
2. **링크 붙여넣기**: URL 입력창에 TikTok/Douyin/YouTube 링크 붙여넣기
3. **다운로드 클릭**: "다운로드" 버튼 클릭 또는 Enter 키
4. **저장 위치 확인**: 다운로드 완료 후 폴더 자동 열기

### 저장 위치

기본값: `C:\Users\사용자명\Downloads\Videos`

"변경" 버튼으로 변경 가능

## 지원 언어

- 🇰🇷 **한국어** (기본값)
- 🇺🇸 **English**
- 🇯🇵 **日本語**

모든 UI 텍스트, 메시지, 오류 알림이 선택한 언어로 표시됩니다.

## 지원 플랫폼

- **TikTok**: `https://www.tiktok.com/@username/video/...`
- **Douyin**: `https://www.douyin.com/video/...`
- **YouTube**: `https://www.youtube.com/watch?v=...`

## 시스템 요구사항

- Python 3.7 이상
- Windows / macOS / Linux
- 인터넷 연결

## 프로젝트 구조

```
export-tiktok-douyin-youtube/
├── main.py               # 메인 프로그램 (GUI + 다국어)
├── create_icon.py        # 아이콘 생성 스크립트
├── icon.ico              # Windows 아이콘
├── icon.png              # PNG 아이콘
├── requirements.txt      # 필수 패키지
├── README.md            # 사용 설명서
├── run.bat              # Windows 실행 스크립트
├── controller/          # 다운로드 로직
│   ├── DouyinExtract.py
│   ├── TicktokExtract.py
│   └── VideoExtract.py
└── common/              # 유틸리티
    ├── DriverConfig.py
    └── Tool.py
```

## 아이콘

프로그램은 커스텀 아이콘을 사용합니다. 아이콘을 다시 생성하려면:

```bash
pip install Pillow
python create_icon.py
```

## 문제 해결

### yt-dlp 오류

```bash
pip install --upgrade yt-dlp
```

### TikTok/Douyin 다운로드 실패

- URL 확인
- 비디오가 공개 상태인지 확인
- 잠시 후 다시 시도

## 주의사항

- 개인적 용도로만 사용
- 저작권법 준수
- 상업적 용도 금지

## 제작

**Made by WITHYM**

이 프로젝트는 개인 사용 및 학습 목적으로 제공됩니다.

## 라이선스

개인 사용 및 학습 목적으로 제공됩니다.

---

© 2024 WITHYM. All rights reserved.
