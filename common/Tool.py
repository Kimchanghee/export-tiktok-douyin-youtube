import re
import time
from urllib.parse import urlparse, urlunparse, unquote, urljoin, parse_qs
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
import html
from typing import Dict, List, Optional, Tuple, Iterable
import random

from common import DriverConfig

def _extract_quality_metrics(url: str) -> Tuple[int, int, int]:
    """
    Inspect known query parameters and path segments to infer relative quality.
    Returns (resolution_height, fps, bitrate) so callers can prioritise highest quality.
    """
    lower = url.lower()
    quality = 0
    fps = 0
    bitrate = 0

    # Look for explicit resolution markers like 1080p, 720p, 2160p, etc.
    for match in re.findall(r'(\d{3,4})p', lower):
        try:
            quality = max(quality, int(match))
        except ValueError:
            continue

    # Ensure well-known high-quality markers count even if "p" not present.
    if "uhd" in lower or "4k" in lower:
        quality = max(quality, 2160)

    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    for ratio in query.get("ratio", []):
        ratio_lower = ratio.lower()
        m = re.search(r'(\d{3,4})', ratio_lower)
        if m:
            quality = max(quality, int(m.group(1)))
        if "uhd" in ratio_lower or "4k" in ratio_lower:
            quality = max(quality, 2160)

    for fps_val in query.get("fps", []):
        if fps_val.isdigit():
            fps = max(fps, int(fps_val))
    for match in re.findall(r'fps[=:_-]?(\d{2,3})', lower):
        try:
            fps = max(fps, int(match))
        except ValueError:
            continue

    # Extract bitrate/bandwidth hints.
    for key in ("bitrate", "br", "bw", "bandwidth"):
        for value in query.get(key, []):
            m = re.search(r'(\d{3,7})', value)
            if m:
                bitrate = max(bitrate, int(m.group(1)))
    for match in re.findall(r'(?:bitrate|br|bw|bandwidth)[=:_-]?(\d{3,7})', lower):
        try:
            bitrate = max(bitrate, int(match))
        except ValueError:
            continue
    for match in re.findall(r'(\d{3,5})kbps', lower):
        try:
            bitrate = max(bitrate, int(match) * 1000)
        except ValueError:
            continue

    return quality, fps, bitrate

def pick_best_url(candidates, platform: str) -> Optional[str]:
    cleaned = []
    for u in candidates:
        if not u:
            continue
        u = html.unescape(u)
        u = u.replace("\\u002F", "/").replace("\\/", "/")
        u = DriverConfig.ensure_https(u)
        if not u.startswith("http"):
            continue
        cleaned.append(u)

    priorities = []
    for u in cleaned:
        score = 0
        if "playwm" in u or "watermark=1" in u or "wm=1" in u:
            score -= 20
        if platform == "tiktok":
            if any(k in u for k in ("v16", "v19", "v24", "tiktokcdn", "tiktokcdn-us")):
                score += 5
            if "/video/" in u or "/play/" in u:
                score += 3
        else:  # douyin
            if "douyin" in u and ("play" in u or "video" in u):
                score += 5
            if "/aweme/v1/play" in u or "video_id=" in u:
                score += 6
            if "play/" in u:
                score += 3
            if ".mp4" in u:
                score += 4
        if any(u.endswith(suf) for suf in (".html", "/", ".htm")):
            score -= 3
        if u.endswith(".mp4"):
            score += 2
        quality, fps, bitrate = _extract_quality_metrics(u)
        priorities.append(((quality, fps, bitrate, score), u))

    priorities.sort(key=lambda x: x[0], reverse=True)
    return priorities[0][1] if priorities else None
    
        
def sanitize_filename(name: str, max_len: int = 150) -> str:
    name = name.strip().replace("\n", " ")
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    name = re.sub(r"\s+", " ", name)
    return name[:max_len].strip()

