from app.adapters.esp32_wr04 import ESP32WR04Actuator
from app.domain.action import Action, ActionType

def test_esp32_adapter_requires_endpoint(monkeypatch):
    monkeypatch.delenv("ESP32_WR04_URL", raising=False)
    try: ESP32WR04Actuator()
    except ValueError: return
    assert False

def test_esp32_adapter_payload_contract(monkeypatch):
    monkeypatch.setenv("ESP32_WR04_URL","http://esp32.local")
    adapter=ESP32WR04Actuator()
    assert adapter.base_url=="http://esp32.local"
