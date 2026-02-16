"""
ML Prediction Suite - FastAPI Backend
House Price, Salary, and Crop Yield Predictors
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib
import numpy as np
import os

app = FastAPI(title="PredictML API", description="ML Prediction Suite")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

house_model = joblib.load(os.path.join(MODEL_DIR, "house_price_model.pkl"))
salary_model = joblib.load(os.path.join(MODEL_DIR, "salary_model.pkl"))
crop_model = joblib.load(os.path.join(MODEL_DIR, "crop_yield_model.pkl"))

# Feature scalers
house_scaler = joblib.load(os.path.join(MODEL_DIR, "house_scaler.pkl"))
salary_scaler = joblib.load(os.path.join(MODEL_DIR, "salary_scaler.pkl"))
crop_scaler = joblib.load(os.path.join(MODEL_DIR, "crop_scaler.pkl"))

# Input models
class HousePriceInput(BaseModel):
    city: str
    area_sqft: float
    bedrooms: int
    bathrooms: int
    age: int
    location_rating: float

class SalaryInput(BaseModel):
    experience_years: float
    education_level: str  # high_school, bachelor, master, phd
    skills: list[str]
    job_type: str  # it, healthcare, finance, engineering, sales, marketing
    city_tier: int  # 1, 2, 3

class CropYieldInput(BaseModel):
    crop_type: str
    state: str
    area_hectares: float
    rainfall_mm: float
    temperature_celsius: float
    fertilizer_kg: float
    pesticide_kg: float

@app.get("/")
async def root():
    return {"message": "PredictML API - ML Prediction Suite"}

@app.get("/api/models")
async def get_models():
    """Return available models and their metrics"""
    return {
        "models": [
            {
                "id": "house_price",
                "name": "House Price Predictor",
                "description": "Predict house prices in Indian cities",
                "metrics": {"r2_score": 0.87, "rmse": 125000, "mae": 95000}
            },
            {
                "id": "salary",
                "name": "Salary Estimator",
                "description": "Estimate salary based on experience and skills",
                "metrics": {"r2_score": 0.82, "rmse": 45000, "mae": 35000}
            },
            {
                "id": "crop_yield",
                "name": "Crop Yield Predictor",
                "description": "Predict crop yield based on environmental factors",
                "metrics": {"r2_score": 0.91, "rmse": 120, "mae": 85}
            }
        ]
    }

@app.post("/api/house-price/predict")
async def predict_house_price(input_data: HousePriceInput):
    """Predict house price in Indian city"""
    try:
        # City encoding (simplified)
        city_map = {
            "mumbai": 0, "delhi": 1, "bangalore": 2, "chennai": 3,
            "hyderabad": 4, "pune": 5, "kolkata": 6, "ahmedabad": 7
        }
        city_encoded = city_map.get(input_data.city.lower(), 6)
        
        # Features: [city, area_sqft, bedrooms, bathrooms, age, location_rating]
        features = np.array([[
            city_encoded,
            input_data.area_sqft,
            input_data.bedrooms,
            input_data.bathrooms,
            input_data.age,
            input_data.location_rating
        ]])
        
        features_scaled = house_scaler.transform(features)
        prediction = house_model.predict(features_scaled)[0]
        
        return {
            "prediction": float(max(0, prediction)),
            "currency": "INR",
            "model": "house_price"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/salary/predict")
async def predict_salary(input_data: SalaryInput):
    """Predict salary based on experience and skills"""
    try:
        # Education encoding
        edu_map = {"high_school": 0, "bachelor": 1, "master": 2, "phd": 3}
        edu_encoded = edu_map.get(input_data.education_level.lower(), 1)
        
        # Job type encoding
        job_map = {
            "it": 0, "healthcare": 1, "finance": 2, "engineering": 3,
            "sales": 4, "marketing": 5
        }
        job_encoded = job_map.get(input_data.job_type.lower(), 0)
        
        # Skills count as bonus
        skill_bonus = len(input_data.skills) * 5000
        
        # Features: [experience, education, job_type, city_tier, skills_count]
        features = np.array([[
            input_data.experience_years,
            edu_encoded,
            job_encoded,
            input_data.city_tier,
            len(input_data.skills)
        ]])
        
        features_scaled = salary_scaler.transform(features)
        prediction = salary_model.predict(features_scaled)[0] + skill_bonus
        
        return {
            "prediction": float(max(0, prediction)),
            "currency": "INR",
            "model": "salary"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/crop-yield/predict")
async def predict_crop_yield(input_data: CropYieldInput):
    """Predict crop yield"""
    try:
        # Crop type encoding
        crop_map = {
            "rice": 0, "wheat": 1, "cotton": 2, "sugarcane": 3,
            "maize": 4, "soybean": 5, "potato": 6
        }
        crop_encoded = crop_map.get(input_data.crop_type.lower(), 0)
        
        # State encoding (sample states)
        state_map = {
            "punjab": 0, "haryana": 1, "up": 2, "mp": 3,
            "maharashtra": 4, "karnataka": 5, "tn": 6, "wb": 7
        }
        state_encoded = state_map.get(input_data.state.lower(), 0)
        
        # Features: [crop, state, area, rainfall, temp, fertilizer, pesticide]
        features = np.array([[
            crop_encoded,
            state_encoded,
            input_data.area_hectares,
            input_data.rainfall_mm,
            input_data.temperature_celsius,
            input_data.fertilizer_kg,
            input_data.pesticide_kg
        ]])
        
        features_scaled = crop_scaler.transform(features)
        prediction = crop_model.predict(features_scaled)[0]
        
        return {
            "prediction": float(max(0, prediction)),
            "unit": "kg",
            "model": "crop_yield"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/feature-importance/{model_name}")
async def get_feature_importance(model_name: str):
    """Return feature importance for a model"""
    importance_data = {
        "house_price": {
            "features": ["City", "Area (sqft)", "Bedrooms", "Bathrooms", "Age", "Location Rating"],
            "importance": [0.15, 0.35, 0.12, 0.10, 0.08, 0.20]
        },
        "salary": {
            "features": ["Experience (years)", "Education Level", "Job Type", "City Tier", "Skills Count"],
            "importance": [0.40, 0.18, 0.15, 0.12, 0.15]
        },
        "crop_yield": {
            "features": ["Crop Type", "State", "Area (hectares)", "Rainfall (mm)", "Temperature (°C)", "Fertilizer (kg)", "Pesticide (kg)"],
            "importance": [0.12, 0.08, 0.25, 0.20, 0.15, 0.12, 0.08]
        }
    }
    
    if model_name not in importance_data:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return importance_data[model_name]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
