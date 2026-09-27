from datetime import datetime
from app.domain.plant import PlantObservation
from app.domain.sensor import SensorObservation, SensorType
from app.domain.state import PlantState

class SensorFusionEngine:
    def build_state(self, observation: PlantObservation, sensors: list[SensorObservation], timestamp: datetime | None = None) -> PlantState:
        def value(sensor_type: SensorType) -> float | None:
            values = [s.value for s in sensors if s.sensor_type == sensor_type]
            return values[-1] if values else None

        soil = value(SensorType.SOIL_MOISTURE)
        temperature = value(SensorType.TEMPERATURE)
        humidity = value(SensorType.HUMIDITY)
        light = value(SensorType.LIGHT)

        moisture_stress = 0.0 if soil is None else max(0.0, min(1.0, (40.0 - soil) / 40.0))
        visual_stress = observation.water_stress_probability or 0.0
        water_stress = max(moisture_stress, visual_stress)
        heat_stress = observation.heat_stress_probability or 0.0

        available = sum(v is not None for v in (soil, temperature, humidity, light))
        sensor_confidence = min(1.0, available / 4.0)
        confidence = max(0.0, min(1.0, 0.5 * observation.image_quality + 0.5 * sensor_confidence))

        return PlantState(
            plant_id=observation.plant_id,
            timestamp=timestamp or observation.timestamp,
            health_score=observation.health_score,
            soil_moisture=soil,
            temperature=temperature,
            humidity=humidity,
            light=light,
            water_stress=water_stress,
            heat_stress=heat_stress,
            disease_risk=observation.disease_probability,
            confidence=confidence,
        )
