import os
<<<<<<< HEAD
import json
from pathlib import Path
=======
>>>>>>> 7c3ea09b9e1745bb2cf9407e30a0ef94b5d9ada2
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Handles configuration and API key management."""
<<<<<<< HEAD
    
    CONFIG_FILE = "config.json"
    
    @classmethod
    def save_api_key(cls, api_key: str) -> None:
        """Save API key to config file."""
        config_data = {"HF_API_KEY": api_key}
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config_data, f)
    
    @classmethod
    def get_hf_api_key(cls) -> str:
        """Get Hugging Face API key from various sources."""
        # Try environment variable first
        return os.getenv("HF_API_KEY")

=======

    @staticmethod
    def get_hf_api_key():
        # Fallback to demo/public access if key not found
        return os.getenv("HF_API_KEY", None)
>>>>>>> 7c3ea09b9e1745bb2cf9407e30a0ef94b5d9ada2
