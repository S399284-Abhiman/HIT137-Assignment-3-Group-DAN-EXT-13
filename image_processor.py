"""
Image Processor Module

This module defines the base ImageProcessor class and specific filter classes.
It demonstrates inheritance, polymorphism, method overriding, and static methods.

OOP Concepts Demonstrated:
- Inheritance: FilterProcessor inherits from ImageProcessor
- Polymorphism: Different filters override the apply() method
- Static Methods: Utility methods that don't need instance data
- Method Overriding: Child classes override parent methods
- Super(): Calling parent class methods
"""

import cv2
import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple


class ImageProcessor(ABC):
    """
    Abstract base class for image processing operations.
    
    This class defines the interface that all image processors must follow.
    It demonstrates the use of abstract methods to enforce a contract on
    derived classes.
    
    Instance Attributes:
        _name (str): Name of the processor (protected attribute)
    """
    
    def __init__(self, name: str):
        """
        Constructor for ImageProcessor.
        
        Args:
            name (str): Name of this processor
        """
        self._name = name  # Protected attribute (single underscore)
    
    @property
    def name(self) -> str:
        """
        Get the processor name.
        
        Returns:
            str: Name of the processor
        """
        return self._name
    
    @abstractmethod
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        Abstract method to apply the processing operation.
        
        This method must be overridden by all child classes.
        Demonstrates polymorphism - each child implements this differently.
        
        Args:
            image (numpy.ndarray): Input image
            **kwargs: Additional parameters specific to each processor
            
        Returns:
            numpy.ndarray: Processed image
        """
        pass
    
    @staticmethod
    def validate_image(image: np.ndarray) -> bool:
        """
        Static method to validate if the input is a valid image.
        
        Demonstrates @staticmethod decorator. Static methods don't access
        instance or class data - they're utility functions grouped with the class.
        
        Args:
            image (numpy.ndarray): Image to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return image is not None and isinstance(image, np.ndarray) and image.size > 0
    
    @staticmethod
    def convert_to_uint8(image: np.ndarray) -> np.ndarray:
        """
        Static utility method to ensure image is in uint8 format.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Image in uint8 format
        """
        if image.dtype != np.uint8:
            # Clip values to valid range and convert
            image = np.clip(image, 0, 255)
            image = image.astype(np.uint8)
        return image
    
    def __str__(self) -> str:
        """
        Magic method for string representation.
        
        Returns:
            str: Name of the processor
        """
        return f"{self.__class__.__name__}: {self._name}"


class FilterProcessor(ImageProcessor):
    """
    Base class for filter-based image processors.
    
    Demonstrates inheritance by extending ImageProcessor.
    This class inherits all methods and attributes from ImageProcessor.
    """
    
    def __init__(self, name: str, description: str):
        """
        Constructor for FilterProcessor.
        
        Demonstrates super() to call parent class constructor.
        
        Args:
            name (str): Name of the filter
            description (str): Description of what the filter does
        """
        # Call parent class constructor using super()
        super().__init__(name)
        self._description = description
    
    @property
    def description(self) -> str:
        """
        Get filter description.
        
        Returns:
            str: Description of the filter
        """
        return self._description
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        Base implementation of apply method.
        
        This method will be overridden by child classes (method overriding).
        
        Args:
            image (numpy.ndarray): Input image
            **kwargs: Additional parameters
            
        Returns:
            numpy.ndarray: Processed image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image provided")
        return image


class GrayscaleFilter(FilterProcessor):
    """
    Grayscale conversion filter.
    
    Demonstrates method overriding - overrides the apply() method
    from the parent FilterProcessor class.
    """
    
    def __init__(self):
        """Constructor initializing grayscale filter."""
        super().__init__("Grayscale", "Converts image to black and white")
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        Apply grayscale conversion.
        
        Method overriding: This overrides the parent's apply() method
        with specific grayscale implementation.
        
        Args:
            image (numpy.ndarray): Input BGR image
            
        Returns:
            numpy.ndarray: Grayscale image (still in BGR format for display)
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for grayscale conversion")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Convert back to BGR for consistent display
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


class BlurFilter(FilterProcessor):
    """
    Gaussian blur filter with adjustable intensity.
    
    Demonstrates method overriding with additional parameters.
    """
    
    def __init__(self):
        """Constructor initializing blur filter."""
        super().__init__("Blur", "Applies Gaussian blur effect")
    
    def apply(self, image: np.ndarray, intensity: int = 5, **kwargs) -> np.ndarray:
        """
        Apply Gaussian blur.
        
        Args:
            image (numpy.ndarray): Input image
            intensity (int): Blur intensity (must be odd number)
            
        Returns:
            numpy.ndarray: Blurred image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for blur")
        
        # Ensure intensity is odd and positive
        kernel_size = max(1, intensity if intensity % 2 == 1 else intensity + 1)
        
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


class EdgeDetectionFilter(FilterProcessor):
    """
    Canny edge detection filter.
    
    Demonstrates method overriding with multiple parameters.
    """
    
    def __init__(self):
        """Constructor initializing edge detection filter."""
        super().__init__("Edge Detection", "Detects edges using Canny algorithm")
    
    def apply(self, image: np.ndarray, threshold1: int = 100, 
              threshold2: int = 200, **kwargs) -> np.ndarray:
        """
        Apply Canny edge detection.
        
        Args:
            image (numpy.ndarray): Input image
            threshold1 (int): First threshold for hysteresis
            threshold2 (int): Second threshold for hysteresis
            
        Returns:
            numpy.ndarray: Edge-detected image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for edge detection")
        
        # Convert to grayscale first
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, threshold1, threshold2)
        
        # Convert back to BGR for display
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


