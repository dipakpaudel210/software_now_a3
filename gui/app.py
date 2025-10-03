"""
GUI implementation for the AI Model interface using Tkinter.

This module demonstrates various OOP concepts:
1. Multiple inheritance: Through model class hierarchies
2. Multiple decorators: In utility functions and model methods
3. Encapsulation: Through proper class structure and private methods
4. Polymorphism: In model implementations
5. Method overriding: In specialized model classes
"""

import os
import sys
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from models.text_model import TextModel
from models.image_model import ImageModel
from models.hf_client import HFClient
from config import Config
from PIL import Image, ImageTk
import io
import json

# Available models configuration
AVAILABLE_MODELS = {
    "Sentiment Analysis": {
        "id": "distilbert-base-uncased-finetuned-sst-2-english",
        "category": "Text Classification",
        "description": "A lightweight BERT model fine-tuned for sentiment analysis. It classifies text as positive or negative sentiment.",
        "input_type": "text",
        "output_type": "text",
        "example": "I love this new feature, it's amazing!",
        "pipeline": "text-classification"
    },
    "Image Recognition": {
        "id": "microsoft/resnet-50",
        "category": "Image Classification",
        "description": "A powerful ResNet model that can classify images into 1000 different categories. Efficient and widely used for image recognition.",
        "input_type": "image",
        "output_type": "text",
        "example": "path/to/image.jpg",
        "pipeline": "image-classification"
    },
    "Text Generation": {
        "id": "gpt2",
        "category": "Text Generation",
        "description": "OpenAI's GPT-2 small model for text generation. It can continue text from a given prompt.",
        "input_type": "text",
        "output_type": "text",
        "example": "Once upon a time in a digital world,",
        "pipeline": "text-generation"
    }
}

