# Food classes supported by the CNN model
FOOD_CLASSES = [
    "Apple",
    "Banana",
    "Burger",
    "Pizza",
    "Salad"
]

# Nutritional Database per 100g (Used to generate ANN target data & fallback lookup)
NUTRITION_DB = {
    "Apple": {"calories": 52, "protein": 0.3, "carbs": 14.0, "fat": 0.2, "volume_factor": 1.5},
    "Banana": {"calories": 89, "protein": 1.1, "carbs": 23.0, "fat": 0.3, "volume_factor": 1.2},
    "Burger": {"calories": 295, "protein": 17.0, "carbs": 30.0, "fat": 14.0, "volume_factor": 2.2},
    "Pizza": {"calories": 266, "protein": 11.0, "carbs": 33.0, "fat": 10.0, "volume_factor": 2.5},
    "Salad": {"calories": 45, "protein": 1.5, "carbs": 5.0, "fat": 2.0, "volume_factor": 1.0}
}