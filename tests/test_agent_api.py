from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.persistence.database import Base, SessionLocal, engine
from app.persistence.models import PlantModel, PlantObservationModel, SensorObservationModel, DecisionModel, AuditEventModel

def setup_function():
    Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
    db=SessionLocal(); db.add(PlantModel(plant_id="plant-001",name="Basil",species="Ocimum basilicum",zone_id="zone-1")); now=datetime.now(timezone.utc)
    db.add(PlantObservationModel(plant_id="plant-001",timestamp=now,health_score=.8,wilting_probability=.1,yellowing_probability=.05,disease_probability=.02,image_quality=.95,leaf_area_ratio=.8,water_stress_probability=.2,heat_stress_probability=.1))
    db.add(SensorObservationModel(sensor_id="soil-1",plant_id="plant-001",zone_id="zone-1",sensor_type="soil_moisture",value=35.,unit="%",timestamp=now))
    db.add(DecisionModel(plant_id="plant-001",action="no_action",reason="Current plant state does not require irrigation.",confidence=.9,duration_seconds=0,created_at=now)); db.commit(); db.close()

def test_plant_state_returns_consolidated_context():
    body=TestClient(app).get("/plants/plant-001/state").json(); assert body["plant"]["name"]=="Basil"; assert body["sensors"]["soil_moisture"]["value"]==35.; assert body["latest_decision"]["action"]=="no_action"

def test_irrigation_requires_actor():
    r=TestClient(app).post("/plants/plant-001/actions/irrigation/request",json={"duration_seconds":30,"reason":"User requested watering"}); assert r.status_code==401

def test_irrigation_is_authorized_safety_gated_and_audited():
    r=TestClient(app).post("/plants/plant-001/actions/irrigation/request",headers={"X-Actor-ID":"operator-1","X-Actor-Role":"operator"},json={"duration_seconds":30,"reason":"User requested watering"}); assert r.status_code==200; assert r.json()["executed"] is False
    db=SessionLocal(); event=db.query(AuditEventModel).one(); assert event.actor_id=="operator-1"; assert event.status=="approved"; db.close()

def test_monitoring_cycle_persists_state_and_does_not_execute_real_hardware():
    r=TestClient(app).post("/monitor/plant-001/run"); assert r.status_code==200; body=r.json(); assert body["status"]=="completed"; assert body["hardware_executed"] is False
    db=SessionLocal(); assert db.query(PlantObservationModel).count()>=2; assert db.query(SensorObservationModel).count()>=2; assert db.query(DecisionModel).count()>=2; db.close()
