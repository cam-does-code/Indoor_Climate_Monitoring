import json
from urllib import request, parse, error
import base64
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for LEDs
CO2_LED_PIN = 18  # Change this to the GPIO pin connected to the CO2 LED
TEMP_LED_PIN = 23  # Change this to the GPIO pin connected to the temperature LED

GPIO.setmode(GPIO.BCM)
GPIO.setup(CO2_LED_PIN, GPIO.OUT)
GPIO.setup(TEMP_LED_PIN, GPIO.OUT)

client_id = "9874bb3c-c43c-4642-80ff-d607dbe9a562"
device_id = "2960012551"
client_secret = "fc22b135-d73d-40a6-a575-6d4830d8a35a"
authorisation_url = "https://accounts-api.airthings.com/v1/token"
device_url = f"https://ext-api.airthings.com/v1/devices/{device_id}/latest-samples"
token_req_payload = {
    "grant_type": "client_credentials",
    "scope": "read:device:current_values",
}

# Encode client_id and client_secret for the Authorization header
credentials = f"{client_id}:{client_secret}"
credentials_encoded = base64.b64encode(credentials.encode()).decode()

while True:
    # Request Access Token from auth server
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

    # Get the latest data for the device from the Airthings API.
    try:
        device_request = request.Request(device_url)
        device_request.add_header("Authorization", f"Bearer {token}")

        with request.urlopen(device_request) as response:
            device_json = response.read()
            device_data = json.loads(device_json.decode())
    except error.HTTPError as e:
        print(f"Error retrieving device data: {e}")
        exit(1)

    # Extract CO2 and temperature data
    co2 = device_data["data"]["co2"]
    temperature = device_data["data"]["temp"]

    print(f"CO2: {co2} ppm")
    print(f"Temperature: {temperature} °C")

    # Control LEDs based on CO2 and temperature readings
    if co2 > 600:
        GPIO.output(CO2_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(CO2_LED_PIN, GPIO.LOW)

    if temperature > 25:
        GPIO.output(TEMP_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(TEMP_LED_PIN, GPIO.LOW)

    # Wait for 30 seconds before the next iteration
    time.sleep(30)

# Clean up GPIO (this part will never be reached in an infinite loop)
GPIO.cleanup()
