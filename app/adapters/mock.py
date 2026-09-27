from datetime import datetime, timezone
from uuid import uuid4

from app.domain.action import Action
from app.domain.camera import CaptureMode, ImageFrame
from app.domain.sensor import SensorObservation, SensorType
from app.ports.actuator import ActuatorPort
from app.ports.camera import CameraPort
from app.ports.sensor import SensorPort

class MockCamera(CameraPort):
    def capture(self) -> ImageFrame:
        return ImageFrame(
            frame_id=str(uuid4()),
            camera_id="mock-camera",
            timestamp=datetime.now(timezone.utc),
            image_path="data/images/mock.jpg",
            capture_mode=CaptureMode.DAY_RGB,
        )

class MockSensor(SensorPort):
    def read_all(self) -> list[SensorObservation]:
        now = datetime.now(timezone.utc)
        return [
            SensorObservation("soil-1", SensorType.SOIL_MOISTURE, 25.0, "%", now, plant_id="plant-001", zone_id="zone-1"),
            SensorObservation("temp-1", SensorType.TEMPERATURE, 30.0, "C", now),
            SensorObservation("humidity-1", SensorType.HUMIDITY, 55.0, "%", now),
            SensorObservation("light-1", SensorType.LIGHT, 500.0, "lux", now),
        ]

class MockActuator(ActuatorPort):
    def __init__(self) -> None:
        self.executed: list[Action] = []

    def execute(self, action: Action) -> None:
        self.executed.append(action)
