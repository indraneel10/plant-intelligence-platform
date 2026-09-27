from app.core.exceptions import SafetyViolation
from app.domain.action import Action, ActionType
from app.domain.decision import Decision, DecisionAction
from app.domain.profile import PlantProfile

class SafetyEngine:
    def approve(self, decision: Decision, profile: PlantProfile, tank_level: float | None = None) -> Action | None:
        if decision.action != DecisionAction.WATER:
            return None
        if tank_level is not None and tank_level <= 0:
            raise SafetyViolation("Water tank is empty.")
        duration = min(decision.duration_seconds, profile.max_irrigation_seconds)
        if duration <= 0:
            raise SafetyViolation("Irrigation duration must be positive.")
        return Action(ActionType.OPEN_VALVE, profile.zone_id, duration)
