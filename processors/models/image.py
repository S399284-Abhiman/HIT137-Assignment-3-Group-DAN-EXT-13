"""
Image Model Module

This module defines the Image class that represents an image in the editor.
It demonstrates key OOP concepts including encapsulation, constructors,
instance/class attributes, properties, and magic methods.

OOP Concepts Demonstrated:
- Encapsulation: Private attributes with property decorators
- Constructor: __init__ method for object initialization
- Instance Attributes: _original_image, _current_image, etc.
- Class Attributes: SUPPORTED_FORMATS (shared across all instances)
- Properties: @property decorator for controlled access
- Magic Methods: __str__ and __repr__ for string representation
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class Image:
    """
    Represents an image with original and current states.
    
    This class encapsulates image data and provides controlled access
    through property decorators. It maintains both the original image
    (for undo operations) and the current working image.
    
    Class Attributes:
        SUPPORTED_FORMATS (tuple): File formats supported by the editor
    
    Instance Attributes:
        _filepath (str): Path to the image file (private, encapsulated)
        _original_image (numpy.ndarray): Original unmodified image
        _current_image (numpy.ndarray): Current working image
        _width (int): Current image width
        _height (int): Current image height
    """
    
    # Class attribute - shared across all Image instances
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp')
    
    def __init__(self, filepath: str):
        """
        Constructor to initialize an Image object.
        
        Demonstrates the constructor concept by initializing all instance
        attributes. Uses encapsulation by making attributes private (underscore prefix).
        
        Args:
            filepath (str): Path to the image file to load
            
        Raises:
            FileNotFoundError: If the image file doesn't exist
            ValueError: If the image cannot be loaded
        """
        self._filepath = filepath  # Private instance attribute (encapsulation)
        self._original_image = None  # Store original for undo
        self._current_image = None  # Current working image
        self._width = 0  # Image width
        self._height = 0  # Image height
        
        # Load the image upon initialization
        self._load_image()
    
    def _load_image(self) -> None:
        """
        Private method to load image from filepath.
        
        Demonstrates encapsulation by making this a private method (underscore prefix).
        This method should only be called internally by the class.
        
        Raises:
            ValueError: If image cannot be loaded from the filepath
        """
        # Load image using OpenCV
        image = cv2.imread(self._filepath)
        
        if image is None:
            raise ValueError(f"Unable to load image from {self._filepath}")
        
        # Store both original and current versions
        self._original_image = image.copy()
        self._current_image = image.copy()
        
        # Store dimensions
        self._height, self._width = image.shape[:2]
    
    # Property decorator for controlled access (getter)
    @property
    def filepath(self) -> str:
        """
        Get the filepath of the image.
        
        Demonstrates the @property decorator for encapsulation.
        Provides read-only access to the private _filepath attribute.
        
        Returns:
            str: The image filepath
        """
        return self._filepath
    
    @property
    def original_image(self) -> np.ndarray:
        """
        Get the original unmodified image.
        
        Returns:
            numpy.ndarray: Copy of the original image
        """
        return self._original_image.copy()
    
    @property
    def current_image(self) -> np.ndarray:
        """
        Get the current working image.
        
        Returns:
            numpy.ndarray: Copy of the current image
        """
        return self._current_image.copy()
    
    @current_image.setter
    def current_image(self, image: np.ndarray) -> None:
        """
        Set the current working image.
        
        Demonstrates the @property.setter decorator for controlled modification.
        Allows external code to update the current image while maintaining encapsulation.
        
        Args:
            image (numpy.ndarray): New image to set as current
        """
        self._current_image = image.copy()
        self._height, self._width = image.shape[:2]
    
    @property
    def width(self) -> int:
        """
        Get current image width.
        
        Returns:
            int: Image width in pixels
        """
        return self._width
    
    @property
    def height(self) -> int:
        """
        Get current image height.
        
        Returns:
            int: Image height in pixels
        """
        return self._height
    
    @property
    def dimensions(self) -> Tuple[int, int]:
        """
        Get current image dimensions as a tuple.
        
        Returns:
            tuple: (width, height) in pixels
        """
        return (self._width, self._height)
    
    def reset_to_original(self) -> None:
        """
        Reset the current image to the original state.
        
        This method is useful for implementing an undo-all functionality.
        """
        self._current_image = self._original_image.copy()
        self._height, self._width = self._original_image.shape[:2]
    
    def update_original(self) -> None:
        """
        Update the original image to match the current state.
        
        This can be used after saving to make the current state the new baseline.
        """
        self._original_image = self._current_image.copy()
    
    # Magic method: __str__ for user-friendly string representation
    def __str__(self) -> str:
        """
        Return user-friendly string representation.
        
        Demonstrates the __str__ magic method for operator overloading.
        This method is called when using str() or print() on an Image object.
        
        Returns:
            str: Formatted string with image information
        """
        return (f"Image: {self._filepath}\n"
                f"Dimensions: {self._width}x{self._height} pixels")
    
    # Magic method: __repr__ for developer-friendly representation
    def __repr__(self) -> str:
        """
        Return developer-friendly string representation.
        
        Demonstrates the __repr__ magic method. This is used in debugging
        and should ideally return a string that could recreate the object.
        
        Returns:
            str: String representation for developers
        """
        return f"Image(filepath='{self._filepath}', dimensions=({self._width}, {self._height}))"
    
    # Magic method: __eq__ for equality comparison
    def __eq__(self, other) -> bool:
        """
        Compare two Image objects for equality.
        
        Demonstrates the __eq__ magic method for operator overloading.
        Allows using the == operator to compare Image objects.
        
        Args:
            other: Another object to compare with
            
        Returns:
            bool: True if images have the same content, False otherwise
        """
        if not isinstance(other, Image):
            return False
        
        # Compare images pixel by pixel
        return np.array_equal(self._current_image, other._current_image)
