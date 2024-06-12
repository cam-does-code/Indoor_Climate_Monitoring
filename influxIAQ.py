import influxdb_client
import os
import time
import json
from urllib import request, parse, error
import base64
from gpiozero import LED

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# GPIO pins til LEDer
CO2_LED_PIN = 24 
TEMP_LED_PIN = 25 
TEMP_COLD_LED_PIN = 18

co2_led = LED(CO2_LED_PIN)
temp_led = LED(TEMP_LED_PIN)
kold_led = LED(TEMP_COLD_LED_PIN)

client_id = "9874bb3c-c43c-4642-80ff-d607dbe9a562"
device_id = "2960012551"
client_secret = "fc22b135-d73d-40a6-a575-6d4830d8a35a"
authorisation_url = "https://accounts-api.airthings.com/v1/token"
device_url = f"https://ext-api.airthings.com/v1/devices/{device_id}/latest-samples"
token_req_payload = {
    "grant_type": "client_credentials",
    "scope": "read:device:current_values",
}

# client_id og client_secret for Authorization header
credentials = f"{client_id}:{client_secret}"
credentials_encoded = base64.b64encode(credentials.encode()).decode()

# InfluxDB konfiguration
token = "FRaiM5my-51qNaEg9BqHzW7c6qiQ7R6uBkRgkGZ1eWygZp2Ya3r3lOIVK9xBaOwQasCoabZKt4RoMt6i9HHZ8A=="  
org = "UCL"
url = "http://localhost:8086"
bucket = "afgangsprojekt"  

# Initialiser InfluxDB client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    # Request Access Token fra auth server
    try:
        token_data = parse.urlencode(token_req_payload).encode()
        token_request = request.Request(authorisation_url, data=token_data)
        token_request.add_header("Authorization", f"Basic {credentials_encoded}")

        with request.urlopen(token_request) as token_response:
            token_json = token_response.read()
            token_data = json.loads(token_json.decode())
            token = token_data["access_token"]
    except error.HTTPError as e:
        print(f"Error retrieving access token: {e}")
        exit(1)

    # Få seneste data fra Airthings API.
    try:
        device_request = request.Request(device_url)
        device_request.add_header("Authorization", f"Bearer {token}")

        with request.urlopen(device_request) as response:
            device_json = response.read()
            device_data = json.loads(device_json.decode())
    except error.HTTPError as e:
        print(f"Error retrieving device data: {e}")
        exit(1)

    # temp og co2 fra json
    co2 = int(device_data["data"]["co2"])
    temperature = int(device_data["data"]["temp"])

    print(f"CO2: {co2} ppm")
    print(f"Temperature: {temperature} °C")

    # send data til InfluxDB
    point = (
        Point("air_quality")
        .tag("device_id", device_id)
        .field("co2", co2)
        .field("temperature", temperature)
    )
    write_api.write(bucket=bucket, record=point)

    # LED styring
    if co2 > 1000:
        co2_led.on()
    else:
        co2_led.off()

    if temperature < 19:
        kold_led.on()
    else:
        kold_led.off()

    if temperature > 22:
        temp_led.on()
    else:
        temp_led.off()

    time.sleep(150)
