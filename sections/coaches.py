"""
sections/coaches.py
ניהול מאמנים – כרטיסים, הוספה, עריכה, זמינות שבועית
"""
import streamlit as st
import os
from sections.shared import top_nav, page_header

DAYS_HE = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
SLOTS   = ["08:00–10:00", "10:00–12:00", "12:00–14:00",
           "14:00–16:00", "16:00–18:00", "18:00–20:00", "20:00–22:00"]
ROLES   = ["מאמן ראשי", "מאמנת ראשית", "עוזר מאמן", "מאמנת נוער",
           "מאמן נוער", "מאמן שוערים", "מדריך"]

DEFAULT_AVAIL = {
    d: {s: (d not in ["שישי", "שבת"] and s in ["16:00–18:00", "18:00–20:00", "20:00–22:00"])
        for s in SLOTS}
    for d in DAYS_HE
}

DEFAULT_COACHES = [
    {"name": "יוסי כהן",  "role": "מאמן ראשי",   "email": "yossi@hapoel.com",  "phone": "050-111-2233", "avail": DEFAULT_AVAIL},
    {"name": "מיכל לוי",  "role": "מאמנת ראשית", "email": "michal@hapoel.com",  "phone": "050-222-3344", "avail": DEFAULT_AVAIL},
    {"name": "דני אברהם", "role": "עוזר מאמן",   "email": "danny@hapoel.com",   "phone": "050-333-4455", "avail": DEFAULT_AVAIL},
    {"name": "שרה גולן",  "role": "מאמנת נוער",  "email": "sara@hapoel.com",    "phone": "050-444-5566", "avail": DEFAULT_AVAIL},
    {"name": "רון שפירא", "role": "מאמן שוערים", "email": "ron@hapoel.com",     "phone": "050-555-6677", "avail": DEFAULT_AVAIL},
]


