"""
pages/3_Schedule.py
Weekly schedule – drag-to-reschedule, conflict detection, confirm changes.
"""
import streamlit as st
import streamlit.components.v1 as components
from utils import apply_global_css, show_logo_header

st.set_page_config(
    page_title="Weekly Schedule – Hapoel RL",
    page_icon="📋",
    layout="wide",
)
apply_global_css()

# ── Back ──────────────────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 8])
with col_btn:
    if st.button("🏠 בית"):
        st.switch_page("app.py")

show_logo_header("לוח האימונים השבועי", "גרור אימונים לשינוי · המערכת תתריע על התנגשויות")
st.write("---")

# ── Filter bar ────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3, col_f4 = st.columns([2, 2, 2, 1])
with col_f1:
    view_mode = st.selectbox("תצוגה לפי", ["לפי קבוצה", "לפי אולם", "לפי מאמן", "סיכום כללי"])
with col_f2:
    week_label = st.selectbox("שבוע", ["שבוע נוכחי (19–25 ינואר)", "שבוע הבא", "שבוע קודם"])
with col_f3:
    hall_filter = st.selectbox("אולם", ["הכל", "אשלים", "רוזן", "נחלת", "גן נחום"])
with col_f4:
    st.write("")
    st.write("")
    show_warnings_only = st.checkbox("⚠️ אזהרות בלבד")

st.write("---")

# ── Pending changes indicator ──────────────────────────────────────────────────
if "pending_changes" not in st.session_state:
    st.session_state.pending_changes = []

if st.session_state.pending_changes:
    n = len(st.session_state.pending_changes)
    col_warn, col_confirm, col_discard = st.columns([4, 2, 1])
    with col_warn:
        st.warning(f"⚡ יש {n} שינוי{'ים' if n>1 else ''} ממתין{'ים' if n>1 else ''} לאישור")
    with col_confirm:
        if st.button("✔️ אשר ושמור שינויים", type="primary"):
            st.session_state.pending_changes = []
            st.success("✅ השינויים נשמרו!")
            st.rerun()
    with col_discard:
        if st.button("↩️ בטל"):
            st.session_state.pending_changes = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════
# DRAG-AND-DROP CALENDAR (HTML component)
# ════════════════════════════════════════════════════════════════════

