import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model Paths
CNN_MODEL_PATH = os.path.join(BASE_DIR, "models", "cnn_model.keras")
ANN_MODEL_PATH = os.path.join(BASE_DIR, "models", "ann_model.keras")

# Image Configurations
IMAGE_SIZE = (128, 128)
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")

# Ensure Uploads Directory Exists
os.makedirs(UPLOAD_DIR, exist_ok=True)