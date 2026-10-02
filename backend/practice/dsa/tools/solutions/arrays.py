"""Written-out solutions for Arrays & Hashing, one module per pattern in arrays_hashing/.
Run: python3 tools/solutions/arrays.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "arrays_hashing"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"arrays_hashing.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
