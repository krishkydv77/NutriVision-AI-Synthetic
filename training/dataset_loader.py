import numpy as np
import tensorflow as tf
from config.settings import IMAGE_SIZE
from utils.labels import FOOD_CLASSES, NUTRITION_DB

def load_or_generate_dummy_cnn_data(num_samples=100):
    """
    Generates synthetic image data if real dataset images are missing.
    Ensures model can be trained instantly for demo/class purposes.
    """
    X = np.random.rand(num_samples, IMAGE_SIZE[0], IMAGE_SIZE[1], 3).astype(np.float32)
    y = np.random.randint(0, len(FOOD_CLASSES), size=(num_samples,))
    y = tf.keras.utils.to_categorical(y, num_classes=len(FOOD_CLASSES))
    return X, y

def generate_ann_dataset(num_samples=500):
    """
    Generates synthetic feature data (Class ID + Estimated Area) -> Micronutrients for ANN.
    """
    X = []
    y = []
    
    for _ in range(num_samples):
        class_idx = np.random.randint(0, len(FOOD_CLASSES))
        food_name = FOOD_CLASSES[class_idx]
        base_nutr = NUTRITION_DB[food_name]
        
        # Portion size multiplier variation (0.8x to 1.5x)
        portion_scale = np.random.uniform(0.8, 1.5)
        
        # One-hot encoded class + portion scale
        one_hot = [0] * len(FOOD_CLASSES)
        one_hot[class_idx] = 1
        x_feature = one_hot + [portion_scale]
        
        # Targets: [Calories, Protein, Carbs, Fat]
        target = [
            base_nutr["calories"] * portion_scale,
            base_nutr["protein"] * portion_scale,
            base_nutr["carbs"] * portion_scale,
            base_nutr["fat"] * portion_scale
        ]
        
        X.append(x_feature)
        y.append(target)
        
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)