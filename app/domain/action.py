from dataclasses import dataclass
from enum import StrEnum

class ActionType(StrEnum):
    OPEN_VALVE = "open_valve"
    CLOSE_VALVE = "close_valve"
    START_PUMP = "start_pump"
    STOP_PUMP = "stop_pump"

@dataclass(frozen=True)
class Action:
    action_type: ActionType
    zone_id: str
    duration_seconds: int = 0
