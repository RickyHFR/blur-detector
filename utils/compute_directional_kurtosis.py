import numpy as np
import math
from scipy import ndimage
from scipy.stats import kurtosis
from PIL import Image

def compute_directional_kurtosis(image):
    """
    Computes the kurtosis of the image gradients in the horizontal and vertical directions.
    
    Parameters:
        image (numpy.ndarray): Input image array.

    Returns:
        tuple: (kurtosis_horizontal, kurtosis_vertical)
    """
    # Compute gradients using Sobel filter
    Gx = ndimage.sobel(image, axis=1)  # Horizontal gradients
    Gy = ndimage.sobel(image, axis=0)  # Vertical gradients
    
    kurtosis_horizontal = kurtosis(Gx.ravel(), fisher=False)
    kurtosis_vertical = kurtosis(Gy.ravel(), fisher=False)
    
    return kurtosis_horizontal, kurtosis_vertical

def compute_kurtosis_score(image):
    """
    Computes the final kurtosis score based on horizontal and vertical kurtosis.
    
    Parameters:
        kurtosis_horizontal (float): Kurtosis in the horizontal direction.
        kurtosis_vertical (float): Kurtosis in the vertical direction.
        
    Returns:
        float: Final kurtosis score.
    """
    kurtosis_horizontal, kurtosis_vertical = compute_directional_kurtosis(image)
    horizontal_score = math.log(kurtosis_horizontal + 3)
    vertical_score = math.log(kurtosis_vertical + 3)
    final_score = min(horizontal_score, vertical_score)
    return final_score
