# Weather Prediction ML Project

## Overview
A machine learning project that uses a Random Forest Classifier to predict weather types (e.g., Sunny, Rainy, Cloudy) based on sensor values like temperature, humidity, precipitation, and UV index. Features a real-time dashboard with simulated sensor data.

## Project Architecture
- **app.py** - Flask web application with weather dashboard, sensor data simulation, and ML prediction
- **main.py** - Entry point for gunicorn (imports app from app.py)
- **train_model.py** - Trains the weather classification model using the CSV dataset and saves the model/encoder as `.pkl` files
- **predict_weather.py** - Makes weather predictions using hardcoded sensor values
- **live_predict.py** - Reads live sensor data from an Arduino via serial port (requires hardware)
- **weather_classification_data.csv** - Training dataset
- **weather_model.pkl** - Pre-trained Random Forest model
- **label_encoder.pkl** - Label encoder for weather type categories
- **templates/** - HTML templates for dashboard pages (index, temp_humidity, precipitation, uv_index, prediction)
- **static/** - Static assets (CSS, JS)

## How to Run
- The app runs via gunicorn on port 5000
- Dashboard shows simulated sensor data with real-time ML predictions
- Navigate between pages: Dashboard, Temp & Humidity, Precipitation, UV Index, AI Prediction

## Dependencies
- Python 3.11
- Flask
- pandas
- scikit-learn
- joblib
- numpy
- gunicorn
- pyserial

## Recent Changes
- 2026-02-14: Completed migration to Replit environment, installed all dependencies, configured gunicorn workflow
