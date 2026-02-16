"""
ML Prediction API
FastAPI backend with 3 prediction endpoints
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI(
    title="ML Prediction API",
    description="ML prediction service with salary, house price, and crop yield models",
    version="1.0.0"
)

# Load models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

salary_model = joblib.load(os.path.join(MODELS_DIR, 'salary_model.pkl'))
house_model = joblib.load(os.path.join(MODELS_DIR, 'house_model.pkl'))
location_map = joblib.load(os.path.join(MODELS_DIR, 'location_map.pkl'))
crop_model = joblib.load(os.path.join(MODELS_DIR, 'crop_model.pkl'))

# ============= Request Models =============

class SalaryRequest(BaseModel):
    years_experience: float

class HouseRequest(BaseModel):
    area: float
    bedrooms: int
    location: str

class CropRequest(BaseModel):
    rainfall: float
    temperature: float

# ============= Routes =============

@app.get("/")
def root():
    return {
        "message": "ML Prediction API",
        "endpoints": {
            "salary": "/predict/salary",
            "house": "/predict/house",
            "crop": "/predict/crop"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict/salary")
def predict_salary(request: SalaryRequest):
    """Predict salary based on years of experience"""
    try:
        prediction = salary_model.predict([[request.years_experience]])[0]
        return {
            "predicted_salary": round(float(prediction), 2),
            "model": "Linear Regression"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/house")
def predict_house(request: HouseRequest):
    """Predict house price based on area, bedrooms, and location"""
    try:
        if request.location.lower() not in location_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid location. Must be one of: {list(location_map.keys())}"
            )
        
        location_encoded = location_map[request.location.lower()]
        prediction = house_model.predict([[request.area, request.bedrooms, location_encoded]])[0]
        
        return {
            "predicted_price": round(float(prediction), 2),
            "model": "Random Forest"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/crop")
def predict_crop(request: CropRequest):
    """Predict crop yield based on rainfall and temperature"""
    try:
        prediction = crop_model.predict([[request.rainfall, request.temperature]])[0]
        return {
            "predicted_yield": round(float(prediction), 2),
            "model": "Decision Tree"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
