from sqlalchemy.orm import Session
from app.domain.action import Action
from app.persistence.audit import record_audit_event
from app.persistence.models import PlantModel
from app.ports.actuator import ActuatorPort

def execute_approved_action(db: Session, actuator: ActuatorPort, *, plant_id: str, action: Action, actor_id: str, actor_role: str, reason: str|None=None) -> dict:
    plant=db.get(PlantModel,plant_id)
    if plant is None:
        record_audit_event(db,event_type="actuator_execution",actor_id=actor_id,actor_role=actor_role,plant_id=plant_id,status="rejected",reason="Plant not found")
        return {"status":"rejected","executed":False,"reason":"Plant not found"}
    if plant.zone_id != action.zone_id:
        record_audit_event(db,event_type="actuator_execution",actor_id=actor_id,actor_role=actor_role,plant_id=plant_id,status="rejected",zone_id=action.zone_id,duration_seconds=action.duration_seconds,reason="Action zone does not match plant zone")
        return {"status":"rejected","executed":False,"reason":"Action zone does not match plant zone"}
    try: actuator.execute(action)
    except Exception as exc:
        record_audit_event(db,event_type="actuator_execution",actor_id=actor_id,actor_role=actor_role,plant_id=plant_id,status="failed",action_type=action.action_type.value,zone_id=action.zone_id,duration_seconds=action.duration_seconds,reason=reason,details=str(exc))
        return {"status":"failed","executed":False,"reason":str(exc)}
    record_audit_event(db,event_type="actuator_execution",actor_id=actor_id,actor_role=actor_role,plant_id=plant_id,status="executed",action_type=action.action_type.value,zone_id=action.zone_id,duration_seconds=action.duration_seconds,reason=reason,details="ESP32 actuator accepted action")
    return {"status":"executed","executed":True,"plant_id":plant_id,"zone_id":action.zone_id,"duration_seconds":action.duration_seconds}
