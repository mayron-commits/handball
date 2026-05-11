"""
sections/db_data.py
נתוני ברירת מחדל מהמחסן – תואמים את מבנה ה-DWH האמיתי.
בשלב ב׳ יוחלפו בשאילתות SQL אמיתיות ל-Supabase.
"""

# ── dim_human (12 רשומות) ────────────────────────────────────────────────────
HUMANS = {
    1001: {"first_name": "הרבויה",   "last_name": "פאזין",     "gender": "M", "phone": "050-1234567", "city": "ראשון לציון"},
    1002: {"first_name": "אמיתי",    "last_name": "דיין",      "gender": "M", "phone": "050-1234568", "city": "ראשון לציון"},
    1003: {"first_name": "אסף",      "last_name": "סיטון",     "gender": "M", "phone": "050-1234569", "city": "ראשון לציון"},
    1004: {"first_name": "ג'וני",    "last_name": "אולייניק",  "gender": "M", "phone": "050-1234570", "city": "ראשון לציון"},
    1005: {"first_name": "עומרי",    "last_name": "מימון",     "gender": "M", "phone": "050-1234571", "city": "ראשון לציון"},
    1006: {"first_name": "פז",       "last_name": "בן הרויה",  "gender": "M", "phone": "050-1234572", "city": "ראשון לציון"},
    1007: {"first_name": "יעל",      "last_name": "עודד",      "gender": "F", "phone": "050-1234573", "city": "ראשון לציון"},
    1008: {"first_name": "שירה",     "last_name": "כהן",       "gender": "F", "phone": "050-1234574", "city": "ראשון לציון"},
    1009: {"first_name": "איוואן",   "last_name": "קראציץ'",   "gender": "M", "phone": "050-1234575", "city": "ראשון לציון"},
    1010: {"first_name": "ניר",      "last_name": "יעיש",      "gender": "M", "phone": "050-1234576", "city": "ראשון לציון"},
    1011: {"first_name": "עמית",     "last_name": "עוזיאל",    "gender": "M", "phone": "050-1234577", "city": "ראשון לציון"},
    1012: {"first_name": "אור",      "last_name": "תורג'מן",   "gender": "M", "phone": "050-1234578", "city": "ראשון לציון"},
}

def full_name(human_key):
    h = HUMANS.get(human_key, {})
    return f"{h.get('first_name','')} {h.get('last_name','')}".strip()


