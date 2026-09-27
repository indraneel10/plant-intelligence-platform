from sqlalchemy.orm import Session
from app.api.state import plant_state
from app.persistence.models import PlantModel


def get_plant_state(db: Session, plant_id: str) -> dict:
    return plant_state(plant_id, db)


def get_current_sensor_state(db: Session, plant_id: str) -> dict:
    state = plant_state(plant_id, db)
    return {"plant_id": plant_id, "sensors": state["sensors"]}


def get_latest_vision_analysis(db: Session, plant_id: str) -> dict:
    state = plant_state(plant_id, db)
    return {"plant_id": plant_id, "observation": state["observation"]}


def get_current_decision(db: Session, plant_id: str) -> dict:
    state = plant_state(plant_id, db)
    return {"plant_id": plant_id, "decision": state["latest_decision"]}


def get_recent_events(db: Session, plant_id: str) -> dict:
    state = plant_state(plant_id, db)
    return {
        "plant_id": plant_id,
        "latest_decision": state["latest_decision"],
        "latest_observation": state["observation"],
    }


def run_monitoring_cycle(db: Session, plant_id: str) -> dict:
    return {"status": "available_via_api", "plant_id": plant_id, "endpoint": f"/monitor/{plant_id}/run"}
