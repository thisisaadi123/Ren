"""In-depth text for the k-sum problems (merged into their sol() calls via sol.EXTRA)."""
from itertools import combinations

from sol import EXTRA, table

FIX_ONE = """
**Fix one, squeeze two.** Three unknowns are hard, two are easy. Sort the values. Fix the first element `a[i]`; the
other two must come from positions after `i`, and their sum must relate to `target − a[i]`. That's the sorted
pair-sum problem, solved by two pointers `j = i + 1` and `k = n − 1` moving inward. Doing this for every `i` costs
`n` squeezes of O(n) each: **O(n²)** instead of O(n³).

**Why sorting is allowed.** The questions are about *sets* of three positions (their values' sum), not their order,
so rearranging the array doesn't change which value-triples exist. Requiring `i < j < k` in the sorted array picks each
set of positions exactly once.
"""


# ---------------------------------------------------------------- three-weights
w, target = [12, 3, 7, 1, 9, 20], 28
a = sorted(w)
rows, found = [], None
for i in range(len(a) - 2):
    j, k, tried = i + 1, len(a) - 1, []
    while j < k:
        s = a[i] + a[j] + a[k]
        tried.append(f"{a[j]}+{a[k]}={a[j] + a[k]}")
        if s == target:
            found = (a[i], a[j], a[k])
            break
        if s < target:
            j += 1
        else:
            k -= 1
    rows.append((a[i], target - a[i], ", ".join(tried), "found" if found else "no pair"))
    if found:
        break
