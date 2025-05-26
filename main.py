import os
from blur_detector import blur_detector, extract_camera_id

def evaluate_folder(folder_path, expected_label, interval_sec=10.0):
    import sys
    total = 0
    correct = 0
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    n_files = len(video_files)
    for idx, filename in enumerate(video_files):
        video_path = os.path.join(folder_path, filename)
        camera_id = extract_camera_id(video_path)
        is_blur = blur_detector(video_path, camera_id, interval_sec)
        pred_label = 'blur' if is_blur else 'clear'
        if pred_label == expected_label:
            correct += 1
        else:
            print(f"\nIncorrect: {filename} | Predicted: {pred_label}, Ground Truth: {expected_label}")
            # inspect_video(video_path)
        total += 1
        # Progress bar
        bar_len = 40
        filled_len = int(round(bar_len * (idx + 1) / n_files))
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write(f'\r[{bar}] {idx + 1}/{n_files}')
        sys.stdout.flush()
    print()  # Newline after progress bar
    accuracy = correct / total if total > 0 else 0
    print(f"Accuracy for {expected_label} folder: {accuracy:.2%} ({correct}/{total})\n")
    return accuracy

if __name__ == "__main__":
    blur_folder = 'test_vid_in_progress/blur'
    clear_folder = 'test_vid_in_progress/clear'
    print("Evaluating blur folder...")
    evaluate_folder(blur_folder, 'blur')
    print("Evaluating clear folder...")
    evaluate_folder(clear_folder, 'clear')



