"""Shared checks for validator.py files. Each raises AssertionError with a readable message.

    from ren_check import ints, integer, text, tree, edges
"""


def integer(name, x, lo, hi):
    assert type(x) is int, "%s must be an integer" % name
    assert lo <= x <= hi, "%s must be between %s and %s" % (name, lo, hi)


def ints(name, arr, min_len, max_len, lo, hi):
    assert isinstance(arr, list), "%s must be a list" % name
    assert min_len <= len(arr) <= max_len, "%s must have %s to %s items" % (name, min_len, max_len)
    for x in arr:
        assert type(x) is int and lo <= x <= hi, "every %s value must be between %s and %s" % (name, lo, hi)


def matrix(name, m, min_rows, max_rows, min_cols, max_cols, lo, hi, rectangular=True):
    assert isinstance(m, list) and min_rows <= len(m) <= max_rows, "%s must have %s to %s rows" % (name, min_rows, max_rows)
    for row in m:
        ints(name + " row", row, min_cols, max_cols, lo, hi)
    if rectangular and m:
        assert all(len(r) == len(m[0]) for r in m), "%s rows must all be the same length" % name


def text(name, s, min_len, max_len, alphabet=None):
    assert isinstance(s, str), "%s must be a string" % name
    assert min_len <= len(s) <= max_len, "%s must have %s to %s characters" % (name, min_len, max_len)
    if alphabet is not None:
        bad = set(s) - set(alphabet)
        assert not bad, "%s may only contain %r" % (name, alphabet if len(alphabet) < 40 else "the allowed characters")


def char_grid(name, g, min_rows, max_rows, min_cols, max_cols, cells):
    assert isinstance(g, list) and min_rows <= len(g) <= max_rows, "%s must have %s to %s rows" % (name, min_rows, max_rows)
    for row in g:
        assert isinstance(row, list) and min_cols <= len(row) <= max_cols, "%s rows must have %s to %s cells" % (name, min_cols, max_cols)
        assert len(row) == len(g[0]), "%s rows must all be the same length" % name
        for c in row:
            assert isinstance(c, str) and len(c) == 1 and c in cells, "%s cells must be one of %r" % (name, cells)


def tree(name, root, max_nodes, lo, hi, min_nodes=0, distinct=False):
    """Level order with None gaps, as the harness expects."""
    assert isinstance(root, list), "%s is given in level order" % name
    values = [v for v in root if v is not None]
    assert min_nodes <= len(values) <= max_nodes, "%s must have %s to %s nodes" % (name, min_nodes, max_nodes)
    assert all(type(v) is int and lo <= v <= hi for v in values), "%s values must be between %s and %s" % (name, lo, hi)
    assert not root or root[0] is not None, "an empty tree is []"
    assert not root or root[-1] is not None, "level order has no trailing nulls"
    slots = 1
    for v in root:
        assert slots > 0, "%s: a value has no parent" % name
        slots -= 1
        if v is not None:
            slots += 2
    if distinct:
        assert len(set(values)) == len(values), "%s values must be distinct" % name
    return values


def is_bst(root):
    """True if a level-order tree is a strict BST."""
    if not root:
        return True
    import collections

    it = iter(root[1:])
    queue = collections.deque([(root[0], float("-inf"), float("inf"))])
    ok = True
    while queue:
        v, lo, hi = queue.popleft()
        if not lo < v < hi:
            ok = False
        for side_lo, side_hi in ((lo, v), (v, hi)):
            child = next(it, None)
            if child is not None:
                queue.append((child, side_lo, side_hi))
    return ok


def edges(name, es, n, directed=False, weight=None, simple=True, allow_self=False, max_edges=None):
    assert isinstance(es, list), "%s must be a list" % name
    if max_edges is not None:
        assert len(es) <= max_edges, "at most %s edges" % max_edges
    seen = set()
    for e in es:
        assert isinstance(e, list) and len(e) == (3 if weight else 2), "each edge is [u, v%s]" % (", w" if weight else "")
        u, v = e[0], e[1]
        assert type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n, "edge endpoints must be 0..n-1"
        assert allow_self or u != v, "no self-loops"
        if weight:
            assert type(e[2]) is int and weight[0] <= e[2] <= weight[1], "weights must be between %s and %s" % weight
        key = (u, v) if directed else (min(u, v), max(u, v))
        if simple:
            assert key not in seen, "no repeated edges"
        seen.add(key)
