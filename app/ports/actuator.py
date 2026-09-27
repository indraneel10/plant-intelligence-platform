from abc import ABC, abstractmethod
from app.domain.action import Action

class ActuatorPort(ABC):
    @abstractmethod
    def execute(self, action: Action) -> None:
        raise NotImplementedError
