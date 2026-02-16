"""
Model Training Script - Train and save all ML models
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import os

# Create models directory
os.makedirs("backend/models", exist_ok=True)

print("=" * 50)
print("Training ML Models for PredictML")
print("=" * 50)

# ============================================
# 1. House Price Model (Indian Cities)
# ============================================
print("\n[1/3] Training House Price Model...")

# Generate synthetic house price data for Indian cities
np.random.seed(42)
n_samples = 2000

cities = ["mumbai", "delhi", "bangalore", "chennai", "hyderabad", "pune", "kolkata", "ahmedabad"]
city_prices = {
    "mumbai": 25000, "delhi": 18000, "bangalore": 22000, "chennai": 15000,
    "hyderabad": 14000, "pune": 12000, "kolkata": 10000, "ahmedabad": 9000
}

house_data = []
for city in cities:
    base_price = city_prices[city]
    for _ in range(n_samples // len(cities)):
        area = np.random.uniform(500, 5000)
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 4)
        age = np.random.randint(0, 30)
        location_rating = np.random.uniform(1, 5)
        
        price = (base_price * area * 
                 (1 + 0.1 * bedrooms + 0.05 * bathrooms) *
                 (1 - 0.01 * age) *
                 (0.8 + 0.1 * location_rating))
        price += np.random.normal(0, price * 0.1)
        
        house_data.append({
            "city": city,
            "area_sqft": area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "age": age,
            "location_rating": location_rating,
            "price": price
        })

df_house = pd.DataFrame(house_data)
city_map = {city: i for i, city in enumerate(cities)}
df_house["city_encoded"] = df_house["city"].map(city_map)

X_house = df_house[["city_encoded", "area_sqft", "bedrooms", "bathrooms", "age", "location_rating"]]
y_house = df_house["price"]

X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_house, y_house, test_size=0.2, random_state=42)

house_scaler = StandardScaler()
X_train_h_scaled = house_scaler.fit_transform(X_train_h)
X_test_h_scaled = house_scaler.transform(X_test_h)

house_model = GradientBoostingRegressor(n_estimators=200, max_depth=6, random_state=42)
house_model.fit(X_train_h_scaled, y_train_h)

y_pred_h = house_model.predict(X_test_h_scaled)
print(f"   R2 Score: {r2_score(y_test_h, y_pred_h):.4f}")
print(f"   RMSE: {np.sqrt(mean_squared_error(y_test_h, y_pred_h)):,.0f}")
print(f"   MAE: {mean_absolute_error(y_test_h, y_pred_h):,.0f}")

joblib.dump(house_model, "backend/models/house_price_model.pkl")
joblib.dump(house_scaler, "backend/models/house_scaler.pkl")
print("   ✓ House Price Model saved")

# ============================================
# 2. Salary Model
# ============================================
print("\n[2/3] Training Salary Model...")

np.random.seed(42)
n_samples = 3000

job_types = ["it", "healthcare", "finance", "engineering", "sales", "marketing"]
job_base = {"it": 80000, "healthcare": 90000, "finance": 85000, 
            "engineering": 75000, "sales": 60000, "marketing": 65000}
edu_multiplier = {"high_school": 0.7, "bachelor": 1.0, "master": 1.3, "phd": 1.6}
city_tier_mult = {1: 1.3, 2: 1.0, 3: 0.7}

salary_data = []
for _ in range(n_samples):
    experience = np.random.uniform(0, 20)
    education = np.random.choice(["high_school", "bachelor", "master", "phd"])
    job = np.random.choice(job_types)
    city_tier = np.random.choice([1, 2, 3])
    n_skills = np.random.randint(0, 10)
    
    base = job_base[job] * edu_multiplier[education] * city_tier_mult[city_tier]
    salary = base * (1 + 0.05 * experience) + n_skills * 3000
    salary += np.random.normal(0, salary * 0.1)
    
    salary_data.append({
        "experience": experience,
        "education": education,
        "job_type": job,
        "city_tier": city_tier,
        "n_skills": n_skills,
        "salary": salary
    })

df_salary = pd.DataFrame(salary_data)
edu_map = {"high_school": 0, "bachelor": 1, "master": 2, "phd": 3}
job_map = {job: i for i, job in enumerate(job_types)}

df_salary["edu_encoded"] = df_salary["education"].map(edu_map)
df_salary["job_encoded"] = df_salary["job_type"].map(job_map)

X_salary = df_salary[["experience", "edu_encoded", "job_encoded", "city_tier", "n_skills"]]
y_salary = df_salary["salary"]

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_salary, y_salary, test_size=0.2, random_state=42)

salary_scaler = StandardScaler()
X_train_s_scaled = salary_scaler.fit_transform(X_train_s)
X_test_s_scaled = salary_scaler.transform(X_test_s)

salary_model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
salary_model.fit(X_train_s_scaled, y_train_s)

y_pred_s = salary_model.predict(X_test_s_scaled)
print(f"   R2 Score: {r2_score(y_test_s, y_pred_s):.4f}")
print(f"   RMSE: {np.sqrt(mean_squared_error(y_test_s, y_pred_s)):,.0f}")
print(f"   MAE: {mean_absolute_error(y_test_s, y_pred_s):,.0f}")

joblib.dump(salary_model, "backend/models/salary_model.pkl")
joblib.dump(salary_scaler, "backend/models/salary_scaler.pkl")
print("   ✓ Salary Model saved")

# ============================================
# 3. Crop Yield Model
# ============================================
print("\n[3/3] Training Crop Yield Model...")

np.random.seed(42)
n_samples = 2500

crops = ["rice", "wheat", "cotton", "sugarcane", "maize", "soybean", "potato"]
crop_yield_base = {
    "rice": 3000, "wheat": 3500, "cotton": 1500, "sugarcane": 70000,
    "maize": 4000, "soybean": 2500, "potato": 25000
}
states = ["punjab", "haryana", "up", "mp", "maharashtra", "karnataka", "tn", "wb"]

crop_data = []
for crop in crops:
    base = crop_yield_base[crop]
    for _ in range(n_samples // len(crops)):
        area = np.random.uniform(1, 50)
        rainfall = np.random.uniform(200, 1500)
        temp = np.random.uniform(15, 40)
        fertilizer = np.random.uniform(0, 500)
        pesticide = np.random.uniform(0, 100)
        state = np.random.choice(states)
        
        # Environmental factors affect yield
        rain_factor = min(1.2, max(0.6, rainfall / 800))
        temp_factor = min(1.1, max(0.7, 1 - abs(temp - 25) / 30))
        yield_per_ha = base * rain_factor * temp_factor * (1 + 0.001 * fertilizer) * (1 - 0.001 * pesticide)
        total_yield = yield_per_ha * area + np.random.normal(0, yield_per_ha * 0.1)
        
        crop_data.append({
            "crop": crop,
            "state": state,
            "area": area,
            "rainfall": rainfall,
            "temp": temp,
            "fertilizer": fertilizer,
            "pesticide": pesticide,
            "yield": total_yield
        })

df_crop = pd.DataFrame(crop_data)
crop_map = {crop: i for i, crop in enumerate(crops)}
state_map = {state: i for i, state in enumerate(states)}

df_crop["crop_encoded"] = df_crop["crop"].map(crop_map)
df_crop["state_encoded"] = df_crop["state"].map(state_map)

X_crop = df_crop[["crop_encoded", "state_encoded", "area", "rainfall", "temp", "fertilizer", "pesticide"]]
y_crop = df_crop["yield"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_crop, y_crop, test_size=0.2, random_state=42)

crop_scaler = StandardScaler()
X_train_c_scaled = crop_scaler.fit_transform(X_train_c)
X_test_c_scaled = crop_scaler.transform(X_test_c)

crop_model = GradientBoostingRegressor(n_estimators=200, max_depth=8, random_state=42)
crop_model.fit(X_train_c_scaled, y_train_c)

y_pred_c = crop_model.predict(X_test_c_scaled)
print(f"   R2 Score: {r2_score(y_test_c, y_pred_c):.4f}")
print(f"   RMSE: {np.sqrt(mean_squared_error(y_test_c, y_pred_c)):,.0f}")
print(f"   MAE: {mean_absolute_error(y_test_c, y_pred_c):,.0f}")

joblib.dump(crop_model, "backend/models/crop_yield_model.pkl")
joblib.dump(crop_scaler, "backend/models/crop_scaler.pkl")
print("   ✓ Crop Yield Model saved")

print("\n" + "=" * 50)
print("All models trained and saved successfully!")
print("=" * 50)
