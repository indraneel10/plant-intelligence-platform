from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.persistence.database import get_db
from app.persistence.models import PlantObservationModel, SensorObservationModel

router = APIRouter(prefix="/plants/{plant_id}", tags=["observations"])

@router.get("/observations")
def plant_observations(plant_id: str, db: Session = Depends(get_db)):
    return db.query(PlantObservationModel).filter(
        PlantObservationModel.plant_id == plant_id
    ).order_by(PlantObservationModel.timestamp.desc()).all()

@router.get("/sensor-history")
def sensor_history(plant_id: str, db: Session = Depends(get_db)):
    return db.query(SensorObservationModel).filter(
        SensorObservationModel.plant_id == plant_id
    ).order_by(SensorObservationModel.timestamp.desc()).all()
