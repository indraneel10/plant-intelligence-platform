from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_plant():
    plant_id = "test-plant-api"
    response = client.post("/plants", json={
        "plant_id": plant_id,
        "name": "Test Basil",
        "species": "Ocimum basilicum",
        "zone_id": "zone-1",
        "location_label": "Balcony A",
    })
    assert response.status_code == 201
    assert response.json()["plant_id"] == plant_id

    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Basil"
