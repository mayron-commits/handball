import streamlit as st
import os

st.set_page_config(
    page_title="הפועל ראשון לציון – מערכת חכמה",
    page_icon="🤾",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');

* { font-family: 'Heebo', sans-serif !important; }

.main, .stApp {
    direction: rtl;
    text-align: right;
    background: #ffffff;
}
[data-testid="stSidebarNav"] { direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }

.block-container {
    padding-top: 2rem !important;
    max-width: 900px !important;
    margin: auto !important;
}

.home-title-sub {
    font-family: 'Heebo', sans-serif !important;
    font-size: 20px;
    font-weight: 700;
    color: #64748b;
    text-align: center;
    margin-bottom: 4px;
    margin-top: 16px;
}
.home-title-main {
    font-family: 'Heebo', sans-serif !important;
    font-size: 40px;
    font-weight: 900;
    color: #0f172a;
    text-align: center;
    margin-bottom: 48px;
    line-height: 1.2;
}

.stButton {
    display: flex;
    justify-content: center;
}
.stButton > button {
    width: 200% !important;
    border-radius: 18px !important;
    height: 120px !important;
    font-family: 'Heebo', sans-serif !important;
    font-size: 34px !important;
    font-weight: 700 !important;
    border: 2px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07) !important;
    transition: all 0.15s ease !important;
    margin-bottom: 14px !important;
}
.stButton > button:hover {
    border-color: #d90429 !important;
    color: #d90429 !important;
    box-shadow: 0 4px 16px rgba(217,4,41,0.15) !important;
    transform: translateY(-1px) !important;
}

/* כפתור אדום – יצירת לוח */
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button {
    background: #d90429 !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 6px 24px rgba(217,4,41,0.4) !important;
    font-size: 30px !important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button:hover {
    background: #b80222 !important;
    color: #ffffff !important;
}

/* כפתור כהה – לוח השבועי */
div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button {
    background: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button:hover {
    background: #1e293b !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo ──────────────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns([1.5, 1, 1.5])
with col_b:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center; font-size:80px;'>🤾</div>",
            unsafe_allow_html=True,
        )

# ── Titles ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='home-title-sub'>הפועל ראשון לציון</div>"
    "<div class='home-title-main'>מערכת חכמה לשיבוץ אימונים</div>",
    unsafe_allow_html=True,
)

# ── Buttons ───────────────────────────────────────────────────────────────────
if st.button("⚙️  ניהול נתונים"):
    st.switch_page("pages/1_Manage_Data.py")

if st.button("📅  יצירת לוח אימונים"):
    st.switch_page("pages/2_Optimization.py")

if st.button("📋  לוח האימונים השבועי"):
    st.switch_page("pages/3_Schedule.py")
