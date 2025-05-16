import ffmpeg

def extract_segment(input_path, start_time, duration_sec, output_path):
    """
    - input_path: path to your long video
    - start_time: string “MM:SS” or “HH:MM:SS” (e.g. “12:34” for 12m34s in)
    - duration_sec: how many seconds to extract
    - output_path: where to save the clip
    """
    (
        ffmpeg
        .input(input_path, ss=start_time)
        .output(output_path, t=duration_sec, c='copy')
        .run(overwrite_output=True)
    )

if __name__ == "__main__":
    extract_segment(
        input_path='test_vid_in_progress/00000003573000000.mp4',
        start_time='01:32:52',
        duration_sec=10,
        output_path='test_vid_in_progress/clear/tb1_Jan_31_2.mp4'
    )