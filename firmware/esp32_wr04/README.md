# ESP32-WR04 firmware

This is the reference firmware contract for the balcony controller.

## Safety behavior

The controller independently enforces:

- all outputs OFF at boot
- only four valid zones
- positive duration
- maximum irrigation runtime
- invalid-command rejection
- automatic shutdown after timeout
- pump and valve shutdown together

Do not treat the Pi/AI as a safety controller. The ESP32 remains the last local enforcement layer.

## Hardware mapping

The example uses:

- GPIO 25: pump relay
- GPIO 26: zone 1 valve
- GPIO 27: zone 2 valve
- GPIO 32: zone 3 valve
- GPIO 33: zone 4 valve

Verify the actual ESP32-WR04 board pinout and relay active-high/active-low behavior before connecting a pump or valve.

## MQTT

Subscribe:

plant/actuators/command

Publish:

plant/actuators/status

The production firmware should also publish sensor telemetry on:

plant/sensors

Never expose MQTT directly to the public internet.
