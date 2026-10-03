"""Written-out solutions for Two Pointers, one module per pattern in two_pointers/.
Run: python3 tools/solutions/two_pointers.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "two_pointers"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"two_pointers.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
