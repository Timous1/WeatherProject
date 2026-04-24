from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/weather")
async def weather_data():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    #Query Data
    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()
    conn.close()

    #Translate to dictionary
    result = []
    for id, temp, time in rows:
        result.append({"temp": temp, "time": time})

    return result