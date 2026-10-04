from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class VisionInferenceResult:
    health_score: float
    wilting_probability: float
    yellowing_probability: float
    disease_probability: float
    image_quality: float
    confidence: float


class VisionInferencePort(ABC):
    @abstractmethod
    def infer(self, image_path: str) -> VisionInferenceResult:
        raise NotImplementedError


class PlaceholderEdgeVisionModel(VisionInferencePort):
    """Deterministic development adapter until a trained ONNX/TFLite model is selected."""

    def infer(self, image_path: str) -> VisionInferenceResult:
        return VisionInferenceResult(
            health_score=0.80,
            wilting_probability=0.10,
            yellowing_probability=0.05,
            disease_probability=0.02,
            image_quality=0.95,
            confidence=0.50,
        )
