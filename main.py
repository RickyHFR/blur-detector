from utils.compute_directional_kurtosis import compute_directional_kurtosis, compute_kurtosis_score
from utils.compute_power_spectrum import compute_spectrum_feature
from utils.compute_tail_heaviness import compute_tail_heaviness 

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Define the paths to the folders
blur_folder = "test_images/blur"
clear_folder = "test_images/clear"

# Function to load images from a folder
def load_images_from_folder(folder_path):
    images = []
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}  # Add valid image extensions here
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in valid_extensions:  # Check file extension
            try:
                img = Image.open(file_path)  # Load the image
                images.append(img)
            except Exception as e:
                print(f"Error loading image {file_path}: {e}")
    return images

# Load images from both folders
blur_images = load_images_from_folder(blur_folder)
clear_images = load_images_from_folder(clear_folder)

# Function to predict the class of an image
def predict(image):
    # Placeholder for prediction logic
    # Replace this with your actual prediction logic
    # For example, you can use compute_directional_kurtosis, compute_kurtosis_score, etc.
    return "blur" if np.random.rand() > 0.5 else "clear"  # Random prediction for now

# Function to compute accuracy
def compute_accuracy(images, true_label):
    correct_predictions = 0
    for image in images:
        prediction = predict(image)
        if prediction == true_label:
            correct_predictions += 1
    return correct_predictions / len(images) if images else 0

# Compute accuracy for blur and clear images
blur_accuracy = compute_accuracy(blur_images, "blur")
clear_accuracy = compute_accuracy(clear_images, "clear")

# Print the results
print(f"Accuracy for blur images: {blur_accuracy * 100:.2f}%")
print(f"Accuracy for clear images: {clear_accuracy * 100:.2f}%")


