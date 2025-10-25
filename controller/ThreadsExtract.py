"""
Threads video downloader helper.

This module fetches public Threads posts and saves the best available
video asset to disk.  Threads changes their internal GraphQL document
identifiers frequently, so the extractor attempts to discover the
current doc id straight from the page scripts before falling back to a
small list of known ids.
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, Iterable, List, Optional, Tuple, Union
from urllib.parse import urlparse, urlunparse

import requests
from requests.cookies import CookieConflictError


MOBILE_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
)

# Known doc ids observed in the wild.  These are used only as a last
# resort – the extractor prefers to scrape the current value from the
# served JavaScript.
FALLBACK_DOC_IDS: Tuple[str, ...] = (
    "24853561097640514",
    "9157002887897348",
    "8845759202181306",
    "9984228236336116",
    "27065904006207281",
    "26945569808375322",
    "8183567811717284",
    "6974099682683103",
)

# Patterns that commonly wrap the post detail query id.
DOC_ID_PATTERNS: Tuple[re.Pattern, ...] = (
    re.compile(
        r"BarcelonaPostPage(?:Direct)?Query_threadsRelayOperation\".*?e\.exports=\"(\d+)\""
    ),
    re.compile(
        r"PostAppThreadQuery_threadsRelayOperation\".*?e\.exports=\"(\d+)\""
    ),
    re.compile(
        r"BarcelonaPostPageQuery.*?doc_id[\"']?\s*:\s*[\"'](\d+)[\"']"
    ),
    re.compile(
        r"threadsRelayOperation.*?\"(\d{15,})\""
    ),
    re.compile(
        r"doc_id[\"']?\s*:\s*[\"'](\d{15,})[\"']"
    ),
)

SHORTCODE_RE = re.compile(
    r"(?:threads\.net|threads\.com)/(?:@[\w\.\-]+/)?(?:post|status)/([A-Za-z0-9_\-]+)"
)
LSD_TOKEN_RE = re.compile(r'"LSD",\s*\[\],\s*\{"token":"([^"]+)"\}')
STREAM_CHUNK = 1 << 16  # 64 KiB


class ThreadsDownloadError(RuntimeError):
    """Raised when the Threads extractor cannot obtain or save media."""


def _extract_shortcode(url: str) -> str:
    match = SHORTCODE_RE.search(url)
    if not match:
        raise ThreadsDownloadError("Unsupported Threads url format.")
    return match.group(1)


def _get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": MOBILE_USER_AGENT,
            "Accept-Language": "en-US,en;q=0.8",
        }
    )
    return session


def _fetch_html(session: requests.Session, url: str, max_retries: int = 3) -> str:
    last_error = None
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=20)
            if resp.status_code >= 400:
                last_error = ThreadsDownloadError(f"Threads returned HTTP {resp.status_code}.")
                if attempt < max_retries - 1:
                    continue
                raise last_error
            return resp.text
        except requests.RequestException as exc:
            last_error = ThreadsDownloadError(f"Request failed: {exc}")
            if attempt < max_retries - 1:
                continue
            raise last_error
    raise last_error or ThreadsDownloadError("Failed to fetch HTML")


def _extract_lsd_token(html: str) -> str:
    match = LSD_TOKEN_RE.search(html)
    if not match:
        raise ThreadsDownloadError("Could not locate LSD token in Threads markup.")
    return match.group(1)


def _iter_scripts(html: str) -> Iterable[str]:
    for script_match in re.finditer(r'<script[^>]+src="([^"]+)"', html):
        yield script_match.group(1)


def _download_script(session: requests.Session, url: str) -> Optional[str]:
    try:
        resp = session.get(url, timeout=15)
        if resp.status_code >= 400:
            return None
        return resp.text
    except requests.RequestException:
        return None


def _discover_doc_ids(session: requests.Session, html: str) -> List[str]:
    discovered: List[str] = []
    for script_url in _iter_scripts(html):
        script_body = _download_script(session, script_url)
        if not script_body:
            continue
        for pattern in DOC_ID_PATTERNS:
            for match in pattern.finditer(script_body):
                doc_id = match.group(1)
                if doc_id not in discovered:
                    discovered.append(doc_id)
        if discovered:
            break
    return discovered


def _collect_candidate_doc_ids(
    session: requests.Session, html: str
) -> List[str]:
    doc_ids = _discover_doc_ids(session, html)
    for fallback in FALLBACK_DOC_IDS:
        if fallback not in doc_ids:
            doc_ids.append(fallback)
    return doc_ids


def _post_graphql(
    session: requests.Session,
    url: str,
    lsd_token: str,
    doc_id: str,
    shortcode: str,
    max_retries: int = 2,
) -> Dict[str, Union[dict, list, str]]:
    try:
        csrf_token = session.cookies.get("csrftoken") or ""
    except CookieConflictError:
        csrf_token = session.cookies.get_dict().get("csrftoken", "") or ""

    headers = {
        "User-Agent": MOBILE_USER_AGENT,
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-FB-LSD": lsd_token,
        "X-IG-App-ID": "238260118697367",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf_token,
        "Origin": "https://www.threads.net",
        "Referer": url,
    }
    payload = {
        "lsd": lsd_token,
        "doc_id": doc_id,
        "variables": json.dumps({"postID": shortcode}),
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            resp = session.post(
                "https://www.threads.net/api/graphql", headers=headers, data=payload, timeout=20
            )
            if resp.status_code >= 400:
                last_error = ThreadsDownloadError(
                    f"GraphQL query failed (doc_id={doc_id}, status={resp.status_code})."
                )
                if attempt < max_retries - 1:
                    continue
                raise last_error

            if "application/json" not in (resp.headers.get("content-type") or ""):
                last_error = ThreadsDownloadError("Unable to access Threads API (unexpected response).")
                if attempt < max_retries - 1:
                    continue
                raise last_error

            try:
                return resp.json()
            except ValueError as exc:
                last_error = ThreadsDownloadError("Unexpected response while decoding GraphQL data.")
                if attempt < max_retries - 1:
                    continue
                raise last_error from exc
        except requests.RequestException as exc:
            last_error = ThreadsDownloadError(f"GraphQL request failed: {exc}")
            if attempt < max_retries - 1:
                continue
            raise last_error

    raise last_error or ThreadsDownloadError("GraphQL query failed")


def _flatten(node: Union[Dict, List]) -> Iterable[Union[Dict, List]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from _flatten(value)
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                yield from _flatten(item)


def _pick_best_video_url(payload: Dict[str, Union[dict, list, str]]) -> Optional[str]:
    """Extract the best video URL from GraphQL payload."""
    best_url = None

    # Look for video_versions in the payload
    for node in _flatten(payload):
        if isinstance(node, dict):
            # Check for video_versions
            if "video_versions" in node:
                versions = node["video_versions"]
                if isinstance(versions, list) and versions:
                    sorted_versions = sorted(
                        (v for v in versions if isinstance(v, dict) and v.get("url")),
                        key=lambda item: item.get("width", 0) or 0,
                        reverse=True,
                    )
                    if sorted_versions:
                        return sorted_versions[0]["url"]

            # Check for video_url field directly
            if "video_url" in node and node["video_url"]:
                return node["video_url"]

            # Check for playback_url
            if "playback_url" in node and node["playback_url"]:
                return node["playback_url"]

            # Check for dash_manifest or other video indicators
            if "dash_manifest" in node and "video_dash_manifest" in node:
                manifest = node.get("video_dash_manifest")
                if manifest:
                    # Try to extract URL from manifest
                    url_match = re.search(r'<BaseURL>([^<]+)</BaseURL>', str(manifest))
                    if url_match:
                        return url_match.group(1)

    return best_url


def _download_binary(session: requests.Session, url: str, target_path: str, max_retries: int = 3) -> str:
    last_error = None
    for attempt in range(max_retries):
        try:
            with session.get(url, stream=True, timeout=30) as resp:
                if resp.status_code >= 400:
                    last_error = ThreadsDownloadError(
                        f"Failed to download media asset ({resp.status_code})."
                    )
                    if attempt < max_retries - 1:
                        continue
                    raise last_error
                with open(target_path, "wb") as handle:
                    for chunk in resp.iter_content(STREAM_CHUNK):
                        if chunk:
                            handle.write(chunk)
            return target_path
        except requests.RequestException as exc:
            last_error = ThreadsDownloadError(f"Download failed: {exc}")
            if attempt < max_retries - 1:
                continue
            raise last_error
    raise last_error or ThreadsDownloadError("Failed to download media")


def _clean_media_url(url: str) -> str:
    trimmed = url.strip().strip("[]()")
    trimmed = trimmed.replace("\\/", "/")
    trimmed = trimmed.replace("\\u0026", "&").replace("\\u003d", "=")
    return trimmed


def _prepare_output_path(
    shortcode: str,
    output_dir: Optional[str],
    media_url: str,
    default_extension: str,
) -> str:
    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    parsed = urlparse(media_url)
    ext = os.path.splitext(parsed.path)[1]
    if not ext or len(ext) > 5:
        ext = default_extension

    base_path = os.path.join(output_dir, f"threads_{shortcode}")
    candidate = f"{base_path}{ext}"
    counter = 1
    while os.path.exists(candidate):
        candidate = f"{base_path}_{counter}{ext}"
        counter += 1
    return candidate


def _download_and_save(
    media_url: str,
    shortcode: str,
    output_dir: Optional[str],
    default_extension: str,
    session: Optional[requests.Session] = None,
) -> str:
    target_path = _prepare_output_path(shortcode, output_dir, media_url, default_extension)
    session_to_use = session or requests.Session()
    session_to_use.headers.setdefault("User-Agent", MOBILE_USER_AGENT)
    return _download_binary(session_to_use, media_url, target_path)


def _download_via_selenium(
    canonical_url: str,
    shortcode: str,
    output_dir: Optional[str],
) -> str:
    """Extract video using Selenium (browser automation)"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        import time

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(canonical_url)
        time.sleep(5)  # Wait for page load

        # Try to find video element
        video_elements = driver.find_elements(By.TAG_NAME, "video")
        if video_elements:
            for video in video_elements:
                src = video.get_attribute("src")
                if src and ("cdninstagram.com" in src or ".mp4" in src):
                    driver.quit()
                    return _download_and_save(src, shortcode, output_dir, ".mp4")

        # Fallback: search page source for mp4 URLs
        page_source = driver.page_source
        mp4_urls = re.findall(r'https://[^\s"\'<>]+\.mp4[^\s"\'<>]*', page_source)
        driver.quit()

        if mp4_urls:
            # Get the first CDN URL (usually the video)
            for url in mp4_urls:
                if "cdninstagram.com" in url:
                    clean_url = _clean_media_url(url)
                    return _download_and_save(clean_url, shortcode, output_dir, ".mp4")

        raise ThreadsDownloadError("Selenium: No video found in page")

    except ImportError:
        raise ThreadsDownloadError("Selenium not installed. Install with: pip install selenium")
    except Exception as exc:
        raise ThreadsDownloadError(f"Selenium extraction failed: {exc}")


