from datetime import datetime, timezone
from tempfile import NamedTemporaryFile

from fastapi.testclient import TestClient

from app.edge.storage.queue import EdgeObservationQueue
from app.main import app
from app.persistence.database import Base, SessionLocal, engine
from app.persistence.models import PlantModel, VisionObservationModel


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(PlantModel(plant_id="plant-001", name="Basil", species="Ocimum basilicum", zone_id="zone-1"))
    db.commit()
    db.close()


def test_edge_observation_is_persisted_and_idempotent():
    client = TestClient(app)
    payload = {
        "device_id": "pi5-01",
        "plant_id": "plant-001",
        "image_id": "img-001",
        "image_path": "data/plant-images/img-001.jpg",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_name": "PlaceholderEdgeVisionModel",
        "model_version": "dev",
        "health_score": 0.8,
        "wilting_probability": 0.1,
        "yellowing_probability": 0.05,
        "disease_probability": 0.02,
        "image_quality": 0.95,
        "confidence": 0.5,
    }
    first = client.post("/edge/v1/observations", json=payload)
    assert first.status_code == 201
    second = client.post("/edge/v1/observations", json=payload)
    assert second.status_code == 201
    assert second.json()["status"] == "duplicate"
    db = SessionLocal()
    assert db.query(VisionObservationModel).count() == 1
    db.close()


def test_edge_queue_survives_until_marked_sent(tmp_path):
    queue = EdgeObservationQueue(str(tmp_path / "queue.db"))
    item_id = queue.enqueue({"plant_id": "plant-001", "image_id": "img-001"})
    assert queue.pending()[0][0] == item_id
    queue.mark_sent(item_id)
    assert queue.pending() == []
