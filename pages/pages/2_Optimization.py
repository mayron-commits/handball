"""
pages/2_Optimization.py
Optimization engine – add constraints and run the scheduling algorithm.
"""
import streamlit as st
from utils import apply_global_css, show_logo_header

st.set_page_config(
    page_title="מנוע אופטימיזציה – הפועל ראשון לציון",
    page_icon="📅",
    layout="wide",
)
apply_global_css()

# ── Back button ───────────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🏠 בית"):
        st.switch_page("app.py")

show_logo_header("מנוע אופטימיזציה", "הוספת אילוצים והרצת האלגוריתם")
st.write("##")

# ── Initialise constraint queue in session state ──────────────────────────────
if "constraints" not in st.session_state:
    st.session_state["constraints"] = []

# ── Layout: two main action buttons ──────────────────────────────────────────
col_a, col_b = st.columns(2)
with col_a:
    add_clicked = st.button("➕ הוספת אילוץ")
with col_b:
    run_clicked = st.button("🚀 הרץ אופטימיזציה")

st.write("---")

# ── Add-constraint form (toggles open on button click) ───────────────────────
if "show_constraint_form" not in st.session_state:
    st.session_state["show_constraint_form"] = False

if add_clicked:
    st.session_state["show_constraint_form"] = not st.session_state["show_constraint_form"]

if st.session_state["show_constraint_form"]:
    st.markdown("### ➕ הוספת אילוץ חדש")
    with st.container(border=True):
        entity_type = st.radio(
            "סוג ישות",
            ["קבוצה", "אולם", "מאמן"],
            horizontal=True,
        )

        # Dynamic entity selector based on type
        entity_options = {
            "קבוצה": ["בוגרים גברים א׳", "בוגרות נשים א׳", "נערים א׳ צפון",
                      "נערות א׳", "ילדים ז׳ 1"],
            "אולם":  ["אשלים", "רוזן", "נחלת", "גן נחום"],
            "מאמן":  ["יוסי כהן", "מיכל לוי", "דני אברהם", "שרה גולן", "רון שפירא"],
        }
        entity_name = st.selectbox(
            f"בחר {entity_type}",
            entity_options[entity_type],
        )

        col_date, col_start, col_end = st.columns(3)
        with col_date:
            constraint_date = st.date_input("תאריך האילוץ")
        with col_start:
            start_time = st.time_input("משעה", value=None)
        with col_end:
            end_time = st.time_input("עד שעה", value=None)

        constraint_reason = st.text_input(
            "סיבת האילוץ",
            placeholder="למשל: טיול שנתי, שיפוץ, מחלה...",
        )

        col_save, col_cancel = st.columns([1, 3])
        with col_save:
            if st.button("✅ הוסף לתור"):
                entry = {
                    "type": entity_type,
                    "entity": entity_name,
                    "date": str(constraint_date),
                    "start": str(start_time) if start_time else "—",
                    "end":   str(end_time)   if end_time   else "—",
                    "reason": constraint_reason or "—",
                }
                st.session_state["constraints"].append(entry)
                st.session_state["show_constraint_form"] = False
                st.toast("✅ האילוץ נוסף לתור!")
                st.rerun()
        with col_cancel:
            if st.button("ביטול"):
                st.session_state["show_constraint_form"] = False
                st.rerun()

# ── Constraint queue display ──────────────────────────────────────────────────
constraints = st.session_state["constraints"]

st.markdown("### 📋 אילוצים בתור")

if not constraints:
    st.info("אין אילוצים בתור. לחץ על 'הוספת אילוץ' כדי להוסיף.")
else:
    color_map = {"קבוצה": "#3B82F6", "אולם": "#A855F7", "מאמן": "#22C55E"}
    for i, c in enumerate(constraints):
        col_info, col_del = st.columns([10, 1])
        with col_info:
            color = color_map.get(c["type"], "#d90429")
            st.markdown(
                f"""
                <div style="background:white; padding:12px 16px; border-radius:10px;
                            border-right:5px solid {color}; margin-bottom:8px;
                            box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                    <strong style="color:{color};">{c['type']}</strong>:
                    {c['entity']} &nbsp;·&nbsp;
                    <span style="color:#64748b;">{c['date']}</span>
                    &nbsp;{c['start']} – {c['end']}&nbsp;
                    <span style="color:#94a3b8; font-size:12px;">{c['reason']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_del:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state["constraints"].pop(i)
                st.rerun()

    if st.button("🗑️ נקה את כל האילוצים"):
        st.session_state["constraints"] = []
        st.rerun()

# ── Run optimisation ──────────────────────────────────────────────────────────
st.write("---")

if run_clicked:
    with st.spinner("מריץ אלגוריתם שיבוץ..."):
        import time
        time.sleep(1.5)   # placeholder for real solver call

    st.success("✅ השיבוץ הושלם בהצלחה!")
    st.balloons()
    st.markdown(
        "**ציון איכות:** 87 / 100 &nbsp;|&nbsp; "
        "**אימונים שובצו:** 38 / 42 &nbsp;|&nbsp; "
        "**אילוצים קשיחים:** 12 ✔️",
        unsafe_allow_html=False,
    )
    st.info("עבור ללוח האימונים השבועי כדי לצפות בתוצאות המלאות.")
    if st.button("📋 צפה בלוח האימונים"):
        st.switch_page("pages/3_Schedule.py")