def _download_via_jina(
    canonical_url: str,
    shortcode: str,
    output_dir: Optional[str],
) -> str:
    jina_url = f"https://r.jina.ai/{canonical_url}"
    try:
        resp = requests.get(jina_url, timeout=15)
    except requests.RequestException as exc:
        raise ThreadsDownloadError("Fallback fetch failed.") from exc

    if resp.status_code >= 400:
        raise ThreadsDownloadError(
            f"Fallback fetch failed with status {resp.status_code}."
        )

    text = resp.text

    mp4_candidates = re.findall(r"\((https://[^)]+\.mp4[^)]*)\)", text)
    if not mp4_candidates:
        mp4_candidates = re.findall(r"(https://[^\s)]+\.mp4[^\s)]*)", text)

    if mp4_candidates:
        media_url = _clean_media_url(mp4_candidates[0])
        return _download_and_save(media_url, shortcode, output_dir, ".mp4")

    image_candidates = re.findall(
        r"\((https://[^)]+\.(?:jpg|jpeg|png)[^)]*)\)", text, flags=re.IGNORECASE
    )
    if not image_candidates:
        image_candidates = re.findall(
            r"(https://[^\s)]+\.(?:jpg|jpeg|png)[^\s)]*)", text, flags=re.IGNORECASE
        )

    if image_candidates:
        media_url = _clean_media_url(image_candidates[0])
        return _download_and_save(media_url, shortcode, output_dir, ".jpg")

    raise ThreadsDownloadError("Fallback extraction did not locate media.")


