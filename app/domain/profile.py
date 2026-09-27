from dataclasses import dataclass

@dataclass(frozen=True)
class PlantProfile:
    plant_id: str
    zone_id: str
    moisture_threshold: float = 30.0
    moisture_recovery_threshold: float = 45.0
    minimum_confidence: float = 0.60
    max_irrigation_seconds: int = 60
    cooldown_seconds: int = 3600
