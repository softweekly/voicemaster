#!/bin/bash

# VoiceMaster Pro - Linux Setup Script
# This script sets up VoiceMaster Pro on Linux systems

set -e  # Exit on any error

echo "========================================"
echo "   VoiceMaster Pro - Linux Setup"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if script is run from the correct directory
if [ ! -f "voicemaster_gui.py" ]; then
    print_error "Please run this script from the VoiceMaster Pro directory"
    exit 1
fi

# [1/7] Check Python installation
print_status "[1/7] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    if [[ $PYTHON_VERSION == 3.* ]]; then
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python"
    else
        print_error "Python 3.8+ required, found Python $PYTHON_VERSION"
        echo "Please install Python 3.8 or newer:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
        echo "  Fedora/CentOS: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
        exit 1
    fi
else
    print_error "Python not found"
    echo "Please install Python 3.8 or newer:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora/CentOS: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check Python version
print_status "[2/7] Verifying Python version..."
VERSION_CHECK=$($PYTHON_CMD -c "import sys; print('OK' if sys.version_info >= (3, 8) else 'FAIL')")
if [ "$VERSION_CHECK" != "OK" ]; then
    print_error "Python 3.8 or newer required"
    exit 1
fi
print_success "Python version is compatible"

# [3/7] Check system dependencies
print_status "[3/7] Checking system dependencies..."

# Check for tkinter
if ! $PYTHON_CMD -c "import tkinter" &> /dev/null; then
    print_warning "tkinter not found, attempting to install..."
    
    # Detect distribution and install tkinter
    if command -v apt &> /dev/null; then
        print_status "Installing python3-tk (Ubuntu/Debian)..."
        sudo apt update && sudo apt install -y python3-tk
    elif command -v dnf &> /dev/null; then
        print_status "Installing tkinter (Fedora)..."
        sudo dnf install -y python3-tkinter
    elif command -v yum &> /dev/null; then
        print_status "Installing tkinter (CentOS/RHEL)..."
        sudo yum install -y tkinter
    elif command -v pacman &> /dev/null; then
        print_status "Installing tk (Arch)..."
        sudo pacman -S tk
    else
        print_error "Could not automatically install tkinter"
        echo "Please install tkinter for your distribution:"
        echo "  Ubuntu/Debian: sudo apt install python3-tk"
        echo "  Fedora: sudo dnf install python3-tkinter"
        echo "  Arch: sudo pacman -S tk"
        exit 1
    fi
fi

# Check for audio dependencies (for pygame and speech features)
print_status "Checking audio system dependencies..."

missing_deps=()

# Check for ALSA/PulseAudio development headers
if ! pkg-config --exists alsa 2>/dev/null; then
    missing_deps+=("alsa-dev")
fi

# Check for PortAudio (needed for PyAudio)
if ! pkg-config --exists portaudio-2.0 2>/dev/null; then
    missing_deps+=("portaudio-dev")
fi

