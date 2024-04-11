from SX1276_Tx import LoRa
from machine import Pin
import time

# LoRa configuration TTGO LORA32
LoRa_MISO_Pin  = 19
LoRa_CS_Pin    = 18
LoRa_SCK_Pin   = 5
LoRa_MOSI_Pin  = 27
LoRa_G0_Pin    = 26  # DIO0_Pin
LoRa_EN_Pin    = 14
LoRa_RST_Pin   = 13
SPI_CH         = 1
LORA_DATARATE = "SF7BW125"
Pin(LoRa_EN_Pin, Pin.OUT).on()
lora = LoRa(LoRa_RST_Pin, LoRa_CS_Pin, SPI_CH, LoRa_SCK_Pin, LoRa_MOSI_Pin, LoRa_MISO_Pin, LoRa_G0_Pin)

lora.write('RegDioMapping1', lora.DioMapping['Dio0']['TxDone'])
lora.after_TxDone = lambda self: print('TxDone')

# Set frequency to match Raspberry Pi (915.0 MHz)
FREQ = 915000000  # Frequency in Hz
lora.write('RegFrfMsb', (FREQ >> 16) & 0xFF)
lora.write('RegFrfMid', (FREQ >> 8) & 0xFF)
lora.write('RegFrfLsb', FREQ & 0xFF)

try:
    while True:
        payload = "Sending message from LilyGO to Raspberry Pi"
        print("Sending: ", payload)
        lora.send(payload)
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped!")
