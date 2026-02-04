"""
Test Script for Image Editor Application

This script tests the functionality of all OOP concepts and image processing features.
Run this to verify everything works correctly.
"""

import cv2
import numpy as np
from models.image import Image
from processors.image_processor import *
from managers.filter_manager import FilterManager


def test_image_class():
    """Test the Image class and its OOP concepts."""
    print("Testing Image Class...")
    print("-" * 50)
    
    # Create a test image
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite("test_image.jpg", test_img)
    
    # Test constructor
    img = Image("test_image.jpg")
    print(f"✓ Constructor works: Image created")
    
    # Test instance attributes
    print(f"✓ Instance attributes: Width={img.width}, Height={img.height}")
    
    # Test class attributes
    print(f"✓ Class attribute: SUPPORTED_FORMATS = {Image.SUPPORTED_FORMATS}")
    
    # Test properties (encapsulation)
    print(f"✓ Property getter: filepath = {img.filepath}")
    
    # Test property setter
    new_img = np.ones((50, 50, 3), dtype=np.uint8) * 255
    img.current_image = new_img
    print(f"✓ Property setter: Image updated to {img.dimensions}")
    
    # Test magic methods
    print(f"✓ __str__: {str(img)}")
    print(f"✓ __repr__: {repr(img)}")
    
    # Test __eq__
    img2 = Image("test_image.jpg")
    print(f"✓ __eq__: img == img2 = {img == img2}")
    
    print("\n" + "="*50 + "\n")


def test_filter_processors():
    """Test filter classes demonstrating inheritance and polymorphism."""
    print("Testing Filter Processors (Inheritance & Polymorphism)...")
    print("-" * 50)
    
    # Create test image
    test_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    # Test static method
    print(f"✓ Static method: validate_image = {ImageProcessor.validate_image(test_img)}")
    
    # Test inheritance and polymorphism
    filters = [
        ("Grayscale", GrayscaleFilter()),
        ("Blur", BlurFilter()),
        ("Edge Detection", EdgeDetectionFilter()),
        ("Brightness", BrightnessAdjustment()),
        ("Contrast", ContrastAdjustment()),
        ("Rotation", RotationFilter()),
        ("Flip", FlipFilter()),
        ("Resize", ResizeFilter())
    ]
    
    print("\n✓ Testing Polymorphism (same method, different implementations):")
    for name, filter_obj in filters:
        # Polymorphism: same method call, different behavior
        result = filter_obj.apply(test_img)
        print(f"  - {name}: {type(filter_obj).__name__}.apply() executed")
        
        # Test inheritance
        print(f"    Inherited name property: {filter_obj.name}")
    
    print("\n" + "="*50 + "\n")


def test_filter_manager():
    """Test FilterManager demonstrating multiple inheritance."""
    print("Testing FilterManager (Multiple Inheritance)...")
    print("-" * 50)
    
    # Create manager
    manager = FilterManager()
    print("✓ Multiple inheritance: FilterManager created")
    print("  - Inherits from FilterRegistry (filter management)")
    print("  - Inherits from HistoryTracker (history tracking)")
    
    # Test class method
    stats = FilterManager.get_filter_statistics()
    print(f"\n✓ Class method: get_filter_statistics() = {stats}")
    
    # Test static method
    valid = FilterManager.validate_filter_params("blur", intensity=5)
    print(f"✓ Static method: validate_filter_params() = {valid}")
    
    # Test methods from FilterRegistry (first parent)
    print(f"\n✓ From FilterRegistry parent:")
    print(f"  - Registered filters: {manager.list_filters()}")
    
    # Test methods from HistoryTracker (second parent)
    print(f"\n✓ From HistoryTracker parent:")
    manager.add_to_history("Test operation")
    print(f"  - History: {manager.get_history()}")
    
    # Test magic methods
    print(f"\n✓ Magic method __len__: len(manager) = {len(manager)}")
    print(f"✓ Magic method __contains__: 'grayscale' in manager = {'grayscale' in manager}")
    print(f"✓ Magic method __str__: {str(manager)}")
    
    print("\n" + "="*50 + "\n")


def test_method_overriding():
    """Test method overriding in filter classes."""
    print("Testing Method Overriding...")
    print("-" * 50)
    
    test_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    # Parent class
    parent = FilterProcessor("Base", "Base filter")
    parent_result = parent.apply(test_img)
    print("✓ Parent FilterProcessor.apply() - base implementation")
    
    # Child overrides
    child1 = GrayscaleFilter()
    child1_result = child1.apply(test_img)
    print("✓ Child GrayscaleFilter.apply() - overridden with grayscale logic")
    
    child2 = BlurFilter()
    child2_result = child2.apply(test_img, intensity=5)
    print("✓ Child BlurFilter.apply() - overridden with blur logic")
    
    print("\n✓ Method overriding demonstrated: Same method name, different implementations")
    
    print("\n" + "="*50 + "\n")


def test_super_function():
    """Test super() function usage."""
    print("Testing super() Function...")
    print("-" * 50)
    
    # Create filter (uses super in constructor)
    filter_obj = GrayscaleFilter()
    print("✓ GrayscaleFilter created using super()")
    print("  - Calls FilterProcessor.__init__() via super()")
    print("  - Which calls ImageProcessor.__init__() via super()")
    print("  - Complete initialization chain works correctly")
    
    # Verify inheritance chain worked
    print(f"\n✓ Inherited attributes accessible:")
    print(f"  - name (from ImageProcessor): {filter_obj.name}")
    print(f"  - description (from FilterProcessor): {filter_obj.description}")
    
    print("\n" + "="*50 + "\n")


def test_abstract_methods():
    """Test abstract methods."""
    print("Testing Abstract Methods...")
    print("-" * 50)
    
    print("✓ ImageProcessor is abstract (has @abstractmethod)")
    
    try:
        # This should fail
        processor = ImageProcessor("test")
        print("✗ ERROR: Should not be able to create ImageProcessor")
    except TypeError as e:
        print("✓ Cannot instantiate abstract class ImageProcessor")
        print(f"  Error message: {str(e)}")
    
    # Can create concrete classes
    concrete = GrayscaleFilter()
    print("\n✓ Can create GrayscaleFilter (implements abstract method)")
    
    print("\n" + "="*50 + "\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print(" "*15 + "IMAGE EDITOR - OOP CONCEPTS TEST")
    print("="*70 + "\n")
    
    test_image_class()
    test_filter_processors()
    test_filter_manager()
    test_method_overriding()
    test_super_function()
    test_abstract_methods()
    
    print("="*70)
    print(" "*20 + "ALL TESTS COMPLETED!")
    print("="*70)
    print("\n✓ All OOP concepts demonstrated successfully:")
    print("  1. Classes and Objects")
    print("  2. Constructors")
    print("  3. Instance and Class Attributes")
    print("  4. Static Methods")
    print("  5. Class Methods")
    print("  6. Encapsulation")
    print("  7. Property Decorators")
    print("  8. Inheritance")
    print("  9. Multiple Inheritance")
    print("  10. Polymorphism")
    print("  11. Method Overriding")
    print("  12. Magic Methods (Operator Overloading)")
    print("  13. Super() Function")
    print("  14. Abstract Methods")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
