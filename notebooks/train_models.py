"""
Model Training Script
Trains and saves ML models for salary, house price, and crop yield predictions.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

# ============= Salary Model (Linear Regression) =============
print("Training Salary Model...")

salary_data = pd.read_csv('data/salary_data.csv')
X_salary = salary_data[['years_experience']]
y_salary = salary_data['salary']

X_train_sal, X_test_sal, y_train_sal, y_test_sal = train_test_split(
    X_salary, y_salary, test_size=0.2, random_state=42
)

salary_model = LinearRegression()
salary_model.fit(X_train_sal, y_train_sal)

y_pred_sal = salary_model.predict(X_test_sal)
print(f"  R² Score: {r2_score(y_test_sal, y_pred_sal):.4f}")
print(f"  MAE: ${mean_absolute_error(y_test_sal, y_pred_sal):,.2f}")

joblib.dump(salary_model, 'models/salary_model.pkl')
print("  Saved: models/salary_model.pkl")

# ============= House Price Model (Random Forest) =============
print("\nTraining House Price Model...")

house_data = pd.read_csv('data/house_data.csv')

# Encode location
location_map = {'rural': 0, 'suburban': 1, 'urban': 2}
house_data['location_encoded'] = house_data['location'].map(location_map)

X_house = house_data[['area', 'bedrooms', 'location_encoded']]
y_house = house_data['price']

X_train_house, X_test_house, y_train_house, y_test_house = train_test_split(
    X_house, y_house, test_size=0.2, random_state=42
)

house_model = RandomForestRegressor(n_estimators=100, random_state=42)
house_model.fit(X_train_house, y_train_house)

y_pred_house = house_model.predict(X_test_house)
print(f"  R² Score: {r2_score(y_test_house, y_pred_house):.4f}")
print(f"  MAE: ${mean_absolute_error(y_test_house, y_pred_house):,.2f}")

joblib.dump(house_model, 'models/house_model.pkl')
joblib.dump(location_map, 'models/location_map.pkl')
print("  Saved: models/house_model.pkl")
print("  Saved: models/location_map.pkl")

# ============= Crop Yield Model (Decision Tree) =============
print("\nTraining Crop Yield Model...")

crop_data = pd.read_csv('data/crop_data.csv')

X_crop = crop_data[['rainfall', 'temperature']]
y_crop = crop_data['yield']

X_train_crop, X_test_crop, y_train_crop, y_test_crop = train_test_split(
    X_crop, y_crop, test_size=0.2, random_state=42
)

crop_model = DecisionTreeRegressor(random_state=42)
crop_model.fit(X_train_crop, y_train_crop)

y_pred_crop = crop_model.predict(X_test_crop)
print(f"  R² Score: {r2_score(y_test_crop, y_pred_crop):.4f}")
print(f"  MAE: {mean_absolute_error(y_test_crop, y_pred_crop):.4f}")

joblib.dump(crop_model, 'models/crop_model.pkl')
print("  Saved: models/crop_model.pkl")

print("\n✅ All models trained and saved successfully!")
