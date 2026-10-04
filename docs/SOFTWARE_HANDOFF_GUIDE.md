# Plant Intelligence Platform — Software Handoff Guide

## Current handoff status

The software foundation is complete for the current pre-hardware PoC milestone. The repository is ready for Raspberry Pi 5, Camera Module 3 and ESP32-WR04 hardware bring-up.

## Software delivered

- FastAPI platform and persistence.
- Web application and AI Copilot foundation.
- Plant state, monitoring, sensor fusion, decision and safety layers.
- Agent v2 tool orchestration.
- Authorization foundation and persistent audit events.
- Raspberry Pi 5 edge runtime.
- Camera Module 3 Picamera2 adapter.
- Pluggable vision-inference interface.
- Local image storage and durable offline SQLite queue.
- Edge observation ingestion API with duplicate protection.
- ESP32-WR04 actuator adapter and firmware/API contract.
- Automated tests and CI foundation.

## Hardware team handoff

### Raspberry Pi 5

1. Install 64-bit Raspberry Pi OS.
2. Connect Camera Module 3 with power removed.
3. Validate the camera independently.
4. Clone and run the platform in a Python virtual environment.
5. Validate edge image capture and local queue.
6. Validate upload to `/edge/v1/observations`.

### ESP32-WR04

1. Confirm exact board and GPIO mapping.
2. Flash/test reference firmware without pump/valve load.
3. Validate sensors and relay outputs independently.
4. Confirm outputs remain OFF at boot/reset/failure.
5. Connect only one protected irrigation zone for the first integrated test.

## First acceptance test

One real plant should complete:

`Camera + sensor → edge observation → plant state → decision → safety → ESP32 → one pump/valve → persisted/audited result`

Use supervised/manual or shadow operation first. Do not enable unattended watering until hardware safety, emergency-stop, watchdog, command idempotency and communication security have been validated.

## AI status

The AI/Copilot and vision software interfaces are implemented. The edge vision model is currently a deterministic development placeholder. A production plant-health/disease model requires representative real images, model selection/training and validation.

## Project wording for stakeholders

**Software foundation complete for the current PoC milestone; hardware commissioning and production AI-model validation are the next phase.**

For detailed setup and safety instructions, use `docs/DEPLOYMENT_GUIDE.md`. For the full completion matrix and remaining work, use `docs/PROJECT_STATUS_AND_DEPLOYMENT.md`.