def init_state():
    for k, v in {
        "coaches":          DEFAULT_COACHES,
        "show_add_coach":   False,
        "edit_coach_idx":   None,
        "avail_coach_idx":  None,
        "coaches_sub":      "list",   # "list" | "availability"
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── טופס הוספה / עריכה ───────────────────────────────────────────────────────
def _coach_form(title, data, save_key, cancel_key):
    with st.container(border=True):
        st.markdown(
            f"<div style='font-size:20px;font-weight:800;margin-bottom:20px;'>{title}</div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='form-lbl'>שם מלא</div>", unsafe_allow_html=True)
            f_name = st.text_input("שם", value=data.get("name", ""),
                                   placeholder="למשל: יוסי כהן",
                                   label_visibility="collapsed", key=f"cn_{save_key}")
        with c2:
            st.markdown("<div class='form-lbl'>תפקיד</div>", unsafe_allow_html=True)
            curr = data.get("role", ROLES[0])
            f_role = st.selectbox("תפקיד", ROLES,
                                   index=ROLES.index(curr) if curr in ROLES else 0,
                                   label_visibility="collapsed", key=f"cr_{save_key}")
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("<div class='form-lbl'>אימייל</div>", unsafe_allow_html=True)
            f_email = st.text_input("אימייל", value=data.get("email", ""),
                                    placeholder="coach@hapoel.com",
                                    label_visibility="collapsed", key=f"ce_{save_key}")
        with c4:
            st.markdown("<div class='form-lbl'>טלפון</div>", unsafe_allow_html=True)
            f_phone = st.text_input("טלפון", value=data.get("phone", ""),
                                    placeholder="050-000-0000",
                                    label_visibility="collapsed", key=f"cp_{save_key}")
        st.write("")
        cb, cs = st.columns(2)
        with cb:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("ביטול", use_container_width=True, key=f"cancel_{cancel_key}"):
                st.session_state.show_add_coach = False
                st.session_state.edit_coach_idx = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cs:
            btn = "עדכן מאמן" if data else "הוסף מאמן"
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button(btn, use_container_width=True, key=f"save_{save_key}"):
                if f_name.strip():
                    return {
                        "name":  f_name.strip(),
                        "role":  f_role,
                        "email": f_email.strip(),
                        "phone": f_phone.strip(),
                        "avail": data.get("avail", {
                            d: {s: False for s in SLOTS} for d in DAYS_HE
                        }),
                    }
                else:
                    st.error("נא להזין שם מאמן")
            st.markdown('</div>', unsafe_allow_html=True)
    return None


# ── מסך זמינות שבועית ────────────────────────────────────────────────────────
def _render_availability():
    idx   = st.session_state.avail_coach_idx
    coach = st.session_state.coaches[idx]

    # ניווט
    col_home, col_back, col_space, col_logo = st.columns([1.2, 2.5, 4.5, 0.8])
    with col_home:
        if st.button("🏠 בית", key="av_home"):
            st.session_state["manage_section"] = "overview"
            st.switch_page("app.py")
    with col_back:
        if st.button("← ניהול מאמנים", key="av_back"):
            st.session_state.coaches_sub     = "list"
            st.session_state.avail_coach_idx = None
            st.rerun()
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=55)
    st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:16px 0;'>",
                unsafe_allow_html=True)

    # כותרת
    st.markdown(
        f"<div class='page-title-lg'>זמינות שבועית – <span style='font-weight:900'>{coach['name']}</span></div>"
        "<div class='page-sub'>סמני את המשבצות הפנויות. משבצות לא מסומנות = אילוץ קבוע.</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    # בחירת מאמן + badge – אם אין avail נייצר ברירת מחדל
    if "avail" not in coach:
        coach["avail"] = {d: {s: False for s in SLOTS} for d in DAYS_HE}
        st.session_state.coaches[idx] = coach
    avail = coach["avail"]
    free_count = sum(1 for d in DAYS_HE for s in SLOTS if avail.get(d, {}).get(s, False))
    total      = len(DAYS_HE) * len(SLOTS)

    col_sel, col_badge = st.columns([5, 1.2])
    with col_sel:
        st.markdown("<div style='font-weight:700;font-size:15px;margin-bottom:6px;'>בחר מאמן</div>",
                    unsafe_allow_html=True)
        names  = [c["name"] for c in st.session_state.coaches]
        chosen = st.selectbox("מאמן", names, index=idx, label_visibility="collapsed")
        if chosen != coach["name"]:
            st.session_state.avail_coach_idx = names.index(chosen)
            st.rerun()
    with col_badge:
        st.markdown(
            f"<div style='background:#eff6ff;color:#1d4ed8;border-radius:12px;"
            f"padding:12px 16px;text-align:center;font-weight:700;font-size:16px;margin-top:4px;'>"
            f"{free_count} / {total}<br>"
            f"<span style='font-size:11px;font-weight:400;'>משבצות פנויות</span></div>",
            unsafe_allow_html=True,
        )

    st.write("")

    # ── גריד ──────────────────────────────────────────────────────────
    new_avail  = {d: {} for d in DAYS_HE}
    header_row = st.columns([1.8] + [1] * 7)
    header_row[0].markdown(
        "<div style='font-size:11px;font-weight:700;color:#94a3b8;letter-spacing:1px;'>"
        "משבצת זמן</div>",
        unsafe_allow_html=True,
    )
    for j, d in enumerate(DAYS_HE):
        color = "#7c3aed" if d == "שישי" else "#0f172a"
        header_row[j + 1].markdown(
            f"<div style='text-align:center;font-size:12px;font-weight:700;color:{color};'>"
            f"{d}</div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        "<hr style='border:none;border-top:2px solid #e2e8f0;margin:8px 0;'>",
        unsafe_allow_html=True,
    )

    for s in SLOTS:
        row = st.columns([1.8] + [1] * 7)
        row[0].markdown(
            f"<div style='font-size:13px;font-weight:600;color:#475569;padding-top:6px;'>{s}</div>",
            unsafe_allow_html=True,
        )
        for j, d in enumerate(DAYS_HE):
            curr = avail.get(d, {}).get(s, False)
            val  = row[j + 1].checkbox(
                "", value=curr,
                key=f"slot_{idx}_{d}_{s}",
                label_visibility="collapsed",
            )
            new_avail[d][s] = val

    st.write("")
    col_save, _ = st.columns([2, 5])
    with col_save:
        st.markdown('<div class="save-btn">', unsafe_allow_html=True)
        if st.button("💾 שמור זמינות", use_container_width=True, key="save_avail"):
            st.session_state.coaches[idx]["avail"] = new_avail
            st.success(f"✅ זמינות {coach['name']} נשמרה!")
        st.markdown('</div>', unsafe_allow_html=True)


# ── מסך רשימת מאמנים ─────────────────────────────────────────────────────────
def _render_list():
    top_nav("ניהול נתונים", "overview")
    page_header(
        "ניהול", "מאמנים",
        "נהל סגל מאמנים וזמינות שבועית",
        "הוסף מאמן חדש", "add_coach_btn", "show_add_coach",
    )

    edit_idx = st.session_state.edit_coach_idx

    # ── טופס עריכה ────────────────────────────────────────────────────
    if edit_idx is not None:
        result = _coach_form(
            "עריכת מאמן",
            st.session_state.coaches[edit_idx],
            f"edit_{edit_idx}",
            f"edit_{edit_idx}",
        )
        if result:
            st.session_state.coaches[edit_idx] = result
            st.session_state.edit_coach_idx    = None
            st.success(f"✅ פרטי {result['name']} עודכנו!")
            st.rerun()
        st.write("")

    # ── טופס הוספה ────────────────────────────────────────────────────
    elif st.session_state.show_add_coach:
        result = _coach_form("הוספת מאמן חדש", {}, "new_coach", "new_coach")
        if result:
            result["avail"] = {d: {s: False for s in SLOTS} for d in DAYS_HE}
            st.session_state.coaches.append(result)
            st.session_state.show_add_coach = False
            st.success(f"✅ המאמן {result['name']} נוסף!")
            st.rerun()
        st.write("")

    # ── כרטיסי מאמנים ─────────────────────────────────────────────────
    for i, coach in enumerate(st.session_state.coaches):
        avail_data = coach.get("avail", {d: {s: False for s in SLOTS} for d in DAYS_HE})
        free = sum(1 for d in DAYS_HE for s in SLOTS if avail_data.get(d, {}).get(s, False))

        col_avatar, col_info, col_avail, col_edit, col_del = st.columns([0.8, 5, 2.5, 0.5, 0.5])

        with col_avatar:
            st.markdown(
                "<div style='width:56px;height:56px;border-radius:50%;background:#dcfce7;"
                "display:flex;align-items:center;justify-content:center;font-size:24px;"
                "margin-top:12px;'>👤</div>",
                unsafe_allow_html=True,
            )

        with col_info:
            st.markdown(
                f"""
                <div class='data-card' style='padding:16px 20px;'>
                    <div style='font-size:20px;font-weight:800;color:#0f172a;margin-bottom:4px;'>
                        {coach['name']}
                    </div>
                    <span class='tag tag-gray' style='margin-bottom:8px;display:inline-block;'>
                        {coach['role']}
                    </span><br>
                    <div style='font-size:13px;color:#64748b;margin-top:4px;'>
                        ✉️ {coach.get('email','—')}
                    </div>
                    <div style='font-size:13px;color:#64748b;margin-top:2px;'>
                        📞 {coach.get('phone','—')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_avail:
            st.write("")
            st.markdown('<div class="purple-btn">', unsafe_allow_html=True)
            if st.button(
                f"📅 ניהול זמינות\n{free}/{len(DAYS_HE)*len(SLOTS)} משבצות",
                key=f"avail_{i}",
                use_container_width=True,
            ):
                st.session_state.avail_coach_idx = i
                st.session_state.coaches_sub     = "availability"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_edit:
            st.write("")
            st.write("")
            if st.button("✏️", key=f"edit_c_{i}"):
                st.session_state.edit_coach_idx = i
                st.session_state.show_add_coach = False
                st.rerun()

        with col_del:
            st.write("")
            st.write("")
            if st.button("🗑️", key=f"del_c_{i}"):
                deleted = st.session_state.coaches.pop(i)
                st.toast(f"המאמן '{deleted['name']}' הוסר")
                st.rerun()


# ── נקודת כניסה ──────────────────────────────────────────────────────────────
def render():
    init_state()
    if st.session_state.get("coaches_sub") == "availability":
        _render_availability()
    else:
        _render_list()
