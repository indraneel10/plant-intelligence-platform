from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Plant:
    plant_id: str
    name: str
    species: str | None = None
    zone_id: str | None = None
    location_label: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class PlantObservation:
    plant_id: str
    timestamp: datetime
    health_score: float
    wilting_probability: float
    yellowing_probability: float
    disease_probability: float
    image_quality: float
    leaf_area_ratio: float | None = None
    water_stress_probability: float | None = None
    heat_stress_probability: float | None = None
