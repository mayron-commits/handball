"""
pages/1_Manage_Data.py
Manage halls, teams, coaches, players and managers.
"""
import streamlit as st
from utils import apply_global_css, show_logo_header, circular_card

st.set_page_config(
    page_title="ניהול נתונים – הפועל ראשון לציון",
    page_icon="⚙️",
    layout="wide",
)
apply_global_css()

# ── Back-to-home button ───────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🏠 בית"):
        st.switch_page("app.py")

show_logo_header("ניהול נתונים", "בחר ישות לצפייה וניהול")
st.write("---")

# ── Determine which sub-section to show ──────────────────────────────────────
# circular_card stores the clicked key in session_state["manage_section"]
section = st.session_state.get("manage_section", "overview")

# ── Overview (landing) ────────────────────────────────────────────────────────
if section == "overview":
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        circular_card("אולמות", 4, "🏢", "#A855F7", "halls_management")
    with r1_c2:
        circular_card("קבוצות", 15, "👥", "#3B82F6", "teams_management")
    with r1_c3:
        circular_card("מאמנים", 12, "👨‍🏫", "#22C55E", "coaches_management")

    st.write("##")
    r2_c1, r2_c2, r2_c3 = st.columns([1, 2, 1])
    with r2_c2:
        sub1, sub2 = st.columns(2)
        with sub1:
            circular_card("שחקנים", 421, "🏃", "#F97316", "players_management")
        with sub2:
            circular_card("מנהלים", 12, "💼", "#EAB308", "managers_management")

