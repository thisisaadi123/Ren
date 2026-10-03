"""Fuller explanations for the "at most k" counting problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, Row, fig, table


def text_of(part):
    return "".join(part) if all(isinstance(x, str) for x in part) else " ".join(map(str, part))


def lefts(values, ok):
    """For each R, the smallest L such that [L, R] satisfies the (shrink-safe) rule; R + 1 if none."""
    out, l = [], 0
    for r in range(len(values)):
        while l <= r and not ok(l, r):
            l += 1
        out.append(l)
    return out


COUNTING = """
**Counting windows, not measuring them.** For a rule that survives shrinking, the valid windows ending at a fixed `R`
are exactly those starting at `L, L + 1, …, R`, where `L` is the earliest valid start. That's `R − L + 1` windows,
and we can add them all in one step. Running the usual two pointers and adding `R − L + 1` for every `R` counts
**every** valid window exactly once (each window is counted at its own right end).
"""


# ---------------------------------------------------------------- exactly-k-breeds
pens, k = [1, 2, 1, 3, 2, 2, 3], 2
lk = lefts(pens, lambda l, r: len(set(pens[l:r + 1])) <= k)
lk1 = lefts(pens, lambda l, r: len(set(pens[l:r + 1])) <= k - 1)
rows = [(r, pens[r], lk[r], lk1[r], r - lk[r] + 1, r - lk1[r] + 1, lk1[r] - lk[r]) for r in range(len(pens))]
EXTRA["exactly-k-breeds"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `k` larger than the number of breeds on the farm: the answer is 0.
        - `k = 1`: count the stretches made of a single breed.
        - Up to ~5 × 10⁹ stretches: the count needs 64 bits.
        """
    ],
    "think": [
        """
        **Why "exactly k" resists a plain window.** Take a stretch with exactly `k` breeds and shrink it: it may drop to
        `k − 1` breeds. Grow it: it may rise to `k + 1`. Neither direction is safe, so there's no single left edge to
        maintain.

        **"At most k" is well-behaved.** Shrinking never adds breeds, so a stretch with at most `k` breeds stays valid
        when shrunk.
        """,
        COUNTING,
        f"""
        **The subtraction trick.** Fix a right end `R`. Moving the start leftwards, the breed count only grows. So:

        - starts with **at most `k`** breeds form a range `[L_k, R]`;
        - starts with **at most `k − 1`** breeds form a smaller range `[L_(k−1), R]`, with `L_(k−1) ≥ L_k`;
        - starts with **exactly `k`** breeds are the difference: `[L_k, L_(k−1) − 1]`.

        Summing over all `R`: `exactly(k) = atMost(k) − atMost(k − 1)`. Here it is for `pens = {pens}`, `k = {k}`:
        """,
        table(["R", "pen", f"L for ≤{k}", f"L for ≤{k - 1}", f"≤{k} count", f"≤{k - 1} count", f"exactly {k}"], *rows),
        f"""
        Totals: atMost({k}) = {sum(r[4] for r in rows)}, atMost({k - 1}) = {sum(r[5] for r in rows)}, difference
        **{sum(r[6] for r in rows)}**.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For every start, extend to the right while keeping a set of breeds seen. Count the ends where the set has
                exactly `k` breeds, and stop as soon as it has more than `k` (it can only grow from there).

                The `mark[v] = i + 1` trick in Java, C++ and C avoids clearing an array for each start: a value counts as
                seen only if it was marked during the current start.
                """
            ],
            "complexity": ["**Time O(n²)** in the worst case (e.g. few breeds and large `k`). **Space O(n).**"],
        },
        1: {
            "idea": [
                """
                Write one function `atMost(t)`: a sliding window with a count per breed and `distinct`. For each `R`, add
                `pens[R]`; while `distinct > t`, remove `pens[L]` and advance; add `R − L + 1` to the total. The answer
                is `atMost(k) − atMost(k − 1)`.

                **Invariant inside `atMost`.** After the while loop, `[L, R]` has at most `t` breeds and `L` is the
                earliest such start, so exactly `R − L + 1` valid stretches end at `R`.

                `atMost(0)` correctly returns 0: the window is emptied for every `R`, adding 0 each time.
                """
            ],
            "build": [
                "`atMost(t)`: counts array (values ≤ n), `distinct = 0`, `L = 0`, `total = 0`.",
                "Add `pens[R]`; a 0 → 1 count raises `distinct`.",
                "While `distinct > t`: remove `pens[L]` (1 → 0 lowers `distinct`), `L += 1`.",
                "`total += R − L + 1`; after the loop return `total`.",
                "Answer: `atMost(k) − atMost(k − 1)`.",
            ],
            "complexity": ["**Time O(n):** two passes, each with at most `2n` pointer moves. **Space O(n)** for the counts."],
        },
    },
    "takeaways": [
        """
        - **Exactly k = atMost(k) − atMost(k − 1)** when "at most" is window-friendly.
        - **Counting windows:** add `R − L + 1` per right end.
        - **Pitfalls:** 32-bit totals; forgetting that `atMost(0)` must be 0.
        """
    ],
}


