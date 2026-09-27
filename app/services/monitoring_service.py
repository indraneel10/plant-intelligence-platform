from sqlalchemy.orm import Session

from app.adapters.mock import MockActuator, MockCamera, MockSensor
from app.domain.profile import PlantProfile
from app.intelligence.decision_engine import DecisionEngine
from app.intelligence.safety_engine import SafetyEngine
from app.intelligence.sensor_fusion import SensorFusionEngine
from app.orchestration.plant_monitor import PlantMonitor
from app.persistence.models import PlantModel
from app.vision.engine import RuleBasedVisionEngine


class SqlAlchemyMonitorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_plant_observation(self, observation) -> None:
        from app.persistence.models import PlantObservationModel
        self.db.add(PlantObservationModel(
            plant_id=observation.plant_id,
            timestamp=observation.timestamp,
            health_score=observation.health_score,
            wilting_probability=observation.wilting_probability,
            yellowing_probability=observation.yellowing_probability,
            disease_probability=observation.disease_probability,
            image_quality=observation.image_quality,
            leaf_area_ratio=observation.leaf_area_ratio,
            water_stress_probability=observation.water_stress_probability,
            heat_stress_probability=observation.heat_stress_probability,
        ))

    def save_sensor_observations(self, readings) -> None:
        from app.persistence.models import SensorObservationModel
        for reading in readings:
            self.db.add(SensorObservationModel(
                sensor_id=reading.sensor_id,
                plant_id=reading.plant_id,
                zone_id=reading.zone_id,
                sensor_type=reading.sensor_type.value,
                value=reading.value,
                unit=reading.unit,
                timestamp=reading.timestamp,
            ))

    def save_decision(self, decision) -> None:
        from app.persistence.models import DecisionModel
        self.db.add(DecisionModel(
            plant_id=decision.plant_id,
            action=decision.action.value,
            reason=decision.reason,
            confidence=decision.confidence,
            duration_seconds=decision.duration_seconds,
            created_at=decision.created_at,
        ))

    def save_action(self, plant_id, action) -> None:
        from datetime import datetime, timezone
        from app.persistence.models import IrrigationActionModel
        self.db.add(IrrigationActionModel(
            plant_id=plant_id,
            zone_id=action.zone_id,
            action_type=action.action_type.value,
            duration_seconds=action.duration_seconds,
            executed_at=datetime.now(timezone.utc),
        ))

    def commit(self) -> None:
        self.db.commit()


def run_monitoring_cycle(db: Session, plant_id: str) -> dict:
    plant = db.get(PlantModel, plant_id)
    if plant is None:
        return {"status": "rejected", "plant_id": plant_id, "reason": "Plant not found"}
    if not plant.zone_id:
        return {"status": "rejected", "plant_id": plant_id, "reason": "Plant has no irrigation zone configured"}

    profile = PlantProfile(plant_id=plant_id, zone_id=plant.zone_id)
    actuator = MockActuator()
    repository = SqlAlchemyMonitorRepository(db)
    monitor = PlantMonitor(
        MockCamera(), MockSensor(), RuleBasedVisionEngine(), actuator,
        DecisionEngine(), SafetyEngine(), SensorFusionEngine(), repository=repository,
    )
    result = monitor.run_once(profile, tank_level=100.0)
    repository.commit()
    return {
        "status": "completed",
        "plant_id": plant_id,
        "frame_id": result.frame_id,
        "health_score": result.observation.health_score,
        "decision": result.decision.action.value,
        "reason": result.decision.reason,
        "confidence": result.decision.confidence,
        "action": result.action.action_type.value if result.action else None,
        "zone_id": result.action.zone_id if result.action else None,
        "duration_seconds": result.action.duration_seconds if result.action else 0,
        "actuator_mode": "mock",
        "hardware_executed": False,
    }
