from fastapi import FastAPI, Query
import sqlite3
from datetime import datetime
from pydantic import BaseModel, EmailStr

#Class for creating alerts used in POST /alerts
class AlertCreate(BaseModel):
    email: EmailStr
    location: str
    metric: str
    operator: str
    threshold: float


app = FastAPI()

#Shows all weather data
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


#Shows minimum, max, avg of weather data. Defaults to the last 24h
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


#Lets users create alerts
@app.post("/alerts")
async def create_alert(alert: AlertCreate):

    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    #adds the alert to the database
    cursor.execute("""
        INSERT INTO alerts
        (email, location, metric, operator, threshold)
        VALUES (?, ?, ?, ?, ?)
    """, (
        alert.email,
        alert.location,
        alert.metric,
        alert.operator,
        alert.threshold
    ))

    connection.commit()

    alert_id = cursor.lastrowid

    connection.close()

    return {
        "id": alert_id,
        "message": "Alert created successfully"
    }


#Lets users see all alerts (demonstration, normally would just show their alerts)
@app.get("/alerts")
async def get_alerts():

    #Fetches all alerts from database
    connection = sqlite3.connect("weather.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM alerts")

    alerts = cursor.fetchall()

    connection.close()

    return [dict(alert) for alert in alerts]


#Lets users delete alerts (demonstration, normally would just let them delete their alerts)
#Deletes the alert with the id that the user called in the endpoint
@app.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: int):

    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    #Deleting the alert in the database
    cursor.execute(
        "DELETE FROM alerts WHERE id = ?",
        (alert_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    #Returns an error if an alert with specified id doesnt exist
    if deleted == 0:
        return {"error": "Alert not found"}

    return {
        "message": "Alert deleted successfully"
    }