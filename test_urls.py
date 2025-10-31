"""
Test script for multiple platform URLs
"""

import os
import sys
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.ThreadsExtract import download_threads_video
from controller.TwitterExtract import download_twitter_video
from controller.InstagramExtract import download_instagram_media
from controller.TikTokExtractYTDLP import download_tiktok_video


def test_url(platform, url, download_func, needs_output_dir=True):
    """Test a single URL download"""
    print("\n" + "="*80)
    print(f"Testing {platform}")
    print("="*80)
    print(f"URL: {url}")

    output_dir = os.path.join(os.path.dirname(__file__), "test_downloads")
    os.makedirs(output_dir, exist_ok=True)

    try:
        if needs_output_dir:
            filepath = download_func(url, output_dir)
        else:
            # For TikTok, the function returns temp path, copy it to output_dir
            temp_filepath = download_func(url)
            filename = os.path.basename(temp_filepath)
            filepath = os.path.join(output_dir, filename)
            shutil.copy2(temp_filepath, filepath)
            print(f"Copied to: {filepath}")

        print(f"[SUCCESS] Downloaded to: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Multi-Platform URL Download Test")
    print("="*80)

    tests = [
        ("Threads", "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1", download_threads_video, True),
        ("Twitter/X", "https://x.com/elonmusk/status/1983810924386644306", download_twitter_video, True),
        ("Instagram", "https://www.instagram.com/p/DQcJ-QYCU2x/", download_instagram_media, True),
        ("TikTok", "https://www.tiktok.com/@tikdoktic/video/7564394978043022609?is_from_webapp=1&sender_device=pc", download_tiktok_video, True)
    ]

    results = {}

    for platform, url, func, needs_output_dir in tests:
        results[platform] = test_url(platform, url, func, needs_output_dir)

    print("\n" + "="*80)
    print("Test Results Summary")
    print("="*80)
    for platform, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{platform}: {status}")
    print("="*80)

    # Exit with error code if any test failed
    if not all(results.values()):
        sys.exit(1)
