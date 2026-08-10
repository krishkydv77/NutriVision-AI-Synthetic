import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.preprocessing import preprocess_image
from services.prediction_service import PredictionService
from config.settings import UPLOAD_DIR

router = APIRouter()
prediction_service = PredictionService()

@router.post("/api/predict")
async def predict_food(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
    
    contents = await file.read()
    
    # Save Image to Static Folder
    file_extension = file.filename.split(".")[-1]
    saved_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
        
    # Preprocess & Predict
    image_tensor = preprocess_image(contents)
    result = prediction_service.predict(image_tensor)
    
    # Add Image URL to Response
    result["image_url"] = f"/static/uploads/{saved_filename}"
    
    return result



# Output #####
# {
# "food":"Pizza",

# "confidence":96.5,

# "nutrition":{

# "calories":266,

# "protein":11,

# "carbs":33,

# "fat":10

# },

# "health_score":8.2,

# "image_url":"/static/uploads/93ac67fd.jpg"
# }