import os
import shutil

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import gc

from blur_detector import blur_detector, extract_camera_id
from frame_extractor import crop_chimney_regions, label_regions, ffmpeg_extract_interval
from blur_fire_test import compute_tail_heaviness

def eval_folder(image_folder, camera_id=None, threshold = 10.0, save_anotated_dir="anotated_images", ground_truth="blur"):
    """
    Evaluate all images and videos in a folder using the blur detection tool.
    """
    # Clear the target folder at the beginning
    if os.path.exists(save_anotated_dir):
        shutil.rmtree(save_anotated_dir)
    os.makedirs(save_anotated_dir, exist_ok=True)

    image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    video_files = [f for f in os.listdir(image_folder) if f.endswith((".mp4", ".avi", ".mov", ".mkv"))]
    num_correct_labels = 0
    count = 0
    
    # Process images
    for image_name in tqdm(image_files, desc="Processing images"):
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path)
        current_camera_id = extract_camera_id(image_path) if camera_id is None else camera_id
        count += 1
        cropped_regions = crop_chimney_regions(image, current_camera_id)

        # Prepare to draw on a copy of the image
        annotated_img = image.convert("RGB").copy()

        # Calculate the average tail heaviness for the cropped regions
        region_scores = []
        for region in cropped_regions:
            tail_heaviness = compute_tail_heaviness(region, use_sobel=True)
            region_scores.append(tail_heaviness)
        annotated_img, pred = label_regions(annotated_img, current_camera_id, region_scores, threshold)

        # Save annotated image
        annotated_img.save(os.path.join(save_anotated_dir, image_name))

        if ground_truth == pred:
            num_correct_labels += 1
            del image, current_camera_id, region_scores, cropped_regions, tail_heaviness, annotated_img
            gc.collect()

    # Process videos
    for video_name in tqdm(video_files, desc="Processing videos"):
        video_path = os.path.join(image_folder, video_name)
        current_camera_id = extract_camera_id(video_path) if camera_id is None else camera_id
        count += 1
        frames = ffmpeg_extract_interval(video_path, interval_sec=10.0)
        image = frames[0] if frames else None
        if image is None:
            print(f"Warning: No frames extracted from video {video_name}. Skipping.")
            continue
        cropped_regions = crop_chimney_regions(image, current_camera_id)

        # Prepare to draw on a copy of the image
        annotated_img = image.convert("RGB").copy()

        # Calculate the average tail heaviness for the cropped regions
        region_scores = []
        for region in cropped_regions:
            tail_heaviness = compute_tail_heaviness(region, use_sobel=True)
            region_scores.append(tail_heaviness)
        annotated_img, pred = label_regions(annotated_img, current_camera_id, region_scores, threshold)

        # Save annotated image
        img_save_name = video_name
        base, _ = os.path.splitext(img_save_name)
        img_save_name = base + ".png"
        annotated_img.save(os.path.join(save_anotated_dir, img_save_name))

        if ground_truth == pred:
            num_correct_labels += 1
            del image, cropped_regions, annotated_img, region_scores
            gc.collect()

    print(f"Accuracy for {image_folder}: {num_correct_labels}/{count} ({(num_correct_labels / count) * 100:.2f}%)")

    
if __name__ == "__main__":
    folder = "test_vid_in_progress/enlarged_images/blur_with_flare/png_form/tb4_png"
    target_folder = folder + "/annotated"
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist.")
        exit(1)
    eval_folder(folder, camera_id='tb4', threshold=10.0, save_anotated_dir=target_folder, ground_truth="blur")

