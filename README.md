# Vo## Features

- 🎤 Custom voice selection from your ElevenLabs account
- ⚡ Quick phrase buttons for common streaming messages
- 💾 **TTS Favorites System** - Save frequently used comments with specific voices
- 📁 **Overlay Archive** - Automatically numbered overlay files for easy tracking
- 🎮 Keyboard shortcuts for hands-free operation
- 📺 OBS overlay integration with archive support
- 🔊 Built-in audio playback
- 🎨 Dark theme optimized for streaming setupsr Pro - Live Streaming TTS

A professional Text-to-Speech application for live streaming with custom ElevenLabs voices.

## Features

- 🎤 Custom voice selection from your ElevenLabs account
- ⚡ Quick phrase buttons for common streaming messages
- 🎮 Keyboard shortcuts for hands-free operation
- 📺 OBS overlay integration
- 🔊 Built-in audio playback
- 🎨 Dark theme optimized for streaming setups
- 🎙️ **NEW: Speech-to-Clone** - Record your voice and generate it in any clone voice
- 💾 TTS Favorites system with voice combinations
- 📁 Automatic overlay archiving with timestamp numbering

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher (3.9-3.12 recommended, 3.13+ supported with compatibility shims)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for application + dependencies
- **Audio**: Working audio output device
- **Microphone**: Required for Speech-to-Clone feature

