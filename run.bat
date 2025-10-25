@echo off
chcp 65001 >nul
title Video Downloader - TikTok/Douyin/YouTube/Threads

echo ======================================================================
echo                      Video Downloader
echo                TikTok · Douyin · YouTube · Threads
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.12+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [INFO] Checking dependencies...
echo.

REM Check if required packages are installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] Starting Video Downloader...
echo.
echo ======================================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Program exited with an error
    pause
) else (
    echo.
    echo [INFO] Program closed normally
)
