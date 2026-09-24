from pathlib import Path
import numpy as np
from app.database.db import SessionLocal
from app.database.models import RiceInfo
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "ml" / "saved_model" / "rice_model_mobilenet.h5"

# Load model only once
model = load_model(MODEL_PATH)

CLASS_NAMES = [
    "Arborio",
    "Basmati",
    "Ipsala",
    "Jasmine",
    "Karacadag"
]

def predict_image(image_path: str):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)[0]

    # Top 3 indices
    top3_indices = np.argsort(predictions)[::-1][:3]

    top3 = []
    for idx in top3_indices:
        top3.append({
            "name": CLASS_NAMES[idx],
            "confidence": round(float(predictions[idx]) * 100, 2)
        })

    best = top3[0]
    db = SessionLocal()
    try:
        rice = (
            db.query(RiceInfo)
            .filter(RiceInfo.variety == best["name"])
            .first()
        )
        
        result = {
            "rice_type": best["name"],
            "confidence": best["confidence"],
            "water": rice.water if rice else "N/A",
            "fertilizer": rice.fertilizer if rice else "N/A",
            "top3": top3
        }
    finally:
        db.close()

    return result