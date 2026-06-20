# 🌾 IoT-Based Crop Yield Prediction System

An intelligent web application that predicts crop yield using **Machine Learning** and **real-time IoT sensor data**. The system integrates an **ESP32/Arduino** with soil moisture, temperature, and humidity sensors to provide accurate crop recommendations and yield predictions through an interactive dashboard.

> **Note:** This project was developed for educational purposes to demonstrate the integration of IoT and Machine Learning for smart agriculture.

---

## 🚀 Live Demo

[https://your-render-app.onrender.com](https://crop-yield-prediction-3-k9yv.onrender.com)

---

## 📸 Preview

<img width="1332" height="800" alt="image" src="https://github.com/user-attachments/assets/efaa0cf3-aa67-48d6-922a-01129b12a28d" />
<img width="981" height="684" alt="image" src="https://github.com/user-attachments/assets/580808a2-fed2-4a16-b6eb-8af339d6c3be" />
<img width="1398" height="780" alt="image" src="https://github.com/user-attachments/assets/2c623845-f1b7-4003-8a0e-592b07c5ec07" />

---

## ✨ Features

### 🌱 Crop Prediction
- Predicts crop yield using Machine Learning.
- Recommends the most suitable crop based on environmental conditions.
- Displays prediction results using interactive charts.

### 📡 IoT Integration
- Real-time soil moisture monitoring.
- Live temperature monitoring.
- Live humidity monitoring.
- ESP32/Arduino-based sensor integration.
- Automatic sensor data updates.

### 📊 Dashboard
- User-friendly dashboard.
- Real-time sensor values.
- Crop recommendation panel.
- Interactive yield prediction graph.
- Historical sensor data visualization.

### 🤖 Machine Learning
- Random Forest Regression model.
- One-Hot Encoding for categorical features.
- Predicts yield using:
  - Season
  - Crop
  - Area
  - Soil Moisture
  - Temperature
  - Humidity

### 💾 Data Management
- SQLite database for sensor readings.
- Sensor history tracking.
- Model performance metrics.

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Random Forest Regressor
- Pandas
- NumPy
- Pickle

### Database
- SQLite

### IoT Hardware
- ESP32 / Arduino
- DHT22 Temperature & Humidity Sensor
- Soil Moisture Sensor

### Deployment
- Render

---

## 📂 Project Structure

```text
Crop_Yield_Prediction/
│
├── app.py
├── train_crop_yield.py
├── sensor_db.py
├── crop_yield.csv
├── crop_season_meta.json
├── metrics.json
├── requirements.txt
├── esp32_sensor_example.ino
├── README.md
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── history.html
│   ├── about.html
│   └── base.html
│
├── static/
│   └── css/
│       └── dashboard.css
│
└── model.pkl
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Rishh16/Crop-Yield-Prediction.git
```

### Navigate to the project

```bash
cd Crop-Yield-Prediction
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Train the Machine Learning model

```bash
python train_crop_yield.py
```

### Run the application

```bash
python app.py
```

### Open in your browser

```
http://127.0.0.1:5000
```

---

## 🌾 How It Works

1. The ESP32/Arduino collects:
   - Soil Moisture
   - Temperature
   - Humidity

2. Sensor readings are sent to the Flask backend through REST APIs.

3. The backend stores the readings in an SQLite database.

4. The Machine Learning model processes:
   - Season
   - Area
   - Soil Moisture
   - Temperature
   - Humidity

5. The system predicts crop yield and recommends the most suitable crop.

6. Results are displayed through an interactive dashboard with charts and sensor history.

---

## 📈 Machine Learning Model

- Algorithm: Random Forest Regressor
- Data Preprocessing:
  - One-Hot Encoding
  - Feature Engineering
- Training Dataset:
  - Historical Crop Yield Dataset
- Model Serialization:
  - Pickle (`model.pkl`)

---

## 📡 IoT Architecture

**Hardware Components**

- ESP32 / Arduino
- Soil Moisture Sensor
- DHT22 Temperature & Humidity Sensor

The ESP32 continuously collects environmental data and sends it to the Flask server through REST APIs. The latest readings are stored in SQLite and used by the Machine Learning model to generate crop recommendations.

---

## 📊 Project Workflow

```
ESP32 + Sensors
        │
        ▼
Flask REST API
        │
        ▼
SQLite Database
        │
        ▼
Machine Learning Model
        │
        ▼
Crop Recommendation
        │
        ▼
Interactive Dashboard
```

---

## 🌐 Deployment

The application is deployed using **Render**.

---

## 📌 Future Enhancements

- Weather API Integration
- Fertilizer Recommendation System
- Crop Disease Detection
- Mobile Application
- Cloud IoT Integration
- SMS & Email Alerts
- AI-based Farming Insights
- Multi-language Support
- Farmer Authentication System

---

## 👩‍💻 Author

**Rishika Nakirtha**

GitHub: https://github.com/Rishh16

---

## 📄 License

This project is developed for educational and portfolio purposes only.
