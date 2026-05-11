"""
pages/2_Optimization.py
מנוע אופטימיזציה – הוספת אילוצים / Upload Match Schedule / Run Optimization
"""
import streamlit as st
import time, random, os
from sections.db_data import קבוצהS_DB, מאמןES_DB, אולםS_DB, מאמן_NAMES, אולם_NAMES, קבוצה_NAMES

st.set_page_config(
    page_title="מנוע אופטימיזציה – הפועל ראשון לציון",
    page_icon="📅",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');
* { font-family: 'Heebo', sans-serif !important; }
.main, .stApp { background: #ffffff; direction: rtl; }
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stHeader"] { background: #ffffff; }
.block-container { max-width: 780px !important; margin: auto !important; padding-top: 1.5rem !important; }

/* ── כפתורי ניווט ── */
.stButton > button {
    border-radius: 10px !important; font-size: 14px !important; font-weight: 600 !important;
    height: 40px !important; background: #ffffff !important; color: #0f172a !important;
    border: 1.5px solid #e2e8f0 !important; padding: 0 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; width: auto !important;
}
.stButton > button:hover { border-color: #d90429 !important; color: #d90429 !important; }

/* ── כפתורי פעולה גדולים ── */
.action-btn > div > button {
    width: 100% !important; border-radius: 16px !important; height: 80px !important;
    font-size: 18px !important; font-weight: 700 !important;
    background: #ffffff !important; color: #0f172a !important;
    border: 1.5px solid #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    display: flex !important; align-items: center !important;
    justify-content: space-between !important; padding: 0 24px !important;
    transition: all 0.15s !important;
}
.action-btn > div > button:hover {
    border-color: #d90429 !important; color: #d90429 !important;
    box-shadow: 0 4px 16px rgba(217,4,41,0.12) !important;
}

/* ── כפתור הרצה אדום ── */
.run-btn > div > button {
    width: 100% !important; border-radius: 16px !important; height: 80px !important;
    font-size: 20px !important; font-weight: 800 !important;
    background: #d90429 !important; color: #ffffff !important; border: none !important;
    box-shadow: 0 6px 24px rgba(217,4,41,0.4) !important;
}
.run-btn > div > button:hover { background: #b80222 !important; color: #ffffff !important; }

/* ── כפתור ניסה שוב ── */
.retry-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    background: #ffffff !important; color: #d90429 !important;
    border: 2px solid #d90429 !important; font-size: 15px !important; font-weight: 700 !important;
}

/* ── כפתור שמירה ירוק ── */
.confirm-btn > div > button {
    width: 100% !important; border-radius: 10px !important; height: 44px !important;
    background: #16a34a !important; color: #ffffff !important;
    border: none !important; font-size: 15px !important; font-weight: 700 !important;
}

/* ── כרטיס אילוץ ── */
.constraint-chip {
    background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px;
    padding: 12px 16px; margin-bottom: 8px;
    display: flex; justify-content: space-between; align-items: flex-start;
}

/* ── Solution card ── */
.solution-card {
    background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px;
    padding: 20px 24px; margin-bottom: 12px;
}
.solution-card.active { border-color: #d90429; box-shadow: 0 0 0 3px rgba(217,4,41,0.08); }
.solution-card.prev   { border-color: #94a3b8; opacity: 0.75; }

/* ── Drop zone ── */
.drop-zone {
    border: 2px dashed #e2e8f0; border-radius: 16px;
    padding: 60px 40px; text-align: center; background: #fafafa;
    transition: border-color 0.15s;
}

/* ── Divider ── */
hr.div { border: none; border-top: 1px solid #e2e8f0; margin: 16px 0; }

/* ── form labels ── */
.form-lbl { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }

/* ── cancel btn in form ── */
.cancel-sm > div > button {
    background: #ffffff !important; color: #64748b !important;
    border: 1.5px solid #e2e8f0 !important; border-radius: 8px !important;
    height: 40px !important; font-size: 14px !important; width: 100% !important;
}
.save-sm > div > button {
    background: #d90429 !important; color: #ffffff !important;
    border: none !important; border-radius: 8px !important;
    height: 40px !important; font-size: 14px !important; font-weight: 700 !important; width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "opt_sub":            "main",   # "main" | "constraints" | "upload"
    "constraints":        [],
    "opt_result":         None,
    "prev_result":        None,
    "show_previous":      False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── פונקציות עזר ─────────────────────────────────────────────────────────────
def fake_solution(seed=None):
    if seed: random.seed(seed)
    score = random.randint(72, 96)
    return {
        "score": score, "scheduled": random.randint(34, 42), "total": 42,
        "hard_constraints": 14, "warnings": random.randint(0, 4),
        "sessions": [
            {"team": "בוגרים",    "day": "שני",    "time": "19:00–20:30", "hall": "נחלת",  "warning": False},
            {"team": "בוגרות",    "day": "שני",    "time": "19:00–20:15", "hall": "אשלים", "warning": False},
            {"team": "י",         "day": "ראשון",  "time": "16:30–17:45", "hall": "רועים", "warning": False},
            {"team": "נוער",      "day": "ראשון",  "time": "16:00–17:15", "hall": "גן נחום","warning": score < 85},
            {"team": "ילדות ז",   "day": "שלישי", "time": "16:00–17:00", "hall": "אשלים", "warning": score < 80},
        ],
    }

def render_solution_card(res, label, css_class):
    score_color = "#16a34a" if res["score"] >= 85 else "#d90429" if res["score"] < 75 else "#d97706"
    warn_txt = f"&nbsp;·&nbsp; ⚠️ {res['warnings']} אזהרות" if res["warnings"] else ""
    st.markdown(f"""
    <div class='solution-card {css_class}'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <div>
                <div style='font-size:17px;font-weight:800;margin-bottom:6px;'>{label}</div>
                <div style='color:#64748b;font-size:13px;'>
                    {res['scheduled']}/{res['total']} אימונים שובצו &nbsp;·&nbsp;
                    {res['hard_constraints']} אילוצים קשיחים ✔️{warn_txt}
                </div>
            </div>
            <div style='text-align:center;'>
                <div style='width:72px;height:72px;border-radius:50%;
                            border:5px solid {score_color};display:flex;
                            align-items:center;justify-content:center;
                            font-size:24px;font-weight:900;color:{score_color};'>
                    {res['score']}
                </div>
                <div style='font-size:11px;color:#94a3b8;margin-top:4px;'>ציון איכות</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── ניווט עליון ───────────────────────────────────────────────────────────────
def top_nav(show_back=True, back_label="← חזרה"):
    col_home, col_back, col_space, col_logo = st.columns([1.2, 1.8, 5.2, 0.8])
    with col_home:
        if st.button("🏠 בית", key="opt_home"):
            st.session_state.opt_sub = "main"
            st.switch_page("app.py")
    if show_back:
        with col_back:
            if st.button(back_label, key="opt_back"):
                st.session_state.opt_sub = "main"
                st.rerun()
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
    st.markdown("<hr class='div'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 1 – ראשי (שלושה כפתורים גדולים)
# ════════════════════════════════════════════════════════════════════
if st.session_state.opt_sub == "main":
    col_home, col_space, col_logo = st.columns([1.2, 6.8, 0.8])
    with col_home:
        if st.button("🏠 בית", key="main_home"):
            st.switch_page("app.py")
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;margin-bottom:40px;'>
            <div style='font-size:22px;font-weight:400;color:#64748b;letter-spacing:2px;'>אופטימיזציה</div>
            <div style='font-size:36px;font-weight:900;color:#0f172a;'>מנוע השיבוץ</div>
        </div>
    """, unsafe_allow_html=True)

    # כפתור 1 – הוספת אילוצים
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("הוספת אילוצים  ≡", use_container_width=True, key="btn_constraints"):
        st.session_state.opt_sub = "constraints"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    # כפתור 2 – העלאת לוח משחקים
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("העלאת לוח משחקים  ↑", use_container_width=True, key="btn_upload"):
        st.session_state.opt_sub = "upload"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    # כפתור 3 – הרצת אופטימיזציה
    st.markdown('<div class="run-btn">', unsafe_allow_html=True)
    run_clicked = st.button("RUN אופטימיזציה  ▶", use_container_width=True, key="btn_run")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center;color:#94a3b8;font-size:13px;margin-top:32px;'>
            הוסף אילוצים → העלה לוח משחקים → הרץ אופטימיזציה
        </div>
    """, unsafe_allow_html=True)

    if run_clicked:
        with st.spinner("מריץ אלגוריתם שיבוץ..."):
            time.sleep(1.8)
        if st.session_state.opt_result:
            st.session_state.prev_result = st.session_state.opt_result
        st.session_state.opt_result  = fake_solution(seed=random.randint(1,9999))
        st.session_state.show_previous = False
        st.session_state.opt_sub = "results"
        st.rerun()

    # תוצאות קיימות
    if st.session_state.opt_result and st.session_state.opt_sub == "main":
        st.write("---")
        st.markdown("### 📊 תוצאות אחרונות")
        col_view, col_retry = st.columns(2)
        with col_view:
            if st.button("📋 צפה בתוצאות", use_container_width=True):
                st.session_state.opt_sub = "results"
                st.rerun()
        with col_retry:
            st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
            if st.button("🔄 נסה פתרון חלופי", use_container_width=True):
                with st.spinner("מחפש פתרון חלופי..."):
                    time.sleep(1.2)
                st.session_state.prev_result = st.session_state.opt_result
                st.session_state.opt_result  = fake_solution(seed=random.randint(1,9999))
                st.session_state.opt_sub = "results"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 2 – הוספת אילוצים
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "constraints":
    top_nav(back_label="← חזרה")

    st.markdown("""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>
            <span style='font-size:22px;'>🔒</span>
            <span style='font-size:28px;font-weight:900;color:#0f172a;'>הוספת אילוצים</span>
        </div>
        <div style='font-size:14px;color:#94a3b8;margin-bottom:24px;'>
            צור תקופות חסימה לקבוצות, אולמות או מאמנים
        </div>
    """, unsafe_allow_html=True)

    col_form, col_queue = st.columns([1.1, 1])

    # ── טופס ─────────────────────────────────────────────────────────
    with col_form:
        with st.container(border=True):
            st.markdown("**＋ אילוץ חדש**")
            st.write("")

            # סוג ישות – 3 כפתורים
            entity_type = st.radio("סוג ישות", ["קבוצה", "אולם", "מאמן"],
                                    horizontal=True, label_visibility="collapsed")
            st.write("")

            # בחירה דינמית
            if entity_type == "קבוצה":
                st.markdown("<div class='form-lbl'>בחר קבוצה</div>", unsafe_allow_html=True)
                team_opts = ["בחר..."] + [t["name"] for t in קבוצהS_DB if t["active"]]
                entity_name = st.selectbox("קבוצה", team_opts, label_visibility="collapsed")
            elif entity_type == "אולם":
                st.markdown("<div class='form-lbl'>בחר אולם</div>", unsafe_allow_html=True)
                hall_opts = ["בחר..."] + [h["name"] for h in אולםS_DB]
                entity_name = st.selectbox("אולם", hall_opts, label_visibility="collapsed")
            else:
                st.markdown("<div class='form-lbl'>בחר מאמן</div>", unsafe_allow_html=True)
                coach_opts = ["בחר..."] + list(מאמן_NAMES.values())
                entity_name = st.selectbox("מאמן", coach_opts, label_visibility="collapsed")

            st.markdown("<div class='form-lbl'>תאריך</div>", unsafe_allow_html=True)
            c_date = st.date_input("תאריך", label_visibility="collapsed")

            col_ts, col_te = st.columns(2)
            with col_ts:
                st.markdown("<div class='form-lbl'>משעה</div>", unsafe_allow_html=True)
                time_opts = ["בחר שעה..."] + [f"{h:02d}:00" for h in range(6, 23)]
                from_time = st.selectbox("From", time_opts, label_visibility="collapsed")
            with col_te:
                st.markdown("<div class='form-lbl'>עד שעה</div>", unsafe_allow_html=True)
                to_time = st.selectbox("To", time_opts, label_visibility="collapsed", key="to_time")

            st.markdown("<div class='form-lbl'>סיבה</div>", unsafe_allow_html=True)
            reason = st.text_input("סיבה",
                                   placeholder="למשל: משחק, טיול שנתי, שיפוץ",
                                   label_visibility="collapsed")

            st.write("")
            st.markdown('<div class="save-sm">', unsafe_allow_html=True)
            if st.button("＋ הוסף לתור", use_container_width=True, key="add_constraint"):
                if entity_name != "בחר..." and from_time != "בחר שעה..." and to_time != "בחר שעה...":
                    st.session_state.constraints.append({
                        "type": entity_type, "entity": entity_name,
                        "date": str(c_date),
                        "from": from_time, "to": to_time,
                        "reason": reason or "—",
                    })
                    st.toast("✅ האילוץ נוסף לתור!")
                    st.rerun()
                else:
                    st.error("נא למלא את כל השדות")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── תור אילוצים ──────────────────────────────────────────────────
    with col_queue:
        constraints = st.session_state.constraints
        n = len(constraints)
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:16px;'>"
            f"<span style='color:#d90429;font-size:18px;'>📅</span>"
            f"<span style='font-size:18px;font-weight:800;'>תור אילוצים ({n})</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if not constraints:
            st.markdown("""
                <div style='text-align:center;padding:40px 20px;color:#94a3b8;'>
                    <div style='font-size:40px;margin-bottom:12px;'>🔒</div>
                    <div style='font-weight:600;'>אין אילוצים בתור עדיין</div>
                    <div style='font-size:13px;'>השתמש בטופס כדי להוסיף אילוצים</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            color_map = {"קבוצה": "#3B82F6", "אולם": "#A855F7", "מאמן": "#22C55E"}
            for i, c in enumerate(constraints):
                color = color_map.get(c["type"], "#d90429")
                col_c, col_x = st.columns([10, 1])
                with col_c:
                    st.markdown(f"""
                    <div style='background:#f8fafc;border:1.5px solid #e2e8f0;
                                border-right:4px solid {color};border-radius:10px;
                                padding:10px 14px;margin-bottom:8px;'>
                        <div style='display:flex;justify-content:space-between;'>
                            <span style='font-size:11px;font-weight:700;background:{color}22;
                                         color:{color};border-radius:4px;padding:2px 8px;'>
                                {c['type'].upper()}
                            </span>
                            <span style='font-size:12px;color:#64748b;'>{c['date']}</span>
                        </div>
                        <div style='font-size:15px;font-weight:700;color:#0f172a;margin:4px 0;'>
                            {c['entity']}
                        </div>
                        <div style='font-size:12px;color:#64748b;'>
                            🕐 {c['from']} – {c['to']} &nbsp;·&nbsp; {c['reason']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_x:
                    if st.button("✕", key=f"del_c_{i}"):
                        st.session_state.constraints.pop(i)
                        st.rerun()

            st.write("")
            col_submit, col_clear = st.columns(2)
            with col_submit:
                st.markdown('<div class="save-sm">', unsafe_allow_html=True)
                if st.button("שלח הכל", use_container_width=True):
                    st.success(f"✅ {n} אילוצים נשלחו!")
                    st.session_state.opt_sub = "main"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_clear:
                st.markdown('<div class="cancel-sm">', unsafe_allow_html=True)
                if st.button("נקה הכל", use_container_width=True):
                    st.session_state.constraints = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 3 – העלאת לוח משחקים
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "upload":
    top_nav(back_label="← חזרה")

    st.markdown("""
        <div style='font-size:22px;font-weight:900;color:#0f172a;margin-bottom:4px;'>
            ייבוא וסנכרון לוח משחקים
        </div>
        <div style='font-size:14px;color:#94a3b8;margin-bottom:24px;'>
            העלה לוח משחקים של הליגה וצור חסימות אוטומטיות
        </div>
    """, unsafe_allow_html=True)

    # Drop zone
    st.markdown("""
        <div class='drop-zone'>
            <div style='font-size:48px;color:#cbd5e1;margin-bottom:16px;'>📄</div>
            <div style='font-size:18px;font-weight:700;color:#0f172a;margin-bottom:8px;'>
                העלאת לוח משחקים של הליגה
            </div>
            <div style='font-size:14px;color:#64748b;'>
                גרור ושחרר קובץ CSV או Excel לכאן
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    uploaded = st.file_uploader(
        "בחר קובץ",
        type=["xlsx", "xls", "csv"],
        label_visibility="collapsed",
    )

    st.markdown("""
        <div style='font-size:12px;color:#94a3b8;margin-top:12px;'>
            פורמטים נתמכים: CSV, Excel (.xlsx, .xls)<br>
            עמודות נדרשות: תאריך, שעה, ליגה, אולם, קבוצת בית, קבוצת חוץ
        </div>
    """, unsafe_allow_html=True)

    if uploaded:
        st.success(f"✅ הקובץ '{uploaded.name}' הועלה בהצלחה!")
        st.info("הקובץ יעובד ויצור חסימות אוטומטיות עבור כל משחק.")

        with st.expander("תצוגה מקדימה"):
            try:
                import pandas as pd
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)
                st.dataframe(df.head(10))
            except Exception:
                st.warning("לא ניתן לטעון תצוגה מקדימה")

        st.write("")
        st.markdown('<div class="save-sm">', unsafe_allow_html=True)
        if st.button("✅ אשר וסנכרן", use_container_width=True, key="confirm_upload"):
            st.success("✅ הסנכרון הושלם! החסימות עודכנו.")
            time.sleep(1)
            st.session_state.opt_sub = "main"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 4 – תוצאות אופטימיזציה
# ════════════════════════════════════════════════════════════════════
elif st.session_state.opt_sub == "results":
    top_nav(back_label="← חזרה")

    result = st.session_state.opt_result
    prev   = st.session_state.prev_result

    st.markdown("<div style='font-size:28px;font-weight:900;margin-bottom:16px;'>📊 תוצאות האופטימיזציה</div>",
                unsafe_allow_html=True)

    # כפתורי פעולה
    col_retry, col_prev_btn = st.columns(2)
    with col_retry:
        st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
        if st.button("🔄 נסה פתרון חלופי", use_container_width=True):
            with st.spinner("מחפש פתרון חלופי..."):
                time.sleep(1.2)
            st.session_state.prev_result = result
            st.session_state.opt_result  = fake_solution(seed=random.randint(1,9999))
            st.session_state.show_previous = False
            st.toast("✅ נמצא פתרון חלופי!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_prev_btn:
        if prev:
            tog = "🙈 הסתר פתרון קודם" if st.session_state.show_previous else "👁️ הצג פתרון קודם"
            if st.button(tog, use_container_width=True):
                st.session_state.show_previous = not st.session_state.show_previous
                st.rerun()

    st.write("")

    # כרטיסי תוצאה
    if st.session_state.show_previous and prev:
        c1, c2 = st.columns(2)
        with c1: render_solution_card(result, "✅ פתרון נוכחי", "active")
        with c2: render_solution_card(prev,   "⏮️ פתרון קודם",  "prev")
    else:
        render_solution_card(result, "✅ פתרון מומלץ", "active")

    # אימונים מתוכננים
    st.markdown("**אימונים מתוכננים:**")
    for s in result["sessions"]:
        icon     = "⚠️" if s["warning"] else "✅"
        warn_txt = " &nbsp;·&nbsp; <span style='color:#f59e0b;'>אזהרת שיבוץ</span>" if s["warning"] else ""
        st.markdown(f"""
        <div style='background:#ffffff;border:1.5px solid #e2e8f0;border-radius:10px;
                    padding:10px 16px;margin-bottom:6px;display:flex;gap:12px;align-items:center;'>
            <span style='font-size:18px;'>{icon}</span>
            <div>
                <div style='font-weight:700;font-size:14px;'>{s['team']}</div>
                <div style='color:#64748b;font-size:12px;'>
                    יום {s['day']} &nbsp;·&nbsp; {s['time']} &nbsp;·&nbsp; 🏢 {s['hall']}{warn_txt}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.write("---")
    col_confirm, col_view = st.columns(2)
    with col_confirm:
        st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
        if st.button("✔️ אשר ושמור לוח אימונים", use_container_width=True):
            st.session_state["confirmed_schedule"] = result
            st.success("✅ הלוח אושר ונשמר!")
            time.sleep(1)
            st.switch_page("pages/3_Schedule.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_view:
        if st.button("📋 צפה בלוח השבועי", use_container_width=True):
            st.switch_page("pages/3_Schedule.py")
