"""
Instagram video/photo downloader using yt-dlp.
"""

import subprocess
import os
import glob
import re


def download_instagram_media(url, output_dir=None):
    """
    Download Instagram video or photo using yt-dlp

    Args:
        url: Instagram post URL (instagram.com)
        output_dir: Directory to save the media

    Returns:
        Path to downloaded media file

    Raises:
        Exception: If download fails
    """
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, "instagram_%(id)s.%(ext)s")

    try:
        # yt-dlp command for Instagram
        cmd = [
            "yt-dlp",
            "-f", "best",
            "-o", output_template,
            "--no-playlist",
            "--restrict-filenames",
            url
        ]

        print(f"[Instagram] Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300
        )

        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')

        print(f"[Instagram] Return code: {result.returncode}")
        print(f"[Instagram] Output: {stdout[:500]}")

        if result.returncode != 0:
            error_msg = f"Instagram download failed: {stderr[:200]}"
            print(f"[Instagram] Error: {error_msg}")
            raise Exception(error_msg)

        # Find downloaded file
        media_files = glob.glob(os.path.join(output_dir, "instagram_*.*"))
        if not media_files:
            # Try any file
            media_files = glob.glob(os.path.join(output_dir, "*.*"))

        if media_files:
            # Return most recent file
            latest_file = max(media_files, key=os.path.getctime)
            print(f"[Instagram] Downloaded: {latest_file}")
            return os.path.abspath(latest_file)

        raise Exception("Instagram media file not found after download")

    except subprocess.TimeoutExpired:
        raise Exception("Instagram download timeout (300s)")
    except FileNotFoundError:
        raise Exception("yt-dlp not installed")
    except Exception as e:
        raise Exception(f"Instagram download failed: {str(e)}")


__all__ = ["download_instagram_media"]
