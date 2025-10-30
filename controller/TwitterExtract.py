"""
Twitter/X video downloader using yt-dlp.
"""

import subprocess
import os
import glob
import re


def download_twitter_video(url, output_dir=None):
    """
    Download Twitter/X video using yt-dlp

    Args:
        url: Twitter/X video URL (twitter.com or x.com)
        output_dir: Directory to save the video

    Returns:
        Path to downloaded video file

    Raises:
        Exception: If download fails
    """
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, "twitter_%(id)s.%(ext)s")

    try:
        # yt-dlp command for Twitter/X
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]/best",
            "-o", output_template,
            "--no-playlist",
            "--restrict-filenames",
            url
        ]

        print(f"[Twitter] Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300
        )

        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')

        print(f"[Twitter] Return code: {result.returncode}")
        print(f"[Twitter] Output: {stdout[:500]}")

        if result.returncode != 0:
            error_msg = f"Twitter download failed: {stderr[:200]}"
            print(f"[Twitter] Error: {error_msg}")
            raise Exception(error_msg)

        # Find downloaded file
        video_files = glob.glob(os.path.join(output_dir, "twitter_*.mp4"))
        if not video_files:
            # Try any video file
            video_files = glob.glob(os.path.join(output_dir, "*.*"))

        if video_files:
            # Return most recent file
            latest_file = max(video_files, key=os.path.getctime)
            print(f"[Twitter] Downloaded: {latest_file}")
            return os.path.abspath(latest_file)

        raise Exception("Twitter video file not found after download")

    except subprocess.TimeoutExpired:
        raise Exception("Twitter download timeout (300s)")
    except FileNotFoundError:
        raise Exception("yt-dlp not installed")
    except Exception as e:
        raise Exception(f"Twitter download failed: {str(e)}")


__all__ = ["download_twitter_video"]
