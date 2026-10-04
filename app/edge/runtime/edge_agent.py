from dataclasses import asdict

from app.ports.camera import CameraPort
from app.edge.vision.inference import VisionInferencePort
from app.edge.storage.queue import EdgeObservationQueue


class EdgeAgent:
    """Raspberry Pi edge runtime: capture -> infer -> durable queue."""

    def __init__(self, camera: CameraPort, vision: VisionInferencePort, queue: EdgeObservationQueue, device_id: str) -> None:
        self.camera = camera
        self.vision = vision
        self.queue = queue
        self.device_id = device_id

    def run_once(self, plant_id: str) -> dict:
        frame = self.camera.capture()
        inference = self.vision.infer(frame.image_path)
        observation = {
            "device_id": self.device_id,
            "plant_id": plant_id,
            "image_id": frame.frame_id,
            "image_path": frame.image_path,
            "timestamp": frame.timestamp.isoformat(),
            "model_name": self.vision.__class__.__name__,
            **asdict(inference),
        }
        self.queue.enqueue(observation)
        return observation
