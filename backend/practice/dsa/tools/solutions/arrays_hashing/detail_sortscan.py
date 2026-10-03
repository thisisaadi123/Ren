"""In-depth text for the sort-then-scan problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

SORTSCAN = """
**Why sort first?** Sorting puts related values next to each other: the closest pair becomes a pair of neighbours,
equal values form blocks, consecutive numbers form runs. A question about *all pairs* (O(n²)) becomes a question about
*neighbours* (O(n)) after an O(n log n) sort. And when the values are bounded, counting into buckets can replace the
sort entirely.
"""

# ---------------------------------------------------------------- closest-heights
hs = [170, 182, 165, 180, 176, 190]
srt = sorted(hs)
gaps = [srt[i + 1] - srt[i] for i in range(len(srt) - 1)]
EXTRA["closest-heights"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Two players: their difference is the answer.
        - Equal heights: the answer is 0.
        - Heights up to 10⁹, so differences fit in a 32-bit int.
        """
    ],
    "think": [
        SORTSCAN,
        f"""
        **Only neighbours matter after sorting.** In sorted order, any pair `s[i] ≤ s[j]` with `j > i + 1` has the
        neighbours `s[i], s[i+1], …, s[j]` in between, and its gap is the **sum** of their neighbour gaps, so it's at
        least the smallest one of them. The minimum over all pairs is therefore a neighbour gap.

        `{hs}` sorted is `{srt}`:
        """,
        table(["neighbours", "gap"], *[(f"{srt[i]}, {srt[i + 1]}", gaps[i]) for i in range(len(gaps))]),
        f"Smallest gap **{min(gaps)}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Compare every pair of players and keep the smallest absolute difference."],
            "build": ["Two nested loops.", "Track the minimum difference."],
            "complexity": ["**Time O(n²):** 5 × 10⁹ pairs for `n = 10⁵`. **Space O(1).**"],
            "limits": ["Most pairs can't be the closest. After sorting, only neighbours need checking."],
        },
        1: {
            "idea": ["Sort, then take the minimum difference between consecutive heights (the argument above shows it's the overall minimum)."],
            "build": ["Sort.", "Minimum of neighbour gaps."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the sorted copy."],
        },
    },
    "takeaways": [
        """
        - **Closest pair in one dimension:** sort, check neighbours.
        - A far pair's gap is a sum of neighbour gaps, so it can't be smaller than all of them.
        - **Pitfall:** taking the gap between the first two sorted values only.
        """
    ],
}


# ---------------------------------------------------------------- influence-score
cit = [3, 0, 6, 1, 5, 4, 8]
cs = sorted(cit, reverse=True)
n = len(cit)
bucket = [0] * (n + 1)
for c in cit:
    bucket[min(c, n)] += 1
brows, at_least, h_ans = [], 0, None
for h in range(n, -1, -1):
    at_least += bucket[h]
    ok = at_least >= h
    brows.append((h, bucket[h], at_least, "yes → answer" if ok and h_ans is None else ("" if h_ans is not None else "no")))
    if ok and h_ans is None:
        h_ans = h
        break
