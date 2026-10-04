"""In-depth text for the monotonic-deque problems (merged into their sol() calls via sol.EXTRA)."""
from collections import deque

from sol import EXTRA, table

DEQUE = """
**The monotonic deque.** For a sliding window's maximum, an element that is **older and not larger** than a newer one
can never be the maximum again: the newer one is at least as large and stays in the window longer. So keep a deque of
indices whose values **decrease** from front to back:

- **back:** before adding an element, pop smaller-or-equal elements from the back (they're dominated);
- **front:** pop the front when it falls out of the window;
- the **front** is always the current window's maximum.

Each index enters and leaves the deque once: O(n) total. Storing indices (not values) is what lets us tell when the
front has left the window.
"""

# ---------------------------------------------------------------- window-peaks
temps, k = [3, 1, -2, 5, 4, 2, 0, 6], 3
dq, out, wrows = deque(), [], []
for i, v in enumerate(temps):
    dropped = []
    while dq and temps[dq[-1]] <= v:
        dropped.append(temps[dq.pop()])
    dq.append(i)
    expired = None
    if dq[0] <= i - k:
        expired = temps[dq.popleft()]
    peak = temps[dq[0]] if i >= k - 1 else "—"
    if i >= k - 1:
        out.append(temps[dq[0]])
    wrows.append((i, v, dropped or "—", expired if expired is not None else "—", [temps[x] for x in dq], peak))
