import yt_dlp

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

def get_video_info(url):
    ydl_opts = {}
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

    filtered_formats = []
    if want_audio_only:
        filtered_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
    else:
        filtered_formats = [f for f in formats if f.get('vcodec') != 'none']

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
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def main():
    url = input("Enter the video URL: ").strip()
    fmt = get_format_choice()

    info = get_video_info(url)
    if not info:
        return

    if fmt == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        format_id = choose_quality(info['formats'], want_audio_only=False)
        selected_format = next(f for f in info['formats'] if f['format_id'] == format_id)
        if selected_format.get('vcodec') != 'none' and selected_format.get('acodec') == 'none':
            ydl_opts = {
                'format': f"{format_id}+bestaudio/best",
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
            }
        else:
            ydl_opts = {
                'format': format_id,
                'outtmpl': '%(title)s.%(ext)s',
            }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("✅ Download complete!")
    except Exception as e:
        print(f"❌ Error during download: {e}")

if __name__ == "__main__":
    main()

