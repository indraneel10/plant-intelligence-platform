from fastapi import FastAPI

from app.api.ai import router as ai_router
from app.api.health import router as health_router
from app.api.edge import router as edge_router
from app.core.config import settings
from app.persistence.database import init_db
from app.api.plants import router as plants_router
from app.api.observations import router as observations_router
from app.api.history import router as history_router
from app.api.monitor import router as monitor_router
from app.api.state import router as state_router
from app.api.actions import router as actions_router

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Hardware-independent plant intelligence platform with Raspberry Pi edge AI and safe ESP32 actuation.",
)

app.include_router(health_router)
app.include_router(plants_router)
app.include_router(observations_router)
app.include_router(history_router)
app.include_router(monitor_router)
app.include_router(state_router)
app.include_router(actions_router)
app.include_router(ai_router)
app.include_router(edge_router)

@app.on_event("startup")
def startup() -> None:
    init_db()

@app.get("/")
def root() -> dict[str, str]:
    return {"name": settings.app_name, "version": "0.2.0", "status": "running"}
