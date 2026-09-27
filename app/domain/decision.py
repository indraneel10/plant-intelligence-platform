from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class DecisionAction(StrEnum):
    NO_ACTION = "no_action"
    WATER = "water"
    INSPECT = "inspect"

@dataclass(frozen=True)
class Decision:
    plant_id: str
    action: DecisionAction
    reason: str
    confidence: float
    duration_seconds: int = 0
    created_at: datetime | None = None
