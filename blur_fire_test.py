import numpy as np
from PIL import Image
from frame_extractor import crop_chimney_regions
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture
from scipy import ndimage
import cv2
import gc

# def get_mask(image):
#     img_hsv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
#     # Define fire-like color range in HSV
#     lower_fire = np.array([0, 50, 100])  # [H, S, V]
#     upper_fire = np.array([50, 255, 255])
#     mask_fire = cv2.inRange(img_hsv, lower_fire, upper_fire)
#     # Optionally dilate the mask to be conservative
#     kernel = np.ones((3,3), np.uint8)
#     mask_fire = cv2.dilate(mask_fire, kernel, iterations=1)
#     mask_non_fire = (mask_fire == 0)
#     return mask_non_fire

def get_mask(image):
    img_hsv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)

    # Define fire-like color range in HSV
    lower_fire = np.array([0, 50, 100])    # [H, S, V]
    upper_fire = np.array([50, 255, 255])
    mask_fire = cv2.inRange(img_hsv, lower_fire, upper_fire)

    # Define whitish fire range (very bright, low saturation)
    lower_white = np.array([0, 0, 240])
    upper_white = np.array([180, 30, 255])
    mask_whitish = cv2.inRange(img_hsv, lower_white, upper_white)

    # Combine both fire-like and whitish regions
    combined_mask = cv2.bitwise_or(mask_fire, mask_whitish)

    # --- Strengthen mask by dilation ---
    kernel = np.ones((5, 5), np.uint8)  # Larger kernel = more aggressive dilation
    dilated_mask = cv2.dilate(combined_mask, kernel, iterations=1)

    # Return inverse mask: True for non-fire regions
    return dilated_mask == 0


def compute_tail_heaviness(image, use_sobel=True):
    # TODO
    # original_img = image 

    non_fire_mask = get_mask(image)
    display_mask = np.zeros_like(np.array(image), dtype=np.uint8)
    display_mask[non_fire_mask] = [255, 0, 0]  # Red for non-fire regions
    if isinstance(image, str):
        img = np.array(Image.open(image).convert('L'), dtype=float)
    else:
        img = np.array(image.convert('L'), dtype=np.float32)

    # TODO
    # grayscale_img = img.copy()  # Keep a copy of the grayscale image for display

    if use_sobel:
        Gx = ndimage.sobel(img, axis=1)
        Gy = ndimage.sobel(img, axis=0)
    else:
        Gy, Gx = np.gradient(img)

    G = np.sqrt(Gx**2 + Gy**2).reshape(-1, 1)

    # TODO
    # # convert the gradient to image for display
    # gradient_magnitude_img = np.clip(G.reshape(img.shape), 0, 255).astype(np.uint8)

    grad_thresh = np.percentile(G, 98)
    G = np.where(G < grad_thresh, G, 0)
    # gradient_magnitude_masked = G
    # new_gradient_magnitude_img = np.clip(gradient_magnitude_masked.reshape(img.shape), 0, 255).astype(np.uint8)

    G_masked = G[non_fire_mask.flatten()]

    # TODO
    # # For visualization: create an image with masked values at non-fire locations
    # new_gradient_magnitude_img = np.zeros_like(img)
    # new_gradient_magnitude_img[non_fire_mask] = np.clip(G.flatten()[non_fire_mask.flatten()], 0, 255)
    # new_gradient_magnitude_img = new_gradient_magnitude_img.astype(np.uint8)

    if G_masked.shape[0] < 2:
        print("Warning: Not enough non-fire pixels for GMM. Returning 0.")
        sigma1 = 0.0
    else:
        gmm = GaussianMixture(n_components=2, covariance_type='diag', random_state=0)
        gmm.fit(G_masked)
        # --- 5) Extract standard deviations and pick the larger ---
        sigmas = np.sqrt(gmm.covariances_.flatten())
        sigma1 = max(sigmas)
    
    # TODO
    # gmm1 = GaussianMixture(n_components=2, covariance_type='diag', random_state=0)
    # gmm1.fit(G)
    # sigmas_pre = np.sqrt(gmm1.covariances_.flatten())
    # sigma1_pre = max(sigmas_pre)

    # TODO
    # # Display the original, grayscale, and gradient magnitude images
    # plt.figure(figsize=(12, 4))
    # plt.subplot(1, 5, 1)
    # plt.imshow(original_img)
    # plt.title('Original Image')
    # plt.axis('off')
    # plt.subplot(1, 5, 2)
    # plt.imshow(grayscale_img, cmap='gray')
    # plt.title('Grayscale Image')
    # plt.axis('off')
    # plt.subplot(1, 5, 3)
    # plt.imshow(gradient_magnitude_img, cmap='gray')
    # plt.title('Gradient Magnitude')
    # plt.axis('off')
    # plt.subplot(1, 5, 4)
    # plt.imshow(new_gradient_magnitude_img, cmap='gray')
    # plt.title('Masked Gradient Magnitude')
    # plt.axis('off')
    # plt.subplot(1, 5, 5)
    # plt.imshow(display_mask)
    # plt.title('Non-Fire Mask')
    # plt.axis('off')
    # plt.tight_layout(rect=[0, 0.08, 1, 1])  # Leave space at the bottom
    # plt.figtext(0.5, 0.01, f"pre_sigma1: {sigma1_pre:.4f} | after_sigma1: {sigma1:.4f}", ha='center', fontsize=14, color='blue')
    # plt.show()

    # At the end, free memory (make sure to use the correct variable name)
    del img, G, Gx, Gy, G_masked, non_fire_mask  # use non_fire_mask, not mask_non_fire
    gc.collect()

    return sigma1

def blur_fire_test(image_path, camera_id, region_id=None):
    img = Image.open(image_path)
    region = crop_chimney_regions(img, camera_id)[region_id]
    compute_tail_heaviness(region, use_sobel=True)

if __name__ == "__main__":
    import os
    folder_path = "test_vid_in_progress/enlarged_images/blur_with_flare/png_form/ad3_png"
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        camera_id = 'ad3'  # Use the filename without extension as camera ID
        blur_fire_test(image_path, camera_id, region_id=0)  # Test with region_id=0 for simplicity
