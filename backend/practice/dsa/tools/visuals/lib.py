"""Builds visual.json walkthroughs from a problem's Example 1.

A trace function runs the real algorithm on the example and records steps; each
step is a list of panels the page's renderer (design/visual.js) can draw.
"""
import json
import os
from collections import deque

PROBLEMS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "problems")
MAX_STEPS = 16


def find(pid):
    for root, dirs, files in os.walk(PROBLEMS):
        if os.path.basename(root) == pid and "problem.yaml" in files:
            return root
    raise KeyError(pid)


def example(pid, k=0):
    with open(os.path.join(find(pid), "tests.json")) as f:
        tests = json.load(f)["tests"]
    exs = [t for t in tests if t.get("example")]
    t = exs[k]
    return t["input"], t.get("expected")


# ---------------------------------------------------------------- binary trees

class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def tree(level):
    """Level order -> root Node (None for empty)."""
    if not level or level[0] is None:
        return None
    root = Node(level[0])
    q, i = deque([root]), 1
    while q and i < len(level):
        n = q.popleft()
        for side in ("left", "right"):
            if i < len(level):
                v = level[i]
                i += 1
                if v is not None:
                    c = Node(v)
                    setattr(n, side, c)
                    q.append(c)
    return root


def bfs_nodes(root):
    """Real nodes in level order: the renderer's indexing."""
    out, q = [], deque([root] if root else [])
    while q:
        n = q.popleft()
        out.append(n)
        q.extend(c for c in (n.left, n.right) if c)
    return out


def level_of(root):
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
            continue
        out.append(n.val)
        q.append(n.left)
        q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def nodes_by_val(root):
    return {n.val: n for n in bfs_nodes(root)}


def T(root, st=None, nt=None, label=None):
    """A tree panel. st / nt map Node -> state / note."""
    order = bfs_nodes(root)
    index = {id(n): i for i, n in enumerate(order)}
    p = {"type": "tree", "tree": level_of(root) if root else []}
    if st:
        p["states"] = {str(index[id(n)]): s for n, s in st.items() if n is not None and id(n) in index and s}
    if nt:
        p["notes"] = {str(index[id(n)]): str(v) for n, v in nt.items() if n is not None and id(n) in index and v is not None}
    if label:
        p["label"] = label
    return p


def preorder(root):
    out, stack = [], [root] if root else []
    while stack:
        n = stack.pop()
        out.append(n)
        stack += [c for c in (n.right, n.left) if c]
    return out


def postorder(root):
    return list(reversed([n for n in _rev_pre(root)]))


def _rev_pre(root):
    out, stack = [], [root] if root else []
    while stack:
        n = stack.pop()
        out.append(n)
        stack += [c for c in (n.left, n.right) if c]
    return out


def inorder(root):
    out, stack, t = [], [], root
    while stack or t:
        while t:
            stack.append(t)
            t = t.left
        t = stack.pop()
        out.append(t)
        t = t.right
    return out


def parents(root):
    par = {id(root): None} if root else {}
    for n in bfs_nodes(root):
        for c in (n.left, n.right):
            if c:
                par[id(c)] = n
    return par


def depth_map(root):
    d = {id(root): 0} if root else {}
    for n in bfs_nodes(root):
        for c in (n.left, n.right):
            if c:
                d[id(c)] = d[id(n)] + 1
    return d


def leaf(n):
    return n is not None and not n.left and not n.right


# ---------------------------------------------------------------- other panels

def L(values, st=None, ptr=None, links=None, cycle=None, label=None):
    p = {"type": "list", "values": list(values)}
    if st:
        p["states"] = {str(k): v for k, v in st.items() if v}
    if ptr:
        p["pointers"] = {k: v for k, v in ptr.items() if v is not None}
    if links is not None:
        p["links"] = links
    if cycle is not None:
        p["cycleAt"] = cycle
    if label:
        p["label"] = label
    return p


def Row(cells, st=None, ptr=None, label=None, slots=False):
    p = {"type": "row", "cells": list(cells)}
    if st:
        p["states"] = {str(k): v for k, v in st.items() if v}
    if ptr:
        p["pointers"] = {k: v for k, v in ptr.items() if v is not None}
    if label:
        p["label"] = label
    if slots:
        p["slots"] = True
    return p


def NT(nodes, st=None, nt=None, label=None):
    p = {"type": "ntree", "nodes": nodes}
    if st:
        p["states"] = {str(k): v for k, v in st.items() if v}
    if nt:
        p["notes"] = {str(k): str(v) for k, v in nt.items() if v is not None}
    if label:
        p["label"] = label
    return p


def Vars(**items):
    return {"type": "vars", "items": {k.replace("_", " "): v for k, v in items.items()}}


def fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    if isinstance(v, (list, dict)):
        return json.dumps(v)
    return str(v)


# ---------------------------------------------------------------- recording

class Walk:
    def __init__(self, pid, title):
        self.pid, self.title, self.steps = pid, title, []

    def step(self, text, *panels, call=None, result=None):
        s = {"text": text, "panels": [p for p in panels if p]}
        if call is not None:
            s["call"] = call
        if result is not None:
            s["result"] = fmt(result)
        self.steps.append(s)

    def save(self, **hints):
        assert self.steps, self.pid
        if len(self.steps) > MAX_STEPS:
            # Keep the first and last steps and an even spread in between.
            keep = [round(i * (len(self.steps) - 1) / (MAX_STEPS - 1)) for i in range(MAX_STEPS)]
            self.steps = [self.steps[i] for i in sorted(set(keep))]
        path = os.path.join(find(self.pid), "visual.json")
        data = {}
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
        data.update(hints)
        data["walkthrough"] = {"title": self.title, "steps": self.steps}
        with open(path, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        return len(self.steps)
