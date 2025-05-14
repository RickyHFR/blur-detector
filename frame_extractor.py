import subprocess
import os

import subprocess
import os

def ffmpeg_extract_interval(video_path, output_dir, interval_sec=1.0, fmt="jpg"):
    """
    Uses ffmpeg to extract frames at a fixed rate.

    :param video_path: Path to MP4 video.
    :param output_dir: Directory where frames will go.
    :param interval_sec: Seconds between each output frame.
    :param fmt: Image format (jpg/png).
    """
    os.makedirs(output_dir, exist_ok=True)

    # -vf fps=1/interval: one frame every `interval_sec` seconds
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{interval_sec}",
        "-q:v", "2",                            # quality for JPEG (1–31, lower = better)
        os.path.join(output_dir, f"frame_%04d.{fmt}")
    ]
    subprocess.run(cmd, check=True)
    print(f"ffmpeg extraction complete into '{output_dir}'")

# Example usage:
ffmpeg_extract_interval("test_videos/test_vid1.mp4", "./ff_frames", interval_sec=0.5)
