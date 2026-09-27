from abc import ABC, abstractmethod
from app.domain.camera import ImageFrame

class CameraPort(ABC):
    @abstractmethod
    def capture(self) -> ImageFrame:
        raise NotImplementedError
