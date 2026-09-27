import sys
from datetime import timezone

from app.adapters.cameras.raspberry_pi import RaspberryPiCamera

def test_camera_adapter_does_not_import_picamera2_until_capture():
    camera = RaspberryPiCamera(output_dir="data/test-images")
    assert camera.camera_id == "pi-camera-3"
    assert camera._camera is None

def test_camera_module_import_is_lazy():
    assert "picamera2" not in sys.modules
