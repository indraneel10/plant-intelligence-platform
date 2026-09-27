from app.ports.vision import VisionPort
from app.domain.camera import ImageFrame
from app.domain.plant import PlantObservation
from datetime import datetime

class RuleBasedVisionEngine(VisionPort):
    """V0 vision adapter.

    Image processing will be added behind this interface. The public contract
    intentionally remains independent of OpenCV/model implementations.
    """

    def analyze(self, frame: ImageFrame, plant_id: str) -> PlantObservation:
        return PlantObservation(
            plant_id=plant_id,
            timestamp=datetime.now(frame.timestamp.tzinfo),
            health_score=1.0,
            wilting_probability=0.0,
            yellowing_probability=0.0,
            disease_probability=0.0,
            image_quality=1.0,
        )
