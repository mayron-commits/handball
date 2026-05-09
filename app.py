import streamlit as st
import os

st.set_page_config(
    page_title="הפועל ראשון לציון - Smart Scheduler",
    page_icon="🤾",
    layout="wide",
)

st.markdown("""
    <style>
    .main, .stApp { direction: rtl; text-align: right; }

    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 5em;
        background-color: MistyRose;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        font-size: 18px !important;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { border-color: #d90429; color: #d90429; }

    [data-testid="stSidebarNav"] { direction: rtl; }
    </style>
""", unsafe_allow_html=True)


def show_logo_header(title, subtitle=""):
    col_text, col_logo = st.columns([5, 1])
    with col_text:
        st.markdown(f"<h1 style='margin:0;'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p style='color:gray; margin:0;'>{subtitle}</p>", unsafe_allow_html=True)
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=100)
        else:
            st.markdown(
                "<div style='text-align:center; font-size:48px;'>🤾</div>",
                unsafe_allow_html=True,
            )


# ── Home screen ──────────────────────────────────────────────────────────────
st.write("##")

col_a, col_b, col_c = st.columns([2, 1, 2])
with col_b:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center; font-size:80px;'>🤾</div>",
            unsafe_allow_html=True,
        )

st.markdown(
    "<h3 style='text-align:center; color:gray;'>הפועל ראשון לציון</h3>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align:center; color:#1e293b; margin-bottom:50px;'>מערכת חכמה לשיבוץ אימונים</h1>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("⚙️ ניהול נתונים"):
        st.switch_page("pages/1_Manage_Data.py")
    if st.button("📅 יצירת לוח אימונים"):
        st.switch_page("pages/2_Optimization.py")
    if st.button("📋 לוח האימונים השבועי"):
        st.switch_page("pages/3_Schedule.py")
