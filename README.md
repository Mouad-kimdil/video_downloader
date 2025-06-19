# Video Downloader

A simple Python script to download videos and audio from various platforms using yt-dlp.

## Features

- Download videos in MP4 format with quality selection
- Extract audio in MP3 format
- Support for multiple video platforms (YouTube, Vimeo, and many others)
- Interactive quality selection
- File size information display

## Requirements

- Python 3.6 or higher
- FFmpeg (for audio conversion)

## Installation

### Option 1: Automated Setup (Recommended for macOS/Linux)

Simply run the setup script:
```bash
chmod +x run.sh
./run.sh
```

The script will automatically:
- Install FFmpeg for your operating system
- Create and activate virtual environment
- Install Python dependencies
- Run the video downloader

### Option 2: Manual Setup

#### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2. Install Python Dependencies

```bash
pip install yt-dlp
```

#### 3. Install FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extract and add to your system PATH

## Usage

### Quick Start (with automated script)
```bash
./run.sh
```

### Manual Usage

1. Activate the virtual environment (if using manual setup):
```bash
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. Run the script:
```bash
python download.py
```

3. Enter the video URL when prompted

4. Choose format:
   - `mp4` for video download
   - `mp3` for audio-only download

5. For video downloads, select your preferred quality from the available options

## Example

```
Enter the video URL: https://www.youtube.com/watch?v=example
Choose format (mp4 for video, mp3 for audio): mp4

Available qualities:
1: format_id=137 - ext=mp4 - 1080p - 45.2 MB
2: format_id=136 - ext=mp4 - 720p - 28.1 MB
3: format_id=135 - ext=mp4 - 480p - 15.3 MB

Select quality (number): 1
✅ Download complete!
```

## Supported Platforms

This script supports hundreds of video platforms including:
- YouTube
- Vimeo
- Dailymotion
- Facebook
- Instagram
- TikTok
- And many more

## Notes

- Downloaded files are saved in the same directory as the script
- For MP3 downloads, audio is extracted at 192 kbps quality
- High-quality video downloads may require merging separate video and audio streams

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
