# Plant Intelligence Platform

A hardware-independent plant perception and autonomous care platform.

## Vision

Build a software platform that can start with a balcony garden and evolve toward mobile robotics and drone-based plant intelligence.

The core pipeline is:

Camera / Sensors
→ Perception
→ Sensor Fusion
→ Plant State
→ Decision
→ Safety Validation
→ Actuator

The intelligence layer must not depend on a specific camera, microcontroller, or actuator.

## Initial target

- Raspberry Pi 5 edge computer
- Raspberry Pi Camera Module 3 NoIR
- ESP32-WR04 for sensors and irrigation control
- Python 3.11+
- FastAPI
- OpenCV
- MQTT
- SQLite initially
- pytest

Hardware integration is deliberately separated behind ports/adapters.

## Architecture

The project follows a hexagonal / ports-and-adapters architecture:

- `domain/` — pure business models
- `ports/` — hardware-independent interfaces
- `adapters/` — physical/device implementations
- `vision/` — image perception
- `intelligence/` — fusion and decisions
- `orchestration/` — workflows
- `api/` — external API
- `persistence/` — storage

No hardware SDK should leak into the domain layer.

## Development

Create a virtual environment and install development dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Raspberry Pi
source .venv/bin/activate

pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```


## Deployment

See `docs/DEPLOYMENT_GUIDE.md` for Raspberry Pi, camera, MQTT, ESP32, safety, and scheduled-monitoring setup.

For unattended Raspberry Pi operation:

1. Set `HARDWARE_MODE=pi` in `.env`.
2. Verify the ESP32 reports `READY`.
3. Test the camera independently.
4. Run a manual monitoring cycle.
5. Install the systemd service and timer from `deploy/systemd/`.
6. Start with one irrigation zone and a physical emergency cutoff.

The default hardware mode is `mock`; real hardware is opt-in.
