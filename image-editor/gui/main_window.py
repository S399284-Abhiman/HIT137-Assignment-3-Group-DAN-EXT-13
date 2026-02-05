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
        self._original_for_sliders: Optional[np.ndarray] = None  # Store original for slider adjustments
        
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
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Modern color scheme
        self.root.configure(bg='#f5f5f5')
        
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
        Create modern flat toolbar with quick access buttons.
        
        Demonstrates Frame widget and button creation.
        """
        toolbar = tk.Frame(self.root, bg='#2c3e50', height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)
        
        # Create modern flat toolbar buttons
        buttons = [
            ("📂 Open", self._open_image, '#3498db'),
            ("💾 Save", self._save_image, '#2ecc71'),
            ("↶ Undo", self._undo, '#95a5a6'),
            ("↷ Redo", self._redo, '#95a5a6'),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(toolbar, text=text, command=command,
                          bg=color, fg='white', 
                          font=('Segoe UI', 10),
                          relief=tk.FLAT,
                          padx=20, pady=10,
                          cursor='hand2',
                          activebackground=self._darken_color(color),
                          activeforeground='white',
                          borderwidth=0)
            btn.pack(side=tk.LEFT, padx=2, pady=5)
            
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self._darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
    
    def _darken_color(self, hex_color: str) -> str:
        """
        Darken a hex color for hover effect.
        
        Args:
            hex_color (str): Hex color code
            
        Returns:
            str: Darkened hex color
        """
        # Simple darkening by reducing RGB values
        rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
        darkened = [max(0, int(c * 0.8)) for c in rgb]
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def _create_main_area(self) -> None:
        """
        Create the main image display area with modern styling.
        
        Demonstrates Canvas widget for image display.
        """
        # Create frame for canvas with scrollbars
        self.canvas_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create canvas with modern styling
        self.canvas = tk.Canvas(self.canvas_frame, 
                               bg='#ecf0f1',
                               highlightthickness=0,
                               borderwidth=0)
        
        # Minimal scrollbars
        v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL,
                                  command=self.canvas.yview,
                                  width=10)
        h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL,
                                  command=self.canvas.xview,
                                  width=10)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _create_control_panel(self) -> None:
        """
        Create modern minimalistic control panel with flat design.
        
        Demonstrates various Tkinter widgets with modern styling.
        """
        # Modern control panel with no gap
        control_panel_container = tk.Frame(self.root, width=280, bg='#ffffff',
                                          relief=tk.FLAT, borderwidth=0)
        control_panel_container.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)
        control_panel_container.pack_propagate(False)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(control_panel_container, width=280, 
                          bg='#ffffff', highlightthickness=0, borderwidth=0)
        
        # Minimal scrollbar
        scrollbar = tk.Scrollbar(control_panel_container, orient=tk.VERTICAL,
                                command=canvas.yview, width=8, 
                                bg='#ffffff', troughcolor='#f5f5f5')
        
        # Create frame inside canvas
        control_panel = tk.Frame(canvas, bg='#ffffff')
        
        # Configure canvas
        canvas.create_window((0, 0), window=control_panel, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Update scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        control_panel.bind("<Configure>", configure_scroll_region)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Modern header
        header = tk.Frame(control_panel, bg='#34495e', height=60)
        header.pack(fill=tk.X, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="FILTERS", 
                        font=('Segoe UI', 14, 'bold'),
                        bg='#34495e', fg='white')
        title.pack(pady=20)
        
        # Separator line
        tk.Frame(control_panel, height=1, bg='#ecf0f1').pack(fill=tk.X)
        
        # Basic Filters Section
        self._create_section_header(control_panel, "BASIC FILTERS")
        
        basic_frame = tk.Frame(control_panel, bg='#ffffff')
        basic_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self._create_modern_button(basic_frame, "Grayscale", 
                                   lambda: self._apply_filter_permanent("grayscale"),
                                   '#7f8c8d')
        self._create_modern_button(basic_frame, "Edge Detection", 
                                   lambda: self._apply_filter_permanent("edge"),
                                   '#7f8c8d')
        
        # Blur Section
        self._create_section_header(control_panel, "BLUR")
        
        blur_frame = tk.Frame(control_panel, bg='#ffffff')
        blur_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.blur_value_label = tk.Label(blur_frame, text="1", 
                                         font=('Segoe UI', 11),
                                         bg='#ffffff', fg='#34495e')
        self.blur_value_label.pack(pady=(0, 5))
        
        self.blur_slider = tk.Scale(blur_frame, from_=1, to=25,
                                   orient=tk.HORIZONTAL, length=250,
                                   command=self._on_blur_change,
                                   showvalue=0,
                                   bg='#ffffff', 
                                   troughcolor='#ecf0f1',
                                   highlightthickness=0,
                                   sliderrelief=tk.FLAT,
                                   activebackground='#3498db',
                                   borderwidth=0)
        self.blur_slider.set(1)
        self.blur_slider.pack(pady=5)
        
        self._create_reset_button(blur_frame, self.blur_slider, 1)
        
        # Brightness Section
        self._create_section_header(control_panel, "BRIGHTNESS")
        
        brightness_frame = tk.Frame(control_panel, bg='#ffffff')
        brightness_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.brightness_value_label = tk.Label(brightness_frame, text="0",
                                               font=('Segoe UI', 11),
                                               bg='#ffffff', fg='#34495e')
        self.brightness_value_label.pack(pady=(0, 5))
        
        self.brightness_slider = tk.Scale(brightness_frame, from_=-100, to=100,
                                         orient=tk.HORIZONTAL, length=250,
                                         command=self._on_brightness_change,
                                         showvalue=0,
                                         bg='#ffffff',
                                         troughcolor='#ecf0f1',
                                         highlightthickness=0,
                                         sliderrelief=tk.FLAT,
                                         activebackground='#f39c12',
                                         borderwidth=0)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(pady=5)
        
        self._create_reset_button(brightness_frame, self.brightness_slider, 0)
        
        # Contrast Section
        self._create_section_header(control_panel, "CONTRAST")
        
        contrast_frame = tk.Frame(control_panel, bg='#ffffff')
        contrast_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.contrast_value_label = tk.Label(contrast_frame, text="1.0",
                                             font=('Segoe UI', 11),
                                             bg='#ffffff', fg='#34495e')
        self.contrast_value_label.pack(pady=(0, 5))
        
        self.contrast_slider = tk.Scale(contrast_frame, from_=0.5, to=3.0,
                                       resolution=0.1, orient=tk.HORIZONTAL,
                                       length=250,
                                       command=self._on_contrast_change,
                                       showvalue=0,
                                       bg='#ffffff',
                                       troughcolor='#ecf0f1',
                                       highlightthickness=0,
                                       sliderrelief=tk.FLAT,
                                       activebackground='#9b59b6',
                                       borderwidth=0)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(pady=5)
        
        self._create_reset_button(contrast_frame, self.contrast_slider, 1.0)
        
        # Transform Section
        self._create_section_header(control_panel, "TRANSFORM")
        
        transform_frame = tk.Frame(control_panel, bg='#ffffff')
        transform_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self._create_modern_button(transform_frame, "↻ Rotate 90°",
                                   lambda: self._apply_filter_permanent("rotate", angle=90),
                                   '#16a085')
        self._create_modern_button(transform_frame, "⟲ Rotate 180°",
                                   lambda: self._apply_filter_permanent("rotate", angle=180),
                                   '#16a085')
        self._create_modern_button(transform_frame, "↺ Rotate 270°",
                                   lambda: self._apply_filter_permanent("rotate", angle=270),
                                   '#16a085')
        self._create_modern_button(transform_frame, "↔ Flip Horizontal",
                                   lambda: self._apply_filter_permanent("flip", direction="horizontal"),
                                   '#16a085')
        self._create_modern_button(transform_frame, "↕ Flip Vertical",
                                   lambda: self._apply_filter_permanent("flip", direction="vertical"),
                                   '#16a085')
        
        # Resize Section
        self._create_section_header(control_panel, "RESIZE")
        
        resize_frame = tk.Frame(control_panel, bg='#ffffff')
        resize_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.resize_value_label = tk.Label(resize_frame, text="100%",
                                           font=('Segoe UI', 11),
                                           bg='#ffffff', fg='#34495e')
        self.resize_value_label.pack(pady=(0, 5))
        
        self.resize_slider = tk.Scale(resize_frame, from_=25, to=200,
                                     orient=tk.HORIZONTAL, length=250,
                                     command=self._on_resize_change,
                                     showvalue=0,
                                     bg='#ffffff',
                                     troughcolor='#ecf0f1',
                                     highlightthickness=0,
                                     sliderrelief=tk.FLAT,
                                     activebackground='#e74c3c',
                                     borderwidth=0)
        self.resize_slider.set(100)
        self.resize_slider.pack(pady=5)
        
        self._create_reset_button(resize_frame, self.resize_slider, 100)
        
        # Apply All Button
        apply_frame = tk.Frame(control_panel, bg='#ffffff')
        apply_frame.pack(fill=tk.X, padx=15, pady=20)
        
        apply_btn = tk.Button(apply_frame, text="✓ APPLY ALL",
                             command=self._commit_slider_changes,
                             bg='#27ae60', fg='white',
                             font=('Segoe UI', 11, 'bold'),
                             relief=tk.FLAT,
                             cursor='hand2',
                             activebackground='#229954',
                             activeforeground='white',
                             height=2,
                             borderwidth=0)
        apply_btn.pack(fill=tk.X, pady=5)
        
        # Hover effect for apply button
        apply_btn.bind('<Enter>', lambda e: apply_btn.config(bg='#229954'))
        apply_btn.bind('<Leave>', lambda e: apply_btn.config(bg='#27ae60'))
    
    def _create_section_header(self, parent, text):
        """Create a modern section header."""
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        label = tk.Label(frame, text=text,
                        font=('Segoe UI', 9, 'bold'),
                        bg='#ffffff', fg='#7f8c8d')
        label.pack(anchor=tk.W)
        
        # Separator line
        tk.Frame(frame, height=1, bg='#ecf0f1').pack(fill=tk.X, pady=(5, 0))
    
    def _create_modern_button(self, parent, text, command, color):
        """Create a modern flat button."""
        btn = tk.Button(parent, text=text,
                       command=command,
                       bg=color, fg='white',
                       font=('Segoe UI', 10),
                       relief=tk.FLAT,
                       cursor='hand2',
                       activebackground=self._darken_color(color),
                       activeforeground='white',
                       height=2,
                       borderwidth=0)
        btn.pack(fill=tk.X, pady=3)
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=self._darken_color(color)))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
    
    def _create_reset_button(self, parent, slider, default_value):
        """Create a small reset button."""
        btn = tk.Button(parent, text="Reset",
                       command=lambda: self._reset_slider(slider, default_value),
                       bg='#ecf0f1', fg='#34495e',
                       font=('Segoe UI', 9),
                       relief=tk.FLAT,
                       cursor='hand2',
                       activebackground='#bdc3c7',
                       activeforeground='#2c3e50',
                       borderwidth=0)
        btn.pack(pady=(5, 0))
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg='#bdc3c7'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#ecf0f1'))
    
    def _create_status_bar(self) -> None:
        """
        Create modern status bar at the bottom of the window.
        
        Demonstrates Label widget for status information.
        """
        self.status_bar = tk.Label(self.root, text="Ready | No image loaded", 
                                  bg='#34495e', fg='white',
                                  font=('Segoe UI', 9),
                                  anchor=tk.W, padx=10, height=2)
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
                
                # Store original for slider adjustments
                self._original_for_sliders = self._image.current_image.copy()
                
                # Reset sliders to default
                self.blur_slider.set(1)
                self.brightness_slider.set(0)
                self.contrast_slider.set(1.0)
                self.resize_slider.set(100)
                
                # Display the image first
                self._display_current_image()
                
                # Force window update to get accurate canvas dimensions
                self.root.update_idletasks()
                
                # Small delay to ensure canvas is fully rendered
                self.root.after(100, self._fit_to_window)
                
                # Update status bar
                filename = filepath.split('/')[-1]
                self._update_status(f"Opened: {filename}")
                
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
    
    def _apply_filter_permanent(self, filter_key: str, **kwargs) -> None:
        """
        Apply a filter permanently (for buttons like grayscale, edge detection, transforms).
        
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
            # Update original for sliders with the new permanent change
            self._original_for_sliders = self._image.current_image.copy()
            
            # Reset sliders after permanent change
            self.blur_slider.set(1)
            self.brightness_slider.set(0)
            self.contrast_slider.set(1.0)
            self.resize_slider.set(100)
            
            self._display_current_image()
            filter_info = self._filter_manager.get_filter_info(filter_key)
            if filter_info:
                self._update_status(f"Applied: {filter_info['name']}")
        else:
            messagebox.showerror("Error", "Failed to apply filter")
    
    def _on_blur_change(self, value) -> None:
        """
        Real-time blur adjustment as slider moves.
        
        Args:
            value: Slider value (automatically passed by Tkinter)
        """
        if self._image is None or self._original_for_sliders is None:
            return
        
        intensity = int(float(value))
        # Ensure odd number for kernel size
        if intensity % 2 == 0:
            intensity += 1
        
        # Update label - just the value
        self.blur_value_label.config(text=f"{int(float(value))}")
        
        # Apply filter to original image (not cumulative)
        try:
            # Get the filter
            blur_filter = self._filter_manager.get_filter("blur")
            
            # Apply to original
            filtered = blur_filter.apply(self._original_for_sliders, intensity=intensity)
            
            # Update display only (not permanent)
            self._image.current_image = filtered
            self._display_current_image()
            
        except Exception as e:
            print(f"Error applying blur: {e}")
    
    def _on_brightness_change(self, value) -> None:
        """
        Real-time brightness adjustment as slider moves.
        
        Args:
            value: Slider value (automatically passed by Tkinter)
        """
        if self._image is None or self._original_for_sliders is None:
            return
        
        brightness_value = int(float(value))
        
        # Update label - just the value
        self.brightness_value_label.config(text=f"{brightness_value}")
        
        # Apply filter to original image
        try:
            brightness_filter = self._filter_manager.get_filter("brightness")
            filtered = brightness_filter.apply(self._original_for_sliders, value=brightness_value)
            
            # Update display only
            self._image.current_image = filtered
            self._display_current_image()
            
        except Exception as e:
            print(f"Error applying brightness: {e}")
    
    def _on_contrast_change(self, value) -> None:
        """
        Real-time contrast adjustment as slider moves.
        
        Args:
            value: Slider value (automatically passed by Tkinter)
        """
        if self._image is None or self._original_for_sliders is None:
            return
        
        contrast_value = float(value)
        
        # Update label - just the value
        self.contrast_value_label.config(text=f"{contrast_value:.1f}")
        
        # Apply filter to original image
        try:
            contrast_filter = self._filter_manager.get_filter("contrast")
            filtered = contrast_filter.apply(self._original_for_sliders, value=contrast_value)
            
            # Update display only
            self._image.current_image = filtered
            self._display_current_image()
            
        except Exception as e:
            print(f"Error applying contrast: {e}")
    
    def _on_resize_change(self, value) -> None:
        """
        Real-time resize adjustment as slider moves.
        
        Args:
            value: Slider value (automatically passed by Tkinter)
        """
        if self._image is None or self._original_for_sliders is None:
            return
        
        scale_percent = int(float(value))
        scale = scale_percent / 100.0
        
        # Update label
        self.resize_value_label.config(text=f"Scale: {scale_percent}%")
        
        # Apply filter to original image
        try:
            resize_filter = self._filter_manager.get_filter("resize")
            filtered = resize_filter.apply(self._original_for_sliders, scale=scale)
            
            # Update display only
            self._image.current_image = filtered
            self._display_current_image()
            
        except Exception as e:
            print(f"Error applying resize: {e}")
    
    def _reset_slider(self, slider, default_value) -> None:
        """
        Reset a slider to its default value.
        
        Args:
            slider: The slider widget to reset
            default_value: The default value to set
        """
        if self._image is None:
            return
        
        slider.set(default_value)
        # The slider's command will automatically trigger and reset the image
    
    def _commit_slider_changes(self) -> None:
        """
        Make the current slider adjustments permanent.
        This updates the original so sliders start fresh.
        """
        if self._image is None:
            return
        
        # Update the stored original to current state
        self._original_for_sliders = self._image.current_image.copy()
        
        # Reset sliders to default
        self.blur_slider.set(1)
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.resize_slider.set(100)
        
        self._update_status("Adjustments applied permanently")
        messagebox.showinfo("Success", "All adjustments have been applied!")
    
    def _apply_blur(self) -> None:
        """Apply blur filter with slider value (legacy - kept for compatibility)."""
        intensity = self.blur_slider.get()
        # Ensure odd number for kernel size
        if intensity % 2 == 0:
            intensity += 1
        self._apply_filter_permanent("blur", intensity=intensity)
    
    def _apply_brightness(self) -> None:
        """Apply brightness adjustment with slider value (legacy)."""
        value = self.brightness_slider.get()
        self._apply_filter_permanent("brightness", value=value)
    
    def _apply_contrast(self) -> None:
        """Apply contrast adjustment with slider value (legacy)."""
        value = self.contrast_slider.get()
        self._apply_filter_permanent("contrast", value=value)
    
    def _apply_resize(self) -> None:
        """Apply resize with slider value (legacy)."""
        scale = self.resize_slider.get() / 100.0
        self._apply_filter_permanent("resize", scale=scale)
    
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
        """Reset image to original state and reset all sliders."""
        if self._image is None:
            messagebox.showwarning("Warning", "No image loaded")
            return
        
        self._image.reset_to_original()
        
        # Update original for sliders
        self._original_for_sliders = self._image.current_image.copy()
        
        # Reset all sliders
        self.blur_slider.set(1)
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.resize_slider.set(100)
        
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
