"""Database models for prediction history and model versions"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///predictions.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)  # salary, house, crop, stock, weather
    model_version = Column(String, nullable=False)  # v1.0, v1.1, etc.
    input_data = Column(JSON, nullable=False)  # Store input parameters as JSON
    prediction = Column(Float, nullable=False)
    confidence = Column(Float, nullable=True)  # Optional confidence score
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False, unique=True)
    current_version = Column(String, nullable=False)  # v1.0, v1.1, etc.
    description = Column(Text, nullable=True)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_model_versions(db):
    """Initialize model versions if they don't exist"""
    models = [
        {"model_name": "salary", "current_version": "v1.0", "description": "Linear Regression", "accuracy": 0.98},
        {"model_name": "house", "current_version": "v1.0", "description": "Random Forest", "accuracy": 0.95},
        {"model_name": "crop", "current_version": "v1.0", "description": "Decision Tree", "accuracy": 0.92},
        {"model_name": "stock", "current_version": "v1.0", "description": "LSTM (simulated)", "accuracy": 0.85},
        {"model_name": "weather", "current_version": "v1.0", "description": "Random Forest", "accuracy": 0.88},
    ]
    
    for model_data in models:
        exists = db.query(ModelVersion).filter(ModelVersion.model_name == model_data["model_name"]).first()
        if not exists:
            model_version = ModelVersion(**model_data)
            db.add(model_version)
    
    db.commit()
