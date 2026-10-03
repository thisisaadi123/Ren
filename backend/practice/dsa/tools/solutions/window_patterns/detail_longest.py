"""Fuller explanations for the longest-valid-window problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, Row, fig, table


def trace(values, ok, show=lambda l, r: ""):
    """Rows of the two-pointer run: R, value added, L after fixing, window, length, best (+ an optional state column)."""
    rows, l, best = [], 0, 0
    for r in range(len(values)):
        while not ok(l, r):
            l += 1
        best = max(best, r - l + 1)
        part = values[l:r + 1]
        window = "".join(part) if all(isinstance(x, str) for x in part) else " ".join(map(str, part))
        row = [r, values[r], l, window, r - l + 1, best]
        if show(l, r) != "":
            extra = show(l, r)
            row.append(", ".join(map(str, extra)) if isinstance(extra, list) else extra)
        rows.append(row)
    return rows


MONOTONE = """
**Why the left edge never goes back.** If the window `[L, R]` breaks the rule, then every longer window `[L, R']` with
`R' > R` contains it and breaks the rule too. So once a start `L` fails for some `R`, it fails for all later `R`, and
we can throw it away forever. That's what lets the left pointer only move forward, and makes the whole scan O(n).
"""


# ---------------------------------------------------------------- longest-fresh-run
s = "abcabdcbb"
fresh = lambda l, r: len(set(s[l:r + 1])) == r - l + 1
rows = trace(list(s), fresh)
EXTRA["longest-fresh-run"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A single character: the answer is 1.
        - All characters different: the whole string.
        - A repeat **outside** the current window (like the first `a` in `abba` when we reach the last `a`) must not
          move the window.
        """
    ],
    "think": [
        f"""
        **The rule and its shape.** A window is valid when no character appears twice in it. Shrinking a valid window
        keeps it valid, and growing an invalid one keeps it invalid. That's the signature of a "longest valid window"
        problem.
        """,
        MONOTONE,
        f"""
        **A trace on `"{s}"`.** `R` adds one character per row; `L` is moved just far enough to remove the repeat:
        """,
        table(["R", "char", "L", "window", "length", "best"], *rows),
        """
        **Moving `L` faster.** When the new character `c` repeats inside the window, the window must start **after the
        previous `c`**: any start at or before it still contains both copies. Instead of stepping `L` one character at a
        time, remember the last index of each character and jump straight there.

        **The stale-entry trap.** The remembered index may already be left of `L` (the earlier copy was dropped long
        ago). Then nothing repeats inside the window, and `L` must not move. In `"abba"`, at the final `a` the last `a`
        is at 0 but `L` is already 2; jumping to 1 would move `L` backwards and allow `"bba"`, which isn't fresh. So the
        jump is taken only if `last[c] ≥ L`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each start `i`, walk right adding characters to a "seen" set until the next character is already
                seen. The run `s[i..j−1]` is the longest fresh run starting at `i`.

                Because there are only 36 possible characters, a fresh run is at most 36 long, so each start stops
                quickly here. But with a large alphabet (say all Unicode) this becomes O(n²), and it re-reads the same
                characters from many starts.
                """
            ],
            "complexity": [
                "**Time O(n · σ)**, where σ is the number of distinct characters (36 here, up to n in general). **Space O(σ)** for the seen set."
            ],
        },
        1: {
            "idea": [
                """
                One pass with `R` over the string, and `L` as the start of the current fresh window. `last[c]` stores the
                most recent index of character `c`.

                For each `R` with character `c`:

                1. If `last[c] ≥ L`, the previous `c` is inside the window; set `L = last[c] + 1`.
                2. Record `last[c] = R`.
                3. The window `s[L..R]` is fresh; update the best length with `R − L + 1`.

                **Invariant.** After step 1, `s[L..R]` has no repeated character, and `L` is the smallest start for which
                that's true. Since every fresh window ending at `R` starts at `L` or later, `R − L + 1` is the longest
                one ending at `R`; taking the max over all `R` gives the answer.
                """
            ],
            "build": [
                "`last` maps each character to its latest index (or −1); `L = 0`, `best = 0`.",
                "For each `R`: if `last[s[R]] ≥ L`, jump `L` to `last[s[R]] + 1`.",
                "Store `last[s[R]] = R`.",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": [
                """
                **Time O(n):** one step per character; `L` jumps in O(1). **Space O(σ)** for `last` (a 128-entry
                array in Java, C++ and C).
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Longest window with "no repeats"** → sliding window with last-seen positions.
        - **Jump, don't crawl:** `L = last[c] + 1`, but only if `last[c] ≥ L` (ignore stale positions).
        - **Template for longest-valid-window:** for each `R`: add, fix the window by moving `L`, record `R − L + 1`.
        """
    ],
}


