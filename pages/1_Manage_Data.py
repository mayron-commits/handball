"""
pages/1_Manage_Data.py
ניהול נתונים – עיצוב לפי Figma
"""
import streamlit as st
import os
from utils import apply_global_css

st.set_page_config(
    page_title="ניהול נתונים – הפועל ראשון לציון",
    page_icon="⚙️",
    layout="centered",
)

apply_global_css()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
* { font-family: 'Heebo', sans-serif !important; }

.main, .stApp { background: #ffffff; direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }
.block-container { max-width: 800px !important; margin: auto !important; padding-top: 2rem !important; }

/* ── כפתור חזרה ── */
.stButton > button {
    border-radius: 12px !important;
    font-family: 'Heebo', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    height: 44px !important;
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 0 18px !important;
    width: auto !important;
}
.stButton > button:hover {
    border-color: #d90429 !important;
    color: #d90429 !important;
}

/* ── כרטיס עיגול ── */
.entity-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 16px 8px;
}
.entity-circle {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
    margin-bottom: 14px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.entity-circle:hover {
    transform: scale(1.06);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.entity-name {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
.entity-badge {
    border-radius: 20px;
    padding: 4px 18px;
    font-size: 15px;
    font-weight: 700;
    text-align: center;
}

/* ── כותרת עמוד ── */
.page-title {
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
    text-align: center;
    margin-bottom: 6px;
}
.page-sub {
    font-size: 15px;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 40px;
}
.page-hint {
    font-size: 13px;
    color: #cbd5e1;
    text-align: center;
    margin-top: 32px;
}
</style>
""", unsafe_allow_html=True)

# ── כפתור חזרה + לוגו ────────────────────────────────────────────────────────
col_back, col_space, col_logo = st.columns([2, 4, 1])
with col_back:
    if st.button("🏠 חזרה לבית"):
        st.switch_page("app.py")
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=70)

# ── כותרת ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class='page-title'>ניהול נתונים</div>
    <div class='page-sub'>בחר ישות לצפייה וניהול</div>
""", unsafe_allow_html=True)

# ── פונקציית כרטיס ───────────────────────────────────────────────────────────
def entity_card(icon, name, count, bg_color, text_color, badge_bg, key):
    st.markdown(f"""
        <div class='entity-card'>
            <div class='entity-circle' style='background:{bg_color};'>
                {icon}
            </div>
            <div class='entity-name'>{name}</div>
            <div class='entity-badge' style='background:{badge_bg}; color:{text_color};'>
                {count}
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button(f"נהל {name}", key=key, use_container_width=True):
        st.session_state["manage_section"] = key
        st.rerun()

# ── שורה 1: אולמות, קבוצות, מאמנים ──────────────────────────────────────────
st.write("")
c1, c2, c3 = st.columns(3)

with c1:
    entity_card("🏢", "אולמות", 4,
                "#f3e8ff", "#7c3aed", "#ede9fe", "halls_management")

with c2:
    entity_card("👥", "קבוצות", 15,
                "#dbeafe", "#1d4ed8", "#eff6ff", "teams_management")

with c3:
    entity_card("👨‍🏫", "מאמנים", 12,
                "#dcfce7", "#15803d", "#f0fdf4", "coaches_management")

# ── שורה 2: שחקנים, מנהלים (ממורכזים) ───────────────────────────────────────
st.write("")
_, c4, c5, _ = st.columns([1, 2, 2, 1])

with c4:
    entity_card("🏃", "שחקנים", 421,
                "#ffedd5", "#c2410c", "#fff7ed", "players_management")

with c5:
    entity_card("💼", "מנהלים", 12,
                "#fef9c3", "#a16207", "#fefce8", "managers_management")

st.markdown("<div class='page-hint'>לחץ על ישות כדי לנהל את הנתונים שלה</div>",
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסכי ניהול פנימיים
# ════════════════════════════════════════════════════════════════════
section = st.session_state.get("manage_section", None)

if section:
    st.write("---")

    def back_btn():
        if st.button("⬅️ חזרה לניהול נתונים", key="back_inner"):
            st.session_state["manage_section"] = None
            st.rerun()

    # ── אולמות ───────────────────────────────────────────────────────
    if section == "halls_management":
        back_btn()
        st.markdown("<div class='page-title' style='font-size:28px;'>ניהול אולמות</div>", unsafe_allow_html=True)
        st.write("")

        halls = [
            {"name": "אשלים",   "address": "הצמרת 17, ראשון לציון",        "split": True},
            {"name": "רוזן",    "address": "מנחם בגין 13, ראשון לציון",     "split": True},
            {"name": "נחלת",    "address": "רחוב העצמאות 37, ראשון לציון",  "split": True},
            {"name": "גן נחום", "address": "תמר אבן 9, ראשון לציון",        "split": False},
        ]
        for h in halls:
            split_label = "ניתן לפיצול" if h["split"] else "מגרש בודד"
            split_color = "#15803d" if h["split"] else "#64748b"
            st.markdown(f"""
            <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-right:5px solid #7c3aed;
                        border-radius:14px; padding:16px 20px; margin-bottom:12px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:17px; font-weight:800; color:#0f172a;">{h['name']}</div>
                        <div style="font-size:13px; color:#64748b; margin-top:4px;">📍 {h['address']}</div>
                    </div>
                    <div style="background:#f3e8ff; color:{split_color}; border-radius:20px;
                                padding:4px 14px; font-size:13px; font-weight:700;">
                        {split_label}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("➕ הוסף אולם חדש", use_container_width=True):
            st.info("פונקציונליות הוספת אולם תיושם בשלב ב׳")

    # ── קבוצות ───────────────────────────────────────────────────────
    elif section == "teams_management":
        back_btn()
        st.markdown("<div class='page-title' style='font-size:28px;'>ניהול קבוצות</div>", unsafe_allow_html=True)
        st.write("")

        teams = [
            {"name": "בוגרים גברים א׳", "league": "ליגת העל",        "trainings": 4, "color": "#d90429"},
            {"name": "בוגרות נשים א׳",  "league": "ליגת העל נשים",   "trainings": 3, "color": "#d90429"},
            {"name": "נערים א׳ צפון",   "league": "ליגה ארצית",      "trainings": 3, "color": "#1d4ed8"},
            {"name": "נערות א׳",        "league": "ליגה ארצית נשים", "trainings": 3, "color": "#1d4ed8"},
            {"name": "ילדים ז׳ 1",      "league": "ליגה מחוזית",     "trainings": 2, "color": "#15803d"},
        ]
        for t in teams:
            st.markdown(f"""
            <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-right:5px solid {t['color']};
                        border-radius:14px; padding:14px 20px; margin-bottom:10px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:16px; font-weight:800; color:#0f172a;">{t['name']}</div>
                        <div style="font-size:13px; color:#64748b; margin-top:3px;">{t['league']}</div>
                    </div>
                    <div style="background:#f1f5f9; color:#475569; border-radius:20px;
                                padding:4px 14px; font-size:13px; font-weight:700;">
                        {t['trainings']} אימונים/שבוע
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("➕ הוסף קבוצה חדשה", use_container_width=True):
            st.info("פונקציונליות הוספת קבוצה תיושם בשלב ב׳")

    # ── מאמנים ───────────────────────────────────────────────────────
    elif section == "coaches_management":
        back_btn()
        st.markdown("<div class='page-title' style='font-size:28px;'>ניהול מאמנים</div>", unsafe_allow_html=True)
        st.write("")

        coaches = [
            {"name": "יוסי כהן",  "role": "מאמן ראשי – בוגרים",  "license": "מאמן בכיר"},
            {"name": "מיכל לוי",  "role": "מאמנת ראשית – נשים",   "license": "מאמנת"},
            {"name": "דני אברהם", "role": "מאמן נוער",             "license": "מאמן"},
            {"name": "שרה גולן",  "role": "מאמנת נוער",            "license": "מאמנת"},
            {"name": "רון שפירא", "role": "מאמן שוערים",           "license": "מדריך"},
        ]
        for c in coaches:
            st.markdown(f"""
            <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-right:5px solid #15803d;
                        border-radius:14px; padding:14px 20px; margin-bottom:10px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:16px; font-weight:800; color:#0f172a;">{c['name']}</div>
                        <div style="font-size:13px; color:#64748b; margin-top:3px;">{c['role']}</div>
                    </div>
                    <div style="background:#dcfce7; color:#15803d; border-radius:20px;
                                padding:4px 14px; font-size:13px; font-weight:700;">
                        {c['license']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("➕ הוסף מאמן חדש", use_container_width=True):
            st.info("פונקציונליות הוספת מאמן תיושם בשלב ב׳")

    # ── שחקנים ───────────────────────────────────────────────────────
    elif section == "players_management":
        back_btn()
        st.markdown("<div class='page-title' style='font-size:28px;'>ניהול שחקנים</div>", unsafe_allow_html=True)
        st.write("")
        st.text_input("🔍 חיפוש שחקן לפי שם")
        st.selectbox("סנן לפי קבוצה", ["הכל","בוגרים גברים","בוגרות נשים","נערים א׳","נערות א׳","ילדים ז׳"])
        st.info("רשימת השחקנים המלאה תוצג לאחר חיבור מסד הנתונים בשלב ב׳")
        if st.button("➕ הוסף שחקן חדש", use_container_width=True):
            st.info("פונקציונליות הוספת שחקן תיושם בשלב ב׳")

    # ── מנהלים ───────────────────────────────────────────────────────
    elif section == "managers_management":
        back_btn()
        st.markdown("<div class='page-title' style='font-size:28px;'>ניהול מנהלים</div>", unsafe_allow_html=True)
        st.write("")

        managers = [
            {"name": "אבי פרידמן",  "team": "בוגרים גברים א׳"},
            {"name": "רות שמיר",    "team": "בוגרות נשים א׳"},
            {"name": "נועם כץ",     "team": "נערים א׳ צפון"},
            {"name": "ליאת בן דוד", "team": "נערות א׳"},
        ]
        for m in managers:
            st.markdown(f"""
            <div style="background:#ffffff; border:1.5px solid #e2e8f0; border-right:5px solid #a16207;
                        border-radius:14px; padding:14px 20px; margin-bottom:10px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="font-size:16px; font-weight:800; color:#0f172a;">{m['name']}</div>
                <div style="font-size:13px; color:#64748b; margin-top:3px;">אחראי: {m['team']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("➕ הוסף מנהל חדש", use_container_width=True):
            st.info("פונקציונליות הוספת מנהל תיושם בשלב ב׳")
