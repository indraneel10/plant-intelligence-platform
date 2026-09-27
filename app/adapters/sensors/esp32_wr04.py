from app.domain.sensor import SensorObservation, SensorType
from app.ports.sensor import SensorPort
from app.adapters.messaging.mqtt import MqttClient

class Esp32WR04SensorAdapter(SensorPort):
    def __init__(self, mqtt: MqttClient, topic: str = "plant/sensors"):
        self.mqtt = mqtt
        self.topic = topic
        self._latest: list[SensorObservation] = []

    def start(self) -> None:
        self.mqtt.subscribe_json(self.topic, self._on_message)

    def _on_message(self, payload: dict) -> None:
        from datetime import datetime
        timestamp = datetime.fromisoformat(payload["timestamp"])
        self._latest = [
            SensorObservation(
                sensor_id=item["sensor_id"],
                sensor_type=SensorType(item["sensor_type"]),
                value=float(item["value"]),
                unit=item["unit"],
                timestamp=timestamp,
                plant_id=item.get("plant_id"),
                zone_id=item.get("zone_id"),
            )
            for item in payload.get("readings", [])
        ]

    def read_all(self) -> list[SensorObservation]:
        return list(self._latest)
