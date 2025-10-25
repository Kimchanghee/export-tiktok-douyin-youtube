@echo off
echo ======================================================================
echo Building Video Downloader EXE
echo ======================================================================
echo.

pyinstaller --name=VideoDownloader --onefile --windowed --clean --noconfirm --icon=icon.ico --hidden-import=selenium --hidden-import=selenium.webdriver --hidden-import=selenium.webdriver.common.by --hidden-import=selenium.webdriver.chrome.options --hidden-import=requests --add-data=controller;controller --add-data=common;common main.py

if %errorlevel% == 0 (
    echo.
    echo ======================================================================
    echo BUILD SUCCESSFUL!
    echo ======================================================================
    echo.
    echo EXE Location: dist\VideoDownloader.exe
    dir dist\VideoDownloader.exe
    echo.
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo BUILD FAILED!
    echo ======================================================================
)

pause
