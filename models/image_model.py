"""
Image Model class for HIT137 Assignment 3

This module contains image processing model implementations.
Demonstrates inheritance and method overriding.

Author: Rohan (Model implementation)
Team: Mission, Rohan, Millan, Dipak
"""

from models.base_model import BaseModel
from typing import Dict, Any
import logging
import base64
import os

logger = logging.getLogger(__name__)


class ImageModel(BaseModel):
    """
    Image classification/analysis model.
    
    Inherits from BaseModel and overrides process_input for image-specific processing.
    """
    
    def process_input(self, image_path: str) -> Dict[str, Any]:
        """
        Process image input through the model.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dict with status, model, and outputs
        """
        # Validate input
        if not self._validate_input(image_path):
            return {
                "status": "error",
                "model": self._model_id,
                "error": "Invalid input",
                "message": "Image path cannot be empty"
            }
        
        # Check if file exists
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "model": self._model_id,
                "error": "File not found",
                "message": f"Image file not found: {image_path}"
            }
        
        try:
            logger.info(f"Processing image with model: {self._model_id}")
            
            # Read image file
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_data).decode()
            
            # Prepare payload
            payload = {"inputs": image_b64}
            
            # Query the model through the client
            response = self._client.query(self._model_id, payload)
            
            # Add image-specific metadata
            if response.get("status") == "success":
                response["input_type"] = "image"
                response["image_path"] = image_path
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return {
                "status": "error",
                "model": self._model_id,
                "error": str(type(e).__name__),
                "message": str(e)
            }
    
    def _validate_input(self, image_path: str) -> bool:
        """
        Validate image file path.
        
        Args:
            image_path: Path to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not super()._validate_input(image_path):
            return False
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
            logger.warning(f"Unusual image extension: {image_path}")
        
        return True