import json
import sqlite3

def get_enabled_alerts():
    #Fetches all alerts from database
    connection = sqlite3.connect("weather.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM alerts WHERE enabled = 1")

    alerts = cursor.fetchall()

    connection.close()

    return alerts

def mark_alert_triggered(alert_id):
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE alerts
        SET is_triggered = 1,
            last_triggered = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (alert_id,))

    connection.commit()
    connection.close()


def reset_alert(alert_id):
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE alerts
        SET is_triggered = 0
        WHERE id = ?
    """, (alert_id,))

    connection.commit()
    connection.close()

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