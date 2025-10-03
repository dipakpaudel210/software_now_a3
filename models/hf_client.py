import requests
from config import Config
from utils.decorators import retry_on_failure, log_call

class HFClient:
    """Encapsulates Hugging Face API interaction with error handling."""

    def __init__(self, model_id: str):
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.headers = {"Authorization": f"Bearer {Config.get_hf_api_key()}"} if Config.get_hf_api_key() else {}

    @log_call
    @retry_on_failure(retries=3, delay=2)
    def query(self, payload: dict):
        """Send input payload to Hugging Face model and return structured response."""
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
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
