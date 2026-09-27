from abc import ABC, abstractmethod
from app.domain.sensor import SensorObservation

class SensorPort(ABC):
    @abstractmethod
    def read_all(self) -> list[SensorObservation]:
        raise NotImplementedError