EXTRA["three-weights"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - "Different" means three different positions; two equal weights at different positions are fine.
        - Exactly three weights: just check their sum.
        - All weights are positive here, but the method works for any sign.
        """
    ],
    "think": [
        FIX_ONE,
        f"""
        **Trace** for target {target} on sorted `{a}` (for each fixed weight, the pair we need and the pairs the squeeze
        tries):
        """,
        table(["fixed", "pair must sum to", "pairs tried", "result"], *rows),
        f"Found {found[0]} + {found[1]} + {found[2]} = {target}: **true**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every triple of positions `i < j < k`. With `n ≤ 500` that's about 2 × 10⁷ triples: borderline, and it doesn't scale."],
            "build": ["Three nested loops.", "Return true on an exact sum."],
            "complexity": ["**Time O(n³).** **Space O(1).**"],
            "limits": ["For each pair `(i, j)` it searches the third weight linearly. After sorting, the last two can be found together by a squeeze."],
            "lines": {
                "loops": "Every set of three different positions, each exactly once.",
                "hit": "An exact total.",
                "ret": "No triple works.",
            },
        },
        1: {
            "idea": [
                """
                Sort. For each `i`, squeeze `j` and `k` over the rest: equal means done, too small moves `j` right, too big
                moves `k` left (the pair-sum argument: the dropped element has no partner left that works).
                """
            ],
            "build": ["Sort.", "Fix `a[i]`.", "Squeeze the remaining two toward `target − a[i]`."],
            "complexity": ["**Time O(n²):** `n` squeezes of O(n). **Space O(1)** besides the sort."],
            "lines": {
                "sort": "Order the weights so the squeeze can tell which way to move.",
                "fix": "The smallest of the three positions; the other two come after it, so no position is used twice.",
                "squeeze": "Pair-sum with two pointers on the part after `i`: exact means true, too small means the left weight is useless, too big means the right weight is useless.",
                "ret": "No fixed weight found a pair.",
            },
        },
    },
    "takeaways": [
        """
        - **k-sum:** sort, fix `k − 2` elements, squeeze the last two: O(n^(k−1)).
        - The fixed element is the smallest position, so positions never repeat.
        - **Pitfall:** letting `j` start at 0 instead of `i + 1`.
        """
    ],
}


# ---------------------------------------------------------------- zero-sum-triples
vals = [-1, 0, 1, 2, -1, -4, 2, -2]
z = sorted(vals)
zrows = []
for i in range(len(z) - 2):
    if i and z[i] == z[i - 1]:
        zrows.append((i, z[i], "same value as the previous fixed one: skip", "—"))
        continue
    if z[i] > 0:
        zrows.append((i, z[i], "positive: every triple from here sums above 0, stop", "—"))
        break
    j, k, got = i + 1, len(z) - 1, []
    while j < k:
        s = z[i] + z[j] + z[k]
        if s < 0:
            j += 1
        elif s > 0:
            k -= 1
        else:
            got.append([z[i], z[j], z[k]])
            j += 1
            while j < k and z[j] == z[j - 1]:
                j += 1
            k -= 1
    zrows.append((i, z[i], "squeeze", ", ".join(map(str, got)) or "none"))
EXTRA["zero-sum-triples"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Repeated values can form the same triple in several ways; each different triple is reported once.
        - `[0, 0, 0]` is a valid triple when there are three zeros.
        - No triple: return an empty list.
        """
    ],
    "think": [
        FIX_ONE,
        """
        **Duplicates.** After sorting, equal values sit next to each other, which makes duplicates easy to avoid:

        1. **Skip a fixed value equal to the previous fixed value.** Every triple it could start was already found by the
           first copy (that copy had at least as many elements after it).
        2. **After a hit, move `j` past equal values.** The same `a[i]` and `a[j]` would force the same `a[k]` again.
           (`k` just moves one step; the next differing `a[j]` changes the needed `a[k]` anyway.)

        **Early stop.** If the fixed value is positive, the two values after it are at least as large, so every sum is
        positive: stop.
        """,
        f"**Trace on sorted `{z}`:**",
        table(["i", "fixed", "action", "triples found"], *zrows),
    ],
    "approaches": {
        0: {
            "idea": ["Check every triple of positions; when one sums to 0, add its sorted values to a set (which removes duplicates). Sort the set at the end."],
            "build": ["Three nested loops.", "Store sorted value-triples in a set.", "Sort the results."],
            "complexity": ["**Time O(n³):** about 1.3 × 10⁹ triples for `n = 2000`. **Space O(t)** for the `t` triples found."],
            "limits": ["Cubic, and it relies on a set to undo duplicates afterwards. Sorting first lets the squeeze find each triple once."],
            "lines": {
                "init": "A set of value-triples, so the same triple is stored once.",
                "loops": "Every set of three positions.",
                "keep": "A zero sum: store its values in increasing order.",
                "ret": "The distinct triples, sorted.",
            },
        },
        1: {
            "idea": [
                """
                Sort. For each `i` (skipping repeated fixed values and stopping at the first positive one), squeeze `j` and
                `k`: below 0 move `j`, above 0 move `k`, on 0 record the triple, then move `j` past its duplicates and `k`
                one step.

                **Output order for free.** Fixed values increase with `i`, and within one `i` the hits come with increasing
                `a[j]`, so the triples are produced already sorted.
                """
            ],
            "build": ["Sort.", "Skip repeated fixed values; stop at a positive one.", "Squeeze toward 0.", "On a hit, record and skip duplicates of `a[j]`."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the sort and the output."],
            "lines": {
                "sort": "Equal values become neighbours, and the squeeze can tell which way to move.",
                "fix": "Skip a fixed value equal to the previous one: all its triples were already found.",
                "stop": "A positive smallest value makes every remaining sum positive.",
                "squeeze": "Too small: move `j` right. Too big: move `k` left.",
                "hit": "Record the triple, then move `j` past equal values (and `k` one step) so the same triple isn't recorded again.",
                "ret": "All different triples, already in sorted order.",
            },
        },
    },
    "takeaways": [
        """
        - **3-sum with distinct answers:** sort, fix, squeeze, and skip equal neighbours.
        - Sorted order makes both duplicate skipping and sorted output automatic.
        - **Pitfall:** skipping duplicates of the fixed value by comparing with the **next** element (that drops valid triples like `[-1, -1, 2]`).
        """
    ],
}


# ---------------------------------------------------------------- triples-under-a-cap
cv, cap = [3, -1, 5, 0, 2, -4], 2
c = sorted(cv)
crows, total = [], 0
for i in range(len(c) - 2):
    j, k = i + 1, len(c) - 1
    while j < k:
        s = c[i] + c[j] + c[k]
        if s < cap:
            total += k - j
            crows.append((c[i], c[j], c[k], s, f"< {cap}: all k in {j + 1}..{k} work with this j → +{k - j}", total))
            j += 1
        else:
            crows.append((c[i], c[j], c[k], s, f"≥ {cap}: this k is too big for every remaining j → k−1", total))
            k -= 1
