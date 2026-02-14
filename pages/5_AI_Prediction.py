import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🤖 AI Market Prediction Lab")

# -----------------------------
# Select Stock
# -----------------------------
tickers = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "RELIANCE": "RELIANCE.NS",
}

option = st.selectbox("Select Stock / Index", list(tickers.keys()))
symbol = tickers[option]

# -----------------------------
# Fetch Data
# -----------------------------
data = yf.download(symbol, period="3mo", interval="1d", progress=False)

if data.empty:
    st.error("No data available.")
    st.stop()

data = data.dropna()

# Flatten multi-index if needed
if hasattr(data.columns, "levels"):
    data.columns = data.columns.get_level_values(0)

# -----------------------------
# Feature Engineering
# -----------------------------
data["Return"] = data["Close"].pct_change()
data["Volatility"] = data["Return"].rolling(5).std()
data = data.dropna()

# Create prediction target (next day close)
data["Next_Close"] = data["Close"].shift(-1)
data = data.dropna()

X = data[["Close"]]
y = data["Next_Close"]

# -----------------------------
# Train Model
# -----------------------------
model = LinearRegression()
model.fit(X, y)

latest_close = float(data["Close"].iloc[-1])
predicted_price = float(model.predict([[latest_close]])[0])

# -----------------------------
# Direction Prediction
# -----------------------------
if predicted_price > latest_close:
    direction = "UP 📈"
else:
    direction = "DOWN 📉"

# -----------------------------
# Volatility Forecast
# -----------------------------
volatility = float(data["Volatility"].iloc[-1]) * 100

# -----------------------------
# Fraud Likelihood (Demo Logic)
# -----------------------------
fraud_prob = min(abs(volatility) * 10, 100)

# -----------------------------
# Display Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", f"₹{latest_close:.2f}")
col2.metric("Predicted Next Price", f"₹{predicted_price:.2f}")
col3.metric("Predicted Direction", direction)
col4.metric("Volatility %", f"{volatility:.2f}%")

st.divider()

# Fraud Probability Meter
st.subheader("🛑 Fraud / Risk Probability")
st.progress(int(fraud_prob))

if fraud_prob > 70:
    st.error(f"High Risk Probability: {fraud_prob:.1f}%")
elif fraud_prob > 40:
    st.warning(f"Moderate Risk Probability: {fraud_prob:.1f}%")
else:
    st.success(f"Low Risk Probability: {fraud_prob:.1f}%")

st.divider()

# -----------------------------
# Chart with Prediction Line
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Close"],
    mode='lines',
    name="Historical Price"
))

fig.add_trace(go.Scatter(
    x=[data.index[-1]],
    y=[predicted_price],
    mode='markers',
    name="Predicted Next Price"
))

fig.update_layout(
    template="plotly_dark",
    title="AI Price Prediction",
    height=450
)

st.plotly_chart(fig, use_container_width=True)