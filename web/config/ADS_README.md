# 광고 설정 가이드 (Advertisement Configuration Guide)

이 가이드는 웹사이트에 다양한 광고를 설정하는 방법을 설명합니다.

## 📁 파일 구조

```
web/
├── config/
│   ├── ads.json           # 통합 광고 설정 파일
│   ├── adsense.json       # 구글 애드센스 설정 (레거시)
│   ├── analytics.json     # 구글 애널리틱스 설정
│   └── ADS_README.md      # 이 파일
```

## 🎯 광고 유형

### 1. 구글 애드센스 (Google AdSense)

**위치:** `ads.json` > `adsense`

#### 설정 방법:

1. **광고 활성화:**
```json
{
  "adsense": {
    "enabled": true,
    "client_id": "ca-pub-1234567890123456",
    "auto_ads": false
  }
}
```

2. **광고 슬롯 설정:**

웹사이트에는 5개의 광고 위치가 있습니다:

| 위치 | 설명 | 권장 포맷 |
|------|------|-----------|
| `header_banner` | 페이지 최상단 배너 | horizontal (가로형) |
| `top_content` | 메인 콘텐츠 상단 | rectangle (사각형) |
| `sidebar` | 우측 사이드바 | vertical (세로형) 300x600 |
| `bottom_content` | 메인 콘텐츠 하단 | rectangle (사각형) |
| `footer_banner` | 페이지 최하단 배너 | horizontal (가로형) |

#### 광고 슬롯 설정 예시:

```json
{
  "adsense": {
    "slots": {
      "header_banner": {
        "enabled": true,
        "slot_id": "1111111111",
        "format": "horizontal",
        "responsive": true
      },
      "sidebar": {
        "enabled": true,
        "slot_id": "3333333333",
        "format": "vertical",
        "style": "display:inline-block;width:300px;height:600px",
        "responsive": false
      }
    }
  }
}
```

### 2. 인터스티셜 광고 (전면 광고)

**위치:** `ads.json` > `interstitial`

다운로드 버튼 클릭 시 나타나는 전면 광고입니다.

#### 설정 옵션:

```json
{
  "interstitial": {
    "enabled": true,
    "provider": "adsense",
    "slot_id": "6666666666",
    "triggers": {
      "on_download_click": true,
      "on_page_load": false,
      "frequency": "every_time",
      "delay_seconds": 0
    },
    "settings": {
      "skip_after_seconds": 5,
      "close_button": true,
      "countdown": true
    }
  }
}
```

**주요 설정 설명:**

- `skip_after_seconds`: 광고를 닫을 수 있을 때까지의 초 (기본: 5초)
- `close_button`: 닫기 버튼 표시 여부
- `countdown`: 카운트다운 표시 여부
- `frequency`: 광고 표시 빈도
  - `"every_time"`: 매번 표시
  - `"once_per_session"`: 세션당 1회
  - `"once_per_day"`: 하루에 1회

### 3. 팝업 광고

**위치:** `ads.json` > `popup_ad`

새 탭으로 열리는 팝업 광고입니다.

```json
{
  "popup_ad": {
    "enabled": true,
    "triggers": {
      "on_download_click": true,
      "on_download_complete": false,
      "delay_seconds": 0
    },
    "settings": {
      "type": "new_tab",
      "url": "https://example.com/offer",
      "frequency": "every_time"
    }
  }
}
```

### 4. 커스텀 배너 광고

**위치:** `ads.json` > `custom_banner`

직접 HTML을 입력하여 커스텀 광고를 삽입할 수 있습니다.

```json
{
  "custom_banner": {
    "enabled": true,
    "positions": {
      "header": {
        "enabled": true,
        "html": "<a href='https://example.com' target='_blank'><img src='/static/ads/header-ad.png' alt='Ad' style='width:100%;max-height:90px;'></a>",
        "max_height": "90px"
      },
      "sidebar": {
        "enabled": true,
        "html": "<a href='https://example.com' target='_blank'><img src='/static/ads/sidebar-ad.png' alt='Ad' style='width:300px;height:600px;'></a>",
        "width": "300px"
      },
      "footer": {
        "enabled": true,
        "html": "<a href='https://example.com' target='_blank'><img src='/static/ads/footer-ad.png' alt='Ad' style='width:100%;max-height:90px;'></a>",
        "max_height": "90px"
      }
    }
  }
}
```

**사용 예시:**

1. `/static/ads/` 폴더에 광고 이미지 업로드
2. `custom_banner` 설정에서 HTML 코드 입력
3. `enabled: true`로 활성화

## 📊 광고 분석 (Analytics)

**위치:** `ads.json` > `analytics`

광고 성과를 구글 애널리틱스로 추적합니다.

