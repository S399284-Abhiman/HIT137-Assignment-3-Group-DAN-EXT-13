# OpenCV GUI Image Processor

An interactive OpenCV-based image processing tool that allows real-time image manipulation using GUI sliders (trackbars). Adjust parameters live and save the processed result to a file.

## Features

- Resize with optional aspect-ratio locking
- Brightness and contrast adjustment
- Rotation and flipping
- Gaussian blur
- Grayscale conversion
- Canny edge detection with adjustable thresholds
- Optional fixed-size preview (center pad/crop)

## Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `r` | Reset all sliders |
| `s` | Save processed image as `output.png` |
| `q` / `Esc` | Quit the application |

You may also close the window using the **X** button.

### Sliders (Trackbars)

| Slider | Description |
|--------|-------------|
| **Lock Aspect Ratio** | Keeps width and height proportional during resize |
| **Free Stretch** | Allows width and height to change independently |
| **Width (px)** | Output image width |
| **Height (px)** | Output image height |
| **Grayscale** | Convert output to grayscale |
| **Blur** | Gaussian blur strength |
| **Edges** | Enable Canny edge detection |
| **Canny Low** | Lower edge threshold |
| **Canny High** | Upper edge threshold |
| **Brightness** | `100` = no change |
| **Contrast** | `100` = no change |
| **Rotate** | `0` = none, `1` = 90° CW, `2` = 180°, `3` = 90° CCW |
| **Flip** | `0` = none, `1` = horizontal, `2` = vertical |
| **Keep Size** | Display output padded/cropped to original size |

## Requirements

- Python 3.8 or higher
- OpenCV
- NumPy

## Installation
Clone the repository:
```bash
https://github.com/S399284-Abhiman/HIT137-Assignment-3-Group-DAN-EXT-13.git




