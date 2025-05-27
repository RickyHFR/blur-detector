from blur_detector import blur_detector, extract_camera_id, internal_blur_engine
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions
import matplotlib.pyplot as plt
import numpy as np
import os


def inspect_video(video_path, region_id, camera_id=None):
    frames = ffmpeg_extract_interval(video_path)
    first_frame = frames[1]
    # show the first frame
    plt.imshow(first_frame)
    plt.title("First Frame")
    plt.axis('off')
    plt.show()

    if camera_id is None:
        camera_id = extract_camera_id(video_path)
    cropped_regions = crop_chimney_regions(first_frame, camera_id)
    # region = cropped_regions[region_id]
    # # show the cropped region
    # plt.imshow(region)
    # plt.title(f"Region {region_id} | Detector Result: {internal_blur_engine(region)}")
    # plt.axis('off')
    # plt.show()

    # show all cropped regions
    for i, frame in enumerate(cropped_regions):
        # plt.imshow(frame)
        # plt.title(f"Region {i}" + f" (Detector Result: {internal_blur_engine(frame)})")
        # plt.axis('off')
        # plt.show()
        internal_blur_engine(frame)

    # print(f"Overall Detector Result: {blur_detector(video_path, camera_id, interval_sec=10.0, chimney_num=-1)}")

if __name__ == "__main__":
    # video_path = "test_videos/smoke_start_c1_2025-05-23_083859.mp4"
    video_path = "test_vid_in_progress/blur/ad3_Mar_6_3.mp4"
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    inspect_video(video_path, region_id=1, camera_id='ad3')

