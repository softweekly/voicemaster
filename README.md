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

5. **Configure your API key**
   - Copy `.env.example` to `.env`
   - Open the `.env` file
   - Add your ElevenLabs API key:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

6. **Launch the application**
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
- **Play/Stop**: Control audio playback (F1/F2)
- **Quick Phrases**: Pre-made streaming messages + your saved favorites
- **💾 Save as Favorite**: Save current text + voice combination
- **🔄 Refresh**: Update favorites list
- **Right-click favorites**: Delete unwanted favorites

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

- `requests` - HTTP requests to ElevenLabs API
- `python-dotenv` - Environment variable management
- `pygame` - Audio playback functionality

## Troubleshooting

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

## Support

For issues with:
- ElevenLabs API: Check your account status and API limits
- Audio playback: Ensure proper audio drivers and permissions
- GUI issues: Make sure Python tkinter is available (usually included with Python)

## Version History

- v1.0 - Initial release with GUI, custom voice filtering, and OBS integration