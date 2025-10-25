"""
Debug Threads - check GraphQL response details
"""

import sys
import os
import json
import requests

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.ThreadsExtract import (
    _extract_shortcode,
    _get_session,
    _fetch_html,
    _extract_lsd_token,
    _collect_candidate_doc_ids,
    MOBILE_USER_AGENT,
    ThreadsDownloadError
)
from requests.cookies import CookieConflictError
from urllib.parse import urlparse, urlunparse

def debug_graphql_response():
    url = "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"

    print(f"🔍 Debugging GraphQL Response")
    print("-" * 60)

    try:
        shortcode = _extract_shortcode(url)
        parsed_url = urlparse(url)
        canonical_url = urlunparse(
            ("https", "www.threads.net", parsed_url.path or "", "", parsed_url.query or "", "")
        )

        session = _get_session()
        html = _fetch_html(session, canonical_url)
        lsd_token = _extract_lsd_token(html)
        candidate_doc_ids = _collect_candidate_doc_ids(session, html)

        print(f"Testing with first doc_id: {candidate_doc_ids[0]}")

        # Manual GraphQL request with detailed logging
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
            "Referer": canonical_url,
        }

        payload = {
            "lsd": lsd_token,
            "doc_id": candidate_doc_ids[0],
            "variables": json.dumps({"postID": shortcode}),
        }

        print(f"\n📤 Sending GraphQL request...")
        print(f"URL: https://www.threads.net/api/graphql")
        print(f"Headers: {json.dumps({k: v[:50] if len(str(v)) > 50 else v for k, v in headers.items()}, indent=2)}")

        resp = session.post(
            "https://www.threads.net/api/graphql",
            headers=headers,
            data=payload,
            timeout=20
        )

        print(f"\n📥 Response received:")
        print(f"Status Code: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        print(f"Content-Length: {len(resp.content)} bytes")

        # Try to save raw response
        raw_file = "threads_raw_response.txt"
        with open(raw_file, "wb") as f:
            f.write(resp.content)
        print(f"💾 Saved raw response to: {raw_file}")

        # Check if it's HTML (redirect or error page)
        if "text/html" in resp.headers.get('content-type', ''):
            print(f"\n⚠️ Response is HTML, not JSON!")
            print(f"First 500 chars:")
            print(resp.text[:500])
        elif "application/json" in resp.headers.get('content-type', ''):
            print(f"\n✅ Response is JSON")
            try:
                data = resp.json()
                json_file = "threads_json_response.json"
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved JSON response to: {json_file}")
                print(f"Keys: {list(data.keys())}")
            except Exception as e:
                print(f"❌ Failed to parse JSON: {e}")
        else:
            print(f"\n⚠️ Unknown content type")
            print(f"First 500 chars:")
            print(resp.text[:500])

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_graphql_response()
