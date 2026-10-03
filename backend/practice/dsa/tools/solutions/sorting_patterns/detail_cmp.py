"""In-depth text for the comparison-sort problems (merged into their sol() calls via sol.EXTRA)."""
import heapq

from sol import EXTRA, table

DIVIDE = """
**Why O(n log n) sorts work.** Insertion sort places each value by scanning a sorted prefix: up to `n` steps per value,
O(n²) total. The O(n log n) sorts **divide** the problem:

- **Merge sort** splits the array in half, sorts each half, and merges two sorted halves in linear time. There are
  `log₂ n` levels of halving and each level does O(n) merging: O(n log n), always. It's **stable** (equal values keep
  their order) but needs an O(n) buffer for arrays.
- **Quick sort** picks a pivot, partitions the values into "smaller" and "larger" around it, then sorts both sides. With
  a random pivot the split is balanced on average: O(n log n) expected, in place, but O(n²) if pivots keep being
  extreme, and not stable.
"""


def merge_levels(a):
    """Rows showing the merge sort from single elements up, level by level."""
    rows, runs = [], [[x] for x in a]
    rows.append(("start", " | ".join(" ".join(map(str, r)) for r in runs)))
    level = 1
    while len(runs) > 1:
        nxt = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                nxt.append(sorted(runs[i] + runs[i + 1]))
            else:
                nxt.append(runs[i])
        runs = nxt
        rows.append((f"after merge level {level}", " | ".join(" ".join(map(str, r)) for r in runs)))
        level += 1
    return rows


# ---------------------------------------------------------------- sort-the-scoreboard
sc = [42, -7, 15, 42, 0, 9]
piv = 9
less, eq, more = [x for x in sc if x < piv], [x for x in sc if x == piv], [x for x in sc if x > piv]
EXTRA["sort-the-scoreboard"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One score: already sorted.
        - Repeated scores, and already sorted or reverse-sorted input (worst cases for a careless quick sort).
        - The built-in sort isn't allowed: write merge sort or quick sort.
        """
    ],
    "think": [
        DIVIDE,
        f"**Merge sort on `{sc}`, bottom-up view** (each level merges neighbouring sorted runs):",
        table(["stage", "runs"], *merge_levels(sc)),
        f"""
        **Quick sort's partition step**, with pivot {piv}: values smaller than the pivot go left, the rest go right, and
        the pivot lands between them in its final position: `{less}` · `{eq}` · `{more}`. Each side is then sorted the
        same way.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Insertion sort: grow a sorted prefix, inserting each new value by shifting larger values one place right."],
            "build": ["For each value, shift larger values in the prefix right.", "Drop the value into the gap."],
            "complexity": ["**Time O(n²)** in the worst case (reverse-sorted input). **Space O(1).**"],
            "limits": ["Each insertion can scan the whole prefix. Dividing the array into halves gives O(n log n)."],
        },
        1: {
            "idea": [
                """
                Pick a random pivot, swap it to the end, and partition: one pointer `i` marks the end of the "smaller than
                pivot" region while `j` scans. Swap the pivot into position `i`; it's now in its final place. Recurse on
                both sides.

                **Why random.** A fixed pivot (say the last element) splits sorted input into sizes `n − 1` and 0 every
                time: O(n²). A random pivot makes such bad splits unlikely, giving O(n log n) expected.
                """
            ],
            "build": ["Random pivot to the end.", "Partition with a write pointer.", "Place the pivot.", "Recurse on both sides."],
            "complexity": ["**Time O(n log n)** expected, O(n²) worst case. **Space O(log n)** expected recursion depth."],
            "limits": ["Its guarantee is only in expectation, and it isn't stable. Merge sort is O(n log n) on every input."],
        },
        2: {
            "idea": [
                """
                Recursively sort the left half and the right half, then merge them into a buffer by repeatedly taking the
                smaller front value (the left one on ties, which keeps the sort stable), and copy back.

                **Recurrence.** `T(n) = 2·T(n/2) + O(n)`: `log₂ n` levels, each doing O(n) total work, so O(n log n).
                """
            ],
            "build": ["Split at the middle.", "Sort both halves recursively.", "Merge into a buffer, then copy back."],
            "complexity": ["**Time O(n log n)** on every input. **Space O(n)** for the buffer plus O(log n) recursion."],
        },
    },
    "takeaways": [
        """
        - **Merge sort:** guaranteed O(n log n), stable, O(n) extra space.
        - **Quick sort:** in place and fast in practice; randomise the pivot to avoid O(n²).
        - **Pitfall:** a fixed pivot on sorted input; forgetting to copy the merged buffer back.
        """
    ],
}


