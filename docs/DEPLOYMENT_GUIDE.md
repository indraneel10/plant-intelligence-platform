# Plant Intelligence Platform — Deployment Guide

## 1. Target architecture

Raspberry Pi 5 runs the Python/FastAPI intelligence service.

Raspberry Pi Camera Module 3 provides images.

ESP32-WR04 reads sensors and controls the pump/valves.

MQTT connects the Pi and ESP32 on the local network.

SQLite stores the initial history.

## 2. Raspberry Pi setup

Use Raspberry Pi OS 64-bit.

Install system packages:

    sudo apt update
    sudo apt install -y python3-venv python3-pip mosquitto mosquitto-clients

Enable MQTT:

    sudo systemctl enable --now mosquitto

Clone the repository:

    git clone https://github.com/indraneel10/plant-intelligence-platform
    cd plant-intelligence-platform

Create the environment:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-pi.txt

Create configuration:

    cp .env.example .env

Set MQTT_BROKER_HOST to the Pi address if the broker is on another machine.

## 3. Camera

Verify the Camera Module 3 with Raspberry Pi camera tools before starting the application.

The application adapter is:

    app.adapters.cameras.raspberry_pi.RaspberryPiCamera

Images are written to IMAGE_DIR.

## 4. ESP32

Open:

    firmware/esp32_wr04/esp32_wr04.ino

Set Wi-Fi and MQTT broker values.

Verify the GPIO mapping against the actual relay board.

Flash the ESP32 and verify it reports READY on:

    plant/actuators/status

## 5. Start the API

    source .venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000

Health check:

    curl http://127.0.0.1:8000/health

## 6. Register a plant

    curl -X POST http://127.0.0.1:8000/plants       -H 'Content-Type: application/json'       -d '{"plant_id":"plant-001","name":"Basil","species":"Ocimum basilicum","zone_id":"zone-1","location_label":"Balcony"}'

## 7. Monitoring

The platform should eventually run the monitoring cycle every 48 hours.

For development, invoke the monitoring endpoint manually:

    curl -X POST http://127.0.0.1:8000/monitor/plant-001/run

The current endpoint is a development integration path and uses mock devices. Before enabling unattended irrigation, wire the real camera, sensor, actuator and persistence dependencies.

## 8. Safety checklist

Before connecting the pump:

- test every valve without water
- verify relay polarity
- verify pump current is within relay/driver limits
- verify a tank-empty signal
- verify maximum runtime
- verify ESP32 boot leaves outputs OFF
- test MQTT disconnect behavior
- provide a physical emergency cutoff
- never expose MQTT to the internet

## 9. Production evolution

For a permanent installation:

- replace SQLite with managed PostgreSQL
- add authenticated API access
- use MQTT authentication and TLS
- add persistent device identity
- add watchdog/reconnect handling
- add actuator acknowledgements
- add audit logging
- add scheduled capture as a system service
- back up image and observation data

## 10. AI limitations

The initial OpenCV vision engine is a V0 perception system. It is not a disease diagnostic system.

Use it for image quality, canopy/green coverage and conservative stress signals first. ML disease/pest models should be introduced only after collecting representative labelled images.
