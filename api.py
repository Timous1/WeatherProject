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
    for id, temp, time in rows:
        result.append({"temp": temp,
                       "time": time,
                       "bratislava_time": datetime.fromtimestamp(time).isoformat()})

    return result

@app.get("/stats")
async def weather_stats(
    from_time: int | None = Query(None, alias="from", description = "Start timestampt (Unix)"),
    to_time: int | None = Query(None, alias="to", description = "End timestampt (Unix)"),
):
    #TIME FILTERING
    query = "SELECT * FROM weather WHERE 1=1"
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
    for id, temp, time in rows:
        result.append({"temp": temp,
                       "time": time,
                       "bratislava_time": datetime.fromtimestamp(time).isoformat()
                       })

    return result