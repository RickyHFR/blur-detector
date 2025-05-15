import cv2
import numpy as np
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions

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
    cropped_regions = [crop_chimney_regions(frame, camera_id) for frame in frames]
    score = 0
    for frame_idx in range(len(frames)):
        for region in cropped_regions[frame_idx]:
            if internal_blur_engine(region) == "blur":
                score += 1
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
    video_path = "test_videos/test_vid3.mp4"
    camera_id = "jtc3"
    is_blurry = blur_detector(video_path, camera_id)
    print(f"Is the video blurry? {'Yes' if is_blurry else 'No'}")