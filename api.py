from fastapi import FastAPI, Query
import sqlite3
from datetime import datetime

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
    for id, temp, time, pressure, wind_speed in rows:
        result.append({"temp": temp,
                       "time": time,
                       "bratislava_time": datetime.fromtimestamp(time).isoformat(),
                       "pressure": pressure,
                       "wind_speed": wind_speed})

    return result

@app.get("/stats")
async def weather_stats(
    from_time: int | None = Query(None, alias="from", description = "Start timestampt (Unix)"),
    to_time: int | None = Query(None, alias="to", description = "End timestampt (Unix)"),
):
    #TIME FILTERING
    query = "SELECT MIN(temp), MAX(temp), AVG(temp), MIN(pressure), MAX(pressure), AVG(pressure), MIN(wind_speed), MAX(wind_speed), AVG(wind_speed) FROM weather WHERE 1=1"
    params=[]


    #Set default values from -24h to now
    now_timestamp=int(datetime.now().timestamp())
    if from_time == None:
        from_time = now_timestamp - (24 * 60 * 60)

    if to_time == None:
        to_time = now_timestamp

    #Add filtering to the query
    query += " AND time >= ? AND time <= ?"
    params.append(from_time)
    params.append(to_time)

    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()


    #Query Data
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()


    #Translate to dictionary
    result = []
    print(rows)
    for min_temp, max_temp, avg_temp, min_pressure, max_pressure, avg_pressure, min_wind_speed, max_wind_speed, avg_wind_speed in rows:
        result.append({"min_temp": min_temp,
                       "max_temp": max_temp,
                       "avg_temp": avg_temp,
                       "min_pressure": min_pressure,
                       "max_pressure": max_pressure,
                       "avg_pressure": avg_pressure,
                       "min_wind_speed": min_wind_speed,
                       "max_wind_speed": max_wind_speed,
                       "avg_wind_speed": avg_wind_speed})

    return result