import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Live BSE / NSE Market Dashboard")

# -----------------------------
# Ticker Selection
# -----------------------------
tickers = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "RELIANCE": "RELIANCE.NS",
}

option = st.selectbox("Select Market / Stock", list(tickers.keys()))
symbol = tickers[option]

# -----------------------------
# Fetch Market Data
# -----------------------------
try:
    data = yf.download(symbol, period="1d", interval="5m", progress=False)
except Exception:
    st.error("Error fetching market data.")
    st.stop()

if data.empty:
    st.error("No market data available.")
    st.stop()

# Flatten multi-index columns if present
if isinstance(data.columns, type(data.columns)) and hasattr(data.columns, "levels"):
    data.columns = data.columns.get_level_values(0)

# Clean data
data = data.dropna()

# -----------------------------
# Candlestick Chart
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"].astype(float),
    high=data["High"].astype(float),
    low=data["Low"].astype(float),
    close=data["Close"].astype(float),
))

fig.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_rangeslider_visible=False,
    title=f"{option} Intraday Price Action"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Safe Close Series Extraction
# -----------------------------
close_series = data["Close"]

# Force to proper 1D Series
close_series = close_series.squeeze()
close_series = close_series.astype(float).dropna()

if len(close_series) < 2:
    st.warning("Not enough data to calculate metrics.")
    st.stop()

# -----------------------------
# Metrics Calculation
# -----------------------------
latest = float(close_series.iloc[-1])
previous = float(close_series.iloc[-2])

change = latest - previous

if previous != 0:
    change_pct = (change / previous) * 100
else:
    change_pct = 0

col1, col2, col3 = st.columns(3)
col1.metric("Latest Price", f"₹{latest:.2f}")
col2.metric("Change", f"{change:+.2f}")
col3.metric("Change %", f"{change_pct:+.2f}%")

# -----------------------------
# Volatility (Market Risk Index)
# -----------------------------
volatility_value = close_series.pct_change().std()

# Force scalar float
volatility = float(volatility_value) * 100

st.markdown("---")
st.subheader("📈 Market Risk Index")

if volatility > 1.2:
    st.error(f"High Market Volatility: {volatility:.2f}%")
elif volatility > 0.6:
    st.warning(f"Moderate Market Volatility: {volatility:.2f}%")
else:
    st.success(f"Low Market Volatility: {volatility:.2f}%")