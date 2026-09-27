from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PlantState:
    plant_id: str
    timestamp: datetime
    health_score: float
    soil_moisture: float | None
    temperature: float | None
    humidity: float | None
    light: float | None
    water_stress: float
    heat_stress: float
    disease_risk: float
    confidence: float
