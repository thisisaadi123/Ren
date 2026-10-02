"""Ren DSA pipeline: runs a problem's Python files.

Reads JSON lines on stdin and writes JSON lines on stdout, flushing after each
line so the caller can watch progress and kill a runaway test.

Modes:
  solve <file> <spec>     spec is the problem's signature as JSON:
                            {"kind": "function", "function", "params": [{name, type}], "returns"}
                            {"kind": "design", "class", ...}
                          function: file defines `class Solution` with that method.
                          design:   file defines the class; args are {"calls": [[name, *args], ...]}
                                    and the answer is the list of what each call returned.
                          ListNode / TreeNode arguments arrive as arrays and are built into nodes;
                          returned nodes are turned back into arrays.
                          in:  {"id", "args"}        out: {"start": id} then {"id", "out", "ms"} or {"id", "error"}
  validate <file>         file defines validate(**args); an AssertionError fails the input.
                          in:  {"id", "args"}        out: {"id", "ok"} or {"id", "ok": false, "msg"}
  small <file> <seed> <n> file defines small(rng) -> args.  No stdin.  out: {"id", "args"} x n
  build <file>            file defines build(rng, **opts) -> args.
                          in:  {"id", "seed", "opts"}  out: {"id", "args"}
  check <file>            file defines check(args, expected, actual) -> True, or a string saying why not.
                          in:  {"id", "args", "expected", "actual"}  out: {"id", "ok", "msg"?}
"""

import bisect
import collections
import heapq
import importlib.util
import json
import math
import os
import random
import sys
import threading
import time
import traceback
import typing


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


LAST_LIST = []  # nodes of the list built just before, for {"join_at": i}
INPUT_NODES = []  # every RandomNode handed to a solution, so a copy can be told apart


def build_list(value):
    """[1, 2, 3] -> 1 -> 2 -> 3.  {"values": [...], "cycle_at": i} links the tail back to node i;
    {"values": [...], "join_at": i} continues the tail into node i of the list built just before."""
    global LAST_LIST
    cycle_at, join_at = -1, None
    if isinstance(value, dict):
        cycle_at = value.get("cycle_at", -1)
        join_at = value.get("join_at")
        value = value["values"]
    dummy = ListNode()
    tail = dummy
    nodes = []
    for v in value:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if 0 <= cycle_at < len(nodes):
        tail.next = nodes[cycle_at]
    if join_at is not None:
        tail.next = LAST_LIST[join_at]
    LAST_LIST = nodes
    return dummy.next


