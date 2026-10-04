"""In-depth text for classic binary search and bounds problems (merged into their sol() calls via sol.EXTRA)."""
from bisect import bisect_left, bisect_right

from sol import EXTRA, table

HALVE = """
**Why binary search works.** In a sorted array, one comparison with the middle element tells you which half can't
contain what you're looking for: everything on the other side of the middle is smaller (or larger) too. Throwing away
half each time leaves 1 element after about `log₂ n` steps: 17 steps for 10⁵ elements.

**Think in invariants, not cases.** Decide what the range `lo … hi` means ("if the target exists, it's inside") and
keep that true on every update. The loop condition and the `±1` details follow from that meaning, which is where most
binary-search bugs come from.
"""

BOUND = """
**Lower and upper bound.** Many questions aren't "where is `x`?" but "where does the region of values `≥ x` (or
`> x`) start?". Over a half-open range `[lo, hi)`:

- if `a[mid] < x`, the boundary is to the right of `mid`: `lo = mid + 1`;
- otherwise `mid` might be the boundary: `hi = mid`.

The loop ends with `lo == hi` at the first index whose value is `≥ x` (**lower bound**), or `n` if there's none. Using
`≤` instead of `<` in the test gives the first index with value `> x` (**upper bound**). Duplicates don't break it.
"""


def closed_trace(a, target):
    lo, hi, rows = 0, len(a) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            rows.append((lo, hi, mid, a[mid], "equal: found"))
            return rows, mid
        if a[mid] < target:
            rows.append((lo, hi, mid, a[mid], f"{a[mid]} < {target}: target is to the right"))
            lo = mid + 1
        else:
            rows.append((lo, hi, mid, a[mid], f"{a[mid]} > {target}: target is to the left"))
            hi = mid - 1
    rows.append((lo, hi, "—", "—", "range empty: not found"))
    return rows, -1


def lower_trace(a, x, strict=False):
    lo, hi, rows = 0, len(a), []
    while lo < hi:
        mid = (lo + hi) // 2
        go_right = a[mid] <= x if strict else a[mid] < x
        rel = "≤" if strict else "<"
        if go_right:
            rows.append((lo, hi, mid, a[mid], f"{a[mid]} {rel} {x}: boundary is right of mid"))
            lo = mid + 1
        else:
            rows.append((lo, hi, mid, a[mid], "mid could be the boundary: keep it"))
            hi = mid
    rows.append((lo, hi, "—", "—", f"lo = hi = {lo}"))
    return rows, lo


TRACE_HEAD = ["lo", "hi", "mid", "value", "decision"]


# ---------------------------------------------------------------- find-the-locker
lockers, target = [-4, 1, 3, 8, 12, 17, 23, 30], 17
lrows, lans = closed_trace(lockers, target)
EXTRA["find-the-locker"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The target may be smaller than everything, larger than everything, or fall between two lockers: return −1.
        - One locker.
        - O(log n) is required, so a scan isn't allowed.
        """
    ],
    "think": [
        HALVE,
        f"""
        **Closed range `[lo, hi]`.** Meaning: if the target exists, its index is in `lo … hi`. The loop runs while the
        range is non-empty (`lo ≤ hi`). After comparing with `a[mid]`, the middle itself is ruled out too, so the new
        range is `mid + 1 … hi` or `lo … mid − 1`. For `{lockers}` and target {target}:
        """,
        table(TRACE_HEAD, *lrows),
        f"Answer **{lans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check lockers from left to right until the target is found."],
            "build": ["Scan.", "Return the index on a match, −1 at the end."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Ignores the sorting, and O(n) breaks the required O(log n)."],
        },
        1: {
            "idea": [
                """
                Keep `lo = 0`, `hi = n − 1`. While `lo ≤ hi`: compare the target with `a[mid]`; return `mid` on equality,
                otherwise discard the half (including `mid`) that can't contain it.

                **Why it terminates.** Every step shrinks the range by at least one (because `mid` is excluded), and it
                halves it, so at most about `log₂ n + 1` steps.
                """
            ],
            "build": ["Closed range over the whole array.", "Compare with the middle.", "Return on a hit, else drop the half without the target."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Exact search in a sorted array:** closed range, `while lo ≤ hi`, move to `mid ± 1`.
        - State what the range means and keep it true.
        - **Pitfall:** `hi = mid` with `while lo ≤ hi` (can loop forever); `(lo + hi)` overflow in fixed-width integers
          (use `lo + (hi − lo) / 2`).
        """
    ],
}