# ---------------------------------------------------------------- one-colour-banner
b, kb = "ABAABBBAB", 1


def repaints(l, r):
    t = b[l:r + 1]
    return len(t) - max(t.count(c) for c in set(t))


rows_b = trace(list(b), lambda l, r: repaints(l, r) <= kb, lambda l, r: repaints(l, r))
EXTRA["one-colour-banner"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 0`: the answer is the longest run of one colour already present.
        - `k ≥ n − 1`: the whole banner can be made one colour.
        - Repainting can only help tiles inside the run we choose; changes elsewhere are wasted.
        """
    ],
    "think": [
        f"""
        **Cost of one run.** To make a run one colour with as few repaints as possible, keep its most common colour and
        repaint everything else. So a run of length `len` whose most frequent colour appears `top` times needs
        `len − top` repaints, and it's achievable when `len − top ≤ k`.

        **Shape of the rule.** Removing a tile from either end can't increase `len − top` (`len` drops by 1 and `top`
        drops by at most 1). So shrinking keeps a run valid: a longest-valid-window problem.
        """,
        MONOTONE,
        f"""
        **A trace on `"{b}"` with `k = {kb}`** (last column = repaints needed for the window):
        """,
        table(["R", "tile", "L", "window", "length", "best", "repaints"], *rows_b),
        """
        **The subtle speed-up.** Computing `top` exactly means scanning 26 counters after every change. But we're only
        hunting for windows **longer than the best so far**. A longer window can only pass `len − top ≤ k` if its `top`
        is larger than any `top` we've already met. So it's enough to remember `maxf`, the **largest count ever seen**,
        even if the current window's real top count is smaller. With a stale `maxf` the window may be invalid for a while,
        but then it just slides at its current length (one in, one out), never reporting a length we haven't legitimately
        reached before. The window only grows when some colour sets a new `maxf`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each start, extend to the right, keeping colour counts and the running top count; stop as soon as
                `len − top > k`. The last valid length is the best run from that start.
                """
            ],
            "complexity": ["**Time O(n²)** when `k` is large (runs extend far from every start). **Space O(1)**: 26 counters."],
        },
        1: {
            "idea": [
                """
                A sliding window with 26 colour counts. Add `s[R]`; while `len − max(count) > k`, remove `s[L]` and move
                `L` right. Record the window length.

                **Correctness** follows the usual pattern: after the while loop, `[L, R]` is the longest valid window
                ending at `R` (any earlier start was rejected for an earlier or equal `R`, and stays invalid).
                """
            ],
            "complexity": ["**Time O(26 · n):** each of the up to `2n` pointer moves recomputes a max over 26 counts. **Space O(1).**"],
        },
        2: {
            "idea": [
                """
                Keep `maxf` = the highest count of any colour in any window so far (it never decreases). After adding
                `s[R]`, if `len − maxf > k`, remove exactly one tile from the left. The window length never decreases;
                it grows by one exactly when the new tile pushes `maxf` up (or the window still fits).

                **Why every recorded length is achievable.** At the step when `maxf` last went up, the window held
                `maxf` copies of one colour and fitted the rule (a step that raises `maxf` never slides). Since then the
                window has grown only while `len − maxf ≤ k`. Take that earlier window and extend it to the current length
                `len`: it still holds at least `maxf` copies of that colour, so at most `len − maxf ≤ k` tiles need
                repainting. So a valid run of length `len` really exists.

                **Why nothing longer is missed.** To beat the current length `len`, a run needs a colour appearing at
                least `len + 1 − k` times, more than `maxf`. While `R` walks through such a run, that colour's count in
                our window climbs past `maxf`, which lets the window grow instead of sliding. So the final length reaches
                the true answer.
                """
            ],
            "build": [
                "26 counts, `L = 0`, `maxf = 0`, `best = 0`.",
                "Add `s[R]`: increment its count and set `maxf = max(maxf, count)`.",
                "If `R − L + 1 − maxf > k`, decrement `count[s[L]]` and move `L` one step (the window slides).",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": ["**Time O(n):** O(1) work per tile. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **"Make a window uniform with ≤ k changes":** cost = length − most frequent count.
        - **Same template as "flip at most k zeros"**, where the "most frequent" is always the 1s.
        - **When only the maximum length matters**, the window may slide instead of shrinking, and a stale maximum
          frequency is safe.
        """
    ],
}


# ---------------------------------------------------------------- patch-the-outage
st, kp = [1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1], 2
rows_p = trace(st, lambda l, r: st[l:r + 1].count(0) <= kp, lambda l, r: st[l:r + 1].count(0))
EXTRA["patch-the-outage"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k = 0`: the longest existing run of 1s.
        - `k` at least the number of zeros: the whole log.
        - All zeros: the answer is `min(k, n)`.
        """
    ],
    "think": [
        """
        **Which zeros should we patch?** Patching a zero only helps if it ends up inside the run we report. So pick the
        run first: a run can be made all ones exactly when it contains **at most `k` zeros**. The problem is "longest
        window with at most `k` zeros".
        """,
        MONOTONE,
        f"""
        **Trace with `k = {kp}`** (last column = zeros in the window):
        """,
        table(["R", "value", "L", "window", "length", "best", "zeros"], *rows_p),
        """
        When a third zero enters, `L` walks right until a zero has left; ones it passes over are simply dropped. Note
        that we never need to decide **which** zeros get patched: all zeros in the final window are.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                From every start, extend while the window has at most `k` zeros. Each start's run is the longest from that
                start; the best of them is the answer. It restarts the zero count for every start.
                """
            ],
            "complexity": ["**Time O(n²)** when `k` is large. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Keep a window `[L, R]` and its zero count. Add `status[R]` (zero → count + 1). While the count exceeds
                `k`, remove `status[L]` (if it's a zero, count − 1) and advance `L`. Then `R − L + 1` is the longest
                patchable run ending at `R`.

                **Invariant.** After the loop, `[L, R]` has at most `k` zeros and `L` is the earliest start that allows
                it.
                """
            ],
            "build": [
                "`L = 0`, `zeros = 0`, `best = 0`.",
                "For each `R`: if `status[R] = 0`, `zeros += 1`.",
                "While `zeros > k`: if `status[L] = 0`, `zeros −= 1`; `L += 1`.",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": ["**Time O(n):** `R` and `L` each move at most `n` times. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **"Flip/patch at most k" = window with at most k bad items.**
        - Count only the bad items; the window length does the rest.
        - The choice of *which* items to change disappears once you pick the window.
        """
    ],
}


# ---------------------------------------------------------------- ride-on-a-budget
fares, budget = [4, 2, 6, 1, 1, 3, 5, 2, 2], 10
rows_r = trace(fares, lambda l, r: sum(fares[l:r + 1]) <= budget, lambda l, r: sum(fares[l:r + 1]))
EXTRA["ride-on-a-budget"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Every fare above the budget: the answer is 0 (the window becomes empty).
        - Budget at least the total of all fares: the answer is `n`.
        - `budget = 0`: no hop is affordable, since fares are at least 1.
        """
    ],
    "think": [
        """
        **Why positivity matters.** All fares are at least 1. So adding a hop always raises the cost, and dropping a hop
        always lowers it. Two consequences:

        1. If a ride fits the budget, every shorter ride inside it fits too (shrinking is safe).
        2. If a ride is over budget, every longer ride containing it is over budget too.

        Point 2 is exactly the property that lets the left edge only move forward.
        """,
        MONOTONE,
        f"""
        **Trace with `budget = {budget}`** (last column = cost of the window):
        """,
        table(["R", "fare", "L", "window", "length", "best", "cost"], *rows_r),
        """
        **What would break with refunds (negative fares)?** Then dropping a hop could *increase* the cost and adding one
        could decrease it, so neither point holds, and the window method gives wrong answers. That variant needs prefix
        sums with a sorted structure instead.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["From every stop, keep adding fares while the total stays within the budget; the number of hops taken is the best ride from that stop."],
            "complexity": ["**Time O(n²)** for a large budget. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Prefix sums `pre[j]` = cost of the first `j` hops. A ride over hops `i..j−1` costs `pre[j] − pre[i]`.
                Because fares are positive, `pre` is strictly increasing, so for a start `i` the furthest affordable end
                is the **largest `j` with `pre[j] ≤ pre[i] + budget`**, found by binary search.

                This uses positivity in a different way (sorted prefixes instead of a moving window). It's a useful
                fallback when only the prefixes are monotone.
                """
            ],
            "complexity": ["**Time O(n log n):** one binary search per start. **Space O(n)** for the prefix sums."],
        },
        2: {
            "idea": [
                """
                Grow the ride one hop at a time with `R`, keeping its cost. While the cost exceeds the budget, drop hops
                from the front with `L`. Then the ride `L..R` is the longest affordable ride ending at hop `R`.

                **Invariant.** After the while loop, `cost(L..R) ≤ budget`, and `L` is the smallest start with that
                property (all smaller starts were dropped because they were over budget for some earlier or equal `R`,
                and stay over budget).

                If a single fare exceeds the budget, `L` moves to `R + 1` and the window is empty: length 0, which is
                exactly right.
                """
            ],
            "build": [
                "`L = 0`, `total = 0`, `best = 0`.",
                "For each `R`: `total += fares[R]`.",
                "While `total > budget`: `total −= fares[L]`; `L += 1`.",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": ["**Time O(n):** each hop enters once and leaves at most once. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Positive values + "sum ≤ budget"** → shrinkable window, O(n).
        - **Prefix sums + binary search** is the O(n log n) alternative that only needs monotone prefixes.
        - With negative values neither works; recognise that before reaching for a window.
        """
    ],
}


# ---------------------------------------------------------------- steady-readings
rd, lim = [8, 2, 4, 7, 5, 6, 9, 3, 4], 3
spread = lambda l, r: max(rd[l:r + 1]) - min(rd[l:r + 1])
rows_s = trace(rd, lambda l, r: spread(l, r) <= lim, lambda l, r: f"max {max(rd[l:r + 1])}, min {min(rd[l:r + 1])}")
EXTRA["steady-readings"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `limit = 0`: the longest run of equal readings.
        - A single reading is always steady (spread 0).
        - Readings up to 10⁹: the spread fits in 32 bits, but compute differences carefully.
        """
    ],
    "think": [
        """
        **Shape of the rule.** The spread `max − min` can only shrink (or stay) when you remove a reading, and only grow
        when you add one. So it's another longest-valid-window problem.
        """,
        MONOTONE,
        f"""
        **Trace with `limit = {lim}`:**
        """,
        table(["R", "reading", "L", "window", "length", "best", "state"], *rows_s),
        """
        **The real difficulty: max and min after removals.** Adding a reading updates the max and min easily, but when
        the left reading leaves, it might have been the max. Recomputing over the window costs O(window).

        **Monotonic deques.** Think about which readings could ever be the window's maximum again. If an older reading is
        **≤** a newer one, the newer one stays in the window at least as long, so the older one can never be the maximum
        again: discard it. What remains, read from front to back, is a strictly decreasing list of candidates, and its
        front is the current maximum. When the window's left edge passes the front's index, drop the front.

        The minimum uses the mirror image: discard older readings that are **≥** a newer one; the remaining list is
        increasing and its front is the minimum.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                "From every start, extend while tracking the running max and min; stop when they're more than `limit` apart. Simple and correct, but every start rescans."
            ],
            "complexity": ["**Time O(n²)** for a generous limit. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Two deques of **indices**: `hi` (readings decreasing from front to back) and `lo` (increasing).

                For each `R` with reading `v`:

                1. Pop from the back of `hi` every index whose reading is `≤ v`, then push `R`. Same for `lo` with `≥ v`.
                2. While `readings[hi.front] − readings[lo.front] > limit`: advance `L`, and pop a deque's front if its
                   index is now `< L`.
                3. Record `R − L + 1`.

                **Invariants.** Every index in a deque lies in `[L, R]`, the deques are monotone, and their fronts are the
                window's maximum and minimum. Storing indices (not values) is what lets us tell when a front has left.
                """
            ],
            "build": [
                "Two empty deques, `L = 0`, `best = 0`.",
                "Push `R` into both, popping dominated indices from the back first.",
                "Shrink: while the fronts are more than `limit` apart, `L += 1` and drop fronts with index `< L`.",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": [
                """
                **Time O(n):** each index is pushed once and popped at most once from each deque, and `L` moves at most
                `n` times. **Space O(n)** in the worst case (e.g. a strictly decreasing sequence fills `hi`).
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Window max/min under removals → monotonic deques of indices**, amortised O(1).
        - Max − min is monotone under shrinking, so the longest-window template applies.
        - The same deques give the "sliding window maximum" for fixed windows.
        """
    ],
}


