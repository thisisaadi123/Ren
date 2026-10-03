"""In-depth text for the quickselect problems (merged into their sol() calls via sol.EXTRA)."""
import random

from sol import EXTRA, table

SELECT = """
**Quickselect: quick sort that only follows one side.** To find the value at sorted position `t`, partition around a
pivot into `< p | = p | > p`. The `= p` block already sits at its final sorted positions `lt … gt`:

- if `t` falls inside `lt … gt`, the answer is the pivot;
- if `t < lt`, the answer is in the left part, so continue only there;
- if `t > gt`, continue only in the right part.

**Why it's O(n) on average.** A random pivot splits the range roughly in half on average, and only one half is kept:
`n + n/2 + n/4 + … ≈ 2n` comparisons. The worst case is O(n²) (consistently terrible pivots), which randomness makes
vanishingly unlikely. Three-way partitioning keeps repeated values from causing that worst case.
"""


def select_trace(a, target, seed):
    rnd = random.Random(seed)
    a = a[:]
    lo, hi, rows = 0, len(a) - 1, []
    while True:
        p = a[rnd.randint(lo, hi)]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] < p:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > p:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        where = "inside the pivot block → answer" if lt <= target <= gt else ("left of the block → keep the left part" if target < lt else "right of the block → keep the right part")
        rows.append((f"{lo} … {hi}", p, f"{a[lo:lt]} | {a[lt:gt + 1]} | {a[gt + 1:hi + 1]}", f"{lt} … {gt}", where))
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return rows, p


# ---------------------------------------------------------------- kth-highest-bid
bids, k = [12, 40, 7, 40, 25, 3, 18], 3
t = len(bids) - k
krows, kans = select_trace(bids, t, 3)
EXTRA["kth-highest-bid"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Repeats count separately: in `[9, 9, 5]` the 2nd highest is 9.
        - `k = 1` is the maximum; `k = n` the minimum.
        - The k-th highest is the value at sorted (ascending) index `n − k`.
        """
    ],
    "think": [
        SELECT,
        f"""
        **Quickselect on `{bids}` for the {k}rd highest** (sorted index {t}); the pivot is random, one possible run:
        """,
        table(["range", "pivot", "after partition (< | = | >)", "pivot block", "decision"], *krows),
        f"Answer **{kans}** (sorted: {sorted(bids)}).",
    ],
    "approaches": {
        0: {
            "idea": ["Sort and read index `n − k`."],
            "build": ["Sort.", "Index `n − k`."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Orders everything to read one position."],
        },
        1: {
            "idea": [
                """
                Keep a min-heap of the `k` largest bids seen so far: push each bid, and pop the smallest whenever the heap
                exceeds `k`. At the end the heap's minimum is the k-th highest.
                """
            ],
            "build": ["Min-heap.", "Push each bid; pop when size exceeds `k`.", "Return the heap's minimum."],
            "complexity": ["**Time O(n log k).** **Space O(k).**"],
            "limits": ["O(log k) per bid; quickselect averages O(1) per element."],
        },
        2: {
            "idea": [
                """
                Quickselect for sorted index `n − k` with three-way partitioning and a random pivot, narrowing `lo … hi`
                to the side that contains the target until it lands in the pivot block.
                """
            ],
            "build": ["Target index `n − k`.", "Random pivot, three-way partition.", "Keep the side containing the target."],
            "complexity": ["**Time O(n)** expected, O(n²) worst case. **Space O(n)** for the copy (O(1) in place)."],
        },
    },
    "takeaways": [
        """
        - **k-th largest/smallest:** quickselect (expected O(n)) or a size-k heap (O(n log k), good for streams).
        - Translate "k-th highest" to the ascending index `n − k`.
        - **Pitfall:** two-way partitioning with many equal values.
        """
    ],
}


# ---------------------------------------------------------------- middle-reading
rd = [8, -3, 15, 4, 4, 11, 0]
mt = len(rd) // 2
mrows, mans = select_trace(rd, mt, 7)
EXTRA["middle-reading"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The length is odd, so the median is a single reading at sorted index `n // 2`.
        - Repeated readings: the median may be one of several equal values.
        - One reading: it's the median.
        """
    ],
    "think": [
        SELECT,
        f"**Quickselect on `{rd}` for sorted index {mt}** (one possible run):",
        table(["range", "pivot", "after partition (< | = | >)", "pivot block", "decision"], *mrows),
        f"Median **{mans}** (sorted: {sorted(rd)}).",
    ],
    "approaches": {
        0: {
            "idea": ["Sort and take the middle element."],
            "build": ["Sort.", "Middle element."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Sorts everything to read one position."],
        },
        1: {
            "idea": ["Quickselect for index `n // 2` with three-way partitioning and random pivots."],
            "build": ["Target `n // 2`.", "Partition and keep the side containing it.", "Return the pivot when the target lands in its block."],
            "complexity": ["**Time O(n)** expected. **Space O(n)** for the copy."],
        },
    },
    "takeaways": [
        """
        - **Median = k-th smallest with `k = n // 2`**: quickselect.
        - For a stream of readings, two heaps maintain the median instead.
        - **Pitfall:** sorting just to read the middle.
        """
    ],
}


# ---------------------------------------------------------------- nearest-stations
st, sk = [[3, 4], [-1, 1], [0, -2], [2, 2], [-2, 0], [5, 0]], 3
keys = sorted((x * x + y * y, x, y) for x, y in st)
EXTRA["nearest-stations"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties in distance: smaller `x`, then smaller `y`.
        - Compare **squared** distances: same order as real distances, no square roots or rounding.
        - `k = n`: return all stations in order.
        """
    ],
    "think": [
        SELECT,
        f"""
        **Keys.** Give each station the key `(x² + y², x, y)`: distance first, then the tie rules. For `{st}`:
        """,
        table(["station", "key"], *[([x, y], (x * x + y * y, x, y)) for x, y in st]),
        f"""
        **Select, then sort only `k`.** Quickselect for key position `k − 1` leaves the `k` smallest keys in the first `k`
        slots (in some order); sorting just those `k` gives the required order. Answer:
        **{[[x, y] for _, x, y in keys[:sk]]}**.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Sort all stations by `(distance², x, y)` and take the first `k`."],
            "build": ["Sort by the key.", "Take `k`."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Orders all `n` stations when only the first `k` matter."],
        },
        1: {
            "idea": [
                """
                Build the keys, quickselect so that position `k − 1` holds the right key and everything before it is
                smaller, then sort the first `k` keys and convert back to points.

                **Why the first `k` slots are the `k` nearest.** After the final partition, every key before the target's
                pivot block is smaller and every key after it is larger, so positions `0 … k − 1` hold exactly the `k`
                smallest keys.
                """
            ],
            "build": ["Keys `(d², x, y)`.", "Quickselect for index `k − 1`.", "Sort the first `k` and return their points."],
            "complexity": ["**Time O(n + k log k)** expected. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **k closest points:** quickselect then sort `k` (expected O(n + k log k)), or a size-k max-heap.
        - Use squared distances and tuple keys for tie rules.
        - **Pitfall:** floating-point distances (rounding can break exact ties).
        """
    ],
}