CALENDAR_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body { background: transparent; direction: rtl; }

  .calendar-wrap { overflow-x: auto; }

  table { width: 100%; border-collapse: collapse; min-width: 680px; }
  th {
    background: #f8fafc; padding: 10px 8px; text-align: center;
    font-size: 13px; font-weight: 700; color: #475569;
    border-bottom: 2px solid #e2e8f0;
  }
  th.time-col { width: 60px; }
  td {
    border: 1px solid #f1f5f9; height: 36px; vertical-align: top;
    position: relative; padding: 2px;
  }
  td.time-label {
    font-size: 11px; color: #94a3b8; text-align: center;
    vertical-align: middle; background: #fafafa; width: 60px;
  }
  td.droppable { transition: background 0.15s; }
  td.droppable.drag-over { background: #fef2f2; }
  td.droppable.drag-over-ok { background: #f0fdf4; }

  .session {
    border-radius: 8px; padding: 5px 8px; font-size: 12px; font-weight: 600;
    cursor: grab; user-select: none; margin: 1px;
    border-left: 4px solid transparent;
    transition: opacity 0.15s, box-shadow 0.15s;
    position: relative;
  }
  .session:active { cursor: grabbing; opacity: 0.7; }
  .session.dragging { opacity: 0.4; }

  .session.type-adult  { background:#fee2e2; border-color:#d90429; color:#991b1b; }
  .session.type-youth  { background:#dbeafe; border-color:#2563eb; color:#1e40af; }
  .session.type-girls  { background:#fce7f3; border-color:#db2777; color:#9d174d; }
  .session.type-kids   { background:#d1fae5; border-color:#059669; color:#065f46; }
  .session.type-match  { background:#fef3c7; border-color:#d97706; color:#92400e; }

  .session .team-name { font-size: 11px; font-weight: 700; }
  .session .session-meta { font-size: 10px; opacity: 0.8; margin-top: 1px; }
  .session .warn-badge {
    position: absolute; top: 3px; left: 6px;
    font-size: 11px;
  }

  /* Conflict toast */
  #conflict-toast {
    display: none;
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: #d90429; color: white; padding: 12px 24px;
    border-radius: 10px; font-size: 14px; font-weight: 700;
    z-index: 9999; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    animation: slideUp 0.3s ease;
  }
  #conflict-toast.success { background: #16a34a; }
  @keyframes slideUp { from { opacity:0; bottom:0; } to { opacity:1; bottom:20px; } }

  #change-log {
    margin-top: 16px; padding: 12px 16px;
    background: #fffbeb; border: 1px solid #fcd34d;
    border-radius: 10px; font-size: 13px; display: none;
  }
  #change-log h4 { font-size: 13px; margin-bottom: 8px; color: #92400e; }
  #change-log li { margin-bottom: 4px; color: #451a03; }

  .legend { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; font-size: 12px; color: #64748b; }
  .legend-item { display: flex; align-items: center; gap: 5px; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; }
</style>
</head>
<body>

<div class="calendar-wrap">
<table id="schedule-table">
<thead>
  <tr>
    <th class="time-col">שעה</th>
    <th>ראשון<br/><small style="font-weight:400;color:#94a3b8;">18 ינואר</small></th>
    <th>שני<br/><small style="font-weight:400;color:#94a3b8;">19 ינואר</small></th>
    <th>שלישי<br/><small style="font-weight:400;color:#94a3b8;">20 ינואר</small></th>
    <th>רביעי<br/><small style="font-weight:400;color:#94a3b8;">21 ינואר</small></th>
    <th>חמישי<br/><small style="font-weight:400;color:#94a3b8;">22 ינואר</small></th>
    <th>שישי<br/><small style="font-weight:400;color:#94a3b8;">23 ינואר</small></th>
  </tr>
</thead>
<tbody id="cal-body">
</tbody>
</table>
</div>

<div id="change-log">
  <h4>⚡ שינויים ממתינים לאישור:</h4>
  <ul id="change-list"></ul>
</div>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#d90429"></div> בוגרים</div>
  <div class="legend-item"><div class="legend-dot" style="background:#2563eb"></div> נוער בנים</div>
  <div class="legend-item"><div class="legend-dot" style="background:#db2777"></div> נוער בנות</div>
  <div class="legend-item"><div class="legend-dot" style="background:#059669"></div> ילדים</div>
  <div class="legend-item"><div class="legend-dot" style="background:#d97706"></div> משחק</div>
  <div class="legend-item">⚠️ אזהרת שיבוץ</div>
</div>

<div id="conflict-toast"></div>

<script>
const HOURS = ['14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30',
               '18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30'];
const DAYS  = ['sun','mon','tue','wed','thu','fri'];
const DAY_NAMES = {sun:'ראשון', mon:'שני', tue:'שלישי', wed:'רביעי', thu:'חמישי', fri:'שישי'};

// Initial sessions data
let sessions = [
  {id:'s1', team:'בוגרים גברים א׳', hall:'נחלת',    type:'adult', day:'mon', hour:'19:00', duration:2, warn:false},
  {id:'s2', team:'בוגרות נשים א׳',  hall:'אשלים',   type:'girls', day:'mon', hour:'19:00', duration:2, warn:false},
  {id:'s3', team:'נערים א׳ צפון',   hall:'רוזן',    type:'youth', day:'sun', hour:'16:30', duration:2, warn:false},
  {id:'s4', team:'נערות א׳',        hall:'גן נחום',  type:'girls', day:'sun', hour:'16:00', duration:2, warn:true},
  {id:'s5', team:'ילדים ז׳ 1',      hall:'אשלים',   type:'kids',  day:'tue', hour:'16:00', duration:2, warn:false},
  {id:'s6', team:'בוגרים גברים א׳', hall:'אשלים',   type:'adult', day:'wed', hour:'19:30', duration:2, warn:false},
  {id:'s7', team:'נערים ט׳',        hall:'רוזן',    type:'youth', day:'thu', hour:'17:00', duration:2, warn:false},
  {id:'s8', team:'משחק – הפועל ת״א',hall:'נחלת',   type:'match', day:'fri', hour:'18:00', duration:3, warn:false},
];

let draggedId = null;
let pendingChanges = [];

function buildCalendar() {
  const tbody = document.getElementById('cal-body');
  tbody.innerHTML = '';
  HOURS.forEach(hour => {
    const tr = document.createElement('tr');
    const td_time = document.createElement('td');
    td_time.className = 'time-label';
    td_time.textContent = hour;
    tr.appendChild(td_time);

    DAYS.forEach(day => {
      const td = document.createElement('td');
      td.className = 'droppable';
      td.dataset.day  = day;
      td.dataset.hour = hour;

      // Find session starting here
      const s = sessions.find(x => x.day === day && x.hour === hour);
      if (s) {
        td.appendChild(makeSessionEl(s));
        td.rowSpan = s.duration;
      }

      // Skip cells covered by a multi-row session
      const covered = sessions.find(x => {
        const startIdx = HOURS.indexOf(x.hour);
        const cellIdx  = HOURS.indexOf(hour);
        return x.day === day && cellIdx > startIdx && cellIdx < startIdx + x.duration;
      });
      if (covered) return;

      setupDrop(td);
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

function makeSessionEl(s) {
  const div = document.createElement('div');
  div.className = `session type-${s.type}`;
  div.draggable = true;
  div.dataset.id = s.id;
  div.innerHTML = `
    ${s.warn ? '<span class="warn-badge">⚠️</span>' : ''}
    <div class="team-name">${s.team}</div>
    <div class="session-meta">🏢 ${s.hall}</div>
  `;
  div.addEventListener('dragstart', e => {
    draggedId = s.id;
    div.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
  });
  div.addEventListener('dragend', () => {
    div.classList.remove('dragging');
    draggedId = null;
  });
  return div;
}

function setupDrop(td) {
  td.addEventListener('dragover', e => {
    e.preventDefault();
    td.classList.add('drag-over');
    e.dataTransfer.dropEffect = 'move';
  });
  td.addEventListener('dragleave', () => td.classList.remove('drag-over'));
  td.addEventListener('drop', e => {
    e.preventDefault();
    td.classList.remove('drag-over');
    if (!draggedId) return;

    const newDay  = td.dataset.day;
    const newHour = td.dataset.hour;
    const s = sessions.find(x => x.id === draggedId);
    if (!s) return;

    const oldDay  = s.day;
    const oldHour = s.hour;

    // Check conflict
    const conflict = sessions.find(x =>
      x.id !== s.id && x.day === newDay && x.hour === newHour
    );

    if (conflict) {
      showToast(`❌ התנגשות עם "${conflict.team}" – לא ניתן לשבץ כאן!`, false);
      return;
    }

    // Apply move
    s.day  = newDay;
    s.hour = newHour;

    pendingChanges.push({
      team: s.team,
      from: `יום ${DAY_NAMES[oldDay]} ${oldHour}`,
      to:   `יום ${DAY_NAMES[newDay]} ${newHour}`,
    });

    showToast(`✅ ${s.team} הוזז ליום ${DAY_NAMES[newDay]} ${newHour}`, true);
    updateChangeLog();
    buildCalendar();
  });
}

function showToast(msg, success) {
  const t = document.getElementById('conflict-toast');
  t.textContent = msg;
  t.className   = success ? 'success' : '';
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 3000);
}

function updateChangeLog() {
  const log  = document.getElementById('change-log');
  const list = document.getElementById('change-list');
  if (pendingChanges.length === 0) { log.style.display = 'none'; return; }
  log.style.display = 'block';
  list.innerHTML = pendingChanges.map(c =>
    `<li><strong>${c.team}</strong> · ${c.from} ← הועבר ל-${c.to}</li>`
  ).join('');
}

buildCalendar();
</script>
</body>
</html>
"""

components.html(CALENDAR_HTML, height=700, scrolling=True)

st.write("---")

# ── Summary footer ────────────────────────────────────────────────────────────
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    st.metric("סה״כ אימונים", 32)
with col_s2:
    st.metric("מגרש מלא", 24)
with col_s3:
    st.metric("חצי מגרש", 8)
with col_s4:
    st.markdown(
        "<div style='background:#f0fdf4;border:1px solid #22c55e;border-radius:8px;"
        "padding:8px 12px;text-align:center;'>"
        "<div style='color:#16a34a;font-weight:900;font-size:22px;'>87</div>"
        "<div style='color:gray;font-size:12px;'>ציון איכות</div></div>",
        unsafe_allow_html=True
    )

st.write("##")
col_pdf, col_back = st.columns(2)
with col_pdf:
    if st.button("📄 ייצא לקובץ PDF"):
        st.info("ייצוא PDF יהיה זמין בשלב ב׳")
with col_back:
    if st.button("🔄 חזור לאופטימיזציה"):
        st.switch_page("pages/2_Optimization.py")