import numpy as np
import math
from scipy import ndimage
from scipy.stats import kurtosis
from PIL import Image

def compute_directional_kurtosis(image_path):
    """
    Computes the kurtosis of the image gradients in the horizontal and vertical directions.
    
    Parameters:
        image_path (str): Path to the input image file.
        
    Returns:
        tuple: (kurtosis_horizontal, kurtosis_vertical)
    """
    # Load image and convert to grayscale
    image = np.array(Image.open(image_path).convert('L'), dtype=float)
    
    # Compute gradients using Sobel filter
    Gx = ndimage.sobel(image, axis=1)  # Horizontal gradients
    Gy = ndimage.sobel(image, axis=0)  # Vertical gradients
    
    # Flatten gradient arrays and compute kurtosis
    # fisher=False returns the "raw" kurtosis (3 for a normal distribution)
    kurtosis_horizontal = kurtosis(Gx.ravel(), fisher=False)
    kurtosis_vertical = kurtosis(Gy.ravel(), fisher=False)
    
    return kurtosis_horizontal, kurtosis_vertical

def compute_kurtosis_score(kurtosis_horizontal, kurtosis_vertical):
    """
    Computes the final kurtosis score based on horizontal and vertical kurtosis.
    
    Parameters:
        kurtosis_horizontal (float): Kurtosis in the horizontal direction.
        kurtosis_vertical (float): Kurtosis in the vertical direction.
        
    Returns:
        float: Final kurtosis score.
    """
    horizontal_score = math.log(kurtosis_horizontal + 3)
    vertical_score = math.log(kurtosis_vertical + 3)
    final_score = min(horizontal_score, vertical_score)
    return final_score

# Example usage
if __name__ == "__main__":
    image_path = "test_data/clear.jpg"
    kx, ky = compute_directional_kurtosis(image_path)
    print(f"Horizontal kurtosis: {kx:.4f}")
    print(f"Vertical kurtosis: {ky:.4f}")
    final_score = compute_kurtosis_score(kx, ky)
    print(f"Final kurtosis score for clear image: {final_score:.4f}")

# Example usage for a blurry image
if __name__ == "__main__":
    image_path = "test_data/blur.jpg"
    kx, ky = compute_directional_kurtosis(image_path)
    print(f"Horizontal kurtosis: {kx:.4f}")
    print(f"Vertical kurtosis: {ky:.4f}")
    final_score = compute_kurtosis_score(kx, ky)
    print(f"Final kurtosis score for blurry image: {final_score:.4f}")
