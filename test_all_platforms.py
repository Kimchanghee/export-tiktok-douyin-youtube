"""
Test script for downloading videos from multiple platforms
"""

import os
import sys
import shutil
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.ThreadsExtract import download_threads_video
from controller.DouyinExtract import download_tiktok_douyin_video


def download_youtube_video(url, output_dir):
    """Download YouTube video using yt-dlp"""
    print(f"\n[YouTube] Downloading: {url}")

    # Create filename template
    timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
    output_template = os.path.join(output_dir, f"youtube_{timestamp}.%(ext)s")

    try:
        # Use yt-dlp to download
        cmd = [
            "yt-dlp",
            "-f", "best",
            "-o", output_template,
            url
        ]

        print(f"[YouTube] Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            # Find the downloaded file
            for file in os.listdir(output_dir):
                if file.startswith(f"youtube_{timestamp}"):
                    filepath = os.path.join(output_dir, file)
                    print(f"[YouTube] Downloaded to: {filepath}")
                    return filepath
            raise Exception("Downloaded file not found")
        else:
            raise Exception(f"yt-dlp failed: {result.stderr}")

    except Exception as e:
        print(f"[YouTube] Error: {str(e)}")
        raise


def test_url(platform, url, download_func, output_dir, needs_output_dir=True):
    """Test a single URL download"""
    print("\n" + "="*80)
    print(f"Testing {platform}")
    print("="*80)
    print(f"URL: {url}")

    try:
        # Call function based on whether it needs output_dir
        if needs_output_dir:
            filepath = download_func(url, output_dir)
        else:
            # For Douyin, function returns temp path
            filepath = download_func(url)

        # For Douyin, copy from temp to output_dir if needed
        if platform == "Douyin" and filepath and os.path.exists(filepath):
            filename = os.path.basename(filepath)
            dest_path = os.path.join(output_dir, filename)
            if filepath != dest_path:
                shutil.copy2(filepath, dest_path)
                print(f"[Douyin] Copied to: {dest_path}")
                filepath = dest_path

        if filepath and os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"[SUCCESS] Downloaded to: {filepath}")
            print(f"[SUCCESS] File size: {size:,} bytes ({size/1024/1024:.2f} MB)")
            return True
        else:
            print(f"[ERROR] File not found: {filepath}")
            return False

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Multi-Platform Video Download Test")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), "test_downloads")
    os.makedirs(output_dir, exist_ok=True)

    tests = [
        ("YouTube Shorts", "https://www.youtube.com/shorts/Fm__4qtSc1g", download_youtube_video, True),
        ("Threads", "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1", download_threads_video, True),
        ("YouTube", "https://youtu.be/He9Uu7ngRks?si=F9f-MIs5GTH0os1N", download_youtube_video, True),
        ("Douyin", "https://v.douyin.com/HsYBBBn3WIU/", download_tiktok_douyin_video, False)
    ]

    results = {}

    for platform, url, func, needs_output_dir in tests:
        results[platform] = test_url(platform, url, func, output_dir, needs_output_dir)

    print("\n" + "="*80)
    print("Test Results Summary")
    print("="*80)
    for platform, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{platform}: {status}")
    print("="*80)

    # Exit with error code if any test failed
    if not all(results.values()):
        print("\nSome tests failed. Will retry failed tests...")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)
