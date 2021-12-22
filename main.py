import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = "AC4662cc37adeab603a2cc509a3ffc9e0b"
auth_token = os.environ.get("AUTH_TOKEN")

WEB_API = "https://api.openweathermap.org/data/2.5/onecall"
KEY = os.environ.get("OWM_API_KEY")

MY_LAT = 52.5162494077299
MY_LNG = 13.377701674153512

parameters = {
    "lat":MY_LAT,
    "lon":MY_LNG,
    "exclude":"current,minutely,daily,alerts",
    "appid": KEY
}

response = requests.get(WEB_API, params=parameters)
response.raise_for_status()
forecast = response.json()["hourly"][:12]

rain = False
for hour_data in forecast:
    if hour_data['weather'][0]['id'] < 700:
        rain = True

if rain:
    msg = "It's going to rain in the next 12 hours! Take an umbrella ☂"
    print(msg)
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body=msg,
        from_='+16205914391',
        to=os.environ.get("MY_PHONE")
    )

    print(message.status)
else:
    print("It's not going to rain in the next 12 hours! Enjoy your day!")
