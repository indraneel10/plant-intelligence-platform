from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

class CaptureMode(StrEnum):
    DAY_RGB = "DAY_RGB"
    NIGHT_IR = "NIGHT_IR"
    THERMAL = "THERMAL"
    MULTISPECTRAL = "MULTISPECTRAL"

@dataclass(frozen=True)
class ImageFrame:
    frame_id: str
    camera_id: str
    timestamp: datetime
    image_path: str
    capture_mode: CaptureMode = CaptureMode.DAY_RGB
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    heading: float | None = None
