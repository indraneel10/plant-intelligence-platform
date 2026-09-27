import cv2
import numpy as np

def resize_for_inference(image: np.ndarray, width: int = 640) -> np.ndarray:
    height, current_width = image.shape[:2]
    if current_width <= width:
        return image
    scale = width / current_width
    return cv2.resize(image, (width, int(height * scale)))

def green_ratio(image: np.ndarray) -> float:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([35, 40, 30], dtype=np.uint8)
    upper = np.array([95, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    return float((mask > 0).mean())
