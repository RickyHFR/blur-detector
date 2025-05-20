from blur_detector import blur_detector, extract_camera_id, internal_blur_engine
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

def inspect_video(video_path):
    """
    Inspect a video by displaying its frames at specified intervals.
    
    Parameters
    ----------
    video_path : str
        Path to the input video file.
    interval_sec : float
        Seconds between each output frame.
    """
    frames = ffmpeg_extract_interval(video_path)
    first_frame = frames[0]
    camera_id = extract_camera_id(video_path)
    cropped_regions = crop_chimney_regions(first_frame, camera_id)

    # show all cropped regions
    for i, frame in enumerate(cropped_regions):
        plt.imshow(frame)
        plt.title(f"Region {i}" + f" (Detector Result: {internal_blur_engine(frame)})")
        plt.axis('off')
        plt.show()

    # print(f"Overall Detector Result: {blur_detector(video_path, camera_id, chimney_num=0)}")

if __name__ == "__main__":
    video_path = "test_vid_in_progress/blur/ad1_Feb_5_1.mp4"
    inspect_video(video_path)
