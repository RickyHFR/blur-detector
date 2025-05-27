from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from sklearn.mixture import GaussianMixture
from scipy import ndimage

def compute_tail_heaviness(image, use_sobel=True):
    """
    Compute the 'tail-heaviness' feature f2 = sigma1 from a 2-component
    GMM fit to the gradient magnitudes, where sigma1 is the larger of the
    two learned standard deviations.

    Parameters:
    -----------
    image : str or PIL.Image.Image
        Path to input image or a PIL Image object.
    use_sobel : bool, default=True
        If True, compute gradients with Sobel filters; otherwise use central differences.

    Returns:
    --------
    float
        tail-heaviness feature (sigma1).
    """
    # --- 1) Load & grayscale ---
    if isinstance(image, str):
        img = np.array(Image.open(image).convert('L'), dtype=float)
    else:
        img = np.array(image.convert('L'), dtype=float)

    # img = np.zeros(img.shape)  # Ensure the image is in float format

    # Display brightness histogram
    plt.figure(figsize=(6, 3))
    plt.hist(img.flatten(), bins=50, color='gray', alpha=0.7)
    plt.title("Brightness Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    plt.imshow(img, cmap='gray')
    plt.title("Grayscale Image")
    plt.axis('off')
    plt.show()

    # Stronger bright point removal using multiple methods
    # Method 1: Percentile-based clipping to remove extreme outliers
    upper_threshold = np.percentile(img, 95)  # Remove top 5% brightest pixels
    # print(f"Upper threshold for clipping: {upper_threshold}")
    img = np.clip(img, 0, upper_threshold)

    plt.figure(figsize=(6, 3))
    plt.hist(img.flatten(), bins=50, color='gray', alpha=0.7)
    plt.title("Brightness Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title("Clipped Image")
    plt.axis('off')
    plt.show()
    
    # # Method 2: MAD-based outlier detection for remaining bright spots
    # median = np.median(img)
    # mad = np.median(np.abs(img - median))
    # threshold = median + 3 * mad  # More robust than standard deviation
    # bright_mask = img > threshold
    # img[bright_mask] = threshold

    # --- 2) Compute gradients ---
    if use_sobel:
        Gx = ndimage.sobel(img, axis=1)
        Gy = ndimage.sobel(img, axis=0)
    else:
        Gy, Gx = np.gradient(img)

    # --- 3) Gradient magnitude and flatten ---
    G = np.sqrt(Gx**2 + Gy**2).reshape(-1, 1)

    # --- 4) Fit 2-component GMM to gradient magnitudes ---
    gmm = GaussianMixture(n_components=2, covariance_type='diag', random_state=0)
    gmm.fit(G)

    # --- 5) Extract standard deviations and pick the larger ---
    # gmm.covariances_ is shape (2, 1) for diag covariances
    sigmas = np.sqrt(gmm.covariances_.flatten())
    sigma1 = max(sigmas)

    return sigma1
