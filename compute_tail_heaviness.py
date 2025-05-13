import numpy as np
from PIL import Image
from sklearn.mixture import GaussianMixture
from scipy import ndimage

def compute_tail_heaviness(image_path, use_sobel=True):
    """
    Compute the 'tail-heaviness' feature f2 = sigma1 from a 2-component
    GMM fit to the gradient magnitudes, where sigma1 is the larger of the
    two learned standard deviations.

    Parameters:
    -----------
    image_path : str
        Path to input image.
    use_sobel : bool, default=True
        If True, compute gradients with Sobel filters; otherwise use central differences.

    Returns:
    --------
    float
        tail-heaviness feature (sigma1).
    """
    # --- 1) Load & grayscale ---
    img = np.array(Image.open(image_path).convert('L'), dtype=float)

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

# Example:
if __name__ == "__main__":
    path = "test_data/blur.jpg"
    tail_heaviness = compute_tail_heaviness(path)
    print(f"Tail-heaviness (σ₁): {tail_heaviness:.4f}")
    path = "test_data/clear.jpg"
    tail_heaviness = compute_tail_heaviness(path)
    print(f"Tail-heaviness (σ₁): {tail_heaviness:.4f}")
