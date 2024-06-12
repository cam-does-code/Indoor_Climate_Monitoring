import socket
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from gpiozero import LED

# InfluxDB konfiguration
token = "FRaiM5my-51qNaEg9BqHzW7c6qiQ7R6uBkRgkGZ1eWygZp2Ya3r3lOIVK9xBaOwQasCoabZKt4RoMt6i9HHZ8A=="
org = "UCL"
url = "http://localhost:8086"
bucket = "afgangsprojekt"

# InfluxDB client
client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Socket konfiguration
HOST = '0.0.0.0'  # alle interfaces
PORT = 8080

sound_led = LED(17) 

# LED
def control_led(sound_level):
    if sound_level > 60:
        sound_led.on()
    else:
        sound_led.off()

# lav TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket til addresse og port
    s.bind((HOST, PORT))
    # Lyt efter forbindelser
    s.listen()

    print("Waiting for ESP32 connection...")

    while True:
        # Accepter forbindelse
        conn, addr = s.accept()
        with conn:
            print("Connected to ESP32 at", addr)
            while True:
                # modtag fra ESP32
                data = conn.recv(1024)
                if not data:
                    print("Connection closed by the ESP32.")
                    break
                # Decode data
                received_data = data.decode("utf-8")
                print("Received data:", received_data)
                
                # split så vi kun får tal
                parts = received_data.split(" dBA")
                if len(parts) == 2:
                    sound_measurement = float(parts[0].split()[-1])
                    print("Sound Measurement:", sound_measurement)
                    # LED
                    control_led(sound_measurement)
                    # data til InfluxDB
                    data_point = Point("sound_measurement").tag("device", "lora").field("measurement", sound_measurement)
                    write_api.write(bucket=bucket, org=org, record=data_point)

print("Server stopped.")
