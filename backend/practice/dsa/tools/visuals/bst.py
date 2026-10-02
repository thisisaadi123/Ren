import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import *

DONE = []


def run(fn):
    pid = fn.__name__.replace("_", "-")
    DONE.append((pid, fn(pid)))
    return fn


def search_path(root, x):
    path, n = [], root
    while n:
        path.append(n)
        if x == n.val:
            break
        n = n.left if x < n.val else n.right
    return path


@run
def membership_register_edits(pid):
    a, exp = example(pid)
    holder = [tree(a["root"])]
    W = Walk(pid, "Each edit walks down from the root as if searching for the key.")
    W.step("The register before any edits.", T(holder[0]))
    for op, k in a["ops"]:
        path = search_path(holder[0], k)
        hit = path and path[-1].val == k
        if op == 1:
            if hit:
                W.step(f"Insert {k}: it's already there, nothing changes.", T(holder[0], {path[-1]: "mark"}))
                continue
            node = Node(k)
            if not holder[0]:
                holder[0] = node
            else:
                last = path[-1]
                if k < last.val:
                    last.left = node
                else:
                    last.right = node
            W.step(f"Insert {k}: the search falls off below {path[-1].val if path else 'the empty root'}, so {k} becomes a new leaf there.", T(holder[0], {**{n: "found" for n in path}, node: "new"}))
            continue
        if not hit:
            W.step(f"Delete {k}: it isn't in the register, nothing changes.", T(holder[0], {n: "found" for n in path}))
            continue
        target = path[-1]
        W.step(f"Delete {k}: found it.", T(holder[0], {**{n: "found" for n in path[:-1]}, target: "active"}))
        if target.left and target.right:
            succ_parent, succ = target, target.right
            while succ.left:
                succ_parent, succ = succ, succ.left
            W.step(f"{k} has two children, so it takes the key of the smallest node on its right, {succ.val}.", T(holder[0], {target: "active", succ: "mark"}))
            target.val = succ.val
            child = succ.right
            if succ_parent is target:
                succ_parent.right = child
            else:
                succ_parent.left = child
            W.step(f"Then remove the old {succ.val} node, which has at most one child.", T(holder[0], {target: "new"}))
        else:
            child = target.left or target.right
            parent = path[-2] if len(path) > 1 else None
            if parent is None:
                holder[0] = child
            elif parent.left is target:
                parent.left = child
            else:
                parent.right = child
            W.step(f"{k} has {'one child, which takes its place' if child else 'no children, so it is simply removed'}.", T(holder[0]))
    assert level_of(holder[0]) == exp
    return W.save()


