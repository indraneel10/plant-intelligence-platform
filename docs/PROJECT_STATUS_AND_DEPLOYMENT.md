# Plant Intelligence Platform — Project Status & Deployment Summary

## 1. Project objective

Build a plant-intelligence and autonomous irrigation platform that combines camera imagery, environmental sensors, plant history and AI-assisted interaction to assess plant condition, explain the state to a user and safely decide when irrigation is required.

## 2. Current architecture

**Raspberry Pi 5** = edge AI compute, Camera Module 3 integration, image capture, inference runtime and offline observation queue.  
**Raspberry Pi Camera Module 3** = plant image acquisition.  
**Plant Intelligence Platform / FastAPI** = APIs, persistence, monitoring, plant state, sensor fusion, decisions, safety, audit and AI Copilot.  
**ESP32-WR04** = deterministic sensor/actuator controller for sensors, relays, pump and valves.  
**Web application** = plant/operator interface and AI Copilot.

Core flow:

`Camera Module 3 → Raspberry Pi Edge Runtime → Vision Observation → Plant Intelligence → Sensor Fusion → Decision Engine → Safety Engine → Actuation Service → ESP32 → Pump/Valve`

AI is an orchestration/explanation layer and is not permitted to bypass the safety layer or directly drive physical GPIO/actuators.

## 3. Completed software milestone

The pre-hardware software foundation is complete. Implemented capabilities include:

- Hardware-independent ports/adapters architecture.
- FastAPI backend and persistence layer.
- Web application and AI Copilot foundation.
- Plant, sensor, observation, decision and irrigation history models.
- Monitoring orchestration and plant-state APIs.
- Sensor-fusion, decision and safety-engine integration.
- Agent v2 tool orchestration over actual platform state.
- Authorization foundation for action APIs.
- Persistent action/audit trail.
- Safe irrigation-request path that does not silently execute hardware.
- `ActuatorPort` abstraction and ESP32-WR04 platform adapter.
- ESP32-WR04 reference firmware/API contract.
- Raspberry Pi 5 edge-runtime architecture.
- Picamera2-based Camera Module 3 adapter.
- Pluggable `VisionInferencePort`.
- Local Raspberry Pi image storage path.
- Durable SQLite offline observation queue.
- Persistent `VisionObservation` model with device/image/model metadata.
- Idempotent `POST /edge/v1/observations` ingestion API.
- Automated backend tests and CI coverage for the major software paths.
- Agent v2 and Raspberry Pi edge-AI changes merged into the main development lineage.

## 4. Important current limitations

The project is **software-ready for hardware bring-up**, not a finished production autonomous irrigation product.

The following still require physical hardware, calibration, real data or production hardening:

- Raspberry Pi 5 commissioning on the target device.
- Camera Module 3 physical capture validation.
- Collection of representative plant images.
- Selection/training and validation of the production vision model; current edge inference is a development placeholder.
- Real sensor connection and calibration.
- ESP32 GPIO/relay/pump/valve commissioning.
- Water-level and sensor-freshness safety validation.
- Command idempotency and actuator acknowledgement.
- ESP32 watchdog/non-blocking runtime and emergency-stop behavior.
- Device authentication/encrypted communication.
- Production user authentication (OIDC/OAuth2/JWT).
- Formal database migrations and production database strategy.
- End-to-end physical testing and long-duration reliability testing.

## 5. Deployment plan

1. Install 64-bit Raspberry Pi OS on Raspberry Pi 5.
2. Install the application and Python environment.
3. Connect and validate Camera Module 3 using Raspberry Pi camera tooling.
4. Run the Raspberry Pi camera adapter and edge runtime.
5. Validate local image storage and the offline SQLite queue.
6. Send observations through `/edge/v1/observations` and verify persistence.
7. Run FastAPI/backend and AI Copilot against the test plant.
8. Connect ESP32-WR04 without physical irrigation loads first.
9. Connect and calibrate sensors.
10. Verify GPIO and relay/driver mapping against the real board.
11. Run decisions in shadow/manual mode with physical execution disabled.
12. Connect one protected pump/valve zone.
13. Validate safety, audit and supervised actuation end to end.
14. Add production device-security/reliability controls.
15. Scale to the remaining zones after the first zone passes commissioning.

See `docs/DEPLOYMENT_GUIDE.md` for the detailed procedure and safety checklist.

## 6. Current completion assessment

| Area | Current assessment |
|---|---:|
| Pre-hardware software/PoC foundation | **Complete for current milestone** |
| Raspberry Pi edge-AI software foundation | **Complete for hardware bring-up** |
| ESP32 software integration foundation | **Complete for hardware bring-up** |
| Physical hardware commissioning | **Not started / pending hardware validation** |
| Production plant-vision AI | **Not complete — model/data validation pending** |
| Production autonomous system | **Not complete** |

The key distinction is that the repository is now at a valid **software handoff point**. Additional speculative application features are lower priority than testing the software on the actual Raspberry Pi, Camera Module 3, ESP32 and sensors.

## 7. Immediate milestone — first physical demonstration

The next acceptance milestone is one real plant and one irrigation zone completing:

`Camera + soil/environment sensor → edge observation → sensor fusion → plant state → decision → safety check → ESP32 → one valve/pump → irrigation → persisted/audited result`

Start with supervised operation. Automatic irrigation should remain disabled until the hardware and failure modes have been validated.

## 8. Software/hardware responsibility

| Component | Primary responsibility |
|---|---|
| Raspberry Pi 5 | Edge compute, camera, inference, local queue |
| Camera Module 3 | Image acquisition |
| Plant Intelligence backend | State, history, decisions, safety, audit, APIs |
| AI Copilot | User interaction, explanation and tool orchestration |
| ESP32-WR04 | Sensor acquisition and deterministic actuator control |
| Relay/driver | Electrical switching |
| Pump/valves | Physical irrigation |

## 9. Long-term direction

The balcony deployment remains the first implementation of the broader **Plant Intelligence Platform**. The ports/adapters and edge-observation design allow future RGB, NoIR, thermal, multispectral or drone-derived imagery to feed the same core plant-state and decision architecture without coupling the intelligence layer to one camera or controller.
