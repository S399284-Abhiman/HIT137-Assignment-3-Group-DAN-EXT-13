"""
Main Window Module

This module defines the main GUI window for the Image Editor application.
It demonstrates Tkinter GUI development, event handling, and class interaction.

OOP Concepts Demonstrated:
- Class Interaction: Works with Image, FilterManager, and processor classes
- Method Overriding: Overrides Tkinter widget behaviors
- Encapsulation: Private methods for internal operations
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image as PILImage, ImageTk
import cv2
import numpy as np
from typing import Optional

from models.image import Image
from managers.filter_manager import FilterManager


class ImageEditorApp:
    """
    Main application window for the Image Editor.
    
    This class creates and manages the entire GUI, demonstrating extensive
    use of Tkinter widgets and event handling. It interacts with Image and
    FilterManager classes to provide complete image editing functionality.
    
    Instance Attributes:
        root (tk.Tk): Main window
        _image (Image): Current image object (encapsulated)
        _filter_manager (FilterManager): Manages all filters
        _display_image (ImageTk.PhotoImage): Image for display
        _zoom_level (float): Current zoom level
    """
    
    def __init__(self, root: tk.Tk):
        """
        Constructor to initialize the application.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        
        # Instance attributes (encapsulation)
        self._image: Optional[Image] = None
        self._filter_manager = FilterManager()
        self._display_image: Optional[ImageTk.PhotoImage] = None
        self._zoom_level = 1.0
        
        # Configure the main window
        self._setup_window()
        
        # Create GUI components
        self._create_menu_bar()
        self._create_toolbar()
        self._create_main_area()
        self._create_control_panel()
        self._create_status_bar()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
    
    def _setup_window(self) -> None:
        """
        Private method to configure the main window.
        
        Demonstrates encapsulation by making this method private.
        """
        self.root.title("Image Editor - HIT137 Assignment 3")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # Icon file not required
    
    def _create_menu_bar(self) -> None:
        """
        Create the menu bar with File and Edit menus.
        
        Demonstrates Tkinter Menu widget creation and command binding.
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self._open_image, 
                            accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_image, 
                            accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self._save_image_as, 
                            accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_application, 
                            accelerator="Ctrl+Q")
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self._undo, 
                            accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self._redo, 
                            accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset to Original", 
                            command=self._reset_to_original)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self._zoom_in, 
                            accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self._zoom_out, 
                            accelerator="Ctrl+-")
        view_menu.add_command(label="Fit to Window", command=self._fit_to_window)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Filter Info", command=self._show_filter_info)
    
    def _create_toolbar(self) -> None:
        """
        Create toolbar with quick access buttons.
        
        Demonstrates Frame widget and button creation.
        """
        toolbar = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Create toolbar buttons
        buttons = [
            ("Open", self._open_image),
            ("Save", self._save_image),
            ("Undo", self._undo),
            ("Redo", self._redo),
        ]
        
        for text, command in buttons:
            btn = tk.Button(toolbar, text=text, command=command, 
                          padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def _create_main_area(self) -> None:
        """
        Create the main image display area.
        
        Demonstrates Canvas widget for image display.
        """
        # Create frame for canvas with scrollbars
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray")
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL,
                                  command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL,
                                  command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _create_control_panel(self) -> None:
        """
        Create the right-side control panel with filter buttons and sliders.
        
        Demonstrates various Tkinter widgets: Frame, LabelFrame, Button, Scale.
        """
        # Main control panel frame
        control_panel = tk.Frame(self.root, width=250, relief=tk.RAISED, 
                               borderwidth=2)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        # Title label
        title = tk.Label(control_panel, text="Image Filters", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Basic Filters Section
        basic_frame = tk.LabelFrame(control_panel, text="Basic Filters", 
                                   padx=10, pady=10)
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(basic_frame, text="Grayscale", 
                 command=lambda: self._apply_filter("grayscale"),
                 width=20).pack(pady=2)
        tk.Button(basic_frame, text="Edge Detection", 
                 command=lambda: self._apply_filter("edge"),
                 width=20).pack(pady=2)
        
        # Blur Section with Slider
        blur_frame = tk.LabelFrame(control_panel, text="Blur Effect", 
                                  padx=10, pady=10)
        blur_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(blur_frame, text="Intensity:").pack()
        self.blur_slider = tk.Scale(blur_frame, from_=1, to=25, 
                                   orient=tk.HORIZONTAL, length=200)
        self.blur_slider.set(5)
        self.blur_slider.pack()
        tk.Button(blur_frame, text="Apply Blur", 
                 command=self._apply_blur, width=20).pack(pady=5)
        
        # Brightness Section with Slider
        brightness_frame = tk.LabelFrame(control_panel, text="Brightness", 
                                        padx=10, pady=10)
        brightness_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(brightness_frame, text="Adjustment:").pack()
        self.brightness_slider = tk.Scale(brightness_frame, from_=-100, to=100, 
                                         orient=tk.HORIZONTAL, length=200)
        self.brightness_slider.set(0)
        self.brightness_slider.pack()
        tk.Button(brightness_frame, text="Apply Brightness", 
                 command=self._apply_brightness, width=20).pack(pady=5)
        
        # Contrast Section with Slider
        contrast_frame = tk.LabelFrame(control_panel, text="Contrast", 
                                      padx=10, pady=10)
        contrast_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(contrast_frame, text="Adjustment:").pack()
        self.contrast_slider = tk.Scale(contrast_frame, from_=0.5, to=3.0, 
                                       resolution=0.1, orient=tk.HORIZONTAL, 
                                       length=200)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack()
        tk.Button(contrast_frame, text="Apply Contrast", 
                 command=self._apply_contrast, width=20).pack(pady=5)
        
        # Transform Section
        transform_frame = tk.LabelFrame(control_panel, text="Transformations", 
                                       padx=10, pady=10)
        transform_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(transform_frame, text="Rotate 90°", 
                 command=lambda: self._apply_filter("rotate", angle=90),
                 width=20).pack(pady=2)
        tk.Button(transform_frame, text="Rotate 180°", 
                 command=lambda: self._apply_filter("rotate", angle=180),
                 width=20).pack(pady=2)
        tk.Button(transform_frame, text="Flip Horizontal", 
                 command=lambda: self._apply_filter("flip", direction="horizontal"),
                 width=20).pack(pady=2)
        tk.Button(transform_frame, text="Flip Vertical", 
                 command=lambda: self._apply_filter("flip", direction="vertical"),
                 width=20).pack(pady=2)
        
        # Resize Section
        resize_frame = tk.LabelFrame(control_panel, text="Resize", 
                                    padx=10, pady=10)
        resize_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(resize_frame, text="Scale (%):").pack()
        self.resize_slider = tk.Scale(resize_frame, from_=25, to=200, 
                                     orient=tk.HORIZONTAL, length=200)
        self.resize_slider.set(100)
        self.resize_slider.pack()
        tk.Button(resize_frame, text="Apply Resize", 
                 command=self._apply_resize, width=20).pack(pady=5)
    
    def _create_status_bar(self) -> None:
        """
        Create status bar at the bottom of the window.
        
        Demonstrates Label widget for status information.
        """
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _bind_shortcuts(self) -> None:
        """
        Bind keyboard shortcuts.
        
        Demonstrates event binding in Tkinter.
        """
        self.root.bind("<Control-o>", lambda e: self._open_image())
        self.root.bind("<Control-s>", lambda e: self._save_image())
        self.root.bind("<Control-Shift-S>", lambda e: self._save_image_as())
        self.root.bind("<Control-z>", lambda e: self._undo())
        self.root.bind("<Control-y>", lambda e: self._redo())
        self.root.bind("<Control-q>", lambda e: self._exit_application())
        self.root.bind("<Control-plus>", lambda e: self._zoom_in())
        self.root.bind("<Control-minus>", lambda e: self._zoom_out())
    
    def _open_image(self) -> None:
        """
        Open an image file using file dialog.
        
        Demonstrates filedialog and error handling.
        """
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        )
        
        filepath = filedialog.askopenfilename(title="Open Image", 
                                             filetypes=filetypes)
        
        if filepath:
            try:
                # Create Image object (class interaction)
                self._image = Image(filepath)
                self._filter_manager.current_image = self._image
                
                # Display the image
                self._display_current_image()
                
                # Update status bar
                self._update_status(f"Opened: {filepath}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def _save_image(self) -> None:
        """
        Save the current image to its original filepath.
        """
        if self._image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        try:
            cv2.imwrite(self._image.filepath, self._image.current_image)
            self._update_status(f"Saved: {self._image.filepath}")
            messagebox.showinfo("Success", "Image saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def _save_image_as(self) -> None:
        """
        Save the current image to a new filepath.
        
        Demonstrates filedialog.asksaveasfilename().
        """
        if self._image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        filetypes = (
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        )
        
        filepath = filedialog.asksaveasfilename(title="Save Image As", 
                                               filetypes=filetypes,
                                               defaultextension=".jpg")
        
        if filepath:
            try:
                cv2.imwrite(filepath, self._image.current_image)
                self._update_status(f"Saved as: {filepath}")
                messagebox.showinfo("Success", "Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def _apply_filter(self, filter_key: str, **kwargs) -> None:
        """
        Apply a filter to the current image.
        
        Demonstrates class interaction with FilterManager.
        
        Args:
            filter_key (str): Key of the filter to apply
            **kwargs: Additional parameters for the filter
        """
        if self._image is None:
            messagebox.showwarning("Warning", "Please open an image first")
            return
        
        # Apply filter using FilterManager (class interaction)
        success = self._filter_manager.apply_filter(filter_key, **kwargs)
        
        if success:
            self._display_current_image()
            filter_info = self._filter_manager.get_filter_info(filter_key)
            if filter_info:
                self._update_status(f"Applied: {filter_info['name']}")
        else:
            messagebox.showerror("Error", "Failed to apply filter")
    
    def _apply_blur(self) -> None:
        """Apply blur filter with slider value."""
        intensity = self.blur_slider.get()
        # Ensure odd number for kernel size
        if intensity % 2 == 0:
            intensity += 1
        self._apply_filter("blur", intensity=intensity)
    
    def _apply_brightness(self) -> None:
        """Apply brightness adjustment with slider value."""
        value = self.brightness_slider.get()
        self._apply_filter("brightness", value=value)
    
    def _apply_contrast(self) -> None:
        """Apply contrast adjustment with slider value."""
        value = self.contrast_slider.get()
        self._apply_filter("contrast", value=value)
    
    def _apply_resize(self) -> None:
        """Apply resize with slider value."""
        scale = self.resize_slider.get() / 100.0
        self._apply_filter("resize", scale=scale)
    
    def _undo(self) -> None:
        """
        Undo the last operation.
        
        Demonstrates method interaction with FilterManager.
        """
        if self._filter_manager.undo():
            self._display_current_image()
            self._update_status("Undo performed")
        else:
            messagebox.showinfo("Info", "Nothing to undo")
    
    def _redo(self) -> None:
        """
        Redo the last undone operation.
        """
        if self._filter_manager.redo():
            self._display_current_image()
            self._update_status("Redo performed")
        else:
            messagebox.showinfo("Info", "Nothing to redo")
    
    def _reset_to_original(self) -> None:
        """Reset image to original state."""
        if self._image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        self._image.reset_to_original()
        self._display_current_image()
        self._update_status("Reset to original image")
    
    def _zoom_in(self) -> None:
        """Zoom in on the image."""
        self._zoom_level *= 1.2
        self._display_current_image()
        self._update_status(f"Zoom: {int(self._zoom_level * 100)}%")
    
    def _zoom_out(self) -> None:
        """Zoom out on the image."""
        self._zoom_level /= 1.2
        self._display_current_image()
        self._update_status(f"Zoom: {int(self._zoom_level * 100)}%")
    
    def _fit_to_window(self) -> None:
        """Fit image to window size."""
        if self._image is None:
            return
        
        # Calculate zoom to fit
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        width_ratio = canvas_width / self._image.width
        height_ratio = canvas_height / self._image.height
        
        self._zoom_level = min(width_ratio, height_ratio) * 0.95
        self._display_current_image()
        self._update_status("Fit to window")
    
    def _display_current_image(self) -> None:
        """
        Display the current image on the canvas.
        
        Demonstrates PIL/Tkinter image handling.
        """
        if self._image is None:
            return
        
        # Get current image from Image object
        img_bgr = self._image.current_image
        
        # Convert BGR to RGB for PIL
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Apply zoom
        if self._zoom_level != 1.0:
            new_width = int(img_rgb.shape[1] * self._zoom_level)
            new_height = int(img_rgb.shape[0] * self._zoom_level)
            img_rgb = cv2.resize(img_rgb, (new_width, new_height))
        
        # Convert to PIL Image
        pil_image = PILImage.fromarray(img_rgb)
        
        # Convert to PhotoImage
        self._display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._display_image)
        
        # Update canvas scroll region
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def _update_status(self, message: str) -> None:
        """
        Update the status bar message.
        
        Args:
            message (str): Status message to display
        """
        if self._image:
            status = f"{message} | Size: {self._image.width}x{self._image.height}"
        else:
            status = message
        
        self.status_bar.config(text=status)
    
    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = """Image Editor Application
        
HIT137 Assignment 3
Version 1.0

Demonstrates OOP concepts:
• Encapsulation
• Inheritance
• Polymorphism
• Multiple Inheritance
• Class/Instance Attributes
• Static/Class Methods
• Property Decorators
• Magic Methods

Developed using:
• Python 3.x
• Tkinter (GUI)
• OpenCV (Image Processing)
• PIL/Pillow (Image Display)
"""
        messagebox.showinfo("About Image Editor", about_text)
    
    def _show_filter_info(self) -> None:
        """Show information about available filters."""
        info = "Available Filters:\n\n"
        
        for key in self._filter_manager.list_filters():
            filter_info = self._filter_manager.get_filter_info(key)
            if filter_info:
                info += f"• {filter_info['name']}: {filter_info['description']}\n"
        
        # Add statistics
        stats = FilterManager.get_filter_statistics()
        info += f"\nTotal Filters: {stats['total_filters']}"
        
        messagebox.showinfo("Filter Information", info)
    
    def _exit_application(self) -> None:
        """
        Exit the application with confirmation.
        
        Demonstrates messagebox.askyesno() for confirmation dialogs.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
