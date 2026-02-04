"""
Filter Manager Module

This module defines the FilterManager class that manages all available filters.
It demonstrates multiple inheritance, class interaction, and advanced OOP concepts.

OOP Concepts Demonstrated:
- Multiple Inheritance: Inheriting from multiple base classes
- Class Interaction: FilterManager works with Image and processors
- Class Methods: @classmethod decorator
- Static Methods: Utility methods
"""

from typing import Dict, List, Optional
import numpy as np
from models.image import Image
from processors.image_processor import (
    FilterProcessor, GrayscaleFilter, BlurFilter, EdgeDetectionFilter,
    BrightnessAdjustment, ContrastAdjustment, RotationFilter, 
    FlipFilter, ResizeFilter
)


class FilterRegistry:
    """
    Base class for managing filter registration.
    
    This class will be used in multiple inheritance to demonstrate
    how multiple base classes can be combined.
    """
    
    def __init__(self):
        """Initialize the filter registry."""
        self._registry: Dict[str, FilterProcessor] = {}
    
    def register_filter(self, key: str, filter_obj: FilterProcessor) -> None:
        """
        Register a filter with a unique key.
        
        Args:
            key (str): Unique identifier for the filter
            filter_obj (FilterProcessor): Filter instance to register
        """
        self._registry[key] = filter_obj
    
    def get_filter(self, key: str) -> Optional[FilterProcessor]:
        """
        Retrieve a filter by its key.
        
        Args:
            key (str): Filter identifier
            
        Returns:
            FilterProcessor or None: The filter if found, None otherwise
        """
        return self._registry.get(key)
    
    def list_filters(self) -> List[str]:
        """
        List all registered filter keys.
        
        Returns:
            list: List of filter keys
        """
        return list(self._registry.keys())


class HistoryTracker:
    """
    Base class for tracking operation history.
    
    This class will be combined with FilterRegistry through multiple inheritance.
    """
    
    def __init__(self):
        """Initialize the history tracker."""
        self._history: List[str] = []
    
    def add_to_history(self, operation: str) -> None:
        """
        Add an operation to the history.
        
        Args:
            operation (str): Description of the operation performed
        """
        self._history.append(operation)
    
    def get_history(self) -> List[str]:
        """
        Get the complete operation history.
        
        Returns:
            list: List of operations performed
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the operation history."""
        self._history.clear()
    
    @property
    def last_operation(self) -> Optional[str]:
        """
        Get the last operation performed.
        
        Returns:
            str or None: Last operation or None if history is empty
        """
        return self._history[-1] if self._history else None


