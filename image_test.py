import os

from matplotlib import pyplot as plt
from PIL import Image
from tqdm import tqdm

from blur_detector import internal_blur_engine, extract_camera_id
from frame_extractor import crop_chimney_regions
from utils.compute_tail_heaviness import compute_tail_heaviness


def eval_image_folder(image_folder):
    """
    Evaluate all images in a folder using the blur detection model.
    """
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    num_correct_labels = 0
    count = 0
    wrong_predictions = []
    
    for image_name in tqdm(image_files, desc="Processing images"):
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path)
        cropped_regions = crop_chimney_regions(image, extract_camera_id(image_path))
        if not cropped_regions:
            print(f"No cropped regions found for {image_name}.")
            continue
        # # display the cropped regions
        # for idx, region in enumerate(cropped_regions):
        #     plt.imshow(region)
        #     plt.title(f"{image_name} | Region {idx} | Detector Result: {internal_blur_engine(region)}")
        #     plt.axis('off')
        #     plt.show()

        # Calculate the average tail heaviness for the cropped regions
        total_tail_heaviness = 0
        for idx, region in enumerate(cropped_regions):
            tail_heaviness = compute_tail_heaviness(region, use_sobel=True)
            plt.imshow(region)
            plt.title(f"{image_name} | Region {idx} | Tail Heaviness: {tail_heaviness}")
            plt.axis('off')
            plt.show()
            total_tail_heaviness += tail_heaviness
        count += 1
        avg_tail_heaviness = total_tail_heaviness / len(cropped_regions) if cropped_regions else 0
        if avg_tail_heaviness > 20:
            num_correct_labels += 1
        else:
            wrong_predictions.append((image_name, image_path))
    print(f"Accuracy for {image_folder}: {num_correct_labels}/{count} ({(num_correct_labels / count) * 100:.2f}%)")
    if wrong_predictions:
        print("Wrongly predicted images:")
        for name, path in wrong_predictions:
            print(f"{name} | Path: {path}")
        # Always clear the wrongly_predicted_images directory before saving new results
        output_dir = "wrongly_predicted_images"
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                file_path = os.path.join(output_dir, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            for name, path in wrong_predictions:
                img = Image.open(path)
                img.save(os.path.join(output_dir, name))
        else:
            os.makedirs(output_dir, exist_ok=True)
            for name, path in wrong_predictions:
                print(name)
                img = Image.open(path)
                img.save(os.path.join(output_dir, name))
    
if __name__ == "__main__":
    # image_folder = "NEA_data/blur_can_see"
    image_folder = "wrongly_predicted_images"
    eval_image_folder(image_folder)

