# gui/app.py
# HIT137 A3 — GUI (Millan's part)

from __future__ import annotations

import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any
from pathlib import Path

# Pillow for image preview
try:
    from PIL import Image, ImageTk
except ImportError as e:
    raise SystemExit(
        "Pillow is not installed. Run: pip install pillow\n"
        f"Original error: {e}"
    )

# Decorators (safe import with fallback to no-op) 
try:

    from utils.decorators import api_call_logger as _log
except Exception:
    # fallback no-op
    def _log(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper

try:
    from utils.decorators import simple_cache as _cache
except Exception:
    # fallback no-op
    def _cache(fn):
        return fn

# Using multiple decorators on the same method
def _human_log_and_cache(fn):
    return _cache(_log(fn))

# A tiny mixin for "multiple inheritance" 
class InfoPanelMixin:
    """Mixin to load markdown/text into info panels; keeps App class tidy."""
    def _load_text_file(self, relpath: str, default_msg: str) -> str:
        p = Path(relpath)
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                return default_msg
        return default_msg

# The GUI 
class App(tk.Tk, InfoPanelMixin):  # Multiple inheritance (Tk + mixin)
    def __init__(self, adapters: Dict[str, Any], mock: bool = False):
        super().__init__()
        self.title("HIT137 – AI Toolkit (GUI)")
        self.geometry("1040x720")
        self.minsize(880, 600)

        # state
        self.adapters = adapters             
        self.mock = mock
        self._busy = False
        self._image_bytes: bytes | None = None
        self._thumb = None  

        # top bar 
        top = ttk.Frame(self)
        top.pack(fill="x", padx=12, pady=10)

        ttk.Label(top, text="Task:").pack(side="left")
        self.task_var = tk.StringVar(value="text")
        self.task_combo = ttk.Combobox(
            top, textvariable=self.task_var, state="readonly",
            values=["text", "image"]
        )
        self.task_combo.pack(side="left", padx=8)

        ttk.Button(top, text="Open Image…", command=self._open_image)\
            .pack(side="left", padx=(12, 0))
        ttk.Button(top, text="Run", command=self._on_run_click)\
            .pack(side="left", padx=8)

        # progress
        self.pbar = ttk.Progressbar(self, mode="indeterminate")
        self.pbar.pack(fill="x", padx=12)

        # main split: left (input/output), right (info/explanations) 
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=10)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(1, weight=1)

        # input box
        ttk.Label(body, text="Input:").grid(row=0, column=0, sticky="w")
        self.input_box = tk.Text(body, height=6)
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        # preview (for image)
        self.preview_label = ttk.Label(body, text="(Image preview appears here)")
        self.preview_label.grid(row=2, column=0, sticky="w", pady=(8, 0))

        # output JSON
        ttk.Label(body, text="Output (JSON):").grid(row=3, column=0, sticky="w", pady=(12, 0))
        self.output_box = tk.Text(body, height=14)
        self.output_box.grid(row=4, column=0, sticky="nsew", padx=(0, 8))

        # right column: info panels
        right = ttk.Frame(body)
        right.grid(row=0, column=1, rowspan=5, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.rowconfigure(3, weight=1)
        right.columnconfigure(0, weight=1)

        ttk.Label(right, text="Model Info").grid(row=0, column=0, sticky="w")
        self.model_info = tk.Text(right, height=12, wrap="word")
        self.model_info.grid(row=1, column=0, sticky="nsew")

        ttk.Label(right, text="OOP Explanations").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.oop_info = tk.Text(right, height=12, wrap="word")
        self.oop_info.grid(row=3, column=0, sticky="nsew")
        self._refresh_docs()
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w")\
            .pack(fill="x", padx=12, pady=(4, 8))

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # helpers
    def _set_busy(self, busy: bool):
        self._busy = busy
        self.status.set("Running…" if busy else "Ready")
        (self.pbar.start(12) if busy else self.pbar.stop())

    def _refresh_docs(self):
        model_text = self._load_text_file(
            "docs/model_info.md",
            default_msg="Model info docs not found. Create docs/model_info.md"
        )
        oop_text = self._load_text_file(
            "docs/oop_explanations.md",
            default_msg="OOP explanation docs not found. Create docs/oop_explanations.md"
        )
        self._set_text(self.model_info, model_text)
        self._set_text(self.oop_info, oop_text)

    def _set_text(self, widget: tk.Text, content: str):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="disabled")

    # UI actions
    @_human_log_and_cache
    def _open_image(self):
        if self.task_var.get() != "image":
            if not messagebox.askyesno(
                "Switch task?",
                "You selected an image, but current task is 'text'. Switch to 'image'?"
            ):
                return
            self.task_var.set("image")

        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")]
        )
        if not path:
            return

        # read bytes for the model
        with open(path, "rb") as f:
            self._image_bytes = f.read()

        # thumbnail for preview
        try:
            img = Image.open(path)
            img.thumbnail((320, 320))
            self._thumb = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self._thumb, text="")
        except Exception as e:
            self.preview_label.config(text=f"(Preview failed: {e})")

        # reflect in input box
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", f"[Selected image: {Path(path).name}]")

    @_human_log_and_cache
    def _on_run_click(self):
        if self._busy:
            return

        task = self.task_var.get()
        raw = self._current_raw(task)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            messagebox.showinfo("Input required", "Please provide text or select an image.")
            return

        
        self._set_busy(True)
        t = threading.Thread(target=self._do_inference, args=(task, raw), daemon=True)
        t.start()

    # core logic 
    def _current_raw(self, task: str):
        if task == "text":
            return self.input_box.get("1.0", "end").strip()
        return self._image_bytes

    def _do_inference(self, task: str, raw):
        try:
            adapter = self.adapters[task]   
            result = adapter.process_input(raw)
        except Exception as e:
            result = {"status": "error", "error": str(e)}

        # hand UI update back to the main thread
        self.after(0, lambda: self._show_result(result))

    def _show_result(self, result: Dict[str, Any]):
        self._set_busy(False)
        self.output_box.delete("1.0", "end")
        try:
            pretty = json.dumps(result, indent=2, ensure_ascii=False)
        except Exception:
            pretty = str(result)
        self.output_box.insert("1.0", pretty)

    def _on_close(self):
        # cleanly close; 
        self.destroy()
