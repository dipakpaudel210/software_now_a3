# main.py
# App entry
# Supports --mock to run fully offline for demos



from __future__ import annotations
import argparse
import sys

from gui.app import App

# Mock adapters (so you can work before models are merged) 
class _MockTextModel:
    def process_input(self, text: str):
    
        return {
            "status": "ok",
            "model": "mock-text",
            "outputs": [{"label": "POSITIVE", "score": 0.98}],
            "note": "Mock mode — no API calls"
        }

class _MockImageModel:
    def process_input(self, image_bytes: bytes):
        
        return {
            "status": "ok",
            "model": "mock-image",
            "outputs": [{"label": "CAT", "score": 0.93}],
            "note": "Mock mode — no API calls"
        }

def _build_adapters(mock: bool):
    if mock:
        return {"text": _MockTextModel(), "image": _MockImageModel()}

        # real adapters
    try:
        from models.text_model import TextModel
        from models.image_model import ImageModel
        return {"text": TextModel(), "image": ImageModel()}
    except Exception as e:
        print(
            "[WARN] Falling back to mock adapters because real models aren't available yet.\n"
            f"Reason: {e}\n"
            "Tip: run with `--mock` to hide this warning.",
            file=sys.stderr
        )
        return {"text": _MockTextModel(), "image": _MockImageModel()}

def main():
    parser = argparse.ArgumentParser(description="HIT137 – Tkinter + HF GUI")
    parser.add_argument("--mock", action="store_true", help="Run without calling any APIs.")
    args = parser.parse_args()

    adapters = _build_adapters(mock=args.mock)
    app = App(adapters=adapters, mock=args.mock)
    app.mainloop()

if __name__ == "__main__":
    main()
