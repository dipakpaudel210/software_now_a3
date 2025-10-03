"""
GUI implementation for the AI Model interface.
"""

import os
import sys
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, scrolledtext
from models.text_model import TextModel
from models.image_model import ImageModel
from PIL import Image, ImageTk
import io

class AIModelGUI:
    """A GUI interface for interacting with AI models."""
    
    def __init__(self, root=None):
        """Initialize the GUI with text and image model capabilities."""
        self.root = root if root else tk.Tk()
        self.root.title("AI Model Interface")
        self.root.geometry("800x600")
        
        # Initialize HF client with mock mode for testing
        from models.hf_client import HFClient
        client = HFClient(mock_mode=True)
        
        # Initialize models with specific model IDs
        self.text_model = TextModel(client, "gpt2")  # Example model ID
        self.image_model = ImageModel(client, "stable-diffusion-v1-5")  # Example model ID
        
        self._setup_gui()
    
    def _setup_gui(self):
        """Set up the GUI components."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Text model tab
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text='Text Model')
        self._setup_text_tab(text_frame)
        
        # Image model tab
        image_frame = ttk.Frame(notebook)
        notebook.add(image_frame, text='Image Model')
        self._setup_image_tab(image_frame)
    
    def _setup_text_tab(self, parent):
        """Set up the text model interface tab."""
        # Input area
        input_frame = ttk.LabelFrame(parent, text="Input Text", padding="5")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(input_frame, height=5)
        self.text_input.pack(fill='x', padx=5, pady=5)
        
        # Process button
        process_btn = ttk.Button(input_frame, text="Process Text", 
                               command=self._process_text)
        process_btn.pack(pady=5)
        
        # Output area
        output_frame = ttk.LabelFrame(parent, text="Model Output", padding="5")
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.text_output = scrolledtext.ScrolledText(output_frame)
        self.text_output.pack(fill='both', expand=True, padx=5, pady=5)
    
    def _setup_image_tab(self, parent):
        """Set up the image model interface tab."""
        # Input area
        input_frame = ttk.LabelFrame(parent, text="Image Input", padding="5")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        # URL input
        ttk.Label(input_frame, text="Image URL:").pack(padx=5, pady=2)
        self.image_url = ttk.Entry(input_frame)
        self.image_url.pack(fill='x', padx=5, pady=2)
        
        # Process button
        process_btn = ttk.Button(input_frame, text="Process Image", 
                               command=self._process_image)
        process_btn.pack(pady=5)
        
        # Output area
        output_frame = ttk.LabelFrame(parent, text="Analysis Results", padding="5")
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.image_output = scrolledtext.ScrolledText(output_frame)
        self.image_output.pack(fill='both', expand=True, padx=5, pady=5)
    
    def _process_text(self):
        """Handle text processing."""
        input_text = self.text_input.get("1.0", tk.END).strip()
        if input_text:
            try:
                result = self.text_model.process_input(input_text)
                self.text_output.delete("1.0", tk.END)
                if result.get("status") == "success":
                    output = result.get("data", {}).get("output", str(result))
                    self.text_output.insert(tk.END, output)
                else:
                    error_msg = result.get("message", "Unknown error occurred")
                    self.text_output.insert(tk.END, f"Error: {error_msg}")
            except Exception as e:
                self.text_output.delete("1.0", tk.END)
                self.text_output.insert(tk.END, f"Error: {str(e)}")
    
    def _process_image(self):
        """Handle image processing."""
        url = self.image_url.get().strip()
        if url:
            try:
                result = self.image_model.process_input(url)
                self.image_output.delete("1.0", tk.END)
                if result.get("status") == "success":
                    output = result.get("data", {}).get("output", str(result))
                    self.image_output.insert(tk.END, output)
                else:
                    error_msg = result.get("message", "Unknown error occurred")
                    self.image_output.insert(tk.END, f"Error: {error_msg}")
            except Exception as e:
                self.image_output.delete("1.0", tk.END)
                self.image_output.insert(tk.END, f"Error: {str(e)}")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = AIModelGUI()
    app.run()
