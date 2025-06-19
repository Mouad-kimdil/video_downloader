# Video Downloader

A simple Python script to download videos and audio from various platforms using yt-dlp.

## Features

- Download videos in MP4 format with quality selection
- Extract audio in MP3 format
- Support for multiple video platforms (YouTube, Vimeo, and many others)
- Interactive quality selection with file size information
- **Playlist support with sequential ordering**
- **Custom download location selection**
- **Playlist limit control (download specific number of videos)**
- **Graceful interruption handling (Ctrl+C preserves downloaded files)**
- **Sequential file numbering for playlists (01 - Title.mp3, 02 - Title.mp3, etc.)**

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

### Single Video Download
```
Enter the video URL: https://www.youtube.com/watch?v=example
Choose format (mp4 for video, mp3 for audio): mp4
Enter download path (or press Enter for current directory): ~/Downloads
📁 Videos will be saved to: /Users/username/Downloads

Available qualities:
1: format_id=137 - ext=mp4 - 1080p - 45.2 MB
2: format_id=136 - ext=mp4 - 720p - 28.1 MB
3: format_id=135 - ext=mp4 - 480p - 15.3 MB

Select quality (number): 1
✅ Download complete!
```

### Playlist Download
```
Enter the video URL: https://www.youtube.com/playlist?list=example
Choose format (mp4 for video, mp3 for audio): mp3
Enter number of videos to download (or press Enter for all): 23
Enter download path (or press Enter for current directory): ~/Music
📁 Videos will be saved to: /Users/username/Music
🔍 Getting playlist information...
📋 Found 23 videos to download

🎵 [1/23] Downloading: Song Title 1
✅ Downloaded: Song Title 1

🎵 [2/23] Downloading: Song Title 2
✅ Downloaded: Song Title 2
...
🎉 Download complete! 23 videos saved.
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

- **Custom Download Location**: Choose where to save your files
- **Playlist Ordering**: Downloads maintain the exact playlist order
- **Sequential Numbering**: Playlist files are numbered (01 - Title.mp3, 02 - Title.mp3, etc.)
- **Interruption Safe**: Press Ctrl+C to stop - already downloaded files are preserved
- **Audio Quality**: MP3 downloads are extracted at 192 kbps quality
- **Video Quality**: High-quality video downloads may require merging separate video and audio streams
- **Directory Creation**: Script can create download directories if they don't exist
=======
- Downloaded files are saved in the same directory as the script
- For MP3 downloads, audio is extracted at 192 kbps quality
- High-quality video downloads may require merging separate video and audio streams

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
