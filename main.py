import os
from blur_detector import blur_detector, extract_camera_id
from frame_extractor import ffmpeg_extract_interval
import matplotlib.pyplot as plt
import numpy as np

def evaluate_folder(folder_path, expected_label, interval_sec=1.0):
    total = 0
    correct = 0
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            continue
        video_path = os.path.join(folder_path, filename)
        camera_id = extract_camera_id(video_path)
        print(f"Evaluating: {video_path}")
        is_blur = blur_detector(video_path, camera_id, interval_sec)
        pred_label = 'blur' if is_blur else 'clear'
        print(f"Predicted: {pred_label}, Ground Truth: {expected_label}")
        if pred_label == expected_label:
            correct += 1
        # else:
        #     # Display the first frame of the wrongly predicted video
        #     frames = ffmpeg_extract_interval(video_path, interval_sec)
        #     if frames:
        #         frame_np = np.array(frames[0])
        #         plt.imshow(frame_np)
        #         plt.title(f"Wrong Prediction: {filename}\nPredicted: {pred_label}, GT: {expected_label}")
        #         plt.axis('off')
        #         plt.show()
        total += 1
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



