"""
sections/db_data.py
נתוני ברירת מחדל – מסונכרנים במלואם עם מחסן הנתונים (DWH_Data.xlsx).
בשלב ב׳ יוחלפו בשאילתות SQL ל-Supabase.

סטטוס סנכרון:
  ✅ dim_hall           – 4 רשומות
  ✅ dim_human          – 12 רשומות
  ✅ dim_coach          – 12 רשומות (כולל license, gk_specialist)
  ✅ dim_team           – 17 רשומות (כולל חלונות זמן, active_flag)
  ✅ bridge_team_hall   – 35 רשומות (אולמות מורשים + priority)
  ⏳ dim_player         – ריק בDWH, יתמלא בשלב ב׳
  ⏳ dim_team_manager   – ריק בDWH, יתמלא בשלב ב׳
  ⏳ bridge_player_team – ריק בDWH, יתמלא בשלב ב׳
"""

# ── dim_human (12 רשומות) ────────────────────────────────────────────────────
HUMANS = {
    1001: {"first_name": "הרבויה",  "last_name": "פאזין",    "gender": "M", "phone": "050-1234567", "city": "ראשון לציון", "address": "ראשון לציון"},
    1002: {"first_name": "אמיתי",   "last_name": "דיין",     "gender": "M", "phone": "050-1234568", "city": "ראשון לציון", "address": "ראשון לציון"},
    1003: {"first_name": "אסף",     "last_name": "סיטון",    "gender": "M", "phone": "050-1234569", "city": "ראשון לציון", "address": "ראשון לציון"},
    1004: {"first_name": "ג'וני",   "last_name": "אולייניק", "gender": "M", "phone": "050-1234570", "city": "ראשון לציון", "address": "ראשון לציון"},
    1005: {"first_name": "עומרי",   "last_name": "מימון",    "gender": "M", "phone": "050-1234571", "city": "ראשון לציון", "address": "ראשון לציון"},
    1006: {"first_name": "פז",      "last_name": "בן הרויה", "gender": "M", "phone": "050-1234572", "city": "ראשון לציון", "address": "ראשון לציון"},
    1007: {"first_name": "יעל",     "last_name": "עודד",     "gender": "F", "phone": "050-1234573", "city": "ראשון לציון", "address": "ראשון לציון"},
    1008: {"first_name": "שירה",    "last_name": "כהן",      "gender": "F", "phone": "050-1234574", "city": "ראשון לציון", "address": "ראשון לציון"},
    1009: {"first_name": "איוואן",  "last_name": "קראציץ'",  "gender": "M", "phone": "050-1234575", "city": "ראשון לציון", "address": "ראשון לציון"},
    1010: {"first_name": "ניר",     "last_name": "יעיש",     "gender": "M", "phone": "050-1234576", "city": "ראשון לציון", "address": "ראשון לציון"},
    1011: {"first_name": "עמית",    "last_name": "עוזיאל",   "gender": "M", "phone": "050-1234577", "city": "ראשון לציון", "address": "ראשון לציון"},
    1012: {"first_name": "אור",     "last_name": "תורג'מן",  "gender": "F", "phone": "050-1234578", "city": "ראשון לציון", "address": "ראשון לציון"},
}

def full_name(human_key: int) -> str:
    h = HUMANS.get(human_key, {})
    return f"{h.get('first_name','')} {h.get('last_name','')}".strip()


