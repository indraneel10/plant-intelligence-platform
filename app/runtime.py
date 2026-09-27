from app.adapters.actuators.esp32_wr04 import Esp32WR04ActuatorAdapter
from app.adapters.cameras.raspberry_pi import RaspberryPiCamera
from app.adapters.messaging.mqtt import MqttClient
from app.adapters.mock import MockActuator, MockCamera, MockSensor
from app.adapters.sensors.esp32_wr04 import Esp32WR04SensorAdapter
from app.core.config import settings
from app.intelligence.decision_engine import DecisionEngine
from app.intelligence.safety_engine import SafetyEngine
from app.intelligence.sensor_fusion import SensorFusionEngine
from app.orchestration.plant_monitor import PlantMonitor
from app.persistence.database import SessionLocal
from app.persistence.repositories import PlantRepository
from app.vision.engine import RuleBasedVisionEngine

def build_monitor() -> PlantMonitor:
    repository = PlantRepository(SessionLocal())

    if settings.hardware_mode.lower() == "pi":
        mqtt = MqttClient(settings.mqtt_broker_host, settings.mqtt_broker_port)
        mqtt.connect()
        sensors = Esp32WR04SensorAdapter(mqtt, settings.mqtt_sensor_topic)
        sensors.start()
        actuator = Esp32WR04ActuatorAdapter(mqtt, settings.mqtt_actuator_topic)
        camera = RaspberryPiCamera(settings.image_dir)
    else:
        camera, sensors, actuator = MockCamera(), MockSensor(), MockActuator()

    return PlantMonitor(
        camera, sensors, RuleBasedVisionEngine(), actuator,
        DecisionEngine(), SafetyEngine(), SensorFusionEngine(), repository,
    )
