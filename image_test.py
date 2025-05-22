import os

from matplotlib import pyplot as plt
from PIL import Image

from blur_detector import internal_blur_engine, extract_camera_id
from frame_extractor import crop_chimney_regions


def eval_image_folder(image_folder):
    """
    Evaluate all images in a folder using the blur detection model.
    """
    for image_name in os.listdir(image_folder):
        if image_name.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_folder, image_name)
            image = Image.open(image_path)
            cropped_regions = crop_chimney_regions(image, extract_camera_id(image_path))
            if not cropped_regions:
                print(f"No cropped regions found for {image_name}.")
                continue
            total = 0
            score = 0
            for region in cropped_regions:
                result = internal_blur_engine(region)
                if result == "blur":
                    score += 1
                total += 1
            if total > 0:
                blur_score = score / total
            
            plt.imshow(image)
            plt.title(f"Original: {image_name} | Blur Score: {blur_score:.2f}")
            plt.axis('off')
            plt.show()

if __name__ == "__main__":
    image_folder = "NEA_data/blur"
    eval_image_folder(image_folder)

