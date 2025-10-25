"""
Test Jina fallback for Threads
"""

import sys
import os
import re
import requests

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_jina():
    url = "https://www.threads.com/@fig080/post/DQGf4IQEomg"
    jina_url = f"https://r.jina.ai/{url}"

    print(f"🔍 Testing Jina fallback")
    print(f"Original URL: {url}")
    print(f"Jina URL: {jina_url}")
    print("-" * 60)

    try:
        print(f"\n📤 Fetching from Jina...")
        resp = requests.get(jina_url, timeout=30)

        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        print(f"Content length: {len(resp.text)} chars")

        # Save response
        output_file = "jina_response.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"💾 Saved response to: {output_file}")

        # Look for video URLs
        print(f"\n🔎 Looking for video URLs...")
        mp4_candidates = re.findall(r"\((https://[^)]+\.mp4[^)]*)\)", resp.text)
        if not mp4_candidates:
            mp4_candidates = re.findall(r"(https://[^\s)]+\.mp4[^\s)]*)", resp.text)

        if mp4_candidates:
            print(f"🎥 Found {len(mp4_candidates)} MP4 URLs:")
            for i, url in enumerate(mp4_candidates[:5], 1):
                clean_url = url.strip().strip("[]()")
                clean_url = clean_url.replace("\\/", "/")
                print(f"   {i}. {clean_url[:100]}...")
        else:
            print(f"⚠️ No MP4 URLs found")

        # Look for image URLs
        print(f"\n🔎 Looking for image URLs...")
        image_candidates = re.findall(
            r"\((https://[^)]+\.(?:jpg|jpeg|png)[^)]*)\)", resp.text, flags=re.IGNORECASE
        )
        if not image_candidates:
            image_candidates = re.findall(
                r"(https://[^\s)]+\.(?:jpg|jpeg|png)[^\s)]*)", resp.text, flags=re.IGNORECASE
            )

        if image_candidates:
            print(f"🖼️ Found {len(image_candidates)} image URLs:")
            for i, url in enumerate(image_candidates[:5], 1):
                clean_url = url.strip().strip("[]()")
                clean_url = clean_url.replace("\\/", "/")
                print(f"   {i}. {clean_url[:100]}...")
        else:
            print(f"⚠️ No image URLs found")

        # Look for any media references
        print(f"\n🔎 Looking for media keywords...")
        if "video" in resp.text.lower():
            video_count = resp.text.lower().count("video")
            print(f"   'video' mentioned {video_count} times")
        if ".mp4" in resp.text.lower():
            mp4_count = resp.text.lower().count(".mp4")
            print(f"   '.mp4' mentioned {mp4_count} times")

        # Show sample of text
        print(f"\n📄 First 1000 chars of response:")
        print(resp.text[:1000])

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jina()