def download_file(url: str, dest_path: str, referer: str, platform: str = ""):
    """강화된 파일 다운로드 함수"""
    print(f"[다운로드] 시작: {url[:100]}...")
    
    headers = DriverConfig.get_random_headers(mobile=(platform == "douyin"))
    headers.update({
        "Referer": referer or "",
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
    })

    # 다운로드 시도
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[다운로드] 시도 {attempt + 1}/{max_retries}")
            
            # 헤더를 매번 새로 생성 (안티봇 우회)
            if attempt > 0:
                headers = DriverConfig.get_random_headers(mobile=(platform == "douyin"))
                headers.update({
                    "Referer": referer or "",
                    "Accept": "*/*",
                    "Range": "bytes=0-",  # Range 헤더 추가
                })
                time.sleep(random.uniform(1, 3))  # 랜덤 대기
            
            req = Request(url, headers=headers)
            with urlopen(req, timeout=60) as resp, open(dest_path, "wb") as f:
                total_size = 0
                while True:
                    chunk = resp.read(1024 * 256)
                    if not chunk:
                        break
                    f.write(chunk)
                    total_size += len(chunk)
                
                print(f"[다운로드] 완료: {total_size} 바이트")
                
                # 파일 크기 검증
                if total_size < 1024:  # 1KB 미만이면 오류로 간주
                    raise Exception(f"파일이 너무 작습니다: {total_size} 바이트")
                
                return  # 성공
                
        except Exception as e:
            print(f"[다운로드] 시도 {attempt + 1} 실패: {str(e)}")
            if attempt < max_retries - 1:
                continue
            else:
                raise e
            
    
def extract_urls_from_text(text):
        import re
        
        urls = []
        
        # Douyin 단축 URL 패턴 - 특수문자 포함 처리
        # S_8XAH0PDaE/ 같은 형태를 정확히 매칭
        douyin_short_pattern = r'https://v\.douyin\.com/[A-Za-z0-9_\-]+/'
        matches = re.findall(douyin_short_pattern, text)
        urls.extend(matches)
        
        # 기타 Douyin 패턴들
        other_douyin_patterns = [
            r'https://www\.douyin\.com/video/\d+/?',
            r'https://www\.iesdouyin\.com/share/video/\d+/?',
        ]
        
        for pattern in other_douyin_patterns:
            matches = re.findall(pattern, text)
            urls.extend(matches)
        
        # TikTok URL 패턴
        tiktok_patterns = [
            r'https://vm\.tiktok\.com/[A-Za-z0-9_\-]+/',
            r'https://vt\.tiktok\.com/[A-Za-z0-9_\-]+/',
            r'https://www\.tiktok\.com/@[^/\s]+/video/\d+/?',
        ]
        
        for pattern in tiktok_patterns:
            matches = re.findall(pattern, text)
            urls.extend(matches)
        
        # 중복 제거
        cleaned_urls = []
        seen = set()
        for url in urls:
            if url not in seen:
                seen.add(url)
                cleaned_urls.append(url)
        
        print(f"[URL 추출] 찾은 URL: {cleaned_urls}")
        
        return cleaned_urls
    
def _clean_extracted_url(self, url):
        """추출된 URL 정리 - 슬래시 유지 수정"""
        if not url:
            return None
        
        url = url.strip()
        
        # URL 끝의 특수문자 제거 (슬래시는 제외!)
        url = re.sub(r'[^\w\-\./:?=&]+$', '', url)
        
        # 중국어 문자 제거
        url = re.sub(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]+.*$', '', url)
        
        # 공백 이후 제거
        url = url.split()[0] if ' ' in url else url
        
        # 불필요한 문자 제거 (슬래시는 보존!)
        url = url.rstrip('.,;!?')
        # url = url.rstrip('/')  # 이 줄 삭제!
        
        # https 확인
        if url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        elif not url.startswith('https://'):
            url = 'https://' + url
        
        return url
    