# ---------------------------------------------------------------- two-flavour-basket
fl = [3, 3, 1, 2, 1, 1, 2, 4, 4, 2]
rows_f = trace(fl, lambda l, r: len(set(fl[l:r + 1])) <= 2, lambda l, r: sorted(set(fl[l:r + 1])))
EXTRA["two-flavour-basket"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One or two flavours in total: the whole counter.
        - All tubs different: the answer is 2 (or 1 if there's a single tub).
        - The best stretch may be in the middle; starting from the first tub isn't required.
        """
    ],
    "think": [
        """
        **Translating the story.** Starting anywhere and walking right until you can't continue means you take a
        contiguous stretch of tubs. The cone allows two flavours, so the question is: the longest stretch with **at most
        two distinct values**.
        """,
        MONOTONE,
        "**Trace** (last column = flavours in the window):",
        table(["R", "flavour", "L", "window", "length", "best", "flavours"], *rows_f),
        """
        **Counting distinct values in O(1).** Keep a count per flavour and a separate number `distinct`. When a count goes
        from 0 to 1, a new flavour entered (`distinct + 1`); when a count drops from 1 to 0, a flavour left completely
        (`distinct − 1`). Other changes don't affect `distinct`.

        When a third flavour enters, `L` must move until one of the flavours disappears entirely; that might take several
        steps, because the leftmost tub's flavour may appear again later in the window.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["From every tub, walk right remembering at most two flavours; stop at the first tub whose flavour would be a third. Correct, but each start re-walks the same tubs."],
            "complexity": ["**Time O(n²)**, e.g. for two alternating flavours. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Sliding window with `count[f]` and `distinct`. Add `flavours[R]`; while `distinct > 2`, remove
                `flavours[L]` and advance `L`. Record `R − L + 1`.

                Because flavours are below `n`, a plain array of counts replaces a hash map.

                **Generalises directly:** replace 2 by `k` for "longest stretch with at most `k` distinct values".
                """
            ],
            "build": [
                "`count` array of size `n`, `distinct = 0`, `L = 0`, `best = 0`.",
                "Add tub `R`: if its count goes 0 → 1, `distinct += 1`.",
                "While `distinct > 2`: decrement `count[flavours[L]]`; if it hits 0, `distinct −= 1`; `L += 1`.",
                "`best = max(best, R − L + 1)`.",
            ],
            "complexity": ["**Time O(n).** **Space O(n)** for the counts (a hash map would hold at most 3 keys)."],
        },
    },
    "takeaways": [
        """
        - **"At most k distinct values" windows:** counts + a distinct counter, updated only on 0 ↔ 1 transitions.
        - Read the story carefully: "walk until you can't" means contiguous.
        - Same template as every other longest-valid-window problem.
        """
    ],
}
