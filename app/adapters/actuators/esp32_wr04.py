from app.domain.action import Action
from app.ports.actuator import ActuatorPort
from app.adapters.messaging.mqtt import MqttClient

class Esp32WR04ActuatorAdapter(ActuatorPort):
    def __init__(self, mqtt: MqttClient, command_topic: str = "plant/actuators/command"):
        self.mqtt = mqtt
        self.command_topic = command_topic

    def execute(self, action: Action) -> None:
        self.mqtt.publish_json(self.command_topic, {
            "action_type": action.action_type.value,
            "zone_id": action.zone_id,
            "duration_seconds": action.duration_seconds,
        })