# ---------------------------------------------------------------- exactly-k-odd-tickets
tk, kt = [2, 5, 4, 7, 3, 6, 8, 1, 2], 2
odd = [x & 1 for x in tk]
p, seen, prow, tot = 0, {0: 1}, [], 0
for i, v in enumerate(tk):
    p += v & 1
    add = seen.get(p - kt, 0)
    tot += add
    prow.append((i, v, p, p - kt, add, tot))
    seen[p] = seen.get(p, 0) + 1
EXTRA["exactly-k-odd-tickets"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Fewer than `k` odd tickets in total: 0.
        - Even tickets around a valid stretch can be added or left out freely, which multiplies the count.
        - The count can reach ~5 × 10⁹: use 64 bits.
        """
    ],
    "think": [
        f"""
        **Only parity matters.** Replace each ticket by 1 if odd, 0 if even: `{odd}`. We're counting stretches whose sum
        is exactly `k = {kt}`.

        **Method 1: prefix counts.** Let `p` be the number of odd tickets among the first `i + 1` tickets. A stretch from
        `a` to `i` has `p(i) − p(a − 1)` odd tickets. It has exactly `k` when the earlier prefix had `p − k`. So for
        each position, add **how many earlier prefixes had `p − k` odd tickets** (the empty prefix, with 0, counts
        once):
        """,
        table(["i", "ticket", "p", "looking for", "matches", "total"], *prow),
        f"""
        Total **{tot}**.

        **Method 2: at-most windows.** "At most `k` odd tickets" survives shrinking, so `atMost(k) − atMost(k − 1)` works
        exactly as for distinct values, with an O(1)-memory window instead of a table.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["From every start, extend while the odd count is at most `k`, counting the ends where it equals `k`. Stops early once past `k`, but still quadratic when odd tickets are rare."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Keep `seen[c]` = how many prefixes so far contain exactly `c` odd tickets, with `seen[0] = 1` for the
                empty prefix. For each ticket: update `p`, add `seen[p − k]` (if `p ≥ k`), then record `seen[p] += 1`.

                **Why it's right.** Each stretch ending at `i` corresponds to one earlier prefix; the stretch has exactly
                `k` odds precisely when that prefix has `p − k`. Counting those prefixes counts those stretches.

                Since `p` never exceeds `n`, an array replaces a hash map.
                """
            ],
            "build": [
                "`seen` array of size `n + 1`, `seen[0] = 1`; `p = 0`, `total = 0`.",
                "For each ticket: `p += ticket & 1`.",
                "If `p ≥ k`: `total += seen[p − k]`.",
                "`seen[p] += 1` (after the lookup, so a prefix never pairs with itself).",
            ],
            "complexity": ["**Time O(n).** **Space O(n)** for `seen`."],
            "limits": ["It needs an O(n) table. The at-most windows give the same count with O(1) memory."],
        },
        2: {
            "idea": [
                """
                `atMost(t)`: window holding at most `t` odd tickets; for each `R`, add `tickets[R] & 1`, shrink while over
                `t`, then add `R − L + 1`. Return `atMost(k) − atMost(k − 1)`.

                The per-`R` difference `L_(k−1) − L_k` is exactly the number of starts giving `k` odd tickets: the
                window for `k − 1` must drop one more odd ticket (and the evens before it) than the window for `k`.
                """
            ],
            "build": [
                "`atMost(t)` with `L`, `odd`, `total`.",
                "Add `tickets[R] & 1`; while `odd > t`, remove `tickets[L] & 1` and `L += 1`.",
                "`total += R − L + 1`.",
                "Answer: `atMost(k) − atMost(k − 1)`.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Subarrays with sum exactly k** (non-negative values): prefix-count table, or atMost difference.
        - Prefix sums with a lookup of `p − k` work even with negative values; at-most windows don't.
        - Reduce to 0/1 when only a property matters.
        """
    ],
}


# ---------------------------------------------------------------- full-set-of-stamps
st = "abcabbcab"
last, srow, tot = {"a": -1, "b": -1, "c": -1}, [], 0
for i, c in enumerate(st):
    last[c] = i
    add = min(last.values()) + 1
    tot += add
    srow.append((i, c, last["a"], last["b"], last["c"], add, tot))
