import streamlit as st
import os

st.set_page_config(
    page_title="הפועל ראשון לציון – מערכת חכמה",
    page_icon="🤾",
    layout="centered",
)

st.markdown("""
<style>
.main, .stApp { direction: rtl; text-align: right; background: #ffffff; }
[data-testid="stSidebarNav"] { direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }

.block-container {
    padding-top: 3rem !important;
    max-width: 560px !important;
}

.home-title-sub {
    font-size: 18px;
    font-weight: 400;
    letter-spacing: 2px;
    color: #64748b;
    text-align: center;
    margin-bottom: 6px;
}
.home-title-main {
    font-size: 42px;
    font-weight: 900;
    color: #0f172a;
    text-align: center;
    margin-bottom: 56px;
    line-height: 1.2;
}

/* ── All buttons base style ── */
.stButton > button {
    width: 100% !important;
    border-radius: 16px !important;
    height: 80px !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07) !important;
    transition: all 0.15s !important;
    margin-bottom: 8px !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    border-color: #d90429 !important;
    color: #d90429 !important;
    box-shadow: 0 2px 12px rgba(217,4,41,0.12) !important;
}

/* ── Red button – יצירת לוח ── */
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button {
    background: #d90429 !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(217,4,41,0.35) !important;
    font-size: 22px !important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button:hover {
    background: #b80222 !important;
    color: #ffffff !important;
}

/* ── Dark button – לוח השבועי ── */
div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button {
    background: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.18) !important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button:hover {
    background: #1e293b !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo ──────────────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns([2, 1, 2])
with col_b:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center; font-size:80px; margin-bottom:8px;'>🤾</div>",
            unsafe_allow_html=True,
        )

# ── Titles ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='home-title-sub'>הפועל ראשון לציון</div>"
    "<div class='home-title-main'>מערכת חכמה לשיבוץ אימונים</div>",
    unsafe_allow_html=True,
)

# ── Buttons ───────────────────────────────────────────────────────────────────
if st.button("⚙️ ניהול נתונים"):
    st.switch_page("pages/1_Manage_Data.py")

if st.button("📅 יצירת לוח אימונים"):
    st.switch_page("pages/2_Optimization.py")

if st.button("📋 לוח האימונים השבועי"):
    st.switch_page("pages/3_Schedule.py")