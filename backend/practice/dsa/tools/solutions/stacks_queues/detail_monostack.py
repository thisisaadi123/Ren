"""In-depth text for the monotonic-stack problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

MONO = """
**The monotonic stack idea.** Keep a stack of items that are still **waiting for an answer** (for example "the next
warmer day"). When a new item arrives, it answers every waiting item it beats; those are popped. Because each popped
item was beaten by the new one, the items left on the stack are always in sorted order (that's the "monotonic" part),
so the new item only needs to look at the top.

**Why it's O(n).** Every item is pushed once and popped at most once, so all the `while` loops together do at most
`n` pops, even though a single step may pop many.
"""


# ---------------------------------------------------------------- warmer-day-wait
temps = [30, 28, 31, 27, 27, 29, 33, 26]
wait, st, wrows = [0] * len(temps), [], []
for i, t in enumerate(temps):
    settled = []
    while st and temps[st[-1]] < t:
        j = st.pop()
        wait[j] = i - j
        settled.append(f"day {j} ({temps[j]}°) waits {i - j}")
    st.append(i)
    wrows.append((i, f"{t}°", "; ".join(settled) or "—", [f"{k}:{temps[k]}°" for k in st]))
EXTRA["warmer-day-wait"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Strictly warmer: an equal temperature doesn't end the wait.
        - Days never followed by a warmer one keep 0.
        - Temperatures range only over −100 … 100, which a value-indexed approach can use.
        """
    ],
    "think": [
        MONO,
        f"""
        **Waiting days.** The stack holds days still waiting for something warmer; their temperatures never increase from
        bottom to top (a warmer day would have settled the ones before it). When a new day is warmer than the top, it is
        the first warmer day for that top day: record the wait and pop, repeatedly. For `{temps}`:
        """,
        table(["day", "temp", "days settled now", "stack after (day:temp)"], *wrows),
        f"Waits: **{wait}**.",
    ],
    "approaches": {
        0: {
            "idea": ["From each day, scan forward to the first warmer day."],
            "build": ["For each day, scan forward.", "Record the distance to the first warmer day."],
            "complexity": ["**Time O(n²)** (e.g. decreasing temperatures). **Space O(1)** besides the output."],
            "limits": ["Scans the same stretch from many days. A stack answers each day exactly once, when its warmer day arrives."],
        },
        1: {
            "idea": [
                """
                Walk from the back, remembering for each temperature the nearest later day with it (`nxt[t]`). A day's
                answer is the smallest `nxt[t']` over all warmer temperatures `t'`, which is at most 200 values to check.
                """
            ],
            "build": ["Array `nxt` over the 201 temperatures.", "From the back, take the nearest warmer day.", "Record this day's temperature."],
            "complexity": ["**Time O(n · 201).** **Space O(201).**"],
            "limits": ["Depends on the small temperature range; with arbitrary values it fails. The stack works for any values in O(n)."],
        },
        2: {
            "idea": [
                """
                Scan forward with a stack of waiting days. Each new day pops every waiting day that is colder, setting its
                wait, then joins the stack.

                **Invariant.** Temperatures on the stack are non-increasing from bottom to top, and every day still on the
                stack hasn't seen a warmer day yet.
                """
            ],
            "build": ["Empty stack, waits all 0.", "Pop colder days and set their waits.", "Push today."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Next greater element:** stack of waiting indices; a new value settles all smaller ones on top.
        - Store **indices**, so distances can be computed.
        - **Pitfall:** `≤` instead of `<` (equal temperatures aren't warmer).
        """
    ],
}


# ---------------------------------------------------------------- next-bigger-on-the-ring
ring = [4, 2, 7, 3, 7, 1]
n = len(ring)
res, st, rrows = [-1] * n, [], []
for i in range(2 * n):
    v = ring[i % n]
    got = []
    while st and ring[st[-1]] < v:
        j = st.pop()
        res[j] = v
        got.append(f"tile {j} → {v}")
    if i < n:
        st.append(i)
    rrows.append((i, i % n, v, "; ".join(got) or "—", "push" if i < n else "second lap: no push", list(st)))
EXTRA["next-bigger-on-the-ring"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The maximum value (and its copies) gets −1.
        - Wrap-around: the answer for a tile near the end may come from the beginning.
        - One tile: −1.
        """
    ],
    "think": [
        MONO,
        f"""
        **Handling the circle.** Walk the tiles **twice** (`i` from 0 to `2n − 1`, tile `i mod n`). During the first lap,
        push every tile; during the second lap, only answer waiting tiles, without pushing again. Any tile's next bigger
        value is at most `n − 1` steps away, so two laps reach it. For `{ring}`:
        """,
        table(["step", "tile", "value", "answers given", "push?", "stack after"], *rrows),
        f"Answers: **{res}**.",
    ],
    "approaches": {
        0: {
            "idea": ["From each tile, walk up to `n − 1` steps clockwise (with `mod n`) until a bigger value appears."],
            "build": ["For each tile, walk around the ring.", "Record the first bigger value."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the output."],
            "limits": ["Walks overlap heavily. A stack over two laps answers each tile once."],
        },
        1: {
            "idea": [
                """
                Monotonic stack of waiting tile indices over two laps. Pop and answer smaller tiles whenever a bigger value
                appears; push only during the first lap.

                **Why two laps suffice.** The second lap shows every tile again, so a tile waiting at the end of the first
                lap sees all tiles after it around the ring.
                """
            ],
            "build": ["Loop `i` over `2n` steps using `i mod n`.", "Answer smaller waiting tiles.", "Push only when `i < n`."],
            "complexity": ["**Time O(n):** `2n` steps, each tile pushed and popped once. **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Circular next greater:** iterate twice, push only in the first pass.
        - Two laps are enough because the answer is within `n − 1` steps.
        - **Pitfall:** pushing again in the second lap (answers would be overwritten).
        """
    ],
}


# ---------------------------------------------------------------- price-streak-tracker
prices = [7, 3, 4, 4, 8, 2, 9]
st, prows = [], []
for p in prices:
    streak, absorbed = 1, []
    while st and st[-1][0] <= p:
        q, s = st.pop()
        streak += s
        absorbed.append(f"({q}, {s})")
    st.append((p, streak))
    prows.append((p, ", ".join(absorbed) or "—", streak, [f"({a}, {b})" for a, b in st]))
EXTRA["price-streak-tracker"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - "At most" includes equal prices: an equal earlier price extends the streak.
        - The first day's streak is 1.
        - Up to 10⁵ calls, so each must be fast on average.
        """
    ],
    "think": [
        MONO,
        f"""
        **Absorbing earlier days.** When today's price is at least an earlier day's price, today's streak covers that
        day **and everything that day's streak covered**. So once a day is covered, it never needs to be looked at again:
        store `(price, streak)` pairs on a stack and fold covered days into today's streak. Recording `{prices}`:
        """,
        table(["price", "pairs absorbed", "streak returned", "stack after (price, streak)"], *prows),
    ],
    "approaches": {
        0: {
            "idea": ["Store every price; for each new price, walk backwards counting days until one is higher."],
            "build": ["List of all prices.", "Append today.", "Count backwards until a higher price."],
            "complexity": ["**Time O(n)** per call in the worst case, O(n²) total. **Space O(n).**"],
            "limits": ["Rising prices make every call walk the whole history. Absorbed days never need to be walked again."],
        },
        1: {
            "idea": [
                """
                Keep a stack of `(price, streak)`. For a new price, start at 1 and pop every pair with price `≤` today's,
                adding its streak. Push `(price, streak)` and return the streak.

                **Invariant.** Prices on the stack strictly decrease from bottom to top, and each pair's streak counts the
                days it absorbed.
                """
            ],
            "build": ["Empty stack.", "Pop and add streaks of pairs with price ≤ today's.", "Push today's pair."],
            "complexity": ["**Time O(1)** amortised per call (each day is pushed once and popped once). **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Stock span:** stack of (price, span) pairs; a new price absorbs smaller-or-equal ones.
        - Storing the span with each pair lets one pop stand for many days.
        - **Pitfall:** using `<` when equal prices should count.
        """
    ],
}


# ---------------------------------------------------------------- trim-the-reading
num, k = "4205318", 3
st, kk, trows = [], k, []
for d in num:
    popped = []
    while kk and st and st[-1] > d:
        popped.append(st.pop())
        kk -= 1
    st.append(d)
    trows.append((d, ", ".join(popped) or "—", kk, "".join(st)))
final = "".join(st[:-kk] if kk else st).lstrip("0") or "0"
EXTRA["trim-the-reading"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Leading zeros after erasing are dropped; an empty or all-zero result is `"0"`.
        - Non-decreasing digits (like `"12345"`): erase from the end.
        - `k = n`: everything erased, `"0"`.
        """
    ],
    "think": [
        MONO,
        """
        **Greedy from the left.** All results have the same length, so the smallest one has the smallest first digit, then
        the smallest second digit, and so on. Scanning left to right, if the last kept digit is bigger than the incoming
        digit, erasing the kept one makes the number smaller in an earlier position, which always beats anything later. So
        pop bigger digits while erasures remain. The kept digits end up non-decreasing; if erasures are left over, cut them
        from the end (the largest digits).
        """,
        f"**Trace on `{num}`, k = {k}:**",
        table(["digit", "erased now", "erasures left", "kept so far"], *trows),
        f"Result **`{final}`**.",
    ],
    "approaches": {
        0: {
            "idea": ["`k` times, erase the first digit that's bigger than the next one (or the last digit if none is), then strip leading zeros."],
            "build": ["Repeat `k` times: find the first drop, erase it.", "Strip leading zeros."],
            "complexity": ["**Time O(n · k).** **Space O(n).**"],
            "limits": ["Each round rescans from the start. A stack finds all the drops in one pass."],
        },
        1: {
            "idea": [
                """
                Push digits onto a stack; before pushing, pop while erasures remain and the top is bigger than the new
                digit. Cut any remaining erasures from the end, then strip leading zeros (empty → `"0"`).
                """
            ],
            "build": ["Stack of kept digits.", "Pop bigger digits while `k > 0`.", "Cut leftovers from the end.", "Strip leading zeros."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Smallest number after removing k digits:** monotonic increasing stack, pop larger tops.
        - Leftover removals come off the end.
        - **Pitfall:** forgetting to strip leading zeros or to return `"0"` for an empty result.
        """
    ],
}


# ---------------------------------------------------------------- low-high-between
vals = [2, 4, 3, 6, 5, 1, 7]
mid, st, lrows, found = float("-inf"), [], [], False
for v in reversed(vals):
    if v < mid:
        lrows.append((v, "—" if mid == float("-inf") else mid, list(st), f"{v} < {mid}: found low < in-between < high"))
        found = True
        break
    popped = []
    while st and st[-1] < v:
        mid = st.pop()
        popped.append(mid)
    st.append(v)
    lrows.append((v, "—" if mid == float("-inf") else mid, list(st), f"pops {popped}: new in-between candidate" if popped else "push"))
EXTRA["low-high-between"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Fewer than three values: false.
        - Strict inequalities: equal values don't count.
        - Sorted (increasing or decreasing) input never works.
        """
    ],
    "think": [
        MONO,
        """
        **Scan from the right, tracking the best "in-between" value.** We want `values[i] < values[k] < values[j]` with
        `i < j < k`. Walking from the right, keep a stack of values seen so far and `mid` = the largest value that already
        has a **bigger value to its left** among those seen (a valid `values[k]` with its `values[j]`). Whenever a new value
        is bigger than the stack top, the popped values become in-between candidates for this new high; keep the largest
        in `mid`. If a value is ever smaller than `mid`, it's the low: done.

        **Why the largest popped value is the right `mid`.** A larger in-between value only makes it easier for some
        earlier value to be smaller than it.
        """,
        f"**Trace on `{vals}` (right to left):**",
        table(["value", "mid (best in-between)", "stack after", "what happens"], *lrows),
        f"Answer: **{str(found).lower()}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every triple `i < j < k`."],
            "build": ["Three nested loops.", "Check `values[i] < values[k] < values[j]`."],
            "complexity": ["**Time O(n³).** **Space O(1).**"],
            "limits": ["Cubic. The best low for a given high is simply the smallest value before it."],
        },
        1: {
            "idea": ["For each `j`, the best `i` is the minimum value before `j`; then search after `j` for a value strictly between that minimum and `values[j]`."],
            "build": ["Running minimum.", "For each `j` above it, scan to the right.", "Check for a value in between."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Still scans the rest of the array for every high. A right-to-left stack tracks the best in-between value incrementally."],
        },
        2: {
            "idea": [
                """
                From the right: if the value is below `mid`, return true. Otherwise pop every stack value smaller than it
                (each becomes `mid` in turn, ending with the largest), then push it.

                **Invariant.** `mid` is the largest value to the right that has a larger value between it and the current
                position, and the stack holds the values to the right that are still candidates for the high.
                """
            ],
            "build": ["`mid = −∞`, empty stack.", "From the right: check `v < mid`.", "Pop smaller values into `mid`.", "Push `v`."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **"1-3-2" patterns:** scan from the right with a stack, tracking the best middle value.
        - Popped values become candidates; keep the largest.
        - **Pitfall:** scanning left to right with a single minimum (it can miss the right high).
        """
    ],
}


# ---------------------------------------------------------------- strongest-crew-stretch
sg = [3, 1, 6, 4, 5, 2]
n2 = len(sg)
P = [0]
for v in sg:
    P.append(P[-1] + v)
left = []
for i in range(n2):
    j = i
    while j > 0 and sg[j - 1] >= sg[i]:
        j -= 1
    left.append(j)
right = []
for i in range(n2):
    j = i
    while j < n2 - 1 and sg[j + 1] >= sg[i]:
        j += 1
    right.append(j)
crows = [(i, sg[i], f"{left[i]} … {right[i]}", P[right[i] + 1] - P[left[i]], sg[i] * (P[right[i] + 1] - P[left[i]])) for i in range(n2)]
best = max(r[4] for r in crows)
EXTRA["strongest-crew-stretch"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One worker: power = strength².
        - Equal strengths: each crew must be counted with a consistent "weakest" choice.
        - Power reaches about `10⁶ × 10¹¹ = 10¹⁷`: use 64 bits.
        """
    ],
    "think": [
        MONO,
        """
        **Fix the weakest worker.** Every crew has a weakest member. For a worker `w` taken as the weakest, the best crew
        is the **widest** stretch around `w` where nobody is weaker: extending further only adds positive strengths to the
        sum while the weakest stays `w`. So the answer is the maximum over workers of `strength[w] × (sum of that widest
        stretch)`.

        **Finding the widest stretch.** Its edges are the previous weaker worker and the next weaker worker, which
        monotonic stacks find in O(n). Prefix sums give the stretch's sum in O(1). Both edges stop only at a **strictly**
        weaker worker, so workers of equal strength are included; several equal workers may share the same widest crew,
        which is fine because only the maximum power is needed.
        """,
        f"**For `{sg}`:**",
        table(["worker", "strength", "widest stretch where they're weakest", "sum", "power"], *crows),
        f"Best power **{best}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try every crew, keeping a running minimum and sum while extending to the right."],
            "build": ["Every start.", "Extend with running min and sum.", "Track the best power."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
            "limits": ["Quadratic. Each crew's power is determined by its weakest worker, so it's enough to consider one widest crew per worker."],
        },
        1: {
            "idea": [
                """
                Prefix sums. A left-to-right stack (popping workers with strength `≥` the current one) gives each worker's
                left edge: just after the previous strictly weaker worker. A right-to-left stack gives the right edge the
                same way. Power =
                `strength[i] × (P[right + 1] − P[left])`; take the maximum.
                """
            ],
            "build": ["Prefix sums.", "Left boundaries with a stack.", "Right boundaries with a stack, computing powers.", "Maximum power."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **"min × something" over subarrays:** fix each element as the minimum; its widest range comes from previous/next smaller elements.
        - Prefix sums turn range sums into O(1).
        - For a maximum, equal values may share a range; when **counting** ranges, make one side strict and the other
          not, so each range is counted once.
        """
    ],
}


# ---------------------------------------------------------------- who-can-you-see
hs = [5, 3, 4, 4, 1, 6]
res2, st, hrows = [0] * len(hs), [], []
for i in range(len(hs) - 1, -1, -1):
    h = hs[i]
    seen = []
    while st and st[-1] < h:
        seen.append(st.pop())
        res2[i] += 1
    blocker = None
    if st:
        res2[i] += 1
        blocker = st[-1]
        if st[-1] == h:
            st.pop()
    st.append(h)
    hrows.append((i, h, seen or "—", blocker if blocker is not None else "—", res2[i], list(st)))
EXTRA["who-can-you-see"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The last person sees nobody.
        - Equal heights block each other: two people of the same height see each other, but nobody behind them.
        - Everyone between must be shorter than **both** people.
        """
    ],
    "think": [
        MONO,
        """
        **Scan from the back, keeping who is still visible.** Walking from the back of the line, keep a stack of heights
        that someone further forward could still see; it's strictly decreasing from bottom to top. For the person at `i`:

        - every stacked person **shorter** than them is visible to them, and is now hidden from everyone further forward:
          pop and count;
        - the next stacked person (taller or equal) is visible too (everyone between is shorter than both), so count one
          more; if they're the **same height**, they're hidden from now on, so pop them;
        - then push this person.
        """,
        f"**Trace on `{hs}` (from the back):**",
        table(["i", "height", "shorter ones seen (popped)", "next taller/equal seen", "count", "stack after"], *hrows),
        f"Counts: **{res2}**.",
    ],
    "approaches": {
        0: {
            "idea": ["For each person, walk backwards through the line tracking the tallest person in between; count `j` when that tallest is shorter than both; stop once someone at least as tall as person `i` appears."],
            "build": ["For each person, walk toward the back.", "Count visible people.", "Stop at the first blocker."],
            "complexity": ["**Time O(n²).** **Space O(1)** besides the output."],
            "limits": ["Quadratic on, e.g., decreasing heights. A stack from the back shares the work."],
        },
        1: {
            "idea": ["From the back, pop and count shorter people, count the next taller-or-equal person (popping them if equal), then push the current person."],
            "build": ["Empty stack.", "Pop shorter people, counting them.", "Count the blocker; pop it if equal.", "Push."],
            "complexity": ["**Time O(n).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Visibility counting:** monotonic stack from the far end; popped people are visible and then hidden.
        - Handle equal heights explicitly (visible once, then blocking).
        - **Pitfall:** forgetting the one taller person who is always visible after the pops.
        """
    ],
}
