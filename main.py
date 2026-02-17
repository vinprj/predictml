"""
ML Prediction API
FastAPI backend with multiple prediction endpoints
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import joblib
import os
from datetime import datetime

# Import database models
from models import (
    get_db, PredictionHistory, ModelVersion, 
    init_model_versions, SessionLocal
)

# Import new prediction models
from backend.stock_model import stock_predictor
from backend.weather_model import weather_predictor

app = FastAPI(
    title="ML Prediction API",
    description="ML prediction service with salary, house price, crop, stock, and weather models",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

salary_model = joblib.load(os.path.join(MODELS_DIR, 'salary_model.pkl'))
house_model = joblib.load(os.path.join(MODELS_DIR, 'house_model.pkl'))
location_map = joblib.load(os.path.join(MODELS_DIR, 'location_map.pkl'))
crop_model = joblib.load(os.path.join(MODELS_DIR, 'crop_model.pkl'))

# Initialize model versions on startup
@app.on_event("startup")
def startup():
    db = SessionLocal()
    init_model_versions(db)
    db.close()

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

class StockRequest(BaseModel):
    current_price: float
    days_ahead: int = 1

class WeatherRequest(BaseModel):
    current_temp: float
    current_humidity: float
    days_ahead: int = 1

class PredictionHistoryResponse(BaseModel):
    id: int
    model_name: str
    model_version: str
    input_data: dict
    prediction: float
    confidence: Optional[float]
    created_at: datetime

class ModelVersionResponse(BaseModel):
    id: int
    model_name: str
    current_version: str
    description: Optional[str]
    accuracy: Optional[float]
    created_at: datetime
    updated_at: datetime

# ============= Helper Functions =============

def save_prediction(
    db: Session, 
    model_name: str, 
    model_version: str, 
    input_data: dict, 
    prediction: float,
    confidence: Optional[float] = None
):
    """Save prediction to history"""
    history = PredictionHistory(
        model_name=model_name,
        model_version=model_version,
        input_data=input_data,
        prediction=prediction,
        confidence=confidence,
        created_at=datetime.utcnow()
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

# ============= Routes =============

@app.get("/")
def root():
    return {
        "message": "ML Prediction API v2.0",
        "endpoints": {
            "salary": "/predict/salary",
            "house": "/predict/house",
            "crop": "/predict/crop",
            "stock": "/predict/stock",
            "weather": "/predict/weather"
        },
        "features": [
            "Prediction History",
            "Model Versioning",
            "5 Prediction Models"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": "2.0.0"}

@app.post("/predict/salary")
def predict_salary(request: SalaryRequest, db: Session = Depends(get_db)):
    """Predict salary based on years of experience"""
    try:
        prediction = salary_model.predict([[request.years_experience]])[0]
        
        # Save to history
        save_prediction(
            db, 
            "salary", 
            "v1.0", 
            {"years_experience": request.years_experience},
            float(prediction)
        )
        
        return {
            "predicted_salary": round(float(prediction), 2),
            "model": "Linear Regression",
            "version": "v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/house")
def predict_house(request: HouseRequest, db: Session = Depends(get_db)):
    """Predict house price based on area, bedrooms, and location"""
    try:
        if request.location.lower() not in location_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid location. Must be one of: {list(location_map.keys())}"
            )
        
        location_encoded = location_map[request.location.lower()]
        prediction = house_model.predict([[request.area, request.bedrooms, location_encoded]])[0]
        
        # Save to history
        save_prediction(
            db,
            "house",
            "v1.0",
            {"area": request.area, "bedrooms": request.bedrooms, "location": request.location},
            float(prediction)
        )
        
        return {
            "predicted_price": round(float(prediction), 2),
            "model": "Random Forest",
            "version": "v1.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/crop")
def predict_crop(request: CropRequest, db: Session = Depends(get_db)):
    """Predict crop yield based on rainfall and temperature"""
    try:
        prediction = crop_model.predict([[request.rainfall, request.temperature]])[0]
        
        # Save to history
        save_prediction(
            db,
            "crop",
            "v1.0",
            {"rainfall": request.rainfall, "temperature": request.temperature},
            float(prediction)
        )
        
        return {
            "predicted_yield": round(float(prediction), 2),
            "model": "Decision Tree",
            "version": "v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/stock")
def predict_stock(request: StockRequest, db: Session = Depends(get_db)):
    """Predict stock price N days ahead"""
    try:
        result = stock_predictor.predict(request.current_price, request.days_ahead)
        
        # Save to history
        save_prediction(
            db,
            "stock",
            "v1.0",
            {"current_price": request.current_price, "days_ahead": request.days_ahead},
            result["predicted_price"],
            result["confidence"]
        )
        
        return {
            **result,
            "model": "LSTM (simulated)",
            "version": "v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/weather")
def predict_weather(request: WeatherRequest, db: Session = Depends(get_db)):
    """Predict weather N days ahead"""
    try:
        result = weather_predictor.predict(
            request.current_temp, 
            request.current_humidity, 
            request.days_ahead
        )
        
        # Save to history
        save_prediction(
            db,
            "weather",
            "v1.0",
            {
                "current_temp": request.current_temp, 
                "current_humidity": request.current_humidity,
                "days_ahead": request.days_ahead
            },
            result["predicted_temperature"],
            result["confidence"]
        )
        
        return {
            **result,
            "model": "Random Forest",
            "version": "v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= History & Versioning Routes =============

@app.get("/history", response_model=List[PredictionHistoryResponse])
def get_prediction_history(
    limit: int = 50, 
    model_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get prediction history with optional filtering by model"""
    query = db.query(PredictionHistory)
    
    if model_name:
        query = query.filter(PredictionHistory.model_name == model_name)
    
    history = query.order_by(PredictionHistory.created_at.desc()).limit(limit).all()
    return history

@app.get("/history/stats")
def get_history_stats(db: Session = Depends(get_db)):
    """Get prediction history statistics"""
    total_predictions = db.query(PredictionHistory).count()
    
    # Count by model
    models = ["salary", "house", "crop", "stock", "weather"]
    model_counts = {}
    for model in models:
        count = db.query(PredictionHistory).filter(PredictionHistory.model_name == model).count()
        model_counts[model] = count
    
    return {
        "total_predictions": total_predictions,
        "predictions_by_model": model_counts
    }

@app.get("/models", response_model=List[ModelVersionResponse])
def get_model_versions(db: Session = Depends(get_db)):
    """Get all model versions"""
    versions = db.query(ModelVersion).all()
    return versions

@app.get("/models/{model_name}")
def get_model_info(model_name: str, db: Session = Depends(get_db)):
    """Get information about a specific model"""
    model_version = db.query(ModelVersion).filter(ModelVersion.model_name == model_name).first()
    
    if not model_version:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get recent predictions for this model
    recent_predictions = db.query(PredictionHistory).filter(
        PredictionHistory.model_name == model_name
    ).order_by(PredictionHistory.created_at.desc()).limit(10).all()
    
    return {
        "model_info": {
            "name": model_version.model_name,
            "version": model_version.current_version,
            "description": model_version.description,
            "accuracy": model_version.accuracy,
            "created_at": model_version.created_at,
            "updated_at": model_version.updated_at
        },
        "recent_predictions": len(recent_predictions),
        "total_predictions": db.query(PredictionHistory).filter(
            PredictionHistory.model_name == model_name
        ).count()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