# ---------------------------------------------------------------- square-floor
x = 2024
lo, hi, srows = 0, min(x, 10**8), []
while lo < hi:
    mid = (lo + hi + 1) // 2
    if mid * mid <= x:
        srows.append((lo, hi, mid, mid * mid, f"{mid}² ≤ {x}: answer ≥ {mid}"))
        lo = mid
    else:
        srows.append((lo, hi, mid, mid * mid, f"{mid}² > {x}: answer < {mid}"))
        hi = mid - 1
EXTRA["square-floor"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `x = 0` and `x = 1`.
        - Perfect squares: the answer is exact.
        - `x` up to 9 × 10¹⁵, so `mid²` needs 64 bits; the answer is at most about 9.5 × 10⁷.
        """
    ],
    "think": [
        HALVE,
        f"""
        **Search on the answer.** The yes/no question "is `k² ≤ x`?" is **yes** for `k = 0, 1, …, ⌊√x⌋` and **no**
        afterwards. We want the last yes, so search over `k` instead of over an array.

        **Rounding up.** The range `[lo, hi]` means "the answer is in here". If `mid² ≤ x`, then `mid` is still a
        candidate, so `lo = mid` (not `mid + 1`). With `mid = (lo + hi) // 2`, a two-element range `lo, lo + 1` would
        give `mid = lo` and never shrink; rounding up, `mid = (lo + hi + 1) // 2`, avoids that.

        **The cap.** `√(9 × 10¹⁵) ≈ 9.49 × 10⁷`, so `hi = min(x, 10⁸)` keeps `mid²` well inside 64 bits. For x = {x}:
        """,
        table(["lo", "hi", "mid", "mid²", "decision"], *srows),
        f"Answer **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Count `k` up while `(k + 1)² ≤ x`."],
            "build": ["`k = 0`.", "Increase while the next square fits."],
            "complexity": ["**Time O(√x):** about 10⁸ steps at the limit. **Space O(1).**"],
            "limits": ["Linear in the answer. The yes/no question is monotone, so binary search finds the last yes in about 27 steps."],
        },
        1: {
            "idea": [
                """
                Binary search the largest `k` with `k² ≤ x` over `[0, min(x, 10⁸)]`, with `mid` rounded up so `lo = mid`
                always makes progress.
                """
            ],
            "build": ["Range `[0, min(x, 10⁸)]`.", "Upper middle.", "`mid² ≤ x` → `lo = mid`, else `hi = mid − 1`."],
            "complexity": ["**Time O(log x).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Integer square root:** binary search for the last `k` with `k² ≤ x`.
        - When the update is `lo = mid`, round `mid` up.
        - **Pitfall:** overflow in `mid * mid` without a cap or 64-bit arithmetic.
        """
    ],
}


# ---------------------------------------------------------------- perfect-square-tiles
tiles = 7056
lo, hi, prows, found = 1, min(tiles, 10**8), [], False
while lo <= hi:
    mid = (lo + hi) // 2
    sq = mid * mid
    if sq == tiles:
        prows.append((lo, hi, mid, sq, "equal: perfect square"))
        found = True
        break
    if sq < tiles:
        prows.append((lo, hi, mid, sq, "too small: go right"))
        lo = mid + 1
    else:
        prows.append((lo, hi, mid, sq, "too big: go left"))
        hi = mid - 1
