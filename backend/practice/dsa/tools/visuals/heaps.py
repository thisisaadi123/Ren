import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import heapq
from lib import *

DONE = []
CUSTOM = {
    "cheapest-pair-totals": [{"a": [1, 3, 8], "b": [2, 4, 9], "k": 5}],
    "running-middle": [{"readings": [5, 15, 1, 3, 8, 7, 9]}],
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


@run
def running_middle(pid):
    a, exp = example(pid)
    W = Walk(pid, "Keep the lower half in a max-heap and the upper half in a min-heap, with the lower half never smaller. The middle is the top of the lower half.")
    low, high, out = [], [], []
    for x in a["readings"]:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))
        moved = len(high) > len(low)
        if moved:
            heapq.heappush(low, -heapq.heappop(high))
        out.append(-low[0])
        W.step(f"Reading {x} arrives" + (", and the upper half's smallest moves down to keep the halves even" if moved else "") + f". Middle: {-low[0]}.",
               HP([-t for t in low], {0: "answer"}, label="lower half (max-heap)"), HP(list(high), {0: "active"}, label="upper half (min-heap)") if high else None, Row(out, st={len(out) - 1: "new"}, label="middles"), result=out if len(out) == len(a["readings"]) else None)
    assert out == exp
    return W.save()


@run
def hand_built_heap(pid):
    a, exp = example(pid)
    h = []
    W = Walk(pid, "The heap lives in an array: index i's children are 2i + 1 and 2i + 2. Push sifts a value up; pop moves the last value to the root and sifts it down.")

    def down(i):
        n = len(h)
        while True:
            m, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and h[l] < h[m]:
                m = l
            if r < n and h[r] < h[m]:
                m = r
            if m == i:
                return i
            h[i], h[m] = h[m], h[i]
            i = m

    out = []
    for c in a["calls"]:
        if c[0] == "TaskHeap":
            h = list(c[1])
            for i in range(len(h) // 2 - 1, -1, -1):
                down(i)
            out.append(None)
            W.step(f"Heapify {c[1]}: sift down every parent, last one first. The smallest reaches the root.", HP(h, {0: "found"}) if h else Vars(size=0))
        elif c[0] == "push":
            h.append(c[1])
            i = len(h) - 1
            while i and h[i] < h[(i - 1) // 2]:
                h[i], h[(i - 1) // 2] = h[(i - 1) // 2], h[i]
                i = (i - 1) // 2
            out.append(None)
            W.step(f"push({c[1]}): add it at the end and swap it up past bigger parents.", HP(h, {i: "new"}))
        elif c[0] == "pop":
            if not h:
                out.append(-1)
                W.step("pop() on an empty heap returns -1.", Vars(size=0), result=-1)
                continue
            top, last = h[0], h.pop()
            at = None
            if h:
                h[0] = last
                at = down(0)
            out.append(top)
            W.step(f"pop() returns {top}. The last value moves to the root and sinks to its place.", HP(h, {at: "new"}) if h else Vars(size=0), result=top)
        elif c[0] == "peek":
            v = h[0] if h else -1
            out.append(v)
            W.step(f"peek() reads the root: {v}.", HP(h, {0: "active"}) if h else Vars(size=0), result=v)
        else:
            out.append(len(h))
            W.step(f"size() is {len(h)}.", Vars(size=len(h)), result=len(h))
    assert out == exp
    return W.save()


if __name__ == "__main__":
    for pid, n in DONE:
        print(f"{pid}: {n} steps")