# ── dim_coach (12 מאמנים) ────────────────────────────────────────────────────
COACHES_DB = [
    {"coach_key": 2001, "human_key": 1001, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2002, "human_key": 1002, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2003, "human_key": 1003, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2004, "human_key": 1004, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2005, "human_key": 1005, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2006, "human_key": 1006, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2007, "human_key": 1007, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2008, "human_key": 1008, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2009, "human_key": 1009, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2010, "human_key": 1010, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2011, "human_key": 1011, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
    {"coach_key": 2012, "human_key": 1012, "license": "A", "role": "Head Coach",       "gk_specialist": False, "active": True},
]

# מפה: coach_key → שם מלא
COACH_NAMES = {c["coach_key"]: full_name(c["human_key"]) for c in COACHES_DB}


# ── dim_hall (4 אולמות) ──────────────────────────────────────────────────────
HALLS_DB = [
    {"hall_key": 1001, "name": "נחלת",   "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1002, "name": "רועים",  "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1003, "name": "אשלים",  "address": "ראשון לציון", "is_divisible": True},
    {"hall_key": 1004, "name": "גן נחום","address": "ראשון לציון", "is_divisible": False},
]

HALL_NAMES = {h["hall_key"]: h["name"] for h in HALLS_DB}


# ── dim_team (17 קבוצות) ─────────────────────────────────────────────────────
TEAMS_DB = [
    {"team_key": 3001, "name": "ז1",             "age_group": 13, "gender": "M", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2004, "coach_asst": None, "active": True},
    {"team_key": 3002, "name": "ז2",             "age_group": 13, "gender": "M", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2001, "coach_asst": None, "active": True},
    {"team_key": 3003, "name": "ז3",             "age_group": 13, "gender": "M", "dept": "Youth",  "sessions": 1, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2011, "coach_asst": None, "active": True},
    {"team_key": 3004, "name": "ז4",             "age_group": 13, "gender": "M", "dept": "Youth",  "sessions": 1, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2004, "coach_asst": None, "active": True},
    {"team_key": 3005, "name": "ח",              "age_group": 14, "gender": "M", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2002, "coach_asst": None, "active": True},
    {"team_key": 3006, "name": "ט",              "age_group": 15, "gender": "M", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2002, "coach_asst": None, "active": True},
    {"team_key": 3007, "name": "י",              "age_group": 16, "gender": "M", "dept": "Youth",  "sessions": 4, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2001, "coach_asst": None, "active": True},
    {"team_key": 3008, "name": "נוער",           "age_group": 17, "gender": "M", "dept": "Youth",  "sessions": 4, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2003, "coach_asst": None, "active": True},
    {"team_key": 3009, "name": "ילדות ז",        "age_group": 13, "gender": "F", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2007, "coach_asst": None, "active": True},
    {"team_key": 3010, "name": "ילדות ח",        "age_group": 14, "gender": "F", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2008, "coach_asst": None, "active": True},
    {"team_key": 3011, "name": "נערות ט",        "age_group": 15, "gender": "F", "dept": "Youth",  "sessions": 3, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2012, "coach_asst": None, "active": True},
    {"team_key": 3012, "name": "מצוינות בנות",   "age_group": 14, "gender": "F", "dept": "Youth",  "sessions": 1, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2001, "coach_asst": None, "active": True},
    {"team_key": 3013, "name": "מצוינות בנים",   "age_group": 14, "gender": "M", "dept": "Youth",  "sessions": 1, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2001, "coach_asst": None, "active": True},
    {"team_key": 3014, "name": "מצוינות נוער",   "age_group": 17, "gender": "M", "dept": "Youth",  "sessions": 1, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2001, "coach_asst": None, "active": True},
    {"team_key": 3015, "name": "בוגרים",         "age_group": 20, "gender": "M", "dept": "Adults", "sessions": 5, "duration": 90, "shortening": False, "half_court": False, "coach_primary": 2005, "coach_asst": 2003, "active": True},
    {"team_key": 3016, "name": "בוגרות",         "age_group": 20, "gender": "F", "dept": "Adults", "sessions": 5, "duration": 90, "shortening": False, "half_court": True,  "coach_primary": 2006, "coach_asst": None, "active": True},
    {"team_key": 3017, "name": "ארצית",          "age_group": 40, "gender": "M", "dept": "Adults", "sessions": 2, "duration": 90, "shortening": True,  "half_court": True,  "coach_primary": 2010, "coach_asst": None, "active": False},
]

TEAM_NAMES = {t["team_key"]: t["name"] for t in TEAMS_DB}


# ── שחקנים לדוגמה (יתחברו ל-dim_player + dim_human בשלב ב׳) ──────────────
PLAYERS_SAMPLE = [
    {"player_key": 4001, "name": "אורי לוי",       "team_key": 3001, "position": "LW",  "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4002, "name": "דן כהן",         "team_key": 3001, "position": "RW",  "is_gk": False, "school": 'בי"ס הרצל', "active": True},
    {"player_key": 4003, "name": "נועם שרון",      "team_key": 3002, "position": "CB",  "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4004, "name": "תום אברהם",      "team_key": 3005, "position": "GK",  "is_gk": True,  "school": 'בי"ס בגין', "active": True},
    {"player_key": 4005, "name": "יובל מזרחי",     "team_key": 3007, "position": "PV",  "is_gk": False, "school": 'בי"ס הרצל', "active": True},
    {"player_key": 4006, "name": "שני גולן",       "team_key": 3009, "position": "LW",  "is_gk": False, "school": 'בי"ס רמות', "active": True},
    {"player_key": 4007, "name": "מאיה ברק",       "team_key": 3010, "position": "RB",  "is_gk": False, "school": 'בי"ס בגין', "active": True},
    {"player_key": 4008, "name": "ליאור פרץ",      "team_key": 3015, "position": "CB",  "is_gk": False, "school": "—",         "active": True},
]


# ── מנהלי קבוצות לדוגמה ──────────────────────────────────────────────────────
MANAGERS_SAMPLE = [
    {"manager_key": 5001, "name": "אבי פרידמן",  "team_key": 3015, "phone": "050-9991111", "email": "avi@hapoel.com",   "active": True},
    {"manager_key": 5002, "name": "רות שמיר",    "team_key": 3016, "phone": "050-9992222", "email": "ruth@hapoel.com",  "active": True},
    {"manager_key": 5003, "name": "נועם כץ",     "team_key": 3007, "phone": "050-9993333", "email": "noam@hapoel.com",  "active": True},
    {"manager_key": 5004, "name": "ליאת בן דוד", "team_key": 3008, "phone": "050-9994444", "email": "liat@hapoel.com",  "active": True},
    {"manager_key": 5005, "name": "רן אלון",     "team_key": 3001, "phone": "050-9995555", "email": "ran@hapoel.com",   "active": True},
]
