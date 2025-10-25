"""
Use Selenium to check if there's a video element
"""

import sys
import os
import time

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("Installing selenium...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "selenium"], check=True)
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options

def check_threads_video():
    url = "https://www.threads.net/@fig080/post/DQGf4IQEomg"

    print(f"🌐 Opening Threads post in browser...")
    print(f"URL: {url}")
    print("-" * 70)

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for page to load
        print(f"⏳ Waiting for page to load...")
        time.sleep(5)

        # Check for video elements
        print(f"\n🔍 Searching for media elements...\n")

        video_elements = driver.find_elements(By.TAG_NAME, "video")
        if video_elements:
            print(f"✅ Found {len(video_elements)} <video> element(s)!")
            for i, video in enumerate(video_elements, 1):
                src = video.get_attribute("src")
                poster = video.get_attribute("poster")
                print(f"\n   Video {i}:")
                if src:
                    print(f"   - src: {src[:100]}...")
                if poster:
                    print(f"   - poster: {poster[:100]}...")

                # Try to get source elements
                sources = video.find_elements(By.TAG_NAME, "source")
                for j, source in enumerate(sources, 1):
                    source_src = source.get_attribute("src")
                    source_type = source.get_attribute("type")
                    print(f"   - source {j}: {source_src[:100] if source_src else 'None'} (type: {source_type})")
        else:
            print(f"❌ No <video> elements found")

        # Check for img elements
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        print(f"\n📷 Found {len(img_elements)} <img> element(s)")

        # Look for any element with video in src/data
        print(f"\n🔎 Searching for .mp4 in page source...")
        page_source = driver.page_source
        import re
        mp4_urls = re.findall(r'https://[^\s"\'<>]+\.mp4[^\s"\'<>]*', page_source)
        if mp4_urls:
            unique_urls = list(set(mp4_urls))
            print(f"✅ Found {len(unique_urls)} unique .mp4 URL(s):")
            for i, url in enumerate(unique_urls[:5], 1):
                print(f"   {i}. {url[:150]}...")
        else:
            print(f"❌ No .mp4 URLs in page source")

        # Check meta tags
        print(f"\n🔎 Checking meta tags...")
        og_type = driver.find_element(By.XPATH, "//meta[@property='og:type']") if driver.find_elements(By.XPATH, "//meta[@property='og:type']") else None
        if og_type:
            content = og_type.get_attribute("content")
            print(f"   og:type = {content}")

        og_video = driver.find_elements(By.XPATH, "//meta[@property='og:video']")
        if og_video:
            for i, meta in enumerate(og_video, 1):
                content = meta.get_attribute("content")
                print(f"   og:video {i} = {content}")
        else:
            print(f"   ❌ No og:video meta tag")

        og_image = driver.find_elements(By.XPATH, "//meta[@property='og:image']")
        if og_image:
            print(f"   ✅ og:image found (indicates image post)")

        # Save screenshot
        screenshot_path = "threads_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Screenshot saved to: {screenshot_path}")

        driver.quit()

        print(f"\n" + "=" * 70)
        print(f"CONCLUSION:")
        if not video_elements and not mp4_urls and og_image:
            print(f"This Threads post contains an IMAGE, not a video.")
            return False
        elif video_elements or mp4_urls:
            print(f"This Threads post contains a VIDEO.")
            return True
        else:
            print(f"Unable to determine media type.")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = check_threads_video()
    sys.exit(0 if result else 1)