EXTRA["perfect-square-tiles"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `tiles = 1` is a perfect square.
        - Non-squares fall strictly between two consecutive squares.
        - Up to 9 × 10¹⁵ tiles: squares need 64 bits.
        """
    ],
    "think": [
        HALVE,
        f"""
        **Searching a sequence that isn't stored.** "Is there a `k` with `k² = tiles`?" is an exact search in the sorted
        sequence `1², 2², 3², …`, which we never need to build: square `mid` on demand. A closed range works like the
        classic search, and the same `10⁸` cap keeps the squares safe. For {tiles}:
        """,
        table(["lo", "hi", "mid", "mid²", "decision"], *prows),
        f"Answer **{str(found).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Increase `k` until `k² ≥ tiles`; it's a perfect square exactly when `k² = tiles` at that point."],
            "build": ["`k = 1`.", "Increase while `k² < tiles`.", "Check equality."],
            "complexity": ["**Time O(√tiles):** up to 10⁸ steps. **Space O(1).**"],
            "limits": ["Linear in the side length. Binary search over the side takes about 27 steps."],
        },
        1: {
            "idea": ["Closed-range binary search for `k` in `[1, min(tiles, 10⁸)]` comparing `mid²` with `tiles`."],
            "build": ["Range of possible sides.", "Square the middle.", "Equal → true; adjust the range otherwise."],
            "complexity": ["**Time O(log tiles).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Binary search works on implicit sorted sequences**, computed on demand.
        - Exact search → closed range; boundary search → half-open or rounded mid.
        - **Pitfall:** floating-point square roots for large integers (rounding errors).
        """
    ],
}


# ---------------------------------------------------------------- insert-position
scores, it = [2, 5, 9, 14, 20, 27, 31], 15
irows, ians = lower_trace(scores, it)
EXTRA["insert-position"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Target smaller than everything: position 0.
        - Target larger than everything: position `n` (past the end).
        - Target present: its own index.
        """
    ],
    "think": [
        BOUND,
        f"""
        **Insert position = lower bound.** The position where the target is, or would be inserted, is the first index
        whose score is `≥ target`. The half-open range starts as `[0, n)` so that "insert at the end" (`n`) is a possible
        answer. For `{scores}` and target {it}:
        """,
        table(TRACE_HEAD, *irows),
        f"Answer **{ians}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan from the left for the first score `≥ target`; if none, return `n`."],
            "build": ["Scan.", "Return the first index with score ≥ target, or `n`."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Breaks the O(log n) requirement. The first index with score ≥ target is a lower bound."],
        },
        1: {
            "idea": ["Lower bound over `[0, n)`: `a[mid] < target` → `lo = mid + 1`, else `hi = mid`; return `lo`."],
            "build": ["Half-open range including `n`.", "Move right past smaller scores.", "Keep `mid` otherwise.", "Return `lo`."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Search insert position = lower bound.**
        - Use `[0, n)` so `n` is a valid answer.
        - **Pitfall:** `hi = n − 1`, which can never return `n`.
        """
    ],
}


