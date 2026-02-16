# ML Prediction API

A simple FastAPI-based ML prediction service with three models for salary, house price, and crop yield predictions.

## Features

- **Salary Prediction** - Linear Regression model predicting salary based on years of experience
- **House Price Prediction** - Random Forest model predicting house prices based on area, bedrooms, and location
- **Crop Yield Prediction** - Decision Tree model predicting crop yield based on rainfall and temperature

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Training Models

```bash
jupyter notebook notebooks/train_models.ipynb
```

Or run the training script:

```bash
python notebooks/train_models.py
```

### Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /predict/salary

Predict salary based on years of experience.

**Request:**
```json
{
  "years_experience": 5
}
```

**Response:**
```json
{
  "predicted_salary": 75000.0,
  "model": "Linear Regression"
}
```

### POST /predict/house

Predict house price based on area, bedrooms, and location.

**Request:**
```json
{
  "area": 2000,
  "bedrooms": 3,
  "location": "urban"
}
```

**Response:**
```json
{
  "predicted_price": 350000.0,
  "model": "Random Forest"
}
```

### POST /predict/crop

Predict crop yield based on rainfall and temperature.

**Request:**
```json
{
  "rainfall": 100,
  "temperature": 25
}
```

**Response:**
```json
{
  "predicted_yield": 4.5,
  "model": "Decision Tree"
}
```

## Project Structure

```
predictml/
├── data/
│   ├── salary_data.csv
│   ├── house_data.csv
│   └── crop_data.csv
├── models/
│   ├── salary_model.pkl
│   ├── house_model.pkl
│   └── crop_model.pkl
├── notebooks/
│   ├── train_models.ipynb
│   └── train_models.py
├── main.py
├── requirements.txt
└── README.md
```

## Model Performance Metrics

### Salary Prediction (Linear Regression)
- **Training R² Score**: 0.98
- **Features**: years_experience

### House Price Prediction (Random Forest)
- **Training R² Score**: 0.95
- **Features**: area, bedrooms, location
- **Location encoding**: rural=0, suburban=1, urban=2

### Crop Yield Prediction (Decision Tree)
- **Training R² Score**: 0.92
- **Features**: rainfall, temperature

## License

MIT
