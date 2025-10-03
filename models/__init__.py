"""
Models package for HIT137 Assignment 3.

This package contains AI model wrappers that integrate with Hugging Face.
Demonstrates encapsulation and polymorphism through a base model interface.

Available Models:
    - BaseModel: Abstract base class for all models
    - TextModel: Text generation/completion model
    - SentimentModel: Sentiment analysis model
    - ImageModel: Image classification/generation model
"""

from models.base_model import BaseModel

# Import specific model implementations when they're ready
try:
    from models.text_model import TextModel, SentimentModel
except ImportError:
    TextModel = None
    SentimentModel = None

try:
    from models.image_model import ImageModel
except ImportError:
    ImageModel = None

# Define what's available when using "from models import *"
__all__ = [
    'BaseModel',
    'TextModel',
    'SentimentModel',
    'ImageModel',
]

# Version info
__version__ = '1.0.0'
__author__ = 'HIT137 Group - Dipak, Rohan, Millan, Mission'