import io
from PIL import Image
import numpy as np
from config.settings import IMAGE_SIZE

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Opens image from raw bytes, resizes to (128, 128), normalizes pixel values to [0, 1].
    Wraps bytes in io.BytesIO to ensure compatibility with Pillow's Image.open().
    """
    # Wrap the raw bytes in a binary stream object
    image_stream = io.BytesIO(image_bytes)
    
    # Open the image from the stream and convert to RGB
    image = Image.open(image_stream).convert("RGB")
    
    # Resize to model's expected input size
    image = image.resize(IMAGE_SIZE)
    
    # Convert to NumPy array and normalize to [0, 1] range
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Add batch dimension: (1, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array