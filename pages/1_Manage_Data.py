"""
pages/1_Manage_Data.py
מסך ניהול נתונים – נתב לתת-מסכים
"""
import streamlit as st
import os
from sections.shared import inject_css, top_nav
from sections import teams as teams_section
from sections import coaches as coaches_section
from sections import players as players_section
from sections import managers as managers_section
from sections.db_data import HALLS_DB, TEAMS_DB, COACHES_DB, COACH_NAMES, HALL_NAMES, TEAM_NAMES

st.set_page_config(
    page_title="ניהול נתונים – הפועל ראשון לציון",
    page_icon="⚙️",
    layout="wide",
)
inject_css()

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "manage_section": "overview",
    "show_add_hall": False,
    "edit_coach_idx": None,
    "avail_coach_idx": None,
    "show_add_coach": False,
    "show_add_team": False,
    "edit_team_idx": None,
    "halls": [
        {"name": "אשלים",   "address": "הצמרת 17, ראשון לציון",       "split": True},
        {"name": "רוזן",    "address": "מנחם בגין 13, ראשון לציון",    "split": True},
        {"name": "נחלת",    "address": "רחוב העצמאות 37, ראשון לציון", "split": True},
        {"name": "גן נחום", "address": "תמר אבן 9, ראשון לציון",       "split": False},
    ],
    "coaches": [
        {"name": "יוסי כהן",  "role": "מאמן ראשי",   "email": "yossi@hapoel.com",  "phone": "050-111-2233"},
        {"name": "מיכל לוי",  "role": "מאמנת ראשית", "email": "michal@hapoel.com",  "phone": "050-222-3344"},
        {"name": "דני אברהם", "role": "עוזר מאמן",   "email": "danny@hapoel.com",   "phone": "050-333-4455"},
        {"name": "שרה גולן",  "role": "מאמנת נוער",  "email": "sara@hapoel.com",    "phone": "050-444-5566"},
        {"name": "רון שפירא", "role": "מאמן שוערים", "email": "ron@hapoel.com",     "phone": "050-555-6677"},
    ],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

section = st.session_state.get("manage_section", "overview")

# ════════════════════════════════════════════════════════════════════
# נתב – מסך לפי section
# ════════════════════════════════════════════════════════════════════

# ── קבוצות ───────────────────────────────────────────────────────────
if section == "teams_management":
    teams_section.render(st.session_state.coaches)

# ── מאמנים ───────────────────────────────────────────────────────────
elif section == "coaches_management":
    coaches_section.render()

