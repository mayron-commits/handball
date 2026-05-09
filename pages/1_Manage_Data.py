"""
pages/1_Manage_Data.py
ניהול נתונים – עיצוב Figma מלא עם תת-מסכים
"""
import streamlit as st
import os

st.set_page_config(
    page_title="ניהול נתונים – הפועל ראשון לציון",
    page_icon="⚙️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');
* { font-family: 'Heebo', sans-serif !important; }
.main, .stApp { background: #ffffff; direction: rtl; }
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stHeader"] { background: #ffffff; }
.block-container { max-width: 900px !important; margin: auto !important; padding-top: 1.5rem !important; }

/* ── כפתורי ניווט ── */
.nav-btn > div > button {
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    height: 40px !important;
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 0 16px !important;
    width: auto !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
.nav-btn > div > button:hover { border-color: #d90429 !important; color: #d90429 !important; }

/* ── כפתור אדום ── */
.red-btn > div > button {
    background: #d90429 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    height: 44px !important;
    box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important;
}
.red-btn > div > button:hover { background: #b80222 !important; }

/* ── כרטיס עיגול ── */
.entity-circle {
    width: 130px; height: 130px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 52px; margin: 0 auto 14px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    cursor: pointer;
}
.entity-circle:hover { transform: scale(1.06); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.entity-name { font-size: 18px; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: 8px; }
.entity-badge { border-radius: 20px; padding: 4px 18px; font-size: 15px; font-weight: 700; text-align: center; display: inline-block; }

/* ── כרטיס אולם ── */
.hall-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: box-shadow 0.15s;
}
.hall-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.hall-icon { font-size: 28px; margin-left: 16px; color: #94a3b8; }
.hall-name { font-size: 18px; font-weight: 800; color: #0f172a; }
.hall-address { font-size: 13px; color: #64748b; margin-top: 3px; }
.hall-tag { font-size: 12px; font-weight: 600; padding: 3px 12px; border-radius: 20px; }
.tag-split { background: #f3e8ff; color: #7c3aed; }
.tag-single { background: #f1f5f9; color: #64748b; }
.action-icons { display: flex; gap: 12px; }
.action-icon { font-size: 18px; cursor: pointer; color: #cbd5e1; padding: 6px; border-radius: 8px; }
.action-icon:hover { color: #64748b; background: #f1f5f9; }

/* ── טופס הוספה ── */
.form-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.form-title { font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 24px; }
.form-label { font-size: 12px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; }

/* ── כפתורי טופס ── */
.cancel-btn > div > button {
    background: #ffffff !important; color: #64748b !important;
    border: 1.5px solid #e2e8f0 !important; border-radius: 10px !important;
    font-size: 15px !important; font-weight: 600 !important; height: 48px !important;
}
.submit-btn > div > button {
    background: #d90429 !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-size: 15px !important; font-weight: 700 !important; height: 48px !important;
    box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important;
}

/* ── כותרת עמוד ── */
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-title-lg { font-size: 32px; font-weight: 900; color: #0f172a; }
.page-title-lg span { font-weight: 400; }
.page-sub { font-size: 14px; color: #94a3b8; margin-top: 4px; }
hr.divider { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "manage_section": "overview",
    "show_add_hall": False,
    "halls": [
        {"name": "אשלים",   "address": "הצמרת 17, ראשון לציון",       "split": True},
        {"name": "רוזן",    "address": "מנחם בגין 13, ראשון לציון",    "split": True},
        {"name": "נחלת",    "address": "רחוב העצמאות 37, ראשון לציון", "split": True},
        {"name": "גן נחום", "address": "תמר אבן 9, ראשון לציון",       "split": False},
    ],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════
# מסך 1 – סקירה כללית
# ════════════════════════════════════════════════════════════════════
if st.session_state.manage_section == "overview":

    # ── ניווט עליון ──────────────────────────────────────────────────
    col_home, col_logo = st.columns([8, 1])
    with col_home:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("🏠 חזרה לבית", key="home_ov"):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=60)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:30px;font-weight:900;text-align:center;color:#0f172a;margin-bottom:6px;'>ניהול נתונים</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:15px;color:#94a3b8;text-align:center;margin-bottom:36px;'>בחר ישות לצפייה וניהול</div>", unsafe_allow_html=True)

    # ── שורה 1 ───────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    def circle_card(col, icon, name, count, bg, text_color, badge_bg, key):
        with col:
            st.markdown(f"""
                <div style='text-align:center;'>
                    <div class='entity-circle' style='background:{bg};'>{icon}</div>
                    <div class='entity-name'>{name}</div>
                    <div style='text-align:center;'>
                        <span class='entity-badge' style='background:{badge_bg};color:{text_color};'>{count}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button(f"נהל {name}", key=key, use_container_width=True):
                st.session_state.manage_section = key
                st.rerun()

    circle_card(c1, "🏢", "אולמות",  4,   "#f3e8ff", "#7c3aed", "#ede9fe", "halls_management")
    circle_card(c2, "👥", "קבוצות",  15,  "#dbeafe", "#1d4ed8", "#eff6ff", "teams_management")
    circle_card(c3, "👨‍🏫", "מאמנים", 12,  "#dcfce7", "#15803d", "#f0fdf4", "coaches_management")

    st.write("##")
    _, c4, c5, _ = st.columns([1, 2, 2, 1])
    circle_card(c4, "🏃", "שחקנים", 421, "#ffedd5", "#c2410c", "#fff7ed", "players_management")
    circle_card(c5, "💼", "מנהלים", 12,  "#fef9c3", "#a16207", "#fefce8", "managers_management")

    st.markdown("<div style='text-align:center;color:#cbd5e1;font-size:13px;margin-top:24px;'>לחץ על ישות כדי לנהל את הנתונים שלה</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 2 – ניהול אולמות
# ════════════════════════════════════════════════════════════════════
elif st.session_state.manage_section == "halls_management":

    # ── ניווט עליון ──────────────────────────────────────────────────
    col_home, col_back, col_space, col_logo = st.columns([1.2, 1.8, 5, 1])
    with col_home:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("🏠 בית", key="home_halls"):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_back:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("← ניהול נתונים", key="back_halls"):
            st.session_state.manage_section = "overview"
            st.session_state.show_add_hall = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=60)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── כותרת + כפתור הוסף ───────────────────────────────────────────
    col_title, col_add = st.columns([7, 2])
    with col_title:
        st.markdown("""
            <div class='page-title-lg'>ניהול <span>אולמות</span></div>
            <div class='page-sub'>הגדר מתקני אימון ויכולות פיצול מגרש</div>
        """, unsafe_allow_html=True)
    with col_add:
        st.markdown('<div class="red-btn" style="margin-top:8px;">', unsafe_allow_html=True)
        if st.button("＋ הוסף אולם חדש", use_container_width=True):
            st.session_state.show_add_hall = not st.session_state.show_add_hall
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # ── טופס הוספת אולם ──────────────────────────────────────────────
    if st.session_state.show_add_hall:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        st.markdown("<div class='form-title'>הוספת אולם חדש</div>", unsafe_allow_html=True)

        col_name, col_addr = st.columns(2)
        with col_name:
            st.markdown("<div class='form-label'>שם האולם</div>", unsafe_allow_html=True)
            new_name = st.text_input("שם האולם", placeholder="למשל: אשלים", label_visibility="collapsed")
        with col_addr:
            st.markdown("<div class='form-label'>כתובת</div>", unsafe_allow_html=True)
            new_addr = st.text_input("כתובת", placeholder="למשל: הצמרת 17, ראשון לציון", label_visibility="collapsed")

        st.write("")
        new_split = st.checkbox("ניתן לפיצול מגרש – אפשר לקיים שני אימונים במקביל")

        st.write("")
        col_cancel, col_submit = st.columns(2)
        with col_cancel:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("ביטול", use_container_width=True):
                st.session_state.show_add_hall = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_submit:
            st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
            if st.button("הוסף אולם", use_container_width=True):
                if new_name.strip():
                    st.session_state.halls.append({
                        "name": new_name.strip(),
                        "address": new_addr.strip() or "כתובת לא הוזנה",
                        "split": new_split,
                    })
                    st.session_state.show_add_hall = False
                    st.success(f"✅ האולם '{new_name}' נוסף בהצלחה!")
                    st.rerun()
                else:
                    st.error("נא להזין שם אולם")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

    # ── רשימת אולמות ─────────────────────────────────────────────────
    for i, hall in enumerate(st.session_state.halls):
        tag_class = "tag-split" if hall["split"] else "tag-single"
        tag_text  = "ניתן לפיצול" if hall["split"] else "מגרש בודד"

        col_card, col_edit, col_del = st.columns([10, 0.6, 0.6])
        with col_card:
            st.markdown(f"""
            <div class='hall-card'>
                <div style='display:flex; align-items:center; gap:16px;'>
                    <div style='font-size:32px; color:#94a3b8;'>🏢</div>
                    <div>
                        <div style='display:flex; align-items:center; gap:10px;'>
                            <span class='hall-name'>{hall['name']}</span>
                            <span class='hall-tag {tag_class}'>{tag_text}</span>
                        </div>
                        <div class='hall-address'>📍 {hall['address']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_edit:
            if st.button("✏️", key=f"edit_{i}", help="ערוך"):
                st.toast(f"עריכת {hall['name']} – יושם בשלב ב׳")
        with col_del:
            if st.button("🗑️", key=f"del_{i}", help="מחק"):
                st.session_state.halls.pop(i)
                st.rerun()

# ════════════════════════════════════════════════════════════════════
# מסכים נוספים – קבוצות / מאמנים / שחקנים / מנהלים
# ════════════════════════════════════════════════════════════════════
else:
    section = st.session_state.manage_section

    titles = {
        "teams_management":   ("קבוצות",  "רשימת הקבוצות הפעילות במועדון"),
        "coaches_management": ("מאמנים",  "פרטי המאמנים וזמינותם"),
        "players_management": ("שחקנים",  "421 שחקנים ושחקניות רשומים"),
        "managers_management":("מנהלים",  "מנהלי קבוצות ואחראים"),
    }
    title, sub = titles.get(section, ("ניהול", ""))

    # ניווט
    col_home, col_back, col_space, col_logo = st.columns([1.2, 1.8, 5, 1])
    with col_home:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("🏠 בית", key="home_sec"):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_back:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("← ניהול נתונים", key="back_sec"):
            st.session_state.manage_section = "overview"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=60)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-title-lg'>ניהול <span>{title}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>{sub}</div>", unsafe_allow_html=True)
    st.write("")

    # ── קבוצות ───────────────────────────────────────────────────────
    if section == "teams_management":
        teams = [
            {"name": "בוגרים גברים א׳", "league": "ליגת העל",        "trainings": 4, "color": "#d90429"},
            {"name": "בוגרות נשים א׳",  "league": "ליגת העל נשים",   "trainings": 3, "color": "#d90429"},
            {"name": "נערים א׳ צפון",   "league": "ליגה ארצית",      "trainings": 3, "color": "#1d4ed8"},
            {"name": "נערות א׳",        "league": "ליגה ארצית נשים", "trainings": 3, "color": "#1d4ed8"},
            {"name": "ילדים ז׳ 1",      "league": "ליגה מחוזית",     "trainings": 2, "color": "#15803d"},
        ]
        for t in teams:
            st.markdown(f"""
            <div class='hall-card' style='border-right:5px solid {t["color"]};'>
                <div>
                    <div class='hall-name'>{t['name']}</div>
                    <div class='hall-address'>{t['league']}</div>
                </div>
                <span class='hall-tag tag-split' style='background:#f1f5f9;color:#475569;'>
                    {t['trainings']} אימונים/שבוע
                </span>
            </div>
            """, unsafe_allow_html=True)
        if st.button("＋ הוסף קבוצה חדשה", use_container_width=True):
            st.info("יושם בשלב ב׳ עם חיבור לבסיס הנתונים")

    # ── מאמנים ───────────────────────────────────────────────────────
    elif section == "coaches_management":
        coaches = [
            {"name": "יוסי כהן",  "role": "מאמן ראשי – בוגרים",  "license": "מאמן בכיר"},
            {"name": "מיכל לוי",  "role": "מאמנת ראשית – נשים",   "license": "מאמנת"},
            {"name": "דני אברהם", "role": "מאמן נוער",             "license": "מאמן"},
            {"name": "שרה גולן",  "role": "מאמנת נוער",            "license": "מאמנת"},
            {"name": "רון שפירא", "role": "מאמן שוערים",           "license": "מדריך"},
        ]
        for c in coaches:
            st.markdown(f"""
            <div class='hall-card' style='border-right:5px solid #15803d;'>
                <div>
                    <div class='hall-name'>{c['name']}</div>
                    <div class='hall-address'>{c['role']}</div>
                </div>
                <span class='hall-tag' style='background:#dcfce7;color:#15803d;'>{c['license']}</span>
            </div>
            """, unsafe_allow_html=True)
        if st.button("＋ הוסף מאמן חדש", use_container_width=True):
            st.info("יושם בשלב ב׳ עם חיבור לבסיס הנתונים")

    # ── שחקנים ───────────────────────────────────────────────────────
    elif section == "players_management":
        col_s, col_f = st.columns(2)
        with col_s:
            st.text_input("🔍 חיפוש לפי שם")
        with col_f:
            st.selectbox("סנן לפי קבוצה", ["הכל","בוגרים גברים","בוגרות נשים","נערים א׳","נערות א׳","ילדים ז׳"])
        st.info("רשימת השחקנים המלאה תוצג לאחר חיבור מסד הנתונים בשלב ב׳")
        if st.button("＋ הוסף שחקן חדש", use_container_width=True):
            st.info("יושם בשלב ב׳")

    # ── מנהלים ───────────────────────────────────────────────────────
    elif section == "managers_management":
        managers = [
            {"name": "אבי פרידמן",  "team": "בוגרים גברים א׳"},
            {"name": "רות שמיר",    "team": "בוגרות נשים א׳"},
            {"name": "נועם כץ",     "team": "נערים א׳ צפון"},
            {"name": "ליאת בן דוד", "team": "נערות א׳"},
        ]
        for m in managers:
            st.markdown(f"""
            <div class='hall-card' style='border-right:5px solid #a16207;'>
                <div>
                    <div class='hall-name'>{m['name']}</div>
                    <div class='hall-address'>אחראי: {m['team']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("＋ הוסף מנהל חדש", use_container_width=True):
            st.info("יושם בשלב ב׳ עם חיבור לבסיס הנתונים")
