import os
import gc
from tqdm import tqdm
from blur_detector import blur_detector
import shutil

def evaluate_folder(src_folder_path, camera_id=None, expected_label=None, output_folder_path=None):
    """
    Evaluate all images and videos in a folder, checking if they are blurry or clear.
    """
    if not os.path.exists(src_folder_path):
        raise FileNotFoundError(f"The source folder {src_folder_path} does not exist.")
    if expected_label not in ['blur', 'clear', None]:
        raise ValueError("Expected label must be 'blur', 'clear', or None.")
    if os.path.exists(output_folder_path):
        # Clear the directory
        for filename in os.listdir(output_folder_path):
            file_path = os.path.join(output_folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(output_folder_path)
    
    if expected_label is None and output_folder_path is None:
        print("No expected label provided, and no output folder specified. Exiting evaluation.")
        exit(0)

    elif expected_label is None and output_folder_path is not None:
        files = (f for f in os.listdir(src_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mov', '.mkv')))
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(src_folder_path, file)
            _, annotated_img = blur_detector(file_path, camera_id=camera_id, output_annotation=True)
            if annotated_img is not None:
                annotated_img.save(os.path.join(output_folder_path, os.path.splitext(file)[0] + '_annotated.png'))
                annotated_img.close()  # Explicitly close PIL image
            del annotated_img, file_path
            gc.collect()

    elif expected_label is not None and output_folder_path is None:
        files = (f for f in os.listdir(src_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mov', '.mkv')))
        num_correct_labels = 0
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(src_folder_path, file)
            result, _ = blur_detector(file_path, camera_id=camera_id)
            if result == expected_label:
                num_correct_labels += 1
            del file_path, result
            gc.collect()
        print(f"Number of files with expected label '{expected_label}': {num_correct_labels} out of {len(os.listdir(src_folder_path))}")
        print(f"Accuracy: {num_correct_labels / len(os.listdir(src_folder_path)) * 100:.2f}%")

    elif expected_label is not None and output_folder_path is not None:
        files = (f for f in os.listdir(src_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mov', '.mkv')))
        num_correct_labels = 0
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(src_folder_path, file)
            result, annotated_img = blur_detector(file_path, camera_id=camera_id, output_annotation=True)
            if result == expected_label:
                num_correct_labels += 1
            if annotated_img is not None:
                annotated_img.save(os.path.join(output_folder_path, os.path.splitext(file)[0] + '_annotated.png'))
                annotated_img.close()  # Explicitly close PIL image
            del file_path, annotated_img, result
            gc.collect()
        print(f"Number of files with expected label '{expected_label}': {num_correct_labels} out of {len(os.listdir(src_folder_path))}")
        print(f"Accuracy: {num_correct_labels / len(os.listdir(src_folder_path)) * 100:.2f}%")

    else:
        raise ValueError("Invalid combination of expected_label and output_folder_path.")



