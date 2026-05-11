"""
pages/2_Optimization.py
מנוע אופטימיזציה – עיצוב זהה לדף הבית
"""
import streamlit as st
import time, random, os
from sections.db_data import TEAMS_DB, COACHES_DB, HALLS_DB, COACH_NAMES, HALL_NAMES, TEAM_NAMES

st.set_page_config(
    page_title="יצירת לוח אימונים – הפועל ראשון לציון",
    page_icon="📅",
    layout="centered",
)

# ── CSS זהה לדף הבית ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
* { font-family: 'Heebo', sans-serif !important; }
.main, .stApp { direction: rtl; text-align: right; background: #ffffff; }
[data-testid="stSidebarNav"] { direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }
.block-container { padding-top: 2rem !important; max-width: 700px !important; margin: auto !important; }

.home-title-sub {
    font-size: 20px; font-weight: 700; color: #64748b;
    text-align: center; margin-bottom: 4px; margin-top: 16px;
}
.home-title-main {
    font-size: 40px; font-weight: 900; color: #0f172a;
    text-align: center; margin-bottom: 48px; line-height: 1.2;
}

.stButton > button {
    width: 100% !important;
    border-radius: 16px !important;
    height: 110px !important;
    font-family: 'Heebo', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    border: none !important;
    transition: all 0.15s ease !important;
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* כפתור 1 – לבן */
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(1) > button {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 2px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(1) > button:hover {
    border-color: #d90429 !important;
    color: #d90429 !important;
}

/* כפתור 2 – אדום */
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(2) > button {
    background: #d90429 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(217,4,41,0.35) !important;
}
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(2) > button:hover {
    background: #b80222 !important;
}

/* כפתור 3 – כהה */
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(3) > button {
    background: #0f172a !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
}
div[data-testid="stVerticalBlock"] .stButton:nth-of-type(3) > button:hover {
    background: #1e293b !important;
}

/* ── מסכי פנים ── */
.form-lbl { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
hr.div { border: none; border-top: 1px solid #e2e8f0; margin: 16px 0; }
.data-card { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 12px 16px; margin-bottom: 8px; }

.inner-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    font-size: 15px !important; font-weight: 700 !important;
    background: #d90429 !important; color: #ffffff !important; border: none !important;
    box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important;
}
.cancel-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    font-size: 15px !important; background: #ffffff !important; color: #64748b !important;
    border: 1.5px solid #e2e8f0 !important;
}
.retry-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    font-size: 15px !important; font-weight: 700 !important;
    background: #ffffff !important; color: #d90429 !important;
    border: 2px solid #d90429 !important;
}
.confirm-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    font-size: 15px !important; font-weight: 700 !important;
    background: #16a34a !important; color: #ffffff !important; border: none !important;
}
.solution-card { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 20px 24px; margin-bottom: 12px; }
.solution-card.active { border-color: #d90429; box-shadow: 0 0 0 3px rgba(217,4,41,0.08); }
.solution-card.prev   { border-color: #94a3b8; opacity: 0.75; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "opt_sub":       "main",
    "constraints":   [],
    "opt_result":    None,
    "prev_result":   None,
    "show_previous": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


def fake_solution(seed=None):
    if seed: random.seed(seed)
    score = random.randint(72, 96)
    return {
        "score": score, "scheduled": random.randint(34, 42), "total": 42,
        "hard_constraints": 14, "warnings": random.randint(0, 4),
        "sessions": [
            {"team": "בוגרים",  "day": "שני",   "time": "19:00–20:30", "hall": "נחלת",   "warning": False},
            {"team": "בוגרות",  "day": "שני",   "time": "19:00–20:15", "hall": "אשלים",  "warning": False},
            {"team": "י",       "day": "ראשון", "time": "16:30–17:45", "hall": "רועים",  "warning": False},
            {"team": "נוער",    "day": "ראשון", "time": "16:00–17:15", "hall": "גן נחום","warning": score < 85},
            {"team": "ילדות ז", "day": "שלישי","time": "16:00–17:00", "hall": "אשלים",  "warning": score < 80},
        ],
    }


def inner_nav(back_label="← חזרה", back_key="inner_back"):
    """header אחיד – כפתור בית מימין, לוגו משמאל"""
    col_home, col_back, col_space, col_logo = st.columns([1.2, 1.8, 5.2, 0.8])
    with col_home:
        if st.button("🏠 בית", key=f"inner_home_{back_key}"):
            st.session_state.opt_sub = "main"
            st.switch_page("app.py")
    with col_back:
        if st.button(back_label, key=back_key):
            st.session_state.opt_sub = "main"
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


# ════════════════════════════════════════════════════════════════════
# מסך ראשי – זהה לדף הבית
# ════════════════════════════════════════════════════════════════════
if st.session_state.opt_sub == "main":

    # ── header אחיד ──────────────────────────────────────────────
    col_home, col_space, col_logo = st.columns([1.2, 7, 0.8])
    with col_home:
        if st.button("🏠 בית", key="main_home"):
            st.switch_page("app.py")
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
        else:
            st.markdown("<div style='text-align:center;font-size:32px;'>🤾</div>", unsafe_allow_html=True)
    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    # ── לוגו גדול + כותרות ────────────────────────────────────────
    col_a, col_b, col_c = st.columns([1.5, 1, 1.5])
    with col_b:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<div style='text-align:center;font-size:80px;'>🤾</div>", unsafe_allow_html=True)

    # כותרות
    st.markdown(
        "<div class='home-title-sub'>הפועל ראשון לציון</div>"
        "<div class='home-title-main'>יצירת לוח אימונים</div>",
        unsafe_allow_html=True,
    )

    # ── עיצוב כפתורים ──
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button {
        background: #ffffff !important; color: #0f172a !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button:hover {
        border-color: #d90429 !important; color: #d90429 !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(5) .stButton > button {
        background: #d90429 !important; color: #ffffff !important;
        border: none !important; box-shadow: 0 4px 20px rgba(217,4,41,0.35) !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(6) .stButton > button {
        background: #0f172a !important; color: #ffffff !important;
        border: none !important; box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # שלושה כפתורים – לבן / אדום / כהה
    if st.button("≡   הוספת אילוצים", use_container_width=True, key="btn_c"):
        st.session_state.opt_sub = "constraints"
        st.rerun()

    run_clicked = st.button("▶   הרץ אופטימיזציה", use_container_width=True, key="btn_r")

    if st.button("↑   העלאת לוח משחקים", use_container_width=True, key="btn_u"):
        st.session_state.opt_sub = "upload"
        st.rerun()

    # כפתור חזרה לבית
    st.write("")
    col_center, _, _ = st.columns([1, 1, 1])
    with col_center:
        if st.button("🏠 חזרה לדף הבית", use_container_width=True, key="btn_home_main"):
            st.switch_page("app.py")

    # הרצה
    if run_clicked:
        with st.spinner("מריץ אלגוריתם שיבוץ..."):
            time.sleep(1.8)
        if st.session_state.opt_result:
            st.session_state.prev_result = st.session_state.opt_result
        st.session_state.opt_result  = fake_solution(seed=random.randint(1, 9999))
        st.session_state.show_previous = False
        st.session_state.opt_sub = "results"
        st.rerun()

    # אם יש תוצאות קודמות
    if st.session_state.opt_result:
        st.write("---")
        st.markdown("### 📊 תוצאות אחרונות")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📋 צפה בתוצאות", use_container_width=True):
                st.session_state.opt_sub = "results"
                st.rerun()
        with c2:
            st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
            if st.button("🔄 נסה פתרון חלופי", use_container_width=True, key="retry_main"):
                with st.spinner("מחפש פתרון חלופי..."):
                    time.sleep(1.2)
                st.session_state.prev_result = st.session_state.opt_result
                st.session_state.opt_result  = fake_solution(seed=random.randint(1, 9999))
                st.session_state.opt_sub = "results"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך הוספת אילוצים
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "constraints":
    inner_nav(back_key='back_constraints')

    st.markdown(
        "<div style='font-size:28px;font-weight:900;color:#0f172a;margin-bottom:4px;'>🔒 הוספת אילוצים</div>"
        "<div style='font-size:14px;color:#94a3b8;margin-bottom:24px;'>צור תקופות חסימה לקבוצות, אולמות או מאמנים</div>",
        unsafe_allow_html=True,
    )

    col_form, col_queue = st.columns([1.1, 1])

    with col_form:
        with st.container(border=True):
            st.markdown("**＋ אילוץ חדש**")
            st.write("")

            entity_type = st.radio("סוג ישות", ["קבוצה", "אולם", "מאמן"],
                                    horizontal=True, label_visibility="collapsed")

            if entity_type == "קבוצה":
                st.markdown("<div class='form-lbl'>בחר קבוצה</div>", unsafe_allow_html=True)
                opts = ["בחר..."] + [t["name"] for t in TEAMS_DB if t["active"]]
                entity_name = st.selectbox("קבוצה", opts, label_visibility="collapsed")
            elif entity_type == "אולם":
                st.markdown("<div class='form-lbl'>בחר אולם</div>", unsafe_allow_html=True)
                opts = ["בחר..."] + [h["name"] for h in HALLS_DB]
                entity_name = st.selectbox("אולם", opts, label_visibility="collapsed")
            else:
                st.markdown("<div class='form-lbl'>בחר מאמן</div>", unsafe_allow_html=True)
                opts = ["בחר..."] + list(COACH_NAMES.values())
                entity_name = st.selectbox("מאמן", opts, label_visibility="collapsed")

            st.markdown("<div class='form-lbl'>תאריך</div>", unsafe_allow_html=True)
            c_date = st.date_input("תאריך", label_visibility="collapsed")

            col_ts, col_te = st.columns(2)
            time_opts = ["בחר שעה..."] + [f"{h:02d}:00" for h in range(6, 23)]
            with col_ts:
                st.markdown("<div class='form-lbl'>משעה</div>", unsafe_allow_html=True)
                from_time = st.selectbox("משעה", time_opts, label_visibility="collapsed")
            with col_te:
                st.markdown("<div class='form-lbl'>עד שעה</div>", unsafe_allow_html=True)
                to_time = st.selectbox("עד שעה", time_opts, label_visibility="collapsed", key="to_t")

            st.markdown("<div class='form-lbl'>סיבה</div>", unsafe_allow_html=True)
            reason = st.text_input("סיבה", placeholder="למשל: משחק, טיול שנתי, שיפוץ",
                                   label_visibility="collapsed")
            st.write("")
            st.markdown('<div class="inner-btn">', unsafe_allow_html=True)
            if st.button("＋ הוסף לתור", use_container_width=True, key="add_c"):
                if entity_name != "בחר..." and from_time != "בחר שעה..." and to_time != "בחר שעה...":
                    st.session_state.constraints.append({
                        "type": entity_type, "entity": entity_name,
                        "date": str(c_date), "from": from_time,
                        "to": to_time, "reason": reason or "—",
                    })
                    st.toast("✅ האילוץ נוסף לתור!")
                    st.rerun()
                else:
                    st.error("נא למלא את כל השדות")
            st.markdown('</div>', unsafe_allow_html=True)

    with col_queue:
        constraints = st.session_state.constraints
        n = len(constraints)
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:16px;'>"
            f"<span style='color:#d90429;font-size:18px;'>📅</span>"
            f"<span style='font-size:18px;font-weight:800;'>תור אילוצים ({n})</span></div>",
            unsafe_allow_html=True,
        )

        if not constraints:
            st.markdown(
                "<div style='text-align:center;padding:40px 20px;color:#94a3b8;'>"
                "<div style='font-size:40px;margin-bottom:12px;'>🔒</div>"
                "<div style='font-weight:600;'>אין אילוצים בתור עדיין</div>"
                "<div style='font-size:13px;'>השתמש בטופס כדי להוסיף</div></div>",
                unsafe_allow_html=True,
            )
        else:
            color_map = {"קבוצה": "#3B82F6", "אולם": "#A855F7", "מאמן": "#22C55E"}
            for i, c in enumerate(constraints):
                color = color_map.get(c["type"], "#d90429")
                col_c, col_x = st.columns([10, 1])
                with col_c:
                    st.markdown(
                        f"<div style='background:#f8fafc;border:1.5px solid #e2e8f0;"
                        f"border-right:4px solid {color};border-radius:10px;"
                        f"padding:10px 14px;margin-bottom:8px;'>"
                        f"<div style='display:flex;justify-content:space-between;'>"
                        f"<span style='font-size:11px;font-weight:700;background:{color}22;"
                        f"color:{color};border-radius:4px;padding:2px 8px;'>{c['type']}</span>"
                        f"<span style='font-size:12px;color:#64748b;'>{c['date']}</span></div>"
                        f"<div style='font-size:15px;font-weight:700;color:#0f172a;margin:4px 0;'>{c['entity']}</div>"
                        f"<div style='font-size:12px;color:#64748b;'>🕐 {c['from']} – {c['to']} · {c['reason']}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                with col_x:
                    if st.button("✕", key=f"del_c_{i}"):
                        st.session_state.constraints.pop(i)
                        st.rerun()

            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="inner-btn">', unsafe_allow_html=True)
                if st.button("שלח הכל", use_container_width=True, key="submit_all"):
                    st.success(f"✅ {n} אילוצים נשלחו!")
                    st.session_state.opt_sub = "main"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                if st.button("נקה הכל", use_container_width=True, key="clear_all"):
                    st.session_state.constraints = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך העלאת לוח משחקים
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "upload":
    inner_nav(back_key='back_upload')

    st.markdown(
        "<div style='font-size:28px;font-weight:900;color:#0f172a;margin-bottom:4px;'>ייבוא וסנכרון לוח משחקים</div>"
        "<div style='font-size:14px;color:#94a3b8;margin-bottom:24px;'>העלה לוח משחקים של הליגה וצור חסימות אוטומטיות</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='border:2px dashed #e2e8f0;border-radius:16px;padding:60px 40px;"
        "text-align:center;background:#fafafa;'>"
        "<div style='font-size:48px;color:#cbd5e1;margin-bottom:16px;'>📄</div>"
        "<div style='font-size:18px;font-weight:700;color:#0f172a;margin-bottom:8px;'>העלאת לוח משחקים</div>"
        "<div style='font-size:14px;color:#64748b;'>גרור ושחרר קובץ CSV או Excel לכאן</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    uploaded = st.file_uploader("בחר קובץ", type=["xlsx","xls","csv"], label_visibility="collapsed")

    st.markdown(
        "<div style='font-size:12px;color:#94a3b8;margin-top:8px;'>"
        "פורמטים נתמכים: CSV, Excel (.xlsx, .xls)<br>"
        "עמודות נדרשות: תאריך, שעה, ליגה, אולם, קבוצת בית, קבוצת חוץ"
        "</div>",
        unsafe_allow_html=True,
    )

    if uploaded:
        st.success(f"✅ הקובץ '{uploaded.name}' הועלה בהצלחה!")
        with st.expander("תצוגה מקדימה"):
            try:
                import pandas as pd
                df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
                st.dataframe(df.head(10))
            except Exception:
                st.warning("לא ניתן לטעון תצוגה מקדימה")

        st.write("")
        st.markdown('<div class="inner-btn">', unsafe_allow_html=True)
        if st.button("✅ אשר וסנכרן", use_container_width=True, key="confirm_upload"):
            st.success("✅ הסנכרון הושלם! החסימות עודכנו.")
            time.sleep(1)
            st.session_state.opt_sub = "main"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך תוצאות
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "results":
    inner_nav(back_key='back_results')

    result = st.session_state.opt_result
    prev   = st.session_state.prev_result

    st.markdown("<div style='font-size:28px;font-weight:900;margin-bottom:16px;'>📊 תוצאות האופטימיזציה</div>",
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
        if st.button("🔄 נסה פתרון חלופי", use_container_width=True, key="retry_res"):
            with st.spinner("מחפש פתרון חלופי..."):
                time.sleep(1.2)
            st.session_state.prev_result = result
            st.session_state.opt_result  = fake_solution(seed=random.randint(1, 9999))
            st.session_state.show_previous = False
            st.toast("✅ נמצא פתרון חלופי!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if prev:
            tog = "🙈 הסתר פתרון קודם" if st.session_state.show_previous else "👁️ הצג פתרון קודם"
            if st.button(tog, use_container_width=True, key="toggle_prev"):
                st.session_state.show_previous = not st.session_state.show_previous
                st.rerun()

    st.write("")

    def render_card(res, label, cls):
        sc = "#16a34a" if res["score"] >= 85 else "#d90429" if res["score"] < 75 else "#d97706"
        w  = f"&nbsp;·&nbsp; ⚠️ {res['warnings']} אזהרות" if res["warnings"] else ""
        st.markdown(
            f"<div class='solution-card {cls}'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
            f"<div><div style='font-size:17px;font-weight:800;margin-bottom:6px;'>{label}</div>"
            f"<div style='color:#64748b;font-size:13px;'>{res['scheduled']}/{res['total']} אימונים שובצו"
            f"&nbsp;·&nbsp; {res['hard_constraints']} אילוצים קשיחים ✔️{w}</div></div>"
            f"<div style='text-align:center;'>"
            f"<div style='width:72px;height:72px;border-radius:50%;border:5px solid {sc};"
            f"display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:{sc};'>"
            f"{res['score']}</div>"
            f"<div style='font-size:11px;color:#94a3b8;margin-top:4px;'>ציון איכות</div>"
            f"</div></div></div>",
            unsafe_allow_html=True,
        )

    if st.session_state.show_previous and prev:
        c1, c2 = st.columns(2)
        with c1: render_card(result, "✅ פתרון נוכחי", "active")
        with c2: render_card(prev,   "⏮️ פתרון קודם",  "prev")
    else:
        render_card(result, "✅ פתרון מומלץ", "active")

    st.markdown("**אימונים מתוכננים:**")
    for s in result["sessions"]:
        icon = "⚠️" if s["warning"] else "✅"
        warn = " &nbsp;·&nbsp; <span style='color:#f59e0b;'>אזהרת שיבוץ</span>" if s["warning"] else ""
        st.markdown(
            f"<div style='background:#ffffff;border:1.5px solid #e2e8f0;border-radius:10px;"
            f"padding:10px 16px;margin-bottom:6px;display:flex;gap:12px;align-items:center;'>"
            f"<span style='font-size:18px;'>{icon}</span>"
            f"<div><div style='font-weight:700;font-size:14px;'>{s['team']}</div>"
            f"<div style='color:#64748b;font-size:12px;'>יום {s['day']} &nbsp;·&nbsp; {s['time']} &nbsp;·&nbsp; 🏢 {s['hall']}{warn}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
        if st.button("✔️ אשר ושמור לוח אימונים", use_container_width=True, key="confirm_res"):
            st.session_state["confirmed_schedule"] = result
            st.success("✅ הלוח אושר ונשמר!")
            time.sleep(1)
            st.switch_page("pages/3_Schedule.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("📋 צפה בלוח השבועי", use_container_width=True, key="view_sched"):
            st.switch_page("pages/3_Schedule.py")