EXTRA["window-peaks"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 1`: every reading is its own peak.
        - `k = n`: one window, the overall maximum.
        - Equal readings: keep the newer one (it stays longer).
        """
    ],
    "think": [
        DEQUE,
        f"**Trace on `{temps}`, k = {k}:**",
        table(["hour", "reading", "dropped from back", "expired from front", "deque values", "peak"], *wrows),
        f"Peaks: **{out}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan each window of `k` readings for its maximum."],
            "build": ["For each window, scan its `k` readings.", "Record the maximum."],
            "complexity": ["**Time O(n · k).** **Space O(1)** besides the output."],
            "limits": ["Neighbouring windows share `k − 1` readings but each is rescanned."],
        },
        1: {
            "idea": [
                """
                Cut the readings into blocks of `k`. Precompute running maxima from each block's start forward and from each
                block's end backward. A window spans at most two blocks, so its maximum is
                `max(to_end[i], from_start[i + k − 1])`.
                """
            ],
            "build": ["Forward maxima restarting at each block.", "Backward maxima restarting at each block.", "Combine the two for each window."],
            "complexity": ["**Time O(n).** **Space O(n)** for the two arrays."],
            "limits": ["Correct and linear, but needs two extra arrays and the whole input up front; the deque works on a stream with O(k) memory."],
        },
        2: {
            "idea": ["Monotonic deque of indices (values decreasing): pop dominated elements from the back, expire the front, and read the front as the peak once the first window is full."],
            "build": ["Empty deque.", "Pop smaller-or-equal from the back; push.", "Expire the front.", "Record the front's value."],
            "complexity": ["**Time O(n).** **Space O(k).**"],
        },
    },
    "takeaways": [
        """
        - **Sliding window maximum:** monotonic deque of indices.
        - Pop from the back when dominated, from the front when expired.
        - **Pitfall:** storing values instead of indices (can't tell when the front leaves the window).
        """
    ],
}


# ---------------------------------------------------------------- stepping-stones-score
stones, sk = [2, -5, -3, 4, -6, -1, 3], 2
n = len(stones)
best = [0] * n
best[0] = stones[0]
dq = deque([0])
srows = [(0, stones[0], "start", best[0], [best[x] for x in dq])]
for i in range(1, n):
    if dq[0] < i - sk:
        dq.popleft()
    src = dq[0]
    best[i] = stones[i] + best[src]
    while dq and best[dq[-1]] <= best[i]:
        dq.pop()
    dq.append(i)
    srows.append((i, stones[i], f"best reachable predecessor: stone {src} ({best[src]})", best[i], [best[x] for x in dq]))
EXTRA["stepping-stones-score"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One stone: its value is the score.
        - All negative stones: you still must land on the first and last; minimise the damage in between.
        - `k ≥ n`: jump straight from the first stone to the last.
        """
    ],
    "think": [
        """
        **Dynamic programming.** Let `best[i]` be the highest score ending on stone `i`. You arrive at `i` from one of the
        previous `k` stones, so `best[i] = stones[i] + max(best[i−k … i−1])`. Greedy choices (always jumping to the best
        nearby stone) can fail; the DP considers every way to arrive.

        **The bottleneck** is the maximum over the last `k` values, recomputed for every stone. That's a **sliding window
        maximum** over the `best` array.
        """,
        DEQUE,
        f"**Trace on `{stones}`, k = {sk}:**",
        table(["stone", "value", "comes from", "best[i]", "deque (best values)"], *srows),
        f"Highest score **{best[-1]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Fill `best[i]` by scanning back over the previous `k` stones for the largest `best`."],
            "build": ["`best[0] = stones[0]`.", "For each stone, scan back up to `k` stones.", "Add the stone's value to the best found."],
            "complexity": ["**Time O(n · k):** 10¹⁰ for the largest inputs. **Space O(n).**"],
            "limits": ["The back-scan is a sliding window maximum recomputed from scratch each time."],
        },
        1: {
            "idea": [
                """
                Same DP, but keep a monotonic deque of indices with decreasing `best` values over the last `k` stones. The
                front is the best predecessor; expire it when it's more than `k` back; after computing `best[i]`, pop
                dominated entries from the back and push `i`.
                """
            ],
            "build": ["`best[0]` and deque `[0]`.", "Expire the front if too far.", "`best[i] = stones[i] + best[front]`.", "Pop dominated entries; push `i`."],
            "complexity": ["**Time O(n).** **Space O(n)** for `best` (the deque holds at most `k`)."],
        },
    },
    "takeaways": [
        """
        - **DP over a window of previous states:** speed up the max (or min) with a monotonic deque.
        - "Jump 1 to k steps" means "take the best of the last k states".
        - **Pitfall:** greedy jumps to the best nearby stone, which can lead into a worse stretch later.
        """
    ],
}


# ---------------------------------------------------------------- shortest-net-gain
ch, tg = [4, -6, 3, 2, -1, 4, 1], 6
P = [0]
for v in ch:
    P.append(P[-1] + v)
dq, bestlen, grows = deque(), len(ch) + 1, []
for j in range(len(P)):
    found = []
    while dq and P[j] - P[dq[0]] >= tg:
        i = dq.popleft()
        bestlen = min(bestlen, j - i)
        found.append(f"start {i}: gain {P[j] - P[i]}, length {j - i}")
    dropped = []
    while dq and P[dq[-1]] >= P[j]:
        dropped.append(dq.pop())
    dq.append(j)
    grows.append((j, P[j], "; ".join(found) or "—", dropped or "—", " ".join(f"{x}:{P[x]}" for x in dq), bestlen if bestlen <= len(ch) else "—"))
EXTRA["shortest-net-gain"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative changes: a sliding window doesn't work (shrinking can increase the sum).
        - No run reaches the target: −1.
        - A single day may already reach the target.
        """
    ],
    "think": [
        f"""
        **Prefix sums.** With `P[j]` = sum of the first `j` changes, a run from day `i` to day `j − 1` gains `P[j] − P[i]`.
        We want the smallest `j − i` with `P[j] − P[i] ≥ target`. For `{ch}`: `P = {P}`.

        **Two observations about candidate starts `i`:**

        1. If a later index `j'` has `P[j'] ≤ P[i]`, start `i` is useless from then on: `j'` is a later start (shorter
           runs) with a smaller prefix (more gain). So keep starts with **increasing** prefix sums (pop the back).
        2. Once start `i` has found an end `j` that works, any later end would only make a longer run from `i`. So pop it
           from the **front** after recording.

        Together this is a monotonic deque over prefix-sum indices.
        """,
        f"**Trace for target {tg}:**",
        table(["j", "P[j]", "runs found (front pops)", "dominated starts (back pops)", "deque (index:P)", "shortest"], *grows),
        f"Shortest run: **{bestlen if bestlen <= len(ch) else -1}**.",
    ],
    "approaches": {
        0: {
            "idea": ["From every start, extend until the sum reaches the target; the first time it does is the shortest run from that start."],
            "build": ["Every start.", "Running sum while extending.", "Record the first length that reaches the target."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["With negative values it can't stop early in general, so it scans everything. Prefix sums with the right data structure avoid that."],
        },
        1: {
            "idea": [
                """
                Prefix sums, and an increasing stack of start indices (by prefix value). For each end `j`, binary-search the
                stack for the **latest** start with `P[i] ≤ P[j] − target`, then push `j` after popping starts with larger or
                equal prefix.
                """
            ],
            "build": ["Prefix sums.", "Increasing stack of starts.", "Binary-search the latest valid start for each end.", "Maintain the stack."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["A binary search per end. Observation 2 shows a start can be discarded once used, which makes every step O(1) amortised."],
        },
        2: {
            "idea": [
                """
                Monotonic deque of prefix indices with increasing `P`. For each `j`: while the front start gives a gain of at
                least `target`, record `j − front` and pop it; then pop back starts with `P ≥ P[j]`; push `j`.
                """
            ],
            "build": ["Prefix sums.", "Front pops record runs.", "Back pops drop dominated starts.", "Push `j`."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Shortest subarray with sum ≥ target, negatives allowed:** prefix sums + monotonic deque.
        - Discard starts that are dominated (back) or already used (front).
        - **Pitfall:** using a sliding window, which needs non-negative values.
        """
    ],
}


