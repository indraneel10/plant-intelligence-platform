from app.domain.action import Action, ActionType
from app.adapters.actuators.esp32_wr04 import Esp32WR04ActuatorAdapter

class FakeMqtt:
    def __init__(self):
        self.messages = []
    def publish_json(self, topic, payload, qos=1):
        self.messages.append((topic, payload, qos))

def test_esp32_actuator_publishes_command():
    mqtt = FakeMqtt()
    Esp32WR04ActuatorAdapter(mqtt).execute(Action(ActionType.OPEN_VALVE, "zone-2", 20))
    assert mqtt.messages == [(
        "plant/actuators/command",
        {"action_type": "open_valve", "zone_id": "zone-2", "duration_seconds": 20},
        1,
    )]
