from utils.compute_directional_kurtosis import compute_directional_kurtosis, compute_kurtosis_score
from utils.compute_power_spectrum import compute_spectrum_feature
from utils.compute_tail_heaviness import compute_tail_heaviness 
from naive_bayes_classifier import GaussianNB

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import torch

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
    tail_heaviness_value = compute_tail_heaviness(image)
    print(f"Tail-heaviness (σ₁): {tail_heaviness_value:.4f}")
    return "blur" if tail_heaviness_value < 20 else "clear"

# Function to compute accuracy and store wrongly predicted images
def compute_accuracy(images, true_label):
    correct_predictions = 0
    wrong_predictions = []  # List to store details of wrongly predicted images

    for idx, image in enumerate(images):
        prediction = predict(image)
        if prediction == true_label:
            correct_predictions += 1
        else:
            wrong_predictions.append({
                "index": idx,
                "true_label": true_label,
                "predicted_label": prediction
            })

    return correct_predictions / len(images) if images else 0, wrong_predictions

# Compute accuracy for blur and clear images
blur_accuracy, blur_wrong_predictions = compute_accuracy(blur_images, "blur")
clear_accuracy, clear_wrong_predictions = compute_accuracy(clear_images, "clear")

# Combine all wrong predictions
all_wrong_predictions = blur_wrong_predictions + clear_wrong_predictions

# Print the results
print(f"Accuracy for blur images: {blur_accuracy * 100:.2f}%")
print(f"Accuracy for clear images: {clear_accuracy * 100:.2f}%")

# Print details of wrongly predicted images
if all_wrong_predictions:
    print("\nWrongly predicted images:")
    for wrong in all_wrong_predictions:
        print(f"Image Index: {wrong['index']}, True Label: {wrong['true_label']}, Predicted Label: {wrong['predicted_label']}")
        # Display the image
        if wrong['true_label'] == "blur":
            blur_images[wrong['index']].show(title=f"True: {wrong['true_label']}, Predicted: {wrong['predicted_label']}")
        else:
            clear_images[wrong['index']].show(title=f"True: {wrong['true_label']}, Predicted: {wrong['predicted_label']}")
else:
    print("\nNo wrongly predicted images.")

# Function to extract features from an image
def extract_features(image):
    kurtosis_score = compute_kurtosis_score(image)
    spectrum_score = compute_spectrum_feature(image)
    tail_heaviness = compute_tail_heaviness(image)
    return [kurtosis_score, spectrum_score, tail_heaviness]

# Prepare the dataset
X = []  # Feature matrix
y = []  # Labels

# Process blur images
for image in blur_images:
    features = extract_features(image)
    X.append(features)
    y.append(0)  # Label for blur

# Process clear images
for image in clear_images:
    features = extract_features(image)
    X.append(features)
    y.append(1)  # Label for clear

# Convert to PyTorch tensors
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.long)

# Train the GaussianNB model
model = GaussianNB(n_features=3, n_classes=2)
model.fit(X, y)

# Print a message indicating training is complete
print("Model training complete.")


