"""
sections/players.py
ניהול שחקנים – רשימה, חיפוש, הוספה, עריכה
מקושר ל: dim_player + dim_human + bridge_player_team
"""
import streamlit as st
from sections.shared import top_nav, page_header
from sections.db_data import PLAYERS_SAMPLE, TEAMS_DB, TEAM_NAMES

POSITIONS = ["LW", "RW", "CB", "LB", "RB", "PV", "GK"]
POSITION_LABELS = {
    "LW": "חלוץ שמאל",
    "RW": "חלוץ ימין",
    "CB": "מרכז",
    "LB": "הגנה שמאל",
    "RB": "הגנה ימין",
    "PV": "ציר",
    "GK": "שוער/ת",
}


def init_state():
    for k, v in {
        "players":         [p.copy() for p in PLAYERS_SAMPLE],
        "show_add_player": False,
        "edit_player_idx": None,
        "player_filter_team": "הכל",
        "player_filter_pos":  "הכל",
        "player_search":      "",
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _player_form(title, data, save_key, cancel_key):
    team_options = ["—"] + [t["name"] for t in TEAMS_DB if t["active"]]
    pos_options  = list(POSITIONS)

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
                                   label_visibility="collapsed", key=f"pn_{save_key}")
        with c2:
            st.markdown("<div class='form-lbl'>קבוצה</div>", unsafe_allow_html=True)
            curr_team = TEAM_NAMES.get(data.get("team_key"), "—")
            f_team_name = st.selectbox("קבוצה", team_options,
                                        index=team_options.index(curr_team) if curr_team in team_options else 0,
                                        label_visibility="collapsed", key=f"pt_{save_key}")

        # שורה 2 – עמדה + שוער
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("<div class='form-lbl'>עמדה</div>", unsafe_allow_html=True)
            curr_pos = data.get("position", "CB")
            f_pos = st.selectbox("עמדה", pos_options,
                                  index=pos_options.index(curr_pos) if curr_pos in pos_options else 2,
                                  label_visibility="collapsed", key=f"pp_{save_key}",
                                  format_func=lambda x: f"{x} – {POSITION_LABELS[x]}")
        with c4:
            st.markdown("<div class='form-lbl'>בית ספר</div>", unsafe_allow_html=True)
            f_school = st.text_input("ביה״ס", value=data.get("school",""),
                                     placeholder='למשל: בי"ס רמות',
                                     label_visibility="collapsed", key=f"ps_{save_key}")

        f_gk = st.checkbox("שוער/ת", value=data.get("is_gk", False), key=f"pgk_{save_key}")
        f_active = st.checkbox("פעיל/ה", value=data.get("active", True), key=f"pa_{save_key}")

        st.write("")
        cb, cs = st.columns(2)
        with cb:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("ביטול", use_container_width=True, key=f"pcancel_{cancel_key}"):
                st.session_state.show_add_player = False
                st.session_state.edit_player_idx = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cs:
            btn = "עדכן שחקן" if data else "הוסף שחקן"
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button(btn, use_container_width=True, key=f"psave_{save_key}"):
                if f_name.strip():
                    team_key = next((t["team_key"] for t in TEAMS_DB if t["name"] == f_team_name), None)
                    return {
                        "player_key": data.get("player_key", 9000 + len(st.session_state.players)),
                        "name":       f_name.strip(),
                        "team_key":   team_key,
                        "position":   f_pos,
                        "is_gk":      f_gk,
                        "school":     f_school.strip(),
                        "active":     f_active,
                    }
                else:
                    st.error("נא להזין שם שחקן/ית")
            st.markdown('</div>', unsafe_allow_html=True)
    return None


