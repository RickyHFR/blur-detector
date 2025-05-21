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

    # Filter out pixels that are at least 50% brighter than average and replace with the average value
    avg = np.median(img)
    bright_mask = img >= (1.5 * avg)
    img[bright_mask] = avg

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

def zoom_into_point(image, zoom_factor, center=None):
    """
    Zoom in on a specific (x, y) point in the image and resize back to original size.

    Parameters
    ----------
    image : PIL.Image
    zoom_factor : float (>1 for zoom-in)
    center : tuple (x, y) - the point to zoom in on. Default is center of image.

    Returns
    -------
    zoomed PIL.Image
    """
    w, h = image.size
    if center is None:
        center = (w // 2, h // 2)

    cx, cy = center
    crop_w = int(w / zoom_factor)
    crop_h = int(h / zoom_factor)

    left = max(cx - crop_w // 2, 0)
    top = max(cy - crop_h // 2, 0)
    right = min(left + crop_w, w)
    bottom = min(top + crop_h, h)

    cropped = image.crop((left, top, right, bottom))
    return cropped.resize((w, h), resample=Image.BILINEAR)
