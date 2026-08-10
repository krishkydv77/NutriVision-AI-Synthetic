import numpy as np
import tensorflow as tf
from config.settings import ANN_MODEL_PATH
from utils.labels import FOOD_CLASSES, NUTRITION_DB

class NutritionService:
    def __init__(self):
        try:
            self.ann_model = tf.keras.models.load_model(ANN_MODEL_PATH)
        except Exception:
            self.ann_model = None

    def estimate_nutrition(self, class_index: int, portion_scale: float = 1.0) -> dict:
        food_name = FOOD_CLASSES[class_index]
        
        if self.ann_model:
            # Prepare feature vector for ANN
            one_hot = [0.0] * len(FOOD_CLASSES)
            one_hot[class_index] = 1.0
            input_features = np.array([one_hot + [portion_scale]], dtype=np.float32)
            
            predictions = self.ann_model.predict(input_features)[0]
            
            calories = float(max(0, predictions[0]))
            protein = float(max(0, predictions[1]))
            carbs = float(max(0, predictions[2]))
            fat = float(max(0, predictions[3]))
        else:
            # Fallback to database lookup if model is missing
            base = NUTRITION_DB.get(food_name, {"calories": 100, "protein": 2, "carbs": 15, "fat": 2})
            calories = base["calories"] * portion_scale
            protein = base["protein"] * portion_scale
            carbs = base["carbs"] * portion_scale
            fat = base["fat"] * portion_scale
            
        return {
            "calories": round(calories, 1),
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1)
        }