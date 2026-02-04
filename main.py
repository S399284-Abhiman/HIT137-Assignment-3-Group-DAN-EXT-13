"""
Image Editor Application - Main Entry Point

This module serves as the entry point for the Image Editor application.
It initializes the Tkinter GUI and launches the main application window.

"""

import tkinter as tk
from gui.main_window import ImageEditorApp


def main():
    """
    Main function to initialize and run the Image Editor application.
    
    This function creates the root Tkinter window and instantiates the
    ImageEditorApp class, which handles the entire application logic.
    The mainloop() method keeps the application running and responsive
    to user interactions.
    """
    # Create the root window
    root = tk.Tk()
    
    # Initialize the Image Editor application
    app = ImageEditorApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
