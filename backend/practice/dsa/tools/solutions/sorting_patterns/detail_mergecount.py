"""In-depth text for the counting-while-merging problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

CROSS = """
**Counting pairs with merge sort.** Questions like "how many pairs `i < j` have `a[i] > a[j]`" split nicely:

- pairs with both positions in the **left half** and pairs in the **right half** are counted recursively;
- pairs that **cross** (`i` in the left half, `j` in the right half) only care about the *values*, not their order
  inside each half, so both halves may be sorted first, and with sorted halves the crossing pairs are counted with a
  linear sweep.

Each level of the recursion does O(n) counting plus O(n) merging, over `log n` levels: **O(n log n)** instead of O(n²).
"""


def inversion_levels(a):
    """Bottom-up merge levels with the number of crossing inversions found at each merge."""
    runs = [[x] for x in a]
    rows = []
    while len(runs) > 1:
        nxt, found = [], []
        for i in range(0, len(runs), 2):
            if i + 1 == len(runs):
                nxt.append(runs[i])
                continue
            L, R = runs[i], runs[i + 1]
            c = sum(1 for x in L for y in R if x > y)
            found.append(f"{L}+{R}: {c}")
            nxt.append(sorted(L + R))
        rows.append((" | ".join(" ".join(map(str, r)) for r in runs), "; ".join(found)))
        runs = nxt
    return rows


# ---------------------------------------------------------------- out-of-order-pairs
rk = [4, 1, 3, 9, 2]
pairs = [(rk[i], rk[j]) for i in range(len(rk)) for j in range(i + 1, len(rk)) if rk[i] > rk[j]]
EXTRA["out-of-order-pairs"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal ranks are **not** out of order (strictly larger is required).
        - Sorted input: 0 pairs; reverse-sorted: `n(n − 1)/2`.
        - Only positions matter for "earlier/later"; values decide "out of order".
        """
    ],
    "think": [
        CROSS,
        f"""
        **The crossing count during a merge.** Merge the sorted halves by taking the smaller front each time. When a
        value from the **right** half is taken while `mid − i` values remain in the left half, all of those remaining
        left values are larger and came earlier: that's `mid − i` out-of-order pairs at once. Taking left values first on
        ties keeps equal values from counting.

        For `{rk}` the out-of-order pairs are {pairs} ({len(pairs)}). The table merges neighbouring runs bottom-up and
        shows the crossing pairs found at each merge. The recursive version splits slightly differently, but every pair
        is still counted exactly once, so the total is the same:
        """,
        table(["runs before merging", "crossing pairs found"], *inversion_levels(rk)),
    ],
    "approaches": {
        0: {
            "idea": ["Check every pair `i < j` and count those with `ranks[i] > ranks[j]`."],
            "build": ["Two nested loops.", "Count out-of-order pairs."],
            "complexity": ["**Time O(n²)**: fine for `n ≤ 1000` (5 × 10⁵ pairs), too slow for large inputs. **Space O(1).**"],
            "limits": ["Quadratic. Merge sort counts all crossing pairs of a merge in linear time."],
        },
        1: {
            "idea": [
                """
                Merge sort that returns the count: `count = left count + right count + crossing count`. During the merge,
                each time a right value is taken, add `mid − i` (the left values still waiting, all larger).
                """
            ],
            "build": ["Recursive sort returning a count.", "During the merge, add `mid − i` for each right value taken.", "Copy back."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the buffer."],
        },
    },
    "takeaways": [
        """
        - **Inversion count:** merge sort, adding `mid − i` when a right element is taken.
        - Take left elements first on ties, so equal values aren't counted.
        - **Pitfall:** 32-bit counts for large inputs (up to about `n²/2`).
        """
    ],
}


# ---------------------------------------------------------------- fewest-neighbour-swaps
hs = [3, 1, 2, 5, 4, 2]
inv = sum(1 for i in range(len(hs)) for j in range(i + 1, len(hs)) if hs[i] > hs[j])
EXTRA["fewest-neighbour-swaps"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal heights may stay in either order, so equal pairs never need a swap.
        - Already sorted: 0.
        - The count reaches about `n²/2 = 5 × 10⁹`: use 64 bits.
        """
    ],
    "think": [
        CROSS,
        f"""
        **Why neighbour swaps = out-of-order pairs.** Swapping two neighbours changes the relative order of exactly
        those two students and no one else. If they were out of order, the number of out-of-order pairs drops by exactly
        one; otherwise it rises by one. The sorted line has zero out-of-order pairs, so at least that many swaps are
        needed, and bubble sort shows that many suffice (it only ever swaps out-of-order neighbours).

        For `{hs}` there are {inv} out-of-order pairs, so **{inv}** swaps.
        """,
        table(["runs before merging", "crossing pairs found"], *inversion_levels(hs)),
    ],
    "approaches": {
        0: {
            "idea": ["Bubble sort, counting every swap. Each swap fixes exactly one out-of-order pair, so the count is the answer."],
            "build": ["Bubble passes.", "Swap out-of-order neighbours and count."],
            "complexity": ["**Time O(n²).** **Space O(n)** for the copy."],
            "limits": ["Performs every swap one by one; counting inversions with merge sort gives the same number in O(n log n)."],
        },
        1: {
            "idea": ["Count inversions with merge sort (add `mid − i` whenever a right value is taken). That count is the minimum number of neighbour swaps."],
            "build": ["Merge sort returning a count.", "Add `mid − i` on right picks.", "Return the total (64-bit)."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum adjacent swaps to sort = number of inversions.**
        - Each adjacent swap changes the inversion count by exactly one.
        - **Pitfall:** counting equal heights as inversions.
        """
    ],
}


