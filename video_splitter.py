import ffmpeg
import os

def extract_segment(input_path, start_time, duration_sec, output_path):
    """
    Extract a segment from a video file using ffmpeg.
    """
    (
        ffmpeg
        .input(input_path, ss=start_time)
        .output(output_path, t=duration_sec, c='copy')
        .run(overwrite_output=True)
    )

if __name__ == "__main__":
    input_path = 'test_vid_in_progress/00000001571000000.mp4'
    start_time = '01:55:55'
    duration_sec = 10
    base_output = 'test_vid_in_progress/intermediate/tb1_Mar_1_'
    ext = '.mp4'

    num = 1
    while True:
        output_path = f"{base_output}{num}{ext}"
        if not os.path.exists(output_path):
            break
        num += 1

    extract_segment(
        input_path=input_path,
        start_time=start_time,
        duration_sec=duration_sec,
        output_path=output_path
    )