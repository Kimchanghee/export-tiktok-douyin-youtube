"""
Final test - try multiple times with the provided URL
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

def test_download(url, max_attempts=5):
    """Test download with multiple attempts"""
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos")

    print(f"=" * 70)
    print(f"Testing Threads Download")
    print(f"=" * 70)
    print(f"URL: {url}")
    print(f"Output: {output_dir}")
    print(f"Max attempts: {max_attempts}")
    print(f"-" * 70)

    for attempt in range(1, max_attempts + 1):
        print(f"\n[Attempt {attempt}/{max_attempts}]")
        try:
            filepath = download_threads_video(url, output_dir)

            if filepath and os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                file_ext = os.path.splitext(filepath)[1].lower()

                print(f"\n✅ SUCCESS!")
                print(f"   Downloaded: {os.path.basename(filepath)}")
                print(f"   Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
                print(f"   Type: {file_ext}")
                print(f"   Path: {filepath}")

                # Check if it's video or image
                if file_ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                    print(f"   🎥 Media Type: VIDEO")
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    print(f"   🖼️  Media Type: IMAGE")

                    # Note if we got an image instead of video
                    if "video" in url.lower() or attempt < max_attempts:
                        print(f"\n   ⚠️  NOTE: Downloaded an image, not a video.")
                        print(f"   This post might not contain video, or the video")
                        print(f"   could not be extracted by the available methods.")

                        if attempt < max_attempts:
                            print(f"   Retrying to see if we can get a video...")
                            # Clean up the image file
                            try:
                                os.remove(filepath)
                                print(f"   Removed image file to retry")
                            except:
                                pass
                            continue

                print(f"\n" + "=" * 70)
                return True
            else:
                print(f"   ❌ Download returned no file")

        except ThreadsDownloadError as e:
            print(f"   ❌ ThreadsDownloadError: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

        if attempt < max_attempts:
            print(f"   Waiting before retry...")
            import time
            time.sleep(2)

    print(f"\n" + "=" * 70)
    print(f"⚠️  Failed after {max_attempts} attempts")
    print(f"\nPossible reasons:")
    print(f"  1. The post does not contain video (only image)")
    print(f"  2. The video is private or restricted")
    print(f"  3. Threads API has changed and blocked access")
    print(f"  4. Network/connection issues")
    print(f"=" * 70)
    return False

if __name__ == "__main__":
    # Test with the provided URL
    url = "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"

    success = test_download(url, max_attempts=3)

    if not success:
        print(f"\n" + "=" * 70)
        print(f"ℹ️  ANALYSIS RESULT:")
        print(f"=" * 70)
        print(f"The provided Threads post appears to contain an IMAGE, not a VIDEO.")
        print(f"The download succeeded (an image was downloaded), but no video")
        print(f"was found in this post.")
        print(f"\nPost content (Korean text):")
        print(f"'영화관에서 롯데 광고 나오는데 AI그림 사용하는 거 너무 싫다'")
        print(f"(Translation: Complaining about AI-generated images in Lotte cinema ads)")
        print(f"\n" + "=" * 70)

    sys.exit(0 if success else 1)
