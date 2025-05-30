import numpy as np
from PIL import Image
from frame_extractor import ffmpeg_extract_interval, crop_chimney_regions, label_regions
from compute_tail_heaviness import compute_tail_heaviness
import gc

def extract_camera_id(src_path):
    """
    Extract the camera ID from the source path (Assuming the camera ID is the first part of the filename before an underscore).
    """
    cam_id = src_path.split('/')[-1].split('_')[0]
    if cam_id.startswith('adm'):
        cam_id = 'ad' + cam_id[3:]
    return cam_id

def blur_detector(src_path, camera_id=None, interval_sec=1.0, threshold=10.0, ad4_threshold=1.0, output_annotation=False):
    """
    Determine if a media (image/video) is blurry and return a boolean value.
    """
    mode = None  # 'video' or 'image'
    if src_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        mode = 'video' if mode is None else mode
    elif src_path.endswith(('.png', '.jpg', '.jpeg')):
        mode = 'image' if mode is None else mode
    else:
        raise ValueError("Unsupported file type. Please provide a video or image file.")
    if mode == 'video' and interval_sec <= 0:
        raise ValueError("Interval must be a positive number for video mode.")
    if camera_id is None:
        camera_id = extract_camera_id(src_path)
        if camera_id == 'ad4':
            threshold = ad4_threshold
    elif camera_id not in ['ad1', 'ad3', 'ad4', 'smk1', 'smk2', 'jtc1', 'jtc2', 'jtc3', 'jtc4', 'tb1', 'tb2', 'tb3', 'tb4']:
        raise ValueError(f"Invalid camera_id: {camera_id}. Valid IDs are: ['ad1', 'ad3', 'ad4', 'smk1', 'smk2', 'jtc1', 'jtc2', 'jtc3', 'jtc4', 'tb1', 'tb2', 'tb3', 'tb4']")

    if mode == 'video':
        frames = ffmpeg_extract_interval(src_path, interval_sec)
        cropped_regions = [crop_chimney_regions(frame, camera_id) for frame in frames]
        if len(frames) == 0:
            raise ValueError("No frames extracted from the video.")
        if len(cropped_regions[0]) == 0:
            raise ValueError("No cropped regions found for the given camera ID.")
        if output_annotation:
            annotated_img = frames[0].convert("RGB").copy()
        blur_score = 0
        total_region_num = 0
        if output_annotation:
            region_scores = []
        for frame_idx in range(len(frames)):
            for region in cropped_regions[frame_idx]:
                blur_score += compute_tail_heaviness(region, detect_fire=True)
                total_region_num += 1
        if total_region_num == 0:
            raise ValueError("No regions to analyze for blurriness.")
        if output_annotation:
            for region in cropped_regions[0]:
                tail_heaviness = compute_tail_heaviness(region, detect_fire=True)
                region_scores.append(tail_heaviness)
            annotated_img, _ = label_regions(annotated_img, camera_id, region_scores, threshold)
        del frames, cropped_regions
        gc.collect()
        return "clear" if blur_score > threshold else "blur", annotated_img if output_annotation else None

    else:
        image = Image.open(src_path)
        cropped_regions = crop_chimney_regions(image, camera_id)
        if len(cropped_regions) == 0:
            raise ValueError("No cropped regions found for the given camera ID.")
        if output_annotation:
            annotated_img = image.convert("RGB").copy()
        region_scores = []
        for region in cropped_regions:
            tail_heaviness = compute_tail_heaviness(region, detect_fire=True)
            region_scores.append(tail_heaviness)
        blur_score = np.mean(region_scores)
        if output_annotation:
            annotated_img, _ = label_regions(annotated_img, camera_id, region_scores, threshold)
        del image, cropped_regions
        gc.collect()
        return "clear" if blur_score > threshold else "blur", annotated_img if output_annotation else None
