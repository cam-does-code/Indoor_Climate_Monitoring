from flask import Flask, request, jsonify
from influxdb import InfluxDBClient

app = Flask(__name__)

# InfluxDB configuration
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = "admin"
INFLUXDB_PASSWORD = "your_password"
INFLUXDB_DATABASE = "sound_measurements"

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USERNAME, password=INFLUXDB_PASSWORD, database=INFLUXDB_DATABASE)

# Create a route to receive sound data
@app.route('/sound_data', methods=['POST'])
def receive_sound_data():
    data = request.json
    sound_level = data.get('sound_level')
    SNR = data.get('SNR')
    RSSI = data.get('RSSI')
    
    # Store data in InfluxDB
    json_body = [
        {
            "measurement": "sound_level",
            "fields": {
                "value": float(sound_level),
                "SNR": float(SNR),
                "RSSI": float(RSSI)
            }
        }
    ]
    client.write_points(json_body)
    
    return jsonify({"message": "Sound data received and stored successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
