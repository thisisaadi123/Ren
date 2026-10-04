"""In-depth text for rotated-array, peak-finding and matrix-search problems (merged into their sol() calls via sol.EXTRA)."""
import heapq

from sol import EXTRA, table

ROTATED = """
**A rotated sorted array is two sorted runs.** `[21, 25, 30, 34, 2, 7, 11, 16]` is the run `21 … 34` followed by the
run `2 … 16`; every value in the first run is larger than every value in the second. Binary search still works if each
step can tell **which side of the drop** the middle is on:

- comparing `a[mid]` with `a[hi]` (the last element of the range): `a[mid] > a[hi]` means `mid` is in the first run,
  so the drop (and the minimum) is to the right; otherwise `mid` is in the second run;
- of the two halves around `mid`, **at least one is completely sorted**, and a sorted half lets us check directly
  whether the target could be inside it.
"""

SLOPE = """
**Follow the slope.** Look at `a[mid]` and its right neighbour. If the next point is **higher**, a summit must exist
to the right: walking right you either keep climbing until the end (the last point is then a summit, since beyond it is
a drop) or the trail turns down somewhere, which is a summit. So the search can discard the left part. If the next point
is lower, a summit exists at `mid` or to its left. The yes/no question "is the next point higher?" is enough to halve
the range even though the array isn't sorted.
"""

MATRIX = """
**Two kinds of sorted grid.**

- **Fully ordered rows** (each row starts after the previous one ends): read row by row, the grid is one sorted array of
  length `m · n`. Index `k` of that array is cell `(k // n, k % n)`, so a plain binary search over `0 … m·n − 1` works.
- **Rows and columns sorted separately:** start at the **top-right** corner. If the value there is too big, every value
  below it in that column is bigger still, so the whole column can go; if it's too small, everything to its left in
  that row is smaller, so the whole row can go. Each step removes a row or a column: at most `m + n` steps.
"""


def trace_rows(rows):
    return table(["lo", "hi", "mid", "a[mid]", "decision"], *rows)


# ---------------------------------------------------------------- rotation-low-point
r1 = [18, 22, 27, 31, 3, 6, 9, 14]
lo, hi, rrows = 0, len(r1) - 1, []
while lo < hi:
    mid = (lo + hi) // 2
    if r1[mid] > r1[hi]:
        rrows.append((lo, hi, mid, r1[mid], f"{r1[mid]} > a[hi] = {r1[hi]}: mid is in the first run, minimum is right of mid"))
        lo = mid + 1
    else:
        rrows.append((lo, hi, mid, r1[mid], f"{r1[mid]} ≤ a[hi] = {r1[hi]}: minimum is at mid or left of it"))
        hi = mid
EXTRA["rotation-low-point"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Not rotated at all (fully sorted): the first element.
        - Rotated by one: the minimum is the last element.
        - One reading.
        """
    ],
    "think": [
        ROTATED,
        f"""
        **Why compare with the last element, not the first.** Comparing `a[mid]` with `a[lo]` can't tell a sorted array
        (minimum at the start) from a rotated one where `mid` is still in the first run: both have `a[lo] ≤ a[mid]`.
        Comparing with `a[hi]` always works: `a[mid] > a[hi]` happens exactly when the drop lies between them. For
        `{r1}`:
        """,
        trace_rows(rrows),
        f"Minimum **{r1[lo]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Take the minimum of all readings."],
            "build": ["Scan for the minimum."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Breaks the O(log n) requirement; the comparison with the last element tells which side the drop is on."],
        },
        1: {
            "idea": [
                """
                `lo = 0`, `hi = n − 1`. While `lo < hi`: if `a[mid] > a[hi]`, the minimum is right of `mid` (`lo = mid + 1`);
                otherwise it's at `mid` or left (`hi = mid`). Return `a[lo]`.

                **Invariant.** The minimum's index is always in `lo … hi`.
                """
            ],
            "build": ["Range over the whole log.", "Compare the middle with the last element of the range.", "Keep the half with the drop."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum of a rotated sorted array:** compare `a[mid]` with `a[hi]`.
        - `hi = mid` (not `mid − 1`), because `mid` itself may be the minimum.
        - **Pitfall:** comparing with `a[lo]`, which fails on unrotated input.
        """
    ],
}


