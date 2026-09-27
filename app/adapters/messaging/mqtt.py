import json
from typing import Callable
import paho.mqtt.client as mqtt
from app.core.exceptions import DeviceError

class MqttClient:
    def __init__(self, host: str, port: int = 1883, client_id: str = "plant-intelligence"):
        self.host, self.port = host, port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

    def connect(self) -> None:
        try:
            self.client.connect(self.host, self.port)
            self.client.loop_start()
        except Exception as exc:
            raise DeviceError(f"MQTT connection failed: {exc}") from exc

    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def publish_json(self, topic: str, payload: dict, qos: int = 1) -> None:
        result = self.client.publish(topic, json.dumps(payload), qos=qos)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise DeviceError(f"MQTT publish failed: {result.rc}")

    def subscribe_json(self, topic: str, handler: Callable[[dict], None], qos: int = 1) -> None:
        def callback(_client, _userdata, message):
            try:
                handler(json.loads(message.payload.decode("utf-8")))
            except Exception as exc:
                raise DeviceError(f"Invalid MQTT payload on {topic}: {exc}") from exc
        self.client.subscribe(topic, qos=qos)
        self.client.message_callback_add(topic, callback)
