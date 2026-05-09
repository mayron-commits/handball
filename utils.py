"""
utils.py – shared helpers for all pages.
Import with:  from utils import apply_global_css, show_logo_header, circular_card
"""
import os
import streamlit as st


def apply_global_css():
    """Inject the shared RTL + component styles."""
    st.markdown(
        """
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

        /* red action button (3rd child inside a vertical block) */
        div[data-testid="stVerticalBlock"]
            > div:nth-child(3) .stButton>button {
            background-color: #d90429;
            color: white;
            border: none;
        }

        [data-testid="stSidebarNav"] { direction: rtl; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_logo_header(title: str, subtitle: str = ""):
    """Render a page header with title on the right and logo on the left."""
    col_text, col_logo = st.columns([5, 1])
    with col_text:
        st.markdown(f"<h1 style='margin:0;'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(
                f"<p style='color:gray; margin:0;'>{subtitle}</p>",
                unsafe_allow_html=True,
            )
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=100)
        else:
            st.markdown(
                "<div style='text-align:center; font-size:48px;'>🤾</div>",
                unsafe_allow_html=True,
            )


def circular_card(label: str, count, icon: str, color: str, page_key: str):
    """
    Render a circular info card with a navigation button beneath it.
    page_key  – used as the button key AND as the target page name under pages/.
    """
    card_html = f"""
    <div style="display:flex; flex-direction:column; align-items:center;
                justify-content:center; margin-bottom:10px;">
        <div style="width:110px; height:110px; border-radius:50%;
                    background-color:white; border:3px solid {color};
                    display:flex; align-items:center; justify-content:center;
                    font-size:40px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            {icon}
        </div>
        <div style="margin-top:10px; font-weight:bold; font-size:18px;
                    color:#1e293b;">{label}</div>
        <div style="background-color:{color}22; color:{color};
                    padding:2px 15px; border-radius:15px; font-weight:bold;
                    margin-top:5px;">
            {count}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button(f"ניהול {label}", key=page_key):
        st.session_state["manage_section"] = page_key
        st.switch_page("pages/1_Manage_Data.py")
