"""
Debug Threads video downloader - shows raw data
"""

import sys
import os
import json

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
    _post_graphql,
    _pick_best_video_url,
    ThreadsDownloadError
)
from urllib.parse import urlparse, urlunparse

def debug_threads():
    url = "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"

    print(f"🔍 Debugging Threads URL: {url}")
    print("-" * 60)

    try:
        # Extract shortcode
        shortcode = _extract_shortcode(url)
        print(f"✅ Shortcode: {shortcode}")

        # Prepare canonical URL
        parsed_url = urlparse(url)
        canonical_url = urlunparse(
            ("https", "www.threads.net", parsed_url.path or "", "", parsed_url.query or "", "")
        )
        print(f"✅ Canonical URL: {canonical_url}")

        # Get session
        session = _get_session()
        print(f"✅ Session created")

        # Fetch HTML
        print(f"\n🌐 Fetching HTML...")
        html = _fetch_html(session, canonical_url)
        print(f"✅ HTML fetched ({len(html)} bytes)")

        # Extract LSD token
        lsd_token = _extract_lsd_token(html)
        print(f"✅ LSD Token: {lsd_token[:20]}...")

        # Collect doc IDs
        print(f"\n🔎 Collecting doc IDs...")
        candidate_doc_ids = _collect_candidate_doc_ids(session, html)
        print(f"✅ Found {len(candidate_doc_ids)} doc IDs:")
        for i, doc_id in enumerate(candidate_doc_ids, 1):
            print(f"   {i}. {doc_id}")

        # Try each doc ID
        print(f"\n📡 Trying GraphQL queries...")
        for i, doc_id in enumerate(candidate_doc_ids, 1):
            try:
                print(f"\n--- Attempt {i}: doc_id={doc_id} ---")
                graph_payload = _post_graphql(session, canonical_url, lsd_token, doc_id, shortcode)

                if graph_payload:
                    print(f"✅ GraphQL query succeeded!")

                    # Save raw response for inspection
                    debug_file = f"threads_debug_response_{i}.json"
                    with open(debug_file, "w", encoding="utf-8") as f:
                        json.dump(graph_payload, f, indent=2, ensure_ascii=False)
                    print(f"💾 Saved raw response to: {debug_file}")

                    # Try to find video URL
                    video_url = _pick_best_video_url(graph_payload)
                    if video_url:
                        print(f"🎥 FOUND VIDEO URL: {video_url[:100]}...")
                        return True
                    else:
                        print(f"⚠️ No video URL found in response")
                        # Show some data structure info
                        print(f"📊 Response structure:")
                        print(f"   Keys: {list(graph_payload.keys())}")

                        # Look for media indicators
                        def find_media_keys(obj, path=""):
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    new_path = f"{path}.{key}" if path else key
                                    if any(keyword in key.lower() for keyword in ['video', 'media', 'playback', 'url', 'image']):
                                        print(f"   Found key: {new_path} = {type(value).__name__}")
                                    if isinstance(value, (dict, list)):
                                        find_media_keys(value, new_path)
                            elif isinstance(obj, list):
                                for idx, item in enumerate(obj):
                                    if isinstance(item, (dict, list)):
                                        find_media_keys(item, f"{path}[{idx}]")

                        find_media_keys(graph_payload)

            except ThreadsDownloadError as e:
                print(f"❌ Failed: {e}")
                continue

        print(f"\n⚠️ All doc IDs exhausted, no video found")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_threads()
    sys.exit(0 if success else 1)
