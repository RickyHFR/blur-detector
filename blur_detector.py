import cv2
import numpy as np
from PIL import Image
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions
from utils.compute_power_spectrum import compute_spectrum_feature
from utils.compute_tail_heaviness import compute_tail_heaviness, zoom_into_point
from utils.compute_directional_kurtosis import compute_kurtosis_score

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

def blur_detector(video_path, camera_id, interval_sec=1.0, chimney_num=-1):
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
    # print(f"Extracted {len(frames)} frames from the video.")
    cropped_regions = [crop_chimney_regions(frame, camera_id) for frame in frames]
    if len(frames) == 0:
        raise ValueError("No frames extracted from the video.")
    if len(cropped_regions[0]) == 0:
        raise ValueError("No cropped regions found for the given camera ID.")
    if chimney_num != -1 and chimney_num >= len(cropped_regions[0]):
        raise ValueError(f"Chimney number {chimney_num} exceeds the number of cropped regions.")
    if chimney_num < -1:
        raise ValueError(f"Chimney number {chimney_num} is invalid. It should be -1 or a non-negative integer.")

    other_count = 0
    focused_count = 0
    focused_total = 0
    other_total = 0

    threshold = 30 if camera_id != 'ad4' else 5
    # threshold = 1.5

    for frame_idx in range(len(frames)):
        for region_idx, region in enumerate(cropped_regions[frame_idx]):
            if camera_id == 'ad1' and (region_idx == 0 or region_idx == 1): # special case for ad1
                continue
            if region_idx == chimney_num:
                focused_total += 1
                if internal_blur_engine(region, threshold) == "blur":
                    focused_count += 1
            else:
                other_total += 1
                if internal_blur_engine(region, threshold) == "blur":
                    other_count += 1
    if focused_total == 0 and other_total != 0:
        return other_count / other_total * 100 > 50
    elif focused_total != 0 and other_total == 0:
        return focused_count / focused_total * 100 > 50
    elif focused_total == 0 and other_total == 0:
        raise ValueError("No regions to analyze.")
    else:
        return focused_count / focused_total * 50 + other_count / other_total * 50 > 50

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

def internal_blur_engine(image, threshold=30):
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
    import matplotlib.pyplot as plt
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
    else:
        pil_image = image

    zoom_point = (pil_image.width // 2, int(pil_image.height * 0.1))

    zoom1 = zoom_into_point(image, zoom_factor=1.5, center=zoom_point)
    zoom2 = zoom_into_point(image, zoom_factor=3.0, center=zoom_point)

    sigma1 = compute_tail_heaviness(pil_image)
    sigma2 = compute_tail_heaviness(zoom1)
    sigma3 = compute_tail_heaviness(zoom2)

    # sigma1 = compute_spectrum_feature(pil_image)
    # sigma2 = compute_spectrum_feature(zoom1)
    # sigma3 = compute_spectrum_feature(zoom2)

    # sigma1 = compute_kurtosis_score(pil_image)
    # sigma2 = compute_kurtosis_score(zoom1)
    # sigma3 = compute_kurtosis_score(zoom2)
    is_blurry = np.mean([sigma1, sigma2, sigma3]) < threshold

    # Display the original and zoomed images after computing tail heaviness
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(pil_image)
    plt.title(f'Original\nσ={sigma1:.2f}')
    plt.axis('off')
    plt.subplot(1, 3, 2)
    plt.imshow(zoom1)
    plt.title(f'Zoom 1.5x\nσ={sigma2:.2f}')
    plt.axis('off')
    plt.subplot(1, 3, 3)
    plt.imshow(zoom2)
    plt.title(f'Zoom 2.0x\nσ={sigma3:.2f}')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return "blur" if is_blurry else "clear"