"""
sections/teams.py
ניהול קבוצות – כרטיסים, הוספה, עריכה
"""
import streamlit as st
from sections.shared import top_nav, page_header

# נתוני ברירת מחדל
DEFAULT_קבוצהS = [
    {"name": "בוגרים גברים א׳", "age_group": "בוגרים",  "sessions": 4, "duration": 90, "coach": "יוסי כהן",  "halls": ["אשלים","נחלת"],    "split_court": False, "shabbat": False, "color": "#d90429"},
    {"name": "בוגרות נשים א׳",  "age_group": "בוגרים",  "sessions": 3, "duration": 90, "coach": "מיכל לוי",  "halls": ["אשלים","רוזן"],     "split_court": True,  "shabbat": False, "color": "#d90429"},
    {"name": "נערים א׳ צפון",   "age_group": "כיתה י׳",  "sessions": 3, "duration": 90, "coach": "דני אברהם", "halls": ["רוזן","גן נחום"],   "split_court": True,  "shabbat": False, "color": "#1d4ed8"},
    {"name": "נערות א׳",        "age_group": "כיתה י׳",  "sessions": 3, "duration": 75, "coach": "שרה גולן",  "halls": ["נחלת"],             "split_court": True,  "shabbat": True,  "color": "#db2777"},
    {"name": "ילדים ז׳ 1",      "age_group": "כיתה ז׳",  "sessions": 2, "duration": 60, "coach": "דני אברהם", "halls": ["אשלים","גן נחום"],  "split_court": True,  "shabbat": False, "color": "#15803d"},
]

ALL_אולםS    = ["אשלים", "רוזן", "נחלת", "גן נחום"]
AGE_GROUPS   = ["בוגרים", "כיתה י״ב", "כיתה י״א", "כיתה י׳", "כיתה ט׳", "כיתה ח׳", "כיתה ז׳"]
COLOR_MAP    = {"בוגרים": "#d90429", "כיתה י׳": "#d90429", "כיתה י״א": "#d90429",
                "כיתה י״ב": "#d90429", "כיתה ט׳": "#1d4ed8", "כיתה ח׳": "#1d4ed8",
                "כיתה ז׳": "#15803d"}


