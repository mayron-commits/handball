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
        st.markdown("<div style='text-align:center;font-size:80px;'>🤾</div>",
                    unsafe_allow_html=True)

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

# ── Buttons ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    if st.button("⚙️  ניהול נתונים", use_container_width=True, key="btn1"):
        st.switch_page("pages/1_Manage_Data.py")

    if st.button("📅  יצירת לוח אימונים", use_container_width=True, key="btn2"):
        st.switch_page("pages/2_Optimization.py")

    if st.button("📋  לוח האימונים השבועי", use_container_width=True, key="btn3"):
        st.switch_page("pages/3_Schedule.py")

# ── Styling by key ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* בסיס לכל הכפתורים */
button[kind="secondary"] {
    width: 100% !important;
    height: 90px !important;
    border-radius: 16px !important;
    font-size: 30px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    border: none !important;
    color: #ffffff !important;
}

/* כפתור 1 – אדום בהיר */
[data-testid="stButton-btn1"] button {
    background: #ff6b6b !important;
}

/* כפתור 2 – אדום בינוני */
[data-testid="stButton-btn2"] button {
    background: #d90429 !important;
}

/* כפתור 3 – אדום כהה */
[data-testid="stButton-btn3"] button {
    background: #7f0014 !important;
}
</style>
""", unsafe_allow_html=True)
