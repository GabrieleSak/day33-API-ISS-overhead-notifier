import smtplib
import time
from datetime import datetime
import requests
from topsecret import *

MY_LAT = 54.687157
MY_LNG = 25.279652


def is_iss_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    iss_position = (iss_latitude, iss_longitude)
    print(iss_position)

    if (abs(MY_LAT - iss_latitude) <= 5) & (abs(MY_LNG - iss_longitude) <= 5):
        return True


def is_it_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    response = requests.get(url=" https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise)
    print(sunset)

    time_now = datetime.now()
    print(time_now.hour)

    if (time_now.hour <= sunrise) | (time_now.hour >= sunset):
        return True


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject:Look up! ISS is close\n\nISS is close to your position."
        )

print(is_iss_close())
print(is_it_dark())

while True:
    time.sleep(60)
    if is_iss_close() and is_it_dark():
        send_email()

