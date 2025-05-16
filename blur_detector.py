import cv2
import numpy as np
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions

def extract_camera_id(video_path):
    """
    Extract the camera ID from the video path.
    
    Parameters
    ----------
    video_path : str
        Path to the input video file.
    
    Returns
    -------
    str
        The camera ID extracted from the video path.
    """
    # Assuming the camera ID is the first part of the filename before an underscore
    return video_path.split('/')[-1].split('_')[0]

def test_pipeline():
    video_path = 'test_vid_in_progress/clear/ad1_Feb_5_1.mp4'
    camera_id = extract_camera_id(video_path)
    interval_sec = 1.0
    # Test the blur detector
    is_blurry = blur_detector(video_path, camera_id, interval_sec)
    print(f"Is the video blurry? {'Yes' if is_blurry else 'No'}")

def blur_detector(video_path, camera_id, interval_sec = 1.0):
    """
    Determine if a video is blurry and return a boolean value.
    
    Parameters
    ----------
    video_path : str
        Path to the input video file.
    interval_sec : float
        Seconds between each output frame.
    camera_id : int
        Camera ID for the video.
    """

    frames = ffmpeg_extract_interval(video_path, interval_sec)

    print(f"Number of frames extracted: {len(frames)}") # TODO: remove this

    cropped_regions = [crop_chimney_regions(frame, camera_id) for frame in frames]

    print(f"Total frames being cropped: {len(cropped_regions)}") # TODO: remove this
    print(f"Number of cropped regions per frame: {len(cropped_regions[0])}") # TODO: remove this

    score = 0
    for frame_idx in range(len(frames)):
        for region in cropped_regions[frame_idx]:
            if internal_blur_engine(region) == "blur":
                print(f"Frame {frame_idx}: {region}") # TODO: remove this
                score += 1
    print(f"Total score: {score}") # TODO: remove this
    print(f"Total cropped regions: {len(cropped_regions) * len(cropped_regions[0])}") # TODO: remove this
    return score > 0.5 * len(cropped_regions) * len(cropped_regions[0])

def internal_blur_engine(image, threshold=0.1):
    """
    Detect blurriness in an image using FFT and a threshold.

    Parameters
    ----------
    image : np.ndarray
        The input image to be analyzed.
    threshold : float
        The threshold for determining blurriness.
       Default is 0.1. 
    """
    region = np.array(image)
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.abs(fshift)

    sorted_magnitude = np.sort(magnitude_spectrum.flatten())
    cutoff_index = int(len(sorted_magnitude) * 0.9)
    cutoff_value = sorted_magnitude[cutoff_index]

    magnitude_spectrum[magnitude_spectrum > cutoff_value] = 0

    high_freq_ratio = np.sum(magnitude_spectrum > 100) / magnitude_spectrum.size

    is_blurry = high_freq_ratio < threshold
    return "blur" if is_blurry else "clear"

if __name__ == "__main__":
    test_pipeline()