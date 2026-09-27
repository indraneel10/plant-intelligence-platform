from app.domain.action import Action, ActionType
from app.domain.decision import Decision, DecisionAction
from app.core.exceptions import SafetyViolation

class SafetyEngine:
    def __init__(self, max_irrigation_seconds: int = 60) -> None:
        self.max_irrigation_seconds = max_irrigation_seconds

    def approve(self, decision: Decision, zone_id: str, tank_level: float | None = None) -> Action | None:
        if decision.action == DecisionAction.NO_ACTION:
            return None
        if decision.action == DecisionAction.INSPECT:
            return None
        if decision.action != DecisionAction.WATER:
            raise SafetyViolation(f"Unsupported decision: {decision.action}")
        if tank_level is not None and tank_level <= 0:
            raise SafetyViolation("Water tank is empty.")
        duration = min(decision.duration_seconds, self.max_irrigation_seconds)
        if duration <= 0:
            raise SafetyViolation("Irrigation duration must be positive.")
        return Action(ActionType.OPEN_VALVE, zone_id, duration)
