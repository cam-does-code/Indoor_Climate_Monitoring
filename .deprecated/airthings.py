from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import RPi.GPIO as GPIO

class AirthingsAPI:
    def __init__(self, client_id, client_secret, influxdb_token, influxdb_org, influxdb_bucket, temp_led_pin, co2_led_pin):
        self.client_id = client_id
        self.client_secret = client_secret
        self.influxdb_token = influxdb_token
        self.influxdb_org = influxdb_org
        self.influxdb_bucket = influxdb_bucket
        self.base_url = 'https://api.airthings.com/v1/'
        self.temp_led_pin = temp_led_pin
        self.co2_led_pin = co2_led_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.temp_led_pin, GPIO.OUT)
        GPIO.setup(self.co2_led_pin, GPIO.OUT)

    def get_access_token(self):
        auth_url = 'https://accounts.airthings.com/connect/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(auth_url, data=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print("Failed to fetch access token:", response.text)
            return None

    def fetch_data(self, access_token, device_id):
        endpoint = f'devices/{device_id}/latest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            temperature = data.get('temperature', {}).get('value')
            co2_level = data.get('co2', {}).get('value')
            return temperature, co2_level
        else:
            print("Failed to fetch data:", response.text)
            return None, None

    def write_to_influxdb(self, temperature, co2_level):
        client = InfluxDBClient(url="http://localhost:8086", token=self.influxdb_token)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        data = [
            {
                "measurement": "environment_data",
                "tags": {"device": "airthings_sensor"},
                "fields": {"temperature": temperature, "co2_level": co2_level}
            }
        ]

        write_api.write(self.influxdb_bucket, self.influxdb_org, data)

    def control_led(self, temperature, co2_level):
        if temperature is not None and temperature > 25:
            GPIO.output(self.temp_led_pin, GPIO.HIGH)
        else:
            GPIO.output(self.temp_led_pin, GPIO.LOW)

        if co2_level is not None and co2_level > 2000:
            GPIO.output(self.co2_led_pin, GPIO.HIGH)
        else:
            GPIO.output(self.co2_led_pin, GPIO.LOW)

if __name__ == "__main__":
    # Replace with your Airthings API client ID and client secret
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    
    # Replace with your InfluxDB credentials
    influxdb_token = 'your_influxdb_token'
    influxdb_org = 'your_influxdb_org'
    influxdb_bucket = 'your_influxdb_bucket'

    # Replace with your device ID
    device_id = 'your_device_id'

    # Replace with the GPIO pins connected to the LEDs
    temp_led_pin = 23
    co2_led_pin = 24

    airthings_api = AirthingsAPI(client_id, client_secret, influxdb_token, influxdb_org, influxdb_bucket, temp_led_pin, co2_led_pin)
    access_token = airthings_api.get_access_token()
    if access_token:
        temperature, co2_level = airthings_api.fetch_data(access_token, device_id)
        if temperature is not None and co2_level is not None:
            print("Temperature:", temperature, "°C")
            print("CO2 Level:", co2_level, "ppm")
            airthings_api.write_to_influxdb(temperature, co2_level)
            airthings_api.control_led(temperature, co2_level)
            print("Data written to InfluxDB successfully.")
        else:
            print("Failed to fetch temperature and CO2 level data.")
    else:
        print("Failed to fetch access token.")