EXTRA["influence-score"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - All papers with 0 citations: the score is 0.
        - The score can never exceed the number of papers `n`.
        - Very large citation counts (up to 10⁹) behave like `n` for this question.
        """
    ],
    "think": [
        SORTSCAN,
        f"""
        **Reading the score from a sorted list.** Sort citations from most to least. The `k`-th paper (1-based) has at
        least as many citations as every paper after it, so "at least `k` papers with at least `k` citations" holds
        exactly when the `k`-th paper has `≥ k` citations. The score is the largest such `k`. For `{cit}` sorted
        descending `{cs}`:
        """,
        table(["k (papers)", "k-th paper's citations", "≥ k?"], *[(k + 1, cs[k], "yes" if cs[k] >= k + 1 else "no") for k in range(n)]),
        f"""
        The last "yes" is at `k = {h_ans}`, so the score is **{h_ans}**.

        **Counting instead of sorting.** The score is at most `n`, so a paper with more than `n` citations counts the
        same as one with exactly `n`. Count papers into buckets `0 … n` (capping at `n`), then walk `h` down from `n`,
        accumulating "papers with at least `h` citations"; the first `h` where that count reaches `h` is the score:
        """,
        table(["h", "papers with exactly h (capped)", "papers with ≥ h", "≥ h papers?"], *brows),
    ],
    "approaches": {
        0: {
            "idea": ["Try each `h` from `n` down to 0 and count the papers with at least `h` citations; return the first `h` that works."],
            "build": ["For each `h` from high to low, count qualifying papers.", "Return the first `h` that works."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Each candidate recounts all papers. Sorting or bucketing answers every `h` together."],
        },
        1: {
            "idea": ["Sort descending; advance `h` while the `(h + 1)`-th paper has at least `h + 1` citations."],
            "build": ["Sort descending.", "Increase `h` while the next paper still qualifies."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the sorted copy."],
            "limits": ["Sorting by exact citation counts is more than needed: only counts up to `n` matter, which buckets handle in O(n)."],
        },
        2: {
            "idea": [
                """
                Bucket papers by `min(citations, n)`. Walk `h` from `n` down to 0, adding `bucket[h]` to a running count of
                papers with at least `h` citations. Return the first `h` with count `≥ h`.

                **Why the first such `h` is the answer.** We're scanning from the largest possible score downwards, so the
                first `h` that works is the largest.
                """
            ],
            "build": ["Buckets `0 … n`, capping citations at `n`.", "Walk `h` downward with a running count.", "Return the first `h` reached."],
            "complexity": ["**Time O(n).** **Space O(n)** for the buckets."],
        },
    },
    "takeaways": [
        """
        - **h-index style questions:** sort descending and compare position with value, or bucket counts capped at `n`.
        - Cap values at the largest answer that matters to enable counting.
        - **Pitfall:** off-by-one between 0-based positions and the 1-based paper count.
        """
    ],
}


# ---------------------------------------------------------------- longest-streak
days = [100, 4, 200, 1, 3, 2, 101, 102, 50]
have = set(days)
lrows = []
for d in sorted(have):
    if d - 1 in have:
        lrows.append((d, f"{d - 1} is present: not a start, skip", "—"))
        continue
    end = d
    while end + 1 in have:
        end += 1
    lrows.append((d, f"start: walk to {end}", end - d + 1))
best = max(r[2] for r in lrows if r[2] != "—")
EXTRA["longest-streak"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No days at all: the answer is 0.
        - Repeated days don't extend a streak.
        - Negative day numbers are fine; only consecutiveness matters.
        """
    ],
    "think": [
        SORTSCAN,
        f"""
        **Two ways to see runs.** After sorting, a streak is a block where each value is the previous plus one
        (duplicates skipped). Without sorting, a hash set answers "is `d + 1` present?" in O(1).

        **Avoid re-walking.** Walking forward from every day would re-count the same streak from each of its members
        (O(n²) in the worst case). Only walk from a **streak start**: a day `d` whose `d − 1` is absent. Then every day is
        visited by exactly one walk. For `{days}`:
        """,
        table(["day (distinct)", "decision", "streak length"], *lrows),
        f"Longest streak **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["From every day, count upward while the next day appears in the list (searching the list each time)."],
            "build": ["For each day, extend while `d + length` is in the list.", "Track the longest."],
            "complexity": ["**Time O(n³)** worst case: walks of length O(n), each step a linear search. **Space O(1).**"],
            "limits": ["Linear searches, and every member of a streak walks it again."],
        },
        1: {
            "idea": ["Sort; walk once, extending the current streak when a value is the previous plus one, skipping duplicates, and restarting otherwise."],
            "build": ["Handle the empty list.", "Sort.", "Extend, skip duplicates, or restart."],
            "complexity": ["**Time O(n log n).** **Space O(n)** for the sorted copy."],
            "limits": ["The sort is the only O(n log n) part; a hash set gives O(1) lookups and O(n) overall."],
        },
        2: {
            "idea": [
                """
                Put all days in a set. For each day `d` that starts a streak (`d − 1` not in the set), walk `d + 1, d + 2, …`
                while present, and record the length.

                **Why it's O(n).** The walks only start at streak starts, and the streaks are disjoint, so each day is
                visited by at most one walk.
                """
            ],
            "build": ["Hash set of days.", "Skip days that aren't streak starts.", "Walk forward from each start."],
            "complexity": ["**Time O(n)** expected. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Longest consecutive run:** hash set, and only start counting at a run's first value.
        - Sorting gives the same answer in O(n log n) with simpler logic.
        - **Pitfall:** counting duplicates as part of a streak.
        """
    ],
}
