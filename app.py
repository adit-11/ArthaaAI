import streamlit as st
from sklearn.linear_model import LogisticRegression
from database import (
    init_db,
    register_user_db,
    authenticate_user_db
)

# 🔥 MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Artha AI", layout="wide")

# -------- Background --------
from styles.login_bg import load_login_background

# ---------------- DATABASE INIT ----------------
init_db()   # ✅ This now creates both users & transactions tables

# ---------------- SESSION INIT ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "last_risk" not in st.session_state:
    st.session_state.last_risk = None

if "page" not in st.session_state:
    st.session_state.page = "login"

# ================= LOGIN PAGE =================
if st.session_state.page == "login":

    st.markdown(load_login_background(), unsafe_allow_html=True)

    st.markdown("""
    <style>
    .brand-box {
        width: 50%;
        margin: 60px auto 25px auto;
        padding: 22px;
        background: #0f1419;
        border-radius: 16px;
        text-align: center;
    }
    .brand-title {
        font-size: 36px;
        font-weight: 600;
        letter-spacing: 1px;
        color: #e6f1f2;
        font-family: 'Segoe UI', sans-serif;
    }
    .brand-title span {
        color: #00c2b8;
        font-weight: 700;
    }
    </style>

    <div class="brand-box">
        <div class="brand-title">
            Artha <span>AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            "<h3 style='text-align:center;'>Fintech Risk Intelligence Platform</h3>",
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # ---------- LOGIN ----------
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login"):
                if authenticate_user_db(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username.lower().strip()  # ✅ lowercase fix
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        # ---------- SIGN UP ----------
        with tab2:
            new_user = st.text_input("New Username", key="signup_user")
            new_pass = st.text_input("New Password", type="password", key="signup_pass")

            if st.button("Register"):
                if register_user_db(new_user, new_pass):
                    st.success("User registered successfully. Please login.")
                else:
                    st.error("Username already exists.")

# ================= DASHBOARD =================
elif st.session_state.page == "dashboard":

    st.title("🚀 Artha AI - Fintech Risk & Payment Intelligence Platform")

    st.sidebar.success(f"Logged in as {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()   # ✅ clean logout
        st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("User", st.session_state.username)
    col2.metric("Authentication", "Active")
    col3.metric(
        "Last Risk Score",
        st.session_state.last_risk
        if st.session_state.last_risk is not None
        else "N/A"
    )

    st.divider()

    st.info("Use the sidebar to navigate between modules.")