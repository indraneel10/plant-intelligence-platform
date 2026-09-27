from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.persistence.database import Base, SessionLocal, engine
from app.persistence.models import PlantModel, PlantObservationModel, SensorObservationModel, DecisionModel


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(PlantModel(plant_id="plant-001", name="Basil", species="Ocimum basilicum", zone_id="zone-1"))
    now = datetime.now(timezone.utc)
    db.add(PlantObservationModel(
        plant_id="plant-001", timestamp=now, health_score=0.8,
        wilting_probability=0.1, yellowing_probability=0.05,
        disease_probability=0.02, image_quality=0.95,
        leaf_area_ratio=0.8, water_stress_probability=0.2,
        heat_stress_probability=0.1,
    ))
    db.add(SensorObservationModel(
        sensor_id="soil-1", plant_id="plant-001", zone_id="zone-1",
        sensor_type="soil_moisture", value=35.0, unit="%", timestamp=now,
    ))
    db.add(DecisionModel(
        plant_id="plant-001", action="no_action",
        reason="Current plant state does not require irrigation.",
        confidence=0.9, duration_seconds=0, created_at=now,
    ))
    db.commit()
    db.close()


def test_plant_state_returns_consolidated_context():
    client = TestClient(app)
    response = client.get("/plants/plant-001/state")
    assert response.status_code == 200
    body = response.json()
    assert body["plant"]["name"] == "Basil"
    assert body["observation"]["health_score"] == 0.8
    assert body["sensors"]["soil_moisture"]["value"] == 35.0
    assert body["latest_decision"]["action"] == "no_action"


def test_irrigation_request_is_safety_gated_and_not_executed():
    client = TestClient(app)
    response = client.post(
        "/plants/plant-001/actions/irrigation/request",
        json={"duration_seconds": 30, "reason": "User requested watering"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "approved"
    assert body["executed"] is False
    assert body["zone_id"] == "zone-1"
