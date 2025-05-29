import os
from PIL import Image

def convert_webp_to_png(source_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.webp'):
            webp_path = os.path.join(source_folder, filename)
            png_name = os.path.splitext(filename)[0] + '.png'
            png_path = os.path.join(target_folder, png_name)
            with Image.open(webp_path) as img:
                img.save(png_path, 'PNG')

if __name__ == "__main__":
    source_folder = "test_vid_in_progress/enlarged_images/blur_with_flare/tb4"  # Change this to your source folder
    target_folder = source_folder + "_png"  # Change this to your target folder
    convert_webp_to_png(source_folder, target_folder)