# ---------------------------------------------------------------- best-pair-of-posts
posts, pk = [[0, 3], [2, 1], [3, 5], [7, 2], [8, 6], [12, 0]], 4
dq, bestv, prow = deque(), None, []
for j, (x, y) in enumerate(posts):
    exp = []
    while dq and x - posts[dq[0]][0] > pk:
        exp.append(dq.popleft())
    val = "—"
    if dq:
        xi, yi = posts[dq[0]]
        val = (y + x) + (yi - xi)
        bestv = val if bestv is None or val > bestv else bestv
    drop = []
    while dq and posts[dq[-1]][1] - posts[dq[-1]][0] <= y - x:
        drop.append(dq.pop())
    dq.append(j)
    prow.append((j, f"[{x}, {y}]", y + x, y - x, exp or "—", val, " ".join(f"{q}:{posts[q][1] - posts[q][0]}" for q in dq), bestv if bestv is not None else "—"))
EXTRA["best-pair-of-posts"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only pairs within distance `k` count; at least one exists.
        - Heights can be negative.
        - Values reach about `3 × 10⁸`; 64 bits are safe.
        """
    ],
    "think": [
        f"""
        **Separate the two posts.** `y_i + y_j + (x_j − x_i) = (y_j + x_j) + (y_i − x_i)`. With the right post `j` fixed,
        the first part is a constant, so we just need the **largest `y_i − x_i`** among earlier posts within distance `k`.
        That's a sliding window maximum, where the window is defined by position rather than by count.

        **The deque** holds earlier posts with decreasing `y − x`; the front is the best partner. Expire posts that are too
        far from the current `x`.
        """,
        f"**Trace on `{posts}`, k = {pk}:**",
        table(["post", "[x, y]", "y + x", "y − x", "expired", "value with best partner", "deque (post:y−x)", "best"], *prow),
        f"Best banner **{bestv}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every pair `i < j` within distance `k` and compute the value."],
            "build": ["Every pair.", "Skip pairs too far apart.", "Track the best value."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Splitting the value makes the best partner a window maximum."],
        },
        1: {
            "idea": [
                """
                For each post `j` in order of position: expire deque fronts with `x_j − x_front > k`; if the deque isn't
                empty, the front gives the best value `(y_j + x_j) + (y_front − x_front)`; then pop back posts with
                `y − x ≤ y_j − x_j` and push `j`.
                """
            ],
            "build": ["Deque of indices with decreasing `y − x`.", "Expire by distance.", "Use the front.", "Pop dominated posts; push."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Pair objectives that split into f(i) + g(j):** fix `j`, maximise `f(i)` over a window.
        - Windows can be defined by coordinates; expire by distance instead of count.
        - **Pitfall:** using the post itself as its own partner (query before pushing).
        """
    ],
}
