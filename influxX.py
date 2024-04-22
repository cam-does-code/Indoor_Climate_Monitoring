import socket
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB configuration
token = "FRaiM5my-51qNaEg9BqHzW7c6qiQ7R6uBkRgkGZ1eWygZp2Ya3r3lOIVK9xBaOwQasCoabZKt4RoMt6i9HHZ8A=="
org = "UCL"
url = "http://localhost:8086"
bucket = "afgangsprojekt"

# Create InfluxDB client
client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Socket configuration
HOST = '0.0.0.0'  # All available interfaces
PORT = 8080

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()

    print("Waiting for ESP32 connection...")

    while True:
        # Accept a connection
        conn, addr = s.accept()
        with conn:
            print("Connected to ESP32 at", addr)
            while True:
                # Receive data from the ESP32
                data = conn.recv(1024)
                if not data:
                    print("Connection closed by the ESP32.")
                    break
                # Decode the received data
                received_data = data.decode("utf-8")
                print("Received data:", received_data)
                
                # Split the received data into parts
                parts = received_data.split(" dBA")
                if len(parts) == 2:
                    # Extract the sound measurement value
                    sound_measurement = parts[0].split()[-1]
                    print("Sound Measurement:", sound_measurement)
                    # Store data in InfluxDB
                    data_point = Point("sound_measurement").tag("device", "lora").field("measurement", float(sound_measurement))
                    write_api.write(bucket=bucket, org=org, record=data_point)

print("Server stopped.")