EXTRA["full-set-of-stamps"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A letter missing from the whole album: 0.
        - Each end contributes 0 until all three letters have appeared.
        - Up to ~5 × 10⁹ substrings: 64-bit count.
        """
    ],
    "think": [
        """
        **Fix the end, count the starts.** For a substring ending at `i`, moving its start further left only adds stamps,
        so "contains a, b and c" stays true. The good starts are therefore `0, 1, …, x` for some `x`.

        **What is `x`?** The start must be at or before the last `a`, the last `b` and the last `c` seen up to `i`;
        otherwise that letter is missing. So `x = min(last a, last b, last c)`, giving `x + 1` full sets ending at `i`
        (and 0 while some letter hasn't appeared, since its last position is −1).
        """,
        table(["i", "stamp", "last a", "last b", "last c", "full sets ending here", "total"], *srow),
        f"""
        Total **{tot}**.

        This is a counting window in disguise: `min(last) + 1` plays the role of the left edge, computed directly instead
        of moved step by step. You could also count "at least one of each" as all substrings minus those missing a
        letter, but the direct count is simpler.
        """,
    ],
    "approaches": {
        0: {
            "idea": [
                """
                For each start, extend until all three letters have appeared, at position `j`. Every substring from that
                start ending at `j` or later is full, so add `n − j` and move to the next start.
                """
            ],
            "complexity": ["**Time O(n²)** when one letter is missing over long stretches. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Track the last index of each letter (initially −1). At each `i`, update the current letter's last index
                and add `min(last) + 1`.

                **Why it's exact.** Substrings ending at `i` with start `≤ min(last)` contain all three letters; any start
                after `min(last)` misses the letter whose last occurrence is `min(last)`.
                """
            ],
            "build": [
                "`last = [−1, −1, −1]`, `total = 0`.",
                "For each `i`: `last[s[i]] = i`.",
                "`total += min(last) + 1`.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **"At least one of each" counts:** for every end, valid starts are `0..min(last positions)`.
        - Counting per right end is the backbone of window counting.
        - **Pitfall:** adding `min(last)` instead of `min(last) + 1`.
        """
    ],
}


# ---------------------------------------------------------------- products-under-a-cap
fac, cap = [3, 2, 5, 1, 4, 6, 1], 25


def prod(l, r):
    v = 1
    for x in fac[l:r + 1]:
        v *= x
    return v


lp = lefts(fac, lambda l, r: prod(l, r) < cap)
prow2, tot = [], 0
for r in range(len(fac)):
    tot += r - lp[r] + 1
    prow2.append((r, fac[r], lp[r], text_of(fac[lp[r]:r + 1]) or "—", prod(lp[r], r) if lp[r] <= r else 1, r - lp[r] + 1, tot))
EXTRA["products-under-a-cap"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `cap ≤ 1`: every product is at least 1, so nothing qualifies.
        - Runs of 1s don't change the product, so windows can get very long.
        - A single factor `≥ cap` empties the window.
        """
    ],
    "think": [
        """
        **Why a window works.** Every factor is at least 1, so extending a run never lowers its product. A run under
        the cap stays under it when shrunk, and the earliest valid start only moves right.
        """,
        COUNTING,
        f"**Trace with `cap = {cap}`:**",
        table(["R", "factor", "L", "window", "product", "runs ending here", "total"], *prow2),
        f"""
        Total **{tot}**.

        **Keeping the product small.** The window always keeps its product below `cap ≤ 10⁶`. Multiplying in one more
        factor (≤ 1000) gives less than 10⁹, which fits even in 32 bits; dividing it back out is exact because it was
        multiplied in. So the running product never overflows, unlike the product of the whole array.

        **Why `cap ≤ 1` is special.** With `cap = 1`, even an empty-looking window can't satisfy `product < 1`, so the
        shrink loop would push `L` past `R`. Returning 0 up front avoids that.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["For each start, multiply factors while the product stays below the cap, counting each run. With many 1s every start extends far: quadratic."],
            "complexity": ["**Time O(n²)** in the worst case. **Space O(1).**"],
        },
        1: {
            "idea": [
                """
                Multiply in `factors[R]`. While `product ≥ cap`, divide by `factors[L]` and advance `L`. Then add
                `R − L + 1`.

                **Invariant.** After the loop, `product` is the product of `[L, R]`, it's below the cap, and `L` is the
                earliest start with that property. So exactly `R − L + 1` runs ending at `R` qualify.
                """
            ],
            "build": [
                "If `cap ≤ 1`, return 0.",
                "`product = 1`, `L = 0`, `total = 0`.",
                "For each `R`: `product *= factors[R]`; while `product ≥ cap`, `product /= factors[L]`, `L += 1`.",
                "`total += R − L + 1`.",
            ],
            "complexity": ["**Time O(n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Products of factors ≥ 1 behave like sums of non-negatives:** counting windows apply.
        - Guard the degenerate cap first.
        - Keep the running value bounded by the window rule to avoid overflow.
        """
    ],
}
