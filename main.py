import os
import subprocess
from tkinter import Tk, filedialog

def compress_video_ffmpeg(input_path, output_path, crf=23):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", str(crf),
        "-preset", "slow",  # Better compression
        "-acodec", "copy",  # Keep original audio
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✔️ Compressed: {os.path.basename(input_path)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compressing {input_path}: {e}")

def main():
    root = Tk()
    root.withdraw()

    files = filedialog.askopenfilenames(
        title="Select Video Files",
        filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv *.webm")]
    )

    if not files:
        print("No files selected.")
        return

    output_folder = "compressed_videos"
    os.makedirs(output_folder, exist_ok=True)

    for file_path in files:
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_compressed{ext}")
        compress_video_ffmpeg(file_path, output_path, crf=23)

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
