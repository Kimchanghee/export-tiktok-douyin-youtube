"""
Test YouTube video download
"""

import sys
import os
import subprocess

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_youtube_download(url, description):
    """Test YouTube download with yt-dlp"""
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"{'='*70}")
    print(f"URL: {url}")
    print(f"Output: {output_dir}")
    print(f"-"*70)

    try:
        cmd = [
            "yt-dlp",
            "-f", "best",
            "-o", os.path.join(output_dir, "%(title)s_%(id)s.%(ext)s"),
            "--no-playlist",
            url
        ]

        print(f"Running: yt-dlp...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180
        )

        print(f"\nReturn code: {result.returncode}")

        if result.stdout:
            print(f"\n📤 Output:")
            print(result.stdout)

        if result.stderr:
            print(f"\n⚠️ Errors/Warnings:")
            print(result.stderr)

        if result.returncode == 0:
            print(f"\n✅ SUCCESS - Download completed!")

            # Find the downloaded file
            import glob
            files = glob.glob(os.path.join(output_dir, "*"))
            if files:
                latest_file = max(files, key=os.path.getctime)
                file_size = os.path.getsize(latest_file)
                print(f"   File: {os.path.basename(latest_file)}")
                print(f"   Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
                print(f"   Path: {latest_file}")
            return True
        else:
            print(f"\n❌ FAILED - Return code: {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n❌ TIMEOUT - Download took too long (>180s)")
        return False
    except FileNotFoundError:
        print(f"\n❌ ERROR - yt-dlp not found!")
        print(f"Please install: pip install yt-dlp")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*70)
    print("YouTube Download Test")
    print("="*70)

    # Test 1: Regular YouTube video
    url1 = "https://youtu.be/He9Uu7ngRks?si=F9f-MIs5GTH0os1N"
    result1 = test_youtube_download(url1, "Regular YouTube Video")

    # Test 2: YouTube Shorts
    url2 = "https://youtube.com/shorts/kFkKrurTpE4?si=eA-1d62ct1h7Cu5D"
    result2 = test_youtube_download(url2, "YouTube Shorts")

    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Regular Video: {'✅ PASS' if result1 else '❌ FAIL'}")
    print(f"YouTube Shorts: {'✅ PASS' if result2 else '❌ FAIL'}")
    print(f"{'='*70}")

    sys.exit(0 if (result1 and result2) else 1)
