@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo    VoiceMaster Pro - First Time Setup
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org/downloads/
    echo 2. Download Python 3.8 or newer
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Run this setup again after Python is installed
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python !PYTHON_VERSION! found

REM Check Python version (basic check)
echo [2/5] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3.8 or newer required
    echo Please update Python from https://python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python version is compatible

REM Create virtual environment
echo [3/5] Creating virtual environment...
if exist ".venv" (
    echo ✅ Virtual environment already exists
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo This might happen if:
        echo - Python was installed without pip
        echo - Insufficient disk space
        echo - Antivirus blocking file creation
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment and install packages
echo [4/5] Installing required packages...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip first
python -m pip install --upgrade pip --quiet

REM Install requirements
echo Installing packages (this may take a few minutes)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install some packages
    echo.
    echo Common solutions:
    echo 1. Check internet connection
    echo 2. Try running as Administrator
    echo 3. Temporarily disable antivirus
    echo 4. Manual install: pip install requests python-dotenv pygame SpeechRecognition pydub
    echo.
    echo For PyAudio issues on Windows:
    echo 1. Install Visual C++ Build Tools
    echo 2. Or try: pip install pipwin ^&^& pipwin install pyaudio
    echo.
    pause
    exit /b 1
)

echo ✅ All packages installed successfully

REM Test imports
echo [5/5] Testing installation...
python -c "import tkinter, requests, pygame; print('✅ Core packages working')" 2>nul
if errorlevel 1 (
    echo ❌ Package import test failed
    echo Some packages may not be properly installed
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 Setup Complete!
echo ========================================
echo.
echo VoiceMaster Pro is now ready to use!
echo.
echo Next steps:
echo 1. Double-click "launch_voicemaster.bat"
echo 2. Enter your Eleven Labs API key when prompted
echo 3. Start using your custom voices!
echo.
echo ✨ Need an API key? Visit: https://elevenlabs.io
echo    Go to Profile ^> API Key to get yours
echo.
pause