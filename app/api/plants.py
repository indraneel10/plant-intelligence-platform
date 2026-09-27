from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.domain.plant import Plant
from app.persistence.database import get_db
from app.persistence.models import PlantModel

router = APIRouter(prefix="/plants", tags=["plants"])

class PlantCreate(BaseModel):
    plant_id: str
    name: str
    species: str | None = None
    zone_id: str | None = None
    location_label: str | None = None

class PlantResponse(PlantCreate):
    pass

@router.post("", response_model=PlantResponse, status_code=201)
def create_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    if db.get(PlantModel, payload.plant_id):
        raise HTTPException(status_code=409, detail="Plant already exists")
    model = PlantModel(**payload.model_dump())
    db.add(model)
    db.commit()
    return payload

@router.get("", response_model=list[PlantResponse])
def list_plants(db: Session = Depends(get_db)):
    return db.query(PlantModel).order_by(PlantModel.plant_id).all()

@router.get("/{plant_id}", response_model=PlantResponse)
def get_plant(plant_id: str, db: Session = Depends(get_db)):
    plant = db.get(PlantModel, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