# ---------------------------------------------------------------- first-and-last-delivery
times, tt = [2, 4, 4, 7, 7, 7, 7, 9, 12], 7
fa_rows, fa = lower_trace(times, tt)
fb_rows, fb = lower_trace(times, tt + 1)
EXTRA["first-and-last-delivery"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Empty list, or a target that doesn't appear: `[−1, −1]`.
        - One copy: first = last.
        - All entries equal to the target.
        """
    ],
    "think": [
        BOUND,
        f"""
        **Two lower bounds.** The first copy of `target` is `lower_bound(target)`. The last copy is just before the first
        value **greater** than the target, which is `lower_bound(target + 1)` for integers. If `lower_bound(target)` is
        `n` or doesn't hold the target, it's absent. For `{times}` and target {tt}:
        """,
        f"**lower_bound({tt}):**",
        table(TRACE_HEAD, *fa_rows),
        f"**lower_bound({tt + 1}):**",
        table(TRACE_HEAD, *fb_rows),
        f"Answer **[{fa}, {fb - 1}]**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan the whole list, recording the first and last positions of the target."],
            "build": ["Scan.", "Record first and last matches."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Breaks O(log n)."],
        },
        1: {
            "idea": ["Binary search for any copy, then walk left and right while neighbours equal the target."],
            "build": ["Classic binary search.", "Walk outward from the hit."],
            "complexity": ["**Time O(log n + c)** for `c` copies: O(n) when most entries are the target. **Space O(1).**"],
            "limits": ["The outward walk is linear in the number of copies. Two boundary searches find both ends in O(log n)."],
        },
        2: {
            "idea": ["`first = lower_bound(target)`; absent if it's `n` or holds another value; `last = lower_bound(target + 1) − 1`."],
            "build": ["Lower-bound helper.", "First position and the absence check.", "Last position from the next value's lower bound."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **First/last occurrence:** lower bound of `x` and of `x + 1` (or an upper bound).
        - One helper serves both searches.
        - **Pitfall:** walking outward from one hit (O(n) with many duplicates).
        """
    ],
}


# ---------------------------------------------------------------- next-gate-letter
gates, cur = "bdfffkm", "f"
grows, gi = lower_trace(list(gates), cur, strict=True)
EXTRA["next-gate-letter"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `current` at or past the last letter: wrap to the first gate.
        - Repeated letters equal to `current` must be skipped (strictly after).
        - `current` may not be a gate letter at all.
        """
    ],
    "think": [
        BOUND,
        f"""
        **Upper bound with wrap-around.** The answer is the first letter strictly greater than `current`: an **upper
        bound** (`≤` in the test). If it runs past the end (index `n`), wrap to index 0 with `index mod n`. For
        `"{gates}"` and current `{cur}`:
        """,
        table(TRACE_HEAD, *grows),
        f"Index {gi} → **`{gates[gi % len(gates)]}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan for the first letter greater than `current`; if none, return the first letter."],
            "build": ["Scan.", "Wrap if nothing is larger."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Linear; the first strictly larger letter is an upper bound, found in O(log n)."],
        },
        1: {
            "idea": ["Upper bound over `[0, n)` (`gates[mid] ≤ current` → go right), then return `gates[lo mod n]`."],
            "build": ["Half-open range.", "Skip letters ≤ current.", "Wrap with mod."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Next strictly greater element in a sorted list:** upper bound.
        - Wrap-around with `mod n`.
        - **Pitfall:** lower bound instead of upper bound (returns `current` itself).
        """
    ],
}