def render():
    init_state()
    top_nav("ניהול נתונים", "overview")
    page_header("ניהול", "שחקנים",
                "רשימת השחקנים והשחקניות הרשומים במועדון",
                "הוסף שחקן/ית", "add_player_btn", "show_add_player")

    # ── טופס עריכה ────────────────────────────────────────────────────
    edit_idx = st.session_state.edit_player_idx
    if edit_idx is not None:
        result = _player_form("עריכת שחקן/ית",
                               st.session_state.players[edit_idx],
                               f"edit_p_{edit_idx}", f"edit_p_{edit_idx}")
        if result:
            st.session_state.players[edit_idx] = result
            st.session_state.edit_player_idx   = None
            st.success(f"✅ הפרטים של {result['name']} עודכנו!")
            st.rerun()
        st.write("")

    elif st.session_state.show_add_player:
        result = _player_form("הוספת שחקן/ית חדש/ה", {}, "new_player", "new_player")
        if result:
            st.session_state.players.append(result)
            st.session_state.show_add_player = False
            st.success(f"✅ {result['name']} נוסף/ה!")
            st.rerun()
        st.write("")

    # ── סינון וחיפוש ──────────────────────────────────────────────────
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            search = st.text_input("🔍 חיפוש לפי שם", value=st.session_state.player_search,
                                   placeholder="הקלד שם...", label_visibility="collapsed")
            st.session_state.player_search = search
        with c2:
            team_opts = ["הכל"] + [t["name"] for t in TEAMS_DB if t["active"]]
            team_f = st.selectbox("קבוצה", team_opts,
                                   index=team_opts.index(st.session_state.player_filter_team)
                                   if st.session_state.player_filter_team in team_opts else 0,
                                   label_visibility="collapsed")
            st.session_state.player_filter_team = team_f
        with c3:
            pos_opts = ["הכל"] + [f"{p} – {POSITION_LABELS[p]}" for p in POSITIONS]
            pos_f = st.selectbox("עמדה", pos_opts, label_visibility="collapsed")

    # ── רשימה מסוננת ──────────────────────────────────────────────────
    players = st.session_state.players
    if search:
        players = [p for p in players if search.lower() in p["name"].lower()]
    if team_f != "הכל":
        team_key = next((t["team_key"] for t in TEAMS_DB if t["name"] == team_f), None)
        players = [p for p in players if p.get("team_key") == team_key]
    if pos_f != "הכל":
        pos_code = pos_f.split(" – ")[0]
        players = [p for p in players if p.get("position") == pos_code]

    st.markdown(
        f"<div style='font-size:13px;color:#94a3b8;margin:12px 0 6px;'>"
        f"מציג {len(players)} שחקנים</div>",
        unsafe_allow_html=True,
    )

    if not players:
        st.markdown(
            "<div style='text-align:center;padding:40px;color:#94a3b8;'>לא נמצאו שחקנים</div>",
            unsafe_allow_html=True,
        )
        return

    # כותרת עמודות
    hc = st.columns([3, 2, 1.5, 2, 0.8, 0.8])
    for col, txt in zip(hc, ["שם", "קבוצה", "עמדה", "בית ספר", "", ""]):
        col.markdown(
            f"<div style='font-size:11px;font-weight:700;color:#94a3b8;"
            f"letter-spacing:1px;padding-bottom:6px;'>{txt}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='border:none;border-top:2px solid #e2e8f0;margin:0 0 8px;'>",
                unsafe_allow_html=True)

    for i, player in enumerate(players):
        real_idx = st.session_state.players.index(player)
        team_name = TEAM_NAMES.get(player.get("team_key"), "—")
        pos_label = POSITION_LABELS.get(player.get("position",""), player.get("position","—"))
        gk_badge  = " 🧤" if player.get("is_gk") else ""
        active_clr = "#0f172a" if player.get("active", True) else "#94a3b8"

        col_name, col_team, col_pos, col_school, col_edit, col_del = st.columns([3, 2, 1.5, 2, 0.8, 0.8])

        with col_name:
            st.markdown(
                f"<div style='font-size:15px;font-weight:700;color:{active_clr};padding:8px 0;'>"
                f"👤 {player['name']}{gk_badge}"
                f"{'  <span style=\"color:#94a3b8;font-size:12px;\">(לא פעיל)</span>' if not player.get('active',True) else ''}"
                f"</div>",
                unsafe_allow_html=True,
            )
        with col_team:
            color = "#1d4ed8" if team_name != "—" else "#94a3b8"
            st.markdown(
                f"<div style='padding:8px 0;'>"
                f"<span class='tag tag-blue' style='font-size:12px;'>{team_name}</span></div>",
                unsafe_allow_html=True,
            )
        with col_pos:
            st.markdown(
                f"<div style='font-size:13px;color:#475569;padding:8px 0;'>{pos_label}</div>",
                unsafe_allow_html=True,
            )
        with col_school:
            st.markdown(
                f"<div style='font-size:13px;color:#64748b;padding:8px 0;'>{player.get('school','—')}</div>",
                unsafe_allow_html=True,
            )
        with col_edit:
            if st.button("✏️", key=f"ep_{real_idx}_{i}"):
                st.session_state.edit_player_idx = real_idx
                st.session_state.show_add_player = False
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"dp_{real_idx}_{i}"):
                deleted = st.session_state.players.pop(real_idx)
                st.toast(f"'{deleted['name']}' הוסר/ה")
                st.rerun()

        st.markdown(
            "<hr style='border:none;border-top:1px solid #f1f5f9;margin:0;'>",
            unsafe_allow_html=True,
        )
