"""In-depth text for the difference-array problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

DIFF = """
**Difference arrays: describe where the values change.** Adding `v` to every position in `[l, r]` changes the
*differences* between neighbours in only two places: the value goes up by `v` at `l`, and back down by `v` at `r + 1`.
So record `diff[l] += v` and `diff[r + 1] −= v` (O(1) per update), and after all updates rebuild the actual values
with one running sum (a prefix sum over `diff`). Many range updates cost O(updates + n) instead of O(updates · n).
"""


# ---------------------------------------------------------------- stadium-sections
n, groups = 6, [[0, 2, 10], [1, 4, 5], [3, 5, 2]]
diff = [0] * (n + 1)
for l, r, p in groups:
    diff[l] += p
    diff[r + 1] -= p
run, out = 0, []
for i in range(n):
    run += diff[i]
    out.append(run)
EXTRA["stadium-sections"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A group covering a single section (`l = r`).
        - A group ending at the last section writes its `−people` at index `n`, so the array needs one extra slot.
        - Totals reach `10⁵ × 10⁴ = 10⁹`, which still fits in a 32-bit int.
        """
    ],
    "think": [
        DIFF,
        f"**Marks for `n = {n}`, groups {groups}:**",
        table(["group [l, r, people]", f"diff[l] += people", "diff[r + 1] −= people"], *[(g, f"diff[{g[0]}] += {g[2]}", f"diff[{g[1] + 1}] −= {g[2]}") for g in groups]),
        "**Rebuilding with a running sum:**",
        table(["section"] + list(range(n)), ["diff"] + diff[:n], ["running sum = fans"] + out),
    ],
    "approaches": {
        0: {
            "idea": ["For each group, add its people to every section from `l` to `r`."],
            "build": ["Zeroed answer.", "For each group, loop over its sections."],
            "complexity": ["**Time O(g · n):** 10¹⁰ additions for 10⁵ groups spanning everything. **Space O(n).**"],
            "limits": ["A wide group touches many sections one by one. Only its two ends change the differences between neighbours."],
        },
        1: {
            "idea": [
                """
                For each group, `diff[l] += people` and `diff[r + 1] −= people`. Then a running sum over `diff` gives each
                section's total.

                **Why it's right.** The running sum at section `i` adds `people` from every group with `l ≤ i` and removes
                it again for every group with `r + 1 ≤ i`, leaving exactly the groups covering `i`.
                """
            ],
            "build": ["Difference array of size `n + 1`.", "Two marks per group.", "Running sum to rebuild."],
            "complexity": ["**Time O(g + n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Many range additions, one final read:** difference array, then a prefix sum.
        - The end mark goes at `r + 1`, so allocate `n + 1` slots.
        - **Pitfall:** marking at `r` instead of `r + 1` (the last section loses the group).
        """
    ],
}


# ---------------------------------------------------------------- shuttle-seats
cap, trips = 6, [[2, 1, 5], [3, 3, 7], [4, 5, 8]]
last = max(t[2] for t in trips)
ch = [0] * (last + 1)
for p, a, b in trips:
    ch[a] += p
    ch[b] -= p
load, srows = 0, []
for m in range(last + 1):
    load += ch[m]
    srows.append((m, ch[m], load, "over capacity" if load > cap else "ok"))
EXTRA["shuttle-seats"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - At the same mark, riders get off **before** new riders get on, so a trip ending at `m` frees its seats for one
          starting at `m`.
        - A party is on board for marks `from … to − 1`, not at `to`.
        - A single party larger than the capacity fails immediately.
        """
    ],
    "think": [
        DIFF,
        """
        **Riders as range updates.** A trip `[p, from, to]` adds `p` riders to every stretch between marks `from` and
        `to − 1`: `+p` at `from`, `−p` at `to`. The load at mark `m` is the running sum, and the trip is feasible exactly
        when that running sum never exceeds the capacity.

        **Getting off before getting on.** Because the party leaves at `to` (the `−p` sits at index `to`), a trip that
        starts at the same mark is added in the same running-sum step after the subtraction is already in place, so the
        rule is handled automatically.
        """,
        f"**Load mark by mark** for capacity {cap} and trips {trips}:",
        table(["mark", "change", "load", ""], *srows),
        (f"The load never exceeds {cap}: **true**." if all(r[2] <= cap for r in srows) else
         f"At mark {next(r[0] for r in srows if r[2] > cap)} the load reaches {next(r[2] for r in srows if r[2] > cap)}, more than {cap}: **false**."),
    ],
    "approaches": {
        0: {
            "idea": ["For every mark, add up the parties on board (those with `from ≤ mark < to`) and compare with the capacity."],
            "build": ["Last mark.", "For each mark, sum the parties on board.", "Fail if over capacity."],
            "complexity": ["**Time O(M · t)** for `M` marks and `t` trips. **Space O(1).**"],
            "limits": ["Each mark rescans all trips, though the load only changes at boarding and leaving points."],
        },
        1: {
            "idea": [
                """
                Turn each trip into two events, `(from, +p)` and `(to, −p)`, sort them, and replay them, keeping the load.
                Sorting by `(mark, change)` puts negative changes first at the same mark, which is exactly "get off before
                getting on".
                """
            ],
            "build": ["Two events per trip.", "Sort by mark, leaving before boarding.", "Replay and check the load."],
            "complexity": ["**Time O(t log t).** **Space O(t)** for the events."],
            "limits": ["Sorting costs O(t log t). Marks are small integers, so a difference array indexed by mark avoids sorting."],
        },
        2: {
            "idea": [
                """
                A difference array over the marks: `change[from] += p`, `change[to] −= p`. A running sum over the marks
                gives the load; fail as soon as it exceeds the capacity.

                **Why same-mark order works.** The net change at a mark already includes everyone leaving and boarding
                there, and since leavers free their seats before boarders take them, only the net load matters.
                """
            ],
            "build": ["Array up to the last mark.", "Two marks per trip.", "Running sum; check against capacity."],
            "complexity": ["**Time O(t + M).** **Space O(M).**"],
        },
    },
    "takeaways": [
        """
        - **Intervals as +/− events:** difference array when coordinates are small, sorted events when they're large.
        - Half-open intervals `[from, to)` make "leave before board" automatic.
        - **Pitfall:** treating `to` as still on board.
        """
    ],
}


# ---------------------------------------------------------------- brightest-spot
lamps = [[2, 3], [6, 1], [4, 1], [10, 2], [5, 2]]
lo = min(p - r for p, r in lamps)
hi = max(p + r for p, r in lamps)
bright = {x: sum(1 for p, r in lamps if p - r <= x <= p + r) for x in range(lo, hi + 1)}
top = max(bright.values())
ans = min(x for x in bright if bright[x] == top)
starts = sorted(p - r for p, r in lamps)
stops = sorted(p + r + 1 for p, r in lamps)
EXTRA["brightest-spot"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The street is effectively infinite (positions up to ±2 × 10⁸), so no array over all points.
        - Ties: return the **smallest** brightest point.
        - A lamp with reach 0 lights only its own position.
        """
    ],
    "think": [
        DIFF,
        f"""
        **Brightness at every point** for `{lamps}` (lit ranges {[[p - r, p + r] for p, r in lamps]}):
        """,
        table(["point"] + list(bright.keys()), ["brightness"] + list(bright.values())),
        f"""
        The highest brightness is {top}, first reached at **{ans}**.

        **Coordinates are too large for an array**, but the difference-array idea still works on *events*: brightness
        goes up by 1 at `position − reach` and down by 1 at `position + reach + 1` (the first unlit point). Between
        events it's constant.

        **Only left edges can be the answer.** Brightness increases only at a lamp's left edge. The smallest point with
        the maximum brightness is where the brightness last went up to that maximum, so it's a left edge. So sweep the
        sorted left edges, and for each one count lamps started (`starts ≤ x`) minus lamps already ended (`stops ≤ x`).
        Sorted starts: `{starts}`; sorted stops: `{stops}`.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Only left edges can be the answer, so for each lamp's left edge count how many lamps light it; keep the brightest, ties to the smaller point."],
            "build": ["Candidates = left edges.", "Count lamps covering each candidate.", "Keep the brightest (smallest on ties)."],
            "complexity": ["**Time O(L²)** for `L` lamps: 10¹⁰ checks at the limit. **Space O(1).**"],
            "limits": ["Each candidate rescans all lamps. Sorting starts and stops lets a sweep count coverage incrementally."],
        },
        1: {
            "idea": [
                """
                Sort the left edges (`position − reach`) and the stop points (`position + reach + 1`). Sweep the left
                edges in order; for a group of equal edges ending at index `i`, advance a stop pointer `j` past stops
                `≤ x`. The brightness at `x` is `(i + 1) − j`: lamps started minus lamps finished. Keep the first maximum.

                **Why stops `≤ x` are finished.** A stop is the first point a lamp no longer lights, so a lamp with stop
                `≤ x` doesn't light `x`.
                """
            ],
            "build": ["Sorted starts and stops.", "Sweep starts, grouping equal ones.", "Advance the stop pointer.", "Brightness = started − finished; keep the first maximum."],
            "complexity": ["**Time O(L log L)** for the sorts; the sweep is O(L). **Space O(L).**"],
        },
    },
    "takeaways": [
        """
        - **Huge coordinates:** use the difference idea on sorted events (a sweep line) instead of an array.
        - The maximum of a step function is reached at a point where it steps up.
        - **Pitfall:** using `position + reach` as the stop (off by one: that point is still lit).
        """
    ],
}