# ── אולמות ───────────────────────────────────────────────────────────
elif section == "halls_management":
    # יושם בקובץ sections/halls.py בשלב הבא
    top_nav("ניהול נתונים", "overview")

    col_title, col_add = st.columns([7, 2])
    with col_title:
        st.markdown("<div class='page-title-lg'>ניהול <span style='font-weight:900'>אולמות</span></div><div class='page-sub'>הגדר מתקני אימון ויכולות פיצול מגרש</div>", unsafe_allow_html=True)
    with col_add:
        st.markdown('<div class="red-btn" style="margin-top:8px;">', unsafe_allow_html=True)
        if st.button("＋ הוסף אולם חדש", use_container_width=True, key="add_hall_btn"):
            st.session_state.show_add_hall = not st.session_state.show_add_hall
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    if st.session_state.show_add_hall:
        with st.container(border=True):
            st.markdown("<div style='font-size:20px;font-weight:800;margin-bottom:16px;'>הוספת אולם חדש</div>", unsafe_allow_html=True)
            cn, ca = st.columns(2)
            with cn:
                st.markdown("<div class='form-lbl'>שם האולם</div>", unsafe_allow_html=True)
                new_name = st.text_input("שם", placeholder="למשל: אשלים", label_visibility="collapsed")
            with ca:
                st.markdown("<div class='form-lbl'>כתובת</div>", unsafe_allow_html=True)
                new_addr = st.text_input("כתובת", placeholder="למשל: הצמרת 17", label_visibility="collapsed")
            new_split = st.checkbox("ניתן לפיצול מגרש")
            st.write("")
            cc, cs = st.columns(2)
            with cc:
                st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                if st.button("ביטול", use_container_width=True, key="cancel_hall"):
                    st.session_state.show_add_hall = False; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with cs:
                st.markdown('<div class="save-btn">', unsafe_allow_html=True)
                if st.button("הוסף אולם", use_container_width=True, key="save_hall"):
                    if new_name.strip():
                        st.session_state.halls.append({"name": new_name.strip(), "address": new_addr.strip() or "—", "split": new_split})
                        st.session_state.show_add_hall = False
                        st.success(f"✅ האולם '{new_name}' נוסף!")
                        st.rerun()
                    else:
                        st.error("נא להזין שם אולם")
                st.markdown('</div>', unsafe_allow_html=True)
        st.write("")

    for i, hall in enumerate(st.session_state.halls):
        tag_txt = "ניתן לפיצול" if hall["split"] else "מגרש בודד"
        tag_clr = "#7c3aed" if hall["split"] else "#64748b"
        tag_bg  = "#f3e8ff" if hall["split"] else "#f1f5f9"
        col_card, col_edit, col_del = st.columns([10, 0.6, 0.6])
        with col_card:
            st.markdown(f"""
            <div class='data-card' style='border-right:5px solid #7c3aed;'>
                <div style='display:flex;align-items:center;gap:16px;'>
                    <div style='font-size:32px;'>🏢</div>
                    <div>
                        <div style='display:flex;align-items:center;gap:10px;'>
                            <span style='font-size:18px;font-weight:800;color:#0f172a;'>{hall['name']}</span>
                            <span style='background:{tag_bg};color:{tag_clr};border-radius:20px;padding:2px 12px;font-size:12px;font-weight:700;'>{tag_txt}</span>
                        </div>
                        <div style='font-size:13px;color:#64748b;margin-top:3px;'>📍 {hall['address']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_edit:
            if st.button("✏️", key=f"edit_hall_{i}"):
                st.toast(f"עריכת {hall['name']} – יושם בשלב ב׳")
        with col_del:
            if st.button("🗑️", key=f"del_hall_{i}"):
                st.session_state.halls.pop(i); st.rerun()

# ── שחקנים ───────────────────────────────────────────────────────────
elif section == "players_management":
    players_section.render()

# ── מנהלים ───────────────────────────────────────────────────────────
elif section == "managers_management":
    managers_section.render()

# ════════════════════════════════════════════════════════════════════
# מסך סקירה כללית – ברירת מחדל
# ════════════════════════════════════════════════════════════════════
else:
    col_home, col_space, col_logo = st.columns([1.2, 7, 0.8])
    with col_home:
        if st.button("🏠 בית"):
            st.session_state["manage_section"] = "overview"
            st.switch_page("app.py")
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)

    st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:30px;font-weight:900;text-align:center;color:#0f172a;margin-bottom:6px;'>ניהול נתונים</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:15px;color:#94a3b8;text-align:center;margin-bottom:36px;'>בחר ישות לצפייה וניהול</div>", unsafe_allow_html=True)

    def circle_card(col, icon, name, count, bg, text_color, badge_bg, key):
        with col:
            st.markdown(f"""
                <div style='text-align:center;'>
                    <div style='width:130px;height:130px;border-radius:50%;background:{bg};
                                display:flex;align-items:center;justify-content:center;font-size:52px;
                                margin:0 auto 14px;'>
                        {icon}
                    </div>
                    <div style='font-size:18px;font-weight:800;color:#0f172a;text-align:center;margin-bottom:8px;'>{name}</div>
                    <div style='text-align:center;'>
                        <span style='background:{badge_bg};color:{text_color};border-radius:20px;
                                     padding:4px 18px;font-size:15px;font-weight:700;'>{count}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button(f"נהל {name}", key=key, use_container_width=True):
                st.session_state.manage_section = key
                st.rerun()

    c1, c2, c3 = st.columns(3)
    circle_card(c1, "🏢", "אולמות",  len(st.session_state.halls),   "#f3e8ff", "#7c3aed", "#ede9fe", "halls_management")
    circle_card(c2, "👥", "קבוצות",  len(st.session_state.get("teams", [])), "#dbeafe", "#1d4ed8", "#eff6ff", "teams_management")
    circle_card(c3, "👨‍🏫", "מאמנים", len(st.session_state.coaches), "#dcfce7", "#15803d", "#f0fdf4", "coaches_management")
    st.write("##")
    _, c4, c5, _ = st.columns([1, 2, 2, 1])
    circle_card(c4, "🏃", "שחקנים", 421, "#ffedd5", "#c2410c", "#fff7ed", "players_management")
    circle_card(c5, "💼", "מנהלים", 12,  "#fef9c3", "#a16207", "#fefce8", "managers_management")
    st.markdown("<div style='text-align:center;color:#cbd5e1;font-size:13px;margin-top:24px;'>לחץ על ישות כדי לנהל את הנתונים שלה</div>", unsafe_allow_html=True)
