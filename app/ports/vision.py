from abc import ABC, abstractmethod
from app.domain.camera import ImageFrame
from app.domain.plant import PlantObservation

class VisionPort(ABC):
    @abstractmethod
    def analyze(self, frame: ImageFrame, plant_id: str) -> PlantObservation:
        raise NotImplementedError
