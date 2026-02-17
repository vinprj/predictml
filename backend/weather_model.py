"""
Weather Forecast Model (Simulated)
Uses simple heuristics for weather prediction
"""
import numpy as np
from datetime import datetime, timedelta

class WeatherPredictor:
    """Simulated weather forecast model"""
    
    def __init__(self):
        # Simulated model parameters
        self.temperature_persistence = 0.7  # Weather tends to persist
        self.temperature_mean_reversion = 20  # Long-term average temp (°C)
        
    def predict(self, current_temp: float, current_humidity: float, days_ahead: int = 1) -> dict:
        """
        Predict weather N days ahead
        
        Args:
            current_temp: Current temperature in Celsius
            current_humidity: Current humidity percentage (0-100)
            days_ahead: Number of days to predict ahead
            
        Returns:
            dict with temperature, humidity, and conditions prediction
        """
        # Temperature prediction with mean reversion
        temp_change = (self.temperature_mean_reversion - current_temp) * 0.1 * days_ahead
        temp_noise = np.random.normal(0, 2 * np.sqrt(days_ahead))
        predicted_temp = current_temp + temp_change + temp_noise
        
        # Humidity prediction
        humidity_noise = np.random.normal(0, 5 * np.sqrt(days_ahead))
        predicted_humidity = np.clip(current_humidity + humidity_noise, 0, 100)
        
        # Determine weather condition
        if predicted_humidity > 70:
            if predicted_temp > 15:
                condition = "Rainy"
                precipitation_chance = min(95, 50 + predicted_humidity * 0.5)
            else:
                condition = "Snowy"
                precipitation_chance = min(95, 40 + predicted_humidity * 0.4)
        elif predicted_humidity > 50:
            condition = "Cloudy"
            precipitation_chance = min(60, predicted_humidity * 0.6)
        else:
            condition = "Sunny"
            precipitation_chance = max(5, predicted_humidity * 0.3)
        
        # Confidence decreases with prediction horizon
        confidence = max(0.4, 0.95 - (days_ahead * 0.08))
        
        return {
            "predicted_temperature": round(predicted_temp, 1),
            "predicted_humidity": round(predicted_humidity, 1),
            "condition": condition,
            "precipitation_chance": round(precipitation_chance, 1),
            "confidence": round(confidence, 2),
            "days_ahead": days_ahead,
            "forecast_date": (datetime.utcnow() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        }

# Create a singleton instance
weather_predictor = WeatherPredictor()
