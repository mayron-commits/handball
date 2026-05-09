import streamlit as st
import os

st.set_page_config(
    page_title="Hapoel Rishon LeZion – Smart Scheduler",
    page_icon="🤾",
    layout="centered",
)

st.markdown("""
<style>
/* ── Global ── */
.main, .stApp { direction: rtl; text-align: right; background: #ffffff; }
[data-testid="stSidebarNav"] { direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }

/* Hide default padding */
.block-container { padding-top: 3rem !important; max-width: 480px !important; }

/* ── Title block ── */
.home-title-sub {
    font-family: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif;
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 4px;
    color: #64748b;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.home-title-main {
    font-family: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #0f172a;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 48px;
    line-height: 1.1;
}

/* ── Buttons – reset ALL streamlit button styles ── */
.stButton > button {
    width: 100% !important;
    border-radius: 14px !important;
    height: 64px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border: 1.5px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    transition: all 0.15s !important;
    margin-bottom: 4px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0 20px !important;
}
.stButton > button:hover {
    border-color: #d90429 !important;
    color: #d90429 !important;
    box-shadow: 0 2px 8px rgba(217,4,41,0.12) !important;
}

/* ── Red "Create" button (second button) ── */
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button {
    background: #d90429 !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(217,4,41,0.3) !important;
}
div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button:hover {
    background: #b80222 !important;
    color: #ffffff !important;
}

/* ── Dark "Schedule" button (third button) ── */
div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button {
    background: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
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
            "<div style='text-align:center; font-size:72px; margin-bottom:16px;'>🤾</div>",
            unsafe_allow_html=True,
        )

# ── Titles ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='home-title-sub'>Hapoel Rishon LeZion</div>"
    "<div class='home-title-main'>Smart Scheduler</div>",
    unsafe_allow_html=True,
)

# ── Buttons ───────────────────────────────────────────────────────────────────
if st.button("MANAGE DATA  ⚙️"):
    st.switch_page("pages/1_Manage_Data.py")

if st.button("CREATE TRAINING SCHEDULE  📅"):
    st.switch_page("pages/2_Optimization.py")

if st.button("THIS WEEK'S TRAINING SCHEDULE  📋"):
    st.switch_page("pages/3_Schedule.py")