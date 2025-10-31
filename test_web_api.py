"""
Test script for web API with all video URLs
"""

import requests
import time
import os
import sys

# Base URL for the web API
BASE_URL = "http://localhost:8081"

def test_download(platform_name, url, retry_count=3):
    """Test downloading a video via web API"""
    print("\n" + "="*80)
    print(f"Testing {platform_name}")
    print("="*80)
    print(f"URL: {url}")

    for attempt in range(retry_count):
        try:
            print(f"\nAttempt {attempt + 1}/{retry_count}")

            # Step 1: Request download
            print("[1/3] Requesting download...")
            response = requests.post(
                f"{BASE_URL}/api/download",
                json={"url": url},
                timeout=300
            )

            if response.status_code != 200:
                print(f"[ERROR] Download request failed: {response.status_code}")
                print(f"Response: {response.text}")
                if attempt < retry_count - 1:
                    print("Retrying...")
                    time.sleep(2)
                    continue
                return False

            data = response.json()
            print(f"[SUCCESS] Download info received")
            print(f"Platform: {data.get('platform')}")
            print(f"Filename: {data.get('filename')}")
            print(f"Size: {data.get('size'):,} bytes ({data.get('size')/1024/1024:.2f} MB)")

            # Step 2: Download the file
            download_url = f"{BASE_URL}{data.get('download_url')}"
            print(f"\n[2/3] Downloading file from: {download_url}")

            file_response = requests.get(download_url, timeout=300, stream=True)

            if file_response.status_code != 200:
                print(f"[ERROR] File download failed: {file_response.status_code}")
                if attempt < retry_count - 1:
                    print("Retrying...")
                    time.sleep(2)
                    continue
                return False

            # Step 3: Save file locally
            output_dir = os.path.join(os.path.dirname(__file__), "test_downloads_web")
            os.makedirs(output_dir, exist_ok=True)

            filename = data.get('filename')
            local_path = os.path.join(output_dir, filename)

            print(f"[3/3] Saving to: {local_path}")

            downloaded_size = 0
            with open(local_path, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

            actual_size = os.path.getsize(local_path)
            print(f"\n[SUCCESS] File saved successfully!")
            print(f"Downloaded size: {downloaded_size:,} bytes")
            print(f"File size on disk: {actual_size:,} bytes ({actual_size/1024/1024:.2f} MB)")
            print(f"Location: {local_path}")

            # Verify file is not empty
            if actual_size < 1000:
                print(f"[WARNING] File is suspiciously small: {actual_size} bytes")
                if attempt < retry_count - 1:
                    print("Retrying...")
                    os.remove(local_path)
                    time.sleep(2)
                    continue
                return False

            return True

        except requests.exceptions.Timeout:
            print(f"[ERROR] Request timeout")
            if attempt < retry_count - 1:
                print("Retrying...")
                time.sleep(2)
                continue
            return False

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
            if attempt < retry_count - 1:
                print("Retrying...")
                time.sleep(2)
                continue
            return False

    return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Web API Video Download Test")
    print("="*80)
    print(f"Testing against: {BASE_URL}")

    # Test if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Server is running")
        else:
            print(f"[WARNING] Server responded with status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Cannot connect to server: {e}")
        print("Please start the web server first with: python web/app.py")
        sys.exit(1)

    # All test URLs
    tests = [
        ("YouTube Shorts", "https://www.youtube.com/shorts/Fm__4qtSc1g"),
        ("Threads", "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"),
        ("YouTube", "https://youtu.be/He9Uu7ngRks?si=F9f-MIs5GTH0os1N"),
        ("Douyin", "https://v.douyin.com/HsYBBBn3WIU/"),
        ("X/Twitter", "https://x.com/elonmusk/status/1983810924386644306"),
        ("Instagram", "https://www.instagram.com/p/DQcJ-QYCU2x/"),
        ("TikTok", "https://www.tiktok.com/@tikdoktic/video/7564394978043022609?is_from_webapp=1&sender_device=pc")
    ]

    results = {}

    for platform_name, url in tests:
        results[platform_name] = test_download(platform_name, url)
        time.sleep(1)  # Brief pause between tests

    print("\n" + "="*80)
    print("Test Results Summary")
    print("="*80)
    for platform_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{platform_name}: {status}")
    print("="*80)

    # Exit with error code if any test failed
    if not all(results.values()):
        print("\nSome tests failed!")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)