# ---------------------------------------------------------------- scores-in-range
sc = [70, 85, 90, 60, 85, 72, 99, 55]
s_sorted = sorted(sc)
qs = [[70, 86], [56, 59], [55, 99], [91, 98]]
EXTRA["scores-in-range"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Inclusive bounds: scores equal to `lo` or `hi` count.
        - A range containing no scores: 0.
        - Many queries (10⁵), so each must be fast after preprocessing.
        """
    ],
    "think": [
        BOUND,
        f"""
        **Sort once, then count with two bounds.** In sorted order, the scores in `[lo, hi]` form one contiguous block:
        from `lower_bound(lo)` (first score `≥ lo`) up to just before `upper_bound(hi)` (first score `> hi`). Its size is
        `upper_bound(hi) − lower_bound(lo)`. Sorted `{s_sorted}`:
        """,
        table(["query", "lower_bound(lo)", "upper_bound(hi)", "count"], *[(q, bisect_left(s_sorted, q[0]), bisect_right(s_sorted, q[1]), bisect_right(s_sorted, q[1]) - bisect_left(s_sorted, q[0])) for q in qs]),
    ],
    "approaches": {
        0: {
            "idea": ["For each query, scan all scores and count those inside the range."],
            "build": ["For each query, scan.", "Count scores in range."],
            "complexity": ["**Time O(n · q):** 10¹⁰ checks at the limits. **Space O(1)** besides the output."],
            "limits": ["Every query rescans everything. After one sort, each query is two binary searches."],
        },
        1: {
            "idea": ["Sort the scores once; for each query, `upper_bound(hi) − lower_bound(lo)`."],
            "build": ["Sort.", "Two bounds per query.", "Subtract."],
            "complexity": ["**Time O(n log n + q log n).** **Space O(n)** for the sorted copy."],
        },
    },
    "takeaways": [
        """
        - **Count values in a range:** sort once, then `upper_bound(hi) − lower_bound(lo)`.
        - Inclusive upper end → upper bound, inclusive lower end → lower bound.
        - **Pitfall:** using lower bound for `hi` (misses scores equal to `hi`).
        """
    ],
}


# ---------------------------------------------------------------- closest-prices
prices, k, xv = [1, 3, 4, 7, 8, 10, 13, 15], 3, 9
lo, hi, crows = 0, len(prices) - k, []
while lo < hi:
    mid = (lo + hi) // 2
    left_d, right_d = xv - prices[mid], prices[mid + k] - xv
    if left_d > right_d:
        crows.append((lo, hi, mid, f"{prices[mid]} (dist {left_d})", f"{prices[mid + k]} (dist {right_d})", "window start moves right"))
        lo = mid + 1
    else:
        crows.append((lo, hi, mid, f"{prices[mid]} (dist {left_d})", f"{prices[mid + k]} (dist {right_d})", "start is mid or earlier"))
        hi = mid
EXTRA["closest-prices"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `x` outside the range of prices: the window sits at one end.
        - Ties in distance: the smaller price wins.
        - Duplicates are allowed.
        """
    ],
    "think": [
        BOUND,
        f"""
        **The answer is a window.** The `k` closest prices to `x` are always `k` consecutive entries of the sorted list,
        so the question is only where the window starts: somewhere in `0 … n − k`.

        **Comparing a window with the next one.** Windows starting at `mid` and `mid + 1` differ in one element:
        `prices[mid]` leaves, `prices[mid + k]` enters. If `x − prices[mid] > prices[mid + k] − x`, the entering price is
        strictly closer, so the window should start later. Otherwise (including ties, which favour the smaller price) it
        should start at `mid` or earlier. This test flips from "go right" to "stay" exactly once, so binary search finds
        the start. For `{prices}`, `k = {k}`, `x = {xv}`:
        """,
        table(["lo", "hi", "mid", "leaving", "entering", "decision"], *crows),
        f"Window start {lo}: **{prices[lo:lo + k]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Sort all prices by `(distance, price)`, take `k`, and sort them back into increasing order."],
            "build": ["Rank by distance.", "Take `k`.", "Sort the result."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["Ignores that the answer is a contiguous window of the sorted input."],
        },
        1: {
            "idea": ["Start with the whole list and shrink it from whichever end is farther from `x` until `k` prices remain."],
            "build": ["Window = whole list.", "Drop the farther end.", "Stop at size `k`."],
            "complexity": ["**Time O(n − k).** **Space O(1)** besides the output."],
            "limits": ["Linear when `k` is small. Binary search over the window start is O(log(n − k))."],
        },
        2: {
            "idea": ["Binary search the window start in `[0, n − k]`: if the price leaving at `mid` is strictly farther than the one entering at `mid + k`, `lo = mid + 1`, else `hi = mid`."],
            "build": ["Range of starts `[0, n − k]`.", "Compare the leaving and entering prices.", "Return the window at `lo`."],
            "complexity": ["**Time O(log(n − k) + k).** **Space O(1)** besides the output."],
        },
    },
    "takeaways": [
        """
        - **k closest elements in a sorted array:** binary search the window's start.
        - Compare the element leaving with the one entering; ties keep the earlier window.
        - **Pitfall:** comparing absolute distances. With equal values on both sides of the window it stops moving:
          for `[0, 0, 0, 0, 1, 6]`, `k = 1`, `x = 5` it returns `[0]` instead of `[6]`. The signed comparison doesn't.
        """
    ],
}
