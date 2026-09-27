from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.exceptions import SafetyViolation
from app.domain.decision import Decision, DecisionAction
from app.domain.profile import PlantProfile
from app.intelligence.safety_engine import SafetyEngine
from app.persistence.database import get_db
from app.persistence.models import PlantModel

router = APIRouter(prefix="/plants", tags=["actions"])


class IrrigationRequest(BaseModel):
    zone_id: str | None = None
    duration_seconds: int = Field(gt=0, le=300)
    reason: str | None = Field(default=None, max_length=500)


@router.post("/{plant_id}/actions/irrigation/request")
def request_irrigation(plant_id: str, payload: IrrigationRequest, db: Session = Depends(get_db)):
    plant = db.get(PlantModel, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    zone_id = payload.zone_id or plant.zone_id
    if not zone_id:
        raise HTTPException(status_code=422, detail="Plant has no irrigation zone configured")
    if plant.zone_id and payload.zone_id and payload.zone_id != plant.zone_id:
        raise HTTPException(status_code=422, detail="Requested zone does not match the plant zone")

    profile = PlantProfile(
        plant_id=plant_id,
        zone_id=zone_id,
        max_irrigation_seconds=min(300, payload.duration_seconds),
    )
    decision = Decision(
        plant_id=plant_id,
        action=DecisionAction.WATER,
        reason=payload.reason or "User requested irrigation.",
        confidence=1.0,
        duration_seconds=payload.duration_seconds,
        created_at=datetime.now(timezone.utc),
    )

    try:
        action = SafetyEngine().approve(decision, profile, tank_level=100.0)
    except SafetyViolation as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if action is None:
        raise HTTPException(status_code=409, detail="Irrigation request was not approved")

    return {
        "status": "approved",
        "executed": False,
        "plant_id": plant_id,
        "zone_id": action.zone_id,
        "duration_seconds": action.duration_seconds,
        "action_type": action.action_type.value,
        "message": "Safety gate approved the request. Hardware execution is intentionally disabled for this API.",
    }
