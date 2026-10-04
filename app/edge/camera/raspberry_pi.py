from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.domain.camera import CaptureMode, ImageFrame
from app.ports.camera import CameraPort


class RaspberryPiCameraAdapter(CameraPort):
    """Camera Module 3 adapter using Picamera2 when running on Raspberry Pi OS."""

    def __init__(self, camera_id: str = "rpi5-camera-01", image_dir: str = "data/plant-images") -> None:
        self.camera_id = camera_id
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(parents=True, exist_ok=True)
        try:
            from picamera2 import Picamera2
        except ImportError as exc:
            raise RuntimeError("Picamera2 is required on Raspberry Pi. Install it from Raspberry Pi OS packages.") from exc
        self.camera = Picamera2()
        config = self.camera.create_still_configuration(main={"size": (2304, 1296)})
        self.camera.configure(config)
        self.camera.start()

    def capture(self) -> ImageFrame:
        frame_id = str(uuid4())
        path = self.image_dir / f"{frame_id}.jpg"
        self.camera.capture_file(str(path))
        return ImageFrame(
            frame_id=frame_id,
            camera_id=self.camera_id,
            timestamp=datetime.now(timezone.utc),
            image_path=str(path),
            capture_mode=CaptureMode.DAY_RGB,
        )
