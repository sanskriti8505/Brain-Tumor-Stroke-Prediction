import json
from pathlib import Path
import numpy as np
from keras.models import load_model
from .preprocessing import preprocess_image

CURRENT_DIR=Path(__file__).resolve().parent
ARTIFACTS_DIR=CURRENT_DIR/"artifacts"
MODEL_PATH=ARTIFACTS_DIR/"brain_tumor_model.keras"
CLASS_NAMES_PATH=ARTIFACTS_DIR/"class_names.json"

try:
    model = load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

try:
    with open(CLASS_NAMES_PATH) as file:
        class_names = json.load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load class names: {e}")
    
def predict_tumor(image_path: str):
    processed_image = preprocess_image(image_path)
    predictions=model.predict(processed_image,verbose=1)
    predicted_index=int(np.argmax(predictions))
    confidence=float(np.max(predictions)*100)
    prediction=class_names[str(predicted_index)]
    return{
        'prediction':prediction,
        'confidence':round(confidence,2)
    }
    