```json
{
  "analytics": {
    "track_ad_impressions": true,
    "track_ad_clicks": true,
    "track_interstitial_shown": true,
    "track_interstitial_skipped": true
  }
}
```

**추적 이벤트:**

| 이벤트 | 설명 |
|--------|------|
| `ad_impression` | 광고가 표시됨 |
| `ad_click` | 광고 클릭 |
| `interstitial_shown` | 전면 광고 표시 |
| `interstitial_skipped` | 전면 광고 건너뛰기 |
| `popup_ad_shown` | 팝업 광고 표시 |

## 🚀 빠른 시작 가이드

### 1단계: 구글 애드센스 계정 생성

1. [Google AdSense](https://www.google.com/adsense/) 접속
2. 계정 생성 및 사이트 등록
3. Publisher ID 확인 (형식: `ca-pub-XXXXXXXXXXXXXXXX`)

### 2단계: 광고 단위 생성

1. AdSense > 광고 > 광고 단위별
2. 새 광고 단위 생성
3. 각 위치별로 광고 단위 ID 복사

### 3단계: ads.json 설정

```json
{
  "adsense": {
    "enabled": true,
    "client_id": "ca-pub-1234567890123456",
    "slots": {
      "header_banner": {
        "enabled": true,
        "slot_id": "YOUR_SLOT_ID_1"
      },
      "top_content": {
        "enabled": true,
        "slot_id": "YOUR_SLOT_ID_2"
      }
    }
  },
  "interstitial": {
    "enabled": true,
    "slot_id": "YOUR_INTERSTITIAL_SLOT_ID",
    "triggers": {
      "on_download_click": true
    },
    "settings": {
      "skip_after_seconds": 5,
      "countdown": true
    }
  }
}
```

### 4단계: 서버 재시작

```bash
python web/app.py
```

또는

```bash
PORT=8080 python web/app.py
```

## 💡 모범 사례

### 1. 광고 로딩 최적화

- `auto_ads: false` 사용 권장 (수동 광고 배치가 더 빠름)
- 필요한 광고 슬롯만 활성화
- `responsive: true` 사용으로 모바일 최적화

### 2. 사용자 경험

- 인터스티셜 광고 `skip_after_seconds`는 3-5초 권장
- 너무 많은 광고는 사용자 이탈 증가
- 팝업 광고는 신중하게 사용

### 3. 광고 수익 최적화

**권장 배치:**
```
✅ Header Banner (상단)
✅ Top Content (콘텐츠 상단)
✅ Bottom Content (콘텐츠 하단)
⚠️ Sidebar (데스크톱만)
⚠️ Footer Banner (필요시)
```

**인터스티셜 광고:**
```
✅ 다운로드 클릭 시 (주요 액션)
❌ 페이지 로드 시 (사용자 경험 저하)
```

## 🔧 문제 해결

### 광고가 표시되지 않는 경우

1. **설정 확인**
```json
{
  "adsense": {
    "enabled": true  // false가 아닌지 확인
  }
}
```

2. **Client ID 확인**
   - 형식: `ca-pub-XXXXXXXXXXXXXXXX`
   - 16자리 숫자 확인

3. **Slot ID 확인**
   - AdSense에서 생성한 광고 단위 ID
   - 숫자만 입력

4. **브라우저 캐시 삭제**
```bash
Ctrl + Shift + Delete (Chrome)
```

5. **서버 재시작**
```bash
python web/app.py
```

### 광고가 승인되지 않은 경우

- AdSense 정책 확인
- 사이트 콘텐츠 품질 확인
- 트래픽이 충분한지 확인
- 보통 1-3일 소요

### 인터스티셜 광고가 작동하지 않는 경우

1. `ads.json` 확인:
```json
{
  "interstitial": {
    "enabled": true,
    "triggers": {
      "on_download_click": true
    }
  }
}
```

2. 브라우저 콘솔 확인 (F12)
3. 애드블록 비활성화 확인

## 📞 지원

### 공식 문서

- [Google AdSense 고객센터](https://support.google.com/adsense/)
- [Google AdSense 정책](https://support.google.com/adsense/answer/48182)
- [Google Analytics 도움말](https://support.google.com/analytics/)

### 이 프로젝트 관련

- 이슈 리포트: GitHub Issues
- 설정 파일 위치: `web/config/ads.json`
- 로그 확인: 서버 콘솔 출력

## 📄 라이센스 및 법적 고지

- Google AdSense 정책을 준수해야 합니다
- 무효 클릭 유도 금지
- 성인/불법 콘텐츠 금지
- 정책 위반 시 계정 정지 가능

---

**Made by WITHYM**

마지막 업데이트: 2025-01-25
