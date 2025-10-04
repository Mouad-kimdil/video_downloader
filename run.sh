#!/bin/bash

# Video Downloader Runner Script

# Detect operating system
OS="$(uname -s)"

# Install FFmpeg based on OS
install_ffmpeg() {
    case "${OS}" in
        Linux*)
            if command -v apt-get &> /dev/null; then
                echo "Installing FFmpeg on Ubuntu/Debian..."
                sudo apt update && sudo apt install -y ffmpeg
            elif command -v yum &> /dev/null; then
                echo "Installing FFmpeg on CentOS/RHEL..."
                sudo yum install -y ffmpeg
            elif command -v dnf &> /dev/null; then
                echo "Installing FFmpeg on Fedora..."
                sudo dnf install -y ffmpeg
            fi
            ;;
        Darwin*)
            if command -v brew &> /dev/null; then
                echo "Installing FFmpeg on macOS..."
                brew install ffmpeg
            else
                echo "Please install Homebrew first: https://brew.sh"
                exit 1
            fi
            ;;
        *)
            echo "Unsupported OS: ${OS}"
            echo "Please install FFmpeg manually"
            ;;
    esac
}

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg not found. Installing..."
    install_ffmpeg
else
    echo "FFmpeg already installed."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade yt-dlp to latest version
echo "Installing/upgrading yt-dlp..."
pip install --upgrade yt-dlp

# Run the download script
echo "Starting video downloader..."
python download.py

# Deactivate virtual environment
deactivate