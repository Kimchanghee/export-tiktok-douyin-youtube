"""
Test main.py download_youtube function
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create a mock root for testing
class MockRoot:
    def after(self, delay, func, *args):
        pass

# Create a minimal VideoDownloader instance
import tkinter as tk
from main import VideoDownloader

def test_download_youtube():
    """Test YouTube download function"""
    print("="*70)
    print("Testing main.py download_youtube function")
    print("="*70)

    # Create minimal Tkinter root (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide window

    # Create VideoDownloader instance
    app = VideoDownloader(root)
    app.authenticated = True  # Bypass authentication

    # Test URLs
    urls = [
        ("https://youtu.be/He9Uu7ngRks?si=F9f-MIs5GTH0os1N", "Regular YouTube Video"),
        ("https://youtube.com/shorts/kFkKrurTpE4?si=eA-1d62ct1h7Cu5D", "YouTube Shorts"),
    ]

    results = []
    for url, description in urls:
        print(f"\n{'='*70}")
        print(f"Testing: {description}")
        print(f"URL: {url}")
        print(f"-"*70)

        success, filename = app.download_youtube(url)

        if success:
            print(f"✅ SUCCESS")
            print(f"   Filename: {filename}")
            results.append(True)
        else:
            print(f"❌ FAILED")
            results.append(False)

    # Cleanup
    root.destroy()

    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Regular Video: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"YouTube Shorts: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"{'='*70}")

    return all(results)

if __name__ == "__main__":
    try:
        success = test_download_youtube()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
