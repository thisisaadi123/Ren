"""In-depth text for the partition (Dutch flag) problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

# ---------------------------------------------------------------- three-colours
balls = [2, 0, 1, 2, 1, 0, 0]
a, lo, mid, hi = balls[:], 0, 0, len(balls) - 1
drows = []
while mid <= hi:
    v = a[mid]
    if v == 0:
        a[lo], a[mid] = a[mid], a[lo]
        act = f"0: swap with a[lo={lo}], lo and mid move right"
        lo, mid = lo + 1, mid + 1
    elif v == 2:
        a[mid], a[hi] = a[hi], a[mid]
        act = f"2: swap with a[hi={hi}], hi moves left (mid stays: the ball that came in is unknown)"
        hi -= 1
    else:
        act = "1: already in the 1s zone, mid moves right"
        mid += 1
    zones = f"0s {a[:lo]} | 1s {a[lo:mid]} | ? {a[mid:hi + 1]} | 2s {a[hi + 1:]}"
    drows.append((v, act, zones))
EXTRA["three-colours"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only one or two colours present: still works, some zones stay empty.
        - Already sorted: one pass with no harmful swaps.
        - One ball: unchanged.
        """
    ],
    "think": [
        """
        **Four zones.** Keep three pointers and think of the row as

        `[ 0s | 1s | unknown | 2s ]`, with the 0s in `[0, lo)`, the 1s in `[lo, mid)`, the unknown part in `[mid, hi]` and
        the 2s in `(hi, n)`.

        Look at the first unknown ball `a[mid]`:

        - **1:** it belongs right where it is, at the end of the 1s zone: `mid += 1`.
        - **0:** swap it with `a[lo]`, the first ball of the 1s zone (or itself if that zone is empty). The 0s zone grows
          and so does the 1s zone's start: `lo += 1`, `mid += 1`.
        - **2:** swap it with `a[hi]`, the last unknown ball, and `hi −= 1`. Don't move `mid`: the ball that just arrived
          came from the unknown zone and hasn't been examined.

        Every step shrinks the unknown zone by one, so after at most `n` steps it's empty and the row is sorted.
        """,
        f"**Trace on `{balls}`:**",
        table(["ball at mid", "action", "zones after"], *drows),
    ],
    "approaches": {
        0: {
            "idea": ["Sort with the built-in sort. Correct but O(n log n), and it ignores that there are only three values."],
            "build": ["Sort."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the copy."],
            "limits": ["Only three distinct values exist; counting or partitioning handles that in O(n)."],
            "lines": {"sort": "A general-purpose sort."},
        },
        1: {
            "idea": ["Count the 0s, 1s and 2s in one pass, then write that many of each. Two passes, O(1) extra space."],
            "build": ["Count each colour.", "Write the colours back in order."],
            "complexity": ["**Time O(n):** two passes. **Space O(1)** besides the output."],
            "limits": ["Two passes, and it rewrites values instead of moving the actual items, which doesn't work when the items carry more data than their colour. The three-pointer partition does one pass and only swaps."],
            "lines": {
                "count": "How many balls of each colour.",
                "write": "Rebuild the row: all 0s, then 1s, then 2s.",
            },
        },
        2: {
            "idea": [
                """
                Pointers `lo = mid = 0`, `hi = n − 1`. While `mid ≤ hi`, classify `a[mid]` as above.

                **Invariant.** `a[0..lo)` are 0s, `a[lo..mid)` are 1s, `a(hi..n)` are 2s; `a[mid..hi]` is unexamined. It
                holds at the start (all zones empty except the unknown one), and each case keeps it.

                **Why advancing `mid` after a 0-swap is safe.** The ball moved from `lo` to `mid` was a 1 (from the 1s
                zone) or, if `lo = mid`, the same 0. Either way it's already classified.
                """
            ],
            "build": ["Three pointers.", "0: swap with `lo`, advance `lo` and `mid`.", "2: swap with `hi`, retreat `hi`.", "1: advance `mid`."],
            "complexity": ["**Time O(n):** each step shrinks the unknown zone by one. **Space O(1).**"],
            "lines": {
                "init": "Empty 0s and 1s zones at the left, empty 2s zone at the right; everything is unknown.",
                "loop": "While unknown balls remain.",
                "zero": "A 0 joins the 0s zone by swapping with the first 1; both boundaries move right.",
                "two": "A 2 joins the 2s zone by swapping with the last unknown ball; `mid` stays to examine the ball that arrived.",
                "one": "A 1 is already in the right zone.",
                "ret": "The sorted row.",
            },
        },
    },
    "takeaways": [
        """
        - **Dutch national flag:** three zones plus an unknown zone, one pass, O(1) space.
        - After swapping with the far end, re-examine the incoming element.
        - **Pitfall:** advancing `mid` after a 2-swap, which skips an unexamined ball.
        - **Related:** quicksort's three-way partition uses exactly this loop.
        """
    ],
}


