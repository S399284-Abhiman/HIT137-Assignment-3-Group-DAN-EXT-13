# OOP Concepts - Detailed Explanation

This document provides a comprehensive explanation of all Object-Oriented Programming concepts used in the Image Editor application, with specific code examples from the project.

---

## Table of Contents

1. [Classes and Objects](#1-classes-and-objects)
2. [Constructors](#2-constructors)
3. [Instance and Class Attributes](#3-instance-and-class-attributes)
4. [Static Methods](#4-static-methods)
5. [Class Methods](#5-class-methods)
6. [Encapsulation](#6-encapsulation)
7. [Property Decorators](#7-property-decorators)
8. [Inheritance](#8-inheritance)
9. [Multiple Inheritance](#9-multiple-inheritance)
10. [Polymorphism](#10-polymorphism)
11. [Method Overriding](#11-method-overriding)
12. [Magic Methods](#12-magic-methods)
13. [Super() Function](#13-super-function)
14. [Abstract Methods](#14-abstract-methods)

---

## 1. Classes and Objects

### What is it?
A **class** is a blueprint for creating objects. An **object** is an instance of a class.

### Where it's used in our project:
```python
# Class definition (models/image.py)
class Image:
    """Represents an image with original and current states."""
    pass

# Creating an object
my_image = Image("photo.jpg")  # Object created from Image class
```

### Why it matters:
- Classes organize related data and functions together
- Objects represent real-world entities (like an image file)
- Promotes code reusability and organization

### Complete example from our code:
- **Image class** (models/image.py): Represents an image file
- **FilterProcessor class** (processors/image_processor.py): Represents an image filter
- **FilterManager class** (managers/filter_manager.py): Manages multiple filters
- **ImageEditorApp class** (gui/main_window.py): Represents the entire application

---

## 2. Constructors

### What is it?
The `__init__` method is a constructor - it's called automatically when creating a new object. It initializes the object's attributes.

### Where it's used:
```python
# From models/image.py
class Image:
    def __init__(self, filepath: str):
        """Constructor to initialize an Image object."""
        self._filepath = filepath
        self._original_image = None
        self._current_image = None
        self._width = 0
        self._height = 0
        self._load_image()  # Called automatically during initialization
```

### Usage:
```python
# When you create an Image object, __init__ is called automatically
image = Image("photo.jpg")
# The constructor sets up all the attributes and loads the image
```

### Why it matters:
- Ensures every object starts in a valid state
- Allows passing initial data when creating objects
- Performs necessary setup operations

---

## 3. Instance and Class Attributes

### Instance Attributes
**What**: Variables unique to each object (prefixed with `self`)

```python
# From models/image.py
class Image:
    def __init__(self, filepath: str):
        self._filepath = filepath      # Instance attribute - unique to each Image
        self._current_image = None     # Instance attribute
        self._width = 0                # Instance attribute
```

**Usage**:
```python
image1 = Image("photo1.jpg")
image2 = Image("photo2.jpg")
# Each has its own _filepath, _current_image, etc.
```

### Class Attributes
**What**: Variables shared by ALL instances of a class

```python
# From models/image.py
class Image:
    # Class attribute - shared by all Image objects
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp')
    
# From managers/filter_manager.py
class FilterManager:
    filter_count = 0  # Class attribute - tracks total filters
```

**Usage**:
```python
# Access without creating an object
print(Image.SUPPORTED_FORMATS)  # ('.jpg', '.jpeg', '.png', '.bmp')

# Shared across all instances
manager1 = FilterManager()
manager2 = FilterManager()
# Both share the same filter_count
```

### Why it matters:
- **Instance attributes**: Store unique data for each object
- **Class attributes**: Store shared data/constants for all objects

---

## 4. Static Methods

### What is it?
Methods that don't need access to instance (`self`) or class (`cls`) data. They're utility functions grouped with the class.

### Where it's used:
```python
# From processors/image_processor.py
class ImageProcessor:
    @staticmethod
    def validate_image(image: np.ndarray) -> bool:
        """
        Static method to validate if the input is a valid image.
        No access to self or cls needed.
        """
        return image is not None and isinstance(image, np.ndarray) and image.size > 0
    
    @staticmethod
    def convert_to_uint8(image: np.ndarray) -> np.ndarray:
        """Static utility method to ensure image is in uint8 format."""
        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255)
            image = image.astype(np.uint8)
        return image
```

### Usage:
```python
# Can be called on the class directly
if ImageProcessor.validate_image(my_image):
    print("Valid image")

# Or on an instance
processor = GrayscaleFilter()
if processor.validate_image(my_image):
    print("Valid image")
```

### Another example from our code:
```python
# From managers/filter_manager.py
class FilterManager:
    @staticmethod
    def validate_filter_params(filter_type: str, **kwargs) -> bool:
        """Validate filter parameters without needing instance data."""
        if filter_type == "blur":
            intensity = kwargs.get("intensity", 5)
            return 1 <= intensity <= 50
        # ... more validation
```

### Why it matters:
- Groups related utility functions with the class
- No need to create an object to use them
- Clearly indicates the method doesn't use instance state

---

## 5. Class Methods

### What is it?
Methods that receive the class itself (as `cls`) rather than an instance. Used for operations on the class itself.

### Where it's used:
```python
# From managers/filter_manager.py
class FilterManager:
    filter_count = 0  # Class attribute
    
    @classmethod
    def get_filter_statistics(cls) -> Dict[str, int]:
        """
        Class method to get statistics about filters.
        Receives 'cls' (the class itself) as first parameter.
        """
        return {
            "total_filters": cls.filter_count,  # Access class attribute
            "class_name": cls.__name__
        }
```

### Usage:
```python
# Call on the class directly
stats = FilterManager.get_filter_statistics()
print(stats)  # {'total_filters': 8, 'class_name': 'FilterManager'}

# Can also call on an instance
manager = FilterManager()
stats = manager.get_filter_statistics()
```

### Why it matters:
- Access class-level data without needing an instance
- Often used for factory methods (alternative constructors)
- Can modify class attributes that affect all instances

### Difference from Static Methods:
- **Static method**: No access to instance (`self`) or class (`cls`)
- **Class method**: Has access to class (`cls`) but not instance (`self`)

---

## 6. Encapsulation

### What is it?
Hiding internal details and providing controlled access to data. Use private attributes (underscore prefix) and expose through methods/properties.

### Where it's used:
```python
# From models/image.py
class Image:
    def __init__(self, filepath: str):
        # Private attributes (single underscore prefix)
        self._filepath = filepath           # Hidden from direct access
        self._original_image = None         # Encapsulated
        self._current_image = None          # Encapsulated
        self._width = 0                     # Encapsulated
        self._height = 0                    # Encapsulated
    
    def _load_image(self) -> None:
        """
        Private method (underscore prefix).
        Should only be called internally by the class.
        """
        # Internal implementation details hidden from users
        pass
```

### Usage - What NOT to do:
```python
image = Image("photo.jpg")
# DON'T access private attributes directly:
# image._current_image = something  # Bad practice!
```

### Usage - Correct way:
```python
image = Image("photo.jpg")
# Use public methods/properties instead:
current = image.current_image  # Using @property (controlled access)
image.current_image = new_image  # Using @property.setter
```

### Why it matters:
- Protects internal state from accidental modification
- Allows changing implementation without breaking code that uses the class
- Provides validation and control over how data is accessed/modified

---

## 7. Property Decorators

### What is it?
The `@property` decorator allows you to use methods like attributes, providing controlled access to private data.

### Where it's used:
```python
# From models/image.py
class Image:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._current_image = None
        self._width = 0
        self._height = 0
    
    # GETTER - Read-only access
    @property
    def filepath(self) -> str:
        """Get the filepath of the image."""
        return self._filepath
    
    # GETTER for current_image
    @property
    def current_image(self) -> np.ndarray:
        """Get the current working image."""
        return self._current_image.copy()
    
    # SETTER for current_image
    @current_image.setter
    def current_image(self, image: np.ndarray) -> None:
        """Set the current working image with validation."""
        self._current_image = image.copy()
        self._height, self._width = image.shape[:2]
    
    # COMPUTED PROPERTY (calculates value on-the-fly)
    @property
    def dimensions(self) -> Tuple[int, int]:
        """Get current image dimensions as a tuple."""
        return (self._width, self._height)
```

### Usage:
```python
image = Image("photo.jpg")

# Use like an attribute (no parentheses!)
path = image.filepath              # Calls the getter
current = image.current_image      # Calls the getter
dims = image.dimensions            # Calls computed property

# Setting also looks like an attribute
image.current_image = new_image    # Calls the setter
```

### Types of Properties:
1. **Getter only** (`@property`): Read-only attribute
   ```python
   @property
   def filepath(self):
       return self._filepath
   # Can read but not write: image.filepath (✓)  image.filepath = x (✗)
   ```

2. **Getter + Setter**: Read and write with validation
   ```python
   @property
   def current_image(self):
       return self._current_image
   
   @current_image.setter
   def current_image(self, value):
       self._current_image = value
   ```

3. **Computed property**: Calculates value each time
   ```python
   @property
   def dimensions(self):
       return (self._width, self._height)
   ```

### Why it matters:
- Looks like simple attribute access but with method control
- Can add validation when setting values
- Can compute values on-the-fly
- Maintains encapsulation while providing clean interface

---

## 8. Inheritance

### What is it?
A class can inherit attributes and methods from another class (parent/base class).

### Where it's used:
```python
# From processors/image_processor.py

# PARENT CLASS (Base class)
class ImageProcessor(ABC):
    """Abstract base class for image processing operations."""
    
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def apply(self, image, **kwargs):
        pass

# CHILD CLASS (inherits from ImageProcessor)
class FilterProcessor(ImageProcessor):
    """
    Inherits all methods and attributes from ImageProcessor.
    """
    
    def __init__(self, name: str, description: str):
        super().__init__(name)  # Call parent constructor
        self._description = description
    
    @property
    def description(self) -> str:
        return self._description

# GRANDCHILD CLASS (inherits from FilterProcessor)
class GrayscaleFilter(FilterProcessor):
    """
    Inherits from FilterProcessor, which inherits from ImageProcessor.
    Has access to methods from both parent classes.
    """
    
    def __init__(self):
        super().__init__("Grayscale", "Converts image to black and white")
    
    def apply(self, image, **kwargs):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
```

### Inheritance Hierarchy:
```
ImageProcessor (base)
    ↓
FilterProcessor (inherits from ImageProcessor)
    ↓
GrayscaleFilter, BlurFilter, EdgeDetectionFilter, etc.
(all inherit from FilterProcessor)
```

### What is inherited:
```python
gray_filter = GrayscaleFilter()

# Can use methods from ImageProcessor (grandparent)
gray_filter.validate_image(img)  # From ImageProcessor

# Can use properties from ImageProcessor (grandparent)
print(gray_filter.name)  # From ImageProcessor

# Can use methods from FilterProcessor (parent)
print(gray_filter.description)  # From FilterProcessor

# Has its own implementation
result = gray_filter.apply(image)  # Own implementation
```

### Why it matters:
- Promotes code reuse
- Creates logical hierarchies
- Child classes extend parent functionality
- Avoids code duplication

---

## 9. Multiple Inheritance

### What is it?
A class can inherit from MORE THAN ONE parent class.

### Where it's used:
```python
# From managers/filter_manager.py

# FIRST PARENT CLASS
class FilterRegistry:
    """Manages filter registration."""
    
    def __init__(self):
        self._registry = {}
    
    def register_filter(self, key: str, filter_obj):
        self._registry[key] = filter_obj
    
    def get_filter(self, key: str):
        return self._registry.get(key)

# SECOND PARENT CLASS
class HistoryTracker:
    """Tracks operation history."""
    
    def __init__(self):
        self._history = []
    
    def add_to_history(self, operation: str):
        self._history.append(operation)
    
    def get_history(self):
        return self._history.copy()

# CHILD CLASS (inherits from BOTH parents)
class FilterManager(FilterRegistry, HistoryTracker):
    """
    Demonstrates Multiple Inheritance.
    Inherits from both FilterRegistry AND HistoryTracker.
    """
    
    def __init__(self):
        # Initialize BOTH parent classes
        FilterRegistry.__init__(self)
        HistoryTracker.__init__(self)
        
        self._current_image = None
        self._undo_stack = []
```

### What FilterManager inherits:
```python
manager = FilterManager()

# Methods from FilterRegistry (first parent)
manager.register_filter("grayscale", GrayscaleFilter())
filter_obj = manager.get_filter("grayscale")

# Methods from HistoryTracker (second parent)
manager.add_to_history("Applied grayscale")
history = manager.get_history()

# Own methods
manager.apply_filter("grayscale")
```

### Multiple Inheritance Diagram:
```
FilterRegistry          HistoryTracker
(filter management)     (history tracking)
        ↓                      ↓
        └──────────┬───────────┘
                   ↓
            FilterManager
    (has both functionalities)
```

### Why it matters:
- Combines functionality from multiple sources
- Reduces code duplication
- Creates more flexible class designs
- **Note**: Use carefully - can become complex with many parents

---

## 10. Polymorphism

### What is it?
Different classes can have methods with the same name, but different implementations. The correct version is called based on the object type.

### Where it's used:
```python
# From processors/image_processor.py

# PARENT defines the interface
class FilterProcessor:
    def apply(self, image, **kwargs):
        """Base implementation - will be overridden."""
        return image

# EACH CHILD implements apply() DIFFERENTLY
class GrayscaleFilter(FilterProcessor):
    def apply(self, image, **kwargs):
        """Implements grayscale conversion."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

class BlurFilter(FilterProcessor):
    def apply(self, image, intensity=5, **kwargs):
        """Implements Gaussian blur."""
        kernel_size = max(1, intensity if intensity % 2 == 1 else intensity + 1)
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

class EdgeDetectionFilter(FilterProcessor):
    def apply(self, image, threshold1=100, threshold2=200, **kwargs):
        """Implements Canny edge detection."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
```

### Polymorphism in Action:
```python
# Create different filter objects
filters = [
    GrayscaleFilter(),
    BlurFilter(),
    EdgeDetectionFilter()
]

# Same method name, different implementations!
for filter_obj in filters:
    result = filter_obj.apply(image)  # Calls the correct version
    # GrayscaleFilter.apply() for first iteration
    # BlurFilter.apply() for second iteration
    # EdgeDetectionFilter.apply() for third iteration
```

### Real-world example from our code:
```python
# From managers/filter_manager.py
def apply_filter(self, filter_key: str, **kwargs) -> bool:
    filter_obj = self.get_filter(filter_key)
    
    # Polymorphism: Same method call, different behavior
    processed_img = filter_obj.apply(current_img, **kwargs)
    # The apply() method that gets called depends on filter_obj's actual type
```

### Why it matters:
- Write code that works with many types
- Same interface, different implementations
- Makes code flexible and extensible
- Can add new filter types without changing existing code

---

## 11. Method Overriding

### What is it?
A child class provides a NEW implementation of a method from its parent class.

### Where it's used:
```python
# From processors/image_processor.py

# PARENT CLASS method
class FilterProcessor(ImageProcessor):
    def apply(self, image, **kwargs):
        """
        Base implementation of apply method.
        This will be OVERRIDDEN by child classes.
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image provided")
        return image  # Simple default behavior

# CHILD CLASS overrides the method
class GrayscaleFilter(FilterProcessor):
    def apply(self, image, **kwargs):
        """
        OVERRIDES parent's apply() method.
        Provides specific grayscale implementation.
        """
        if not self.validate_image(image):
            raise ValueError("Invalid image for grayscale conversion")
        
        # Different implementation than parent
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
```

### Complete override example:
```python
# PARENT: FilterProcessor.apply()
def apply(self, image, **kwargs):
    return image  # Simple return

# CHILD 1: GrayscaleFilter.apply() - OVERRIDES
def apply(self, image, **kwargs):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# CHILD 2: BlurFilter.apply() - OVERRIDES differently
def apply(self, image, intensity=5, **kwargs):
    kernel_size = max(1, intensity if intensity % 2 == 1 else intensity + 1)
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

# CHILD 3: RotationFilter.apply() - OVERRIDES differently
def apply(self, image, angle=90, **kwargs):
    rotation_map = {90: cv2.ROTATE_90_CLOCKWISE, ...}
    return cv2.rotate(image, rotation_map[angle])
```

### Method Overriding vs. Polymorphism:
- **Method Overriding**: The mechanism (child replaces parent's method)
- **Polymorphism**: The result (different objects, same method name, different behavior)

### Why it matters:
- Customize parent behavior for specific needs
- Keep same interface but change implementation
- Essential for polymorphism to work

---

## 12. Magic Methods (Operator Overloading)

### What is it?
Special methods with double underscores (`__method__`) that Python calls automatically. They allow custom behavior for operators and built-in functions.

### Where it's used in our project:

#### 1. `__str__()` - User-Friendly String
```python
# From models/image.py
class Image:
    def __str__(self) -> str:
        """
        Called by str() or print().
        Returns user-friendly description.
        """
        return (f"Image: {self._filepath}\n"
                f"Dimensions: {self._width}x{self._height} pixels")

# Usage:
image = Image("photo.jpg")
print(image)  # Automatically calls __str__()
# Output: Image: photo.jpg
#         Dimensions: 1920x1080 pixels
```

#### 2. `__repr__()` - Developer-Friendly String
```python
# From models/image.py
class Image:
    def __repr__(self) -> str:
        """
        Called by repr() or in interactive shell.
        Returns technical representation.
        """
        return f"Image(filepath='{self._filepath}', dimensions=({self._width}, {self._height}))"

# Usage:
image = Image("photo.jpg")
repr(image)  # Calls __repr__()
# Output: Image(filepath='photo.jpg', dimensions=(1920, 1080))
```

#### 3. `__eq__()` - Equality Comparison
```python
# From models/image.py
class Image:
    def __eq__(self, other) -> bool:
        """
        Called when using == operator.
        Compares two Image objects.
        """
        if not isinstance(other, Image):
            return False
        return np.array_equal(self._current_image, other._current_image)

# Usage:
image1 = Image("photo1.jpg")
image2 = Image("photo2.jpg")
if image1 == image2:  # Calls __eq__()
    print("Images are identical")
```

#### 4. `__len__()` - Length Support
```python
# From managers/filter_manager.py
class FilterManager:
    def __len__(self) -> int:
        """
        Called by len() function.
        Returns number of registered filters.
        """
        return len(self._registry)

# Usage:
manager = FilterManager()
num_filters = len(manager)  # Calls __len__()
print(f"Total filters: {num_filters}")  # Total filters: 8
```

#### 5. `__contains__()` - Membership Testing
```python
# From managers/filter_manager.py
class FilterManager:
    def __contains__(self, filter_key: str) -> bool:
        """
        Called when using 'in' operator.
        Checks if filter exists.
        """
        return filter_key in self._registry

# Usage:
manager = FilterManager()
if "grayscale" in manager:  # Calls __contains__()
    print("Grayscale filter available")
```

### Common Magic Methods:

| Method | Operator/Function | Purpose |
|--------|------------------|---------|
| `__str__()` | `str()`, `print()` | User-friendly string |
| `__repr__()` | `repr()`, interactive shell | Developer string |
| `__eq__()` | `==` | Equality comparison |
| `__len__()` | `len()` | Get length/size |
| `__contains__()` | `in` | Membership test |
| `__add__()` | `+` | Addition operator |
| `__getitem__()` | `[]` | Index access |

### Why it matters:
- Makes classes behave like built-in types
- Natural, intuitive syntax
- Operator overloading for custom classes
- Integrates with Python's built-in functions

---

## 13. Super() Function

### What is it?
`super()` calls a method from the parent class. Essential for proper initialization in inheritance.

### Where it's used:

#### Basic Inheritance:
```python
# From processors/image_processor.py

# PARENT CLASS
class ImageProcessor:
    def __init__(self, name: str):
        self._name = name

# CHILD CLASS
class FilterProcessor(ImageProcessor):
    def __init__(self, name: str, description: str):
        # Call parent's __init__ using super()
        super().__init__(name)
        # Now add child-specific initialization
        self._description = description
```

#### Multiple Inheritance:
```python
# From processors/image_processor.py

# GRANDPARENT
class ImageProcessor:
    def __init__(self, name: str):
        self._name = name

# PARENT
class FilterProcessor(ImageProcessor):
    def __init__(self, name: str, description: str):
        super().__init__(name)  # Calls ImageProcessor.__init__
        self._description = description

# GRANDCHILD
class GrayscaleFilter(FilterProcessor):
    def __init__(self):
        # Calls FilterProcessor.__init__, which calls ImageProcessor.__init__
        super().__init__("Grayscale", "Converts image to black and white")
```

### What super() does:
```python
class GrayscaleFilter(FilterProcessor):
    def __init__(self):
        # WITHOUT super() - wrong!
        # Parent initialization is skipped
        pass
        
        # WITH super() - correct!
        super().__init__("Grayscale", "Converts image to black and white")
        # This ensures:
        # 1. FilterProcessor.__init__ is called
        # 2. Which calls ImageProcessor.__init__
        # 3. All parent attributes are properly initialized
```

### Multiple Inheritance with super():
```python
# From managers/filter_manager.py
class FilterManager(FilterRegistry, HistoryTracker):
    def __init__(self):
        # Must initialize both parents
        FilterRegistry.__init__(self)
        HistoryTracker.__init__(self)
        
        # Now initialize own attributes
        self._current_image = None
```

### Why it matters:
- Ensures parent classes are properly initialized
- Maintains the initialization chain
- Works correctly with multiple inheritance
- More maintainable than calling parent directly

---

## 14. Abstract Methods

### What is it?
Methods declared in a parent class that MUST be implemented by child classes. Uses `@abstractmethod` decorator from `abc` module.

### Where it's used:
```python
# From processors/image_processor.py
from abc import ABC, abstractmethod

# ABSTRACT BASE CLASS
class ImageProcessor(ABC):
    """
    Abstract base class - cannot be instantiated directly.
    """
    
    @abstractmethod
    def apply(self, image, **kwargs):
        """
        Abstract method - MUST be overridden by child classes.
        This is just a declaration, not an implementation.
        """
        pass  # No implementation here

# This will cause an ERROR:
# processor = ImageProcessor("test")  # TypeError: Can't instantiate abstract class
```

### Child Classes MUST Implement Abstract Methods:
```python
# CORRECT - Implements apply()
class GrayscaleFilter(ImageProcessor):
    def apply(self, image, **kwargs):
        """Concrete implementation of abstract method."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# Can now create objects:
gray_filter = GrayscaleFilter()  # Works!

# INCORRECT - Doesn't implement apply()
class BrokenFilter(ImageProcessor):
    pass  # No apply() method

# This will ERROR:
# broken = BrokenFilter()  # TypeError: Can't instantiate abstract class
```

### Complete Example:
```python
from abc import ABC, abstractmethod

# ABSTRACT BASE CLASS
class ImageProcessor(ABC):
    """Cannot create ImageProcessor objects directly."""
    
    def __init__(self, name: str):
        self._name = name
    
    @abstractmethod
    def apply(self, image, **kwargs):
        """All children MUST implement this."""
        pass
    
    @staticmethod
    def validate_image(image):
        """Regular method - can have implementation."""
        return image is not None

# CONCRETE CHILD CLASS
class FilterProcessor(ImageProcessor):
    """Still abstract - doesn't implement apply()."""
    
    def __init__(self, name: str, description: str):
        super().__init__(name)
        self._description = description
    
    # Still no apply() - remains abstract

# CONCRETE GRANDCHILD
class GrayscaleFilter(FilterProcessor):
    """Concrete class - implements apply()."""
    
    def apply(self, image, **kwargs):
        """Finally implements the abstract method."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
```

### Why it matters:
- Enforces a contract - all children must implement certain methods
- Prevents creating incomplete objects
- Documents required interface clearly
- Catches errors at object creation time, not at method call time

---

## Summary Table

| Concept | File Location | Key Example |
|---------|---------------|-------------|
| **Classes & Objects** | All files | `Image`, `FilterManager`, `ImageEditorApp` |
| **Constructors** | All classes | `__init__` methods |
| **Instance Attributes** | models/image.py | `self._filepath`, `self._current_image` |
| **Class Attributes** | models/image.py | `Image.SUPPORTED_FORMATS` |
| **Static Methods** | processors/image_processor.py | `@staticmethod validate_image()` |
| **Class Methods** | managers/filter_manager.py | `@classmethod get_filter_statistics()` |
| **Encapsulation** | models/image.py | Private attributes with `_` |
| **Property Decorators** | models/image.py | `@property filepath`, `@property.setter` |
| **Inheritance** | processors/image_processor.py | `FilterProcessor` extends `ImageProcessor` |
| **Multiple Inheritance** | managers/filter_manager.py | `FilterManager` extends two classes |
| **Polymorphism** | All filter classes | Different `apply()` implementations |
| **Method Overriding** | All filter classes | Override parent's `apply()` |
| **Magic Methods** | models/image.py | `__str__`, `__repr__`, `__eq__`, `__len__` |
| **Super()** | All child classes | `super().__init__()` |
| **Abstract Methods** | processors/image_processor.py | `@abstractmethod apply()` |

---

## Questions for Understanding

### Test Your Knowledge:

1. **What's the difference between `@staticmethod` and `@classmethod`?**
   - Static: No access to instance or class
   - Class: Has access to class (cls) but not instance

2. **Why use properties instead of direct attribute access?**
   - Provides validation
   - Maintains encapsulation
   - Can compute values on-the-fly
   - Allows changing implementation later

3. **What's the purpose of `super()`?**
   - Calls parent class methods
   - Essential for proper initialization
   - Maintains inheritance chain

4. **How is method overriding different from polymorphism?**
   - Overriding: Mechanism (replacing parent's method)
   - Polymorphism: Result (different behavior based on type)

5. **Why use abstract methods?**
   - Enforce contract on child classes
   - Prevent incomplete implementations
   - Document required interface

---

This comprehensive guide covers all OOP concepts used in the Image Editor project with detailed explanations and real code examples!
