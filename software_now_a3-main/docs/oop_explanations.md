# OOP Concepts used in our GUI

**Multiple Inheritance**
- `class App(tk.Tk, InfoPanelMixin)`: we combine Tk’s window class with a small mixin that loads docs into panels. This keeps the main class tidy and shows mixin-style reuse.The mixin keeps extra functionality (like loading text into the side panels) separate, so the main class doesn’t get too cluttered.

**Encapsulation**
- The GUI keeps some state private-ish (e.g., `_image_bytes`, `_busy`, `_thumb`). Only methods on `App` can read/update them. This makes the internal state safer and ensures other parts of the program don’t mess with it directly.

**Polymorphism & Method Overriding**
- The GUI calls `adapter.process_input(raw)` without caring if it’s text or image. Different adapters (Text vs Image) implement their own behavior behind a common method signature.

**Multiple Decorators**
- GUI actions like `_open_image` and `_on_run_click` are wrapped with two decorators (`_log` and `_cache` via `_human_log_and_cache`) to demonstrate stacked decorators. They are no-ops if helpers aren’t merged yet.

**Why this matters**
- These OOP features make the GUI easier to maintain and extend. For example, we could add a new type of model later without rewriting the whole interface. The code also stays more organized and flexible.