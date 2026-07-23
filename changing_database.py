import json
import sqlite3

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE weather ADD COLUMN pressure REAL")
cursor.execute("ALTER TABLE weather ADD COLUMN wind_speed REAL")
conn.commit()