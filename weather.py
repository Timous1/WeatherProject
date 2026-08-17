import requests
import json
import sqlite3
import os
import smtplib
from email.message import EmailMessage
from database import (
    get_enabled_alerts,
    mark_alert_triggered,
    reset_alert
)
import operator

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "weather.project.email.alerts@gmail.com"
    msg["from"] = user
    password = os.getenv("GMAIL_ALERT_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

def evaluate_alert(alert, weather_data):

    #Getting coding names of the metrics and validating user input
    metric_attribute = METRICS.get(alert["metric"])

    if metric_attribute is None:
        return False

    operation = OPERATORS.get(alert["operator"])

    if operation is None:
        return False

    #Assigning actual value of the metric user has chosen
    if metric_attribute == "wind_speed":
        value = weather_data["wind"]["speed"]
    else:
        value = weather_data["main"][metric_attribute]

    #Evaluating user condition
    return operation(value, alert["threshold"])

def check_alerts(weather_data):

    alerts = get_enabled_alerts()

    for alert in alerts:

        condition_met = evaluate_alert(alert, weather_data)

        #Checks if condition is met
        #includes a functionality where the user will not receive the same alerts again so if it was already triggered the user will not receive an alert anymore
        if condition_met and not alert["is_triggered"]:

            email_alert(str(alert["metric"]) + str(alert["operator"]) + str(alert["threshold"]), ("You received a weather alert "
            "because " + str(alert["metric"]) + str(alert["operator"]) + str(alert["threshold"]) + ". If you no longer "
            "wish to receive alerts refer to our documentation." ),alert["email"])

            mark_alert_triggered(alert["id"])

        elif not condition_met and alert["is_triggered"]:

            reset_alert(alert["id"])


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

#Email Debug
#if data["main"]["temp"]>10:
#    email_alert("Too hot", "It is too hot", "timotxp@gmail.com")


#Storing data in SQL database and sending alerts
#(time will break in 2038)
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

#Storing data
cursor.execute("INSERT INTO weather (temp, time, pressure, wind_speed) VALUES (?,?,?,?)", (data["main"]["temp"], data["dt"], data["main"]["pressure"], data["wind"]["speed"]))
conn.commit()
conn.close()
#SENDING ALERTS
#Dictionaries for checking user input
OPERATORS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le
}

METRICS = {
    "temperature": "temp",
    "wind_speed": "wind_speed",
    "pressure": "pressure"
}

#Evaluation of alerts and sending emails
check_alerts(data)