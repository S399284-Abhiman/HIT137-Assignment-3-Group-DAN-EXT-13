import cv2
import numpy as np


class ImageProcessor:
    """
    Handles image processing operations and manages current image state.
    """

    def __init__(self, image: np.ndarray):
        """
        Constructor initializes the image state.
        """
        self._original_image = image.copy()
        self._current_image = image.copy()
        self._history = []

    # Internal Helpers
    def _save_state(self):
        """Save current image state for undo functionality."""
        self._history.append(self._current_image.copy())

    def reset(self):
        """Reset image to original."""
        self._current_image = self._original_image.copy()
        self._history.clear()

    def get_image(self):
        """Return the current image."""
        return self._current_image


    # Image Processing Methods
    def to_grayscale(self):
        self._save_state()
        self._current_image = cv2.cvtColor(self._current_image, cv2.COLOR_BGR2GRAY)

    def apply_blur(self, intensity: int):
        """
        Apply Gaussian blur.
        Intensity must be an odd number.
        """
        self._save_state()
        if intensity % 2 == 0:
            intensity += 1
        self._current_image = cv2.GaussianBlur(
            self._current_image, (intensity, intensity), 0
        )

    def detect_edges(self, threshold1=100, threshold2=200):
        self._save_state()
        gray = self._current_image
        if len(gray.shape) == 3:
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, threshold1, threshold2)
        self._current_image = edges

    def adjust_brightness_contrast(self, brightness=0, contrast=1.0):
        """
        Brightness range: -100 to +100
        Contrast range: 0.5 to 3.0
        """
        self._save_state()
        self._current_image = cv2.convertScaleAbs(
            self._current_image,
            alpha=contrast,
            beta=brightness
        )

    def rotate(self, angle: int):
        """
        Rotate image by 90, 180, or 270 degrees.
        """
        self._save_state()
        if angle == 90:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_180)
        elif angle == 270:
            self._current_image = cv2.rotate(self._current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            raise ValueError("Angle must be 90, 180, or 270")

    def flip(self, direction: str):
        """
        direction: 'horizontal' or 'vertical'
        """
        self._save_state()
        if direction == "horizontal":
            self._current_image = cv2.flip(self._current_image, 1)
        elif direction == "vertical":
            self._current_image = cv2.flip(self._current_image, 0)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")

    def resize(self, scale_x: float, scale_y: float):
        """
        Resize image by scale factors.
        """
        self._save_state()
        height, width = self._current_image.shape[:2]
        new_size = (int(width * scale_x), int(height * scale_y))
        self._current_image = cv2.resize(self._current_image, new_size)


    # Undo Support
    def undo(self):
        """Revert to the previous image state."""
        if self._history:
            self._current_image = self._history.pop()
