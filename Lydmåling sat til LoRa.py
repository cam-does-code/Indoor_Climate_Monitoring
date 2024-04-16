from SX1276_Tx import LoRa
from machine import Pin, ADC
import time

# Lydmåler konfiguration
sound_pin = 36  # Pin for lydsensoren
adc = ADC(Pin(sound_pin))
adc.width(ADC.WIDTH_10BIT)  # 10-bit opløsning
adc.atten(ADC.ATTN_11DB)     # Attenuation for 3.6V max range

# LoRa konfiguration TTGO LORA32
LoRa_MISO_Pin  = 19
LoRa_CS_Pin    = 18
LoRa_SCK_Pin   = 5
LoRa_MOSI_Pin  = 27
LoRa_G0_Pin    = 26  # DIO0_Pin
LoRa_EN_Pin    = 26
LoRa_RST_Pin   = 13
SPI_CH         = 1
LORA_DATARATE = "SF7BW125"
Pin(LoRa_EN_Pin, Pin.OUT).on()
lora = LoRa(LoRa_RST_Pin, LoRa_CS_Pin, SPI_CH, LoRa_SCK_Pin, LoRa_MOSI_Pin, LoRa_MISO_Pin, LoRa_G0_Pin)

lora.write('RegDioMapping1', lora.DioMapping['Dio0']['TxDone'])
lora.after_TxDone = lambda self: print('TxDone')

try:
    while True:
        # Mål lydniveauet
        sound_level = adc.read()

        # Lav payload med lydniveau og besked
        payload = "Sound Level: {} - sending message".format(sound_level)
        print(payload)

        # Send payload via LoRa
        lora.send(payload)
        
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped!")
