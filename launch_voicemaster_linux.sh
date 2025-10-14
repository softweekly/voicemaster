#!/bin/bash

# VoiceMaster Pro - Linux Launcher Script
# Simple launcher that handles environment setup and credential detection

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo "   VoiceMaster Pro - Starting..."
echo -e "========================================${NC}"

# Check if virtual environment exists
if [ ! -f ".venv/bin/python" ]; then
    echo -e "${RED}ERROR: Virtual environment not found!${NC}"
    echo "Please run setup_linux.sh first to create the virtual environment."
    echo
    echo "Quick setup:"
    echo "  chmod +x setup_linux.sh"
    echo "  ./setup_linux.sh"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if we can activate the virtual environment
if [ ! -f ".venv/bin/activate" ]; then
    echo -e "${RED}ERROR: Virtual environment activation script not found!${NC}"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Verify Python is working
if ! .venv/bin/python -c "import sys; print('Python', sys.version)" 2>/dev/null; then
    echo -e "${RED}ERROR: Python virtual environment is broken!${NC}"
    echo "Try running setup_linux.sh again"
    exit 1
fi

# Check for required packages
echo "Checking required packages..."
missing_packages=()

if ! .venv/bin/python -c "import tkinter" 2>/dev/null; then
    missing_packages+=("tkinter")
fi

if ! .venv/bin/python -c "import requests" 2>/dev/null; then
    missing_packages+=("requests")
fi

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo -e "${RED}ERROR: Missing required packages: ${missing_packages[*]}${NC}"
    echo "Please run setup_linux.sh to install dependencies"
    exit 1
fi

# Check if .env file exists, if not launch login GUI first
if [ ! -f ".env" ]; then
    echo
    echo -e "${BLUE}No credentials found. Launching setup wizard...${NC}"
    echo "This will help you configure your Eleven Labs API key."
    echo
    .venv/bin/python login_gui.py
else
    echo
    echo -e "${GREEN}Credentials found. Launching VoiceMaster Pro...${NC}"
    echo
    .venv/bin/python voicemaster_gui.py
fi

echo
echo -e "${BLUE}VoiceMaster Pro has closed.${NC}"
echo "Thanks for using VoiceMaster Pro!"