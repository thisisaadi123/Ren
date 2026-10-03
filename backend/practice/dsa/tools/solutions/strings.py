"""Written-out solutions for Strings, one module per pattern in strings_patterns/.
Run: python3 tools/solutions/strings.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "strings_patterns"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"strings_patterns.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
