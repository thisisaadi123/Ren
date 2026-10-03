"""Written-out solutions for Stacks & Queues, one module per pattern in stacks_queues/.
Run: python3 tools/solutions/stacks_queues.py [id ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sol  # noqa: E402

for name in sorted(os.listdir(os.path.join(HERE, "stacks_queues"))):
    if name.endswith(".py") and not name.startswith("_"):
        importlib.import_module(f"stacks_queues.{name[:-3]}")

if __name__ == "__main__":
    sol.run(set(sys.argv[1:]))