# ---------------------------------------------------------------- rotated-playlist
pl, pt = [21, 25, 30, 34, 2, 7, 11, 16], 7
lo, hi, prows, pans = 0, len(pl) - 1, [], -1
while lo <= hi:
    mid = (lo + hi) // 2
    if pl[mid] == pt:
        prows.append((lo, hi, mid, pl[mid], "found"))
        pans = mid
        break
    if pl[lo] <= pl[mid]:
        if pl[lo] <= pt < pl[mid]:
            prows.append((lo, hi, mid, pl[mid], f"left half {pl[lo]}…{pl[mid]} is sorted and contains {pt}: go left"))
            hi = mid - 1
        else:
            prows.append((lo, hi, mid, pl[mid], f"left half {pl[lo]}…{pl[mid]} is sorted but doesn't contain {pt}: go right"))
            lo = mid + 1
    else:
        if pl[mid] < pt <= pl[hi]:
            prows.append((lo, hi, mid, pl[mid], f"right half {pl[mid]}…{pl[hi]} is sorted and contains {pt}: go right"))
            lo = mid + 1
        else:
            prows.append((lo, hi, mid, pl[mid], f"right half {pl[mid]}…{pl[hi]} is sorted but doesn't contain {pt}: go left"))
            hi = mid - 1
EXTRA["rotated-playlist"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Not rotated: an ordinary sorted search.
        - Target equal to the first or last element of a half (inclusive range checks).
        - Target absent: −1.
        """
    ],
    "think": [
        ROTATED,
        f"""
        **One half is always sorted.** The drop is in at most one of the two halves around `mid`, so the other half is
        sorted. Check which (`a[lo] ≤ a[mid]` means the left half is sorted), then test whether the target lies within
        that sorted half's range: if yes, search there; if not, it can only be in the other half. For `{pl}` and target
        {pt}:
        """,
        trace_rows(prows),
        f"Answer **{pans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan the playlist for the target."],
            "build": ["Scan.", "Return the index or −1."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Breaks O(log n)."],
        },
        1: {
            "idea": ["First find the rotation point (the minimum) with the low-point search, then do an ordinary binary search in whichever of the two sorted runs could contain the target."],
            "build": ["Find the minimum's index `p`.", "Pick the run: `[p, n−1]` if target is within its range, else `[0, p−1]`.", "Classic binary search in that run."],
            "complexity": ["**Time O(log n):** two binary searches. **Space O(1).**"],
            "limits": ["Two passes; one pass can decide the half at each step directly."],
        },
        2: {
            "idea": [
                """
                One binary search: at each step, if `a[mid]` is the target, done. Otherwise identify the sorted half; if the
                target is inside its value range, keep that half, else keep the other half.

                **Why it's safe.** A sorted half contains exactly the values between its two ends, so the range check is
                decisive; the target, if present, must be in the half we keep.
                """
            ],
            "build": ["Closed range.", "Hit check.", "Find the sorted half.", "Range-check the target and keep the right half."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Search in a rotated sorted array:** one half is always sorted; range-check the target against it.
        - Use `≤` in `a[lo] ≤ a[mid]` so a one-element left half counts as sorted.
        - **Pitfall:** strict inequalities at the half's ends (misses targets equal to an end).
        """
    ],
}


