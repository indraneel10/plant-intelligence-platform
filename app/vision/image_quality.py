from pathlib import Path
import cv2
import numpy as np

def load_image(path: str) -> np.ndarray:
    image = cv2.imread(str(Path(path)))
    if image is None:
        raise FileNotFoundError(f"Unable to read image: {path}")
    return image

def blur_score(image: np.ndarray) -> float:
    variance = float(cv2.Laplacian(image, cv2.CV_64F).var())
    return min(1.0, variance / 500.0)

def brightness_score(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = float(gray.mean())
    distance = abs(mean - 128.0) / 128.0
    return max(0.0, 1.0 - distance)

def image_quality_score(image: np.ndarray) -> float:
    return max(0.0, min(1.0, 0.6 * blur_score(image) + 0.4 * brightness_score(image)))
