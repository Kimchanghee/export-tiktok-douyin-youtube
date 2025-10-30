"""
Test script for Twitter and Instagram downloaders
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.TwitterExtract import download_twitter_video
from controller.InstagramExtract import download_instagram_media


def test_twitter():
    """Test Twitter downloader"""
    print("\n" + "="*50)
    print("Testing Twitter Downloader")
    print("="*50)

    # Test URL - replace with actual Twitter video URL
    test_url = "https://twitter.com/example/status/123"

    output_dir = os.path.join(os.path.dirname(__file__), "test_downloads")

    try:
        print(f"\nDownloading from: {test_url}")
        filepath = download_twitter_video(test_url, output_dir)
        print(f"✓ Success! Downloaded to: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_instagram():
    """Test Instagram downloader"""
    print("\n" + "="*50)
    print("Testing Instagram Downloader")
    print("="*50)

    # Test URL - replace with actual Instagram post URL
    test_url = "https://www.instagram.com/p/example/"

    output_dir = os.path.join(os.path.dirname(__file__), "test_downloads")

    try:
        print(f"\nDownloading from: {test_url}")
        filepath = download_instagram_media(test_url, output_dir)
        print(f"✓ Success! Downloaded to: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Platform Downloader Tests")
    print("="*50)

    # Note: Replace test URLs with real ones before running
    print("\n⚠ IMPORTANT: Update test URLs in this script before running!")
    print("   - Line 19: Replace with real Twitter video URL")
    print("   - Line 39: Replace with real Instagram post URL")

    results = {
        "Twitter": None,
        "Instagram": None
    }

    # Uncomment to test (after adding real URLs)
    # results["Twitter"] = test_twitter()
    # results["Instagram"] = test_instagram()

    print("\n" + "="*50)
    print("Test Results Summary")
    print("="*50)
    for platform, result in results.items():
        if result is None:
            status = "SKIPPED"
        elif result:
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
        print(f"{platform}: {status}")
    print("="*50)
