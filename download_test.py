
import os
import sys
import shutil

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.ThreadsExtract import download_threads_video, ThreadsDownloadError

def test_threads_download():
    """Tests the Threads download functionality."""
    output_file = "test_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        url = "https://www.threads.com/@fig080/post/DQGf4IQEomg?xmt=AQF07sE3gWdKiRT-Hus1ABKS6KQ_HRMZIM-8cmfWtoBx7g&slof=1"
        download_dir = "test_downloads"
        
        # Create a clean directory for the download
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        os.makedirs(download_dir)
        
        f.write(f"Attempting to download: {url}\n")
        
        try:
            filepath = download_threads_video(url, download_dir)
            
            if filepath and os.path.exists(filepath):
                f.write(f"Download successful!\n")
                f.write(f"File saved to: {os.path.abspath(filepath)}\n")
            else:
                f.write("Download failed. No file was created.\n")
                if filepath:
                    f.write(f"Function returned: {filepath}\n")
                
        except Exception as e:
            f.write(f"An error occurred: {e}\n")

if __name__ == "__main__":
    test_threads_download()
