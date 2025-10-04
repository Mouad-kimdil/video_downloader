import yt_dlp
import signal
import sys
import os

def format_filesize(bytes_size):
    if not bytes_size:
        return "Unknown size"
    gb = bytes_size / (1024 ** 3)
    mb = bytes_size / (1024 ** 2)
    if gb >= 1:
        return f"{gb:.2f} GB"
    return f"{mb:.2f} MB"

def get_format_choice():
    while True:
        fmt = input("Choose format (mp4 for video, mp3 for audio): ").strip().lower()
        if fmt in ["mp4", "mp3"]:
            return fmt
        print("Invalid format. Please enter 'mp4' or 'mp3'.")

def get_playlist_limit():
    while True:
        try:
            limit = input("Enter number of videos to download (or press Enter for all): ").strip()
            if not limit:
                return None
            limit = int(limit)
            if limit > 0:
                return limit
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

def get_download_path():
    while True:
        path = input("Enter download path (or press Enter for current directory): ").strip()
        if not path:
            return os.getcwd()
        
        path = os.path.expanduser(path)
        
        if os.path.exists(path) and os.path.isdir(path):
            return path
        else:
            create = input(f"Directory '{path}' doesn't exist. Create it? (y/n): ").strip().lower()
            if create in ['y', 'yes']:
                try:
                    os.makedirs(path, exist_ok=True)
                    return path
                except Exception as e:
                    print(f"❌ Failed to create directory: {e}")
            else:
                print("Please enter a valid directory path.")

def get_video_info(url, limit=None):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    if limit:
        ydl_opts['playlistend'] = limit
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except yt_dlp.utils.DownloadError as e:
            if "Unsupported URL" in str(e):
                print("❌ Error: This site is not supported.")
            else:
                print(f"❌ Download error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

def choose_quality(formats, want_audio_only=False):
    if want_audio_only:
        filtered_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
    else:
        filtered_formats = [f for f in formats if f.get('vcodec') != 'none']
    
    if not filtered_formats:
        print("❌ No suitable formats found. Using best available format.")
        return 'best'

    print("\nAvailable qualities:")
    for i, f in enumerate(filtered_formats):
        size = format_filesize(f.get('filesize') or f.get('filesize_approx'))
        note = f.get('format_note') or ''
        res = f.get('resolution') or ''
        fps = f.get('fps')
        fps_str = f"{fps}fps" if fps else ''
        desc = ' '.join(filter(None, [note, res, fps_str]))
        print(f"{i+1}: format_id={f['format_id']} - ext={f.get('ext')} - {desc} - {size}")

    while True:
        try:
            choice = int(input("Select quality (number): ")) - 1
            if 0 <= choice < len(filtered_formats):
                return filtered_formats[choice]['format_id']
        except (ValueError, KeyboardInterrupt):
            if KeyboardInterrupt:
                raise
            pass
        print("Invalid choice. Try again.")

def signal_handler(sig, frame):
    print("\n⚠️  Download interrupted by user. Already downloaded videos are saved.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    url = input("Enter the video URL: ").strip()
    fmt = get_format_choice()
    
    playlist_limit = None
    if 'playlist' in url or 'list=' in url:
        playlist_limit = get_playlist_limit()
    
    download_path = get_download_path()
    print(f"📁 Videos will be saved to: {download_path}")

    print("🔍 Getting playlist information...")
    info = get_video_info(url, playlist_limit)
    if not info:
        return
    if 'entries' in info:
        entries = [entry for entry in info['entries'] if entry is not None]
        
        print(f"📋 Found {len(entries)} videos to download")
        
        downloaded_count = 0
        for i, entry in enumerate(entries, 1):
            video_url = entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry['id']}"
            title = entry.get('title', 'Unknown')
            
            print(f"\n🎵 [{i}/{len(entries)}] Downloading: {title}")
            
            ydl_opts = {
                'outtmpl': os.path.join(download_path, f'{i:02d} - %(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if fmt == "mp3" else [],
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                    downloaded_count += 1
                    print(f"✅ Downloaded: {title}")
            except KeyboardInterrupt:
                print(f"\n⚠️  Download interrupted. {downloaded_count} videos saved.")
                return
            except Exception as e:
                print(f"❌ Failed to download: {title} - {e}")
                continue
        
        print(f"\n🎉 Download complete! {downloaded_count} videos saved.")
    else:
        base_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
        }

        if fmt == "mp3":
            ydl_opts = {
                **base_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            format_id = choose_quality(info['formats'], want_audio_only=False)
            if format_id == 'best':
                ydl_opts = {
                    **base_opts,
                    'format': 'best[ext=mp4]/best',
                }
            else:
                selected_format = next((f for f in info['formats'] if f['format_id'] == format_id), None)
                if selected_format and selected_format.get('vcodec') != 'none' and selected_format.get('acodec') == 'none':
                    ydl_opts = {
                        **base_opts,
                        'format': f"{format_id}+bestaudio/best",
                        'merge_output_format': 'mp4',
                    }
                else:
                    ydl_opts = {
                        **base_opts,
                        'format': format_id,
                    }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print("✅ Download complete!")
        except KeyboardInterrupt:
            print("\n⚠️  Download interrupted by user. Already downloaded videos are saved.")
        except Exception as e:
            print(f"❌ Error during download: {e}")

if __name__ == "__main__":
    main()

