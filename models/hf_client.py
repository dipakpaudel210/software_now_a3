import requests
<<<<<<< HEAD
import logging
from config import Config
from utils.decorators import retry_on_failure, log_call
from typing import Dict, Any, Optional
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)
=======
from config import Config
from utils.decorators import retry_on_failure, log_call
>>>>>>> 7c3ea09b9e1745bb2cf9407e30a0ef94b5d9ada2

class HFClient:
    """Encapsulates Hugging Face API interaction with error handling."""

    def __init__(self, model_id: str = None, *, api_key: str = None, mock_mode: bool = False):
        """Initialize the HuggingFace API client.
        
        Args:
            model_id: The ID of the model to use
            api_key: Optional API key to use (overrides config)
            mock_mode: If True, operate in mock mode (no actual API calls)
        """
        self.mock_mode = mock_mode
        self.model_id = model_id
<<<<<<< HEAD
        
        # Get API key from config or parameter
        self.api_key = api_key or Config.get_hf_api_key()
        if not self.api_key and not mock_mode:
            logger.warning("No API key provided. Some models may not work without authentication.")
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json"
        }
        # Remove None values from headers
        self.headers = {k: v for k, v in self.headers.items() if v is not None}

    def _prepare_image_input(self, image_path: str) -> str:
        """Prepare image for API input by converting to base64."""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Resize if too large
                if max(img.size) > 1024:
                    img.thumbnail((1024, 1024))
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                return base64.b64encode(img_byte_arr).decode('utf-8')
        except Exception as e:
            logger.error(f"Error preparing image: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")

    def _format_text_output(self, response: list) -> Dict[str, Any]:
        """Format text classification output."""
        try:
            # Handle different response formats
            if isinstance(response, list):
                if len(response) > 0:
                    if isinstance(response[0], dict):
                        # Classification results
                        results = sorted(response[0], key=lambda x: x.get('score', 0), reverse=True)
                        formatted = {
                            "predictions": results,
                            "top_prediction": results[0]['label'],
                            "confidence": results[0]['score']
                        }
                    else:
                        formatted = {"output": str(response[0])}
                else:
                    formatted = {"output": "No results returned"}
            else:
                formatted = {"output": str(response)}
                
            return {
                "status": "success",
                "data": formatted
            }
        except Exception as e:
            logger.error(f"Error formatting text output: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to format output: {str(e)}"
            }

    def _format_image_output(self, response: list) -> Dict[str, Any]:
        """Format image classification output."""
        try:
            if isinstance(response, list):
                # Classification results
                results = sorted(response, key=lambda x: x.get('score', 0), reverse=True)[:5]
                formatted = {
                    "predictions": results,
                    "top_prediction": results[0]['label'],
                    "confidence": results[0]['score'],
                    "all_predictions": [
                        f"{pred['label']} ({pred['score']:.2%})"
                        for pred in results
                    ]
                }
            else:
                formatted = {"output": str(response)}
                
            return {
                "status": "success",
                "data": formatted
            }
        except Exception as e:
            logger.error(f"Error formatting image output: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to format output: {str(e)}"
            }

    @log_call
    @retry_on_failure(retries=3, delay=2)
    def query(self, model_id: str, input_data: str, pipeline: str) -> Dict[str, Any]:
        """Send query to Hugging Face model and return structured response.
        
        Args:
            model_id: The ID of the model to use
            input_data: The input text or image path
            pipeline: The type of pipeline to use (e.g., "text-classification", "image-classification")
        
        Returns:
            Dict containing the response with proper formatting
        """
=======
        if model_id:
            self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.api_key = api_key or Config.get_hf_api_key()
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    @log_call
    @retry_on_failure(retries=3, delay=2)
    def query(self, model_id_or_payload: str | dict, payload: dict = None):
        """Send input payload to Hugging Face model and return structured response.
        
        This method accepts two calling conventions:
        1. query(payload_dict) - Use the model ID from initialization
        2. query(model_id, payload_dict) - Override the model ID for this call
        
        In mock mode, returns a simulated response without making an actual API call.
        """
        # Handle both calling conventions
        if isinstance(model_id_or_payload, str):
            # Called as query(model_id, payload)
            model_id = model_id_or_payload
            if payload is None:
                raise ValueError("Payload is required when providing model_id")
        else:
            # Called as query(payload)
            model_id = self.model_id
            payload = model_id_or_payload

>>>>>>> 7c3ea09b9e1745bb2cf9407e30a0ef94b5d9ada2
        if self.mock_mode:
            return {
                "status": "success",
                "data": {
<<<<<<< HEAD
                    "model": model_id,
                    "predictions": [
                        {"label": "MOCK_LABEL", "score": 0.95},
                        {"label": "MOCK_LABEL_2", "score": 0.05}
                    ],
                    "top_prediction": "MOCK_LABEL",
                    "confidence": 0.95
                }
            }

        try:
            # Prepare the payload based on pipeline type
            if pipeline == "image-classification":
                # Handle image input
                image_b64 = self._prepare_image_input(input_data)
                payload = {"inputs": image_b64}
            else:
                # Handle text input
                payload = {"inputs": input_data}

            # Make API request
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            response = requests.post(api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # Format the response based on pipeline type
            if pipeline == "image-classification":
                return self._format_image_output(response.json())
            else:
                return self._format_text_output(response.json())
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                "status": "error",
                "message": f"API request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "status": "error",
                "message": f"Error processing query: {str(e)}"
            }
=======
                    "model": model_id or self.model_id or "mock-model",
                    "input": payload.get("inputs", ""),
                    "output": "[Mock Response] " + str(payload.get("inputs", ""))
                }
            }
            
        if not model_id:
            raise ValueError("Model ID must be provided either during initialization or in the query call")
            
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        try:
            response = requests.post(api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
>>>>>>> 7c3ea09b9e1745bb2cf9407e30a0ef94b5d9ada2


# Example usage
if __name__ == "__main__":
    # Text classification model
    client = HFClient("distilbert-base-uncased-finetuned-sst-2-english")
    result = client.query({"inputs": "I love programming with AI!"})
    print(result)

    # Text-to-image (Stable Diffusion small model)
    client2 = HFClient("stabilityai/stable-diffusion-2-1")
    img_result = client2.query({"inputs": "A futuristic car in cyberpunk Tokyo"})
    print(img_result.keys())
