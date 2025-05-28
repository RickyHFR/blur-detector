import os
from blur_detector import extract_camera_id
from frame_extractor import crop_chimney_regions, label_regions
from PIL import Image

target_path = 'test_vid_in_progress/crop_demo/crop_result'
def get_demo(path):
        image_files = [f for f in os.listdir(path) if f.endswith((".png", ".jpg", ".jpeg"))]
        for image_name in image_files:
            image_path = os.path.join(path, image_name)
            image = Image.open(image_path)
            cropped_regions = crop_chimney_regions(image, extract_camera_id(image_path))
            
            for i, region in enumerate(cropped_regions):
                # save the regions
                region.save(os.path.join(target_path, f"{image_name}_region_{i}.png"))
            # label the regions
            image_rgb = image.convert("RGB")  # Ensure RGB mode for drawing
            labeled_image = label_regions(image_rgb, extract_camera_id(image_path))
            labeled_image.save(os.path.join(target_path, f"{image_name}_labeled.png"))

if __name__ == "__main__":
    path = 'test_vid_in_progress/crop_demo/crop_src'
    get_demo(path)