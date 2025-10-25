"""
Parse Threads HTML directly to find video
"""

import sys
import os
import re
import json

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.ThreadsExtract import _get_session, _fetch_html

def find_video_in_html():
    url = "https://www.threads.net/@fig080/post/DQGf4IQEomg"

    print(f"🔍 Fetching and parsing Threads HTML...")
    print(f"URL: {url}")
    print("-" * 70)

    session = _get_session()
    html = _fetch_html(session, url)

    print(f"✅ HTML fetched ({len(html)} bytes)")

    # Save HTML for inspection
    with open("threads_html.txt", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 Saved HTML to threads_html.txt")

    # Look for various video URL patterns
    patterns = [
        (r'video_url["\']\s*:\s*["\']([^"\']+)', "video_url in JSON"),
        (r'playback_url["\']\s*:\s*["\']([^"\']+)', "playback_url in JSON"),
        (r'"video_versions":\s*\[(.*?)\]', "video_versions array"),
        (r'https://[^\s"\'<>]+\.mp4[^\s"\'<>]*', "direct .mp4 URL"),
        (r'https://[^\s"\'<>]+/video[^\s"\'<>]*', "URL with /video/"),
        (r'"dash_manifest":\s*"([^"]+)"', "dash_manifest"),
        (r'src=["\'](https://[^"\']+\.mp4[^"\']*)', "src attribute mp4"),
        (r'<video[^>]+src=["\'](https://[^"\']+)', "video tag src"),
        (r'cdninstagram\.com/[^\s"\'<>]+\.mp4', "Instagram CDN mp4"),
        (r'scontent[^\s"\'<>]+\.mp4', "scontent mp4"),
    ]

    print(f"\n🔎 Searching for video URLs...\n")

    found_anything = False
    for pattern, description in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        if matches:
            found_anything = True
            print(f"✅ Found via '{description}':")
            for i, match in enumerate(matches[:5], 1):
                # Clean up the match
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                match_clean = match.replace('\\/', '/').replace('\\u0026', '&')
                match_clean = match_clean.strip()[:200]
                print(f"   {i}. {match_clean}")
            print()

    if not found_anything:
        print(f"❌ No video URLs found with standard patterns")
        print(f"\n🔎 Looking for any media-related data...")

        # Look for __NEXT_DATA__ or similar embedded JSON
        json_patterns = [
            r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>',
            r'window\.__NEXT_DATA__\s*=\s*(\{.*?\});',
            r'window\._sharedData\s*=\s*(\{.*?\});',
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            if matches:
                print(f"\n✅ Found embedded JSON data ({len(matches)} blocks)")
                for i, json_str in enumerate(matches[:3], 1):
                    try:
                        data = json.loads(json_str)
                        with open(f"threads_json_block_{i}.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"   💾 Saved to threads_json_block_{i}.json")

                        # Search for video in JSON
                        def search_video(obj, path=""):
                            results = []
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    if any(k in key.lower() for k in ['video', 'playback', 'media']):
                                        results.append(f"{path}.{key}: {type(value).__name__}")
                                    if isinstance(value, str) and ('.mp4' in value or 'video' in value):
                                        results.append(f"{path}.{key} = {value[:100]}")
                                    if isinstance(value, (dict, list)):
                                        results.extend(search_video(value, f"{path}.{key}"))
                            elif isinstance(obj, list):
                                for idx, item in enumerate(obj):
                                    if isinstance(item, (dict, list)):
                                        results.extend(search_video(item, f"{path}[{idx}]"))
                            return results

                        video_refs = search_video(data)
                        if video_refs:
                            print(f"   🎥 Video-related fields found:")
                            for ref in video_refs[:10]:
                                print(f"      - {ref}")
                    except json.JSONDecodeError:
                        print(f"   ⚠️ Block {i} is not valid JSON")
                        continue

if __name__ == "__main__":
    find_video_in_html()