# ---------------------------------------------------------------- rotated-with-repeats
sh, st = [6, 6, 6, 6, 6, 1, 3, 6, 6], 3
lo, hi, wrows, wans = 0, len(sh) - 1, [], False
while lo <= hi:
    mid = (lo + hi) // 2
    if sh[mid] == st:
        wrows.append((lo, hi, mid, sh[mid], "found"))
        wans = True
        break
    if sh[lo] == sh[mid] == sh[hi]:
        wrows.append((lo, hi, mid, sh[mid], "a[lo] = a[mid] = a[hi]: can't tell the halves apart, shrink both ends"))
        lo += 1
        hi -= 1
    elif sh[lo] <= sh[mid]:
        go_left = sh[lo] <= st < sh[mid]
        wrows.append((lo, hi, mid, sh[mid], "left half sorted: " + ("go left" if go_left else "go right")))
        if go_left:
            hi = mid - 1
        else:
            lo = mid + 1
    else:
        go_right = sh[mid] < st <= sh[hi]
        wrows.append((lo, hi, mid, sh[mid], "right half sorted: " + ("go right" if go_right else "go left")))
        if go_right:
            lo = mid + 1
        else:
            hi = mid - 1
EXTRA["rotated-with-repeats"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Many equal ids can hide where the rotation is.
        - All ids equal: the answer depends only on whether the target is that id.
        - Worst case O(n) is unavoidable (see below).
        """
    ],
    "think": [
        ROTATED,
        f"""
        **What repeats break.** When `a[lo] = a[mid] = a[hi]`, both halves look sorted: `[6, 6, 6, 6, 6, 1, 3, 6, 6]` and
        `[6, 1, 3, 6, 6, 6, 6, 6, 6]` show the same three values. No single comparison can tell where the drop is. But
        since `a[lo]` and `a[hi]` equal `a[mid]` (which isn't the target), dropping both ends loses nothing; we shrink
        by one on each side and try again. With many repeats this degrades to O(n), and that's unavoidable: a lone
        different value hidden among equal ones can't be found without looking. For `{sh}` and target {st}:
        """,
        trace_rows(wrows),
        f"Answer **{str(wans).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check whether the target is anywhere on the shelf."],
            "build": ["Linear membership test."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Always linear; the rotated binary search is O(log n) whenever repeats don't hide the drop."],
        },
        1: {
            "idea": ["The rotated search with one extra case: if `a[lo] = a[mid] = a[hi]`, move both ends inward by one; otherwise decide by the sorted half as usual."],
            "build": ["Closed range.", "Hit check.", "Ambiguous case: shrink both ends.", "Otherwise the sorted-half rule."],
            "complexity": ["**Time O(log n)** typically, **O(n)** in the worst case. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Rotated search with duplicates:** when the three probes are equal, shrink both ends.
        - Worst case O(n) can't be avoided with duplicates.
        - **Pitfall:** applying the no-duplicates rule blindly (it can pick the wrong half).
        """
    ],
}


# ---------------------------------------------------------------- low-point-with-repeats
lr = [4, 4, 5, 6, 1, 2, 2, 4, 4, 4]
lo, hi, lrows = 0, len(lr) - 1, []
while lo < hi:
    mid = (lo + hi) // 2
    if lr[mid] > lr[hi]:
        lrows.append((lo, hi, mid, lr[mid], f"> a[hi] = {lr[hi]}: minimum right of mid"))
        lo = mid + 1
    elif lr[mid] < lr[hi]:
        lrows.append((lo, hi, mid, lr[mid], f"< a[hi] = {lr[hi]}: minimum at mid or left"))
        hi = mid
    else:
        lrows.append((lo, hi, mid, lr[mid], f"= a[hi] = {lr[hi]}: ambiguous, drop hi (its value is still at mid)"))
        hi -= 1
