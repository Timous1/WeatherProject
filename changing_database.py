import json
import sqlite3

#conn = sqlite3.connect("weather.db")
#cursor = conn.cursor()
#cursor.execute("ALTER TABLE weather ADD COLUMN pressure REAL")
#cursor.execute("ALTER TABLE weather ADD COLUMN wind_speed REAL")
#conn.commit()

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        location TEXT NOT NULL,
        metric TEXT NOT NULL,
        operator TEXT NOT NULL,
        threshold REAL NOT NULL,
        enabled INTEGER DEFAULT 1,
        is_triggered INTEGER DEFAULT 0,
        last_triggered TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()