class FilterManager(FilterRegistry, HistoryTracker):
    """
    Manages all image filters and their application.
    
    Demonstrates Multiple Inheritance: Inherits from both FilterRegistry
    and HistoryTracker, combining functionality from both parent classes.
    
    This class also demonstrates class interaction by working with Image
    objects and various FilterProcessor instances.
    
    Class Attributes:
        _instance (FilterManager): Singleton instance (class attribute)
        filter_count (int): Total number of filters managed
    """
    
    # Class attribute for tracking total filters across all instances
    filter_count = 0
    _instance = None  # For singleton pattern (optional)
    
    def __init__(self):
        """
        Constructor demonstrating multiple inheritance initialization.
        
        Calls constructors of both parent classes using super().
        This demonstrates proper initialization in multiple inheritance.
        """
        # Initialize both parent classes
        FilterRegistry.__init__(self)
        HistoryTracker.__init__(self)
        
        # Instance attributes
        self._current_image: Optional[Image] = None
        self._undo_stack: List[np.ndarray] = []
        self._redo_stack: List[np.ndarray] = []
        
        # Register all available filters
        self._register_default_filters()
    
    def _register_default_filters(self) -> None:
        """
        Private method to register all default filters.
        
        Demonstrates encapsulation and class interaction by creating
        instances of various FilterProcessor subclasses.
        """
        # Register all filter types
        self.register_filter("grayscale", GrayscaleFilter())
        self.register_filter("blur", BlurFilter())
        self.register_filter("edge", EdgeDetectionFilter())
        self.register_filter("brightness", BrightnessAdjustment())
        self.register_filter("contrast", ContrastAdjustment())
        self.register_filter("rotate", RotationFilter())
        self.register_filter("flip", FlipFilter())
        self.register_filter("resize", ResizeFilter())
        
        # Update class attribute
        FilterManager.filter_count = len(self._registry)
    
    @property
    def current_image(self) -> Optional[Image]:
        """
        Get the current image being processed.
        
        Returns:
            Image or None: Current image object
        """
        return self._current_image
    
    @current_image.setter
    def current_image(self, image: Image) -> None:
        """
        Set the current image.
        
        Args:
            image (Image): Image object to set as current
        """
        self._current_image = image
        # Clear undo/redo stacks when new image is loaded
        self._undo_stack.clear()
        self._redo_stack.clear()
    
    def apply_filter(self, filter_key: str, **kwargs) -> bool:
        """
        Apply a filter to the current image.
        
        Demonstrates class interaction: this method works with both
        Image objects and FilterProcessor objects.
        
        Args:
            filter_key (str): Key of the filter to apply
            **kwargs: Parameters to pass to the filter
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self._current_image is None:
            return False
        
        # Get the filter from registry (inherited from FilterRegistry)
        filter_obj = self.get_filter(filter_key)
        
        if filter_obj is None:
            return False
        
        try:
            # Save current state for undo
            self._undo_stack.append(self._current_image.current_image)
            self._redo_stack.clear()  # Clear redo stack on new operation
            
            # Apply the filter
            current_img = self._current_image.current_image
            processed_img = filter_obj.apply(current_img, **kwargs)
            
            # Update the image
            self._current_image.current_image = processed_img
            
            # Add to history (inherited from HistoryTracker)
            operation = f"Applied {filter_obj.name}"
            if kwargs:
                operation += f" with params: {kwargs}"
            self.add_to_history(operation)
            
            return True
            
        except Exception as e:
            # Restore previous state if error occurs
            if self._undo_stack:
                self._undo_stack.pop()
            print(f"Error applying filter: {e}")
            return False
    
    def undo(self) -> bool:
        """
        Undo the last operation.
        
        Returns:
            bool: True if undo was successful, False otherwise
        """
        if not self._undo_stack or self._current_image is None:
            return False
        
        # Save current state to redo stack
        self._redo_stack.append(self._current_image.current_image)
        
        # Restore previous state
        previous_state = self._undo_stack.pop()
        self._current_image.current_image = previous_state
        
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone operation.
        
        Returns:
            bool: True if redo was successful, False otherwise
        """
        if not self._redo_stack or self._current_image is None:
            return False
        
        # Save current state to undo stack
        self._undo_stack.append(self._current_image.current_image)
        
        # Restore redo state
        redo_state = self._redo_stack.pop()
        self._current_image.current_image = redo_state
        
        return True
    
    def can_undo(self) -> bool:
        """
        Check if undo is available.
        
        Returns:
            bool: True if undo stack is not empty
        """
        return bool(self._undo_stack)
    
    def can_redo(self) -> bool:
        """
        Check if redo is available.
        
        Returns:
            bool: True if redo stack is not empty
        """
        return bool(self._redo_stack)
    
    @classmethod
    def get_filter_statistics(cls) -> Dict[str, int]:
        """
        Class method to get statistics about filters.
        
        Demonstrates @classmethod decorator. Class methods receive the class
        as their first argument (cls) rather than an instance (self).
        They can access class attributes but not instance attributes.
        
        Returns:
            dict: Dictionary with filter statistics
        """
        return {
            "total_filters": cls.filter_count,
            "class_name": cls.__name__
        }
    
    @staticmethod
    def validate_filter_params(filter_type: str, **kwargs) -> bool:
        """
        Static method to validate filter parameters.
        
        Demonstrates @staticmethod. Static methods don't receive self or cls
        as they don't need access to instance or class data.
        
        Args:
            filter_type (str): Type of filter
            **kwargs: Parameters to validate
            
        Returns:
            bool: True if parameters are valid
        """
        # Basic validation logic
        if filter_type == "blur":
            intensity = kwargs.get("intensity", 5)
            return 1 <= intensity <= 50
        elif filter_type == "brightness":
            value = kwargs.get("value", 0)
            return -100 <= value <= 100
        elif filter_type == "contrast":
            value = kwargs.get("value", 1.0)
            return 0.5 <= value <= 3.0
        
        return True  # No specific validation for other types
    
    def get_filter_info(self, filter_key: str) -> Optional[Dict[str, str]]:
        """
        Get information about a specific filter.
        
        Args:
            filter_key (str): Filter identifier
            
        Returns:
            dict or None: Dictionary with filter info or None if not found
        """
        filter_obj = self.get_filter(filter_key)
        
        if filter_obj is None:
            return None
        
        return {
            "name": filter_obj.name,
            "description": filter_obj.description,
            "type": type(filter_obj).__name__
        }
    
    def __str__(self) -> str:
        """
        Magic method for string representation.
        
        Returns:
            str: String describing the FilterManager state
        """
        return (f"FilterManager: {len(self._registry)} filters registered, "
                f"{len(self._history)} operations performed")
    
    def __len__(self) -> int:
        """
        Magic method to support len() function.
        
        Demonstrates operator overloading with __len__.
        Allows using len(filter_manager) to get the number of filters.
        
        Returns:
            int: Number of registered filters
        """
        return len(self._registry)
    
    def __contains__(self, filter_key: str) -> bool:
        """
        Magic method to support 'in' operator.
        
        Demonstrates operator overloading with __contains__.
        Allows using: if "grayscale" in filter_manager
        
        Args:
            filter_key (str): Filter key to check
            
        Returns:
            bool: True if filter exists, False otherwise
        """
        return filter_key in self._registry
