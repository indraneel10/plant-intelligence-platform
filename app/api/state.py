from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.persistence.database import get_db
from app.persistence.models import DecisionModel, PlantModel, PlantObservationModel, SensorObservationModel

router = APIRouter(prefix="/plants", tags=["state"])


def _iso(value):
    return value.isoformat() if value else None


@router.get("/{plant_id}/state")
def plant_state(plant_id: str, db: Session = Depends(get_db)):
    plant = db.get(PlantModel, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    observation = (
        db.query(PlantObservationModel)
        .filter(PlantObservationModel.plant_id == plant_id)
        .order_by(PlantObservationModel.timestamp.desc())
        .first()
    )
    sensors = (
        db.query(SensorObservationModel)
        .filter(SensorObservationModel.plant_id == plant_id)
        .order_by(SensorObservationModel.timestamp.desc())
        .limit(20)
        .all()
    )
    decision = (
        db.query(DecisionModel)
        .filter(DecisionModel.plant_id == plant_id)
        .order_by(DecisionModel.created_at.desc())
        .first()
    )

    latest_sensors = {}
    for row in sensors:
        latest_sensors.setdefault(row.sensor_type, {
            "sensor_id": row.sensor_id,
            "value": row.value,
            "unit": row.unit,
            "zone_id": row.zone_id,
            "timestamp": _iso(row.timestamp),
        })

    return {
        "plant": {
            "plant_id": plant.plant_id,
            "name": plant.name,
            "species": plant.species,
            "zone_id": plant.zone_id,
            "location_label": plant.location_label,
        },
        "observation": None if observation is None else {
            "timestamp": _iso(observation.timestamp),
            "health_score": observation.health_score,
            "wilting_probability": observation.wilting_probability,
            "yellowing_probability": observation.yellowing_probability,
            "disease_probability": observation.disease_probability,
            "image_quality": observation.image_quality,
            "leaf_area_ratio": observation.leaf_area_ratio,
            "water_stress_probability": observation.water_stress_probability,
            "heat_stress_probability": observation.heat_stress_probability,
        },
        "sensors": latest_sensors,
        "latest_decision": None if decision is None else {
            "action": decision.action,
            "reason": decision.reason,
            "confidence": decision.confidence,
            "duration_seconds": decision.duration_seconds,
            "created_at": _iso(decision.created_at),
        },
    }