### Software Prerequisites
- **Python 3.8+**: Download from [python.org](https://python.org)
- **Git** (optional): For version control - [git-scm.com](https://git-scm.com/download/windows)
- **Visual C++ Build Tools** (Windows): May be required for PyAudio - [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### ElevenLabs Account Requirements
- **Active ElevenLabs Account**: [elevenlabs.io](https://elevenlabs.io)
- **API Key**: Available in your ElevenLabs account settings
- **Custom Voices**: At least one custom voice created in your account
- **Character Credits**: Sufficient credits for TTS generation

## Setup Instructions

### First Time Setup on New Machine

1. **Install Python** (if not already installed)
   - Download from https://python.org
   - Make sure to add Python to PATH during installation

2. **Install Git** (if not already installed)
   - Download from https://git-scm.com/download/windows
   - Use default installation options

3. **Clone/Copy the project files** to your desired location
   ```bash
   # If cloning from a Git repository
   git clone [repository-url]
   cd voicemaster-pro
   
   # If copying files manually, just copy the entire folder
   ```

4. **Run the setup script**
   ```
   Double-click setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all required dependencies from requirements.txt

5. **Install Speech Recognition Dependencies (for Speech-to-Clone feature)**
   ```
   Double-click install_speech_deps.bat
   ```
   If PyAudio installation fails, you may need:
   - Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Or use: `pip install pipwin && pipwin install pyaudio`

6. **Launch VoiceMaster Pro**
   ```
   Double-click launch_voicemaster.bat
   ```
   
   **First-time setup:** If no credentials are found, VoiceMaster will automatically open a setup wizard where you can:
   - Enter your Eleven Labs API key
   - Test the connection
   - Save your credentials securely
   
   **How to get your API key:**
   1. Go to [ElevenLabs.io](https://elevenlabs.io)
   2. Sign in to your account
   3. Click on your profile (top right)
   4. Select "Profile + API Key"
   5. Copy the API key
   
   The setup wizard will guide you through the rest!

   **Security Note:** Your API key is stored locally in a `.env` file and never shared

7. **Create Custom Voices (Required)**
   - This app only works with YOUR custom voices
   - Go to ElevenLabs → Voice Lab → Add New Voice
   - Create at least one custom voice using:
     - Voice cloning (upload audio samples)
     - Professional voice cloning (higher quality)
     - Instant voice cloning (quick setup)
   - Wait a few minutes for voice processing to complete

8. **Test your setup**
   - Launch the application: `Double-click launch_voicemaster.bat`
   - Check that your custom voices appear in the dropdown
   - Test TTS generation with a short phrase
   - Verify audio playback works

8. **Test your setup**
   - Launch the application: `Double-click launch_voicemaster.bat`
   - Check that your custom voices appear in the dropdown
   - Test TTS generation with a short phrase
   - Verify audio playback works

9. **Launch the application**
   ```
   Double-click launch_voicemaster.bat
   ```

### Git Repository Setup

If you want to set up version control:

1. **Automated Git setup**
   ```
   Double-click git_setup.bat
   ```

2. **Manual Git setup**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

### Manual Setup (Alternative)

If the batch files don't work, you can set up manually:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python voicemaster_gui.py
```

## Usage

### GUI Controls
- **Voice Selection**: Choose from your custom ElevenLabs voices
- **Text Input**: Enter text to convert to speech
- **Generate Button**: Create speech (Ctrl+Enter)
- **🎙️ Speech-to-Clone**: Record your voice and generate in selected clone voice (F3)
- **Play/Stop**: Control audio playback (F1/F2)
- **Quick Phrases**: Pre-made streaming messages + your saved favorites
- **💾 Save as Favorite**: Save current text + voice combination
- **🔄 Refresh**: Update favorites list
- **Right-click favorites**: Delete unwanted favorites

### Credentials Management
- **Settings Menu**: Access "Settings → Eleven Labs Credentials" to update your API key
- **Automatic Setup**: First-time users get a guided setup wizard
- **Secure Storage**: API keys stored locally in encrypted .env files
- **Easy Updates**: Change API keys anytime without restarting
- **Connection Testing**: Built-in API key validation and connection testing

### Speech-to-Clone System
- **🎙️ Record & Clone**: Press F3 or click Speech-to-Clone button
- **Automatic Recognition**: Converts your speech to text using Google Speech Recognition
- **Voice Cloning**: Generates the recognized text in your selected custom voice
- **Perfect for Streaming**: Quickly clone your voice saying anything
- **Real-time Process**: Record → Recognize → Generate → Play (all automatic)

### TTS Favorites System
- Save any text with specific voice combinations
- Quick access to your most-used comments
- Right-click to delete unwanted favorites
- Automatically loads both text and voice when selected
- Perfect for recurring stream interactions

### Overlay Archive System
- Every overlay is automatically saved with timestamp numbers
- Easy to identify newest vs older overlays
- Files saved in `saved_overlays/` directory
- Higher numbers = newer overlays
- Use `view_archives.py` to browse saved overlays

### Keyboard Shortcuts
- `Ctrl + Enter` - Generate speech
- `F1` - Play audio
- `F2` - Stop audio
- `F3` - **NEW: Speech-to-Clone** (record your voice)

### OBS Integration
- Add `overlay.html` as a Browser Source in OBS
- The overlay automatically updates with current voice info

## Files Structure

```
VoiceMaster Pro/
├── voicemaster_gui.py      # Main GUI application
├── app_logic.py           # Core TTS functionality
├── view_archives.py       # Overlay archive viewer
├── requirements.txt       # Python dependencies
├── setup.bat             # Automated setup script
├── git_setup.bat         # Git repository setup script
├── launch_voicemaster.bat # Application launcher
├── .env.example          # Environment variables template
├── .env                  # Environment variables (API key) - Git ignored
├── .gitignore           # Git ignore rules
├── README.md            # This documentation
├── overlay.html          # Current OBS overlay file
├── tts_favorites.json    # Saved favorites database - Git ignored
├── generated_audio/      # Generated audio files - Git ignored
├── saved_overlays/       # Archived overlay files - Git ignored
├── tts_favorites/        # Favorites audio cache - Git ignored
└── .venv/               # Virtual environment - Git ignored
```

## Dependencies

**Core TTS:**
- `requests==2.32.5` - HTTP requests to ElevenLabs API
- `python-dotenv==1.1.1` - Environment variable management
- `pygame==2.6.1` - Audio playback functionality

**Speech-to-Clone Feature:**
- `SpeechRecognition==3.10.4` - Speech recognition capabilities
- `pyaudio==0.2.14` - Microphone audio recording
- `pydub==0.25.1` - Audio processing utilities

**Standard Library (included with Python):**
- `tkinter` - GUI framework
- `threading` - Async operations
- `os`, `json`, `time` - System utilities

## Environment Configuration

### Environment Variables (.env file)

Create a `.env` file in the project root with these settings:

```env
# Required: Your ElevenLabs API Key
ELEVENLABS_API_KEY=your_api_key_here

# Optional: Audio settings (uncomment if needed)
# PYGAME_AUDIO_DRIVER=directsound  # Windows audio driver
# PYGAME_AUDIO_FREQUENCY=22050     # Audio sample rate
# PYGAME_AUDIO_SIZE=-16            # Audio bit depth
# PYGAME_AUDIO_CHANNELS=2          # Stereo audio

# Optional: Speech recognition settings
# SPEECH_RECOGNITION_TIMEOUT=5     # Recording timeout in seconds
# SPEECH_RECOGNITION_LANGUAGE=en-US # Recognition language
```

### File Permissions

Ensure the application has permissions to:
- Read/write in the project directory
- Access microphone (for Speech-to-Clone)
- Access audio output devices
- Make network requests (for API calls)

### Firewall/Antivirus

If you encounter connection issues:
- Allow Python through Windows Firewall
- Add project folder to antivirus exclusions
- Ensure antivirus isn't blocking API requests

## Troubleshooting

### Installation Issues

**Python 3.13 Compatibility Issues**
```
ModuleNotFoundError: No module named 'aifc'
ModuleNotFoundError: No module named 'audioop'
ModuleNotFoundError: No module named 'distutils'
```
Solutions:
1. **Automatic Fix**: The launch script automatically installs compatibility packages
2. **Manual Fix**: Install setuptools: `pip install "setuptools<70"`
3. **Alternative**: Downgrade to Python 3.12 or earlier where these modules are included
4. **Root Cause**: Python 3.13 removed these deprecated modules per PEP 594

The launch script (`launch_voicemaster.bat`) automatically detects and fixes these issues.

**PyAudio Installation Fails (Windows)**
```
ERROR: Microsoft Visual C++ 14.0 is required
```
Solutions:
1. Install Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Alternative: `pip install pipwin && pipwin install pyaudio`
3. Use pre-compiled wheel: Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

**Python Not Found**
```
'python' is not recognized as an internal or external command
```
Solutions:
1. Reinstall Python with "Add to PATH" option checked
2. Use full path: `C:\Python\python.exe` instead of `python`
3. Try `py` instead of `python` on Windows

**Virtual Environment Issues**
```
cannot import name '_ssl' from '_ssl'
```
Solutions:
1. Reinstall Python with SSL support
2. Use system Python instead of virtual environment temporarily
3. Update pip: `python -m pip install --upgrade pip`

**Dependencies Installation Fails**
```
ERROR: Could not find a version that satisfies the requirement
```
Solutions:
1. Update pip: `python -m pip install --upgrade pip`
2. Use specific index: `pip install -i https://pypi.org/simple/ package_name`
3. Install dependencies one by one instead of from requirements.txt

### Runtime Issues

**No Custom Voices Found**
```
Error: No custom voices available
```
Solutions:
1. Create custom voices in your ElevenLabs account first
2. Check API key is correct in `.env` file
3. Verify ElevenLabs account has active subscription
4. Wait a few minutes after creating voices for API sync

**Audio Playback Problems**
```
pygame.error: No available audio device
```
Solutions:
1. Check system audio settings and default playback device
2. Restart application after plugging in audio devices
3. Try different audio format: Add to `.env`: `PYGAME_AUDIO_DRIVER=directsound`
4. Install audio drivers for your system

**Speech Recognition Not Working**
```
Could not understand audio
```
Solutions:
1. Check microphone permissions and default input device
2. Speak clearly and close to microphone
3. Reduce background noise
4. Test microphone in other applications first
5. Try different speech recognition engine in settings

**API Connection Issues**
```
requests.exceptions.ConnectionError
```
Solutions:
1. Check internet connection
2. Verify ElevenLabs API status: https://status.elevenlabs.io/
3. Check firewall/antivirus blocking Python
4. Try using VPN if region-blocked

### Common Issues

1. **ModuleNotFoundError**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **API Key Error**
   - Check your `.env` file has the correct API key
   - Verify your ElevenLabs account has custom voices

3. **No Custom Voices Found**
   - Create custom voices in your ElevenLabs account
   - The app filters out built-in voices and only shows your custom ones

4. **Audio Playback Issues**
   - Make sure pygame is installed: `pip install pygame`
   - Check your system audio settings

### Performance Issues

**Slow TTS Generation**
- Check ElevenLabs API limits and credits
- Reduce text length for faster processing
- Use lower quality settings in ElevenLabs account

**High Memory Usage**
- Clear `generated_audio/` folder periodically
- Restart application if using for extended periods
- Close other applications to free up RAM

**GUI Freezing**
- Don't click buttons rapidly while processing
- Wait for current operation to complete
- Restart application if GUI becomes unresponsive

## Support

For issues with:
- ElevenLabs API: Check your account status and API limits
- Audio playback: Ensure proper audio drivers and permissions
- GUI issues: Make sure Python tkinter is available (usually included with Python)

## Version History

- v1.0 - Initial release with GUI, custom voice filtering, and OBS integration