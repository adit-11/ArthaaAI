import streamlit as st
import numpy as np
import qrcode
from io import BytesIO
from sklearn.linear_model import LogisticRegression
from database import insert_transaction

st.title("💳 AI Secure UPI QR Generator")

# ----------------------------
# 🔐 Authentication Check
# ----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated or st.session_state.username is None:
    st.warning("Please login first.")
    st.stop()

username = st.session_state.username.lower()

# ----------------------------
# Initialize Session State
# ----------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "model" not in st.session_state:
    st.session_state.model = LogisticRegression()

if "model_trained" not in st.session_state:
    st.session_state.model_trained = False

# ----------------------------
# User Inputs
# ----------------------------
amount = st.number_input("Enter Amount (₹)", min_value=1.0, step=1.0)
upi_id = st.text_input("Enter Receiver UPI ID", value="yourupi@okaxis")
name = st.text_input("Receiver Name", value="Aditya")
note = st.text_input("Transaction Note", value="AI Secure Payment")

payment_type = st.radio(
    "Select Payment Type",
    ["Fixed Amount (Auto Filled)", "Dynamic Amount (User Enters Manually)"]
)

# ----------------------------
# Generate QR Button
# ----------------------------
if st.button("Generate Secure QR"):

    # Save locally for ML learning
    st.session_state.transactions.append({"amount": amount})

    # ----------------------------
    # Train model ONLY ONCE after 5 transactions
    # ----------------------------
    if (
        len(st.session_state.transactions) == 5
        and not st.session_state.model_trained
    ):

        X = np.array([[t["amount"]] for t in st.session_state.transactions])
        y = np.array(
            [1 if t["amount"] > 5000 else 0
             for t in st.session_state.transactions]
        )

        if len(np.unique(y)) > 1:
            st.session_state.model.fit(X, y)
            st.session_state.model_trained = True
            st.success("AI Risk Model Trained ✅")

    # ----------------------------
    # Risk Prediction (Instant)
    # ----------------------------
    risk = 0
    if st.session_state.model_trained:
        risk = st.session_state.model.predict([[amount]])[0]

    # ----------------------------
    # High Risk → Block
    # ----------------------------
    if risk == 1:
        st.error("⚠️ High Risk Transaction Detected!")
        st.warning("QR Generation Blocked for Security.")
        st.stop()

    # ----------------------------
    # Save to Database
    # ----------------------------
    try:
        insert_transaction(username, amount)
        st.success("Transaction Saved in Database ✅")
    except Exception as e:
        st.error(f"Database Error: {e}")
        st.stop()

    # ----------------------------
    # Generate UPI Link
    # ----------------------------
    if payment_type == "Fixed Amount (Auto Filled)":
        upi_link = (
            f"upi://pay?"
            f"pa={upi_id}&"
            f"pn={name}&"
            f"am={amount:.2f}&"
            f"cu=INR&"
            f"tn={note}"
        )
    else:
        upi_link = (
            f"upi://pay?"
            f"pa={upi_id}&"
            f"pn={name}&"
            f"cu=INR&"
            f"tn={note}"
        )

    # ----------------------------
    # Generate QR Code
    # ----------------------------
    qr = qrcode.make(upi_link)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    st.image(buffer.getvalue(), caption="Scan with Any UPI App")
    st.success("QR Generated Successfully 🚀")