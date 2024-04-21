#include <SPI.h>
#include <LoRa.h>

#define SS_PIN    5
#define RST_PIN   14
#define DI0_PIN   2

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  LoRa.setTxPower(20);

  // Initialize LoRa LED pin
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // Turn on LED

  // Send data packet
  LoRa.beginPacket();
  LoRa.print("Hello from LilyGO!");
  LoRa.endPacket();

  digitalWrite(LED_BUILTIN, LOW);   // Turn off LED
  delay(5000);  // Wait for 5 seconds before sending next packet
}
