from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from frame_extractor import crop_chimney_regions
from utils.compute_tail_heaviness import compute_tail_heaviness

def generate_report(image, camera_id, save_detected_dir=None):
    # --- 1) Load & grayscale ---
    shown_images = []  # Collect images to be shown
    if isinstance(image, str):
        pil_img = Image.open(image).convert('L')
    else:
        pil_img = image.convert('L')
    img = np.array(pil_img, dtype=float)
    
    plt.imshow(img, cmap='gray')
    plt.title(f"Grayscale Image | Camera ID: {camera_id}")
    plt.axis('off')
    plt.show()
    shown_images.append(img)
    
    regions = crop_chimney_regions(pil_img, camera_id)

    for region in regions:
        score = compute_tail_heaviness(region, use_sobel=True)  # Pass PIL Image
        region_np = np.array(region, dtype=float)
        plt.imshow(region_np, cmap='gray')
        plt.title(f'Camera ID: {camera_id} | Tail Heaviness: {score:.2f}')
        plt.axis('off')
        plt.show()
        shown_images.append(region_np)
    
    # Combine all shown images vertically and save
    if save_detected_dir is not None and len(shown_images) > 0:
        # Normalize and convert to uint8 for saving
        norm_imgs = [(255 * (img - np.min(img)) / (np.ptp(img) if np.ptp(img) > 0 else 1)).astype(np.uint8) for img in shown_images]
        combined_img = np.vstack(norm_imgs)
        combined_pil = Image.fromarray(combined_img)
        save_path = save_detected_dir if save_detected_dir.endswith('.png') else f"{save_detected_dir}/combined_report_{camera_id}.png"
        combined_pil.save(save_path)
