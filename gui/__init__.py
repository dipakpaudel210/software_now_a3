"""
GUI package for HIT137 Assignment 3.

This package contains the Tkinter-based graphical user interface.
Demonstrates object-oriented design with proper separation of concerns.

Main Components:
    - AIModelGUI: Main application class with Tkinter widgets
    - Implements multiple inheritance, encapsulation, and polymorphism
"""

# Import main GUI class when ready
try:
    from gui.app import AIModelGUI
except ImportError:
    AIModelGUI = None

# Define public exports
__all__ = [
    'AIModelGUI',
]

# Package metadata
__version__ = '1.0.0'
__description__ = 'Tkinter GUI for Hugging Face AI Model Integration'