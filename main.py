import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "udemyshitikanthapython@gmail.com"
PASSWORD = "ijdkawaabzslthyw"
MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_latitude - 5 <= MY_LAT <= iss_latitude + 5 and iss_longitude - 5 <= MY_LONG <= iss_longitude + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    my_time = time_now.hour

    if my_time >= sunset or my_time <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="nshitikantha@gmail.com",
                                msg=f"Subject:Look Up\n\nThe ISS is above you in the sky..")
