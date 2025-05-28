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

    # --- 2) Compute gradients ---
    if use_sobel:
        Gx = ndimage.sobel(img, axis=1)
        Gy = ndimage.sobel(img, axis=0)
    else:
        Gy, Gx = np.gradient(img)

    # --- 3) Gradient magnitude and flatten ---
    G = np.sqrt(Gx**2 + Gy**2).reshape(-1, 1)

    grad_thresh = np.percentile(G, 98)
    gradient_magnitude_masked = np.where(G < grad_thresh, G, 0)

    # --- 4) Fit 2-component GMM to gradient magnitudes ---
    gmm = GaussianMixture(n_components=2, covariance_type='diag', random_state=0)
    gmm.fit(gradient_magnitude_masked)

    # --- 5) Extract standard deviations and pick the larger ---
    # gmm.covariances_ is shape (2, 1) for diag covariances
    sigmas = np.sqrt(gmm.covariances_.flatten())
    sigma1 = max(sigmas)

    return sigma1