# ── dim_coach (12 רשומות) ────────────────────────────────────────────────────
# שדות: coach_key, human_key, coaching_license_level, primary_role,
#        hire_date, is_goalkeeper_specialist_flag, active_flag
COACHES_DB = [
    {"coach_key": 2001, "human_key": 1001, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2002, "human_key": 1002, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2003, "human_key": 1003, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2004, "human_key": 1004, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2005, "human_key": 1005, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2006, "human_key": 1006, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2007, "human_key": 1007, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2008, "human_key": 1008, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2009, "human_key": 1009, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2010, "human_key": 1010, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2011, "human_key": 1011, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
    {"coach_key": 2012, "human_key": 1012, "license": "A", "role": "Head Coach", "gk_specialist": False, "active": True},
]

# מפות מהירות
COACH_BY_KEY  = {c["coach_key"]: c for c in COACHES_DB}
COACH_NAMES   = {c["coach_key"]: full_name(c["human_key"]) for c in COACHES_DB}


# ── dim_hall (4 רשומות) ──────────────────────────────────────────────────────
# שדות: hall_key, hall_name, address, is_divisible_flag
HALLS_DB = [
    {"hall_key": 1001, "name": "נחלת",    "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1002, "name": "רועים",   "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1003, "name": "אשלים",   "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1004, "name": "גן נחום", "address": "ראשון לציון", "is_divisible": False},
]

HALL_BY_KEY = {h["hall_key"]: h for h in HALLS_DB}
HALL_NAMES  = {h["hall_key"]: h["name"] for h in HALLS_DB}
ALL_HALL_NAMES = [h["name"] for h in HALLS_DB]


# ── bridge_team_hall (35 רשומות) ─────────────────────────────────────────────
# שדות: team_key, hall_key, priority, is_active
# Priority 1 = אולם ראשי, 2 = אולם גיבוי
BRIDGE_TEAM_HALL = [
    # priority 1 (אולם ראשי לכל קבוצה)
    {"team_key": 3001, "hall_key": 1001, "priority": 1},
    {"team_key": 3002, "hall_key": 1002, "priority": 1},
    {"team_key": 3003, "hall_key": 1004, "priority": 1},
    {"team_key": 3004, "hall_key": 1001, "priority": 1},
    {"team_key": 3005, "hall_key": 1003, "priority": 1},
    {"team_key": 3006, "hall_key": 1003, "priority": 1},
    {"team_key": 3007, "hall_key": 1003, "priority": 1},
    {"team_key": 3008, "hall_key": 1001, "priority": 1},
    {"team_key": 3009, "hall_key": 1002, "priority": 1},
    {"team_key": 3010, "hall_key": 1003, "priority": 1},
    {"team_key": 3011, "hall_key": 1002, "priority": 1},
    {"team_key": 3012, "hall_key": 1001, "priority": 1},
    {"team_key": 3013, "hall_key": 1002, "priority": 1},
    {"team_key": 3014, "hall_key": 1003, "priority": 1},
    {"team_key": 3015, "hall_key": 1001, "priority": 1},
    {"team_key": 3016, "hall_key": 1001, "priority": 1},
    {"team_key": 3017, "hall_key": 1003, "priority": 1},
    # priority 2 (אולם גיבוי)
    {"team_key": 3001, "hall_key": 1002, "priority": 2},
    {"team_key": 3002, "hall_key": 1003, "priority": 2},
    {"team_key": 3003, "hall_key": 1002, "priority": 2},
    {"team_key": 3004, "hall_key": 1003, "priority": 2},
    {"team_key": 3005, "hall_key": 1002, "priority": 2},
    {"team_key": 3006, "hall_key": 1002, "priority": 2},
    {"team_key": 3007, "hall_key": 1001, "priority": 2},
    {"team_key": 3007, "hall_key": 1002, "priority": 2},
    {"team_key": 3008, "hall_key": 1002, "priority": 2},
    {"team_key": 3008, "hall_key": 1003, "priority": 2},
    {"team_key": 3009, "hall_key": 1001, "priority": 2},
    {"team_key": 3009, "hall_key": 1003, "priority": 2},
    {"team_key": 3010, "hall_key": 1002, "priority": 2},
    {"team_key": 3011, "hall_key": 1003, "priority": 2},
    {"team_key": 3012, "hall_key": 1002, "priority": 2},
    {"team_key": 3013, "hall_key": 1001, "priority": 2},
    {"team_key": 3014, "hall_key": 1002, "priority": 2},
    {"team_key": 3016, "hall_key": 1003, "priority": 2},
]

def get_team_halls(team_key: int) -> list:
    """מחזיר שמות אולמות מורשים לקבוצה לפי priority."""
    entries = sorted(
        [b for b in BRIDGE_TEAM_HALL if b["team_key"] == team_key],
        key=lambda x: x["priority"]
    )
    return [HALL_NAMES[e["hall_key"]] for e in entries if e["hall_key"] in HALL_NAMES]


# ── dim_team (17 רשומות) ─────────────────────────────────────────────────────
# שדות: team_key, team_id_federation, team_name, season, age_group, gender,
#        department, trainings_per_week_planned, base_training_duration_minutes,
#        is_shortening_allowed_flag, is_half_court_allowed_flag,
#        requires_assistant_coach_flag, coach_primary_key, coach_assistant_key,
#        can_train_early_afternoon, can_train_mid_afternoon,
#        can_train_late_afternoon, can_train_evening, active_flag

def _ui_color(dept: str, gender: str) -> str:
    if dept == "Adults":
        return "#d90429"
    return "#db2777" if gender == "F" else "#1d4ed8"

TEAMS_DB = [
    {
        "team_key": 3001, "fed_id": 1,  "name": "ז1",           "season": "2025/2026",
        "age_group": 13, "gender": "M", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2004, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3002, "fed_id": 2,  "name": "ז2",           "season": "2025/2026",
        "age_group": 13, "gender": "M", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2001, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3003, "fed_id": 3,  "name": "ז3",           "season": "2025/2026",
        "age_group": 13, "gender": "M", "dept": "Youth",
        "sessions": 1,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2011, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3004, "fed_id": 4,  "name": "ז4",           "season": "2025/2026",
        "age_group": 13, "gender": "M", "dept": "Youth",
        "sessions": 1,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2004, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3005, "fed_id": 5,  "name": "ח",            "season": "2025/2026",
        "age_group": 14, "gender": "M", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2002, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3006, "fed_id": 6,  "name": "ט",            "season": "2025/2026",
        "age_group": 15, "gender": "M", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2002, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": True,  "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3007, "fed_id": 7,  "name": "י",            "season": "2025/2026",
        "age_group": 16, "gender": "M", "dept": "Youth",
        "sessions": 4,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2001, "coach_asst": None,
        "time_early": False, "time_mid": False, "time_late": True,  "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3008, "fed_id": 8,  "name": "נוער",         "season": "2025/2026",
        "age_group": 17, "gender": "M", "dept": "Youth",
        "sessions": 4,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2003, "coach_asst": None,
        "time_early": False, "time_mid": False, "time_late": True,  "time_eve": True,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3009, "fed_id": 9,  "name": "ילדות ז",      "season": "2025/2026",
        "age_group": 13, "gender": "F", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2007, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","F"),
    },
    {
        "team_key": 3010, "fed_id": 10, "name": "ילדות ח",      "season": "2025/2026",
        "age_group": 14, "gender": "F", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2008, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","F"),
    },
    {
        "team_key": 3011, "fed_id": 11, "name": "נערות ט",      "season": "2025/2026",
        "age_group": 15, "gender": "F", "dept": "Youth",
        "sessions": 3,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2012, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": True,  "time_eve": False,
        "active": True,  "color": _ui_color("Youth","F"),
    },
    {
        "team_key": 3012, "fed_id": 12, "name": "מצוינות בנות", "season": "2025/2026",
        "age_group": 14, "gender": "F", "dept": "Youth",
        "sessions": 1,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2001, "coach_asst": None,
        "time_early": True,  "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","F"),
    },
    {
        "team_key": 3013, "fed_id": 13, "name": "מצוינות בנים", "season": "2025/2026",
        "age_group": 14, "gender": "M", "dept": "Youth",
        "sessions": 1,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2001, "coach_asst": None,
        "time_early": True,  "time_mid": True,  "time_late": False, "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3014, "fed_id": 14, "name": "מצוינות נוער", "season": "2025/2026",
        "age_group": 17, "gender": "M", "dept": "Youth",
        "sessions": 1,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2001, "coach_asst": None,
        "time_early": False, "time_mid": True,  "time_late": True,  "time_eve": False,
        "active": True,  "color": _ui_color("Youth","M"),
    },
    {
        "team_key": 3015, "fed_id": 15, "name": "בוגרים",       "season": "2025/2026",
        "age_group": 20, "gender": "M", "dept": "Adults",
        "sessions": 5,  "duration": 90, "shortening": False, "half_court": False, "req_asst": True,
        "coach_primary": 2005, "coach_asst": 2003,
        "time_early": True,  "time_mid": False, "time_late": True,  "time_eve": True,
        "active": True,  "color": _ui_color("Adults","M"),
    },
    {
        "team_key": 3016, "fed_id": 16, "name": "בוגרות",       "season": "2025/2026",
        "age_group": 20, "gender": "F", "dept": "Adults",
        "sessions": 5,  "duration": 90, "shortening": False, "half_court": True,  "req_asst": False,
        "coach_primary": 2006, "coach_asst": None,
        "time_early": True,  "time_mid": False, "time_late": True,  "time_eve": True,
        "active": True,  "color": _ui_color("Adults","F"),
    },
    {
        "team_key": 3017, "fed_id": 17, "name": "ארצית",        "season": "2025/2026",
        "age_group": 40, "gender": "M", "dept": "Adults",
        "sessions": 2,  "duration": 90, "shortening": True,  "half_court": True,  "req_asst": False,
        "coach_primary": 2010, "coach_asst": None,
        "time_early": False, "time_mid": False, "time_late": False, "time_eve": True,
        "active": False, "color": _ui_color("Adults","M"),  # ← לא פעיל!
    },
]

TEAM_BY_KEY  = {t["team_key"]: t for t in TEAMS_DB}
TEAM_NAMES   = {t["team_key"]: t["name"] for t in TEAMS_DB}

# רק קבוצות פעילות
ACTIVE_TEAMS = [t for t in TEAMS_DB if t["active"]]


# ── שחקנים לדוגמה – יתמלאו מ-dim_player בשלב ב׳ ────────────────────────────
PLAYERS_SAMPLE = [
    {"player_key": 4001, "name": "אורי לוי",    "team_key": 3001, "position": "LW", "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4002, "name": "דן כהן",      "team_key": 3001, "position": "RW", "is_gk": False, "school": 'בי"ס הרצל', "active": True},
    {"player_key": 4003, "name": "נועם שרון",   "team_key": 3002, "position": "CB", "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4004, "name": "תום אברהם",   "team_key": 3005, "position": "GK", "is_gk": True,  "school": 'בי"ס בגין', "active": True},
    {"player_key": 4005, "name": "יובל מזרחי",  "team_key": 3007, "position": "PV", "is_gk": False, "school": 'בי"ס הרצל', "active": True},
    {"player_key": 4006, "name": "שני גולן",    "team_key": 3009, "position": "LW", "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4007, "name": "מאיה ברק",    "team_key": 3010, "position": "RB", "is_gk": False, "school": 'בי"ס בגין', "active": True},
    {"player_key": 4008, "name": "ליאור פרץ",   "team_key": 3015, "position": "CB", "is_gk": False, "school": "—",         "active": True},
]


# ── מנהלי קבוצות לדוגמה – יתמלאו מ-dim_team_manager בשלב ב׳ ────────────────
MANAGERS_SAMPLE = [
    {"manager_key": 5001, "name": "אבי פרידמן",  "team_key": 3015, "phone": "050-9991111", "email": "avi@hapoel.com",  "active": True},
    {"manager_key": 5002, "name": "רות שמיר",    "team_key": 3016, "phone": "050-9992222", "email": "ruth@hapoel.com", "active": True},
    {"manager_key": 5003, "name": "נועם כץ",     "team_key": 3007, "phone": "050-9993333", "email": "noam@hapoel.com", "active": True},
    {"manager_key": 5004, "name": "ליאת בן דוד", "team_key": 3008, "phone": "050-9994444", "email": "liat@hapoel.com", "active": True},
    {"manager_key": 5005, "name": "רן אלון",     "team_key": 3001, "phone": "050-9995555", "email": "ran@hapoel.com",  "active": True},
]
