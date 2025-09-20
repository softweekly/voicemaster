@echo off
echo Setting up VoiceMaster Pro environment...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo.
echo Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo To run VoiceMaster Pro:
echo 1. Double-click launch_voicemaster.bat
echo 2. Or run: .venv\Scripts\python.exe voicemaster_gui.py
echo.
echo Don't forget to:
echo - Add your ElevenLabs API key to the .env file
echo - Create custom voices in your ElevenLabs account
echo.
pause