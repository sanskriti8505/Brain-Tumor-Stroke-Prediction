from pathlib import Path
import numpy as np
from PIL import Image

IMAGE_SIZE=(224,224)

def preprocess_image(image_path:str)->np.ndarray:
    image_path=Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found : {image_path}")
    try:
        image=Image.open(image_path)
    except Exception:
        raise ValueError("Invalid image file.")
    
    with Image.open(image_path) as image:
        image=image.convert("RGB")
       
    image=image.resize(IMAGE_SIZE,Image.Resampling.LANCZOS)
    image=np.array(image)
    image=image.astype(np.float32)
    image=np.expand_dims(image,axis=0)
    return image 
    