@run
def next_ticket_up(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    x = a["x"]
    W = Walk(pid, f"Walk down from the root. Whenever a node is bigger than {x}, it's a candidate; then look left for a smaller one.")
    best, n = None, root
    while n:
        if n.val > x:
            best = n
            W.step(f"{n.val} > {x}: best so far is {n.val}. Go left for something smaller but still above {x}.", T(root, {n: "active", **({best: "found"} if best is not n else {})}))
            n = n.left
        else:
            W.step(f"{n.val} ≤ {x}: everything on its left is too small. Go right.", T(root, {n: "dim", **({best: "found"} if best else {})}))
            n = n.right
    res = best.val if best else -1
    W.step(f"Nothing left to check: the answer is {res}.", T(root, {best: "answer"} if best else {}), result=res)
    assert res == exp
    return W.save()


@run
def catalogue_order_check(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Pass each node the range its value must fall in. Going left lowers the upper bound; going right raises the lower bound.")
    ok, stack = True, [(root, None, None)]
    while stack:
        n, lo, hi = stack.pop()
        good = (lo is None or n.val > lo) and (hi is None or n.val < hi)
        rng = f"({'−∞' if lo is None else lo}, {'∞' if hi is None else hi})"
        W.step(f"{n.val} must be in {rng}: {'yes' if good else 'no'}.", T(root, {n: "found" if good else "mark"}, {n: rng}))
        if not good:
            ok = False
            break
        for c, l2, h2 in ((n.right, n.val, hi), (n.left, lo, n.val)):
            if c:
                stack.append((c, l2, h2))
    W.step("Every node is in its range: it's a valid search tree." if ok else "A node is out of its range: not a valid search tree.", T(root), result=ok)
    assert ok == exp
    return W.save()


@run
def richest_orderly_branch(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Each node reports (is my branch orderly, its min, its max, its sum). A branch is orderly when both sides are and left max < node < right min.")
    info, best = {}, None
    for n in postorder(root):
        L_ = info.get(id(n.left)) if n.left else (True, None, None, 0)
        R_ = info.get(id(n.right)) if n.right else (True, None, None, 0)
        ok = L_[0] and R_[0] and (L_[2] is None or L_[2] < n.val) and (R_[1] is None or n.val < R_[1])
        s = n.val + L_[3] + R_[3]
        mn = L_[1] if L_[1] is not None else n.val
        mx = R_[2] if R_[2] is not None else n.val
        info[id(n)] = (ok, mn, mx, s)
        if ok:
            best = s if best is None else max(best, s)
        W.step(f"{n.val}'s branch is {'orderly, total ' + str(s) if ok else 'not orderly'}. Best orderly total so far: {best}.",
               T(root, {**{m: ("found" if info[id(m)][0] else "dim") for m in bfs_nodes(root) if id(m) in info}, n: "active" if ok else "mark"},
                 {m: info[id(m)][3] for m in bfs_nodes(root) if id(m) in info and info[id(m)][0]}))
    W.step(f"The richest orderly branch totals {best}.", T(root), result=best)
    assert best == exp
    return W.save()


@run
def rebalance_the_catalogue(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Read the values in order (they come out sorted), then rebuild from the middle outwards.")
    vals = [n.val for n in inorder(root)]
    W.step("In-order gives the values sorted: " + ", ".join(map(str, vals)) + ".", T(root, nt={n: i for i, n in enumerate(inorder(root))}), Row(vals, label="sorted"))
    built = {}
    root_ref = [None]

    def build(lo, hi, parent=None, side=None):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        n = Node(vals[mid])
        if root_ref[0] is None:
            root_ref[0] = n
        if parent:
            setattr(parent, side, n)
        W.step(f"The middle of positions {lo}–{hi} is {vals[mid]}: it becomes {'the root' if parent is None else 'a child of ' + str(parent.val)}.",
               Row(vals, st={**{i: "found" for i in range(lo, hi + 1)}, mid: "active"}, label="sorted"), T(root_ref[0], {n: "new"}))
        build(lo, mid - 1, n, "left")
        build(mid + 1, hi, n, "right")
        return n

    r = build(0, len(vals) - 1)
    assert level_of(r) == exp
    return W.save()


@run
def balanced_shelf_index(pid):
    a, exp = example(pid)
    vals = a["codes"]
    W = Walk(pid, "The middle code becomes the root, so both sides get about the same number of codes. Repeat on each half.")
    root_ref = [None]

    def build(lo, hi, parent=None, side=None):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        n = Node(vals[mid])
        if root_ref[0] is None:
            root_ref[0] = n
        if parent:
            setattr(parent, side, n)
        W.step(f"Middle of positions {lo}–{hi}: {vals[mid]}.", Row(vals, st={**{i: "found" for i in range(lo, hi + 1)}, mid: "active"}, label="codes"), T(root_ref[0], {n: "new"}))
        build(lo, mid - 1, n, "left")
        build(mid + 1, hi, n, "right")
        return n

    r = build(0, len(vals) - 1)
    assert level_of(r) == exp
    return W.save()


@run
def chain_to_tree(pid):
    a, exp = example(pid)
    vals = a["head"]
    W = Walk(pid, "Build in in-order: the left subtree first, then take the next list node as the root, then the right subtree. Each list node is used once, in order.")
    cur = [0]
    root_ref = [None]

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        left = build(lo, mid - 1)
        n = Node(vals[cur[0]], left)
        cur[0] += 1
        if root_ref[0] is None or root_ref[0] is left:
            root_ref[0] = n
        W.step(f"Take list node {n.val} as the root of positions {lo}–{hi}" + (f", with {left.val}'s subtree on its left." if left else "."),
               L(vals, st={**{i: "dim" for i in range(cur[0] - 1)}, cur[0] - 1: "active"}, ptr={"cur": cur[0] - 1}), T(n, {n: "new"}))
        n.right = build(mid + 1, hi)
        return n

    r = build(0, len(vals) - 1)
    assert level_of(r) == exp
    W.step("All list nodes are placed.", T(r, {n: "found" for n in bfs_nodes(r)}))
    return W.save()


@run
def trim_the_price_list(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    lo, hi = a["low"], a["high"]
    W = Walk(pid, f"A node below {lo} can only keep its right side; a node above {hi} can only keep its left side.")
    W.step(f"Keep prices from {lo} to {hi}.", T(root, {n: ("found" if lo <= n.val <= hi else "dim") for n in bfs_nodes(root)}))

    def trim(n):
        if not n:
            return None
        if n.val < lo:
            W.step(f"{n.val} < {lo}: drop it and its left side, keep what its right side trims to.", T(root, {n: "mark"}))
            return trim(n.right)
        if n.val > hi:
            W.step(f"{n.val} > {hi}: drop it and its right side, keep what its left side trims to.", T(root, {n: "mark"}))
            return trim(n.left)
        n.left, n.right = trim(n.left), trim(n.right)
        return n

    r = trim(root)
    assert level_of(r) == exp
    W.step("The trimmed tree.", T(r, {n: "found" for n in bfs_nodes(r)}))
    return W.save()


@run
def archive_shelf_lookup(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "An in-order walk lists ids in increasing order, skipping whole branches that fall outside the band.")
    out = []
    for lo, hi, k in a["queries"]:
        band = [n for n in inorder(root) if lo <= n.val <= hi]
        res = band[k - 1].val if k <= len(band) else -1
        out.append(res)
        st = {n: "found" for n in band}
        if res != -1:
            st[band[k - 1]] = "answer"
        W.step(f"Query [{lo}, {hi}, {k}]: the band holds {', '.join(str(n.val) for n in band) or 'nothing'}" + (f"; the {k}-th is {res}." if res != -1 else f"; fewer than {k}, so -1."),
               T(root, st, {n: i + 1 for i, n in enumerate(band)}), result=res)
    assert out == exp
    return W.save()


@run
def harvest_in_a_band(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    lo, hi = a["low"], a["high"]
    W = Walk(pid, f"Walk the tree but skip any side that can't hold weights between {lo} and {hi}.")
    total, stack = 0, [root]
    while stack:
        n = stack.pop()
        if not n:
            continue
        if n.val < lo:
            W.step(f"{n.val} < {lo}: skip it and its whole left side.", T(root, {n: "dim"}), Vars(total=total))
            stack.append(n.right)
        elif n.val > hi:
            W.step(f"{n.val} > {hi}: skip it and its whole right side.", T(root, {n: "dim"}), Vars(total=total))
            stack.append(n.left)
        else:
            total += n.val
            W.step(f"{n.val} is in the band: add it.", T(root, {n: "found"}), Vars(total=total))
            stack += [n.right, n.left]
    W.step(f"Total: {total}.", T(root, {n: "found" for n in bfs_nodes(root) if lo <= n.val <= hi}), result=total)
    assert total == exp
    return W.save()


@run
def audio_guide_steps(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "Keep a stack of the path to the next exhibit: push the left edge, and after each visit push the left edge of the right child.")
    stack = []

    def push_left(n):
        while n:
            stack.append(n)
            n = n.left

    push_left(root)
    W.step("Start by pushing the left edge from the root.", T(root, {n: "found" for n in stack}), Row([n.val for n in stack], label="stack"))
    out = []
    for op in a["ops"]:
        if op == "next":
            n = stack.pop()
            push_left(n.right)
            out.append(n.val)
            W.step(f"next: pop {n.val}" + (f", then push the left edge of {n.right.val}." if n.right else "."), T(root, {**{m: "found" for m in stack}, n: "answer"}), Row([m.val for m in stack], label="stack"), call="next", result=n.val)
        else:
            out.append(1 if stack else 0)
            W.step("hasNext: is the stack non-empty?", T(root, {m: "found" for m in stack}), Row([m.val for m in stack], label="stack"), call="hasNext", result=out[-1])
    assert out == exp
    return W.save()


@run
def two_misplaced_keys(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    W = Walk(pid, "In-order should be increasing. The swapped keys show up as the places where it goes down.")
    order = inorder(root)
    vals = [n.val for n in order]
    drops = [i for i in range(len(vals) - 1) if vals[i] > vals[i + 1]]
    W.step("In-order reads " + ", ".join(map(str, vals)) + ".", T(root), Row(vals, st={i: "mark" for d in drops for i in (d, d + 1)}, label="in-order"))
    first, second = order[drops[0]], order[drops[-1] + 1]
    W.step(f"The first drop's larger key ({first.val}) and the last drop's smaller key ({second.val}) are the swapped pair.", T(root, {first: "mark", second: "mark"}), Row(vals, st={drops[0]: "active", drops[-1] + 1: "active"}, label="in-order"))
    first.val, second.val = second.val, first.val
    assert level_of(root) == exp
    W.step("Swap them back.", T(root, {first: "new", second: "new"}), Row([n.val for n in order], label="in-order"))
    return W.save()


@run
def crate_pairs_by_weight(pid):
    a, exp = example(pid)
    root = tree(a["root"])
    t = a["target"]
    W = Walk(pid, f"Read the weights in order and squeeze two pointers inward, looking for pairs that add up to {t}.")
    order = inorder(root)
    vals = [n.val for n in order]
    i, j, count = 0, len(vals) - 1, 0
    while i < j:
        s = vals[i] + vals[j]
        if s == t:
            count += 1
            W.step(f"{vals[i]} + {vals[j]} = {t}: a pair. Pairs: {count}.", T(root, {order[i]: "answer", order[j]: "answer"}), Row(vals, ptr={"lo": i, "hi": j}, label="in order"))
            i += 1
            j -= 1
        elif s < t:
            W.step(f"{vals[i]} + {vals[j]} = {s} < {t}: move lo up.", T(root, {order[i]: "active", order[j]: "active"}), Row(vals, ptr={"lo": i, "hi": j}, label="in order"))
            i += 1
        else:
            W.step(f"{vals[i]} + {vals[j]} = {s} > {t}: move hi down.", T(root, {order[i]: "active", order[j]: "active"}), Row(vals, ptr={"lo": i, "hi": j}, label="in order"))
            j -= 1
    W.step(f"The pointers met: {count} pairs.", T(root), result=count)
    assert count == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
