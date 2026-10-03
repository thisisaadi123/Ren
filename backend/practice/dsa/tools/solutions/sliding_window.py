"""Written-out solutions for Sliding Window, one module per pattern in window_patterns/.
Run: python3 tools/solutions/sliding_window.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "window_patterns"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"window_patterns.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
