# Plant Intelligence Platform — Status & Deployment Guide

## 1. Project objective

Build an autonomous plant monitoring and irrigation platform that combines camera imagery, environmental sensors and plant history to assess plant condition and safely decide when irrigation is required.

## 2. Current architecture

**Raspberry Pi 5** = edge intelligence and orchestration  
**ESP32-WR04** = real-time sensor and actuator controller  
**MQTT** = communication between Pi and ESP32  
**Raspberry Pi Camera Module 3 NoIR** = initial plant camera

Core flow:

`Camera → Vision → Sensor Fusion → Plant State → Decision Engine → Safety Engine → MQTT → ESP32 → Pump/Valve`

## 3. Completed

- Hardware-independent software architecture using ports/adapters.
- Raspberry Pi camera adapter.
- OpenCV-based V0 plant perception and image-quality checks.
- Sensor-fusion and plant-state pipeline.
- Decision engine: **Water / Inspect / No Action**.
- Safety layer before actuator execution.
- ESP32/MQTT sensor and actuator communication framework.
- Database/history for plants, sensor readings, observations, decisions and irrigation actions.
- REST API for plant registration, history and monitoring.
- Scheduled monitoring framework for Raspberry Pi.
- ESP32 firmware foundation for pump and four irrigation zones.
- Deployment documentation.

## 4. Remaining

- Connect and calibrate the actual sensors.
- Finalize pump, valve and relay/driver hardware integration.
- Implement/validate water-level and sensor-freshness safety checks.
- Complete end-to-end testing with real plants.
- Build and validate a production plant-health/disease AI model and dataset.
- Add stronger historical trend and plant-specific intelligence.
- Build dashboard/mobile UI.
- Add production security, reliability, actuator acknowledgements and watchdogs.

## 5. Deployment plan

1. Install 64-bit Raspberry Pi OS on the Raspberry Pi 5.
2. Install the application, Python dependencies and MQTT broker.
3. Connect and validate the Camera Module 3 NoIR.
4. Flash ESP32-WR04 firmware and configure Wi-Fi/MQTT.
5. Connect and calibrate sensors.
6. Connect one pump and one valve through an appropriately rated driver/relay and protection circuitry.
7. Run in **manual/shadow mode** first: record decisions without automatic watering.
8. Enable controlled autonomous irrigation after safety and calibration tests.
9. Scale from one zone to all four zones.

See `docs/DEPLOYMENT_GUIDE.md` for the detailed installation and hardware checklist.

## 6. Software completion

| Area | Current assessment |
|---|---:|
| Prototype software foundation | **~70–75%** |
| Production-ready autonomous system | **~40–50%** |
| Production-grade plant perception AI | **~15–20%** |

The 70–75% figure refers to the **prototype software architecture and core workflow**, not a claim that the final autonomous product is production-ready. Real hardware validation, calibration, AI model development, reliability and security remain.

## 7. Immediate milestone

### First End-to-End Physical Demonstration

One real plant should complete:

`Camera + soil sensor → analysis → sensor fusion → decision → safety check → ESP32 → one valve/pump → irrigation → recorded result`

Start with one plant and one irrigation zone before expanding to four zones.

## 8. Long-term direction

The balcony system is the first deployment of a broader **Plant Intelligence Platform**. The perception layer is hardware-independent so future RGB, thermal, multispectral and drone imagery can use the same core intelligence architecture.
