from app.domain.decision import Decision, DecisionAction
from app.domain.state import PlantState

class DecisionEngine:
    def __init__(self, moisture_threshold: float = 30.0) -> None:
        self.moisture_threshold = moisture_threshold

    def evaluate(self, state: PlantState) -> Decision:
        if state.soil_moisture is None:
            return Decision(state.plant_id, DecisionAction.INSPECT, "Soil moisture is unavailable.", 0.4)
        if state.soil_moisture < self.moisture_threshold and state.water_stress >= 0.5:
            return Decision(state.plant_id, DecisionAction.WATER, "Low soil moisture with elevated water stress.", min(0.99, max(0.0, state.confidence)), 30)
        return Decision(state.plant_id, DecisionAction.NO_ACTION, "Current plant state does not require irrigation.", min(0.99, max(0.0, state.confidence)))
