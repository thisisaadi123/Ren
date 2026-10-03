"""Written-out solutions for Binary Search, one module per pattern in binary_search/.
Run: python3 tools/solutions/binary_search.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "binary_search"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"binary_search.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
