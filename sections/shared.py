"""
sections/shared.py
עיצוב ופונקציות משותפות לכל תת-מסכי ניהול הנתונים
"""
import streamlit as st
import os

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');
* { font-family: 'Heebo', sans-serif !important; }
.main, .stApp { background: #ffffff; direction: rtl; }
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stHeader"] { background: #ffffff; }
.block-container { max-width: 960px !important; margin: auto !important; padding-top: 1.5rem !important; }

/* ── כפתורי ניווט ── */
.stButton > button {
    border-radius: 10px !important; font-size: 14px !important; font-weight: 600 !important;
    height: 40px !important; background: #ffffff !important; color: #0f172a !important;
    border: 1.5px solid #e2e8f0 !important; padding: 0 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; width: auto !important;
}
.stButton > button:hover { border-color: #d90429 !important; color: #d90429 !important; }

/* ── כפתור אדום ── */
.red-btn > div > button {
    background: #d90429 !important; color: #ffffff !important; border: none !important;
    border-radius: 10px !important; font-size: 15px !important; font-weight: 700 !important;
    height: 44px !important; box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important; width: 100% !important;
}
.red-btn > div > button:hover { background: #b80222 !important; }

/* ── כפתור ביטול ── */
.cancel-btn > div > button {
    background: #ffffff !important; color: #64748b !important;
    border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important;
    font-size: 15px !important; font-weight: 600 !important;
    height: 48px !important; width: 100% !important;
}

/* ── כפתור שמירה ── */
.save-btn > div > button {
    background: #d90429 !important; color: #ffffff !important; border: none !important;
    border-radius: 10px !important; font-size: 15px !important; font-weight: 700 !important;
    height: 48px !important; box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important; width: 100% !important;
}

/* ── כפתור סגול ── */
.purple-btn > div > button {
    background: #f3e8ff !important; color: #7c3aed !important;
    border: 1.5px solid #e9d5ff !important; border-radius: 10px !important;
    font-size: 13px !important; font-weight: 700 !important;
    height: 56px !important; width: 100% !important;
}
.purple-btn > div > button:hover { background: #ede9fe !important; }

/* ── כרטיסים ── */
.data-card {
    background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px;
    padding: 20px 24px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: box-shadow 0.15s;
}
.data-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }

/* ── תגיות ── */
.tag {
    display: inline-block; border-radius: 20px;
    padding: 2px 12px; font-size: 12px; font-weight: 700;
}
.tag-blue   { background: #dbeafe; color: #1d4ed8; }
.tag-green  { background: #dcfce7; color: #15803d; }
.tag-red    { background: #fee2e2; color: #b91c1c; }
.tag-purple { background: #f3e8ff; color: #7c3aed; }
.tag-gray   { background: #f1f5f9; color: #475569; }
.tag-yellow { background: #fef9c3; color: #a16207; }
.tag-orange { background: #ffedd5; color: #c2410c; }

/* ── כותרת עמוד ── */
.page-title-lg { font-size: 30px; font-weight: 900; color: #0f172a; }
.page-title-lg span { font-weight: 400; }
.page-sub { font-size: 14px; color: #94a3b8; margin-top: 2px; }
hr.div { border: none; border-top: 1px solid #e2e8f0; margin: 16px 0; }

/* ── תוויות טופס ── */
.form-lbl {
    font-size: 11px; font-weight: 700; color: #94a3b8;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px;
}

/* ── מספרים גדולים בכרטיס ── */
.stat-box {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 12px 16px; text-align: center;
}
.stat-number { font-size: 28px; font-weight: 900; }
.stat-label  { font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #94a3b8; text-transform: uppercase; margin-top: 2px; }
</style>
"""


def inject_css():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def top_nav(back_label=None, back_section="overview"):
    """header אחיד – כפתור בית מימין, לוגו משמאל, קו מפריד"""
    col_home, col_back, col_space, col_logo = st.columns([1.2, 2, 5, 0.8])

    with col_home:
        if st.button("🏠 בית", key=f"home_{back_section}_{id(back_label)}"):
            st.session_state["manage_section"] = "overview"
            st.switch_page("app.py")

    if back_label:
        with col_back:
            if st.button(f"← {back_label}", key=f"back_{back_section}_{id(back_label)}"):
                st.session_state["manage_section"] = back_section
                for k in ["edit_team_idx","show_add_team",
                          "edit_coach_idx","show_add_coach","avail_coach_idx"]:
                    st.session_state[k] = None if "idx" in k else False
                st.rerun()

    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
        else:
            st.markdown(
                "<div style='text-align:center;font-size:32px;'>🤾</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='div'>", unsafe_allow_html=True)


def page_header(title_light, title_bold, subtitle, btn_label, btn_key, show_add_key):
    """כותרת עמוד + כפתור הוספה אדום"""
    col_title, col_add = st.columns([7, 2])
    with col_title:
        st.markdown(
            f"<div class='page-title-lg'>{title_light} <span style='font-weight:900'>{title_bold}</span></div>"
            f"<div class='page-sub'>{subtitle}</div>",
            unsafe_allow_html=True
        )
    with col_add:
        st.markdown('<div class="red-btn" style="margin-top:8px;">', unsafe_allow_html=True)
        if st.button(f"＋ {btn_label}", use_container_width=True, key=btn_key):
            st.session_state[show_add_key] = not st.session_state.get(show_add_key, False)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
