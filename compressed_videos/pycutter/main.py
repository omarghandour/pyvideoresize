import os
import subprocess
from tkinter import Tk, filedialog

def select_video_file():
    """Open a file dialog to select a video file."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")]
    )
    return file_path

def split_video_ffmpeg(input_path, segment_length=500):  # 500s = 10 mins
    """
    Split video into segments with proper audio/video sync.
    """
    if not input_path:
        print("❌ No file selected. Exiting.")
        return

    # Create output directory
    output_dir = os.path.splitext(input_path)[0] + "_segments"
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(input_path))[0]

    # Get video duration
    cmd_probe = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        input_path
    ]
    duration = float(subprocess.check_output(cmd_probe).decode().strip())

    # Split into segments
    segment_num = 1
    for start_time in range(0, int(duration), segment_length):
        end_time = min(start_time + segment_length, duration)
        output_path = os.path.join(
            output_dir,
            f"{basename}_part{segment_num}.mp4"
        )

        # FFmpeg command with re-encoding for clean cuts
        cmd = [
            "ffmpeg",
            "-ss", str(start_time),          # Start time
            "-i", input_path,               # Input file
            "-to", str(end_time - start_time),  # Duration (end - start)
            "-c:v", "libx264",              # Re-encode video
            "-crf", "23",                   # Quality (18-28, lower=better)
            "-preset", "fast",              # Speed/quality trade-off
            "-c:a", "aac",                  # Re-encode audio
            "-b:a", "128k",                 # Audio bitrate
            "-avoid_negative_ts", "make_zero",  # Fix timestamps
            "-y",                          # Overwrite output
            output_path
        ]

        print(f"⏳ Cutting segment {segment_num}...")
        subprocess.run(cmd, check=True)
        print(f"✅ Saved: {output_path}")
        segment_num += 1

    print(f"\n🎉 Successfully split into {segment_num-1} segments in:\n{output_dir}")

if __name__ == "__main__":
    print("🔍 Select a video to split into 10-minute segments")
    video_path = select_video_file()
    split_video_ffmpeg(video_path)