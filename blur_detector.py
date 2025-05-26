import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions
from utils.compute_tail_heaviness import compute_tail_heaviness

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
    cam_id = video_path.split('/')[-1].split('_')[0]
    if cam_id.startswith('adm'):
        cam_id = 'ad' + cam_id[3:]
    return cam_id

def blur_detector(video_path, camera_id, interval_sec=1.0, threshold=20):
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
    chimney_num : int
        Chimney number to process (default is -1, meaning all chimneys).
    """
    frames = ffmpeg_extract_interval(video_path, interval_sec)
    cropped_regions = [crop_chimney_regions(frame, camera_id) for frame in frames]
    if len(frames) == 0:
        raise ValueError("No frames extracted from the video.")
    if len(cropped_regions[0]) == 0:
        raise ValueError("No cropped regions found for the given camera ID.")

    count = 0
    total = 0

    for frame_idx in range(len(frames)):
        for region_idx, region in enumerate(cropped_regions[frame_idx]):
            total += compute_tail_heaviness(region, use_sobel=True)
            count += 1
    if total == 0:
        raise ValueError("No regions to analyze for blurriness.")
    avg_tail_heaviness = total / count
    return avg_tail_heaviness < threshold

# def internal_blur_engine(image, threshold=0.2):
#     """
#     Detect blurriness in an image using FFT and a threshold.

#     Parameters
#     ----------
#     image : np.ndarray
#         The input image to be analyzed.
#     threshold : float
#         The threshold for determining blurriness.
#        Default is 0.1. 
#     """
#     region = np.array(image)
#     gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
#     f = np.fft.fft2(gray)
#     fshift = np.fft.fftshift(f)
#     magnitude_spectrum = np.abs(fshift)

#     sorted_magnitude = np.sort(magnitude_spectrum.flatten())
#     cutoff_index = int(len(sorted_magnitude) * 0.9)
#     cutoff_value = sorted_magnitude[cutoff_index]

#     magnitude_spectrum[magnitude_spectrum > cutoff_value] = 0

#     high_freq_ratio = np.sum(magnitude_spectrum > 100) / magnitude_spectrum.size

#     is_blurry = high_freq_ratio < threshold
#     return "blur" if is_blurry else "clear"

def internal_blur_engine(image):
    """
    Detect blurriness in an image using Gaussian Mixture Model (GMM) and a threshold.
    Parameters
    ----------
    image : np.ndarray or PIL.Image.Image
        The input image to be analyzed.
    threshold : float
        The threshold for determining blurriness.
        Default is 30.
    """
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
    else:
        pil_image = image
    
    result = compute_tail_heaviness(pil_image, use_sobel=True)

    # Display the original and zoomed images after computing tail heaviness
    plt.figure(figsize=(12, 4))
    plt.imshow(pil_image)
    plt.title(f'Original\nσ={result:.2f}')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return result