class AIModelGUI:
    """A GUI interface for interacting with AI models."""
    
    def __init__(self, root=None):
        """Initialize the GUI with text and image model capabilities."""
        self.root = root if root else tk.Tk()
        self.root.title("Tkinter AI GUI")
        self.root.geometry("1200x800")
        
        # Initialize HF client
        self.client = HFClient(mock_mode=False)  # Set to True for testing without API
        
        # Initialize variables
        self.current_model = tk.StringVar(value="Sentiment Analysis")
        self.input_type = tk.StringVar(value="text")
        self.status_var = tk.StringVar(value="Ready")
        
        # Create main menu
        self._create_menu()
        
        # Setup the GUI components
        self._setup_gui()
    
    def _setup_gui(self):
        """Set up the GUI components."""
        # Create main sections
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        # Model selection section
        model_frame = ttk.LabelFrame(top_frame, text="Model Selection")
        model_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(model_frame, text="Model:").pack(side='left', padx=5)
        model_menu = ttk.OptionMenu(model_frame, self.current_model, "Text-to-Image", 
                                  *AVAILABLE_MODELS.keys(), 
                                  command=self._on_model_change)
        model_menu.pack(side='left', padx=5)
        
        # Main content area
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Input
        input_frame = ttk.LabelFrame(content_frame, text="User Input Section")
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        # Input type selection
        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill='x', padx=5, pady=5)
        ttk.Radiobutton(type_frame, text="Text", variable=self.input_type, 
                       value="text").pack(side='left', padx=5)
        ttk.Radiobutton(type_frame, text="Image", variable=self.input_type, 
                       value="image").pack(side='left', padx=5)
        ttk.Button(type_frame, text="Browse", command=self._browse_input).pack(side='left', padx=5)
        
        # Input guidance
        self.input_guidance = ttk.Label(input_frame, text="Enter text for analysis")
        self.input_guidance.pack(fill='x', padx=5, pady=2)
        
        # Input area
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10)
        self.input_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Example text
        self.example_label = ttk.Label(input_frame, text="Example: ", font=('TkDefaultFont', 9, 'italic'))
        self.example_label.pack(fill='x', padx=5, pady=2)
        
        # Run buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Run Model 1", command=lambda: self._run_model(1)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Run Model 2", command=lambda: self._run_model(2)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self._clear_input).pack(side='left', padx=5)
        
        # Right panel - Output
        output_frame = ttk.LabelFrame(content_frame, text="Model Output Section")
        output_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        self.output_text = scrolledtext.ScrolledText(output_frame)
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bottom panel - Model Info and OOP Explanations
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Model information
        model_info_frame = ttk.LabelFrame(info_frame, text="Model Information & Explanation")
        model_info_frame.pack(fill='x', padx=5, pady=5)
        
        info_content = ttk.Frame(model_info_frame)
        info_content.pack(fill='x', padx=5, pady=5)
        
        # Left column - Model Info
        model_details = ttk.Frame(info_content)
        model_details.pack(side='left', fill='both', expand=True)
        
        ttk.Label(model_details, text="Selected Model Info:").pack(anchor='w')
        self.model_info_text = scrolledtext.ScrolledText(model_details, height=6)
        self.model_info_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Right column - OOP Concepts
        oop_details = ttk.Frame(info_content)
        oop_details.pack(side='left', fill='both', expand=True)
        
        ttk.Label(oop_details, text="OOP Concepts Explanation:").pack(anchor='w')
        self.oop_text = scrolledtext.ScrolledText(oop_details, height=6)
        self.oop_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Status bar
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill='x', side='bottom', padx=10, pady=5)
        ttk.Label(status_bar, textvariable=self.status_var).pack(side='left')
        
        # Update initial model information
        self._update_model_info()
    
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
    
    def _create_menu(self):
        """Create the main menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Input", command=self._browse_input)
        file_menu.add_command(label="Save Output", command=self._save_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Models menu
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        for model_name in AVAILABLE_MODELS:
            models_menu.add_command(label=model_name, 
                                  command=lambda m=model_name: self.current_model.set(m))
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configure API Key", command=self._configure_api_key)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Documentation", command=self._show_docs)
        help_menu.add_command(label="Get API Key", command=self._show_api_help)

    def _update_input_guidance(self):
        """Update the input guidance and example based on selected model."""
        model_info = AVAILABLE_MODELS[self.current_model.get()]
        
        if model_info['input_type'] == 'text':
            self.input_guidance.config(
                text="Enter text for analysis:"
            )
            self.example_label.config(
                text=f"Example: {model_info['example']}"
            )
        else:
            self.input_guidance.config(
                text="Enter image file path or use Browse button:"
            )
            self.example_label.config(
                text="Supported formats: .jpg, .jpeg, .png, .gif, .bmp"
            )

    def _on_model_change(self, *args):
        """Handle model selection changes."""
        self._update_model_info()
        model_info = AVAILABLE_MODELS[self.current_model.get()]
        self.input_type.set(model_info["input_type"])
        self._update_input_guidance()
        self._clear_input()

    def _update_model_info(self):
        """Update the model information display."""
        model_name = self.current_model.get()
        if model_name in AVAILABLE_MODELS:
            info = AVAILABLE_MODELS[model_name]
            self.model_info_text.delete("1.0", tk.END)
            info_text = f"""• Model Name: {model_name}
• Category: {info['category']}
• Description: {info['description']}
• Input Type: {info['input_type']}
• Output Type: {info['output_type']}"""
            self.model_info_text.insert(tk.END, info_text)
        
        # Update OOP concepts explanation
        self.oop_text.delete("1.0", tk.END)
        oop_text = """OOP Concepts in this implementation:

