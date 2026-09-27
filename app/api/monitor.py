from fastapi import APIRouter, HTTPException

from app.adapters.mock import MockActuator, MockCamera, MockSensor
from app.domain.profile import PlantProfile
from app.intelligence.decision_engine import DecisionEngine
from app.intelligence.safety_engine import SafetyEngine
from app.intelligence.sensor_fusion import SensorFusionEngine
from app.orchestration.plant_monitor import PlantMonitor
from app.vision.engine import RuleBasedVisionEngine

router = APIRouter(prefix="/monitor", tags=["monitor"])

@router.post("/{plant_id}/run")
def run_monitor(plant_id: str):
    profile = PlantProfile(plant_id=plant_id, zone_id="zone-1")
    monitor = PlantMonitor(
        MockCamera(), MockSensor(), RuleBasedVisionEngine(), MockActuator(),
        DecisionEngine(), SafetyEngine(), SensorFusionEngine(),
    )
    try:
        result = monitor.run_once(profile, tank_level=100.0)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail="Camera test image is unavailable") from exc

    return {
        "frame_id": result.frame_id,
        "decision": result.decision.action.value,
        "reason": result.decision.reason,
        "confidence": result.decision.confidence,
        "action": result.action.action_type.value if result.action else None,
        "zone_id": result.action.zone_id if result.action else None,
        "duration_seconds": result.action.duration_seconds if result.action else 0,
    }