class BrightnessAdjustment(FilterProcessor):
    """
    Brightness adjustment filter.
    
    Demonstrates method overriding for brightness manipulation.
    """
    
    def __init__(self):
        """Constructor initializing brightness adjustment."""
        super().__init__("Brightness", "Adjusts image brightness")
    
    def apply(self, image: np.ndarray, value: int = 0, **kwargs) -> np.ndarray:
        """
        Adjust brightness.
        
        Args:
            image (numpy.ndarray): Input image
            value (int): Brightness adjustment value (-100 to 100)
            
        Returns:
            numpy.ndarray: Brightness-adjusted image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for brightness adjustment")
        
        # Add value to all pixels
        adjusted = image.astype(np.int16) + value
        
        # Ensure result is in uint8 format
        return self.convert_to_uint8(adjusted)


class ContrastAdjustment(FilterProcessor):
    """
    Contrast adjustment filter.
    
    Demonstrates method overriding for contrast manipulation.
    """
    
    def __init__(self):
        """Constructor initializing contrast adjustment."""
        super().__init__("Contrast", "Adjusts image contrast")
    
    def apply(self, image: np.ndarray, value: float = 1.0, **kwargs) -> np.ndarray:
        """
        Adjust contrast.
        
        Args:
            image (numpy.ndarray): Input image
            value (float): Contrast multiplier (0.5 to 3.0)
            
        Returns:
            numpy.ndarray: Contrast-adjusted image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for contrast adjustment")
        
        # Apply contrast adjustment
        adjusted = image.astype(np.float32) * value
        
        return self.convert_to_uint8(adjusted)


class RotationFilter(FilterProcessor):
    """
    Image rotation filter.
    
    Demonstrates method overriding for geometric transformations.
    """
    
    def __init__(self):
        """Constructor initializing rotation filter."""
        super().__init__("Rotation", "Rotates image by specified angle")
    
    def apply(self, image: np.ndarray, angle: int = 90, **kwargs) -> np.ndarray:
        """
        Rotate image by specified angle.
        
        Args:
            image (numpy.ndarray): Input image
            angle (int): Rotation angle (90, 180, or 270)
            
        Returns:
            numpy.ndarray: Rotated image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for rotation")
        
        # Map angle to OpenCV rotation code
        rotation_map = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }
        
        if angle in rotation_map:
            return cv2.rotate(image, rotation_map[angle])
        else:
            # Custom angle rotation
            height, width = image.shape[:2]
            center = (width // 2, height // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(image, matrix, (width, height))


class FlipFilter(FilterProcessor):
    """
    Image flip filter.
    
    Demonstrates method overriding for flip operations.
    """
    
    def __init__(self):
        """Constructor initializing flip filter."""
        super().__init__("Flip", "Flips image horizontally or vertically")
    
    def apply(self, image: np.ndarray, direction: str = "horizontal", **kwargs) -> np.ndarray:
        """
        Flip image in specified direction.
        
        Args:
            image (numpy.ndarray): Input image
            direction (str): "horizontal" or "vertical"
            
        Returns:
            numpy.ndarray: Flipped image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for flip")
        
        if direction.lower() == "horizontal":
            return cv2.flip(image, 1)  # Flip horizontally
        elif direction.lower() == "vertical":
            return cv2.flip(image, 0)  # Flip vertically
        else:
            return cv2.flip(image, -1)  # Flip both


class ResizeFilter(FilterProcessor):
    """
    Image resize filter.
    
    Demonstrates method overriding for scaling operations.
    """
    
    def __init__(self):
        """Constructor initializing resize filter."""
        super().__init__("Resize", "Resizes image to specified dimensions")
    
    def apply(self, image: np.ndarray, width: int = None, 
              height: int = None, scale: float = 1.0, **kwargs) -> np.ndarray:
        """
        Resize image.
        
        Args:
            image (numpy.ndarray): Input image
            width (int): Target width (None to use scale)
            height (int): Target height (None to use scale)
            scale (float): Scale factor if width/height not specified
            
        Returns:
            numpy.ndarray: Resized image
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for resize")
        
        if width and height:
            # Resize to specific dimensions
            return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        else:
            # Resize by scale factor
            new_width = int(image.shape[1] * scale)
            new_height = int(image.shape[0] * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
