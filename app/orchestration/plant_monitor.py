from dataclasses import dataclass
from app.domain.action import Action
from app.domain.decision import Decision
from app.domain.plant import PlantObservation
from app.domain.profile import PlantProfile
from app.domain.sensor import SensorObservation, SensorType
from app.intelligence.decision_engine import DecisionEngine
from app.intelligence.safety_engine import SafetyEngine
from app.intelligence.sensor_fusion import SensorFusionEngine
from app.ports.actuator import ActuatorPort
from app.ports.camera import CameraPort
from app.ports.sensor import SensorPort
from app.ports.vision import VisionPort

@dataclass(frozen=True)
class MonitorResult:
    frame_id: str
    observation: PlantObservation
    sensor_readings: list[SensorObservation]
    decision: Decision
    action: Action | None

class PlantMonitor:
    def __init__(self, camera: CameraPort, sensors: SensorPort, vision: VisionPort, actuator: ActuatorPort,
                 decision_engine: DecisionEngine, safety_engine: SafetyEngine, fusion: SensorFusionEngine,
                 repository=None):
        self.camera, self.sensors, self.vision, self.actuator = camera, sensors, vision, actuator
        self.decision_engine, self.safety_engine, self.fusion = decision_engine, safety_engine, fusion
        self.repository = repository

    def run_once(self, profile: PlantProfile, tank_level: float | None = None) -> MonitorResult:
        frame = self.camera.capture()
        readings = self.sensors.read_all()
        observation = self.vision.analyze(frame, profile.plant_id)
        if tank_level is None:
            levels = [r.value for r in readings if r.sensor_type == SensorType.WATER_LEVEL]
            tank_level = levels[-1] if levels else None
        state = self.fusion.build_state(observation, readings)
        decision = self.decision_engine.evaluate(state, profile)
        action = self.safety_engine.approve(decision, profile, tank_level)

        if self.repository:
            self.repository.save_plant_observation(observation)
            self.repository.save_sensor_observations(readings)
            self.repository.save_decision(decision)

        if action:
            self.actuator.execute(action)
            if self.repository:
                self.repository.save_action(profile.plant_id, action)

        return MonitorResult(frame.frame_id, observation, readings, decision, action)