def build_random(pairs):
    """[[val, random index or None], ...] -> nodes linked by next, with random pointers."""
    nodes = [RandomNode(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        nodes[i].random = nodes[r] if r is not None else None
    INPUT_NODES.extend(nodes)
    return nodes[0] if nodes else None


def random_values(head, limit=2_000_000):
    given = {id(n) for n in INPUT_NODES}
    order, index, node = [], {}, head
    while node is not None and len(order) < limit:
        if id(node) in given:
            raise ValueError("the answer reuses an original node; build new nodes")
        index[id(node)] = len(order)
        order.append(node)
        node = node.next
    if node is not None:
        raise ValueError("returned list is longer than %d nodes (a cycle?)" % limit)
    out = []
    for n in order:
        if n.random is not None and id(n.random) not in index:
            raise ValueError("a random pointer leads outside the returned list")
        out.append([n.val, index[id(n.random)] if n.random is not None else None])
    return out


def list_values(node, limit=2_000_000):
    out = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    if node is not None:
        raise ValueError("returned list is longer than %d nodes (a cycle?)" % limit)
    return out


def build_tree(values):
    """Level order with None for missing children: [3, 9, 20, None, None, 15, 7]."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = collections.deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_values(root):
    out = []
    queue = collections.deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def to_arg(value, type_):
    base = type_.rstrip("[]")
    depth = (len(type_) - len(base)) // 2
    if base not in ("ListNode", "TreeNode", "RandomNode"):
        return value
    if depth:
        return [to_arg(v, type_[:-2]) for v in value]
    if base == "RandomNode":
        return build_random(value)
    return build_list(value) if base == "ListNode" else build_tree(value)


def from_out(value, type_):
    base = type_.rstrip("[]")
    depth = (len(type_) - len(base)) // 2
    if base not in ("ListNode", "TreeNode", "RandomNode"):
        return plain(value)
    if depth:
        return [from_out(v, type_[:-2]) for v in value]
    if base == "RandomNode":
        return random_values(value)
    return list_values(value) if base == "ListNode" else tree_values(value)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # What LeetCode-style solutions expect to find without importing.
    module.ListNode = ListNode
    module.RandomNode = RandomNode
    module.TreeNode = TreeNode
    for extra in ("List", "Optional", "Dict", "Tuple", "Set"):
        setattr(module, extra, getattr(typing, extra))
    module.collections = collections
    module.heapq = heapq
    module.math = math
    module.bisect = bisect
    spec.loader.exec_module(module)
    return module


def emit(obj):
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def plain(value):
    """Tuples and other sequences become lists so every language compares the same way."""
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def lines():
    for raw in sys.stdin:
        raw = raw.strip()
        if raw:
            yield json.loads(raw)


def short_error(exc):
    tb = traceback.extract_tb(exc.__traceback__)
    where = "line %d" % tb[-1].lineno if tb else ""
    return "%s: %s (%s)" % (type(exc).__name__, exc, where)


def main():
    mode, path = sys.argv[1], sys.argv[2]
    # Shared helpers for gen.py and validator.py (ren_gen, ren_check).
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pylib"))
    sys.setrecursionlimit(1 << 22)

    if mode == "solve":
        spec = json.loads(sys.argv[3])
        module = load(path, "solution")
        for test in lines():
            emit({"start": test["id"]})
            try:
                if spec["kind"] == "design":
                    cls = getattr(module, spec["class"])
                    calls = test["args"]["calls"]
                    t0 = time.perf_counter()
                    obj = cls(*calls[0][1:])
                    out = [None]
                    for call in calls[1:]:
                        out.append(plain(getattr(obj, call[0])(*call[1:])))
                else:
                    args = {p["name"]: to_arg(test["args"][p["name"]], p["type"]) for p in spec["params"]}
                    fn = getattr(module.Solution(), spec["function"])
                    t0 = time.perf_counter()
                    raw = fn(**args)
                    ms = (time.perf_counter() - t0) * 1000
                    out = from_out(raw, spec["returns"])
                if spec["kind"] == "design":
                    ms = (time.perf_counter() - t0) * 1000
                emit({"id": test["id"], "out": out, "ms": round(ms, 3)})
            except Exception as exc:  # noqa: BLE001 - any failure is a failed test
                emit({"id": test["id"], "error": short_error(exc)})

    elif mode == "validate":
        module = load(path, "validator")
        for test in lines():
            try:
                module.validate(**test["args"])
                emit({"id": test["id"], "ok": True})
            except AssertionError as exc:
                emit({"id": test["id"], "ok": False, "msg": str(exc) or "assertion failed"})
            except Exception as exc:  # noqa: BLE001
                emit({"id": test["id"], "ok": False, "msg": short_error(exc)})

    elif mode == "small":
        module = load(path, "gen")
        seed, count = sys.argv[3], int(sys.argv[4])
        for i in range(count):
            rng = random.Random("%s:small:%d" % (seed, i))
            emit({"id": "small-%d" % i, "args": module.small(rng)})

    elif mode == "build":
        module = load(path, "gen")
        for test in lines():
            rng = random.Random("%s:%s" % (test["seed"], test["id"]))
            emit({"id": test["id"], "args": module.build(rng, **test["opts"])})

    elif mode == "check":
        module = load(path, "checker")
        for test in lines():
            try:
                verdict = module.check(test["args"], test["expected"], test["actual"])
            except Exception as exc:  # noqa: BLE001
                verdict = short_error(exc)
            if verdict is True:
                emit({"id": test["id"], "ok": True})
            else:
                emit({"id": test["id"], "ok": False, "msg": str(verdict)})

    else:
        sys.exit("unknown mode: %s" % mode)


if __name__ == "__main__":
    # A deep stack for recursive solutions (a 10^5-node chain), as the Java harness has.
    # Python 3.9 crashes near 50,000 frames on the main thread's 8 MB stack.
    threading.stack_size(512 * 1024 * 1024)
    failed = []

    def run():
        try:
            main()
        except SystemExit as exc:
            failed.append(exc.code)
        except BaseException:  # noqa: BLE001 - report it as the main thread would
            traceback.print_exc()
            failed.append(1)

    worker = threading.Thread(target=run)
    worker.start()
    worker.join()
    if failed:
        sys.exit(failed[0])
