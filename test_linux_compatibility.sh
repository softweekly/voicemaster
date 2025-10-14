#!/bin/bash

# VoiceMaster Pro - Linux Compatibility Test
# This script tests various aspects of Linux compatibility

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "   $1"
}

echo -e "${BLUE}🐧 VoiceMaster Pro - Linux Compatibility Test${NC}"
echo "==========================================================="

# Test 1: Basic System Information
print_header "📋 System Information"
echo "Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || echo "Unknown")"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Desktop: ${XDG_CURRENT_DESKTOP:-Unknown}"
echo "Display Server: ${XDG_SESSION_TYPE:-Unknown}"
echo

# Test 2: Python Installation
print_header "🐍 Python Installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Python found: $PYTHON_VERSION"
    
    # Check Python version
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        print_success "Python version is compatible (3.8+)"
    else
        print_error "Python 3.8+ required"
    fi
else
    print_error "Python3 not found"
fi
echo

# Test 3: Required System Packages
print_header "📦 System Dependencies"

# Test tkinter
if python3 -c "import tkinter" 2>/dev/null; then
    print_success "tkinter available"
else
    print_error "tkinter not found"
    print_info "Install: sudo apt install python3-tk (Ubuntu/Debian)"
    print_info "Install: sudo dnf install python3-tkinter (Fedora)"
fi

# Test audio libraries
if pkg-config --exists alsa 2>/dev/null; then
    print_success "ALSA development libraries found"
else
    print_warning "ALSA dev libraries not found"
    print_info "Install: sudo apt install libasound2-dev"
fi

if pkg-config --exists portaudio-2.0 2>/dev/null; then
    print_success "PortAudio development libraries found"
else
    print_warning "PortAudio dev libraries not found"
    print_info "Install: sudo apt install portaudio19-dev"
fi

echo

# Test 4: Audio System
print_header "🔊 Audio System"

# Test PulseAudio
if command -v pulseaudio &> /dev/null; then
    if pulseaudio --check 2>/dev/null; then
        print_success "PulseAudio running"
    else
        print_warning "PulseAudio not running"
    fi
else
    print_info "PulseAudio not found (may be using ALSA directly)"
fi

# Test ALSA
if [ -f /proc/asound/cards ]; then
    SOUND_CARDS=$(cat /proc/asound/cards | grep -c ":")
    if [ "$SOUND_CARDS" -gt 0 ]; then
        print_success "ALSA sound cards detected: $SOUND_CARDS"
    else
        print_warning "No ALSA sound cards found"
    fi
else
    print_warning "ALSA not available"
fi

echo

# Test 5: Display System
print_header "🖥️  Display System"

if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    print_info "Wayland display server detected"
    if command -v Xwayland &> /dev/null; then
        print_success "XWayland available (tkinter compatibility)"
    else
        print_warning "XWayland not found (may affect tkinter)"
    fi
elif [ "$XDG_SESSION_TYPE" = "x11" ]; then
    print_success "X11 display server (full compatibility)"
else
    print_info "Unknown display server: ${XDG_SESSION_TYPE:-none}"
fi

# Test DISPLAY variable
if [ -n "$DISPLAY" ]; then
    print_success "DISPLAY environment variable set: $DISPLAY"
else
    print_warning "DISPLAY not set (may affect GUI)"
fi

echo

# Test 6: File Permissions
print_header "🔐 File Permissions"

if [ -f "setup_linux.sh" ]; then
    if [ -x "setup_linux.sh" ]; then
        print_success "setup_linux.sh is executable"
    else
        print_warning "setup_linux.sh not executable"
        print_info "Fix: chmod +x setup_linux.sh"
    fi
else
    print_error "setup_linux.sh not found"
fi

if [ -f "launch_voicemaster_linux.sh" ]; then
    if [ -x "launch_voicemaster_linux.sh" ]; then
        print_success "launch_voicemaster_linux.sh is executable"
    else
        print_warning "launch_voicemaster_linux.sh not executable"
        print_info "Fix: chmod +x launch_voicemaster_linux.sh"
    fi
else
    print_error "launch_voicemaster_linux.sh not found"
fi

echo

# Test 7: Virtual Environment
print_header "🔧 Virtual Environment"

if [ -d ".venv" ]; then
    print_success "Virtual environment directory exists"
    
    if [ -f ".venv/bin/python" ]; then
        print_success "Python executable found in venv"
        
        # Test venv python
        VENV_PYTHON_VERSION=$(.venv/bin/python --version 2>&1)
        print_success "Venv Python: $VENV_PYTHON_VERSION"
    else
        print_error "Python executable not found in venv"
    fi
    
    if [ -f ".venv/bin/activate" ]; then
        print_success "Activation script exists"
    else
        print_error "Activation script not found"
    fi
else
    print_info "Virtual environment not created yet"
    print_info "Will be created by setup_linux.sh"
fi

echo

# Test 8: Internet Connectivity
print_header "🌐 Internet Connectivity"

if ping -c 1 8.8.8.8 &> /dev/null; then
    print_success "Internet connectivity working"
    
    if ping -c 1 pypi.org &> /dev/null; then
        print_success "PyPI reachable (for package installation)"
    else
        print_warning "PyPI not reachable"
    fi
    
    if ping -c 1 api.elevenlabs.io &> /dev/null; then
        print_success "Eleven Labs API reachable"
    else
        print_warning "Eleven Labs API not reachable"
    fi
else
    print_error "No internet connectivity"
fi

echo

# Test 9: Microphone (for Speech-to-Clone)
print_header "🎙️  Microphone Test"

if command -v arecord &> /dev/null; then
    MIC_DEVICES=$(arecord -l 2>/dev/null | grep -c "card")
    if [ "$MIC_DEVICES" -gt 0 ]; then
        print_success "Microphone devices detected: $MIC_DEVICES"
    else
        print_warning "No microphone devices found"
    fi
else
    print_warning "arecord not available (ALSA utils)"
    print_info "Install: sudo apt install alsa-utils"
fi

echo

# Summary
print_header "📊 Compatibility Summary"
echo "==========================================================="

echo "System: $(lsb_release -d 2>/dev/null | cut -f2 || uname -s)"
echo "Python: $(python3 --version 2>&1 || echo "Not found")"
echo "Display: ${XDG_SESSION_TYPE:-Unknown}"
echo "Audio: $(if pulseaudio --check 2>/dev/null; then echo "PulseAudio"; elif [ -f /proc/asound/cards ]; then echo "ALSA"; else echo "Unknown"; fi)"

echo
echo "🎯 Readiness Assessment:"

# Check critical requirements
critical_ok=true

if ! command -v python3 &> /dev/null; then
    critical_ok=false
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    critical_ok=false
fi

if [ "$critical_ok" = true ]; then
    print_success "System appears ready for VoiceMaster Pro!"
    echo
    echo "Next steps:"
    echo "1. Run: chmod +x setup_linux.sh && ./setup_linux.sh"
    echo "2. Run: ./launch_voicemaster_linux.sh"
    echo "3. Enter your Eleven Labs API key"
else
    print_warning "System needs some preparation"
    echo
    echo "Please install missing components and run this test again"
fi

echo
echo "For detailed setup instructions, see: LINUX_SETUP_GUIDE.md"