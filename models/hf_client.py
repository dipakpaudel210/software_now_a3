import requests
from config import Config
from utils.decorators import retry_on_failure, log_call

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

        if self.mock_mode:
            return {
                "status": "success",
                "data": {
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
