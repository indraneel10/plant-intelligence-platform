from fastapi import APIRouter, HTTPException
from app.persistence.database import SessionLocal
from app.services.monitoring_service import run_monitoring_cycle

router = APIRouter(prefix="/monitor", tags=["monitor"])

@router.post("/{plant_id}/run")
def run_monitor(plant_id: str):
    db = SessionLocal()
    try:
        result = run_monitoring_cycle(db, plant_id)
        if result["status"] == "rejected":
            raise HTTPException(status_code=404, detail=result["reason"])
        return result
    finally:
        db.close()
