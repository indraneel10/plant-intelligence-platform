# Plant Intelligence Platform — Deployment Guide

## 1. Deployment status

The software foundation is complete for the pre-hardware/PoC milestone. The next phase is physical commissioning and validation with the Raspberry Pi 5, Camera Module 3, ESP32-WR04, sensors, relay/driver, pump and valves.

Do not enable unattended physical irrigation until the hardware safety checks in this guide are complete.

## 2. Target architecture

- **Raspberry Pi 5** — edge AI compute, camera acquisition, local inference, edge runtime and offline queue.
- **Raspberry Pi Camera Module 3** — plant image acquisition.
- **Plant Intelligence FastAPI service** — plant state, history, AI Copilot, monitoring, decision and safety services.
- **ESP32-WR04** — deterministic sensor/actuator controller for sensors, relay, pump and irrigation valves.
- **SQLite** — current development/edge persistence. PostgreSQL is the recommended production evolution.

Core flow:

`Camera Module 3 → Raspberry Pi Edge Runtime → Vision Observation → Plant Intelligence → Sensor Fusion → Decision Engine → Safety Engine → Actuation Service → ESP32 → Pump/Valve`

The AI/Copilot must not directly control GPIO, relays, pumps or valves. Physical actions must pass through the platform safety and actuation layers.

## 3. Raspberry Pi 5 setup

Use 64-bit Raspberry Pi OS.

Install the base packages:

    sudo apt update
    sudo apt install -y python3-venv python3-pip python3-picamera2

Clone the repository:

    git clone https://github.com/indraneel10/plant-intelligence-platform
    cd plant-intelligence-platform

Create and activate the Python environment:

    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate

Install the repository dependencies using the dependency file currently maintained by the project. Keep Picamera2 from Raspberry Pi OS available to the virtual environment.

## 4. Camera Module 3 commissioning

Connect the Camera Module 3 with the Pi powered off. After boot, verify the camera with the Raspberry Pi camera utilities before running the platform.

The current application adapter is:

    app/edge/camera/raspberry_pi.py

The adapter uses Picamera2 and stores captured images under:

    data/plant-images/

The edge runtime is:

    app/edge/runtime/edge_agent.py

It performs:

`capture → vision inference → durable local queue`

The current vision inference implementation is a deterministic development placeholder. It must be replaced by a selected/trained and validated plant-vision model before production AI claims are made.

## 5. Edge offline operation

The Raspberry Pi edge runtime includes a durable SQLite observation queue:

    app/edge/storage/queue.py

This allows observations to be retained locally when the central API is unavailable. Pending observations can later be synchronized to the platform.

The platform ingestion endpoint is:

    POST /edge/v1/observations

Image IDs are treated idempotently so a retried observation does not create duplicate vision observations.

## 6. Start the FastAPI platform

Activate the environment:

    source .venv/bin/activate

Start the API:

    uvicorn app.main:app --host 0.0.0.0 --port 8000

Health check:

    curl http://127.0.0.1:8000/health

Open the generated API documentation during development at `/docs`.

## 7. Plant and monitoring validation

Register/configure the test plant through the plant API, then validate state and monitoring before connecting physical actuators.

Development monitoring endpoint:

    POST /monitor/{plant_id}/run

Validate that observations, sensor readings, decisions and audit events are persisted.

The hardware execution path must remain disabled/mock during initial Raspberry Pi and camera commissioning.

## 8. ESP32-WR04 integration

The ESP32 remains the real-time physical controller. The repository contains the actuator adapter and reference firmware contract under:

    app/adapters/esp32_wr04.py
    app/firmware/esp32_wr04/

The platform-side actuator contract uses:

    POST /v1/actuators/irrigation

Before flashing/using the firmware:

- verify the exact ESP32-WR04 board and GPIO mapping;
- verify relay/driver polarity;
- keep every output OFF at boot;
- validate one irrigation zone first;
- do not expose the ESP32 directly to the public internet.

The reference firmware is a prototype and must be commissioned against the actual hardware before physical irrigation is enabled.

## 9. Hardware commissioning sequence

Use this order:

1. Boot Raspberry Pi 5 and validate OS/network.
2. Validate Camera Module 3 capture independently.
3. Run the FastAPI platform and health check.
4. Validate Raspberry Pi edge capture and local queue.
5. Send a test vision observation to `/edge/v1/observations`.
6. Validate database/history and AI Copilot read paths.
7. Connect ESP32-WR04 without pump/valve loads and validate communication.
8. Connect and calibrate sensors.
9. Validate relay outputs with no water load.
10. Connect one appropriately protected pump/valve zone.
11. Run in shadow/manual mode: generate decisions but do not execute automatic irrigation.
12. Validate SafetyEngine decisions and audit trail.
13. Perform a supervised single-zone irrigation test.
14. Add emergency-stop, watchdog, command idempotency and device authentication before unattended operation.
15. Scale to additional zones only after the first zone passes commissioning.

## 10. Mandatory safety checklist

Before connecting or energizing a pump:

- verify relay/driver voltage and current ratings;
- verify pump current is within the switching hardware limits;
- verify electrical isolation/protection appropriate to the hardware;
- verify every valve independently;
- verify maximum irrigation runtime;
- implement/validate tank-empty or water-level protection;
- verify ESP32 boot and reset leave outputs OFF;
- verify communication-loss behavior;
- provide a physical emergency cutoff;
- keep AI unable to bypass SafetyEngine;
- keep physical execution disabled until supervised commissioning passes.

## 11. Production hardening remaining

Before production deployment:

- replace placeholder vision inference with a validated model and representative dataset;
- add device authentication and encrypted communication;
- add command IDs/idempotency and actuator acknowledgements;
- add ESP32 watchdog, non-blocking actuation and emergency stop;
- implement production identity (OIDC/OAuth2/JWT) instead of trusting actor headers;
- introduce formal database migrations;
- validate sensor freshness and water-level safety rules;
- add device heartbeat/status monitoring;
- replace or supplement SQLite with production PostgreSQL where appropriate;
- define image retention/backup policy;
- run long-duration reliability and failure-recovery tests.

## 12. Deployment acceptance criteria

The first physical milestone is complete only when one real plant demonstrates:

`Camera + sensor → edge observation → plant state → decision → safety check → approved actuator command → ESP32 → one pump/valve → recorded/audited result`

Until that test passes, describe the project as **software foundation complete; hardware commissioning in progress**.