EXTRA["low-point-with-repeats"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties between `a[mid]` and `a[hi]` hide the side of the drop.
        - All readings equal.
        - Not rotated.
        """
    ],
    "think": [
        ROTATED,
        f"""
        **Handling a tie safely.** When `a[mid] = a[hi]`, the minimum could be on either side (`[3, 1, 3, 3, 3]` vs
        `[3, 3, 3, 1, 3]`). But removing `hi` is safe: its value also sits at `mid`, which stays in the range, so if
        `a[hi]` were the minimum value, it would still be present. Shrink `hi` by one and continue. For `{lr}`:
        """,
        trace_rows(lrows),
        f"Minimum **{lr[lo]}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Scan for the first drop (a reading smaller than the previous one); if none, the first reading is the minimum."],
            "build": ["Scan for a drop.", "Return the reading after it, or the first one."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Always linear; the comparison with `a[hi]` halves the range except on ties."],
        },
        1: {
            "idea": ["The low-point search with a third case: on `a[mid] = a[hi]`, do `hi −= 1`."],
            "build": ["Range over the log.", "Bigger → go right; smaller → keep left including mid.", "Equal → drop `hi`."],
            "complexity": ["**Time O(log n)** typically, **O(n)** worst case (many equal readings). **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum of a rotated array with duplicates:** on a tie with `a[hi]`, drop `hi`.
        - Dropping is safe because the same value remains at `mid`.
        - **Pitfall:** dropping `lo` instead (it can remove the only copy of the minimum).
        """
    ],
}


# ---------------------------------------------------------------- mountain-top
mt = [1, 4, 6, 9, 13, 11, 7, 2]
lo, hi, mrows = 0, len(mt) - 1, []
while lo < hi:
    mid = (lo + hi) // 2
    if mt[mid] < mt[mid + 1]:
        mrows.append((lo, hi, mid, mt[mid], f"next is higher ({mt[mid + 1]}): top is right of mid"))
        lo = mid + 1
    else:
        mrows.append((lo, hi, mid, mt[mid], f"next is lower ({mt[mid + 1]}): top is at mid or left"))
        hi = mid
EXTRA["mountain-top"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The top is never at either end (guaranteed).
        - The smallest mountain has 3 points.
        - Strictly rising then strictly falling: no plateaus.
        """
    ],
    "think": [
        SLOPE,
        f"""
        **A monotone yes/no question.** "Is the next point higher?" is **yes** for every point before the top and **no**
        from the top onward, so the top is the first "no", a boundary that binary search finds. For `{mt}`:
        """,
        trace_rows(mrows),
        f"Top at index **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Walk up while the next point is higher; stop at the top."],
            "build": ["Walk while rising.", "Return the stopping index."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Linear; the slope test lets binary search find the boundary in O(log n)."],
        },
        1: {
            "idea": ["`lo < hi`: if `a[mid] < a[mid + 1]`, `lo = mid + 1`, else `hi = mid`. Return `lo`."],
            "build": ["Range over the trail.", "Compare mid with its right neighbour.", "Keep the side with the top."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Peak of a mountain array:** binary search on "is the next one higher?".
        - `mid + 1` is always valid because `mid < hi`.
        - **Pitfall:** `hi = mid − 1` when going left (can skip the top).
        """
    ],
}


# ---------------------------------------------------------------- any-summit
hs = [2, 5, 3, 1, 4, 8, 6, 7, 0]
summits = [i for i in range(len(hs)) if (i == 0 or hs[i] > hs[i - 1]) and (i == len(hs) - 1 or hs[i] > hs[i + 1])]
lo, hi, arows = 0, len(hs) - 1, []
while lo < hi:
    mid = (lo + hi) // 2
    if hs[mid] < hs[mid + 1]:
        arows.append((lo, hi, mid, hs[mid], f"uphill to {hs[mid + 1]}: a summit exists to the right"))
        lo = mid + 1
    else:
        arows.append((lo, hi, mid, hs[mid], f"downhill to {hs[mid + 1]}: a summit exists at mid or left"))
        hi = mid
