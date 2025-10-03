"""
Text Model classes for HIT137 Assignment 3

This module contains text processing model implementations.
Demonstrates inheritance and method overriding.

Author: Rohan (Model implementation)
Team: Mission, Rohan, Millan, Dipak
"""

from models.base_model import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TextModel(BaseModel):
    """
    Text generation/completion model.
    
    Inherits from BaseModel and overrides process_input for text-specific processing.
    """
    
    def process_input(self, input_text: str) -> Dict[str, Any]:
        """
        Process text input through the model.
        
        Args:
            input_text: The text to process
            
        Returns:
            Dict with status, model, and outputs
        """
        # Validate input
        if not self._validate_input(input_text):
            return {
                "status": "error",
                "model": self._model_id,
                "error": "Invalid input",
                "message": "Input text cannot be empty"
            }
        
        try:
            logger.info(f"Processing text with model: {self._model_id}")
            
            # Prepare payload for API
            payload = {"inputs": input_text}
            
            # Query the model through the client
            response = self._client.query(self._model_id, payload)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return {
                "status": "error",
                "model": self._model_id,
                "error": str(type(e).__name__),
                "message": str(e)
            }


class SentimentModel(TextModel):
    """
    Sentiment analysis model.
    
    Specialized text model for sentiment analysis.
    Demonstrates further inheritance and specialization.
    """
    
    def process_input(self, input_text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of input text.
        
        Args:
            input_text: Text to analyze
            
        Returns:
            Dict with sentiment analysis results
        """
        # Use parent's validation
        if not self._validate_input(input_text):
            return {
                "status": "error",
                "model": self._model_id,
                "error": "Invalid input",
                "message": "Input text cannot be empty"
            }
        
        try:
            logger.info(f"Analyzing sentiment with model: {self._model_id}")
            
            payload = {"inputs": input_text}
            response = self._client.query(self._model_id, payload)
            
            # Add sentiment-specific formatting
            if response.get("status") == "success":
                response["analysis_type"] = "sentiment"
            
            return response
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {
                "status": "error",
                "model": self._model_id,
                "error": str(type(e).__name__),
                "message": str(e)
            }