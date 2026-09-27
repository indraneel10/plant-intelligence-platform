from dataclasses import dataclass
from app.domain.action import Action
from app.domain.decision import Decision
from app.domain.profile import PlantProfile
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
    decision: Decision
    action: Action | None

class PlantMonitor:
    def __init__(self, camera: CameraPort, sensors: SensorPort, vision: VisionPort, actuator: ActuatorPort, decision_engine: DecisionEngine, safety_engine: SafetyEngine, fusion: SensorFusionEngine):
        self.camera, self.sensors, self.vision, self.actuator = camera, sensors, vision, actuator
        self.decision_engine, self.safety_engine, self.fusion = decision_engine, safety_engine, fusion

    def run_once(self, profile: PlantProfile, tank_level: float | None = None) -> MonitorResult:
        frame = self.camera.capture()
        readings = self.sensors.read_all()
        observation = self.vision.analyze(frame, profile.plant_id)
        state = self.fusion.build_state(observation, readings)
        decision = self.decision_engine.evaluate(state, profile)
        action = self.safety_engine.approve(decision, profile, tank_level)
        if action:
            self.actuator.execute(action)
        return MonitorResult(frame.frame_id, decision, action)
