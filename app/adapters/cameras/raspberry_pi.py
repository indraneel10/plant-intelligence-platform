from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.core.exceptions import DeviceError
from app.domain.camera import CaptureMode, ImageFrame
from app.ports.camera import CameraPort

class RaspberryPiCamera(CameraPort):
    """Picamera2 adapter for Raspberry Pi Camera Module 3.

    The dependency is imported lazily so the rest of the platform can run
    on development machines without Raspberry Pi camera libraries installed.
    """

    def __init__(self, output_dir: str = "data/images", camera_id: str = "pi-camera-3"):
        self.output_dir = Path(output_dir)
        self.camera_id = camera_id
        self._camera = None

    def _get_camera(self):
        if self._camera is None:
            try:
                from picamera2 import Picamera2
            except ImportError as exc:
                raise DeviceError(
                    "Picamera2 is not installed. Install it on Raspberry Pi OS."
                ) from exc
            self._camera = Picamera2()
            config = self._camera.create_still_configuration()
            self._camera.configure(config)
            self._camera.start()
        return self._camera

    def capture(self) -> ImageFrame:
        camera = self._get_camera()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc)
        frame_id = str(uuid4())
        path = self.output_dir / f"{frame_id}.jpg"

        try:
            camera.capture_file(str(path))
        except Exception as exc:
            raise DeviceError(f"Failed to capture image: {exc}") from exc

        return ImageFrame(
            frame_id=frame_id,
            camera_id=self.camera_id,
            timestamp=timestamp,
            image_path=str(path),
            capture_mode=CaptureMode.DAY_RGB,
        )

    def close(self) -> None:
        if self._camera is not None:
            self._camera.stop()
            self._camera.close()
            self._camera = None
