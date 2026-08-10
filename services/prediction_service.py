import numpy as np
import tensorflow as tf
from config.settings import CNN_MODEL_PATH
from utils.labels import FOOD_CLASSES
from services.nutrition_service import NutritionService
from utils.helper import calculate_health_score

class PredictionService:
    def __init__(self):
        try:
            self.cnn_model = tf.keras.models.load_model(CNN_MODEL_PATH)
        except Exception:
            self.cnn_model = None
            
        self.nutrition_service = NutritionService()

    def predict(self, image_tensor: np.ndarray) -> dict:
        if self.cnn_model:
            preds = self.cnn_model.predict(image_tensor)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(np.max(preds))
            detected_food = FOOD_CLASSES[class_idx]
        else:
            # Mock fallback if CNN model file is not created yet
            class_idx = 0
            detected_food = "Apple"
            confidence = 0.95

        # Pass detected class to ANN Service for Nutrition Estimation
        nutrition_data = self.nutrition_service.estimate_nutrition(class_idx, portion_scale=1.0)
        
        # Calculate Health Score
        health_score = calculate_health_score(
            nutrition_data["calories"],
            nutrition_data["protein"],
            nutrition_data["carbs"],
            nutrition_data["fat"]
        )

        return {
            "food": detected_food,
            "confidence": round(confidence * 100, 2),
            "nutrition": nutrition_data,
            "health_score": health_score
        }





###Expected output 

# {
# "food":"Burger",

# "confidence":92,

# "nutrition":{

# "calories":295,

# "protein":17,

# "carbs":30,

# "fat":14

# },

# "health_score":7.5
# }