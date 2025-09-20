@echo off
echo Setting up Git repository for VoiceMaster Pro...
echo.

REM Initialize Git repository
echo Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH.
    echo Please install Git from: https://git-scm.com/download/windows
    pause
    exit /b 1
)

REM Set up Git configuration (optional - user can change these)
echo.
set /p username="Enter your Git username (or press Enter to skip): "
set /p email="Enter your Git email (or press Enter to skip): "

if not "%username%"=="" (
    git config user.name "%username%"
    echo Git username set to: %username%
)

if not "%email%"=="" (
    git config user.email "%email%"
    echo Git email set to: %email%
)

REM Add files to Git
echo.
echo Adding files to Git repository...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files to Git.
    pause
    exit /b 1
)

REM Create initial commit
echo.
echo Creating initial commit...
git commit -m "Initial commit: VoiceMaster Pro - Live Streaming TTS Application

Features:
- Custom ElevenLabs voice integration
- Live streaming GUI with hotkeys
- OBS overlay support
- Audio playback controls
- Quick phrase buttons
- Dark theme optimized for streaming"

if %errorlevel% neq 0 (
    echo Error: Failed to create initial commit.
    pause
    exit /b 1
)

echo.
echo ✅ Git repository setup complete!
echo.
echo What's been created:
echo - Git repository initialized
echo - .gitignore configured (excludes .env, .venv, generated audio)
echo - .env.example template created
echo - Initial commit with all source files
echo.
echo Next steps:
echo 1. To connect to GitHub: git remote add origin [your-repo-url]
echo 2. To push to GitHub: git push -u origin main
echo 3. To create a new branch: git checkout -b feature-name
echo.
echo Repository status:
git status --short
echo.
pause