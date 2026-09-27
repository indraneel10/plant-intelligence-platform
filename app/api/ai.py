from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.service import chat
from app.persistence.database import get_db

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    plant_id: str | None = None


class ChatResponse(BaseModel):
    message: str
    mode: str
    tools_used: list[str]


@router.post("/chat", response_model=ChatResponse)
def ai_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    return chat(db, payload.message, payload.plant_id)