# ── Halls management ──────────────────────────────────────────────────────────
elif section == "halls_management":
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ חזרה"):
            st.session_state["manage_section"] = "overview"
            st.rerun()

    show_logo_header("ניהול אולמות", "הגדר מתקני אימון ויכולות פיצול מגרש")
    st.write("##")

    halls = [
        {"name": "אשלים",  "address": "הצמרת 17, ראשון לציון",         "type": "ניתן לפיצול"},
        {"name": "רוזן",   "address": "מנחם בגין 13, ראשון לציון",      "type": "ניתן לפיצול"},
        {"name": "נחלת",   "address": "רחוב העצמאות 37, ראשון לציון",   "type": "ניתן לפיצול"},
        {"name": "גן נחום","address": "תמר אבן 9, ראשון לציון",         "type": "מגרש בודד"},
    ]

    for hall in halls:
        st.markdown(
            f"""
            <div style="background-color:white; padding:20px; border-radius:10px;
                        border-right:5px solid #d90429; margin-bottom:10px;
                        box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                <h4 style="margin:0;">{hall['name']}
                    <span style="font-size:12px; color:gray;">({hall['type']})</span>
                </h4>
                <p style="margin:5px 0 0 0; color:#64748b;">📍 {hall['address']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("##")
    if st.button("➕ הוסף אולם חדש"):
        st.info("פונקציונליות הוספת אולם תיושם בשלב ב׳")

# ── Teams management ──────────────────────────────────────────────────────────
elif section == "teams_management":
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ חזרה"):
            st.session_state["manage_section"] = "overview"
            st.rerun()

    show_logo_header("ניהול קבוצות", "צפה ועדכן קבוצות פעילות במועדון")
    st.write("##")

    teams = [
        {"name": "בוגרים גברים א׳", "league": "ליגת העל",        "coach": "מאמן ראשי", "trainings": 4},
        {"name": "בוגרות נשים א׳",  "league": "ליגת העל נשים",   "coach": "מאמנת ראשית","trainings": 3},
        {"name": "נערים א׳ צפון",   "league": "ליגה ארצית",      "coach": "מאמן נוער",  "trainings": 3},
        {"name": "נערות א׳",        "league": "ליגה ארצית נשים", "coach": "מאמנת נוער", "trainings": 3},
        {"name": "ילדים ז׳ 1",      "league": "ליגה מחוזית",     "coach": "מדריך",      "trainings": 2},
    ]

    for team in teams:
        col_name, col_league, col_coach, col_train = st.columns([3, 2, 2, 1])
        with col_name:
            st.markdown(f"**{team['name']}**")
        with col_league:
            st.markdown(f"<span style='color:gray;font-size:13px;'>{team['league']}</span>",
                        unsafe_allow_html=True)
        with col_coach:
            st.markdown(f"<span style='color:gray;font-size:13px;'>{team['coach']}</span>",
                        unsafe_allow_html=True)
        with col_train:
            st.markdown(f"<span style='color:#3B82F6; font-weight:bold;'>{team['trainings']}✕</span>",
                        unsafe_allow_html=True)
        st.divider()

    if st.button("➕ הוסף קבוצה חדשה"):
        st.info("פונקציונליות הוספת קבוצה תיושם בשלב ב׳")

# ── Coaches management ────────────────────────────────────────────────────────
elif section == "coaches_management":
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ חזרה"):
            st.session_state["manage_section"] = "overview"
            st.rerun()

    show_logo_header("ניהול מאמנים", "פרטי מאמנים וזמינות")
    st.write("##")

    coaches = [
        {"name": "יוסי כהן",    "role": "מאמן ראשי – בוגרים",   "license": "מאמן בכיר"},
        {"name": "מיכל לוי",    "role": "מאמנת ראשית – נשים",    "license": "מאמנת"},
        {"name": "דני אברהם",   "role": "מאמן נוער",             "license": "מאמן"},
        {"name": "שרה גולן",    "role": "מאמנת נוער",            "license": "מאמנת"},
        {"name": "רון שפירא",   "role": "מאמן שוערים",           "license": "מדריך"},
    ]

    for coach in coaches:
        st.markdown(
            f"""
            <div style="background-color:white; padding:16px; border-radius:10px;
                        border-right:5px solid #22C55E; margin-bottom:10px;
                        box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                <h4 style="margin:0;">{coach['name']}</h4>
                <p style="margin:4px 0 0; color:#64748b; font-size:13px;">
                    {coach['role']} &nbsp;·&nbsp;
                    <strong style="color:#22C55E;">{coach['license']}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("➕ הוסף מאמן חדש"):
        st.info("פונקציונליות הוספת מאמן תיושם בשלב ב׳")

# ── Players management ────────────────────────────────────────────────────────
elif section == "players_management":
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ חזרה"):
            st.session_state["manage_section"] = "overview"
            st.rerun()

    show_logo_header("ניהול שחקנים", "421 שחקנים ושחקניות רשומים")
    st.write("##")

    search = st.text_input("🔍 חיפוש שחקן לפי שם")
    team_filter = st.selectbox(
        "סנן לפי קבוצה",
        ["הכל", "בוגרים גברים", "בוגרות נשים", "נערים א׳", "נערות א׳", "ילדים ז׳"],
    )

    st.info("רשימת השחקנים המלאה תוצג לאחר חיבור מסד הנתונים בשלב ב׳")

    if st.button("➕ הוסף שחקן חדש"):
        st.info("פונקציונליות הוספת שחקן תיושם בשלב ב׳")

# ── Managers management ───────────────────────────────────────────────────────
elif section == "managers_management":
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅️ חזרה"):
            st.session_state["manage_section"] = "overview"
            st.rerun()

    show_logo_header("ניהול מנהלים", "מנהלי קבוצות ואחראים")
    st.write("##")

    managers = [
        {"name": "אבי פרידמן",  "team": "בוגרים גברים א׳"},
        {"name": "רות שמיר",    "team": "בוגרות נשים א׳"},
        {"name": "נועם כץ",     "team": "נערים א׳ צפון"},
        {"name": "ליאת בן דוד", "team": "נערות א׳"},
    ]

    for m in managers:
        st.markdown(
            f"""
            <div style="background-color:white; padding:16px; border-radius:10px;
                        border-right:5px solid #EAB308; margin-bottom:10px;
                        box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                <h4 style="margin:0;">{m['name']}</h4>
                <p style="margin:4px 0 0; color:#64748b; font-size:13px;">
                    אחראי על: <strong>{m['team']}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("➕ הוסף מנהל חדש"):
        st.info("פונקציונליות הוספת מנהל תיושם בשלב ב׳")
