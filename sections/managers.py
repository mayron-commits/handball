"""
sections/managers.py
ניהול מנהלי קבוצות – רשימה, הוספה, עריכה
מקושר ל: dim_team_manager + dim_human
"""
import streamlit as st
from sections.shared import top_nav, page_header
from sections.db_data import MANAGERS_SAMPLE, TEAMS_DB, TEAM_NAMES


def init_state():
    for k, v in {
        "managers":         [m.copy() for m in MANAGERS_SAMPLE],
        "show_add_manager": False,
        "edit_manager_idx": None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _manager_form(title, data, save_key, cancel_key):
    team_options = ["—"] + [t["name"] for t in TEAMS_DB if t["active"]]

    with st.container(border=True):
        st.markdown(
            f"<div style='font-size:20px;font-weight:800;margin-bottom:18px;'>{title}</div>",
            unsafe_allow_html=True,
        )

        # שורה 1 – שם + קבוצה
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='form-lbl'>שם מלא</div>", unsafe_allow_html=True)
            f_name = st.text_input("שם", value=data.get("name",""),
                                   placeholder="שם פרטי ושם משפחה",
                                   label_visibility="collapsed", key=f"mn_{save_key}")
        with c2:
            st.markdown("<div class='form-lbl'>קבוצה אחראית</div>", unsafe_allow_html=True)
            curr_team = TEAM_NAMES.get(data.get("team_key"), "—")
            f_team = st.selectbox("קבוצה", team_options,
                                   index=team_options.index(curr_team) if curr_team in team_options else 0,
                                   label_visibility="collapsed", key=f"mt_{save_key}")

        # שורה 2 – מייל + טלפון
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("<div class='form-lbl'>אימייל</div>", unsafe_allow_html=True)
            f_email = st.text_input("אימייל", value=data.get("email",""),
                                    placeholder="manager@hapoel.com",
                                    label_visibility="collapsed", key=f"me_{save_key}")
        with c4:
            st.markdown("<div class='form-lbl'>טלפון</div>", unsafe_allow_html=True)
            f_phone = st.text_input("טלפון", value=data.get("phone",""),
                                    placeholder="050-000-0000",
                                    label_visibility="collapsed", key=f"mp_{save_key}")

        f_active = st.checkbox("פעיל/ה", value=data.get("active", True), key=f"ma_{save_key}")

        st.write("")
        cb, cs = st.columns(2)
        with cb:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("ביטול", use_container_width=True, key=f"mcancel_{cancel_key}"):
                st.session_state.show_add_manager = False
                st.session_state.edit_manager_idx = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cs:
            btn = "עדכן מנהל" if data else "הוסף מנהל"
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button(btn, use_container_width=True, key=f"msave_{save_key}"):
                if f_name.strip():
                    team_key = next((t["team_key"] for t in TEAMS_DB if t["name"] == f_team), None)
                    return {
                        "manager_key": data.get("manager_key", 8000 + len(st.session_state.managers)),
                        "name":        f_name.strip(),
                        "team_key":    team_key,
                        "email":       f_email.strip(),
                        "phone":       f_phone.strip(),
                        "active":      f_active,
                    }
                else:
                    st.error("נא להזין שם מנהל/ת")
            st.markdown('</div>', unsafe_allow_html=True)
    return None


def render():
    init_state()
    top_nav("ניהול נתונים", "overview")
    page_header("ניהול", "מנהלי קבוצות",
                "מנהלי ואחראי הקבוצות במועדון",
                "הוסף מנהל/ת", "add_manager_btn", "show_add_manager")

    # ── טפסים ────────────────────────────────────────────────────────
    edit_idx = st.session_state.edit_manager_idx

    if edit_idx is not None:
        result = _manager_form("עריכת מנהל/ת",
                                st.session_state.managers[edit_idx],
                                f"edit_m_{edit_idx}", f"edit_m_{edit_idx}")
        if result:
            st.session_state.managers[edit_idx] = result
            st.session_state.edit_manager_idx   = None
            st.success(f"✅ פרטי {result['name']} עודכנו!")
            st.rerun()
        st.write("")

    elif st.session_state.show_add_manager:
        result = _manager_form("הוספת מנהל/ת חדש/ה", {}, "new_manager", "new_manager")
        if result:
            st.session_state.managers.append(result)
            st.session_state.show_add_manager = False
            st.success(f"✅ {result['name']} נוסף/ה!")
            st.rerun()
        st.write("")

    # ── רשימת מנהלים ─────────────────────────────────────────────────
    managers = st.session_state.managers
    if not managers:
        st.markdown(
            "<div style='text-align:center;padding:40px;color:#94a3b8;'>אין מנהלים רשומים</div>",
            unsafe_allow_html=True,
        )
        return

    for i, mgr in enumerate(managers):
        team_name  = TEAM_NAMES.get(mgr.get("team_key"), "—")
        active_clr = "#a16207" if mgr.get("active", True) else "#94a3b8"
        tag_bg     = "#fef9c3" if mgr.get("active", True) else "#f1f5f9"

        col_card, col_edit, col_del = st.columns([10, 0.6, 0.6])
        with col_card:
            st.markdown(
                f"""
                <div class='data-card' style='border-right:5px solid #a16207;'>
                    <div style='display:flex;align-items:center;justify-content:space-between;'>
                        <div style='display:flex;align-items:center;gap:16px;'>
                            <div style='width:52px;height:52px;border-radius:50%;
                                        background:#fef9c3;display:flex;align-items:center;
                                        justify-content:center;font-size:24px;'>💼</div>
                            <div>
                                <div style='font-size:18px;font-weight:800;color:#0f172a;'>
                                    {mgr['name']}
                                    {"" if mgr.get("active",True) else
                                     " <span style='font-size:12px;color:#94a3b8;'>(לא פעיל)</span>"}
                                </div>
                                <div style='margin-top:4px;'>
                                    <span class='tag' style='background:{tag_bg};color:{active_clr};'>
                                        {team_name}
                                    </span>
                                </div>
                                <div style='font-size:13px;color:#64748b;margin-top:6px;'>
                                    ✉️ {mgr.get('email','—')} &nbsp;&nbsp;
                                    📞 {mgr.get('phone','—')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_edit:
            if st.button("✏️", key=f"em_{i}"):
                st.session_state.edit_manager_idx = i
                st.session_state.show_add_manager = False
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"dm_{i}"):
                deleted = st.session_state.managers.pop(i)
                st.toast(f"'{deleted['name']}' הוסר/ה")
                st.rerun()