brute = sum(1 for t in combinations(cv, 3) if sum(t) < cap)
EXTRA["triples-under-a-cap"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Strictly less than `cap`: a sum equal to `cap` doesn't count.
        - The count can reach `C(2000, 3) ≈ 1.3 × 10⁹`, so use 64 bits.
        - Negative values and a negative cap are allowed.
        """
    ],
    "think": [
        FIX_ONE,
        """
        **Counting a whole range at once.** Fix `a[i]` and look at the pair `(j, k)`. If `a[i] + a[j] + a[k] < cap`,
        then replacing `a[k]` by any smaller value `a[j+1] … a[k−1]` keeps the sum below the cap. So **all `k − j` triples
        `(i, j, j+1) … (i, j, k)` qualify**: add them in one step and move `j` on. If the sum is too big, `a[k]` is too
        big for this `j` and for every larger `j` too, so move `k` left.
        """,
        f"**Trace on sorted `{c}`, cap {cap}:**",
        table(["a[i]", "a[j]", "a[k]", "sum", "decision", "total"], *crows),
        f"Total **{total}** (checked against all triples: {brute}).",
    ],
    "approaches": {
        0: {
            "idea": ["Check every triple of positions and count those below the cap."],
            "build": ["Three nested loops.", "Count sums below `cap`."],
            "complexity": ["**Time O(n³):** 1.3 × 10⁹ triples for `n = 2000`. **Space O(1).**"],
            "limits": ["Counts qualifying triples one by one, even when a whole range of third values qualifies together."],
            "lines": {
                "init": "The count (64-bit).",
                "loops": "Every set of three positions; count it if its sum is below the cap.",
                "ret": "The count.",
            },
        },
        1: {
            "idea": [
                """
                Sort. For each `i`, start `j = i + 1`, `k = n − 1`. If the sum is below the cap, add `k − j` and move `j`
                right; otherwise move `k` left.

                **Why nothing is missed or double-counted.** Each triple `(i, j, m)` with `m > j` that qualifies is counted
                exactly when `j` is the middle pointer and `m ≤ k` at that moment; `k` only moved past values that are too
                big for this `j` and all later ones.
                """
            ],
            "build": ["Sort.", "Fix `a[i]`.", "Squeeze, adding `k − j` whenever the sum is below the cap."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the sort."],
            "lines": {
                "sort": "Sorting doesn't change which sets of positions qualify, and it lets ranges be counted at once.",
                "fix": "The smallest of the three positions.",
                "squeeze": "Pointers over the part after `i`.",
                "count": "Below the cap: every third value from `j + 1` to `k` works with this `j`, so add `k − j` and move `j`. Otherwise `a[k]` is too big for any remaining `j`: move `k`.",
                "ret": "The total, 64-bit.",
            },
        },
    },
    "takeaways": [
        """
        - **Counting k-sum below a bound:** when a pair works, the whole range between the pointers works.
        - Add `k − j` at once instead of counting one by one.
        - **Pitfall:** 32-bit counts; using `≤` when the bound is strict.
        """
    ],
}


# ---------------------------------------------------------------- triples-in-a-band
bv, low, high = [4, -3, 1, 6, -1, 2], 0, 5
bs = sorted(bv)


def at_most(x):
    t = 0
    for i in range(len(bs) - 2):
        j, k = i + 1, len(bs) - 1
        while j < k:
            if bs[i] + bs[j] + bs[k] <= x:
                t += k - j
                j += 1
            else:
                k -= 1
    return t


upto_high, below_low = at_most(high), at_most(low - 1)
inband = [t for t in combinations(bv, 3) if low <= sum(t) <= high]
EXTRA["triples-in-a-band"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Both ends of the band are inclusive.
        - `low = high`: count triples with exactly that sum.
        - Counts reach `C(1500, 3) ≈ 5.6 × 10⁸`; use 64 bits.
        """
    ],
    "think": [
        FIX_ONE,
        f"""
        **Two-sided → two one-sided counts.** For integers, `low ≤ sum ≤ high` means "`sum ≤ high`" but not
        "`sum ≤ low − 1`". So

        `count in band = atMost(high) − atMost(low − 1)`,

        and `atMost(x)` is the counting squeeze from "triples under a cap", with `≤` instead of `<`.

        For `{bv}` and band [{low}, {high}]: atMost({high}) = {upto_high}, atMost({low - 1}) = {below_low}, so the answer is
        **{upto_high - below_low}**. Listing them directly gives {len(inband)}: {', '.join(str(list(t)) for t in inband)}.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Check every triple of positions and count the sums inside the band."],
            "build": ["Three nested loops.", "Count sums with `low ≤ s ≤ high`."],
            "complexity": ["**Time O(n³):** 5.6 × 10⁸ triples for `n = 1500`. **Space O(1).**"],
            "limits": ["One by one is too slow; the counting squeeze adds whole ranges at once, and two one-sided counts handle the band."],
            "lines": {
                "init": "The count.",
                "loops": "Every set of three positions; count it if its sum is inside the band.",
                "ret": "The count.",
            },
        },
        1: {
            "idea": [
                """
                Sort once. `atMost(x)` counts triples with sum `≤ x` using the range-counting squeeze. Return
                `atMost(high) − atMost(low − 1)`.

                **Why subtraction works.** Every triple with sum `≤ high` either has sum `≤ low − 1` (below the band) or
                lies in the band, never both.
                """
            ],
            "build": ["Sort.", "`atMost(x)` with the counting squeeze.", "Subtract the two counts."],
            "complexity": ["**Time O(n²):** two squeezing passes. **Space O(1)** besides the sort."],
            "lines": {
                "sort": "One sort serves both counts.",
                "count": "`atMost(x)`: for each fixed element, squeeze; when the sum is at most `x`, all `k − j` third values work, so add them and move `j`, else move `k`.",
                "ret": "At most `high`, minus at most `low − 1`, leaves exactly the band.",
            },
        },
    },
    "takeaways": [
        """
        - **Two-sided bounds = difference of two one-sided counts** (`≤ high` minus `≤ low − 1`).
        - Reuse one counting routine for both.
        - **Pitfall:** subtracting `atMost(low)`, which wrongly excludes sums equal to `low`.
        """
    ],
}


# ---------------------------------------------------------------- closest-triple-sum
tv, tt = [4, -2, 9, 1, -6, 7], 6
ts = sorted(tv)
trows, best = [], ts[0] + ts[1] + ts[2]
for i in range(len(ts) - 2):
    j, k, seen = i + 1, len(ts) - 1, []
    while j < k:
        s = ts[i] + ts[j] + ts[k]
        seen.append(s)
        if (abs(s - tt), s) < (abs(best - tt), best):
            best = s
        if s < tt:
            j += 1
        elif s > tt:
            k -= 1
        else:
            break
    trows.append((ts[i], ", ".join(map(str, seen)), best))
    if best == tt:
        break
EXTRA["closest-triple-sum"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Ties: equally close sums → return the smaller one.
        - An exact match ends the search.
        - Exactly three values: their sum is the answer.
        """
    ],
    "think": [
        FIX_ONE,
        """
        **Squeezing toward a target instead of hitting it.** With `a[i]` fixed and `s = a[i] + a[j] + a[k]`:

        - `s < target`: every other third value for this `j` is at most `a[k]`, giving sums at most `s`: no closer
          from below. `a[j]` is finished; move `j` right.
        - `s > target`: symmetric; move `k` left.
        - `s = target`: distance 0, stop.

        Record every sum visited; the best one is the answer.
        """,
        f"**Trace for target {tt}** on sorted `{ts}` (sums visited for each fixed value):",
        table(["fixed", "sums visited", "best so far"], *trows),
        f"Answer **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Check every triple and keep the sum that's closest, comparing `(distance, sum)` so ties prefer the smaller sum."],
            "build": ["Three nested loops.", "Compare by `(distance, sum)`."],
            "complexity": ["**Time O(n³):** 1.7 × 10⁸ triples for `n = 1000`. **Space O(1).**"],
            "limits": ["Cubic. The squeeze visits only the sums that could still be closest."],
            "lines": {
                "init": "No triple seen yet.",
                "loops": "Every set of three positions.",
                "better": "Closer wins; on equal distance the smaller sum wins.",
                "ret": "The best sum.",
            },
        },
        1: {
            "idea": [
                """
                Sort. Start `best` at any triple (the first three). For each `i`, squeeze `j`, `k`, recording each sum if
                it's better and moving toward the target; return immediately on an exact hit.

                **Why the best triple is visited.** Every triple not visited contains an element that was dropped while the
                sum was on the wrong side of the target, so its sum is no closer than one that was recorded.
                """
            ],
            "build": ["Sort.", "Initial best from the first three values.", "Fix `a[i]`, squeeze toward the target, record improvements."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the sort."],
            "lines": {
                "sort": "Sorting lets each comparison with the target rule out a whole range.",
                "fix": "The smallest of the three positions.",
                "squeeze": "The other two pointers over the part after `i`.",
                "better": "Keep the sum if it's closer, or equally close and smaller.",
                "move": "Below the target, move `j` up; above, move `k` down; exact, return.",
                "ret": "The best sum.",
            },
        },
    },
    "takeaways": [
        """
        - **Closest k-sum:** fix, squeeze toward the target, record every visit.
        - Tie rules as a tuple key `(distance, value)`.
        - **Pitfall:** initialising `best` with a huge sentinel in 32 bits; start with a real triple instead.
        """
    ],
}
