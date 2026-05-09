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

.main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #ffffff !important;
    direction: rtl;
}
[data-testid="stSidebarNav"] { direction: rtl; }
.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Logo ──────────────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns([1.5, 1, 1.5])
with col_b:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<div style='text-align:center;font-size:80px;'>🤾</div>", unsafe_allow_html=True)

# ── Titles ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-top:16px; margin-bottom:48px;'>
    <div style='font-size:20px; font-weight:700; color:#64748b; margin-bottom:6px;'>
        הפועל ראשון לציון
    </div>
    <div style='font-size:40px; font-weight:900; color:#0f172a; line-height:1.2;'>
        מערכת חכמה לשיבוץ אימונים
    </div>
</div>
""", unsafe_allow_html=True)

# ── Buttons – כולם דרך HTML ───────────────────────────────────────────────────
BTN_STYLE = """
    display: block;
    width: 100%;
    padding: 28px 20px;
    border-radius: 16px;
    font-family: 'Heebo', sans-serif;
    font-size: 26px;
    font-weight: 700;
    text-align: center;
    text-decoration: none;
    margin-bottom: 16px;
    cursor: pointer;
    border: none;
    transition: opacity 0.15s;
"""

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    # כפתור 1 – לבן
    if st.button("⚙️  ניהול נתונים", use_container_width=True):
        st.switch_page("pages/1_Manage_Data.py")

    # כפתור 2 – אדום
    if st.button("📅  יצירת לוח אימונים", use_container_width=True):
        st.switch_page("pages/2_Optimization.py")

    # כפתור 3 – כהה
    if st.button("📋  לוח האימונים השבועי", use_container_width=True):
        st.switch_page("pages/3_Schedule.py")

st.markdown("""
<style>
/* כל הכפתורים – בסיס אחיד */
div[data-testid="stVerticalBlock"] .stButton > button {
    width: 100% !important;
    height: 90px !important;
    border-radius: 16px !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    border: 2px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #0f172a !important;
}

/* כפתור ראשון – אדום בהיר */
div[data-testid="stVerticalBlock"] .stButton:nth-child(1) > button {
    background: #ff6b6b !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 32px !important;
}

/* כפתור שני – אדום בינוני */
div[data-testid="stVerticalBlock"] .stButton:nth-child(2) > button {
    background: #d90429 !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 32px !important;
}

/* כפתור שלישי – אדום כהה */
div[data-testid="stVerticalBlock"] .stButton:nth-child(3) > button {
    background: #7f0014 !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 32px !important;
}
</style>
""", unsafe_allow_html=True)
