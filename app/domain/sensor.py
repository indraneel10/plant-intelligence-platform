from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class SensorType(StrEnum):
    SOIL_MOISTURE = "soil_moisture"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LIGHT = "light"
    WATER_LEVEL = "water_level"

@dataclass(frozen=True)
class SensorObservation:
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: datetime
    plant_id: str | None = None
    zone_id: str | None = None
