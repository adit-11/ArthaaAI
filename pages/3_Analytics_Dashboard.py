import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Smart AI Transaction Analytics")

# ----------------------------
# Check Data
# ----------------------------

if "transactions" not in st.session_state or len(st.session_state.transactions) == 0:
    st.warning("No transactions available yet.")
    st.stop()

transactions = st.session_state.transactions
amounts = [t["amount"] for t in transactions]

# Risk calculation (same logic as model)
risks = [1 if amt > 5000 else 0 for amt in amounts]

total_transactions = len(amounts)
total_revenue = sum(amounts)
high_risk = sum(risks)
low_risk = total_transactions - high_risk
avg_transaction = np.mean(amounts)
max_transaction = np.max(amounts)

# ----------------------------
# Metrics Section
# ----------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Revenue (₹)", f"{total_revenue:.2f}")
col3.metric("High Risk Transactions", high_risk)

st.divider()

col4, col5 = st.columns(2)

col4.metric("Average Transaction (₹)", f"{avg_transaction:.2f}")
col5.metric("Largest Transaction (₹)", f"{max_transaction:.2f}")

st.divider()

# ----------------------------
# Transaction Trend Line Chart
# ----------------------------

st.subheader("📈 Transaction Trend Over Time")

plt.figure()
plt.plot(amounts, marker='o')
plt.xlabel("Transaction Index")
plt.ylabel("Amount (₹)")
plt.title("Transaction Growth Trend")
st.pyplot(plt)

# ----------------------------
# Risk Distribution Pie Chart
# ----------------------------

st.subheader("🛑 Risk Distribution")

plt.figure()
plt.pie(
    [low_risk, high_risk],
    labels=["Low Risk", "High Risk"],
    autopct="%1.1f%%"
)
plt.title("Risk Breakdown")
st.pyplot(plt)

# ----------------------------
# AI Insight Section
# ----------------------------

st.subheader("🤖 AI Insights")

if high_risk > 0:
    st.error("⚠️ High value transactions detected. Monitor for potential fraud.")
else:
    st.success("✅ All transactions appear within safe limits.")

if avg_transaction > 4000:
    st.warning("💡 Average transaction value is relatively high.")

st.info("AI risk threshold currently set at ₹5000.")