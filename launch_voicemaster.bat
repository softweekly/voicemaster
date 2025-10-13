@echo off
cd /d "%~dp0"

echo ========================================
echo    VoiceMaster Pro - Starting...
echo ========================================

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment.
    echo.
    pause
    exit /b 1
)

REM Check and install missing Python 3.13 compatibility packages
echo Checking Python 3.13 compatibility...
".venv\Scripts\python.exe" -c "import distutils" 2>nul
if errorlevel 1 (
    echo Installing Python 3.13 compatibility packages...
    ".venv\Scripts\pip.exe" install "setuptools<70" --quiet
    if errorlevel 1 (
        echo WARNING: Failed to install compatibility packages. Some features may not work.
    )
)

REM Check if .env file exists, if not launch login GUI first
if not exist ".env" (
    echo.
    echo No credentials found. Launching setup wizard...
    echo This will help you configure your Eleven Labs API key.
    echo.
    ".venv\Scripts\python.exe" login_gui.py
) else (
    echo.
    echo Credentials found. Launching VoiceMaster Pro...
    echo.
    ".venv\Scripts\python.exe" voicemaster_gui.py
)

echo.
echo VoiceMaster Pro has closed.
pause