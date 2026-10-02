import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import heapq
from lib import *

DONE = []
CUSTOM = {
    "cheapest-pair-totals": [{"a": [1, 3, 8], "b": [2, 4, 9], "k": 5}],
}
run = make_runner(DONE, CUSTOM)


def HP(arr, st=None, label="heap"):
    """A heap drawn as the complete tree it is: index i has children 2i + 1 and 2i + 2."""
    p = {"type": "tree", "tree": list(arr), "label": label}
    if st:
        p["states"] = {str(i): s for i, s in st.items() if s and 0 <= i < len(arr)}
    return p


@run
def smash_the_boulders(pid):
    a, exp = example(pid)
    h = [-w for w in a["boulders"]]
    heapq.heapify(h)
    W = Walk(pid, "Keep the boulders in a max-heap: the heaviest sits at the top, so each turn is two pops and maybe one push.")
    W.step("Heapify the weights; the heaviest is at the root.", HP([-x for x in h], {0: "active"}))
    while len(h) > 1:
        x, y = -heapq.heappop(h), -heapq.heappop(h)
        if x != y:
            heapq.heappush(h, -(x - y))
            v = [-t for t in h]
            W.step(f"Smash {x} and {y}: a {x - y} goes back in.", HP(v, {v.index(x - y): "new"}), Vars(left=len(h)))
        else:
            W.step(f"Smash {x} and {y}: both are destroyed.", HP([-t for t in h]) if h else Vars(left=0), Vars(left=len(h)))
    res = -h[0] if h else 0
    W.step(f"Last boulder: {res}." if h else "Nothing is left: 0.", HP([res], {0: "answer"}) if h else None, result=res)
    assert res == exp
    return W.save()


@run
def cheapest_pair_totals(pid):
    a, exp = example(pid)
    A, B, k = a["a"], a["b"], a["k"]
    W = Walk(pid, "Row i is a[i] + b[0], a[i] + b[1], … and is already sorted. Merge the rows with a min-heap of their fronts, opening a new row only when the previous row's first pair is used.")
    grid = [[x + y for y in B] for x in A]
    h = [(A[0] + B[0], 0, 0)]
    out, used = [], set()
    W.step("Every combo price, as a grid (mains down, sides across). Start with the top-left pair.", Grid(grid, {(0, 0): "active"}, label="a[i] + b[j]"))
    while len(out) < k:
        s, i, j = heapq.heappop(h)
        out.append(s)
        used.add((i, j))
        if j + 1 < len(B):
            heapq.heappush(h, (A[i] + B[j + 1], i, j + 1))
        if j == 0 and i + 1 < len(A):
            heapq.heappush(h, (A[i + 1] + B[0], i + 1, 0))
        st = {p: "found" for p in used}
        st[(i, j)] = "answer"
        st.update({(r, c): "active" for _, r, c in h})
        W.step(f"Pop {s} (main {A[i]} + side {B[j]}). The heap now holds the next candidates: {sorted(t[0] for t in h)}.", Grid(grid, st, label="a[i] + b[j]"), Row(out, label="cheapest so far"), result=out if len(out) == k else None)
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
