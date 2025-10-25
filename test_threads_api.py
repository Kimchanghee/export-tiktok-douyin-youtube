"""
Try different Threads extraction methods
"""

import sys
import os
import requests
import json
import re

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def method_1_oembed():
    """Try oEmbed API"""
    url = "https://www.threads.net/@fig080/post/DQGf4IQEomg"
    oembed_url = f"https://www.threads.net/oembed?url={url}"

    print(f"Method 1: oEmbed API")
    print(f"URL: {oembed_url}")

    try:
        resp = requests.get(oembed_url, timeout=15)
        print(f"Status: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print(f"Response keys: {list(data.keys())}")
            print(json.dumps(data, indent=2, ensure_ascii=False))

            with open("oembed_response.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to oembed_response.json")
        else:
            print(f"Failed: {resp.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

    print("-" * 70)

def method_2_instagram_graph():
    """Try Instagram Graph API approach"""
    url = "https://www.threads.net/@fig080/post/DQGf4IQEomg"
    shortcode = "DQGf4IQEomg"

    # Try Instagram's embed endpoint (Threads is part of Instagram)
    embed_url = f"https://www.instagram.com/p/{shortcode}/embed/"

    print(f"\nMethod 2: Instagram Embed")
    print(f"URL: {embed_url}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(embed_url, headers=headers, timeout=15)
        print(f"Status: {resp.status_code}")

        if resp.status_code == 200:
            html = resp.text

            # Look for video URL in embed
            video_patterns = [
                r'"video_url":"([^"]+)"',
                r'<video[^>]+src="([^"]+)"',
                r'"playback_url":"([^"]+)"',
            ]

            for pattern in video_patterns:
                matches = re.findall(pattern, html)
                if matches:
                    print(f"✅ Found video URL: {matches[0]}")
                    break
            else:
                print(f"No video found in embed")

            with open("instagram_embed.html", "w", encoding="utf-8") as f:
                f.write(html)
            print(f"💾 Saved to instagram_embed.html")
    except Exception as e:
        print(f"Error: {e}")

    print("-" * 70)

def method_3_direct_api():
    """Try Threads' internal API directly"""
    shortcode = "DQGf4IQEomg"

    print(f"\nMethod 3: Direct API with different endpoints")

    endpoints = [
        f"https://www.threads.net/api/v1/media/{shortcode}/info/",
        f"https://www.threads.net/api/v1/posts/{shortcode}/",
        f"https://i.instagram.com/api/v1/media/{shortcode}/info/",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36",
        "X-IG-App-ID": "238260118697367",
        "Accept": "application/json",
    }

    for endpoint in endpoints:
        print(f"\nTrying: {endpoint}")
        try:
            resp = requests.get(endpoint, headers=headers, timeout=15)
            print(f"Status: {resp.status_code}")
            print(f"Content-Type: {resp.headers.get('content-type')}")

            if resp.status_code == 200 and 'json' in resp.headers.get('content-type', ''):
                data = resp.json()
                print(f"Keys: {list(data.keys())}")

                filename = f"api_response_{endpoint.split('/')[-2]}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved to {filename}")
        except Exception as e:
            print(f"Error: {e}")

    print("-" * 70)

def method_4_mobile_web():
    """Try mobile web version"""
    url = "https://www.threads.net/@fig080/post/DQGf4IQEomg"

    print(f"\nMethod 4: Mobile Web")

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {resp.status_code}")

        html = resp.text
        with open("mobile_web.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"💾 Saved to mobile_web.html ({len(html)} bytes)")

        # Look for video URLs
        video_urls = re.findall(r'https://[^\s"\'<>]+\.mp4[^\s"\'<>]*', html)
        if video_urls:
            print(f"✅ Found {len(video_urls)} video URLs:")
            for url in video_urls[:5]:
                print(f"   - {url[:100]}")
        else:
            print(f"No .mp4 URLs found")

    except Exception as e:
        print(f"Error: {e}")

    print("-" * 70)

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Different Threads Extraction Methods")
    print("=" * 70)

    method_1_oembed()
    method_2_instagram_graph()
    method_3_direct_api()
    method_4_mobile_web()

    print("\n" + "=" * 70)
    print("All methods tested. Check the generated files for details.")
    print("=" * 70)
