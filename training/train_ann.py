import os
import tensorflow as tf
from tensorflow.keras import layers, models
from config.settings import ANN_MODEL_PATH
from utils.labels import FOOD_CLASSES
from training.dataset_loader import generate_ann_dataset

def build_ann_model():
    # Input size = number of food classes + 1 portion scaling factor feature
    input_dim = len(FOOD_CLASSES) + 1
    
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(4)  # Outputs: [Calories, Protein, Carbs, Fat]
    ])
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    return model

if __name__ == "__main__":
    print("Training ANN Model for Nutrition Estimation...")
    X, y = generate_ann_dataset()
    
    ann_model = build_ann_model()
    ann_model.fit(X, y, epochs=20, batch_size=32)
    
    os.makedirs(os.path.dirname(ANN_MODEL_PATH), exist_ok=True)
    ann_model.save(ANN_MODEL_PATH)
    print(f"ANN Model successfully saved to: {ANN_MODEL_PATH}")