def init_state():
    for k, v in {
        "teams": DEFAULT_קבוצהS,
        "show_add_team": False,
        "edit_team_idx": None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _form(title, data, save_key, cancel_key, coaches):
    """טופס הוספה / עריכה"""
    with st.container(border=True):
        st.markdown(f"<div style='font-size:20px;font-weight:800;margin-bottom:16px;'>{title}</div>", unsafe_allow_html=True)

        # שורה 1 – שם + שנתון
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='form-lbl'>שם הקבוצה</div>", unsafe_allow_html=True)
            f_name = st.text_input("שם", value=data.get("name",""), placeholder="למשל: נערים א׳", label_visibility="collapsed", key=f"f_name_{save_key}")
        with c2:
            st.markdown("<div class='form-lbl'>שנתון / קטגוריה</div>", unsafe_allow_html=True)
            curr_age = data.get("age_group", AGE_GROUPS[0])
            f_age = st.selectbox("שנתון", AGE_GROUPS,
                                  index=AGE_GROUPS.index(curr_age) if curr_age in AGE_GROUPS else 0,
                                  label_visibility="collapsed", key=f"f_age_{save_key}")

        # שורה 2 – אימונים + משך + מאמן
        c3, c4, c5 = st.columns(3)
        with c3:
            st.markdown("<div class='form-lbl'>אימונים בשבוע</div>", unsafe_allow_html=True)
            f_sessions = st.number_input("אימונים", min_value=1, max_value=6,
                                          value=data.get("sessions", 3),
                                          label_visibility="collapsed", key=f"f_sess_{save_key}")
        with c4:
            st.markdown("<div class='form-lbl'>משך אימון (דקות)</div>", unsafe_allow_html=True)
            f_duration = st.number_input("משך", min_value=45, max_value=120, step=15,
                                          value=data.get("duration", 90),
                                          label_visibility="collapsed", key=f"f_dur_{save_key}")
        with c5:
            st.markdown("<div class='form-lbl'>מאמן אחראי</div>", unsafe_allow_html=True)
            coach_names = ["בחר מאמן"] + [c["name"] for c in coaches]
            curr_coach = data.get("coach", "בחר מאמן")
            f_coach = st.selectbox("מאמן", coach_names,
                                    index=coach_names.index(curr_coach) if curr_coach in coach_names else 0,
                                    label_visibility="collapsed", key=f"f_coach_{save_key}")

        # שורה 3 – אולמות מורשים
        st.markdown("<div class='form-lbl' style='margin-top:12px;'>אולמות מורשים</div>", unsafe_allow_html=True)
        curr_halls = data.get("halls", [])
        hall_cols = st.columns(4)
        f_halls = []
        for j, hall in enumerate(ALL_אולםS):
            with hall_cols[j]:
                if st.checkbox(hall, value=hall in curr_halls, key=f"f_hall_{j}_{save_key}"):
                    f_halls.append(hall)

        # שורה 4 – checkboxes
        st.write("")
        cx1, cx2 = st.columns(2)
        with cx1:
            with st.container(border=True):
                f_split = st.checkbox(
                    "ניתן לפיצול מגרש",
                    value=data.get("split_court", False),
                    key=f"f_split_{save_key}",
                    help="ניתן לאמן שתי קבוצות במקביל"
                )
                st.caption("ניתן לחלוק אולם עם קבוצה נוספת")
        with cx2:
            with st.container(border=True):
                f_shabbat = st.checkbox(
                    "שומר שבת",
                    value=data.get("shabbat", False),
                    key=f"f_shabbat_{save_key}",
                    help="ללא אימונים בשישי בערב ושבת"
                )
                st.caption("ללא אימונים בשישי בערב / שבת")

        # כפתורים
        st.write("")
        cb, cs = st.columns(2)
        with cb:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("ביטול", use_container_width=True, key=cancel_key):
                st.session_state.show_add_team = False
                st.session_state.edit_team_idx = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cs:
            btn_label = "עדכן קבוצה" if data else "הוסף קבוצה"
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button(btn_label, use_container_width=True, key=save_key):
                if f_name.strip():
                    return {
                        "name": f_name.strip(),
                        "age_group": f_age,
                        "sessions": int(f_sessions),
                        "duration": int(f_duration),
                        "coach": f_coach if f_coach != "בחר מאמן" else "—",
                        "halls": f_halls,
                        "split_court": f_split,
                        "shabbat": f_shabbat,
                        "color": COLOR_MAP.get(f_age, "#1d4ed8"),
                    }
                else:
                    st.error("נא להזין שם קבוצה")
            st.markdown('</div>', unsafe_allow_html=True)
    return None


def render(coaches):
    """מסך ניהול קבוצות"""
    init_state()
    top_nav("ניהול נתונים", "overview")
    page_header("ניהול", "קבוצות", "הגדר קבוצות, מאמנים ודרישות אימון",
                "הוסף קבוצה חדשה", "add_team_btn", "show_add_team")

    edit_idx = st.session_state.edit_team_idx

    # ── טופס עריכה ───────────────────────────────────────────────────
    if edit_idx is not None:
        result = _form(
            "עריכת קבוצה",
            st.session_state.teams[edit_idx],
            f"save_edit_team_{edit_idx}",
            f"cancel_edit_team_{edit_idx}",
            coaches,
        )
        if result:
            st.session_state.teams[edit_idx] = result
            st.session_state.edit_team_idx = None
            st.success(f"✅ הקבוצה '{result['name']}' עודכנה!")
            st.rerun()
        st.write("")

    # ── טופס הוספה ───────────────────────────────────────────────────
    elif st.session_state.show_add_team:
        result = _form("הוספת קבוצה חדשה", {}, "save_new_team", "cancel_new_team", coaches)
        if result:
            st.session_state.teams.append(result)
            st.session_state.show_add_team = False
            st.success(f"✅ הקבוצה '{result['name']}' נוספה!")
            st.rerun()
        st.write("")

    # ── רשימת קבוצות ─────────────────────────────────────────────────
    for i, team in enumerate(st.session_state.teams):
        color = team.get("color", "#1d4ed8")
        col_info, col_sess, col_dur, col_coach, col_edit, col_del = st.columns([4, 1.2, 1.2, 1.8, 0.5, 0.5])

        with col_info:
            tags_html = f"<span class='tag tag-gray'>{team['age_group']}</span>"
            if team.get("shabbat"):
                tags_html += " <span class='tag tag-yellow'>שומר שבת</span>"
            if team.get("split_court"):
                tags_html += " <span class='tag tag-purple'>פיצול מגרש</span>"
            st.markdown(f"""
            <div class='data-card' style='border-right:5px solid {color};padding:16px 20px;'>
                <div style='display:flex;align-items:center;gap:14px;'>
                    <div style='width:48px;height:48px;border-radius:12px;background:#f0f9ff;
                                display:flex;align-items:center;justify-content:center;font-size:22px;'>👥</div>
                    <div>
                        <div style='font-size:18px;font-weight:800;color:#0f172a;'>{team['name']}</div>
                        <div style='margin-top:4px;'>{tags_html}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_sess:
            st.markdown(f"""
            <div class='stat-box' style='background:#eff6ff;border-color:#bfdbfe;margin-top:2px;'>
                <div class='stat-number' style='color:#1d4ed8;'>📅<br>{team['sessions']}</div>
                <div class='stat-label'>אימונים/שבוע</div>
            </div>
            """, unsafe_allow_html=True)

        with col_dur:
            st.markdown(f"""
            <div class='stat-box' style='background:#f0fdf4;border-color:#bbf7d0;margin-top:2px;'>
                <div class='stat-number' style='color:#15803d;'>⏱<br>{team['duration']}</div>
                <div class='stat-label'>דקות</div>
            </div>
            """, unsafe_allow_html=True)

        with col_coach:
            st.markdown(f"""
            <div class='stat-box' style='margin-top:2px;'>
                <div style='font-size:11px;font-weight:700;color:#94a3b8;letter-spacing:1px;'>מאמן</div>
                <div style='font-size:14px;font-weight:700;color:#0f172a;margin-top:4px;'>👤 {team.get('coach','—')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_edit:
            st.write("")
            if st.button("✏️", key=f"edit_t_{i}"):
                st.session_state.edit_team_idx = i
                st.session_state.show_add_team = False
                st.rerun()

        with col_del:
            st.write("")
            if st.button("🗑️", key=f"del_t_{i}"):
                deleted = st.session_state.teams.pop(i)
                st.toast(f"הקבוצה '{deleted['name']}' נמחקה")
                st.rerun()
