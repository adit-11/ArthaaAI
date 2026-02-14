# 🚀 Artha AI  
### Intelligent Fintech Risk & Market Intelligence Platform

Artha AI is a modular AI-powered fintech intelligence platform built using Python and Streamlit.  
It integrates secure authentication, transaction risk detection, behavioral anomaly analysis, live market tracking, and AI-based price prediction into a unified dashboard.

This project demonstrates how machine learning models can be embedded into financial systems for fraud detection, risk scoring, and predictive analytics.

---

## 🌟 Key Features

### 🔐 Authentication & Security
- User Registration & Login
- SHA-256 Password Hashing
- SQLite Database Storage
- Session-Based Access Control
- Protected Dashboard Access

### 💳 Secure Transaction & QR Module
- UPI QR Code Generation (Fixed & Dynamic)
- Transaction Logging
- ML-Based Risk Detection
- Automatic High-Risk Blocking
- User-Specific Transaction History

### 🧠 Behavioral Risk Intelligence Engine
- Isolation Forest Anomaly Detection
- Transaction Deviation Analysis
- Risk Score (0–95%)
- Confidence Calculation
- Behavioral Insights Dashboard

### 📊 Live Market Intelligence
- NSE/BSE Data via yfinance
- Intraday Candlestick Charts
- Real-Time Price Metrics
- Volatility-Based Market Risk Index

### 🤖 AI Market Prediction Lab
- Linear Regression Model
- Next-Day Price Estimation
- Direction Forecast (UP / DOWN)
- Volatility-Based Risk Probability
- Interactive Plotly Visualization

### 📈 Smart Transaction Analytics
- Total Transactions
- Total Revenue
- Average & Maximum Transaction
- Risk Distribution Pie Chart
- Transaction Trend Visualization

---

## 🏗 System Architecture

### High-Level Architecture

```
+-------------------------------------------------------------------+
|                              USER                                 |
|                    (Browser / Streamlit UI)                       |
+-------------------------------------------------------------------+
                                |
                                v
+-------------------------------------------------------------------+
|                       PRESENTATION LAYER                          |
|  Login • Dashboard • QR Generator • Charts • Analytics           |
+-------------------------------------------------------------------+
                                |
                                v
+-------------------------------------------------------------------+
|                       APPLICATION LAYER                           |
|  Authentication • Transaction Manager • Risk Engine              |
|  Market Data Handler • Prediction Engine                         |
+-------------------------------------------------------------------+
            |                               |
            v                               v
+-----------------------------+    +------------------------------+
|     MACHINE LEARNING LAYER  |    |       EXTERNAL DATA         |
|  LogisticRegression         |    |  yfinance (NSE/BSE)         |
|  IsolationForest            |    +------------------------------+
|  LinearRegression           |
+-----------------------------+
            |
            v
+-------------------------------------------------------------------+
|                          DATA LAYER                               |
|  SQLite Database (users, transactions)                            |
|  Session State                                                    |
+-------------------------------------------------------------------+
```

---

## 🔁 Core Functional Flows

### 🔐 Authentication Flow

```
User Login
   ↓
Password Hash (SHA-256)
   ↓
Validate Against SQLite
   ↓
Session State Updated
   ↓
Access Dashboard
```

---

### 💳 Transaction & Risk Flow

```
Transaction Created
      ↓
Stored in Database
      ↓
Historical Data Extracted
      ↓
IsolationForest Model
      ↓
Anomaly Score Generated
      ↓
Final Risk Score (0–95%)
      ↓
Displayed on Dashboard
```

Risk Formula:

```
Final Risk = Behavioral Deviation + ML Boost
Confidence = min(100, transaction_count × 10)
```

---

### 📊 Market Intelligence Flow

```
Select Stock
      ↓
Fetch Data via yfinance
      ↓
Data Cleaning & Processing
      ↓
Candlestick Rendering
      ↓
Volatility Calculation
      ↓
Market Risk Classification
```

---

### 🤖 Prediction Engine Flow

```
Historical Market Data
      ↓
Feature Engineering
 (Returns + Volatility)
      ↓
LinearRegression Model
      ↓
Next-Day Price Prediction
      ↓
Direction + Risk Probability
```

---

## 🧠 Machine Learning Models Used

| Model               | Purpose                                  |
|--------------------|------------------------------------------|
| LogisticRegression | Basic transaction risk classification    |
| IsolationForest    | Behavioral anomaly detection             |
| LinearRegression   | Stock price prediction                   |

---

## 🗄 Database Structure

### users
- id
- username
- password (hashed)

### transactions
- id
- username
- amount

---

## 🛠 Technology Stack

| Layer        | Technology |
|-------------|------------|
| Frontend    | Streamlit  |
| Backend     | Python     |
| Database    | SQLite     |
| ML          | scikit-learn |
| Market API  | yfinance   |
| Data        | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Security    | hashlib (SHA-256) |

---

## 📦 Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/adit-11/ArthaaAI.git
cd ArthaaAI/ArthaAI
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### requirements.txt

```
streamlit
pandas
numpy
plotly
yfinance
scikit-learn
requests
```

### 4️⃣ Run Application

```bash
streamlit run main.py
```

---

## 🎨 Design Philosophy

- Modular architecture
- Clear separation of concerns
- Lightweight database integration
- Reproducible ML workflow
- Clean financial UI theme
- Scalable structure for future backend expansion

---

## 🚀 Future Enhancements

- FastAPI backend integration
- Deep learning-based fraud detection
- Real UPI payment gateway integration
- Cloud deployment (AWS / Azure)
- Admin analytics dashboard
- Portfolio risk scoring engine

---

## 👨‍💻 Author

Aditya Anand  
B.Tech – Information Technology  
Manipal University Jaipur  

---

## ⭐ Support

If you found this project useful:

⭐ Star the repository  
🍴 Fork it  
🚀 Share it  
