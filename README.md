# HIT137-Assignment-3-Group-DAN-EXT-13
# Image Editor Application

**HIT137 Assignment 3 - Summer Semester 2025**

A professional desktop image editing application demonstrating advanced Object-Oriented Programming concepts, GUI development with Tkinter, and image processing using OpenCV.

---

## 📋 Table of Contents

- [Features](#features)
- [OOP Concepts Demonstrated](#oop-concepts-demonstrated)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Filter Documentation](#filter-documentation)
- [Code Documentation](#code-documentation)
- [Team Members](#team-members)

---

## ✨ Features

### Image Processing Capabilities
- ✅ **Grayscale Conversion** - Convert images to black and white
- ✅ **Blur Effect** - Apply Gaussian blur with adjustable intensity (1-25)
- ✅ **Edge Detection** - Canny edge detection algorithm
- ✅ **Brightness Adjustment** - Increase/decrease brightness (-100 to +100)
- ✅ **Contrast Adjustment** - Modify image contrast (0.5x to 3.0x)
- ✅ **Image Rotation** - Rotate by 90°, 180°, or 270°
- ✅ **Image Flip** - Flip horizontally or vertically
- ✅ **Resize/Scale** - Scale images (25% to 200%)

### GUI Features
- 📂 **File Operations**: Open, Save, Save As with support for JPG, PNG, BMP
- ↩️ **Undo/Redo**: Complete history tracking with unlimited undo/redo
- 🎚️ **Adjustable Controls**: Sliders for blur, brightness, contrast, and resize
- 📊 **Status Bar**: Real-time image information display
- ⌨️ **Keyboard Shortcuts**: Quick access to common operations
- 🖼️ **Zoom Controls**: Zoom in, zoom out, fit to window
- 📋 **Menu System**: Comprehensive menu bar with all features

---

## 🎓 OOP Concepts Demonstrated

This project comprehensively demonstrates all required OOP concepts:

### 1. **Classes and Objects**
- **Image** class: Represents image data and state
- **ImageProcessor** and subclasses: Process images with various filters
- **FilterManager** class: Manages all available filters
- **ImageEditorApp** class: Main GUI application

### 2. **Constructors (`__init__`)**
- Every class has a proper constructor initializing instance attributes
- Example: `Image.__init__(filepath)` initializes image from file path

### 3. **Instance and Class Attributes**
- **Instance attributes**: `self._current_image`, `self._width`, `self._height` (Image class)
- **Class attributes**: `Image.SUPPORTED_FORMATS`, `FilterManager.filter_count`

### 4. **Static Methods (`@staticmethod`)**
- `ImageProcessor.validate_image()` - Validates image without needing instance
- `FilterManager.validate_filter_params()` - Validates filter parameters

### 5. **Class Methods (`@classmethod`)**
- `FilterManager.get_filter_statistics()` - Returns class-level statistics

### 6. **Encapsulation**
- **Private attributes**: `_original_image`, `_current_image`, `_filepath` (underscore prefix)
- **Property decorators**: `@property` for controlled access to private attributes
- **Private methods**: `_load_image()`, `_display_current_image()` for internal operations

### 7. **Property Decorators**
- `@property` for getters: `Image.filepath`, `Image.width`, `Image.height`
- `@property.setter` for setters: `Image.current_image = new_value`
- Demonstrates controlled access to encapsulated data

### 8. **Inheritance**
- `FilterProcessor` inherits from `ImageProcessor` (abstract base class)
- All filter classes inherit from `FilterProcessor`:
  - `GrayscaleFilter`, `BlurFilter`, `EdgeDetectionFilter`, etc.

### 9. **Multiple Inheritance**
- `FilterManager` inherits from both:
  - `FilterRegistry` (manages filter registration)
  - `HistoryTracker` (tracks operation history)
- Demonstrates proper initialization of multiple parent classes

### 10. **Polymorphism**
- All filter classes implement `apply()` method differently
- Same interface, different implementations
- Example: `GrayscaleFilter.apply()` vs `BlurFilter.apply()`

### 11. **Method Overriding**
- Each filter overrides `apply()` method from `FilterProcessor`
- Child classes provide specific implementations

### 12. **Magic Methods (Operator Overloading)**
- `__str__()` - User-friendly string representation
- `__repr__()` - Developer string representation
- `__eq__()` - Equality comparison for Image objects
- `__len__()` - Length of FilterManager (number of filters)
- `__contains__()` - Check if filter exists using `in` operator

### 13. **Super() Function**
- Used in all child classes to call parent constructors
- Example: `super().__init__(name)` in FilterProcessor classes

### 14. **Abstract Methods**
- `ImageProcessor` is abstract base class with `@abstractmethod`
- Forces all subclasses to implement `apply()` method

---

## 📁 Project Structure

```
image-editor/
│
├── main.py                          # Application entry point
│
├── models/                          # Data models
│   ├── __init__.py
│   └── image.py                     # Image class with encapsulation
│
├── processors/                      # Image processing classes
│   ├── __init__.py
│   └── image_processor.py          # Base and filter classes
│
├── managers/                        # Application logic managers
│   ├── __init__.py
│   └── filter_manager.py           # Filter management with multiple inheritance
│
├── gui/                            # GUI components
│   ├── __init__.py
│   └── main_window.py              # Main application window
│
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── github_link.txt                 # GitHub repository link
```

### File Responsibilities

**main.py**
- Application entry point
- Creates Tkinter root window
- Initializes ImageEditorApp

**models/image.py**
- Image class with encapsulation
- Property decorators for controlled access
- Magic methods for operator overloading

**processors/image_processor.py**
- Abstract base class ImageProcessor
- FilterProcessor base class (inheritance)
- 8 filter implementations (polymorphism, method overriding)
- Static methods for utilities

**managers/filter_manager.py**
- Multiple inheritance (FilterRegistry + HistoryTracker)
- Filter registration and management
- Undo/redo functionality
- Class methods and static methods

**gui/main_window.py**
- Complete Tkinter GUI implementation
- Menu bar, toolbar, canvas, control panel, status bar
- Event handling and keyboard shortcuts
- Class interaction with Image and FilterManager

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/S399284-Abhiman/HIT137-Assignment-3-Group-DAN-EXT-13.git
   cd image-editor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 📖 Usage

### Opening an Image
1. Click **File → Open** or press `Ctrl+O`
2. Select an image file (JPG, PNG, or BMP)
3. The image will appear in the main canvas area

### Applying Filters

#### Basic Filters
- Click any filter button in the control panel
- Example: Click **Grayscale** to convert image to black and white

#### Adjustable Filters
1. **Blur**: Adjust intensity slider (1-25), click **Apply Blur**
2. **Brightness**: Adjust slider (-100 to +100), click **Apply Brightness**
3. **Contrast**: Adjust slider (0.5 to 3.0), click **Apply Contrast**
4. **Resize**: Set scale percentage (25% to 200%), click **Apply Resize**

#### Transformations
- **Rotate 90°/180°**: Click respective button
- **Flip Horizontal/Vertical**: Click respective button

### Undo/Redo
- **Undo**: Edit → Undo or `Ctrl+Z`
- **Redo**: Edit → Redo or `Ctrl+Y`
- **Reset to Original**: Edit → Reset to Original

### Saving Images
- **Save**: File → Save or `Ctrl+S` (overwrites original)
- **Save As**: File → Save As or `Ctrl+Shift+S` (new file)

### Zoom Controls
- **Zoom In**: View → Zoom In or `Ctrl++`
- **Zoom Out**: View → Zoom Out or `Ctrl+-`
- **Fit to Window**: View → Fit to Window

### Keyboard Shortcuts
- `Ctrl+O` - Open image
- `Ctrl+S` - Save image
- `Ctrl+Shift+S` - Save as
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+Q` - Exit application
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out

---

## 🎨 Filter Documentation

### Grayscale Conversion
**Class**: `GrayscaleFilter`  
**Method**: `apply(image)`  
**Description**: Converts a color image to grayscale using OpenCV's COLOR_BGR2GRAY conversion.  
**Implementation**: Polymorphic override of base `apply()` method.

### Gaussian Blur
**Class**: `BlurFilter`  
**Method**: `apply(image, intensity=5)`  
**Parameters**: 
- `intensity` (int): Blur kernel size (must be odd, 1-25)  
**Description**: Applies Gaussian blur to reduce noise and detail.

### Edge Detection
**Class**: `EdgeDetectionFilter`  
**Method**: `apply(image, threshold1=100, threshold2=200)`  
**Parameters**:
- `threshold1` (int): First threshold for hysteresis
- `threshold2` (int): Second threshold for hysteresis  
**Description**: Uses Canny algorithm to detect edges in the image.

### Brightness Adjustment
**Class**: `BrightnessAdjustment`  
**Method**: `apply(image, value=0)`  
**Parameters**:
- `value` (int): Brightness adjustment (-100 to +100)  
**Description**: Adds/subtracts a constant value from all pixels.

### Contrast Adjustment
**Class**: `ContrastAdjustment`  
**Method**: `apply(image, value=1.0)`  
**Parameters**:
- `value` (float): Contrast multiplier (0.5 to 3.0)  
**Description**: Multiplies all pixel values by the contrast factor.

### Rotation
**Class**: `RotationFilter`  
**Method**: `apply(image, angle=90)`  
**Parameters**:
- `angle` (int): Rotation angle (90, 180, 270, or custom)  
**Description**: Rotates the image by specified angle.

### Flip
**Class**: `FlipFilter`  
**Method**: `apply(image, direction="horizontal")`  
**Parameters**:
- `direction` (str): "horizontal" or "vertical"  
**Description**: Flips the image along specified axis.

### Resize
**Class**: `ResizeFilter`  
**Method**: `apply(image, width=None, height=None, scale=1.0)`  
**Parameters**:
- `width` (int): Target width
- `height` (int): Target height
- `scale` (float): Scale factor if dimensions not specified  
**Description**: Resizes image using linear interpolation.

---

## 📚 Code Documentation

All code is thoroughly documented with:

### Docstrings
- **Module-level**: Describes the module's purpose and OOP concepts
- **Class-level**: Describes the class, its attributes, and role
- **Method-level**: Describes parameters, return values, and behavior
- **Examples**: 
  ```python
  def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
      """
      Apply the processing operation.
      
      Args:
          image (numpy.ndarray): Input image
          **kwargs: Additional parameters
          
      Returns:
          numpy.ndarray: Processed image
      """
  ```

### Inline Comments
- Explain complex logic
- Highlight OOP concepts in use
- Example:
  ```python
  # Call parent class constructor using super()
  super().__init__(name)
  ```

### Type Hints
- All function parameters and return values are type-hinted
- Improves code readability and IDE support
- Example: `def apply(self, image: np.ndarray, intensity: int = 5) -> np.ndarray:`

---

## 👥 Team Members

[Add your team member names and student IDs here]

## GROUP MEMBERS

| Name | GitHub Username |
|-----|----------------|
| *Abhiman Bhattarai (S399284)* | `S399284-Abhiman` |
| *Antim (S397254)* | `Antim10` |
| *Samuel Jacob Reid (S386533)* | `sjreading` |
| *Zachary Desmond Mullen (S366010)* | `ZMullen2004` |

---


## 🔧 Technical Details

### Dependencies
- **opencv-python**: Image processing operations
- **numpy**: Array operations for images
- **Pillow (PIL)**: Image format conversions for Tkinter display
- **tkinter**: GUI framework (included with Python)

### Image Format Support
- **Input**: JPG, JPEG, PNG, BMP
- **Output**: JPG, PNG, BMP

### Performance Considerations
- Images are copied for undo functionality
- Large images may require more memory
- Zoom operations create temporary scaled versions

---


## 🙏 Acknowledgments

- OpenCV library for powerful image processing capabilities
- Python community for excellent documentation
- Tkinter for cross-platform GUI support

---

**Last Updated**: 4th February 2026  
**Version**: 1.0

