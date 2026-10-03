"""Fuller explanations for the shortest-valid-window problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, Row, fig, table
from window_patterns.shortest_window import trail_ref


def text_of(part):
    return "".join(part) if all(isinstance(x, str) for x in part) else " ".join(map(str, part))


def trace(values, valid, show=None):
    """Rows: R, value added, tightest valid window ending at R (or —), its length, best so far."""
    rows, l, best = [], 0, None
    for r in range(len(values)):
        tight = None
        while l <= r and valid(l, r):
            tight = l
            if best is None or r - l + 1 < best:
                best = r - l + 1
            l += 1
        win = text_of(values[tight:r + 1]) if tight is not None else "— (not valid yet)"
        row = [r, values[r], win, (r - tight + 1) if tight is not None else "—", best if best is not None else "—"]
        if show:
            row.append(show(l if tight is None else tight, r))
        rows.append(row)
    return rows


MONOTONE = """
**Why one left pointer is enough.** Here the rule gets *easier* as a window grows: if `[L, R]` is valid, every longer
window `[L, R']` with `R' > R` is valid too. For each right end `R`, the best window is the valid one with the
**latest** start. And that latest start never moves backwards as `R` grows: a start that was too early to be the
tightest for `R` is still too early for `R + 1`. So `R` grows the window until it's valid, then `L` moves forward as
long as the window stays valid, recording each valid window on the way.
"""

SHRINK_PROOF = """
**Why every candidate is seen.** When the inner loop stops at `R`, `[L − 1, R]` was the last valid window, the tightest
one ending at `R`. The shortest valid window overall ends at some `R`, and is the tightest one for that `R`, so it's
recorded at that moment.
"""


# ---------------------------------------------------------------- shortest-push
g, target = [2, 3, 1, 2, 4, 3, 1, 5], 9
EXTRA["shortest-push"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The total of all hours is below the target: return 0.
        - One hour alone reaches the target: the answer is 1.
        - The answer can be anywhere; the earliest valid window isn't necessarily the shortest.
        """
    ],
    "think": [
        """
        **This is the mirror image of "longest window under a budget".** Gains are positive, so adding an hour raises
        the total and dropping one lowers it. A window is *valid* when its total is at least the target, and validity is
        kept when the window grows.
        """,
        MONOTONE,
        f"**Trace with `target = {target}`** (the tightest valid window ending at each `R`):",
        table(["R", "gain", "tightest window", "length", "best", "its sum"], *trace(g, lambda l, r: sum(g[l:r + 1]) >= target, lambda l, r: sum(g[l:r + 1]))),
        SHRINK_PROOF,
    ],
    "approaches": {
        0: {
            "idea": ["From every hour, add hours until the total reaches the target. That first moment gives the shortest push starting at that hour; keep the minimum over all starts."],
            "complexity": ["**Time O(n²)** when the target is large. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Grow with `R`, adding `gains[R]` to `total`. While `total ≥ target`, the window `[L, R]` is valid: record
                its length, then remove `gains[L]` and advance `L` to try a shorter one.

                After the loop, `[L, R]` is no longer valid, which means `[L − 1, R]` was the tightest valid window ending
                at `R` (when any exists).

                Use `n + 1` as "not found" and translate it to 0 at the end.
                """
            ],
            "build": [
                "`L = 0`, `total = 0`, `best = n + 1`.",
                "For each `R`: `total += gains[R]`.",
                "While `total ≥ target`: `best = min(best, R − L + 1)`; `total −= gains[L]`; `L += 1`.",
                "Return `best` if it's at most `n`, else 0.",
            ],
            "complexity": ["**Time O(n):** every hour enters once and leaves at most once. **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Shortest window with a "big enough" rule:** grow until valid, then shrink while valid, recording inside the
          shrink loop.
        - Needs a rule that survives growing (positive values for sums).
        - Use a sentinel for "not found".
        """
    ],
}


# ---------------------------------------------------------------- every-flavour-sampler
jars = [7, 3, 7, 7, 9, 3, 3, 9, 7, 1, 3]
d = len(set(jars))
EXTRA["every-flavour-sampler"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One flavour only: the answer is 1.
        - Every jar different: the answer is `n`.
        - Flavours are up to 10⁹, so they can't index an array directly.
        """
    ],
    "think": [
        f"""
        **Two phases.** First count how many flavours exist: `d = {d}` for `jars = {jars}`. Then a window is valid when
        it contains all `d` flavours. Adding jars never removes a flavour, so validity survives growing.
        """,
        MONOTONE,
        "**Trace** (last column = flavours present in the window):",
        table(["R", "jar", "tightest window", "length", "best", "flavours"], *trace(jars, lambda l, r: len(set(jars[l:r + 1])) == d, lambda l, r: len(set(jars[l:r + 1])))),
        """
        **Checking "all flavours present" in O(1).** Keep `count[f]` for the window and `have` = flavours with a positive
        count. A count rising from 0 to 1 adds to `have`; one dropping from 1 to 0 subtracts. The window is valid exactly
        when `have == d`.
        """,
        SHRINK_PROOF,
    ],
    "approaches": {
        0: {
            "idea": ["From every jar, extend until all `d` flavours have been seen; only extensions shorter than the best so far are worth trying. Each start rebuilds its set."],
            "complexity": ["**Time O(n²)** in the worst case. **Space O(n).**"],
        },
        1: {
            "idea": [
                """
                Grow with `R` (updating `count` and `have`). While `have == d`, record `R − L + 1`, then remove `jars[L]`;
                if its count falls to 0, `have` drops and the loop stops.

                **Large values.** Use a hash map for the counts, or compress the flavours once (sort the distinct values,
                and replace each jar by its rank), which lets C use a plain array.
                """
            ],
            "build": [
                "`d` = number of distinct flavours.",
                "Counts, `have = 0`, `L = 0`, `best = n`.",
                "Add `jars[R]`: a 0 → 1 count means `have += 1`.",
                "While `have == d`: record; remove `jars[L]` (1 → 0 means `have −= 1`); `L += 1`.",
            ],
            "complexity": ["**Time O(n)** expected with hashing (O(n log n) with sorting-based compression). **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Shortest window containing every kind:** counts + "kinds present" counter, grow then shrink.
        - Decide the target (`d`) before sliding.
        - Large keys → hash map or one-time compression.
        """
    ],
}


