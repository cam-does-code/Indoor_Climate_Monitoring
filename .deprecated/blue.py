import bluetooth

# Define ESP32 Bluetooth MAC address (in all caps)
esp32_mac_address = "24:D7:EB:0F:C9:64"

# Define Bluetooth UUID for the service (Serial Port Profile)
bt_uuid = "00001101-0000-1000-8000-00805F9B34FB"

print("Raspberry Pi: Attempting to connect to ESP32...")
# Connect to ESP32
esp32_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
try:
    esp32_socket.connect((esp32_mac_address, 1))
    print("Raspberry Pi: Connected to ESP32")

    try:
        while True:
            # Continuously receive data from ESP32
            received_data = esp32_socket.recv(1024)
            if received_data:
                print("Raspberry Pi: Received from ESP32:", received_data.decode())

    except KeyboardInterrupt:
        pass

    finally:
        esp32_socket.close()

except Exception as e:
    print("Raspberry Pi: Error connecting to ESP32:", e)
