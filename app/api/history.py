from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.persistence.database import get_db
from app.persistence.models import DecisionModel, IrrigationActionModel

router = APIRouter(prefix="/plants/{plant_id}", tags=["history"])

@router.get("/decisions")
def decisions(plant_id: str, db: Session = Depends(get_db)):
    return db.query(DecisionModel).filter(
        DecisionModel.plant_id == plant_id
    ).order_by(DecisionModel.created_at.desc()).all()

@router.get("/irrigation-history")
def irrigation_history(plant_id: str, db: Session = Depends(get_db)):
    return db.query(IrrigationActionModel).filter(
        IrrigationActionModel.plant_id == plant_id
    ).order_by(IrrigationActionModel.executed_at.desc()).all()
