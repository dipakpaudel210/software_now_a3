"""
Base Model class for HIT137 Assignment 3

This module defines the abstract base class for all AI models.
Demonstrates inheritance, polymorphism, and encapsulation.

Author: Rohan (Model architecture)
Team: Mission, Rohan, Millan, Dipak
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModel(ABC):
    """
    Abstract base class for all AI models.
    
    This class demonstrates:
    - Abstraction through ABC
    - Encapsulation with protected attributes
    - Polymorphism through abstract methods
    
    Attributes:
        _client: HuggingFace API client (protected)
        _model_id: Model identifier (protected)
    """
    
    def __init__(self, client, model_id: str):
        """
        Initialize the base model.
        
        Args:
            client: HuggingFace API client instance
            model_id: The model identifier from HuggingFace
        """
        self._client = client
        self._model_id = model_id
    
    @abstractmethod
    def process_input(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input data through the model.
        
        This is an abstract method that must be implemented by subclasses.
        Each model type (text, image) will have its own implementation.
        
        Args:
            input_data: The input to process (type varies by model)
            
        Returns:
            Dict containing status, model name, and outputs
            
        Raises:
            NotImplementedError: If subclass doesn't implement this method
        """
        pass
    
    def get_model_id(self) -> str:
        """
        Get the model identifier.
        
        Returns:
            The model ID string
        """
        return self._model_id
    
    def _validate_input(self, input_data: Any) -> bool:
        """
        Validate input data (protected method).
        
        Args:
            input_data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if input_data is None:
            return False
        if isinstance(input_data, str) and len(input_data.strip()) == 0:
            return False
        return True
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}(model_id='{self._model_id}')"