• Multiple Inheritance: Used in model class hierarchy
• Encapsulation: Private methods and data hiding
• Polymorphism: Model interface implementations
• Method Overriding: Specialized model behaviors
• Decorators: Used for logging and caching"""
        self.oop_text.insert(tk.END, oop_text)

    def _browse_input(self):
        """Open file browser for input selection."""
        if self.input_type.get() == "image":
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
            if file_path:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, file_path)
        else:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'r') as file:
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, file.read())

    def _save_output(self):
        """Save the output to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output_text.get("1.0", tk.END))

    def _clear_input(self):
        """Clear the input and output areas."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("Ready")

    def _format_output(self, result: dict, model_num: int) -> str:
        """Format the model output for display."""
        if result.get("status") != "success":
            return f"Error from Model {model_num}: {result.get('message', 'Unknown error occurred')}"
        
        data = result.get("data", {})
        output_lines = [f"Model {model_num} Results:"]
        output_lines.append("-" * 40)
        
        if "top_prediction" in data:
            output_lines.append(f"Top Prediction: {data['top_prediction']}")
            output_lines.append(f"Confidence: {data['confidence']:.2%}")
            output_lines.append("\nDetailed Results:")
            for pred in data.get("predictions", [])[:5]:  # Show top 5 predictions
                output_lines.append(f"• {pred['label']}: {pred['score']:.2%}")
        else:
            output_lines.append(str(data.get("output", "No output available")))
            
        return "\n".join(output_lines)

    def _validate_input(self, input_text: str, expected_type: str) -> bool:
        """Validate the input based on the expected type."""
        if expected_type == "image":
            # For image input, verify it's a valid image file path
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            if not any(input_text.lower().endswith(ext) for ext in valid_extensions):
                messagebox.showwarning(
                    "Invalid Input",
                    "Please provide a valid image file path (jpg, jpeg, png, gif, bmp)"
                )
                return False
            if not os.path.exists(input_text):
                messagebox.showwarning(
                    "Invalid Input",
                    f"Image file not found: {input_text}"
                )
                return False
        return True

    def _run_model(self, model_num):
        """Run the selected model on the input."""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Required", "Please provide input text or image path.")
            return
        
        try:
            # Get model info
            model_name = self.current_model.get()
            model_info = AVAILABLE_MODELS[model_name]
            
            # Validate input type
            if not self._validate_input(input_text, model_info['input_type']):
                return
                
            # Update status
            self.status_var.set("⏳ Processing...")
            self.root.update()  # Force GUI update
            
            # Process input through client
            result = self.client.query(
                model_id=model_info["id"],
                input_data=input_text,
                pipeline=model_info["pipeline"]
            )
            
            # Format and display result
            self.output_text.delete("1.0", tk.END)
            formatted_output = self._format_output(result, model_num)
            self.output_text.insert(tk.END, formatted_output)
            
            # Update status
            self.status_var.set("✅ Processing complete")
                
        except Exception as e:
            error_msg = str(e)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error running model {model_num}: {error_msg}")
            self.status_var.set("❌ Error occurred")
            messagebox.showerror("Error", f"Error running model: {error_msg}")

    def _show_about(self):
        """Show about dialog."""
        about_text = """HIT137 Assignment 3
AI Model Interface

This application demonstrates OOP concepts while
providing an interface to Hugging Face AI models.

Team Members:
- Your team members here"""
        messagebox.showinfo("About", about_text)

    def _show_docs(self):
        """Show documentation."""
        docs_text = """Usage Instructions:

1. Configure your Hugging Face API key in Settings
2. Select a model from the dropdown
3. Choose input type (text/image)
4. Enter input or browse for a file
5. Click Run Model 1 or 2 to process
6. View results in the output section

Model outputs and information are displayed
in their respective sections."""
        messagebox.showinfo("Documentation", docs_text)

    def _configure_api_key(self):
        """Show dialog to configure API key."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configure API Key")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Add widgets
        ttk.Label(dialog, text="Enter your Hugging Face API key:").pack(padx=20, pady=(20,5))
        
        # API key entry
        key_var = tk.StringVar(value=self.client.api_key or "")
        key_entry = ttk.Entry(dialog, textvariable=key_var, width=50)
        key_entry.pack(padx=20, pady=5)
        
        # Help text
        help_text = """You can get your API key from Hugging Face:
1. Go to https://huggingface.co
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token"""
        ttk.Label(dialog, text=help_text, justify='left').pack(padx=20, pady=5)
        
        def save_key():
            api_key = key_var.get().strip()
            if api_key:
                Config.save_api_key(api_key)
                self.client.api_key = api_key
                self.client.headers["Authorization"] = f"Bearer {api_key}"
                messagebox.showinfo("Success", "API key saved successfully!")
                dialog.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter an API key.")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=20, pady=20)
        ttk.Button(btn_frame, text="Save", command=save_key).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=5)

    def _show_api_help(self):
        """Show help for getting an API key."""
        help_text = """How to Get Your Hugging Face API Key:

1. Visit https://huggingface.co
2. Sign up for a free account or log in
3. Go to your Profile Settings
4. Click on "Access Tokens" in the sidebar
5. Click "New Token"
6. Give it a name and create
7. Copy the token and paste it in Settings → Configure API Key

The API key is required to use the models.
Your key will be saved securely in your config file."""
        messagebox.showinfo("Get API Key", help_text)

    def run(self):
        """Start the GUI application."""
        # Check for API key on startup
        if not self.client.api_key:
            result = messagebox.askyesno(
                "API Key Required",
                "A Hugging Face API key is required to use the models. Would you like to configure it now?"
            )
            if result:
                self._configure_api_key()
        
        self.root.mainloop()


if __name__ == "__main__":
    app = AIModelGUI()
    app.run()
