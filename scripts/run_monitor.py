import sys
from app.core.config import settings
from app.domain.profile import PlantProfile
from app.runtime import build_monitor

if len(sys.argv) != 3:
    raise SystemExit("Usage: python scripts/run_monitor.py <plant_id> <zone_id>")

plant_id, zone_id = sys.argv[1], sys.argv[2]
result = build_monitor().run_once(PlantProfile(plant_id, zone_id))
print({
    "frame_id": result.frame_id,
    "decision": result.decision.action.value,
    "reason": result.decision.reason,
    "action": result.action.action_type.value if result.action else None,
    "duration_seconds": result.action.duration_seconds if result.action else 0,
})
