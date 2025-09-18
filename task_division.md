# Assignment Work Division

This document defines the **task breakdown across 4 engineers** for building the HIT137 Assignment 3 project. One engineer is junior, so their tasks are lighter and easier.

---

## 👨‍💻 Mission — 
**Files Owned:**
- `config.py`
- `models/hf_client.py`
- `requirements.txt`

**Responsibilities:**
- Finalize Hugging Face API key handling (via env vars, fallback to demo).
- Harden `HFClient` with proper error handling, retries, and structured responses.
- Ensure no secrets are stored in code; update `.gitignore`.
- Pin dependency versions in `requirements.txt`.
- Provide integration examples (sample API responses, cURL snippets).

**Deliverables:**
- Working `HFClient` tested with mock + real API.
- Stable requirements and integration docs.
- Final QA & code review for all PRs.

---

## 👨‍💻 Rohan — 
**Files Owned:**
- `models/base_model.py`
- `models/text_model.py`
- `models/image_model.py`
- Unit tests in `tests/`

**Responsibilities:**
- Implement `BaseModel` abstract class with `process_input()`.
- Build `TextModel`, `SentimentModel`, and `ImageModel` classes.
- Normalize outputs (dicts with `status`, `model`, and `outputs`).
- Add error handling for invalid inputs.
- Write unit tests using `pytest` & `requests-mock`.

**Deliverables:**
- Fully implemented models.
- Tests for all model behaviors (valid + invalid inputs).
- Predictable outputs for GUI consumption.

---

## 👨‍💻 Millan — 
**Files Owned:**
- `gui/app.py`
- `main.py`
- `docs/oop_explanations.md`
- `docs/model_info.md`

**Responsibilities:**
- Improve GUI responsiveness (threads + `after()` updates).
- Add progress indicator and JSON pretty-print in outputs.
- Implement `--mock` mode for offline demos.
- Enhance image preview with thumbnail resizing.
- Update docs with clear OOP concept explanations and model details.

**Deliverables:**
- Smooth, user-friendly GUI.
- Mock/demo mode functional without API key.
- Docs aligned with assignment rubric.

---

## 👨‍💻 Dipak —  (Helpers, Docs, Smoke Tests)
**Files Owned:**
- `utils/decorators.py`
- `models/__init__.py`
- `gui/__init__.py`
- `README.md`
- `smoke/run_smoke.py`

**Responsibilities:**
- Implement helper decorators (`api_call_logger`, `simple_cache`, `retry`).
- Add clean `__init__.py` exports.
- Write beginner-friendly `README.md` (setup, run, troubleshoot).
- Build a smoke test script (`run_smoke.py`) to verify app starts and mock response works.

**Deliverables:**
- Decorators with inline docstrings and examples.
- Easy-to-follow README.
- Simple smoke test proving end-to-end flow.

---

## 🔄 Workflow & Integration
1. **Branching** — Each engineer works on their feature branch.
2. **PR Order:**
   - Dipak (helpers & docs)
   - Rohan (models + tests)
   - Millan (GUI)
   - Mission (HF client + final integration)
3. **Testing:**
   - `pytest` for models & utils.
   - Manual GUI test with `--mock` mode.
   - Smoke test script run before final merge.
4. **Final QA Checklist:**
   - App launches and runs text/image tasks.
   - API key handling correct.
   - Outputs formatted and clear.
   - Docs complete and assignment-ready.

---

## ✅ Final Deliverable
A **fully working, modular Tkinter + Hugging Face application** demonstrating:
- Multiple inheritance
- Multiple decorators
- Encapsulation
- Polymorphism & method overriding
- Separation of concerns (scalable structure)

All tasks divided, tested, and merged — ensuring a smooth system ready for submission. ✨