EXTRA["any-summit"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Any summit is accepted; there may be several.
        - The first and last points count as summits if their one neighbour is lower (the edges are drops).
        - One point: it's a summit.
        """
    ],
    "think": [
        SLOPE,
        f"""
        **Not sorted, still halvable.** `{hs}` has summits at {summits}. The array isn't sorted, yet each comparison with
        the right neighbour still guarantees a summit on one side, so half the range can always be discarded:
        """,
        trace_rows(arows),
        f"Summit at index **{lo}** (height {hs[lo]}).",
    ],
    "approaches": {
        0: {
            "idea": ["Scan for the first point higher than the next one; if none, the last point is a summit."],
            "build": ["Scan for a downturn.", "Return it, or the last index."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Linear; following the uphill side halves the range each step."],
        },
        1: {
            "idea": [
                """
                Same loop as the mountain top: go right when the next point is higher, otherwise keep `mid`.

                **Invariant.** The range `lo … hi` always contains a summit (the boundaries act as drops), so when it shrinks
                to one point, that point is a summit.
                """
            ],
            "build": ["Range over the trail.", "Uphill → right; downhill → keep mid.", "Return `lo`."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Find any peak:** binary search uphill; no sorting needed.
        - The guarantee comes from the boundaries being lower than everything.
        - **Pitfall:** comparing with the left neighbour at `mid = 0` (out of range).
        """
    ],
}


# ---------------------------------------------------------------- mountain-lookups
el, targets = [1, 3, 6, 9, 12, 10, 6, 4, 3, 0], [6, 3, 11, 0]
top = el.index(max(el))
look = []
for t in targets:
    left = next((i for i in range(top + 1) if el[i] == t), None)
    right = next((i for i in range(top, len(el)) if el[i] == t), None)
    ans = left if left is not None else (right if right is not None else -1)
    look.append((t, left if left is not None else "—", right if right is not None else "—", ans))
