import os
import sys
import argparse
import subprocess
import yt_dlp

# Импортируйте TEMP_DIR из temp_dir.py
from temp_dir import TEMP_DIR

def download_video(url, temp_dir):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'merge_output_format': None,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_video(input_path, output_path, fps):
    command = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'hevc_nvenc',  # Используем кодек hevc_nvenc
        '-preset', 'fast',    # Быстрая предустановка для кодирования
        '-an',                # Выключаем аудиотрек
    ]
    
    if fps:
        command.extend(['-r', str(fps)])
    
    command.append(output_path)
    
    subprocess.run(command, check=True)

def cleanup_temp_directory(temp_dir):
    """Удаляет все файлы и директории в указанной временной директории."""
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(temp_dir)

def main():
    parser = argparse.ArgumentParser(description='Download and convert YouTube video.')
    parser.add_argument('--url', required=True, help='URL of the video to download')
    parser.add_argument('--output-dir', required=True, help='Directory to save the converted video')
    parser.add_argument('--fps', type=float, default=None, help='Frames per second for conversion')

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' does not exist.")
        sys.exit(1)

    # Create the temporary directory if it does not exist
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Download video
    try:
        download_video(args.url, TEMP_DIR)
    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)

    # Convert the downloaded video
    downloaded_files = [f for f in os.listdir(TEMP_DIR) if os.path.isfile(os.path.join(TEMP_DIR, f))]
    if not downloaded_files:
        print("No video files found in the temporary directory.")
        sys.exit(1)

    for file_name in downloaded_files:
        input_path = os.path.join(TEMP_DIR, file_name)
        output_file_name = os.path.splitext(file_name)[0] + '.mp4'
        output_path = os.path.join(output_dir, output_file_name)

        try:
            convert_video(input_path, output_path, args.fps)
        except subprocess.CalledProcessError as e:
            print(f"Error converting video: {e}")
            sys.exit(1)

    # Cleanup
    try:
        cleanup_temp_directory(TEMP_DIR)
    except Exception as e:
        print(f"Error cleaning up temporary directory: {e}")
        sys.exit(1)

    print("Conversion completed successfully.")

if __name__ == '__main__':
    main()
