#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

// LoRaWAN NwkSKey, network session key
static const PROGMEM u1_t NWKSKEY[16] = { /* Your NWKSKEY here */ };

// LoRaWAN AppSKey, application session key
static const u1_t PROGMEM APPSKEY[16] = { /* Your APPSKEY here */ };

// LoRaWAN end-device address
static const u4_t DEVADDR = /* Your DEVADDR here */ ;

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 18,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 14,
    .dio = {26, 33, 32},
};

void os_getArtEui(u1_t *buf) {
    // Not used
}

void os_getDevEui(u1_t *buf) {
    // Not used
}

void os_getDevKey(u1_t *buf) {
    // Not used
}

void onEvent(ev_t ev) {
    // Not used
}

void setup() {
    Serial.begin(115200);

    // LMIC init
    os_init();
    LMIC_reset();
    LMIC_setSession(0x1, DEVADDR, NWKSKEY, APPSKEY);
    LMIC_setupChannel(0, 868000000, DR_RANGE_MAP(DR_SF7, DR_SF12), BAND_CENTI);  // Channel 0, 868.0 MHz
}

void loop() {
    // Transmit data periodically
    // Replace this with your data transmission logic
    LMIC_setTxData2(1, (uint8_t *)"Hello, LoRa!", 12, 0);
    delay(5000);  // Delay for 5 seconds before next transmission
}
