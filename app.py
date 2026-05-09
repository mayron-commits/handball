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

# ── Streamlit buttons (hidden) for navigation ─────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    btn1 = st.button("ניהול נתונים", key="btn1", use_container_width=True)
    btn2 = st.button("יצירת לוח אימונים", key="btn2", use_container_width=True)
    btn3 = st.button("לוח האימונים השבועי", key="btn3", use_container_width=True)

if btn1:
    st.switch_page("pages/1_Manage_Data.py")
if btn2:
    st.switch_page("pages/2_Optimization.py")
if btn3:
    st.switch_page("pages/3_Schedule.py")

# ── Style: hide real buttons, show beautiful HTML ones ───────────────────────
st.markdown("""
<style>
/* הסתר את כפתורי Streamlit */
[data-testid="stButton-btn1"],
[data-testid="stButton-btn2"],
[data-testid="stButton-btn3"] {
    position: absolute;
    opacity: 0;
    pointer-events: none;
}
</style>

<div style='max-width:600px; margin:0 auto; padding:0 16px;'>

<button onclick="document.querySelector('[data-testid=stButton-btn1] button').click()"
style="
    width:100%; height:90px; border-radius:16px; border:none;
    background:#ff6b6b; color:#ffffff;
    font-family:'Heebo',sans-serif; font-size:30px; font-weight:700;
    margin-bottom:14px; cursor:pointer; display:block;
    transition: filter 0.15s;
" onmouseover="this.style.filter='brightness(0.9)'"
   onmouseout="this.style.filter='brightness(1)'">
⚙️ &nbsp; ניהול נתונים
</button>

<button onclick="document.querySelector('[data-testid=stButton-btn2] button').click()"
style="
    width:100%; height:90px; border-radius:16px; border:none;
    background:#d90429; color:#ffffff;
    font-family:'Heebo',sans-serif; font-size:30px; font-weight:700;
    margin-bottom:14px; cursor:pointer; display:block;
    transition: filter 0.15s;
" onmouseover="this.style.filter='brightness(0.9)'"
   onmouseout="this.style.filter='brightness(1)'">
📅 &nbsp; יצירת לוח אימונים
</button>

<button onclick="document.querySelector('[data-testid=stButton-btn3] button').click()"
style="
    width:100%; height:90px; border-radius:16px; border:none;
    background:#7f0014; color:#ffffff;
    font-family:'Heebo',sans-serif; font-size:30px; font-weight:700;
    margin-bottom:14px; cursor:pointer; display:block;
    transition: filter 0.15s;
" onmouseover="this.style.filter='brightness(0.9)'"
   onmouseout="this.style.filter='brightness(1)'">
📋 &nbsp; לוח האימונים השבועי
</button>

</div>
""", unsafe_allow_html=True)