# ---------------------------------------------------------------- split-around-a-pivot
vals, pivot = [9, 12, 5, 10, 3, 10, 14], 10
less = sum(1 for x in vals if x < pivot)
equal = sum(1 for x in vals if x == pivot)
out, pa, pb, pc = [None] * len(vals), 0, less, less + equal
srows = []
for x in vals:
    if x < pivot:
        out[pa] = x
        srows.append((x, "less", pa, list(out)))
        pa += 1
    elif x == pivot:
        out[pb] = x
        srows.append((x, "equal", pb, list(out)))
        pb += 1
    else:
        out[pc] = x
        srows.append((x, "greater", pc, list(out)))
        pc += 1
EXTRA["split-around-a-pivot"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The pivot may not appear at all (empty middle group).
        - All values on one side: unchanged order.
        - Order **inside** each group must match the input (a stable partition).
        """
    ],
    "think": [
        """
        **Why the in-place Dutch flag doesn't fit.** Swapping balls around scrambles the order inside the groups. Here
        each group must keep its original order, so we need a *stable* partition.

        **Count first, then place.** Once we know how many values are less than the pivot (`L`) and equal to it (`E`),
        every group's final block is fixed: less → `[0, L)`, equal → `[L, L + E)`, greater → `[L + E, n)`. Keep a write
        position per group and place each value at its group's next slot while reading left to right. Reading in order
        keeps each group in order.
        """,
        f"**Pivot {pivot}:** {less} less, {equal} equal, so the blocks start at 0, {less} and {less + equal}.",
        table(["value", "group", "slot", "output so far"], *[(x, g, s, " ".join("·" if v is None else str(v) for v in o)) for x, g, s, o in srows]),
    ],
    "approaches": {
        0: {
            "idea": ["Sort by group number (0 for less, 1 for equal, 2 for greater) with a **stable** sort, which keeps equal keys in their original order."],
            "build": ["Group key for each value.", "Stable sort by the key."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Sorting three group labels doesn't need O(n log n): counting the groups gives every value's final position directly. (C's `qsort` isn't stable, so the C version breaks ties by each value's original position.)"],
            "lines": {
                "key": "0, 1 or 2 depending on the value's relation to the pivot.",
                "sort": "A stable sort by that key keeps the original order within each group.",
            },
        },
        1: {
            "idea": [
                """
                Count values less than and equal to the pivot. Set write positions `a = 0`, `b = L`, `c = L + E`. Read the
                values in order and place each one at its group's write position, advancing it.

                **Why the order is kept.** Within a group, values are written to increasing slots in the order they're
                read, which is their original order.
                """
            ],
            "build": ["Count the less and equal groups.", "Three write positions.", "Place every value in one pass."],
            "complexity": ["**Time O(n):** two passes. **Space O(n)** for the output."],
            "lines": {
                "count": "Sizes of the less and equal groups (the greater group is the rest).",
                "starts": "Where each group's block begins in the output.",
                "place": "Each value goes to the next free slot of its group's block.",
                "ret": "The partitioned list, stable within each group.",
            },
        },
    },
    "takeaways": [
        """
        - **Stable partition:** count group sizes, then place with one write pointer per group (counting sort's idea).
        - In-place swap partitions are fast but not stable.
        - **Pitfall:** using an unstable sort for the brute force.
        """
    ],
}


# ---------------------------------------------------------------- sort-k-colours
kb, k = [3, 1, 4, 2, 4, 1, 3, 2], 4
arr = kb[:]
krows, stack = [], [(0, len(arr) - 1, 1, k)]
while stack:
    left, right, lo_c, hi_c = stack.pop()
    if left >= right or lo_c >= hi_c:
        continue
    m = (lo_c + hi_c) // 2
    i, j = left, right
    before = arr[left:right + 1]
    while i <= j:
        while i <= j and arr[i] <= m:
            i += 1
        while i <= j and arr[j] > m:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    krows.append((f"{left}..{right}", f"{lo_c}..{hi_c}", m, before, arr[left:right + 1], f"{left}..{j} gets {lo_c}..{m}, {i}..{right} gets {m + 1}..{hi_c}"))
    stack.append((left, j, lo_c, m))
    stack.append((i, right, m + 1, hi_c))
EXTRA["sort-k-colours"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 1`: already sorted.
        - Colours missing from the input: their halves are simply empty.
        - The goal is O(n log k) time with no count array of size `k`.
        """
    ],
    "think": [
        """
        **Partition by colour range, recursively.** In the sorted result, colours `lo..mid` all come before colours
        `mid+1..hi`. One two-pointer pass can separate a segment into those two groups (like quicksort's partition, with
        the colour value `mid` as a fixed pivot). Then each half is the same problem with half the colour range.

        **Why O(n log k).** The colour range halves at every level, so there are about `log₂ k` levels. On each level the
        segments don't overlap, so all partition passes together touch each ball once: O(n) per level.
        """,
        f"**Trace on `{kb}` with k = {k}:**",
        table(["segment", "colours", "split at", "before", "after", "next"], *krows),
        f"Result **`{arr}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Use a comparison sort. O(n log n), which is more than needed when `k` is small."],
            "build": ["Sort."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["It ignores that there are only `k` distinct values. Splitting the colour range gives O(n log k) without a count array."],
            "lines": {"sort": "A general-purpose comparison sort."},
        },
        1: {
            "idea": [
                """
                Keep a stack of tasks `(left, right, lo, hi)`: "segment `[left, right]` holds only colours `lo..hi`". For a
                task, set `mid = (lo + hi) / 2` and partition: `i` moves right over colours `≤ mid`, `j` moves left over
                colours `> mid`, and out-of-place pairs are swapped. Then push `[left, j]` with `lo..mid` and `[i, right]`
                with `mid+1..hi`. A segment with one colour or one ball needs nothing.

                Using an explicit stack instead of recursion avoids deep call stacks.
                """
            ],
            "build": ["Task stack starting with the whole array and colours `1..k`.", "Partition each task around the middle colour.", "Push the two halves with halved colour ranges."],
            "complexity": ["**Time O(n log k).** **Space O(log k)** for the task stack (each level adds a constant number of tasks)."],
            "lines": {
                "init": "A working copy and the first task: the whole array, colours `1..k`.",
                "loop": "Process tasks until none remain; skip segments that are trivially sorted.",
                "split": "Two pointers move inward: `i` past colours that belong left (`≤ mid`), `j` past colours that belong right; a pair on the wrong sides is swapped. When they cross, `[left, j]` holds the low colours and `[i, right]` the high ones.",
                "halves": "Each half becomes a new task with half the colour range.",
                "ret": "The sorted balls.",
            },
        },
    },
    "takeaways": [
        """
        - **Sorting few distinct values:** partition by value range (O(n log k)), or counting sort (O(n + k) with extra space).
        - Partitioning around a fixed value instead of a random element guarantees balanced recursion in the value range.
        - **Pitfall:** recursing on segments that hold a single colour.
        """
    ],
}