EXTRA["mountain-lookups"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A height can appear on both slopes; the **smallest** index (on the rising slope) wins.
        - The top's height appears once.
        - Up to 10⁵ lookups: each must be O(log n) after preprocessing.
        """
    ],
    "think": [
        SLOPE,
        f"""
        **Three binary searches.** First find the top (the slope test). The left slope `0 … top` is increasing and the
        right slope `top … n − 1` is decreasing, so each is a sorted array. For each target, search the rising slope first
        (it holds the smaller indices); only if it's not there, search the falling slope (with comparisons reversed). For
        `{el}` (top at {top}):
        """,
        table(["target", "on the rising slope", "on the falling slope", "answer"], *look),
    ],
    "approaches": {
        0: {
            "idea": ["For each target, scan the whole trail for its first occurrence."],
            "build": ["For each target, scan.", "First match or −1."],
            "complexity": ["**Time O(n · q):** 10¹⁰ at the limits. **Space O(1)** besides the output."],
            "limits": ["Every lookup rescans; one preprocessing step can make each lookup fast."],
        },
        1: {
            "idea": ["Record each height's first index in a hash map (scanning left to right), then answer each lookup in O(1)."],
            "build": ["Map height → first index.", "Look up each target."],
            "complexity": ["**Time O(n + q)** expected. **Space O(n).**"],
            "limits": ["O(n) extra memory; the mountain's two sorted slopes allow O(log n) lookups with O(1) memory."],
        },
        2: {
            "idea": [
                """
                Find the top with the slope test. For each target: lower bound on the rising slope `[0, top]`; if it hits the
                target, that's the answer. Otherwise, on the falling slope `[top, n)`, find the first index whose height is
                `≤` the target and check it.
                """
            ],
            "build": ["Find the top.", "Lower bound on the rising slope.", "Mirrored search on the falling slope.", "Collect answers."],
            "complexity": ["**Time O(log n)** per lookup plus O(log n) for the top. **Space O(1)** besides the output."],
        },
    },
    "takeaways": [
        """
        - **Search in a mountain array:** find the peak, then binary search each monotone side.
        - Search the left side first when the smallest index is wanted.
        - **Pitfall:** using the same comparison on the falling side (it's sorted the other way).
        """
    ],
}


# ---------------------------------------------------------------- seat-map-lookup
g2, t2 = [[2, 4, 7, 9], [12, 15, 18, 20], [23, 26, 31, 35]], 18
m2, n2 = len(g2), len(g2[0])
lo, hi, srows, sfound = 0, m2 * n2 - 1, [], False
while lo <= hi:
    mid = (lo + hi) // 2
    v = g2[mid // n2][mid % n2]
    if v == t2:
        srows.append((lo, hi, mid, f"({mid // n2}, {mid % n2})", v, "found"))
        sfound = True
        break
    srows.append((lo, hi, mid, f"({mid // n2}, {mid % n2})", v, "go right" if v < t2 else "go left"))
    if v < t2:
        lo = mid + 1
    else:
        hi = mid - 1
EXTRA["seat-map-lookup"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One row or one column.
        - Target smaller than the first seat or larger than the last.
        - O(log(m·n)) is required.
        """
    ],
    "think": [
        MATRIX,
        f"""
        **One long sorted array.** For the grid {g2}, flattened index `k` is cell `(k // {n2}, k % {n2})`. Binary search
        over `0 … {m2 * n2 - 1}` for target {t2}:
        """,
        table(["lo", "hi", "mid", "cell", "value", "decision"], *srows),
        f"Answer **{str(sfound).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every seat."],
            "build": ["Scan all cells."],
            "complexity": ["**Time O(m · n).** **Space O(1).**"],
            "limits": ["Ignores all the ordering."],
        },
        1: {
            "idea": ["Staircase walk from the top-right corner, discarding a row or a column per step."],
            "build": ["Start top-right.", "Too big → left; too small → down."],
            "complexity": ["**Time O(m + n).** **Space O(1).**"],
            "limits": ["O(m + n) is more than O(log(m·n)); this grid's stronger ordering allows a full binary search."],
        },
        2: {
            "idea": ["Binary search over `0 … m·n − 1`, reading the value at `(mid // n, mid % n)`."],
            "build": ["Dimensions.", "Closed range over flattened indices.", "Map mid to a cell and compare."],
            "complexity": ["**Time O(log(m·n)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Fully ordered grid = one sorted array:** index `k` ↔ `(k // n, k % n)`.
        - The staircase works for weaker orderings but is slower here.
        - **Pitfall:** dividing by the number of rows instead of the number of columns.
        """
    ],
}


# ---------------------------------------------------------------- staircase-search
g3, t3 = [[2, 5, 9, 14], [4, 7, 11, 18], [6, 10, 15, 21], [12, 16, 19, 25]], 10
r, c, crows, cfound = 0, len(g3[0]) - 1, [], False
while r < len(g3) and c >= 0:
    v = g3[r][c]
    if v == t3:
        crows.append((r, c, v, "found"))
        cfound = True
        break
    if v > t3:
        crows.append((r, c, v, f"{v} > {t3}: everything below in column {c} is bigger, drop the column"))
        c -= 1
    else:
        crows.append((r, c, v, f"{v} < {t3}: everything left in row {r} is smaller, drop the row"))
        r += 1
EXTRA["staircase-search"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Rows can start below where the previous row ended, so the grid isn't one sorted array.
        - Duplicates are allowed.
        - The target may be off the grid's value range.
        """
    ],
    "think": [
        MATRIX,
        f"""
        **Why the top-right corner.** At the top-right, moving left makes values smaller and moving down makes them
        bigger: exactly one direction for each outcome of the comparison. (The top-left corner wouldn't work: both moves
        increase the value.) For the grid {g3} and target {t3}:
        """,
        table(["row", "col", "value", "decision"], *crows),
        f"Answer **{str(cfound).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every cell."],
            "build": ["Scan all cells."],
            "complexity": ["**Time O(m · n).** **Space O(1).**"],
            "limits": ["Uses none of the ordering."],
        },
        1: {
            "idea": ["Binary search each row for the target."],
            "build": ["For each row, lower bound for the target.", "Check equality."],
            "complexity": ["**Time O(m log n).** **Space O(1).**"],
            "limits": ["Uses only the row ordering; the column ordering lets each step discard a whole row or column."],
        },
        2: {
            "idea": ["Start at the top-right; too big → move left (drop the column), too small → move down (drop the row), equal → found."],
            "build": ["Top-right corner.", "Compare and move left or down.", "Stop when found or out of the grid."],
            "complexity": ["**Time O(m + n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Rows and columns sorted:** staircase search from the top-right (or bottom-left) corner.
        - Each comparison eliminates a whole row or column.
        - **Pitfall:** starting at the top-left, where both moves go up in value.
        """
    ],
}


# ---------------------------------------------------------------- kth-in-sorted-grid
g4, k4 = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]], 7
n4 = len(g4)


def count_at_most(v):
    r, c, total = n4 - 1, 0, 0
    while r >= 0 and c < n4:
        if g4[r][c] <= v:
            total += r + 1
            c += 1
        else:
            r -= 1
    return total


lo, hi, krows = g4[0][0], g4[-1][-1], []
while lo < hi:
    mid = (lo + hi) // 2
    cnt = count_at_most(mid)
    krows.append((lo, hi, mid, cnt, "≥ k: answer ≤ mid" if cnt >= k4 else "< k: answer > mid"))
    if cnt >= k4:
        hi = mid
    else:
        lo = mid + 1
EXTRA["kth-in-sorted-grid"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Duplicates count separately.
        - `k = 1` is the top-left value; `k = n²` the bottom-right.
        - Values can be negative; the search is over values, not indices.
        """
    ],
    "think": [
        MATRIX,
        f"""
        **Binary search on the value.** Let `count(v)` = number of cells `≤ v`. It grows with `v`, and the k-th smallest
        value is the smallest `v` with `count(v) ≥ k`. Counting is a staircase walk from the bottom-left: if the cell is
        `≤ v`, the whole column above it is too (add `row + 1`, move right); otherwise move up. That's O(n) per count.

        **Why the answer is a real grid value.** The smallest `v` with `count(v) ≥ k` must be a value in the grid: at any
        `v` not in the grid, `count(v − 1) = count(v)`, so a smaller `v` would also qualify. For the grid {g4} and
        `k = {k4}`:
        """,
        table(["lo", "hi", "mid", "count(mid)", "decision"], *krows),
        f"Answer **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Flatten the grid, sort, take the k-th value."],
            "build": ["Collect all values.", "Sort.", "Index `k − 1`."],
            "complexity": ["**Time O(n² log n).** **Space O(n²).**"],
            "limits": ["Uses O(n²) memory and ignores the ordering."],
        },
        1: {
            "idea": ["Merge the sorted rows with a min-heap: start with each row's first cell; pop `k` times, pushing the next cell in the popped row each time."],
            "build": ["Heap of each row's first value.", "Pop the smallest, push the next in its row.", "The k-th pop is the answer."],
            "complexity": ["**Time O(k log n).** **Space O(n).**"],
            "limits": ["With `k` up to `n²`, that's O(n² log n) time. Binary search on the value needs only O(n log range)."],
        },
        2: {
            "idea": ["Binary search the value range `[grid[0][0], grid[n−1][n−1]]`: if `count(mid) ≥ k`, `hi = mid`, else `lo = mid + 1`. `count` is the staircase walk."],
            "build": ["Staircase count of cells ≤ v.", "Binary search for the smallest v with count ≥ k."],
            "complexity": ["**Time O(n · log(range)):** about 300 × 31 steps. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **k-th smallest in a sorted matrix:** binary search on the value + staircase counting.
        - "Smallest value with count ≥ k" is always an element of the grid.
        - **Pitfall:** `(lo + hi) // 2` with negative values in languages that truncate toward zero (use a floor midpoint).
        """
    ],
}
