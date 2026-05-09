"""
pages/2_Optimization.py
Optimization engine – constraints, retry, solution comparison.
"""
import streamlit as st
import time
import random
from utils import apply_global_css, show_logo_header

st.set_page_config(
    page_title="Optimization Engine – Hapoel RL",
    page_icon="📅",
    layout="wide",
)
apply_global_css()

st.markdown("""
<style>
.run-btn>div>button {
    background-color: #d90429 !important;
    color: white !important;
    border: none !important;
    height: 3.5em !important;
    font-size: 16px !important;
}
.retry-btn>div>button {
    background-color: white !important;
    color: #d90429 !important;
    border: 2px solid #d90429 !important;
    height: 3.5em !important;
}
.confirm-btn>div>button {
    background-color: #16a34a !important;
    color: white !important;
    border: none !important;
    height: 3.5em !important;
}
.solution-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 12px;
}
.solution-card.active  { border-color: #d90429; box-shadow: 0 0 0 3px rgba(217,4,41,0.08); }
.solution-card.prev    { border-color: #94a3b8; opacity: 0.75; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "constraints": [],
    "show_constraint_form": False,
    "optimization_result": None,
    "previous_result": None,
    "show_previous": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def fake_solution(seed=None):
    if seed:
        random.seed(seed)
    score = random.randint(72, 96)
    return {
        "score": score,
        "scheduled": random.randint(34, 42),
        "total": 42,
        "hard_constraints": 14,
        "warnings": random.randint(0, 4),
        "sessions": [
            {"team": "בוגרים גברים א׳", "day": "שני",    "time": "19:00–20:30", "hall": "נחלת",    "warning": False},
            {"team": "בוגרות נשים א׳",  "day": "שני",    "time": "19:00–20:15", "hall": "אשלים",   "warning": False},
            {"team": "נערים א׳ צפון",   "day": "ראשון",  "time": "16:30–17:45", "hall": "רוזן",    "warning": False},
            {"team": "נערות א׳",        "day": "ראשון",  "time": "16:00–17:15", "hall": "גן נחום", "warning": score < 85},
            {"team": "ילדים ז׳ 1",      "day": "שלישי", "time": "16:00–17:00", "hall": "אשלים",   "warning": score < 80},
        ],
    }

# ── Back ──────────────────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🏠 בית"):
        st.switch_page("app.py")

show_logo_header("Optimization Engine", "הוסף אילוצים והרץ את האלגוריתם")
st.write("---")

# ════════════════════════════════════════════════════════════════════
# A – CONSTRAINTS
# ════════════════════════════════════════════════════════════════════
st.markdown("### 🔒 אילוצים")

col_add, col_upload, _ = st.columns([2, 2, 3])
with col_add:
    if st.button("➕ הוסף אילוץ"):
        st.session_state.show_constraint_form = not st.session_state.show_constraint_form
with col_upload:
    uploaded = st.file_uploader("📤 העלה לוח משחקים", type=["xlsx","csv"],
                                 label_visibility="collapsed")
    if uploaded:
        st.success(f"✅ הועלה: {uploaded.name}")

if st.session_state.show_constraint_form:
    with st.container(border=True):
        st.markdown("**אילוץ חדש**")
        entity_type = st.radio("סוג ישות", ["קבוצה","אולם","מאמן"], horizontal=True)
        options_map = {
            "קבוצה": ["בוגרים גברים א׳","בוגרות נשים א׳","נערים א׳ צפון","נערות א׳","ילדים ז׳ 1"],
            "אולם":  ["אשלים","רוזן","נחלת","גן נחום"],
            "מאמן":  ["יוסי כהן","מיכל לוי","דני אברהם","שרה גולן"],
        }
        col_e, col_d = st.columns(2)
        with col_e:
            entity_name = st.selectbox(f"בחר {entity_type}", options_map[entity_type])
        with col_d:
            constraint_date = st.date_input("תאריך")
        col_s, col_en = st.columns(2)
        with col_s:
            start_time = st.time_input("משעה", value=None)
        with col_en:
            end_time = st.time_input("עד שעה", value=None)
        reason = st.text_input("סיבה", placeholder="למשל: טיול שנתי, שיפוץ...")
        c1, c2 = st.columns([1,3])
        with c1:
            if st.button("✅ הוסף לתור"):
                st.session_state.constraints.append({
                    "type": entity_type, "entity": entity_name,
                    "date": str(constraint_date),
                    "start": str(start_time) if start_time else "—",
                    "end":   str(end_time)   if end_time   else "—",
                    "reason": reason or "—",
                })
                st.session_state.show_constraint_form = False
                st.toast("✅ האילוץ נוסף!")
                st.rerun()
        with c2:
            if st.button("ביטול"):
                st.session_state.show_constraint_form = False
                st.rerun()

color_map = {"קבוצה":"#3B82F6","אולם":"#A855F7","מאמן":"#22C55E"}
for i, c in enumerate(st.session_state.constraints):
    color = color_map.get(c["type"], "#d90429")
    col_info, col_del = st.columns([11, 1])
    with col_info:
        st.markdown(
            f"""<div style="background:white; border:1px solid #e2e8f0; border-right:4px solid {color};
                            border-radius:10px; padding:10px 16px; margin-bottom:6px;">
                <strong style="color:{color};">{c['type']}</strong> · <strong>{c['entity']}</strong>
                · <span style="color:#64748b;">{c['date']}</span> · {c['start']} – {c['end']}
                <br/><span style="color:#94a3b8; font-size:12px;">"{c['reason']}"</span>
            </div>""", unsafe_allow_html=True)
    with col_del:
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.constraints.pop(i); st.rerun()

if st.session_state.constraints:
    if st.button("🗑️ נקה הכל"):
        st.session_state.constraints = []; st.rerun()
else:
    st.caption("אין אילוצים בתור.")

st.write("---")

# ════════════════════════════════════════════════════════════════════
# B – RUN / RETRY
# ════════════════════════════════════════════════════════════════════
has_result = st.session_state.optimization_result is not None

col_run, col_retry = st.columns([3, 2])
with col_run:
    st.markdown('<div class="run-btn">', unsafe_allow_html=True)
    run_clicked = st.button("🚀 הרץ אופטימיזציה", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

retry_clicked = False
if has_result:
    with col_retry:
        st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
        retry_clicked = st.button("🔄 נסה פתרון חלופי", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if run_clicked:
    with st.spinner("מריץ אלגוריתם שיבוץ..."):
        time.sleep(1.8)
    if st.session_state.optimization_result:
        st.session_state.previous_result = st.session_state.optimization_result
    st.session_state.optimization_result = fake_solution(seed=random.randint(1,9999))
    st.session_state.show_previous = False
    st.rerun()

if retry_clicked:
    with st.spinner("מחפש פתרון חלופי..."):
        time.sleep(1.4)
    st.session_state.previous_result = st.session_state.optimization_result
    st.session_state.optimization_result = fake_solution(seed=random.randint(1,9999))
    st.session_state.show_previous = False
    st.toast("✅ נמצא פתרון חלופי!")
    st.rerun()

# ════════════════════════════════════════════════════════════════════
# C – RESULTS
# ════════════════════════════════════════════════════════════════════
if st.session_state.optimization_result:
    result = st.session_state.optimization_result
    prev   = st.session_state.previous_result

    st.markdown("### 📊 תוצאות")

    if prev:
        tog = "🙈 הסתר פתרון קודם" if st.session_state.show_previous else "👁️ הצג פתרון קודם"
        if st.button(tog):
            st.session_state.show_previous = not st.session_state.show_previous
            st.rerun()

    def render_card(res, label, extra_class):
        score_color = "#16a34a" if res["score"] >= 85 else "#d90429" if res["score"] < 75 else "#d97706"
        st.markdown(
            f"""<div class="solution-card {extra_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:17px; font-weight:800; margin-bottom:6px;">{label}</div>
                        <div style="color:#64748b; font-size:13px;">
                            {res['scheduled']}/{res['total']} אימונים שובצו &nbsp;·&nbsp;
                            {res['hard_constraints']} אילוצים קשיחים ✔️
                            {"&nbsp;·&nbsp; ⚠️ " + str(res['warnings']) + " אזהרות" if res['warnings'] else ""}
                        </div>
                    </div>
                    <div style="text-align:center;">
                        <div style="width:72px;height:72px;border-radius:50%;
                                    border:5px solid {score_color};
                                    display:flex;align-items:center;justify-content:center;
                                    font-size:24px;font-weight:900;color:{score_color};">
                            {res['score']}
                        </div>
                        <div style="font-size:11px;color:#94a3b8;margin-top:4px;">ציון איכות</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    if st.session_state.show_previous and prev:
        col_cur, col_prev = st.columns(2)
        with col_cur:
            render_card(result, "✅ פתרון נוכחי", "active")
        with col_prev:
            render_card(prev, "⏮️ פתרון קודם", "prev")
    else:
        render_card(result, "✅ פתרון מומלץ", "active")

    # Session list
    st.markdown("**אימונים מתוכננים:**")
    for s in result["sessions"]:
        icon  = "⚠️" if s["warning"] else "✅"
        warn_txt = "&nbsp;·&nbsp; <span style='color:#f59e0b;'>אזהרת שיבוץ</span>" if s["warning"] else ""
        st.markdown(
            f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;
                            padding:10px 16px;margin-bottom:6px;display:flex;gap:12px;align-items:center;">
                <span style="font-size:18px;">{icon}</span>
                <div>
                    <div style="font-weight:700;font-size:14px;">{s['team']}</div>
                    <div style="color:#64748b;font-size:12px;">
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
