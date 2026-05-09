"""
pages/1_Manage_Data.py
ניהול נתונים – כולל תת-מסך מאמנים מלא עם זמינות שבועית
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
.block-container { max-width: 960px !important; margin: auto !important; padding-top: 1.5rem !important; }

/* ── ניווט ── */
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
    font-size: 15px !important; font-weight: 600 !important; height: 48px !important; width: 100% !important;
}

/* ── כפתור שמירה ── */
.save-btn > div > button {
    background: #d90429 !important; color: #ffffff !important; border: none !important;
    border-radius: 10px !important; font-size: 15px !important; font-weight: 700 !important;
    height: 48px !important; box-shadow: 0 4px 14px rgba(217,4,41,0.3) !important; width: 100% !important;
}

/* ── כפתור זמינות (סגול) ── */
.avail-btn > div > button {
    background: #f3e8ff !important; color: #7c3aed !important;
    border: 1.5px solid #e9d5ff !important; border-radius: 10px !important;
    font-size: 13px !important; font-weight: 700 !important; height: 56px !important; width: 100% !important;
}
.avail-btn > div > button:hover { background: #ede9fe !important; }

/* ── כרטיס מאמן ── */
.coach-card {
    background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px;
    padding: 20px 24px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.coach-avatar {
    width: 56px; height: 56px; border-radius: 50%; background: #dcfce7;
    display: flex; align-items: center; justify-content: center; font-size: 24px;
}
.coach-name { font-size: 20px; font-weight: 800; color: #0f172a; }
.coach-role-tag {
    display: inline-block; background: #f1f5f9; color: #475569;
    border-radius: 20px; padding: 2px 12px; font-size: 13px; font-weight: 600; margin: 4px 0 8px;
}
.coach-detail { font-size: 13px; color: #64748b; margin: 2px 0; }

/* ── טבלת זמינות ── */
.avail-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.avail-table th {
    background: #f8fafc; padding: 10px 8px; font-size: 12px; font-weight: 700;
    color: #475569; border-bottom: 2px solid #e2e8f0; text-align: center;
    letter-spacing: 0.5px; text-transform: uppercase;
}
.avail-table th.friday { color: #7c3aed; background: #faf5ff; }
.avail-table td { padding: 8px; border-bottom: 1px solid #f1f5f9; text-align: center; font-size: 13px; }
.avail-table td.time-col { font-weight: 600; color: #475569; text-align: right; padding-right: 12px; }
.slot-free { color: #15803d; font-size: 18px; }
.slot-blocked { color: #cbd5e1; font-size: 11px; }

/* ── Divider ── */
hr.div { border: none; border-top: 1px solid #e2e8f0; margin: 16px 0; }

/* ── כותרת ── */
.page-title-lg { font-size: 30px; font-weight: 900; color: #0f172a; }
.page-title-lg span { font-weight: 400; }
.page-sub { font-size: 14px; color: #94a3b8; margin-top: 2px; }

/* ── form labels ── */
.form-lbl { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }

/* ── עיגול ── */
.entity-circle {
    width: 130px; height: 130px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 52px;
    margin: 0 auto 14px; transition: transform 0.15s ease;
}
.entity-circle:hover { transform: scale(1.06); }
.entity-name { font-size: 18px; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: 8px; }
.entity-badge { border-radius: 20px; padding: 4px 18px; font-size: 15px; font-weight: 700; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
DAYS_HE = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
SLOTS = ["08:00–10:00","10:00–12:00","12:00–14:00","14:00–16:00","16:00–18:00","18:00–20:00","20:00–22:00"]

default_avail = {
    d: {s: (d not in ["שישי","שבת"] and s in ["16:00–18:00","18:00–20:00","20:00–22:00"])
        for s in SLOTS}
    for d in DAYS_HE
}

for k, v in {
    "manage_section": "overview",
    "show_add_hall": False,
    "edit_coach_idx": None,
    "avail_coach_idx": None,
    "show_add_coach": False,
    "halls": [
        {"name": "אשלים",   "address": "הצמרת 17, ראשון לציון",       "split": True},
        {"name": "רוזן",    "address": "מנחם בגין 13, ראשון לציון",    "split": True},
        {"name": "נחלת",    "address": "רחוב העצמאות 37, ראשון לציון", "split": True},
        {"name": "גן נחום", "address": "תמר אבן 9, ראשון לציון",       "split": False},
    ],
    "coaches": [
        {"name": "יוסי כהן",  "role": "מאמן ראשי",  "email": "yossi@hapoel.com",  "phone": "050-111-2233", "avail": default_avail},
        {"name": "מיכל לוי",  "role": "מאמנת ראשית","email": "michal@hapoel.com",  "phone": "050-222-3344", "avail": default_avail},
        {"name": "דני אברהם", "role": "עוזר מאמן",   "email": "danny@hapoel.com",   "phone": "050-333-4455", "avail": default_avail},
        {"name": "שרה גולן",  "role": "מאמנת נוער",  "email": "sara@hapoel.com",    "phone": "050-444-5566", "avail": default_avail},
        {"name": "רון שפירא", "role": "מאמן שוערים", "email": "ron@hapoel.com",     "phone": "050-555-6677", "avail": default_avail},
    ],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── פונקציית ניווט עליון ──────────────────────────────────────────────────────
def top_nav(back_label=None, back_section="overview"):
    col_home, col_back, col_space, col_logo = st.columns([1.2, 2, 5, 0.8])
    with col_home:
        if st.button("🏠 בית", key=f"home_{back_section}"):
            st.switch_page("app.py")
    if back_label:
        with col_back:
            if st.button(f"← {back_label}", key=f"back_{back_section}"):
                st.session_state.manage_section = back_section
                st.session_state.edit_coach_idx = None
                st.session_state.avail_coach_idx = None
                st.session_state.show_add_coach = False
                st.rerun()
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
    st.markdown("<hr class='div'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 1 – סקירה כללית
# ════════════════════════════════════════════════════════════════════
if st.session_state.manage_section == "overview":
    top_nav()
    st.markdown("<div style='font-size:30px;font-weight:900;text-align:center;color:#0f172a;margin-bottom:6px;'>ניהול נתונים</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:15px;color:#94a3b8;text-align:center;margin-bottom:36px;'>בחר ישות לצפייה וניהול</div>", unsafe_allow_html=True)

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

    c1, c2, c3 = st.columns(3)
    circle_card(c1, "🏢", "אולמות",  4,   "#f3e8ff", "#7c3aed", "#ede9fe", "halls_management")
    circle_card(c2, "👥", "קבוצות",  15,  "#dbeafe", "#1d4ed8", "#eff6ff", "teams_management")
    circle_card(c3, "👨‍🏫", "מאמנים", len(st.session_state.coaches), "#dcfce7", "#15803d", "#f0fdf4", "coaches_management")
    st.write("##")
    _, c4, c5, _ = st.columns([1,2,2,1])
    circle_card(c4, "🏃", "שחקנים", 421, "#ffedd5", "#c2410c", "#fff7ed", "players_management")
    circle_card(c5, "💼", "מנהלים", 12,  "#fef9c3", "#a16207", "#fefce8", "managers_management")
    st.markdown("<div style='text-align:center;color:#cbd5e1;font-size:13px;margin-top:24px;'>לחץ על ישות כדי לנהל את הנתונים שלה</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסך 2 – ניהול אולמות
# ════════════════════════════════════════════════════════════════════
elif st.session_state.manage_section == "halls_management":
    top_nav("ניהול נתונים", "overview")

    col_title, col_add = st.columns([7, 2])
    with col_title:
        st.markdown("<div class='page-title-lg'>ניהול <span>אולמות</span></div><div class='page-sub'>הגדר מתקני אימון ויכולות פיצול מגרש</div>", unsafe_allow_html=True)
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
            col_n, col_a = st.columns(2)
            with col_n:
                st.markdown("<div class='form-lbl'>שם האולם</div>", unsafe_allow_html=True)
                new_name = st.text_input("שם", placeholder="למשל: אשלים", label_visibility="collapsed")
            with col_a:
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
            <div class='coach-card' style='border-right:5px solid #7c3aed;'>
                <div style='display:flex;align-items:center;gap:16px;'>
                    <div style='font-size:32px;color:#94a3b8;'>🏢</div>
                    <div>
                        <div style='display:flex;align-items:center;gap:10px;'>
                            <span style='font-size:18px;font-weight:800;color:#0f172a;'>{hall['name']}</span>
                            <span style='background:{tag_bg};color:{tag_clr};border-radius:20px;padding:2px 12px;font-size:12px;font-weight:700;'>{tag_txt}</span>
                        </div>
                        <div class='coach-detail'>📍 {hall['address']}</div>
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

# ════════════════════════════════════════════════════════════════════
# מסך 3 – ניהול מאמנים
# ════════════════════════════════════════════════════════════════════
elif st.session_state.manage_section == "coaches_management":
    top_nav("ניהול נתונים", "overview")

    col_title, col_add = st.columns([7, 2])
    with col_title:
        st.markdown("<div class='page-title-lg'>ניהול <span>מאמנים</span></div><div class='page-sub'>נהל סגל מאמנים וזמינות שבועית</div>", unsafe_allow_html=True)
    with col_add:
        st.markdown('<div class="red-btn" style="margin-top:8px;">', unsafe_allow_html=True)
        if st.button("＋ הוסף מאמן חדש", use_container_width=True, key="add_coach_btn"):
            st.session_state.show_add_coach = not st.session_state.show_add_coach
            st.session_state.edit_coach_idx = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # ── טופס עריכה / הוספה ───────────────────────────────────────────
    edit_idx = st.session_state.edit_coach_idx
    show_add = st.session_state.show_add_coach

    if show_add or edit_idx is not None:
        is_edit = edit_idx is not None
        coach_data = st.session_state.coaches[edit_idx] if is_edit else {}
        form_title = "עריכת מאמן" if is_edit else "הוספת מאמן חדש"

        with st.container(border=True):
            st.markdown(f"<div style='font-size:20px;font-weight:800;margin-bottom:16px;'>{form_title}</div>", unsafe_allow_html=True)
            col_n, col_r = st.columns(2)
            with col_n:
                st.markdown("<div class='form-lbl'>שם מלא</div>", unsafe_allow_html=True)
                f_name = st.text_input("שם", value=coach_data.get("name",""), placeholder="למשל: יוסי כהן", label_visibility="collapsed")
            with col_r:
                st.markdown("<div class='form-lbl'>תפקיד</div>", unsafe_allow_html=True)
                roles = ["מאמן ראשי","מאמנת ראשית","עוזר מאמן","מאמן שוערים","מאמן נוער","מאמנת נוער"]
                curr_role = coach_data.get("role","מאמן ראשי")
                f_role = st.selectbox("תפקיד", roles, index=roles.index(curr_role) if curr_role in roles else 0, label_visibility="collapsed")
            col_e, col_p = st.columns(2)
            with col_e:
                st.markdown("<div class='form-lbl'>אימייל</div>", unsafe_allow_html=True)
                f_email = st.text_input("אימייל", value=coach_data.get("email",""), placeholder="coach@hapoel.com", label_visibility="collapsed")
            with col_p:
                st.markdown("<div class='form-lbl'>טלפון</div>", unsafe_allow_html=True)
                f_phone = st.text_input("טלפון", value=coach_data.get("phone",""), placeholder="050-000-0000", label_visibility="collapsed")
            st.write("")
            cc, cs = st.columns(2)
            with cc:
                st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                if st.button("ביטול", use_container_width=True, key="cancel_coach"):
                    st.session_state.show_add_coach = False
                    st.session_state.edit_coach_idx = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with cs:
                btn_label = "עדכן מאמן" if is_edit else "הוסף מאמן"
                st.markdown('<div class="save-btn">', unsafe_allow_html=True)
                if st.button(btn_label, use_container_width=True, key="save_coach"):
                    if f_name.strip():
                        entry = {"name": f_name.strip(), "role": f_role, "email": f_email.strip(), "phone": f_phone.strip(), "avail": coach_data.get("avail", {d: {s: False for s in SLOTS} for d in DAYS_HE})}
                        if is_edit:
                            st.session_state.coaches[edit_idx] = entry
                            st.success(f"✅ פרטי {f_name} עודכנו!")
                        else:
                            st.session_state.coaches.append(entry)
                            st.success(f"✅ המאמן {f_name} נוסף!")
                        st.session_state.show_add_coach = False
                        st.session_state.edit_coach_idx = None
                        st.rerun()
                    else:
                        st.error("נא להזין שם מאמן")
                st.markdown('</div>', unsafe_allow_html=True)
        st.write("")

    # ── כרטיסי מאמנים ────────────────────────────────────────────────
    for i, coach in enumerate(st.session_state.coaches):
        col_card, col_avail, col_edit, col_del = st.columns([6, 2.5, 0.5, 0.5])
        with col_card:
            st.markdown(f"""
            <div class='coach-card'>
                <div style='display:flex;align-items:center;gap:16px;'>
                    <div class='coach-avatar'>👤</div>
                    <div>
                        <div class='coach-name'>{coach['name']}</div>
                        <span class='coach-role-tag'>{coach['role']}</span>
                        <div class='coach-detail'>✉️ {coach.get('email','—')}</div>
                        <div class='coach-detail'>📞 {coach.get('phone','—')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_avail:
            st.write("")
            st.markdown('<div class="avail-btn">', unsafe_allow_html=True)
            if st.button(f"📅 ניהול זמינות\nקבע לוח שבועי", key=f"avail_{i}", use_container_width=True):
                st.session_state.avail_coach_idx = i
                st.session_state.manage_section = "coach_availability"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_edit:
            st.write("")
            if st.button("✏️", key=f"edit_c_{i}"):
                st.session_state.edit_coach_idx = i
                st.session_state.show_add_coach = False
                st.rerun()
        with col_del:
            st.write("")
            if st.button("🗑️", key=f"del_c_{i}"):
                st.session_state.coaches.pop(i); st.rerun()

# ════════════════════════════════════════════════════════════════════
# מסך 4 – זמינות שבועית של מאמן
# ════════════════════════════════════════════════════════════════════
elif st.session_state.manage_section == "coach_availability":
    idx = st.session_state.avail_coach_idx
    coach = st.session_state.coaches[idx]

    top_nav("ניהול מאמנים", "coaches_management")

    st.markdown(f"<div class='page-title-lg'>זמינות שבועית – <span>{coach['name']}</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>סמן את המשבצות הפנויות. משבצות לא מסומנות יהפכו לאילוצים קבועים.</div>", unsafe_allow_html=True)
    st.write("")

    # סיכום זמינות
    avail = coach["avail"]
    free_count = sum(1 for d in DAYS_HE for s in SLOTS if avail.get(d,{}).get(s,False))
    total = len(DAYS_HE) * len(SLOTS)

    col_info, col_badge = st.columns([6,1])
    with col_info:
        st.markdown("<div style='font-weight:700;font-size:16px;'>בחר מאמן</div>", unsafe_allow_html=True)
        coaches_names = [c["name"] for c in st.session_state.coaches]
        chosen = st.selectbox("מאמן", coaches_names, index=idx, label_visibility="collapsed")
        if chosen != coach["name"]:
            new_idx = coaches_names.index(chosen)
            st.session_state.avail_coach_idx = new_idx
            st.rerun()
    with col_badge:
        st.markdown(f"""
            <div style='background:#eff6ff;color:#1d4ed8;border-radius:12px;padding:10px 16px;
                        text-align:center;font-weight:700;font-size:15px;margin-top:4px;'>
                {free_count} / {total}<br>
                <span style='font-size:11px;font-weight:400;'>משבצות פנויות</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ── גריד זמינות ──────────────────────────────────────────────────
    new_avail = {d: {} for d in DAYS_HE}
    header_cols = st.columns([1.5] + [1]*7)
    header_cols[0].markdown("<div style='font-size:11px;font-weight:700;color:#94a3b8;letter-spacing:1px;'>משבצת זמן</div>", unsafe_allow_html=True)
    for j, d in enumerate(DAYS_HE):
        color = "#7c3aed" if d == "שישי" else "#0f172a"
        header_cols[j+1].markdown(f"<div style='text-align:center;font-size:12px;font-weight:700;color:{color};'>{d}</div>", unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    for s in SLOTS:
        row_cols = st.columns([1.5] + [1]*7)
        row_cols[0].markdown(f"<div style='font-size:13px;font-weight:600;color:#475569;padding-top:6px;'>{s}</div>", unsafe_allow_html=True)
        for j, d in enumerate(DAYS_HE):
            curr = avail.get(d,{}).get(s, False)
            val = row_cols[j+1].checkbox("", value=curr, key=f"slot_{idx}_{d}_{s}", label_visibility="collapsed")
            new_avail[d][s] = val

    st.write("")
    col_save, _ = st.columns([2,5])
    with col_save:
        st.markdown('<div class="save-btn">', unsafe_allow_html=True)
        if st.button("💾 שמור זמינות", use_container_width=True, key="save_avail"):
            st.session_state.coaches[idx]["avail"] = new_avail
            st.success(f"✅ זמינות {coach['name']} נשמרה!")
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# מסכים נוספים – קבוצות / שחקנים / מנהלים
# ════════════════════════════════════════════════════════════════════
else:
    section = st.session_state.manage_section
    titles = {
        "teams_management":    ("קבוצות",  "רשימת הקבוצות הפעילות במועדון"),
        "players_management":  ("שחקנים",  "421 שחקנים ושחקניות רשומים"),
        "managers_management": ("מנהלים",  "מנהלי קבוצות ואחראים"),
    }
    title, sub = titles.get(section, ("ניהול",""))
    top_nav("ניהול נתונים", "overview")
    st.markdown(f"<div class='page-title-lg'>ניהול <span>{title}</span></div><div class='page-sub'>{sub}</div>", unsafe_allow_html=True)
    st.write("")

    if section == "teams_management":
        teams = [
            {"name":"בוגרים גברים א׳","league":"ליגת העל","trainings":4,"color":"#d90429"},
            {"name":"בוגרות נשים א׳","league":"ליגת העל נשים","trainings":3,"color":"#d90429"},
            {"name":"נערים א׳ צפון","league":"ליגה ארצית","trainings":3,"color":"#1d4ed8"},
            {"name":"נערות א׳","league":"ליגה ארצית נשים","trainings":3,"color":"#1d4ed8"},
            {"name":"ילדים ז׳ 1","league":"ליגה מחוזית","trainings":2,"color":"#15803d"},
        ]
        for t in teams:
            st.markdown(f"""<div class='coach-card' style='border-right:5px solid {t["color"]};'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div><div style='font-size:17px;font-weight:800;color:#0f172a;'>{t['name']}</div>
                    <div class='coach-detail'>{t['league']}</div></div>
                    <span style='background:#f1f5f9;color:#475569;border-radius:20px;padding:4px 14px;font-size:13px;font-weight:700;'>{t['trainings']} אימונים/שבוע</span>
                </div></div>""", unsafe_allow_html=True)
        if st.button("＋ הוסף קבוצה חדשה", use_container_width=True):
            st.info("יושם בשלב ב׳ עם חיבור לבסיס הנתונים")

    elif section == "players_management":
        col_s, col_f = st.columns(2)
        with col_s: st.text_input("🔍 חיפוש לפי שם")
        with col_f: st.selectbox("סנן לפי קבוצה", ["הכל","בוגרים","נוער","ילדים"])
        st.info("רשימת השחקנים המלאה תוצג לאחר חיבור מסד הנתונים בשלב ב׳")

    elif section == "managers_management":
        managers = [
            {"name":"אבי פרידמן","team":"בוגרים גברים א׳"},
            {"name":"רות שמיר","team":"בוגרות נשים א׳"},
            {"name":"נועם כץ","team":"נערים א׳ צפון"},
            {"name":"ליאת בן דוד","team":"נערות א׳"},
        ]
        for m in managers:
            st.markdown(f"""<div class='coach-card' style='border-right:5px solid #a16207;'>
                <div style='font-size:16px;font-weight:800;color:#0f172a;'>{m['name']}</div>
                <div class='coach-detail'>אחראי: {m['team']}</div></div>""", unsafe_allow_html=True)
        if st.button("＋ הוסף מנהל חדש", use_container_width=True):
            st.info("יושם בשלב ב׳ עם חיבור לבסיס הנתונים")
