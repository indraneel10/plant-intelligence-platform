from datetime import datetime, timezone

from app.domain.decision import Decision, DecisionAction
from app.domain.profile import PlantProfile
from app.domain.state import PlantState

class DecisionEngine:
    def evaluate(self, state: PlantState, profile: PlantProfile, last_watered_at: datetime | None = None, now: datetime | None = None) -> Decision:
        now = now or datetime.now(timezone.utc)

        if state.confidence < profile.minimum_confidence:
            return Decision(state.plant_id, DecisionAction.INSPECT, "Confidence is below the configured threshold.", state.confidence, created_at=now)

        if state.soil_moisture is None:
            return Decision(state.plant_id, DecisionAction.INSPECT, "Soil moisture is unavailable.", 0.4, created_at=now)

        if last_watered_at is not None and (now - last_watered_at).total_seconds() < profile.cooldown_seconds:
            return Decision(state.plant_id, DecisionAction.NO_ACTION, "Irrigation cooldown is active.", state.confidence, created_at=now)

        if state.soil_moisture < profile.moisture_threshold and state.water_stress >= 0.5:
            return Decision(state.plant_id, DecisionAction.WATER, "Low soil moisture with elevated water stress.", state.confidence, min(30, profile.max_irrigation_seconds), now)

        return Decision(state.plant_id, DecisionAction.NO_ACTION, "Current plant state does not require irrigation.", state.confidence, created_at=now)
