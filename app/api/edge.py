from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.persistence.database import get_db
from app.persistence.models import PlantModel, VisionObservationModel

router = APIRouter(prefix="/edge/v1", tags=["edge"])


class EdgeVisionObservation(BaseModel):
    device_id: str
    plant_id: str
    image_id: str
    image_path: str | None = None
    timestamp: datetime
    model_name: str
    model_version: str | None = None
    health_score: float = Field(ge=0, le=1)
    wilting_probability: float = Field(ge=0, le=1)
    yellowing_probability: float = Field(ge=0, le=1)
    disease_probability: float = Field(ge=0, le=1)
    image_quality: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)


@router.post("/observations", status_code=201)
def ingest_observation(payload: EdgeVisionObservation, db: Session = Depends(get_db)) -> dict:
    if db.get(PlantModel, payload.plant_id) is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    existing = db.query(VisionObservationModel).filter(VisionObservationModel.image_id == payload.image_id).first()
    if existing:
        return {"status": "duplicate", "observation_id": existing.id, "image_id": payload.image_id}
    row = VisionObservationModel(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"status": "accepted", "observation_id": row.id, "image_id": row.image_id}
