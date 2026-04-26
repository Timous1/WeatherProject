import requests
import json
import sqlite3
import os

#Variables for gathering data from openweather
key = os.getenv("OPENWEATHER_API_KEY")
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "Bratislava",
    "appid": key,
    "units": "metric"
}


#Fetching data from openweather
response = requests.get(url, params=params)
data = response.json()

#Debug:
#print(data["main"]["temp"])
#print(data["dt"])

#Storing data in SQL database
#Table: weather; Columns: temp, time (time will break in 2038)
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO weather (temp, time) VALUES (?,?)", (data["main"]["temp"], data["dt"]))
conn.commit()

# Query data
#cursor.execute("SELECT * FROM weather")
#rows = cursor.fetchall()

# Print results
#for row in rows:
#    print(row)
#conn.close()