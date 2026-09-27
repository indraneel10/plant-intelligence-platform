# ESP32-WR04 Actuator Gateway

Platform owns authorization and safety; ESP32 owns GPIO and physical actuation.

Contract: POST /v1/actuators/irrigation

Request: {"action_type":"water","zone_id":"zone-1","duration_seconds":30}

Response: {"status":"accepted","zone_id":"zone-1","duration_seconds":30}

Firmware must reject malformed requests, unknown zones, non-positive durations, and durations above its hardware maximum. Outputs default OFF at boot and on invalid requests. Do not expose the device directly to the public internet; use a trusted local network and an authenticated gateway/mTLS in production.
