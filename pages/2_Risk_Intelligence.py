import streamlit as st
import numpy as np
from database import init_db, get_user_transactions
from ml_model import train_user_model, predict_user_risk

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Risk Intelligence", layout="wide")

# ================= SESSION SAFETY =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated or st.session_state.username is None:
    st.warning("Session expired. Please login again.")
    st.stop()

# ================= INIT DB =================
init_db()

st.title("🧠 AI Behavioral Risk Intelligence Engine")

username = st.session_state.username

# ================= REFRESH BUTTON =================
if st.button("🔄 Refresh Data"):
    st.rerun()

# ================= FETCH USER DATA =================
user_history = get_user_transactions(username)

# Ensure clean float conversion
user_history = [float(x) for x in user_history] if user_history else []

# ================= NEW USER CASE =================
if len(user_history) == 0:
    st.info("👋 Welcome! Your AI Risk Engine is not activated yet.")
    st.warning("Generate your first QR transaction to start building behavioral intelligence.")

    st.markdown("### 🚀 Activation Steps")
    st.markdown("""
    1️⃣ Generate QR  
    2️⃣ Complete transaction  
    3️⃣ AI learns your pattern  
    4️⃣ Risk scoring activates automatically  
    """)

    st.progress(0)
    st.metric("Model Confidence", "0%")
    st.stop()

# ================= LEARNING PHASE =================
if len(user_history) < 5:
    st.info(f"🧠 Learning Phase: {len(user_history)}/5 transactions collected")
    st.progress(len(user_history) / 5)

    st.metric("Model Confidence", f"{len(user_history) * 20}%")
    st.success("AI is building your behavioral baseline.")
    st.stop()

# ================= RISK CALCULATION =================
latest_amount = user_history[-1]
historical_data = np.array(user_history[:-1], dtype=float)

avg_amount = np.mean(historical_data)
std_dev = np.std(historical_data)

if std_dev == 0:
    std_dev = 1

deviation_score = abs(latest_amount - avg_amount) / std_dev
behavioral_risk = min(80, deviation_score * 20)

# ================= ML MODEL =================
@st.cache_resource
def load_model(data):
    return train_user_model(data)

model = load_model(tuple(historical_data))
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
st.progress(risk_percent / 100)
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