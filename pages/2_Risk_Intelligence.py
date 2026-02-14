import streamlit as st
import numpy as np
from database import init_db, get_user_transactions
from ml_model import train_user_model, predict_user_risk

# 🔐 Protect page
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please login first.")
    st.stop()

init_db()

st.title("🧠 AI Behavioral Risk Intelligence Engine")

username = st.session_state.username
user_history = get_user_transactions(username)

if len(user_history) == 0:
    st.info("No transactions found. Please generate a QR first.")
    st.stop()

# ================= LEARNING PHASE =================
if len(user_history) < 5:
    st.info(f"Learning phase: {len(user_history)}/5 transactions collected.")
    st.progress(len(user_history) * 20)
    st.success("AI is building behavioral baseline.")
    st.stop()

# ================= USE LAST TRANSACTION =================
latest_amount = user_history[-1]
historical_data = user_history[:-1]

avg_amount = np.mean(historical_data)
std_dev = np.std(historical_data)
if std_dev == 0:
    std_dev = 1

deviation_score = abs(latest_amount - avg_amount) / std_dev
behavioral_risk = min(80, deviation_score * 20)

# ================= ML MODEL =================
model = train_user_model(historical_data)
prediction, anomaly_strength = predict_user_risk(model, latest_amount)

ml_boost = 0
if prediction == -1:
    ml_boost = min(20, abs(anomaly_strength) * 10)

# ================= FINAL SCORE =================
risk_percent = int(min(95, behavioral_risk + ml_boost))
confidence = min(100, len(historical_data) * 10)

# ================= DISPLAY =================
st.subheader("📊 Risk Assessment Result")

st.metric("Risk Score", f"{risk_percent}%")
st.progress(risk_percent)
st.metric("Model Confidence", f"{confidence}%")

if risk_percent < 30:
    st.success("✅ Low Risk – Normal Behavioral Pattern")
elif risk_percent < 70:
    st.warning("⚠ Moderate Risk – Pattern Deviation Detected")
else:
    st.error("🚨 High Risk – Strong Behavioral Anomaly")

st.write("### Behavioral Insights")
st.write(f"• Average Amount: ₹{round(avg_amount,2)}")
st.write(f"• Standard Deviation: ₹{round(std_dev,2)}")
st.write(f"• Deviation Score: {round(deviation_score,2)}")