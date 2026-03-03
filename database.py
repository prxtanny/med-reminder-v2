import sqlite3

DB_NAME = "meds.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time TEXT,
            taken_today INTEGER DEFAULT 0,
            last_notified TEXT
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        defaults = {
            "caregiver_email": "",
            "notify_delay": "10",
            "email_enabled": "0",
            "last_reset_date": ""
        }
        for k, v in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)",
                (k, v)
            )

def get_setting(key):
    with connect() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key=?",
            (key,)
        ).fetchone()
        return row[0] if row else ""

def set_setting(key, value):
    with connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
            (key, value)
        )

def log(msg):
    print("[LOG]", msg)
