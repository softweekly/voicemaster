@echo off
echo Installing Speech Recognition Dependencies...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Installing SpeechRecognition...
pip install SpeechRecognition==3.10.4
if %errorlevel% neq 0 (
    echo Warning: SpeechRecognition installation may have issues
)

echo.
echo Installing pyaudio...
pip install pyaudio==0.2.14
if %errorlevel% neq 0 (
    echo Warning: PyAudio installation failed. You may need to install Visual C++ Build Tools
    echo Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo Or try: pip install pipwin && pipwin install pyaudio
)

echo.
echo Installing pydub...
pip install pydub==0.25.1
if %errorlevel% neq 0 (
    echo Warning: pydub installation may have issues
)

echo.
echo ✅ Speech recognition setup complete!
echo.
echo Note: If PyAudio failed to install:
echo 1. Download Visual C++ Build Tools
echo 2. Or use: pip install pipwin && pipwin install pyaudio
echo 3. Or download pre-compiled wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo.
echo Features added:
echo - 🎙️ Speech-to-Clone button (F3 hotkey)
echo - Record your voice and generate it in selected clone voice
echo - Automatic speech recognition to text
echo - Works with Google Speech Recognition (requires internet)
echo.
pause