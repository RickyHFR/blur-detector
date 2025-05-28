import os
import shutil

from PIL import Image
from tqdm import tqdm
import gc

from blur_detector import blur_detector, extract_camera_id
from frame_extractor import crop_chimney_regions
from utils.compute_tail_heaviness import compute_tail_heaviness

save_detected_dir = 'NEA_data/wrongly_predicted_images_blur_can_see'
ground_truth = "clear" 

def eval_folder(image_folder):
    """
    Evaluate all images and videos in a folder using the blur detection tool.
    """
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    video_files = [f for f in os.listdir(image_folder) if f.endswith((".mp4", ".avi", ".mov", ".mkv"))]
    num_correct_labels = 0
    count = 0
    wrong_predictions = []
    threshold = 10 
    
    # Process images
    for image_name in tqdm(image_files, desc="Processing images"):
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path)
        cropped_regions = crop_chimney_regions(image, extract_camera_id(image_path))
        if not cropped_regions:
            print(f"No cropped regions found for {image_name}.")
            continue

        # Calculate the average tail heaviness for the cropped regions
        total_tail_heaviness = 0
        for region in cropped_regions:
            tail_heaviness = compute_tail_heaviness(region, use_sobel=True)
            total_tail_heaviness += tail_heaviness
        count += 1
        avg_tail_heaviness = total_tail_heaviness / len(cropped_regions) if cropped_regions else 0
        if (ground_truth == "blur" and avg_tail_heaviness < threshold) or (ground_truth == "clear" and avg_tail_heaviness >= threshold):
            num_correct_labels += 1
            del image, cropped_regions, total_tail_heaviness, avg_tail_heaviness
            gc.collect()
        else:
            # Insert score before file extension to keep a valid image extension
            base, ext = os.path.splitext(image_name)
            image_name_scored = f"{base}_score_{avg_tail_heaviness:.2f}{ext}"
            wrong_predictions.append((image_name_scored, image_path))

    # Process videos
    for video_name in tqdm(video_files, desc="Processing videos"):
        video_path = os.path.join(image_folder, video_name)
        camera_id = extract_camera_id(video_path)
        is_blur = blur_detector(video_path, camera_id, interval_sec=10, save_detected_dir=None)
        pred_label = 'blur' if is_blur else 'clear'
        if ground_truth == pred_label:
            num_correct_labels += 1
        else:
            # Save wrongly predicted video with label in filename
            base, ext = os.path.splitext(video_name)
            video_name_scored = f"{base}_pred_{pred_label}{ext}"
            wrong_predictions.append((video_name_scored, video_path))
        count += 1
        del video_path, camera_id, is_blur, pred_label
        gc.collect()

    print(f"Accuracy for {image_folder}: {num_correct_labels}/{count} ({(num_correct_labels / count) * 100:.2f}%)")

    if wrong_predictions:
        # Clear the save_detected_dir before saving new results
        if os.path.exists(save_detected_dir):
            shutil.rmtree(save_detected_dir)
        os.makedirs(save_detected_dir, exist_ok=True)
        for name, path in wrong_predictions:
            if path.lower().endswith(('.png', '.jpg', '.jpeg')):
                with Image.open(path) as img:
                    img.save(os.path.join(save_detected_dir, name))
            elif path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                shutil.copy2(path, os.path.join(save_detected_dir, name))
            gc.collect()

    
if __name__ == "__main__":
    folder = "NEA_data/blur_can_see"
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist.")
        exit(1)
    eval_folder(folder)