# ---------------------------------------------------------------- balance-the-quartet
q4 = "SSATSSBS"
n4, q = len(q4), len(q4) // 4


def outside_ok(l, r):
    rest = q4[:l] + q4[r + 1:]
    return all(rest.count(c) <= q for c in "SATB")


extra4 = ", ".join(f"{q4.count(c) - q} extra {c}" for c in "SATB" if q4.count(c) > q)
EXTRA["balance-the-quartet"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Already balanced: the answer is 0 (an empty piece).
        - The piece may contain singers who don't need to change; they can be "repainted" to the same voice.
        - Several voices can be over the quota at once.
        """
    ],
    "think": [
        f"""
        **Think about what stays, not what changes.** Everything outside the chosen piece keeps its voice. If some voice
        already has more than `n/4 = {q}` singers outside the piece, no repainting inside can fix that. So a piece is
        usable only if **every voice appears at most `{q}` times outside it**.

        **That condition is also enough.** Suppose every voice is at most `{q}` outside. Each voice then needs
        `{q} − outside` more singers, and these shortfalls add up to exactly the piece's length (all counts add up to
        `n`). So we can repaint the piece's singers to fill every shortfall.

        For `"{q4}"` the surplus is {extra4}: the piece must include at least that many of each surplus voice. As the
        piece grows, the outside counts only go down, so validity survives growing.
        """,
        MONOTONE,
        "**Trace** (last column = voice counts outside the tightest window):",
        table(["R", "singer", "tightest window", "length", "best", "outside S A T B"], *trace(list(q4), outside_ok, lambda l, r: " ".join(str((q4[:l] + q4[r + 1:]).count(c)) for c in "SATB"))),
        SHRINK_PROOF,
    ],
    "approaches": {
        0: {
            "idea": ["Check for 0 first. Then from every start, move singers one by one from the outside counts into the piece until no voice exceeds `n/4` outside; that length is the best piece from this start."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Start with `out` = the counts of the whole string (the piece is empty). `R` moves a singer into the
                piece: `out[s[R]] −= 1`. While every `out[c] ≤ n/4`, record the piece and give back the leftmost singer
                (`out[s[L]] += 1`, `L += 1`).

                The validity check looks at only four counters, so it's O(1).
                """
            ],
            "build": [
                "Count each voice; return 0 if all are `n/4`.",
                "`L = 0`, `best = n`.",
                "For each `R`: `out[s[R]] −= 1`.",
                "While all four `out` counts are `≤ n/4`: record `R − L + 1`; `out[s[L]] += 1`; `L += 1`.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Reframe "what to change" as "what stays":** the outside must already satisfy the limits.
        - The window tracks counts of its *complement*.
        - Then it's the standard shortest-valid-window template.
        """
    ],
}


# ---------------------------------------------------------------- shortest-trail-window
ts, tt = "cabxbcaxbyc", "abc"
EXTRA["shortest-trail-window"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `t` doesn't occur as a subsequence at all: return `""`.
        - `t` repeats a letter (like `"aba"`): the same position of `s` can't serve two letters of `t`.
        - Ties: return the leftmost shortest window.
        """
    ],
    "think": [
        f"""
        **Why counts aren't enough here.** In other shortest-window problems, the window only had to contain certain
        letters. Here the letters of `t` must appear **in order**, so `"cba"` doesn't contain `"abc"` even though it has
        the same letters. A count map can't see order.

        **Fix the right end and ask for the latest start.** For a window ending at position `i`, we want it to start as
        late as possible while still containing `t` in order. Build that up letter by letter:

        - `start[j]` = the latest position from which `t[0..j)` (the first `j` letters of the route) can be matched in
          order, finishing at or before the current position.
        - If `s[i] = t[j−1]`, then `t[0..j)` can finish exactly at `i`, starting where `t[0..j−1)` started:
          `start[j] = start[j−1]` (for `j = 1`, the start is `i` itself).

        When `start[m]` is set, the window `s[start[m] .. i]` is the shortest one ending at `i`.

        **Example.** `s = "{ts}"`, `t = "{tt}"`: the answer is `"{trail_ref(ts, tt)}"`.
        """,
        fig(Row(list(ts), label="s"), Row(list(tt), label="t")),
        """
        **Update order matters.** Process `j` from `m` down to 1. Otherwise, when `t` has a repeated letter, `start[j]`
        could read a `start[j − 1]` that was just updated with the *same* position `i`, letting one character of `s`
        match two letters of `t`.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For every position holding `t[0]`, match `t` greedily to the right; the first place where the whole route
                is matched gives the shortest window starting there. Keep the shortest (first on ties).

                Greedy matching is optimal for a fixed start: taking each letter of `t` at its earliest possible position
                can only make the end earlier.
                """
            ],
            "complexity": ["**Time O(n²)** in the worst case (every start scans to the end). **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Keep `start[0..m]` (−1 = not matched yet). For each `i` and each `j` from `m` down to 1 with
                `t[j−1] = s[i]`, set `start[j] = (j == 1 ? i : start[j−1])`. Then, if `start[m] ≥ 0`, compare the window
                `start[m]..i` with the best (strictly shorter only, which keeps the leftmost among equals).

                **Why `start[m]` is optimal for end `i`.** By induction on `j`, `start[j]` is the latest start of any
                in-order match of `t[0..j)` ending at or before `i`. A later start would need a later match of the first
                `j − 1` letters, contradicting the definition of `start[j−1]`.
                """
            ],
            "build": [
                "`start` array of `m + 1` entries, all −1.",
                "For each `i`: for `j = m..1`, if `t[j−1] = s[i]`, set `start[j]`.",
                "If `start[m] ≥ 0` and `i − start[m] + 1` beats the best, record it.",
                "Return the best window, or `\"\"`.",
            ],
            "complexity": [
                """
                **Time O(n · m)** = 2 × 10⁶ at the limits (the Python version only touches the positions of `t` that match
                `s[i]`). **Space O(m).**
                """
            ],
        },
    },
    "takeaways": [
        """
        - **Order-sensitive windows** need progress through the pattern, not counts.
        - **"Latest start" per pattern prefix** shares work across all windows.
        - Update dependent entries from high to low so each position is used once.
        """
    ],
}


# ---------------------------------------------------------------- smallest-covering-window
cs, ct = "XBAYCBAXCA", "ABC"


def covers(l, r):
    w = cs[l:r + 1]
    return all(w.count(c) >= ct.count(c) for c in set(ct))


EXTRA["smallest-covering-window"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `t` longer than `s`, or a letter of `t` missing from `s`: return `""`.
        - Repeated letters in `t` must be matched with multiplicity (`"AA"` needs two `A`s).
        - Upper and lower case are different letters.
        """
    ],
    "think": [
        """
        **Shape of the rule.** A window is valid when it contains every letter of `t` at least as many times as `t`
        does. Adding letters never breaks that, so it's a shortest-valid-window problem.
        """,
        MONOTONE,
        f"**Trace** on `s = \"{cs}\"`, `t = \"{ct}\"` (last column = letters still missing):",
        table(["R", "char", "tightest window", "length", "best", "missing"], *trace(list(cs), covers, lambda l, r: sum(max(0, ct.count(c) - cs[l:r + 1].count(c)) for c in set(ct)))),
        """
        **Validity in O(1) with one counter.** Keep `need[c]` = how many more `c` the window still needs (it goes negative
        when the window has extras) and `missing` = the total still needed.

        - Adding `c`: if `need[c] > 0`, this copy was actually needed, so `missing −= 1`. Either way `need[c] −= 1`.
        - Removing `c`: `need[c] += 1`; if it becomes positive, the window now lacks a `c`, so `missing += 1`.

        The window is valid exactly when `missing == 0`. No 52-letter comparison is needed.
        """,
        SHRINK_PROOF,
    ],
    "approaches": {
        0: {
            "idea": ["From every start, copy the requirement counts and extend until nothing is missing (only while shorter than the best). Each start redoes the counting."],
            "complexity": ["**Time O(n²)** in the worst case. **Space O(σ)**: one count per letter."],
        },
        1: {
            "idea": [
                """
                Grow with `R` (updating `need` and `missing`). While `missing == 0`, record the window if it's strictly
                shorter (that keeps the leftmost on ties, because `R` only increases), then remove `s[L]` and advance.

                Store the best window as (length, start) and cut the substring once at the end.
                """
            ],
            "build": [
                "`need` from `t`; `missing = len(t)`; `L = 0`; best = (n + 1, 0).",
                "Add `s[R]`: `missing −= 1` if it was needed; `need[s[R]] −= 1`.",
                "While `missing == 0`: record if strictly shorter; `need[s[L]] += 1`; if positive, `missing += 1`; `L += 1`.",
                "Return the best substring or `\"\"`.",
            ],
            "complexity": ["**Time O(n + m):** each index enters and leaves once. **Space O(σ)**: 128 counters."],
        },
    },
    "takeaways": [
        """
        - **Minimum window containing a multiset:** shrinking window + one `missing` counter.
        - Let `need` go negative for extras; only threshold crossings change `missing`.
        - Strict `<` when recording keeps the leftmost of equal-length answers.
        """
    ],
}
