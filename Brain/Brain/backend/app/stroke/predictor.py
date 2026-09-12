import json
from pathlib import Path
import numpy as np
from keras.models import load_model
from .preprocessing import preprocess_image

CURRENT_DIR=Path(__file__).resolve().parent
ARTIFACTS_DIR=CURRENT_DIR/"artifacts"
MODEL_PATH=ARTIFACTS_DIR/"stroke_model.keras"
CLASS_NAMES_PATH=ARTIFACTS_DIR/"stroke_class_labels.json"

try:
    model=load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model : {e}")

try:
    with open(CLASS_NAMES_PATH) as file:
        class_names=json.load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load model : {e}")

def predict_stroke(image_path:str):
    processed_image=preprocess_image(image_path)
    predictions=model.predict(processed_image,verbose=1)
    prob=float(predictions[0][0])
    predicted_index=1 if prob>=0.50 else 0
    if predicted_index==1:
        confidence=prob*100
    else:
        confidence=(1-prob)*100;
    prediction=class_names[predicted_index]
    return{
        'prediction':prediction,
        'confidence':round(confidence,2)
    }