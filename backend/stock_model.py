"""
Stock Price Prediction Model (Simulated)
Uses simple linear regression with trend and volatility factors
"""
import numpy as np

class StockPredictor:
    """Simulated stock price prediction model"""
    
    def __init__(self):
        # Simulated model parameters
        self.trend_weight = 0.05  # Average daily trend
        self.volatility = 0.02  # Price volatility
        
    def predict(self, current_price: float, days_ahead: int = 1) -> dict:
        """
        Predict stock price N days ahead
        
        Args:
            current_price: Current stock price
            days_ahead: Number of days to predict ahead
            
        Returns:
            dict with prediction, confidence, and range
        """
        # Simple trend-based prediction with random walk
        trend = current_price * self.trend_weight * days_ahead
        noise = np.random.normal(0, current_price * self.volatility * np.sqrt(days_ahead))
        
        predicted_price = current_price + trend + noise
        
        # Calculate confidence interval (95%)
        std_error = current_price * self.volatility * np.sqrt(days_ahead)
        lower_bound = predicted_price - 1.96 * std_error
        upper_bound = predicted_price + 1.96 * std_error
        
        # Confidence decreases with prediction horizon
        confidence = max(0.5, 1.0 - (days_ahead * 0.05))
        
        return {
            "predicted_price": round(predicted_price, 2),
            "confidence": round(confidence, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "days_ahead": days_ahead
        }

# Create a singleton instance
stock_predictor = StockPredictor()