# ---------------------------------------------------------------- big-drops
pr = [7, 3, 10, 2, 1, 6]
drops = [(pr[i], pr[j]) for i in range(len(pr)) for j in range(i + 1, len(pr)) if pr[i] > 2 * pr[j]]
EXTRA["big-drops"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative prices are allowed: `2 · price` can then be smaller than the price.
        - `2 · price` can reach 2³², past 32 bits, so compute it in 64 bits.
        - The condition is strict: exactly double doesn't count.
        """
    ],
    "think": [
        CROSS,
        f"""
        **Counting crossing drops with a separate sweep.** Unlike plain inversions, the condition `a[i] > 2·a[j]` isn't
        the same comparison the merge uses, so count first, then merge. With both halves sorted, for each left value `x`
        (in increasing order) advance a pointer `j` in the right half while `x > 2·right[j]`; then `j − mid` right values
        are big drops for `x`. Because left values increase, `j` never moves back: the sweep is linear.

        For `{pr}` the big drops are {drops}: **{len(drops)}**.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Check every pair of days and count those with `prices[i] > 2·prices[j]`."],
            "build": ["Two nested loops.", "Count big drops (64-bit doubling)."],
            "complexity": ["**Time O(n²):** 1.25 × 10⁹ pairs for `n = 5 × 10⁴`. **Space O(1).**"],
            "limits": ["Quadratic. Sorted halves let a two-pointer sweep count all crossing drops in linear time."],
        },
        1: {
            "idea": [
                """
                Merge sort returning a count. After sorting both halves, sweep: for each left value, advance `j` while it's
                more than double `a[j]`, adding `j − mid`. Then merge the halves normally.

                **Why the sweep pointer only moves forward.** If `x > 2·a[j]` holds for some left value, it also holds for
                every larger left value.
                """
            ],
            "build": ["Recursive sort returning a count.", "Two-pointer sweep for crossing drops.", "Standard merge."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Pairs with a condition other than `>`:** count with a separate sweep over sorted halves, then merge.
        - Use 64-bit arithmetic for `2 · value`.
        - **Pitfall:** counting during the merge itself, which uses the wrong comparison.
        """
    ],
}


# ---------------------------------------------------------------- shorter-behind
sh = [5, 2, 6, 1, 3]
cnt = [sum(1 for y in sh[i + 1:] if y < x) for i, x in enumerate(sh)]
EXTRA["shorter-behind"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Strictly shorter: equal heights don't count.
        - The last person always gets 0.
        - Heights can be negative (down to −10⁴), so a Fenwick tree needs an offset.
        """
    ],
    "think": [
        CROSS,
        f"""
        **Inversions per person.** Here each person needs their **own** count. For `{sh}`:
        """,
        table(["person", "height", "shorter people behind"], *[(i, sh[i], cnt[i]) for i in range(len(sh))]),
        """
        **Two fast ways.**

        - **Merge sort on positions:** sort the positions by height. When a person from the left half is placed, every
          right-half person already placed is shorter and stands behind them: credit the left person with that number.
        - **Fenwick tree from the back:** walk from the back of the queue, keeping counts of the heights seen so far
          (everyone behind). For each person, query how many seen heights are smaller, then add their height. A Fenwick
          tree answers "how many values below h" and adds a value in O(log R).
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each person, scan everyone behind and count the shorter ones."],
            "build": ["For each person, scan behind.", "Count shorter heights."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the output."],
            "limits": ["Each scan restarts. Merge sort or a Fenwick tree shares the work."],
        },
        1: {
            "idea": [
                """
                Merge sort an array of positions by height. During each merge, when the next left-half person is placed,
                the right-half people already placed (`j − mid` of them) are shorter and behind: add that to their count.
                """
            ],
            "build": ["Positions array.", "Merge by height, crediting left people with `j − mid`.", "Copy back."],
            "complexity": ["**Time O(n log n).** **Space O(n).**"],
            "limits": ["More bookkeeping (sorting positions). With a small height range, a Fenwick tree is simpler."],
        },
        2: {
            "idea": [
                """
                Walk from the back. For each person, query the Fenwick tree for how many heights below theirs have been
                added (everyone behind), record it, then add their height. Heights are shifted by 10001 so they're positive
                indices.
                """
            ],
            "build": ["Fenwick tree over the shifted height range.", "From the back: query, record, add."],
            "complexity": ["**Time O(n log R)** with `R` = 20001 possible heights. **Space O(R).**"],
        },
    },
    "takeaways": [
        """
        - **Per-element inversion counts:** merge sort on positions, or a Fenwick tree scanning from the back.
        - Shift negative values to positive indices for the Fenwick tree.
        - **Pitfall:** querying "≤ h" instead of "< h" (counts equal heights).
        """
    ],
}
