import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Handles configuration and API key management."""

    @staticmethod
    def get_hf_api_key():
        # Fallback to demo/public access if key not found
        return os.getenv("HF_API_KEY", None)
