# VoiceMaster Pro - Linux Setup Guide 🐧

## 🚀 Quick Start for Linux Users

### 📋 **Prerequisites**
- **Python 3.8+** (most Linux distributions have this)
- **Audio system** working (ALSA/PulseAudio)
- **Internet connection** for package installation
- **Eleven Labs account** with custom voices

### ⚡ **One-Command Setup**

```bash
# Make setup script executable and run it
chmod +x setup_linux.sh && ./setup_linux.sh
```

That's it! The script will:
- ✅ Check Python installation
- ✅ Install system dependencies (tkinter, audio libs)
- ✅ Create virtual environment
- ✅ Install all Python packages
- ✅ Create Linux launcher script
- ✅ Test everything works

### 🚀 **Launch VoiceMaster Pro**

```bash
# After setup, launch with:
./launch_voicemaster_linux.sh
```

## 📦 **Distribution-Specific Instructions**

### **Ubuntu/Debian**
```bash
# Install prerequisites (if needed)
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
sudo apt install libasound2-dev portaudio19-dev python3-dev build-essential

# Run VoiceMaster setup
chmod +x setup_linux.sh && ./setup_linux.sh
```

### **Fedora/CentOS/RHEL**
```bash
# Install prerequisites (if needed)
sudo dnf install python3 python3-pip python3-tkinter
sudo dnf install alsa-lib-devel portaudio-devel python3-devel gcc

# Run VoiceMaster setup
chmod +x setup_linux.sh && ./setup_linux.sh
```

### **Arch Linux**
```bash
# Install prerequisites (if needed)
sudo pacman -S python python-pip tk alsa-lib portaudio gcc

# Run VoiceMaster setup
chmod +x setup_linux.sh && ./setup_linux.sh
```

### **openSUSE**
```bash
# Install prerequisites (if needed)
sudo zypper install python3 python3-pip python3-tk
sudo zypper install alsa-devel portaudio-devel python3-devel gcc

# Run VoiceMaster setup
chmod +x setup_linux.sh && ./setup_linux.sh
```

## 🔧 **Manual Setup (If Automatic Fails)**

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Test installation
python -c "import tkinter, requests, pygame; print('All good!')"

# 5. Launch
python login_gui.py  # First time (enter API key)
python voicemaster_gui.py  # Subsequent launches
```

## 🎮 **Desktop Integration**

The setup script creates a desktop entry, so you can:
- Find "VoiceMaster Pro" in your applications menu
- Add it to your taskbar/dock
- Launch from desktop

## 🎵 **Audio System Notes**

### **PulseAudio (Most Common)**
- Should work out of the box
- Make sure `pulseaudio` is running
- Test: `pactl info`

### **ALSA**
- Usually works automatically
- Test: `aplay /usr/share/sounds/alsa/Front_Left.wav`

### **JACK**
- Advanced audio system
- May need additional configuration
- Consider using `pulseaudio-jack` bridge

## 🎙️ **Microphone Setup (Speech-to-Clone)**

```bash
# Test microphone
arecord -l  # List recording devices
arecord -d 3 test.wav  # Record 3-second test
aplay test.wav  # Play back test

# If microphone issues:
sudo usermod -a -G audio $USER  # Add user to audio group
# Logout and login again
```

## 🖥️ **Display System Compatibility**

### **X11 (Traditional)**
- ✅ Fully supported
- Works with all window managers

### **Wayland (Modern)**
- ✅ Supported through XWayland
- May have minor scaling differences
- Works with GNOME, KDE Plasma, Sway

## 🐛 **Troubleshooting**

### **"tkinter not found"**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### **"No module named '_tkinter'"**
```bash
# Rebuild Python with tkinter support
# Or use system Python with tkinter installed
```

### **PyAudio installation fails**
```bash
# Install development headers first
sudo apt install portaudio19-dev python3-dev  # Ubuntu/Debian
sudo dnf install portaudio-devel python3-devel  # Fedora

# Then try again
pip install PyAudio
```

### **Audio playback issues**
```bash
# Check audio system
pulseaudio --check -v  # PulseAudio
cat /proc/asound/cards  # ALSA

# Test with simple audio
python3 -c "import pygame; pygame.mixer.init(); print('Audio system OK')"
```

### **Permission denied errors**
```bash
# Make sure scripts are executable
chmod +x *.sh

# Check audio group membership
groups $USER | grep audio
```

## 🔗 **File Permissions Quick Fix**

```bash
# Make all scripts executable
chmod +x *.sh
chmod +x *.py

# Or make everything executable
find . -name "*.sh" -exec chmod +x {} \;
find . -name "*.py" -exec chmod +x {} \;
```

## 🎯 **Performance Tips**

- **SSD storage**: Faster startup times
- **Sufficient RAM**: 4GB+ recommended for speech processing
- **Good internet**: For Eleven Labs API calls
- **Working audio**: Essential for TTS playback

## 🆘 **Getting Help**

If you encounter issues:

1. **Check the setup log** - The setup script shows detailed error messages
2. **Verify prerequisites** - Python 3.8+, audio system working
3. **Try manual setup** - Step-by-step instructions above
4. **Check permissions** - Make sure scripts are executable
5. **Test audio system** - Ensure basic audio playback works

## 🎉 **Success Indicators**

You'll know everything is working when:
- ✅ Setup script completes without errors
- ✅ `./launch_voicemaster_linux.sh` starts the login GUI
- ✅ You can enter your API key and connect
- ✅ Your custom voices appear in the dropdown
- ✅ TTS generation and playback works

**VoiceMaster Pro is now ready to rock on Linux!** 🐧🚀