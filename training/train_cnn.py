import os
import tensorflow as tf
from tensorflow.keras import layers, models
from config.settings import CNN_MODEL_PATH, IMAGE_SIZE
from utils.labels import FOOD_CLASSES
from training.dataset_loader import load_or_generate_dummy_cnn_data

def build_cnn_model():
    model = models.Sequential([
        layers.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(len(FOOD_CLASSES), activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

if __name__ == "__main__":
    print("Training CNN Model for Food Image Classification...")
    X, y = load_or_generate_dummy_cnn_data()
    
    cnn_model = build_cnn_model()
    cnn_model.fit(X, y, epochs=5, batch_size=16)
    
    os.makedirs(os.path.dirname(CNN_MODEL_PATH), exist_ok=True)
    cnn_model.save(CNN_MODEL_PATH)
    print(f"CNN Model successfully saved to: {CNN_MODEL_PATH}")