"""
pages/3_Schedule.py
Weekly training schedule – read-only view with hall / team / coach filter.
"""
import streamlit as st
from utils import apply_global_css, show_logo_header

st.set_page_config(
    page_title="לוח אימונים שבועי – הפועל ראשון לציון",
    page_icon="📋",
    layout="wide",
)
apply_global_css()

# ── Back button ───────────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🏠 בית"):
        st.switch_page("app.py")

show_logo_header("לוח האימונים השבועי", "תצוגת השיבוץ לשבוע הנוכחי")
st.write("##")

# ── Filter bar ────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    view_mode = st.selectbox(
        "תצוגה לפי",
        ["קבוצה", "אולם", "מאמן"],
    )
with col_f2:
    options_map = {
        "קבוצה": ["הכל", "בוגרים גברים א׳", "בוגרות נשים א׳",
                  "נערים א׳ צפון", "נערות א׳", "ילדים ז׳ 1"],
        "אולם":  ["הכל", "אשלים", "רוזן", "נחלת", "גן נחום"],
        "מאמן":  ["הכל", "יוסי כהן", "מיכל לוי", "דני אברהם",
                  "שרה גולן", "רון שפירא"],
    }
    selected_filter = st.selectbox(
        f"בחר {view_mode}",
        options_map[view_mode],
    )
with col_f3:
    week_label = st.selectbox(
        "שבוע",
        ["שבוע נוכחי", "שבוע הבא", "שבוע קודם"],
    )

st.write("---")

# ── Sample schedule data ──────────────────────────────────────────────────────
SCHEDULE = [
    # day,       hall,        team,                coach,           start,  end,    half_court
    ("ראשון",   "אשלים",     "בוגרים גברים א׳",   "יוסי כהן",     "18:00","19:30", False),
    ("ראשון",   "אשלים",     "נערים א׳ צפון",      "דני אברהם",    "16:00","17:15", False),
    ("ראשון",   "רוזן",      "נערות א׳",           "שרה גולן",     "16:30","17:45", True),
    ("שני",     "נחלת",      "בוגרות נשים א׳",     "מיכל לוי",     "19:00","20:15", True),
    ("שני",     "אשלים",     "ילדים ז׳ 1",         "דני אברהם",    "16:00","17:00", True),
    ("שלישי",  "אשלים",     "בוגרים גברים א׳",   "יוסי כהן",     "18:00","19:30", False),
    ("שלישי",  "גן נחום",   "נערים א׳ צפון",      "דני אברהם",    "16:30","17:45", False),
    ("רביעי",  "רוזן",      "בוגרות נשים א׳",     "מיכל לוי",     "19:00","20:15", True),
    ("רביעי",  "נחלת",      "נערות א׳",           "שרה גולן",     "17:00","18:15", False),
    ("חמישי",  "אשלים",     "בוגרים גברים א׳",   "יוסי כהן",     "18:30","20:00", False),
    ("חמישי",  "גן נחום",   "ילדים ז׳ 1",         "דני אברהם",    "16:00","17:00", True),
    ("חמישי",  "אשלים",     "נערים א׳ צפון",      "דני אברהם",    "16:00","17:15", True),
]

DAYS_ORDER = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

# Apply filter
def matches(row):
    day, hall, team, coach, *_ = row
    if selected_filter == "הכל":
        return True
    if view_mode == "קבוצה":
        return team == selected_filter
    if view_mode == "אולם":
        return hall == selected_filter
    if view_mode == "מאמן":
        return coach == selected_filter
    return True

filtered = [r for r in SCHEDULE if matches(r)]

# ── Day-by-day columns ────────────────────────────────────────────────────────
days_present = [d for d in DAYS_ORDER if any(r[0] == d for r in filtered)]

if not days_present:
    st.info("אין אימונים מתוכננים עם הסינון הנוכחי.")
else:
    cols = st.columns(len(days_present))
    for col, day in zip(cols, days_present):
        with col:
            st.markdown(
                f"<div style='background:#f8f9fa; border-radius:10px; "
                f"padding:10px; text-align:center;'>"
                f"<strong style='color:#d90429; font-size:15px;'>יום {day}</strong>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.write("")
            day_sessions = [r for r in filtered if r[0] == day]
            day_sessions.sort(key=lambda r: r[4])  # sort by start time

            for row in day_sessions:
                _, hall, team, coach, start, end, half_court = row
                border_color = "#f59e0b" if half_court else "#d90429"
                half_label   = "½ מגרש" if half_court else "מגרש מלא"
                st.markdown(
                    f"""
                    <div style="background:white; border-right:4px solid {border_color};
                                border-radius:8px; padding:10px 12px; margin-bottom:8px;
                                box-shadow:0 1px 3px rgba(0,0,0,0.08);">
                        <div style="font-weight:bold; font-size:13px;">{team}</div>
                        <div style="color:#64748b; font-size:12px;">
                            🕐 {start} – {end}
                        </div>
                        <div style="color:#64748b; font-size:12px;">🏢 {hall}</div>
                        <div style="color:#64748b; font-size:12px;">👨‍🏫 {coach}</div>
                        <div style="margin-top:4px;">
                            <span style="background:{border_color}22; color:{border_color};
                                         border-radius:4px; padding:1px 6px; font-size:11px;
                                         font-weight:bold;">
                                {half_label}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ── Summary footer ────────────────────────────────────────────────────────────
st.write("---")
total = len(filtered)
half_count = sum(1 for r in filtered if r[6])
full_count  = total - half_count

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    st.metric("סה״כ אימונים", total)
with col_s2:
    st.metric("מגרש מלא", full_count)
with col_s3:
    st.metric("חצי מגרש", half_count)
with col_s4:
    # quality badge
    st.markdown(
        "<div style='background:#22c55e22; border:1px solid #22c55e; "
        "border-radius:8px; padding:8px 12px; text-align:center;'>"
        "<div style='color:#22c55e; font-weight:bold; font-size:22px;'>87</div>"
        "<div style='color:gray; font-size:12px;'>ציון איכות</div>"
        "</div>",
        unsafe_allow_html=True,
    )

st.write("##")
col_export, col_rerun = st.columns([1, 1])
with col_export:
    if st.button("📄 ייצא לקובץ PDF"):
        st.info("ייצוא PDF יהיה זמין בשלב ב׳")
with col_rerun:
    if st.button("🔄 הרץ אופטימיזציה מחדש"):
        st.switch_page("pages/2_Optimization.py")
