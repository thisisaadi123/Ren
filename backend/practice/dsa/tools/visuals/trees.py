import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


CUSTOM = {
    "widest-floor": [{"root": [1, 3, 2, 5, 3, None, 9, 6, None, None, None, None, None, 7]}],
    "shallowest-leaf": [{"root": [2, None, 3, None, 4, None, 5, None, 6]}],
    "average-per-floor": [{"root": [3, 9, 20, 1, None, 15, 7, None, 2, None, None, 8]}],
    "zigzag-floors": [{"root": [3, 9, 20, 1, 4, 15, 7, 6, None, None, None, 5]}],
    "mirror-trails": [{"root": [2, 3, 1, 3, 1, 4, 1, None, None, 2, 3]}],
    "smallest-leaf-word": [{"root": [25, 1, 3, 1, 3, 0, 2, 4, None, None, None, None, 7]}],
    "right-side-view": [{"root": [1, 2, 3, 4, 5, None, 6, 7, None, None, 8]}],
    "nearest-exit": [{"root": [1, None, 2, None, 3, None, 4, None, 5, None, 6], "start": 3}],
    "twin-trees": [{"a": [1, 2, 3, 4, 5, 6, 7], "b": [1, 2, 3, 4, 5, 6, 7]}],
    "mirror-image-check": [{"root": [1, 2, 2, 3, 4, 4, 3, 5, None, None, 6, 6, None, None, 5]}],
    "shared-ancestor-queries": [{"parent": [-1, 0, 0, 1, 1, 2, 2, 3, 3, 6], "queries": [[7, 8], [7, 4], [8, 9], [4, 5], [9, 6]]}],
    "hops-between-nodes": [{"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 7, "q": 8}],
    "ancestor-or-none": [{"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 7, "q": 4}],
    "tree-outline": [{"root": [1, 2, 3, 4, 5, 6, None, None, None, 7, 8, 9, 10]}],
    "longest-zigzag-walk": [{"root": [1, 1, 1, None, 1, None, None, 1, 1, None, 1]}],
}
run = make_runner(DONE, CUSTOM)


def _left_edge(n):
    out = []
    while n:
        out.append(n)
        n = n.left
    return out


def lvl(root):
    """Nodes grouped by level."""
    out, cur = [], [root] if root else []
    while cur:
        out.append(cur)
        cur = [c for n in cur for c in (n.left, n.right) if c]
    return out


# ======================================================================== dfs-orders

@run
def flatten_to_a_spine(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Rewiring the tree into a pre-order chain, one node at a time, without extra memory.")
    W.step("Walk down the right pointers. At each node with a left subtree, that subtree must slot in between the node and its right subtree.", T(root, {root: "active"}))
    cur = root
    while cur:
        if cur.left:
            tail = cur.left
            while tail.right:
                tail = tail.right
            W.step(f"At {cur.val}: the last node of its left subtree in pre-order is {tail.val}. Hang {cur.val}'s right subtree off {tail.val}.", T(root, {cur: "active", tail: "found"}))
            tail.right = cur.right
            cur.right, cur.left = cur.left, None
            W.step(f"Move the left subtree over to the right of {cur.val} and clear its left pointer.", T(root, {cur: "active", cur.right: "new"}))
        cur = cur.right
    assert level_of(root) == exp
    W.step("Every left pointer is empty, and following the right pointers reads the tree in pre-order.", T(root, {n: "found" for n in bfs_nodes(root)}))
    return W.save()


@run
def subtree_tally_updates(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    order = preorder(root)
    tin = {id(n): i for i, n in enumerate(order)}
    size = {}
    for n in postorder(root):
        size[id(n)] = 1 + sum(size[id(c)] for c in (n.left, n.right) if c)
    byv = nodes_by_val(root)
    tally = [0] * len(order)
    W = Walk(pid, "Number the offices in pre-order: every branch becomes one unbroken stretch of that list.")
    W.step("In pre-order, an office comes right before everything in its branch. So office v's branch is the stretch starting at its position, as long as the branch's size.",
           T(root, nt={n: tin[id(n)] for n in order}), Row([n.val for n in order], label="pre-order"))
    out = []
    for op in a["ops"]:
        v = byv[op[1]]
        i = tin[id(v)]
        if op[0] == 1:
            tally[i] += op[2]
            W.step(f"Office {v.val} gets {op[2]} more: add it at position {i}.", T(root, {v: "active"}, {n: tally[tin[id(n)]] or None for n in order}),
                   Row(tally, st={i: "new"}, label="tally by position"))
        else:
            lo, hi = i, i + size[id(v)]
            s = sum(tally[lo:hi])
            out.append(s)
            W.step(f"Report {v.val}: its branch is positions {lo}–{hi - 1}, which add up to {s}. (A Fenwick tree makes each update and range sum O(log n).)",
                   T(root, {n: "found" for n in order if lo <= tin[id(n)] < hi}, {n: tally[tin[id(n)]] or None for n in order}),
                   Row(tally, st={j: "found" for j in range(lo, hi)}, label="tally by position"))
    assert out == exp
    return W.save()


@run
def shelf_order_readout(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "An in-order walk with a stack: go left as far as possible, then read a node and turn right.")
    out, stack, t = [], [], root
    while stack or t:
        while t:
            stack.append(t)
            t = t.left
        t = stack.pop()
        out.append(t.val)
        W.step(f"Nothing further left: read {t.val}, then move to its right subtree.", T(root, {t: "active", **{s: "found" for s in stack}}),
               Row([s.val for s in stack], label="stack"), Row(out, st={len(out) - 1: "new"}, label="output"))
        t = t.right
    assert out == exp
    return W.save()


@run
def family_line_queries(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    clock = [0]
    tin, tout = {}, {}

    def go(n):
        tin[n.val] = clock[0]
        clock[0] += 1
        for c in (n.left, n.right):
            if c:
                go(c)
        tout[n.val] = clock[0]
        clock[0] += 1

    go(root)
    W = Walk(pid, "Stamp each person with the time a depth-first walk enters and leaves them.")
    allnodes = bfs_nodes(root)
    W.step("Walk the tree depth-first with a clock. a is an ancestor of b exactly when a is entered before b and left after b.",
           T(root, nt={n: f"{tin[n.val]}–{tout[n.val]}" for n in allnodes}))
    out = []
    byv = nodes_by_val(root)
    for x, y in a["queries"]:
        ok = x != y and tin[x] < tin[y] and tout[y] < tout[x]
        out.append(ok)
        W.step(f"Is {x} a strict ancestor of {y}? {x} spans {tin[x]}–{tout[x]} and {y} spans {tin[y]}–{tout[y]}: {'yes, it sits inside' if ok else 'no'}.",
               T(root, {byv[x]: "mark", byv[y]: "answer" if ok else "active"}, {n: f"{tin[n.val]}–{tout[n.val]}" for n in allnodes}), result=ok)
    assert out == exp
    return W.save()


@run
def folder_cleanup_order(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "A post-order walk: a folder is deleted only after everything inside it.")
    out = []
    for n in postorder(root):
        out.append(n.val)
        W.step(f"Both of {n.val}'s branches are done, so delete {n.val}.", T(root, {n: "active", **{m: "dim" for m in bfs_nodes(root) if m.val in out[:-1]}}), Row(out, st={len(out) - 1: "new"}, label="order"))
    assert out == exp
    return W.save()


# ======================================================================== level-order

@run
def widest_floor(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Number every seat: the root is seat 0, and a node in seat i has children in seats 2i and 2i + 1.")
    seat = {id(root): 0}
    best = 0
    for floor in lvl(root):
        for n in floor:
            if n.left:
                seat[id(n.left)] = 2 * seat[id(n)]
            if n.right:
                seat[id(n.right)] = 2 * seat[id(n)] + 1
        w = seat[id(floor[-1])] - seat[id(floor[0])] + 1
        best = max(best, w)
        W.step(f"This floor runs from seat {seat[id(floor[0])]} to seat {seat[id(floor[-1])]}: width {w}. Widest so far: {best}.",
               T(root, {n: "active" for n in floor}, {n: seat[id(n)] for n in floor}))
    assert best == exp
    return W.save()


@run
def shallowest_leaf(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Go floor by floor; the first floor with a leaf gives the answer.")
    for d, floor in enumerate(lvl(root), 1):
        hit = [n for n in floor if leaf(n)]
        if hit:
            W.step(f"Floor {d} has a leaf ({hit[0].val}), so the shallowest leaf is at depth {d}.", T(root, {**{n: "active" for n in floor}, hit[0]: "answer"}))
            assert d == exp
            break
        W.step(f"Floor {d}: no leaves yet, every node has a child.", T(root, {n: "active" for n in floor}))
    return W.save()


@run
def average_per_floor(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Visit each floor with a queue and average its values.")
    out = []
    for floor in lvl(root):
        s = sum(n.val for n in floor)
        out.append(s / len(floor))
        W.step(f"Floor values {', '.join(str(n.val) for n in floor)}: sum {s} over {len(floor)} node{'s' if len(floor) > 1 else ''} = {fmt(out[-1])}.",
               T(root, {n: "active" for n in floor}), Row([fmt(x) for x in out], st={len(out) - 1: "new"}, label="averages"))
    assert all(abs(x - y) < 1e-9 for x, y in zip(out, exp))
    return W.save()


@run
def cousin_sums(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "A node's cousins are everyone on its floor except itself and its sibling.")
    new = {}
    floors = lvl(root)
    W.step("Work floor by floor. For each family (a parent's children), cousins' sum = floor total − the family's own total.", T(root))
    for floor in floors:
        total = sum(n.val for n in floor)
        if floor[0] is root:
            new[id(root)] = 0
            W.step("The root has no cousins: it becomes 0.", T(root, {root: "active"}, {root: 0}))
            continue
        parents_ = [p for p in bfs_nodes(root) if p.left in floor or p.right in floor]
        for p in parents_:
            kids = [c for c in (p.left, p.right) if c]
            fam = sum(c.val for c in kids)
            for c in kids:
                new[id(c)] = total - fam
        W.step(f"This floor adds up to {total}. Each node gets the total minus its own family's sum.", T(root, {n: "active" for n in floor}, {n: new[id(n)] for n in floor}))
    for n in bfs_nodes(root):
        n.val = new[id(n)]
    assert level_of(root) == exp
    W.step("Write the new values into the tree.", T(root, {n: "found" for n in bfs_nodes(root)}))
    return W.save()


@run
def zigzag_floors(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Read floors with a queue, flipping direction on every other floor.")
    out = []
    for d, floor in enumerate(lvl(root)):
        vals = [n.val for n in floor]
        if d % 2:
            vals.reverse()
        out.append(vals)
        W.step(f"Floor {d}: read {'right to left' if d % 2 else 'left to right'}: {vals}.", T(root, {n: "active" for n in floor}), Row(vals, label=f"floor {d}"))
    assert out == exp
    return W.save()


# ======================================================================== root-to-leaf

def leaf_paths(root):
    """Root-to-leaf paths in DFS order (left first)."""
    out, stack = [], [(root, [root])]
    while stack:
        n, path = stack.pop()
        if leaf(n):
            out.append(path)
        for c in (n.right, n.left):
            if c:
                stack.append((c, path + [c]))
    return out


@run
def mirror_trails(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Walk every trail from the root to a leaf and check whether its digits read the same both ways.")
    count = 0
    for path in leaf_paths(root):
        digits = [n.val for n in path]
        ok = digits == digits[::-1]
        count += ok
        W.step(f"Trail {' → '.join(map(str, digits))} {'reads the same backwards' if ok else 'does not read the same backwards'}. Mirror trails: {count}.",
               T(root, {n: ("answer" if ok else "active") for n in path}))
    assert count == exp
    return W.save()


@run
def smallest_leaf_word(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Spell the word for every leaf (leaf up to root) and keep the smallest.")
    best = None
    for path in leaf_paths(root):
        word = "".join(chr(97 + n.val) for n in reversed(path))
        if best is None or word < best:
            best = word
        W.step(f"From leaf {path[-1].val} up: \"{word}\". Smallest so far: \"{best}\".", T(root, {n: "active" for n in path}, {n: chr(97 + n.val) for n in bfs_nodes(root)}))
    assert best == exp
    return W.save()


@run
def trails_hitting_target(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    t = a["target"]
    W = Walk(pid, f"Carry the running sum down each trail and keep the trails that end at a leaf with sum {t}.")
    out = []
    for path in leaf_paths(root):
        s = sum(n.val for n in path)
        if s == t:
            out.append([n.val for n in path])
        W.step(f"Trail {' → '.join(str(n.val) for n in path)} adds up to {s}{' — a match' if s == t else ''}.", T(root, {n: ("answer" if s == t else "active") for n in path}))
    assert out == exp
    return W.save()


@run
def digit_trail_total(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Pass the number built so far down the tree: at each node it becomes number × 10 + digit.")
    num = {id(root): root.val}
    for n in bfs_nodes(root):
        for c in (n.left, n.right):
            if c:
                num[id(c)] = num[id(n)] * 10 + c.val
    W.step("Each node's note is the number spelled from the root down to it.", T(root, nt={n: num[id(n)] for n in bfs_nodes(root)}))
    total = 0
    for path in leaf_paths(root):
        total += num[id(path[-1])]
        W.step(f"Leaf {path[-1].val} finishes the number {num[id(path[-1])]}. Running total: {total}.", T(root, {n: "active" for n in path}, {n: num[id(n)] for n in bfs_nodes(root)}))
    assert total == exp
    return W.save()


@run
def exact_trail_sum(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    t = a["target"]
    W = Walk(pid, f"Subtract each node's value from {t} on the way down; a leaf that leaves exactly 0 is a match.")
    found = False
    for path in leaf_paths(root):
        s = sum(n.val for n in path)
        W.step(f"Trail {' → '.join(str(n.val) for n in path)} adds up to {s}.", T(root, {n: ("answer" if s == t else "active") for n in path}))
        if s == t:
            found = True
            W.step(f"That's {t}, so the answer is true and the search can stop.", T(root, {n: "answer" for n in path}), result=True)
            break
    assert found == exp
    return W.save()


# ======================================================================== bottom-up

def post_walk(W, root, compute, say, extra=None, note=None):
    """compute(node, left_value, right_value) -> value; say(node, value) -> text."""
    note = note or fmt_note
    val = {}
    for n in postorder(root):
        lv = val.get(id(n.left)) if n.left else None
        rv = val.get(id(n.right)) if n.right else None
        val[id(n)] = compute(n, lv, rv)
        notes = {m: note(val[id(m)]) for m in bfs_nodes(root) if id(m) in val}
        st = {m: "found" for m in bfs_nodes(root) if id(m) in val}
        st[n] = "active"
        W.step(say(n, val[id(n)]), T(root, st, notes), *(extra() if extra else []))
    return val


def fmt_note(v):
    return v if not isinstance(v, tuple) else v[0]


@run
def best_split_product(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    total = sum(n.val for n in bfs_nodes(root))
    W = Walk(pid, "Cutting the link above a node splits off that node's whole branch. Branch sums give every possible cut.")
    best = [0, None]

    def comp(n, l, r):
        s = n.val + (l or 0) + (r or 0)
        if n is not root and s * (total - s) > best[0]:
            best[0], best[1] = s * (total - s), n
        return s

    post_walk(W, root, comp, lambda n, s: f"{n.val}'s branch sums to {s}." + (f" Cutting above it gives {s} × {total - s} = {s * (total - s)}." if n is not root else f" That's the whole tree, {total}."))
    W.step(f"The best cut is above {best[1].val}: product {best[0]}.", T(root, {m: "answer" for m in preorder(best[1])}), result=best[0] % (10**9 + 7))
    assert best[0] % (10**9 + 7) == exp
    return W.save()


@run
def longest_walk_across(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node reports its height; the longest walk bending at a node uses both sides' heights.")
    best = [0]

    def comp(n, l, r):
        l, r = l or 0, r or 0
        best[0] = max(best[0], l + r)
        return 1 + max(l, r)

    post_walk(W, root, comp, lambda n, h: f"{n.val} has height {h}. A walk bending here can use {h - 1 if not (n.left and n.right) else 'both sides'}; longest so far: {best[0]} corridors.")
    assert best[0] == exp
    return W.save()


@run
def complete_tree_headcount(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "In a complete tree, compare the leftmost and rightmost depths: when they match, that subtree is perfect and has 2^h − 1 nodes.")

    def edge_h(n, side):
        h = 0
        while n:
            h += 1
            n = getattr(n, side)
        return h

    def count(n):
        if not n:
            return 0
        lh, rh = edge_h(n, "left"), edge_h(n, "right")
        if lh == rh:
            W.step(f"Under {n.val} the left and right edges are both {lh} deep: a perfect subtree of 2^{lh} − 1 = {2 ** lh - 1} nodes. No need to look inside.", T(root, {m: "found" for m in preorder(n)} | {n: "active"}))
            return 2 ** lh - 1
        W.step(f"Under {n.val} the left edge is {lh} deep but the right edge only {rh}: count {n.val} itself and recurse into both children.", T(root, {n: "active"}))
        return 1 + count(n.left) + count(n.right)

    c = count(root)
    W.step(f"Total: {c} nodes.", T(root, {m: "found" for m in bfs_nodes(root)}), result=c)
    assert c == exp
    return W.save()


@run
def tallest_branch(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node's height is 1 + the taller of its children's heights. Leaves have height 1.")
    val = post_walk(W, root, lambda n, l, r: 1 + max(l or 0, r or 0), lambda n, h: f"{n.val}: height {h}.")
    assert val[id(root)] == exp
    return W.save()


@run
def richest_route(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node reports the best downward route starting at it; a route can bend at any node and use both sides.")
    best = [root.val]

    def comp(n, l, r):
        gl, gr = max(0, l or 0), max(0, r or 0)
        best[0] = max(best[0], n.val + gl + gr)
        return n.val + max(gl, gr)

    post_walk(W, root, comp, lambda n, g: f"Best route going down from {n.val}: {g}. Best route anywhere so far, bending at any node: {best[0]}.")
    W.step(f"The richest route totals {best[0]}.", T(root), result=best[0])
    assert best[0] == exp
    return W.save()


@run
def balanced_canopy(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node reports its height; it's balanced when its children's heights differ by at most 1.")
    ok = [True]

    def comp(n, l, r):
        l, r = l or 0, r or 0
        if abs(l - r) > 1:
            ok[0] = False
        return 1 + max(l, r)

    def say(n, h):
        return f"{n.val}: height {h}, children's heights differ by {abs((post_h.get(id(n.left), 0)) - (post_h.get(id(n.right), 0)))}."

    post_h = {}

    def comp2(n, l, r):
        h = comp(n, l, r)
        post_h[id(n)] = h
        return h

    post_walk(W, root, comp2, say)
    W.step("Every node is within 1, so the canopy is balanced." if ok[0] else "Some node's sides differ by more than 1: not balanced.", T(root), result=ok[0])
    assert ok[0] == exp
    return W.save()


# ======================================================================== lca

@run
def where_paths_split(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    p, q = a["p"], a["q"]
    W = Walk(pid, f"Ask each subtree whether it holds {p} or {q}; the first node that hears back from both sides is the answer.")
    byv = nodes_by_val(root)
    marks = {byv[p]: "mark", byv[q]: "mark"}
    W.step(f"We're looking for {p} and {q}. Each node asks its two subtrees what they found.", T(root, {root: "active", **marks}))
    got = {}
    answer = None
    for n in postorder(root):
        l, r = got.get(id(n.left)), got.get(id(n.right))
        if n.val in (p, q):
            got[id(n)] = n
            W.step(f"{n.val} is one of the two, so it reports itself (anything below it can't be lower than it).", T(root, {**{m: "found" for m in bfs_nodes(root) if got.get(id(m))}, n: "found", **{x: s for x, s in marks.items() if not got.get(id(x))}}))
        elif l and r:
            got[id(n)] = n
            answer = n
            W.step(f"{n.val} hears {l.val} from the left and {r.val} from the right: the paths split here.", T(root, {**{m: "found" for m in bfs_nodes(root) if got.get(id(m))}, n: "answer"}))
            break
        else:
            got[id(n)] = l or r
            if l or r:
                W.step(f"{n.val} heard from one side only, so it passes {(l or r).val} up.", T(root, {**{m: "found" for m in bfs_nodes(root) if got.get(id(m))}, **{x: s for x, s in marks.items() if not got.get(id(x))}}))
    if answer is None:
        answer = got[id(root)]
    if answer.val != exp:
        raise AssertionError((pid, answer.val, exp))
    if W.steps[-1]["text"].find("split") < 0:
        W.step(f"Only one side ever reported, so the answer is the node that was found first: {answer.val}.", T(root, {answer: "answer"}))
    return W.save(mark=["p", "q"], answer="nodes")


@run
def hops_between_nodes(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    p, q = a["p"], a["q"]
    byv = nodes_by_val(root)
    par, dep = parents(root), depth_map(root)
    W = Walk(pid, f"Climb from the deeper of {p} and {q} until both are at the same depth, then climb both together until they meet. Each climb is one hop.")
    x, y = byv[p], byv[q]
    notes = {n: dep[id(n)] for n in bfs_nodes(root)}
    W.step(f"{p} is at depth {dep[id(x)]} and {q} at depth {dep[id(y)]} (notes are depths).", T(root, {x: "mark", y: "mark"}, notes))
    a1, b1, hops, trail = x, y, 0, set()
    while dep[id(a1)] > dep[id(b1)] or dep[id(b1)] > dep[id(a1)]:
        if dep[id(a1)] > dep[id(b1)]:
            trail.add(a1)
            a1 = par[id(a1)]
        else:
            trail.add(b1)
            b1 = par[id(b1)]
        hops += 1
        W.step(f"Even out the depths: climb to {a1.val if a1 not in trail else b1.val}. Hops so far {hops}.", T(root, {**{n: "found" for n in trail}, a1: "active", b1: "active", x: "mark", y: "mark"}, notes))
    while a1 is not b1:
        trail.add(a1)
        trail.add(b1)
        a1, b1 = par[id(a1)], par[id(b1)]
        hops += 2
        W.step(f"Climb both: now at {a1.val} and {b1.val}. Hops so far {hops}.", T(root, {**{n: "found" for n in trail}, a1: "active", b1: "active", x: "mark", y: "mark"}, notes))
    W.step(f"They meet at {a1.val}: {hops} hops.", T(root, {**{n: "found" for n in trail}, a1: "answer", x: "mark", y: "mark"}, notes), result=hops)
    assert hops == exp
    return W.save(mark=["p", "q"])



@run
def deepest_leaves_ancestor(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each subtree reports (its depth, the lowest node covering its deepest nodes).")
    info = {}
    for n in postorder(root):
        dl, al = info.get(id(n.left), (0, None)) if n.left else (0, None)
        dr, ar = info.get(id(n.right), (0, None)) if n.right else (0, None)
        if dl > dr:
            info[id(n)] = (dl + 1, al)
            why = f"the left side is deeper, so pass {al.val} up"
        elif dr > dl:
            info[id(n)] = (dr + 1, ar)
            why = f"the right side is deeper, so pass {ar.val} up"
        else:
            info[id(n)] = (dl + 1, n)
            why = "both sides are equally deep, so this node covers all their deepest nodes" if n.left else "a leaf covers itself"
        cover = info[id(n)][1]
        W.step(f"At {n.val}: {why}.", T(root, {**{m: "found" for m in bfs_nodes(root) if id(m) in info}, n: "active", cover: "mark" if cover is not n else "active"}, {m: info[id(m)][0] for m in bfs_nodes(root) if id(m) in info}))
    ans = info[id(root)][1]
    W.step(f"The root reports {ans.val}.", T(root, {ans: "answer"}), result=ans.val)
    assert ans.val == exp
    return W.save()


@run
def ancestor_or_none(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    p, q = a["p"], a["q"]
    W = Walk(pid, f"One full post-order pass counts how many of {p} and {q} each subtree holds (notes). The lowest node whose count reaches 2 is the answer; if none does, one is missing.")
    cnt, ans = {}, None
    for n in postorder(root):
        c = (n.val == p) + (n.val == q) + (cnt.get(id(n.left), 0) if n.left else 0) + (cnt.get(id(n.right), 0) if n.right else 0)
        cnt[id(n)] = c
        notes = {m: cnt[id(m)] for m in bfs_nodes(root) if id(m) in cnt}
        if c == 2 and ans is None:
            ans = n
            W.step(f"{n.val}'s subtree holds both: it's the lowest common node.", T(root, {n: "answer"}, notes))
            break
        W.step(f"{n.val}'s subtree holds {c} of the two" + (" (it is one of them)." if n.val in (p, q) else "."), T(root, {**{m: "found" for m in bfs_nodes(root) if cnt.get(id(m))}, n: "active"}, notes))
    res = ans.val if ans else -1
    if ans is None:
        W.step("No subtree holds both: -1.", T(root), result=-1)
    assert res == exp
    return W.save(mark=["p", "q"], answer="nodes")


# ======================================================================== tree-views

@run
def tree_outline(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "The outline is the root, the left edge going down, every leaf left to right, then the right edge coming back up.")
    out, st = [root.val], {root: "answer"}
    W.step("Start with the root.", T(root, dict(st)), Row(out, label="outline"))
    if not leaf(root):
        n = root.left
        while n and not leaf(n):
            out.append(n.val)
            st[n] = "found"
            W.step(f"Left edge: {n.val}.", T(root, {**st, n: "active"}), Row(out, label="outline"))
            n = n.left or n.right
        for x in [m for m in preorder(root) if leaf(m) and m is not root]:
            out.append(x.val)
            st[x] = "found"
            W.step(f"Leaf {x.val}.", T(root, {**st, x: "active"}), Row(out, label="outline"))
        right, n = [], root.right
        while n and not leaf(n):
            right.append(n)
            n = n.right or n.left
        for x in reversed(right):
            out.append(x.val)
            st[x] = "found"
            W.step(f"Right edge, coming up: {x.val}.", T(root, {**st, x: "active"}), Row(out, label="outline"))
    assert out == exp
    return W.save()



@run
def view_from_above(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Give each node a column (left child −1, right child +1) and keep the first node a BFS meets in each column.")
    col = {id(root): 0}
    top = {}
    for floor in lvl(root):
        for n in floor:
            for c, d in ((n.left, -1), (n.right, 1)):
                if c:
                    col[id(c)] = col[id(n)] + d
        new = [n for n in floor if col[id(n)] not in top]
        for n in new:
            top[col[id(n)]] = n
        hidden = [n for n in floor if n not in new]
        W.step(("New columns seen: " + ", ".join(f"{n.val} (column {col[id(n)]})" for n in new) if new else "No new columns on this floor") +
               (f". Hidden below: {', '.join(str(n.val) for n in hidden)}." if hidden else "."),
               T(root, {**{n: "answer" for n in top.values()}, **{n: "dim" for n in hidden}}, {n: col[id(n)] for n in bfs_nodes(root) if id(n) in col}))
    out = [top[c].val for c in sorted(top)]
    W.step("Read the visible nodes from the leftmost column to the rightmost: " + str(out) + ".", T(root, {n: "answer" for n in top.values()}), result=out)
    assert out == exp
    return W.save()


@run
def right_side_view(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Go floor by floor; the last node on each floor is the one seen from the right.")
    out = []
    for floor in lvl(root):
        out.append(floor[-1].val)
        W.step(f"Floor {', '.join(str(n.val) for n in floor)}: the rightmost is {floor[-1].val}.", T(root, {**{n: "active" for n in floor}, floor[-1]: "answer"}), Row(out, label="view"))
    assert out == exp
    return W.save()


@run
def column_readout(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Place each node at (column, row), then read column by column; ties in the same spot go smallest first.")
    pos = {id(root): (0, 0)}
    for n in bfs_nodes(root):
        c, r = pos[id(n)]
        if n.left:
            pos[id(n.left)] = (c - 1, r + 1)
        if n.right:
            pos[id(n.right)] = (c + 1, r + 1)
    W.step("Each node's note is its column.", T(root, nt={n: pos[id(n)][0] for n in bfs_nodes(root)}))
    cols = sorted({p[0] for p in pos.values()})
    out = []
    for c in cols:
        members = sorted((pos[id(n)][1], n.val, n) for n in bfs_nodes(root) if pos[id(n)][0] == c)
        out.append([m[1] for m in members])
        W.step(f"Column {c}: {out[-1]}.", T(root, {m[2]: "active" for m in members}, {n: pos[id(n)][0] for n in bfs_nodes(root)}), Row(out[-1], label=f"column {c}"))
    assert out == exp
    return W.save()


# ======================================================================== tree-as-graph

def bfs_rings(root, start):
    par = parents(root)
    seen, frontier, rings = {id(start)}, [start], [[start]]
    while frontier:
        nxt = []
        for x in frontier:
            for y in (x.left, x.right, par.get(id(x))):
                if y and id(y) not in seen:
                    seen.add(id(y))
                    nxt.append(y)
        frontier = nxt
        if nxt:
            rings.append(nxt)
    return rings


@run
def nodes_k_steps_away(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    s = nodes_by_val(root)[a["start"]]
    k = a["k"]
    W = Walk(pid, "Treat the tree as a graph (children and parent are neighbours) and spread out from the start one step at a time.")
    rings = bfs_rings(root, s)
    for d, ring in enumerate(rings[:k + 1]):
        done = [n for r in rings[:d] for n in r]
        W.step(f"Step {d}: " + ", ".join(str(n.val) for n in ring) + ("." if d < k else f" — these are exactly {k} steps away."),
               T(root, {**{n: "dim" for n in done}, **{n: ("answer" if d == k else "active") for n in ring}, s: "mark"}))
    out = sorted(n.val for n in rings[k]) if k < len(rings) else []
    assert out == exp
    return W.save(mark=["start"], answer="nodes")


@run
def infection_spread(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    s = nodes_by_val(root)[a["start"]]
    W = Walk(pid, "The virus moves to parents and children alike, so spread out from the start like a ripple.")
    rings = bfs_rings(root, s)
    for d, ring in enumerate(rings):
        done = [n for r in rings[:d] for n in r]
        W.step(f"Minute {d}: " + ", ".join(str(n.val) for n in ring) + " infected.", T(root, {**{n: "found" for n in done}, **{n: "active" for n in ring}, s: "mark"}))
    W.step(f"Everything is infected after {len(rings) - 1} minutes.", T(root, {n: "found" for n in bfs_nodes(root)}), result=len(rings) - 1)
    assert len(rings) - 1 == exp
    return W.save(mark=["start"])


@run
def nearest_exit(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    s = nodes_by_val(root)[a["start"]]
    W = Walk(pid, "Spread out from the start (up or down) and stop on the first ring that contains a leaf.")
    for d, ring in enumerate(bfs_rings(root, s)):
        hits = [n for n in ring if leaf(n)]
        if hits:
            best = min(hits, key=lambda n: n.val)
            W.step(f"{d} step{'s' if d != 1 else ''} away: leaves {', '.join(str(n.val) for n in hits)}. The smallest is {best.val}.", T(root, {**{n: "active" for n in ring}, best: "answer", s: "mark"}), result=best.val)
            assert best.val == exp
            break
        W.step(f"{d} step{'s' if d != 1 else ''} away: " + ", ".join(str(n.val) for n in ring) + ", no exits.", T(root, {**{n: "active" for n in ring}, s: "mark"}))
    return W.save(mark=["start"], answer="nodes")


# ======================================================================== any-path-sums

def prefix_walk(W, root, on_node):
    """DFS keeping the current root path; on_node(node, path, sums) -> text."""
    stack = [(root, [root])]
    while stack:
        n, path = stack.pop()
        text = on_node(n, path)
        if text:
            W.step(text, T(root, {**{m: "found" for m in path[:-1]}, n: "active"}))
        for c in (n.right, n.left):
            if c:
                stack.append((c, path + [c]))


@run
def downward_paths_to_target(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    t = a["target"]
    W = Walk(pid, f"Keep the prefix sums of the current root path. A path ending here sums to {t} once for each earlier prefix equal to (current − {t}).")
    total = [0]

    def on(n, path):
        sums = [0]
        for m in path:
            sums.append(sums[-1] + m.val)
        cur = sums[-1]
        hits = [i for i in range(len(sums) - 1) if sums[i] == cur - t]
        total[0] += len(hits)
        if hits:
            starts = [path[i].val for i in hits]
            return f"At {n.val}, the prefix is {cur}; {cur - t} appeared {len(hits)} time{'s' if len(hits) > 1 else ''} above, so path{'s' if len(hits) > 1 else ''} starting at {', '.join(map(str, starts))} end here. Total {total[0]}."
        return f"At {n.val}, the prefix is {cur}; no earlier prefix equals {cur - t}."

    prefix_walk(W, root, on)
    assert total[0] == exp
    return W.save()


@run
def longest_path_to_target(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    t = a["target"]
    W = Walk(pid, f"Remember where each prefix sum FIRST appears on the root path; the earliest match gives the longest path to {t}.")
    best = [0]

    def on(n, path):
        sums = [0]
        for m in path:
            sums.append(sums[-1] + m.val)
        cur = sums[-1]
        first = next((i for i in range(len(sums) - 1) if sums[i] == cur - t), None)
        if first is not None:
            length = len(path) - first
            best[0] = max(best[0], length)
            return f"At {n.val}, a path of {length} node{'s' if length > 1 else ''} from {path[first].val} sums to {t}. Longest: {best[0]}."
        return f"At {n.val}: no path ending here sums to {t}."

    prefix_walk(W, root, on)
    assert best[0] == exp
    return W.save()


@run
def paths_divisible_by_k(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    k = a["k"]
    W = Walk(pid, f"Two prefix sums with the same remainder mod {k} bracket a path whose sum is divisible by {k}.")
    total = [0]

    def on(n, path):
        sums = [0]
        for m in path:
            sums.append(sums[-1] + m.val)
        r = sums[-1] % k
        hits = [i for i in range(len(sums) - 1) if sums[i] % k == r]
        total[0] += len(hits)
        return f"At {n.val}, the prefix leaves remainder {r}; {len(hits)} earlier prefix{'es' if len(hits) != 1 else ''} match. Total {total[0]}."

    prefix_walk(W, root, on)
    assert total[0] == exp
    return W.save()


# ======================================================================== pointer-rewiring

@run
def straighten_a_search_tree(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Visit nodes in order (smallest first) and link each one onto the end of a growing chain.")
    order = inorder(root)
    W.step("In-order visits the values from smallest to largest: " + ", ".join(str(n.val) for n in order) + ".", T(root, nt={n: i + 1 for i, n in enumerate(order)}))
    vals = []
    for n in order:
        vals.append(n.val)
        W.step(f"Link {n.val} onto the chain and clear its left pointer.", L(vals, st={len(vals) - 1: "new"}, label="chain"))
    head = None
    for v in reversed(vals):
        head = Node(v, None, head)
    assert level_of(head) == exp
    W.step("Done: a right-leaning chain in increasing order.", T(head, {n: "found" for n in bfs_nodes(head)}))
    return W.save()


@run
def upside_down_tree(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Walk down the left edge. Each node takes its old right sibling as its left child and its old parent as its right child.")
    W.step("The left edge: " + " → ".join(str(n.val) for n in _left_edge(root)) + ".", T(root, {n: "active" for n in _left_edge(root)}))
    node, prev, prev_right = root, None, None
    snap = []
    while node:
        nxt, right = node.left, node.right
        node.left, node.right = prev_right, prev
        snap.append(node)
        prev, prev_right = node, right
        node = nxt
        W.step(f"{prev.val} now has {prev.left.val if prev.left else 'nothing'} on its left and {prev.right.val if prev.right else 'nothing'} on its right.", T(prev, {prev: "new"}, label="rewired so far"))
    assert level_of(prev) == exp
    W.step(f"{prev.val} is the new root.", T(prev, {prev: "answer"}))
    return W.save()




@run
def running_totals_from_the_top(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Walk right → node → left (largest first) with a running total, writing the total into each node.")
    order = list(reversed(inorder(root)))
    total = 0
    done = []
    for n in order:
        total += n.val
        n.val = total
        done.append(n)
        W.step(f"Running total {total}: write it into this node.", T(root, {**{m: "found" for m in done[:-1]}, n: "new"}))
    assert level_of(root) == exp
    return W.save()


# ======================================================================== build-serialize

def partial_tree(built):
    """built: dict id->Node of created nodes with links; returns the root (first created)."""
    return built


@run
def rebuild_from_pre_and_in(pid):
    a, exp = example(pid)
    pre, ino = a["preorder"], a["inorder"]
    W = Walk(pid, "The next pre-order value is always a root; its place in the in-order list splits its left and right subtrees.")
    at = {v: i for i, v in enumerate(ino)}
    pos = [0]
    root_ref = [None]

    def build(lo, hi):
        if lo > hi:
            return None
        v = pre[pos[0]]
        pos[0] += 1
        n = Node(v)
        if root_ref[0] is None:
            root_ref[0] = n
        W.step(f"Next in pre-order: {v}. In the in-order list it sits at {at[v]}: positions {lo}–{at[v] - 1} go left, {at[v] + 1}–{hi} go right.",
               Row(pre, st={**{i: "dim" for i in range(pos[0] - 1)}, pos[0] - 1: "active"}, label="preorder"),
               Row(ino, st={**{i: "found" for i in range(lo, at[v])}, at[v]: "active", **{i: "mark" for i in range(at[v] + 1, hi + 1)}}, label="inorder"),
               T(root_ref[0], {n: "new"}))
        n.left = build(lo, at[v] - 1)
        n.right = build(at[v] + 1, hi)
        return n

    r = build(0, len(ino) - 1)
    assert level_of(r) == exp
    W.step("Every value is placed.", T(r, {n: "found" for n in bfs_nodes(r)}))
    return W.save()


@run
def rebuild_from_in_and_post(pid):
    a, exp = example(pid)
    ino, post = a["inorder"], a["postorder"]
    W = Walk(pid, "Read post-order from the back: each value is a root, and the right subtree comes before the left.")
    at = {v: i for i, v in enumerate(ino)}
    pos = [len(post) - 1]
    root_ref = [None]

    def build(lo, hi):
        if lo > hi:
            return None
        v = post[pos[0]]
        pos[0] -= 1
        n = Node(v)
        if root_ref[0] is None:
            root_ref[0] = n
        W.step(f"Next from the back of post-order: {v}. In-order positions {lo}–{at[v] - 1} are its left subtree and {at[v] + 1}–{hi} its right.",
               Row(post, st={**{i: "dim" for i in range(pos[0] + 2, len(post))}, pos[0] + 1: "active"}, label="postorder"),
               Row(ino, st={**{i: "found" for i in range(lo, at[v])}, at[v]: "active", **{i: "mark" for i in range(at[v] + 1, hi + 1)}}, label="inorder"),
               T(root_ref[0], {n: "new"}))
        n.right = build(at[v] + 1, hi)
        n.left = build(lo, at[v] - 1)
        return n

    r = build(0, len(ino) - 1)
    assert level_of(r) == exp
    W.step("Every value is placed.", T(r, {n: "found" for n in bfs_nodes(r)}))
    return W.save()


@run
def rebuild_from_pre_and_post(pid):
    a, exp = example(pid)
    pre, post = a["preorder"], a["postorder"]
    W = Walk(pid, "pre-order gives each root; the next pre-order value is its first child, and that child's place in post-order says where its subtree ends.")
    at = {v: i for i, v in enumerate(post)}
    pos = [0]
    root_ref = [None]

    def build(lo, hi):
        v = pre[pos[0]]
        pos[0] += 1
        n = Node(v)
        if root_ref[0] is None:
            root_ref[0] = n
        if lo < hi:
            m = at[pre[pos[0]]]
            W.step(f"{v} is a root. Its first child is {pre[pos[0]]}, whose subtree ends at post-order position {m}.",
                   Row(pre, st={**{i: "dim" for i in range(pos[0] - 1)}, pos[0] - 1: "active", pos[0]: "mark"}, label="preorder"),
                   Row(post, st={**{i: "found" for i in range(lo, m + 1)}, hi: "active"}, label="postorder"), T(root_ref[0], {n: "new"}))
            n.left = build(lo, m)
            if m + 1 <= hi - 1:
                n.right = build(m + 1, hi - 1)
        else:
            W.step(f"{v} is a leaf.", Row(pre, st={**{i: "dim" for i in range(pos[0] - 1)}, pos[0] - 1: "active"}, label="preorder"), Row(post, st={hi: "active"}, label="postorder"), T(root_ref[0], {n: "new"}))
        return n

    r = build(0, len(post) - 1)
    assert level_of(r) == exp
    return W.save()


@run
def tree_from_brackets(pid):
    a, exp = example(pid)
    s = a["s"]
    W = Walk(pid, "A stack holds the nodes whose brackets are still open; each new number becomes the top's next child.")
    stack, root, i = [], None, 0
    left_done = set()
    while i < len(s):
        c = s[i]
        if c == "(":
            if s[i + 1] == ")":
                left_done.add(id(stack[-1]))
                i += 2
                continue
            i += 1
        elif c == ")":
            stack.pop()
            i += 1
        else:
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            n = Node(int(s[i:j]))
            side = None
            if stack:
                top = stack[-1]
                if id(top) not in left_done:
                    top.left = n
                    left_done.add(id(top))
                    side = f"left child of {top.val}"
                else:
                    top.right = n
                    side = f"right child of {top.val}"
            else:
                root = n
                side = "the root"
            stack.append(n)
            W.step(f"Read {n.val}: it's {side}.", Row(list(s), st={k: "found" for k in range(i)} | {k: "active" for k in range(i, j)}, label="s"), T(root, {n: "new"}))
            i = j
    assert level_of(root) == exp
    return W.save()


@run
def tree_to_brackets(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Write each node, then its children in brackets. Keep \"()\" only when a missing left child is followed by a right child.")
    out = []

    def go(n):
        out.append(str(n.val))
        W.step(f"Write {n.val}.", T(root, {n: "active"}), Vars(so_far="".join(out)))
        if n.left or n.right:
            out.append("(")
            if n.left:
                go(n.left)
            else:
                W.step(f"{n.val} has a right child but no left one: write \"()\".", T(root, {n: "active"}), Vars(so_far="".join(out) + ")"))
            out.append(")")
        if n.right:
            out.append("(")
            go(n.right)
            out.append(")")

    go(root)
    res = "".join(out)
    W.step(f"Result: {res}", T(root), result=res)
    assert res == exp
    return W.save()


# ======================================================================== tree-shape

@run
def flip_the_tree(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Swap every node's two children. The order doesn't matter, as long as each node is swapped once.")
    for n in bfs_nodes(root):
        if n.left or n.right:
            n.left, n.right = n.right, n.left
            W.step(f"Swap the children of {n.val}.", T(root, {n: "active", **{c: "new" for c in (n.left, n.right) if c}}))
    assert level_of(root) == exp
    W.step("Every level now reads backwards.", T(root, {n: "found" for n in bfs_nodes(root)}))
    return W.save()


def pair_walk(W, a, b, pairs, label_a, label_b, check):
    for x, y in pairs:
        ok, text = check(x, y)
        W.step(text, T(a[0], {x: "active" if ok else "mark"} if x else {}, label=label_a), T(b[0], {y: "active" if ok else "mark"} if y else {}, label=label_b))
        if not ok:
            return False
    return True


@run
def twin_trees(pid):
    a, exp = example(pid)
    ra, rb = tree(a["a"]), tree(a["b"])
    W = Walk(pid, "Compare the trees position by position: both nodes must exist and hold the same value.")
    stack, ok = [(ra, rb)], True
    while stack:
        x, y = stack.pop()
        if not x and not y:
            continue
        same = bool(x and y and x.val == y.val)
        W.step(f"{x.val if x else 'nothing'} vs {y.val if y else 'nothing'}: {'match' if same else 'different'}.", T(ra, {x: "found" if same else "mark"} if x else {}, label="a"), T(rb, {y: "found" if same else "mark"} if y else {}, label="b"))
        if not same:
            ok = False
            break
        stack += [(x.right, y.right), (x.left, y.left)]
    W.step("The trees are identical." if ok else "They differ.", T(ra, label="a"), T(rb, label="b"), result=ok)
    assert ok == exp
    return W.save()


@run
def mirror_image_check(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Compare the left half with the right half as mirror images: outer with outer, inner with inner.")
    stack, ok = [(root.left, root.right)], True
    while stack:
        x, y = stack.pop()
        if not x and not y:
            continue
        same = bool(x and y and x.val == y.val)
        W.step(f"{x.val if x else 'nothing'} mirrors {y.val if y else 'nothing'}: {'match' if same else 'no match'}.", T(root, {**({x: "found" if same else "mark"} if x else {}), **({y: "found" if same else "mark"} if y else {})}))
        if not same:
            ok = False
            break
        stack += [(x.right, y.left), (x.left, y.right)]
    W.step("Symmetric." if ok else "Not symmetric.", T(root), result=ok)
    assert ok == exp
    return W.save()


@run
def hidden_branch(pid):
    a, exp = example(pid)
    root, br = tree(a["root"]), tree(a["branch"])
    W = Walk(pid, "Try each node of the big tree as a starting point and compare the whole subtree below it with the branch.")

    def same(x, y):
        if not x and not y:
            return True
        if not x or not y or x.val != y.val:
            return False
        return same(x.left, y.left) and same(x.right, y.right)

    found = False
    for n in preorder(root):
        ok = same(n, br)
        W.step(f"Start at {n.val}: " + ("its whole subtree matches the branch." if ok else ("the values differ." if n.val != br.val else "the shapes differ below it.")),
               T(root, {m: ("answer" if ok else "active") for m in preorder(n)} if ok else {n: "active"}, label="root"), T(br, label="branch"))
        if ok:
            found = True
            break
    assert found == exp
    return W.save()


@run
def flip_equivalent(pid):
    a, exp = example(pid)
    ra, rb = tree(a["a"]), tree(a["b"])
    W = Walk(pid, "Match nodes pairwise; at each pair, line the children up straight or crossed, whichever makes the values agree.")
    stack, ok = [(ra, rb)], True
    while stack:
        x, y = stack.pop()
        if not x and not y:
            continue
        if not x or not y or x.val != y.val:
            ok = False
            W.step(f"{x.val if x else 'nothing'} vs {y.val if y else 'nothing'}: no match.", T(ra, {x: "mark"} if x else {}, label="a"), T(rb, {y: "mark"} if y else {}, label="b"))
            break
        xl = x.left.val if x.left else None
        yl = y.left.val if y.left else None
        crossed = xl != yl
        W.step(f"{x.val} matches. Its children line up {'crossed: flip here' if crossed else 'straight'}.", T(ra, {x: "found"}, label="a"), T(rb, {y: "found"}, label="b"))
        if crossed:
            stack += [(x.left, y.right), (x.right, y.left)]
        else:
            stack += [(x.left, y.left), (x.right, y.right)]
    W.step("Every pair matched, so the trees are flip-equivalent." if ok else "Not flip-equivalent.", T(ra, label="a"), T(rb, label="b"), result=ok)
    assert ok == exp
    return W.save()


# ======================================================================== tree-dp

@run
def orchard_heist(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each tree reports two numbers: the best total if it's picked, and the best if it isn't.")

    def comp(n, l, r):
        lt, ls = l or (0, 0)
        rt, rs = r or (0, 0)
        return (n.val + ls + rs, max(lt, ls) + max(rt, rs))

    val = post_walk(W, root, comp, lambda n, v: f"{n.val}: picked gives {v[0]} (its children skipped), skipped gives {v[1]} (its children free). Notes show picked/skipped.",
                    note=lambda v: f"{v[0]}/{v[1]}")
    best = max(val[id(root)])
    W.step(f"The root's better option: {best}.", T(root, nt={m: f"{val[id(m)][0]}/{val[id(m)][1]}" for m in bfs_nodes(root)}), result=best)
    assert best == exp
    return W.save()


@run
def coin_moves(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node reports its branch's surplus (coins − nodes). That many coins must cross the edge above it.")
    moves = [0]

    def comp(n, l, r):
        moves[0] += abs(l or 0) + abs(r or 0)
        return n.val - 1 + (l or 0) + (r or 0)

    post_walk(W, root, comp, lambda n, e: f"{n.val}'s branch has a surplus of {e}: {abs(e)} coin{'s' if abs(e) != 1 else ''} cross the edge above it{' (going up)' if e > 0 else ' (coming down)' if e < 0 else ''}. Moves so far: {moves[0]}.")
    W.step(f"Total moves: {moves[0]}.", T(root), result=moves[0])
    assert moves[0] == exp
    return W.save()


@run
def longest_zigzag_walk(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Carry, into each node, the length of the zigzag that arrives there: turning extends it by 1, going the same way starts over at 1.")
    best, length, seen = 0, {}, []
    stack = [(root, 0, 0)]
    while stack:
        n, came, ln = stack.pop()
        length[id(n)] = ln
        best = max(best, ln)
        seen.append(n)
        how = "the start" if n is root else ("a turn, so the zigzag grows" if ln > 1 else "a first step, or the same direction twice, so it starts at 1")
        W.step(f"Arrive by {how}: length {ln}. Longest {best}.", T(root, {**{m: "found" for m in seen[:-1]}, n: "active"}, {m: length[id(m)] for m in seen}))
        if n.right:
            stack.append((n.right, 1, ln + 1 if came == -1 else 1))
        if n.left:
            stack.append((n.left, -1, ln + 1 if came == 1 else 1))
    W.step(f"The longest zigzag has {best} edges.", T(root, {m: ("answer" if length[id(m)] == best else "") for m in seen}, {m: length[id(m)] for m in seen}), result=best)
    assert best == exp
    return W.save()



@run
def fewest_cameras(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Settle rooms from the bottom up: put a camera on a room only when one of its children is left unwatched.")
    state, cams = {}, 0
    names = {0: "unwatched", 1: "camera", 2: "watched"}
    for n in postorder(root):
        kids = [state[id(c)] for c in (n.left, n.right) if c]
        if 0 in kids:
            state[id(n)] = 1
            cams += 1
            why = "a child is unwatched, so put a camera here"
        elif 1 in kids:
            state[id(n)] = 2
            why = "a child has a camera, so this room is watched"
        else:
            state[id(n)] = 0
            why = "nothing below watches it yet: leave it for its parent"
        st = {m: {0: "mark", 1: "answer", 2: "found"}[state[id(m)]] for m in bfs_nodes(root) if id(m) in state}
        where = "a leaf" if leaf(n) else ("the top room" if n is root else "a room above")
        W.step(f"Next, {where}: {why}.", T(root, st))
    if state[id(root)] == 0:
        cams += 1
        state[id(root)] = 1
        W.step("The root is still unwatched, so it gets a camera too.", T(root, {m: {0: "mark", 1: "answer", 2: "found"}[state[id(m)]] for m in bfs_nodes(root)}))
    W.step(f"Cameras used: {cams}.", T(root, {m: {0: "mark", 1: "answer", 2: "found"}[state[id(m)]] for m in bfs_nodes(root)}), result=cams)
    assert cams == exp
    return W.save()


# ======================================================================== binary-lifting

def parent_tree(parent):
    return [{"id": i, "label": str(i), "parent": (p if p != -1 else None)} for i, p in enumerate(parent)]


@run
def ancestor_jumps(pid):
    a, exp = example(pid)
    parent = a["parent"]
    n = len(parent)
    up = [parent[:]]
    while (1 << len(up)) <= n:
        prev = up[-1]
        up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])
    W = Walk(pid, "Precompute each person's 1st, 2nd, 4th, … ancestor; any k-th ancestor is then a few jumps.")
    W.step("up[j][v] is v's 2^j-th ancestor. The notes show each person's 2nd ancestor (up[1]).", NT(parent_tree(parent), nt={v: up[1][v] if len(up) > 1 and up[1][v] != -1 else "–" for v in range(n)}))
    out = []
    for v0, k in a["queries"]:
        v, j, hops = v0, 0, []
        kk = k
        while kk and v != -1:
            if kk & 1:
                v = up[j][v] if j < len(up) else -1
                hops.append(f"2^{j}")
            kk >>= 1
            j += 1
        out.append(v)
        W.step(f"Query [{v0}, {k}]: k = {k} is {' + '.join(hops) if hops else '0'}, so jump that way. " + (f"Answer {v}." if v != -1 else "That passes the root: -1."),
               NT(parent_tree(parent), {**{v0: "mark"}, **({v: "answer"} if v != -1 else {})}), result=v)
    assert out == exp
    return W.save()


@run
def shared_ancestor_queries(pid):
    a, exp = example(pid)
    parent = a["parent"]
    n = len(parent)
    depth = [0] * n
    for v in range(n):
        d, x = 0, v
        while parent[x] != -1:
            x = parent[x]
            d += 1
        depth[v] = d
    W = Walk(pid, "Lift the deeper person to the same depth, then lift both together until their parents match.")
    W.step("Notes show each person's depth.", NT(parent_tree(parent), nt={v: depth[v] for v in range(n)}))
    out = []
    for u, v in a["queries"]:
        x, y = u, v
        if depth[x] < depth[y]:
            x, y = y, x
        while depth[x] > depth[y]:
            x = parent[x]
        while x != y:
            x, y = parent[x], parent[y]
        out.append(x)
        W.step(f"Query [{u}, {v}]: after evening out the depths and climbing together, they meet at {x}.", NT(parent_tree(parent), {u: "mark", v: "mark", x: "answer"}, {w: depth[w] for w in range(n)}), result=x)
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