def download_threads_video(url: str, output_dir: Optional[str] = None) -> str:
    """
    Download a Threads post (video) to *output_dir* and return the saved path.
    Raises ThreadsDownloadError on failure.
    """

    shortcode = _extract_shortcode(url)
    parsed_url = urlparse(url)
    canonical_url = urlunparse(
        (
            "https",
            "www.threads.net",
            parsed_url.path or "",
            "",
            parsed_url.query or "",
            "",
        )
    )
    session = _get_session()

    html = _fetch_html(session, canonical_url)
    lsd_token = _extract_lsd_token(html)

    candidate_doc_ids = _collect_candidate_doc_ids(session, html)
    if not candidate_doc_ids:
        raise ThreadsDownloadError("Could not locate a usable GraphQL doc id.")

    graph_payload: Optional[Dict[str, Union[dict, list, str]]] = None
    last_error: Optional[Exception] = None
    for doc_id in candidate_doc_ids:
        try:
            graph_payload = _post_graphql(session, canonical_url, lsd_token, doc_id, shortcode)
            if graph_payload:
                break
        except ThreadsDownloadError as exc:
            last_error = exc
            continue

    if not graph_payload:
        # Try Selenium first, then Jina
        try:
            return _download_via_selenium(canonical_url, shortcode, output_dir)
        except ThreadsDownloadError:
            try:
                return _download_via_jina(canonical_url, shortcode, output_dir)
            except ThreadsDownloadError:
                if last_error:
                    raise ThreadsDownloadError(str(last_error))
                raise

    video_url = _pick_best_video_url(graph_payload)
    if not video_url:
        # Try Selenium first, then Jina
        try:
            return _download_via_selenium(canonical_url, shortcode, output_dir)
        except ThreadsDownloadError:
            return _download_via_jina(canonical_url, shortcode, output_dir)

    return _download_and_save(video_url, shortcode, output_dir, ".mp4", session=session)


__all__ = ["download_threads_video", "ThreadsDownloadError"]
