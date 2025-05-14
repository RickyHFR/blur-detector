import numpy as np
from PIL import Image

def compute_spectrum_feature(image, patch=None, eps=1e-8):
    """
    Compute the frequency-domain blur feature f3 = sum(log(J(omega))),
    where J(omega) is the angle-averaged power spectrum at radius omega.

    Parameters
    ----------
    image : str or PIL.Image.Image
        Path to the input image or a PIL Image object.
    patch : tuple or None
        If given, a 4-tuple (x, y, w, h) specifying a sub-window. Otherwise use full image.
    eps : float
        Small constant to avoid log(0).

    Returns
    -------
    float
        f3 = sum(log(J(omega))) across all non-zero radial frequencies.
    """
    # 1) Load & optionally crop to patch, convert to grayscale float array
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image

    if img.mode == "RGBA":  # Handle PNG with transparency
        img = img.convert("RGB")
    img = img.convert('L')  # Convert to grayscale
    img = np.array(img, dtype=float)

    if patch is not None:
        x, y, w, h = patch
        img = img[y:y+h, x:x+w]

    # 2) Compute centered 2D FFT and power spectrum
    F = np.fft.fftshift(np.fft.fft2(img))
    P = np.abs(F)**2

    # 3) Build a radial frequency map
    rows, cols = P.shape
    cy, cx = rows // 2, cols // 2
    y, x = np.indices((rows, cols))
    r = np.sqrt((x - cx)**2 + (y - cy)**2).astype(int)

    # 4) Accumulate and average power in each radial bin
    max_r = min(cx, cy)
    # total power per radius
    sum_P = np.bincount(r.ravel(), weights=P.ravel(), minlength=max_r+1)
    # counts per radius
    count = np.bincount(r.ravel(), minlength=max_r+1)
    # avoid division by zero
    J = sum_P[:max_r+1] / (count[:max_r+1] + eps)

    # 5) Exclude the DC component at r=0, sum log-power
    #    (as per Eq. (13) in the paper)
    feature_f3 = np.sum(np.log(J[1:] + eps))
    return feature_f3

# Example usage
if __name__ == "__main__":
    path = "test_data/blur.jpg"
    f3 = compute_spectrum_feature(path)
    print(f"Spectrum feature f3 = {f3:.4f}")
    path = "test_data/clear.jpg"
    f3 = compute_spectrum_feature(path)
    print(f"Spectrum feature f3 = {f3:.4f}")
