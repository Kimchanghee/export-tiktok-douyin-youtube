"""
Test Threads video downloader with specific URL
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller.ThreadsExtract import download_threads_video, ThreadsDownloadError

def test_threads_download():
    url = "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos")

    print(f"Testing Threads download...")
    print(f"URL: {url}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}/{max_attempts}...")
        try:
            filepath = download_threads_video(url, output_dir)
            print(f"\n✅ SUCCESS!")
            print(f"Downloaded video to: {filepath}")

            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
            return True

        except ThreadsDownloadError as e:
            print(f"❌ ThreadsDownloadError: {e}")
            if attempt < max_attempts:
                print(f"Retrying...")
            else:
                print(f"\n⚠️ Failed after {max_attempts} attempts")
                return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            if attempt < max_attempts:
                print(f"Retrying...")
            else:
                print(f"\n⚠️ Failed after {max_attempts} attempts")
                return False

    return False

if __name__ == "__main__":
    success = test_threads_download()
    sys.exit(0 if success else 1)