if [ ${#missing_deps[@]} -gt 0 ]; then
    print_warning "Missing audio dependencies, attempting to install..."
    
    if command -v apt &> /dev/null; then
        print_status "Installing audio dependencies (Ubuntu/Debian)..."
        sudo apt install -y libasound2-dev portaudio19-dev python3-dev gcc
    elif command -v dnf &> /dev/null; then
        print_status "Installing audio dependencies (Fedora)..."
        sudo dnf install -y alsa-lib-devel portaudio-devel python3-devel gcc
    elif command -v yum &> /dev/null; then
        print_status "Installing audio dependencies (CentOS/RHEL)..."
        sudo yum install -y alsa-lib-devel portaudio-devel python3-devel gcc
    elif command -v pacman &> /dev/null; then
        print_status "Installing audio dependencies (Arch)..."
        sudo pacman -S alsa-lib portaudio python gcc
    else
        print_warning "Could not automatically install audio dependencies"
        echo "You may need to install development packages for audio:"
        echo "  Ubuntu/Debian: sudo apt install libasound2-dev portaudio19-dev python3-dev"
        echo "  Fedora: sudo dnf install alsa-lib-devel portaudio-devel python3-devel"
        echo "  Arch: sudo pacman -S alsa-lib portaudio python"
    fi
fi

print_success "System dependencies checked"

# [4/7] Create virtual environment
print_status "[4/7] Creating virtual environment..."
if [ -d ".venv" ]; then
    print_success "Virtual environment already exists"
else
    $PYTHON_CMD -m venv .venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

# [5/7] Activate virtual environment and upgrade pip
print_status "[5/7] Activating virtual environment..."
source .venv/bin/activate

print_status "Upgrading pip..."
pip install --upgrade pip --quiet

# [6/7] Install Python packages
print_status "[6/7] Installing Python packages..."
echo "This may take a few minutes..."

if pip install -r requirements.txt --quiet; then
    print_success "All packages installed successfully"
else
    print_warning "Some packages failed to install, trying individual installation..."
    
    # Try installing packages individually
    packages=("requests" "python-dotenv" "pygame" "SpeechRecognition" "pydub")
    
    for package in "${packages[@]}"; do
        print_status "Installing $package..."
        if pip install "$package" --quiet; then
            print_success "$package installed"
        else
            print_warning "$package failed to install"
        fi
    done
    
    # PyAudio often needs special handling on Linux
    print_status "Installing PyAudio..."
    if pip install PyAudio --quiet; then
        print_success "PyAudio installed"
    else
        print_warning "PyAudio installation failed"
        echo "PyAudio is needed for Speech-to-Clone feature"
        echo "Try manual installation:"
        echo "  Ubuntu/Debian: sudo apt install python3-pyaudio"
        echo "  Or: pip install PyAudio --global-option=\"build_ext\" --global-option=\"-I/usr/local/include\" --global-option=\"-L/usr/local/lib\""
    fi
fi

# [7/7] Test installation
print_status "[7/7] Testing installation..."
if $PYTHON_CMD -c "import tkinter, requests, pygame; print('Core packages working')" 2>/dev/null; then
    print_success "Core packages test passed"
else
    print_error "Package import test failed"
    echo "Some packages may not be properly installed"
fi

# Create Linux launcher script
print_status "Creating Linux launcher script..."
cat > launch_voicemaster.sh << 'EOF'
#!/bin/bash

# VoiceMaster Pro - Linux Launcher
cd "$(dirname "$0")"

echo "========================================"
echo "   VoiceMaster Pro - Starting..."
echo "========================================"

# Check if virtual environment exists
if [ ! -f ".venv/bin/python" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup_linux.sh first to create the virtual environment."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if .env file exists, if not launch login GUI first
if [ ! -f ".env" ]; then
    echo
    echo "No credentials found. Launching setup wizard..."
    echo "This will help you configure your Eleven Labs API key."
    echo
    python login_gui.py
else
    echo
    echo "Credentials found. Launching VoiceMaster Pro..."
    echo
    python voicemaster_gui.py
fi

echo
echo "VoiceMaster Pro has closed."
read -p "Press Enter to continue..."
EOF

chmod +x launch_voicemaster.sh
print_success "Linux launcher created: launch_voicemaster.sh"

# Create desktop entry (optional)
if command -v desktop-file-install &> /dev/null || [ -d "$HOME/.local/share/applications" ]; then
    print_status "Creating desktop entry..."
    
    CURRENT_DIR=$(pwd)
    cat > voicemaster-pro.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=VoiceMaster Pro
Comment=Professional Text-to-Speech with Eleven Labs
Exec=$CURRENT_DIR/launch_voicemaster.sh
Icon=$CURRENT_DIR/icon.png
Terminal=false
Categories=AudioVideo;Audio;
StartupNotify=true
EOF

    if [ -d "$HOME/.local/share/applications" ]; then
        cp voicemaster-pro.desktop "$HOME/.local/share/applications/"
        print_success "Desktop entry installed"
    fi
fi

echo
echo "========================================"
echo "🎉 Setup Complete!"
echo "========================================"
echo
echo "VoiceMaster Pro is now ready to use on Linux!"
echo
echo "Next steps:"
echo "1. Run: ./launch_voicemaster.sh"
echo "2. Enter your Eleven Labs API key when prompted"
echo "3. Start using your custom voices!"
echo
echo "✨ Need an API key? Visit: https://elevenlabs.io"
echo "   Go to Profile → API Key to get yours"
echo
echo "🐧 Linux-specific notes:"
echo "• Audio system: Make sure your audio is working"
echo "• Microphone: Required for Speech-to-Clone feature"
echo "• Display: Tested with X11 and Wayland"
echo
read -p "Press Enter to continue..."