"""
Build EXE using PyInstaller
"""

import sys
import os
import subprocess
import shutil

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def build_exe():
    print("="*70)
    print("Building Video Downloader EXE")
    print("="*70)

    # Check if icon exists
    icon_path = "icon.ico"
    if not os.path.exists(icon_path):
        print(f"⚠️  Icon file not found: {icon_path}")
        print(f"Creating icon from icon.png...")
        if os.path.exists("create_icon.py"):
            subprocess.run([sys.executable, "create_icon.py"])
        else:
            print(f"⚠️  Will build without icon")
            icon_path = None

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=VideoDownloader",
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--clean",  # Clean build
        "--noconfirm",  # Overwrite without asking
    ]

    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])

    # Add hidden imports for selenium
    cmd.extend([
        "--hidden-import", "selenium",
        "--hidden-import", "selenium.webdriver",
        "--hidden-import", "selenium.webdriver.common.by",
        "--hidden-import", "selenium.webdriver.chrome.options",
        "--hidden-import", "requests",
        "--hidden-import", "urllib3",
    ])

    # Add data files (controller modules)
    cmd.extend([
        "--add-data", "controller;controller",
        "--add-data", "common;common",
    ])

    # Main script
    cmd.append("main.py")

    print(f"\n📦 Building EXE...")
    print(f"Command: {' '.join(cmd)}\n")
    print("-"*70)

    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print(f"\n{'='*70}")
            print(f"✅ BUILD SUCCESSFUL!")
            print(f"{'='*70}")

            # Check output
            exe_path = os.path.join("dist", "VideoDownloader.exe")
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path)
                print(f"\n📁 Output:")
                print(f"   Path: {os.path.abspath(exe_path)}")
                print(f"   Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

                print(f"\n✨ EXE is ready to use!")
                print(f"   Run: {exe_path}")
                return True
            else:
                print(f"\n⚠️  EXE file not found at expected location")
                return False
        else:
            print(f"\n❌ BUILD FAILED")
            print(f"Return code: {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n❌ BUILD TIMEOUT - took too long (>300s)")
        return False
    except Exception as e:
        print(f"\n❌ BUILD ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def clean_build_files():
    """Clean up build files"""
    print(f"\n🧹 Cleaning up build files...")

    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["VideoDownloader.spec"]

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   Removed: {dir_name}/")
            except Exception as e:
                print(f"   Failed to remove {dir_name}: {e}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"   Removed: {file_name}")
            except Exception as e:
                print(f"   Failed to remove {file_name}: {e}")

if __name__ == "__main__":
    try:
        success = build_exe()

        # Ask to clean up
        print(f"\n{'='*70}")
        response = input("Clean up build files? (y/n): ").strip().lower()
        if response == 'y':
            clean_build_files()

        print(f"{'='*70}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
