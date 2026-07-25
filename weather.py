import requests
import json
import sqlite3
import os
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "weather.project.email.alerts@gmail.com"
    msg["from"] = user
    password = "rchvrjmejobarvve"#os.getenv("GMAIL_ALERT_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

#Variables for gathering data from openweather
key = "3f4f4e6b2a290797b99c9595be35dde3"#os.getenv("OPENWEATHER_API_KEY")
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

if data["main"]["temp"]>10:
    email_alert("Too hot", "It is too hot", "timotxp@gmail.com")

#Storing data in SQL database
#Table: weather; Columns: temp, time (time will break in 2038)
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO weather (temp, time, pressure, wind_speed) VALUES (?,?,?,?)", (data["main"]["temp"], data["dt"], data["main"]["pressure"], data["wind"]["speed"]))
conn.commit()

# Query data
#cursor.execute("SELECT * FROM weather")
#rows = cursor.fetchall()

# Print results
#for row in rows:
#    print(row)
#conn.close()