# ---------------------------------------------------------------- nearly-sorted-log
times, k = [3, 1, 2, 6, 4, 5, 9, 7, 8], 2
heap, out, hrows = [], [], []
for t in times:
    heapq.heappush(heap, t)
    popped = "—"
    if len(heap) > k:
        popped = heapq.heappop(heap)
        out.append(popped)
    hrows.append((t, sorted(heap), popped, list(out)))
while heap:
    out.append(heapq.heappop(heap))
EXTRA["nearly-sorted-log"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 0`: already sorted.
        - `k` is small (≤ 10) while `n` is large: exploit that.
        - Equal timestamps are fine.
        """
    ],
    "think": [
        f"""
        **Where can the next smallest be?** Every entry is at most `k` positions from its sorted place. So the smallest
        entry overall sits within the first `k + 1` positions, and in general, the entry that belongs at position `i`
        sits within positions `i … i + k`. Keeping a min-heap of the next `k + 1` unread-or-unplaced entries, the smallest
        in the heap is always the next one in sorted order.

        **Trace** for `{times}`, `k = {k}` (push each entry; once the heap holds more than `k`, pop its minimum):
        """,
        table(["push", "heap (sorted for display)", "popped", "output so far"], *hrows),
        f"Drain the rest of the heap: **{out}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Use the built-in sort. Correct, O(n log n), but ignores that entries are almost in place."],
            "build": ["Sort."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Doesn't use the `k` bound; each entry only needs to move a few places."],
        },
        1: {
            "idea": [
                """
                Insertion sort. Each entry is shifted left past larger entries; because it's at most `k` places from home,
                and entries before it are also nearly placed, each insertion shifts O(k) entries.
                """
            ],
            "build": ["Copy.", "Insert each entry into the sorted prefix by shifting."],
            "complexity": ["**Time O(n · k)**: 10⁶ steps for `n = 10⁵`, `k = 10`. **Space O(n)** for the copy."],
            "limits": ["O(n · k) grows with `k`; a heap of size `k + 1` gives O(n log k)."],
        },
        2: {
            "idea": [
                """
                Push each entry into a min-heap; when the heap holds more than `k` entries, pop the minimum into the output.
                At the end, pop everything left.

                **Why the popped value is correct.** When position `i` of the output is filled, all entries that could
                belong there (positions `i … i + k` of the input) have been pushed, and the heap holds the smallest
                remaining ones.
                """
            ],
            "build": ["Empty min-heap.", "Push each entry; pop when size exceeds `k`.", "Drain the heap."],
            "complexity": ["**Time O(n log k).** **Space O(k)** for the heap."],
        },
    },
    "takeaways": [
        """
        - **k-sorted input:** a min-heap of size `k + 1` sorts it in O(n log k).
        - Insertion sort is also fast on nearly sorted data (O(n · k)).
        - **Pitfall:** a heap of size `k` (one too small) misplaces entries exactly `k` away.
        """
    ],
}


# ---------------------------------------------------------------- sort-the-train-cars
cars = [4, 2, 1, 3, 2]
EXTRA["sort-the-train-cars"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - An empty train or a single car: already sorted.
        - Equal weights: either order is fine.
        - Linked lists have no indexing, so array-style quick sort (random access, swaps by index) doesn't fit.
        """
    ],
    "think": [
        DIVIDE,
        f"""
        **Why merge sort suits linked lists.** Its two operations are exactly what lists do well:

        - **Split:** find the middle with slow/fast pointers (fast moves two cars per step, so when it reaches the end,
          slow is in the middle), then cut the link after the middle.
        - **Merge:** relink the smaller front car each step; no extra array is needed.

        For `{cars}`:
        """,
        table(["stage", "runs"], *merge_levels(cars)),
    ],
    "approaches": {
        0: {
            "idea": ["Copy the weights into an array, sort it, and write the sorted weights back into the cars in order."],
            "build": ["Read the weights.", "Sort.", "Write them back."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the array."],
            "limits": ["Needs an array as large as the train, and rewrites values instead of reordering the cars themselves."],
        },
        1: {
            "idea": [
                """
                If the train has 0 or 1 cars, return it. Otherwise find the middle with slow/fast pointers, cut the list in
                two, sort each half recursively, and merge them with a dummy head.

                **Why `fast` starts at `head.next`.** For a two-car list, `slow` then stays on the first car, so the cut
                produces two non-empty halves and the recursion always shrinks.
                """
            ],
            "build": ["Base case: 0 or 1 cars.", "Slow/fast to the middle; cut.", "Sort both halves.", "Merge with a dummy head."],
            "complexity": ["**Time O(n log n).** **Space O(log n)** for the recursion; no arrays."],
        },
    },
    "takeaways": [
        """
        - **Sorting a linked list:** merge sort (split with slow/fast, merge by relinking).
        - Cut the list after finding the middle, or the halves stay connected.
        - **Pitfall:** starting `fast` at `head`, which can leave a two-node list unsplit forever.
        """
    ],
}


# ---------------------------------------------------------------- sort-with-many-repeats
rd = [5, 3, 5, 1, 5, 3, 5]
p = 5
a, lt, i, gt = rd[:], 0, 0, len(rd) - 1
trows = []
while i <= gt:
    v = a[i]
    if v < p:
        a[lt], a[i] = a[i], a[lt]
        act = f"{v} < {p}: swap into the 'less' zone"
        lt += 1
        i += 1
    elif v > p:
        a[i], a[gt] = a[gt], a[i]
        act = f"{v} > {p}: swap to the 'greater' zone (re-check what arrived)"
        gt -= 1
    else:
        act = f"{v} = {p}: stays in the 'equal' zone"
        i += 1
    trows.append((v, act, f"less {a[:lt]} | equal {a[lt:i]} | ? {a[i:gt + 1]} | greater {a[gt + 1:]}"))
EXTRA["sort-with-many-repeats"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All readings equal: a two-way quick sort degrades to O(n²) and n-deep recursion.
        - Only a few distinct values: most of the work should be skipped.
        - The built-in sort isn't allowed.
        """
    ],
    "think": [
        DIVIDE,
        """
        **What goes wrong with repeats.** Two-way partitioning puts values equal to the pivot on one side. When almost
        everything equals the pivot, each partition removes only the pivot itself: `n` levels of O(n) work.

        **Three-way partitioning.** Split into `< pivot | = pivot | > pivot`. The middle block is already in its final
        place and is never touched again, so a value repeated many times is handled in one pass. The loop is the Dutch
        national flag: `lt` ends the "less" zone, `i` scans, `gt` starts the "greater" zone.
        """,
        f"**Partitioning `{rd}` around pivot {p}:**",
        table(["value at i", "action", "zones after"], *trows),
    ],
    "approaches": {
        0: {
            "idea": ["Quick sort with a random pivot and two-way partitioning (`< pivot` on the left, everything else on the right)."],
            "build": ["Random pivot.", "Two-way partition.", "Recurse on both sides."],
            "complexity": ["**Time O(n²)** when most values are equal (each partition peels off one value). **Space O(n)** recursion in that case."],
            "limits": ["Equal values keep landing on the same side. Grouping them into their own block removes them from further work."],
        },
        1: {
            "idea": [
                """
                Three-way quick sort with an explicit stack: partition `[lo, hi]` into `< p`, `= p`, `> p` with `lt`, `i`,
                `gt`, then push only `[lo, lt − 1]` and `[gt + 1, hi]`.

                **Why it's fast with repeats.** With `d` distinct values, each value becomes the pivot's equal block once,
                so the work is about O(n log d) expected.
                """
            ],
            "build": ["Stack of ranges.", "Random pivot value.", "Dutch-flag partition.", "Push the less and greater ranges only."],
            "complexity": ["**Time O(n log n)** expected, O(n log d) with `d` distinct values. **Space O(log n)** expected stack."],
        },
    },
    "takeaways": [
        """
        - **Many duplicates → three-way partition** (`<`, `=`, `>`).
        - The equal block is final and skipped from then on.
        - **Pitfall:** advancing `i` after swapping with `gt` (the arriving value is unexamined).
        """
    ],
}
