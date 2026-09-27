from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.domain.plant import Plant, PlantObservation
from app.domain.sensor import SensorObservation
from app.domain.decision import Decision
from app.domain.action import Action
from app.persistence.models import PlantModel, PlantObservationModel, SensorObservationModel, DecisionModel, IrrigationActionModel

class PlantRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_plant(self, plant: Plant) -> None:
        model = self.db.get(PlantModel, plant.plant_id)
        if model is None:
            model = PlantModel(plant_id=plant.plant_id, name=plant.name)
        model.name = plant.name
        model.species = plant.species
        model.zone_id = plant.zone_id
        model.location_label = plant.location_label
        self.db.add(model)
        self.db.commit()

    def save_sensor_observations(self, readings: list[SensorObservation]) -> None:
        self.db.add_all([
            SensorObservationModel(sensor_id=r.sensor_id, plant_id=r.plant_id, zone_id=r.zone_id,
                                   sensor_type=r.sensor_type.value, value=r.value, unit=r.unit, timestamp=r.timestamp)
            for r in readings
        ])
        self.db.commit()

    def save_plant_observation(self, observation: PlantObservation) -> None:
        self.db.add(PlantObservationModel(
            plant_id=observation.plant_id, timestamp=observation.timestamp,
            health_score=observation.health_score, wilting_probability=observation.wilting_probability,
            yellowing_probability=observation.yellowing_probability, disease_probability=observation.disease_probability,
            image_quality=observation.image_quality, leaf_area_ratio=observation.leaf_area_ratio,
            water_stress_probability=observation.water_stress_probability,
            heat_stress_probability=observation.heat_stress_probability))
        self.db.commit()

    def save_decision(self, decision: Decision) -> None:
        self.db.add(DecisionModel(
            plant_id=decision.plant_id, action=decision.action.value, reason=decision.reason,
            confidence=decision.confidence, duration_seconds=decision.duration_seconds,
            created_at=decision.created_at or datetime.now(timezone.utc)))
        self.db.commit()

    def save_action(self, plant_id: str, action: Action) -> None:
        self.db.add(IrrigationActionModel(
            plant_id=plant_id, zone_id=action.zone_id, action_type=action.action_type.value,
            duration_seconds=action.duration_seconds, executed_at=datetime.now(timezone.utc)))
        self.db.commit()