# ---------------------------------------------------------------- fewest-swaps-three-colours
fb = [2, 0, 1, 0, 2, 1, 0]
n0, n1 = fb.count(0), fb.count(1)
target = [0] * n0 + [1] * n1 + [2] * (len(fb) - n0 - n1)
cm = [[0] * 3 for _ in range(3)]
for i, x in enumerate(fb):
    cm[x][target[i]] += 1
pairs = {(x, y): min(cm[x][y], cm[y][x]) for x in range(3) for y in range(x + 1, 3)}
after = [row[:] for row in cm]
for (x, y), m in pairs.items():
    after[x][y] -= m
    after[y][x] -= m
left = sum(after[x][y] for x in range(3) for y in range(3) if x != y)
answer = sum(pairs.values()) + 2 * left // 3
EXTRA["fewest-swaps-three-colours"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already arranged: 0 swaps.
        - Any two balls may be swapped, not only neighbours.
        - Balls already in the right zone never need to move.
        """
    ],
    "think": [
        f"""
        **Where every ball must go.** The final row is `{n0}` zeros, `{n1}` ones, then the twos, so each slot has a
        required colour. Compare `{fb}` with `{target}` and count balls by **(colour it is, colour its slot needs)**:
        """,
        table(["ball \\ slot needs", "0", "1", "2"], *[[f"is {x}"] + [cm[x][y] if x != y else f"({cm[x][y]} in place)" for y in range(3)] for x in range(3)]),
        f"""
        **Best case: a swap that fixes two balls.** A "0 in a 1-slot" and a "1 in a 0-slot" swap with each other and both
        become correct. No swap can fix more than two balls, so use as many of these mutual pairs as possible:
        {', '.join(f'{m} pair(s) of {x}↔{y}' for (x, y), m in pairs.items())}.

        **What's left forms 3-cycles.** After the pairs are used up, the remaining misplacements can only be of the form
        "0 needs 1's slot, 1 needs 2's slot, 2 needs 0's slot" (or the reverse direction): {left} ball(s), so {left // 3}
        cycle(s). A 3-cycle can't be fixed in one swap (that would need a mutual pair), but two swaps always do it. So each
        costs 2.

        Total: {sum(pairs.values())} + 2 · {left // 3} = **{answer}**.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Build the 3 × 3 table of (actual colour, needed colour) counts for misplaced balls. Add the mutual pairs
                `min(c[x][y], c[y][x])` for each pair of colours, remove them, and add 2 for every 3 remaining misplaced
                balls.

                **Why it's optimal.** Each swap fixes at most two balls, and only a mutual pair fixes two, so using all
                mutual pairs first can't hurt. Every remaining ball sits in a 3-cycle that needs at least 2 swaps for 3
                balls, and 2 always suffice.
                """
            ],
            "build": ["Find each slot's required colour from the counts.", "Tally misplacements by (actual, needed).", "Use all mutual pairs.", "Add 2 per remaining 3-cycle."],
            "complexity": ["**Time O(n).** **Space O(1):** a 3 × 3 table."],
            "lines": {
                "target": "Count the zeros and ones: slots `[0, n0)` need 0, `[n0, n0 + n1)` need 1, the rest need 2.",
                "tally": "For each ball, record (its colour, the colour its slot needs). Diagonal entries are balls already in place.",
                "pairs": "Two balls that need each other's slots: one swap fixes both. Use as many as possible for each pair of colours.",
                "cycles": "Remaining misplaced balls form 3-cycles of three balls; each costs exactly 2 swaps.",
            },
        },
    },
    "takeaways": [
        """
        - **Minimum swaps to a target arrangement:** count misplacements by (is, needs); fix 2-cycles with one swap, `k`-cycles with `k − 1`.
        - For three colours only 2-cycles and 3-cycles occur.
        - **Pitfall:** counting misplaced balls and dividing by 2, which ignores the 3-cycles.
        """
    ],
}
