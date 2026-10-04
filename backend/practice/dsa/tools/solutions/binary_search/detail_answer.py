"""In-depth text for the search-on-the-answer problems (merged into their sol() calls via sol.EXTRA)."""
import math

from sol import EXTRA, table

ANSWER = """
**Binary search on the answer.** Sometimes there's no sorted array at all, but the **answer** lives in a range of
numbers, and there's a yes/no question about a candidate value that is **monotone**: once it's yes, it stays yes for
every larger value (or every smaller one). Then:

1. pick the range `[lo, hi]` that surely contains the answer;
2. write `check(x)`, a fast test of the yes/no question for one candidate;
3. binary search for the boundary where `check` flips.

Total cost: `O(cost of check × log(range))`. The hard parts are noticing the monotone question and writing `check`
correctly; the search itself is always the same few lines.
"""


def search_min(lo, hi, check, fmt=lambda x, ok: "yes" if ok else "no"):
    """Smallest x in [lo, hi] with check(x) true; returns (rows, answer)."""
    rows = []
    while lo < hi:
        mid = (lo + hi) // 2
        ok = check(mid)
        rows.append((lo, hi, mid, fmt(mid, ok), "answer ≤ mid: hi = mid" if ok else "answer > mid: lo = mid + 1"))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    return rows, lo


HEAD = ["lo", "hi", "mid", "check(mid)", "decision"]

# ---------------------------------------------------------------- reading-speed
books, hours = [3, 6, 7, 11], 8
need = lambda s: sum((p + s - 1) // s for p in books)
r_rows, r_ans = search_min(1, max(books), lambda s: need(s) <= hours, lambda s, ok: f"{need(s)} hours → {'fits' if ok else 'too slow'}")
EXTRA["reading-speed"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `hours` equal to the number of books: you must finish each book in one hour, so the speed is the largest book.
        - Lots of spare hours: speed 1 may be enough.
        - A partly used hour is wasted, so the hours for a book are `⌈pages / s⌉`.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **The monotone question.** "Can I finish within `hours` at speed `s`?" A faster speed never needs more hours, so
        the answer is no for slow speeds and yes from some speed onwards: find the smallest yes. The range is
        `[1, max(books)]`: at the largest book's size, every book takes one hour, which is the best possible. For
        `{books}` and {hours} hours:
        """,
        table(HEAD, *r_rows),
        f"Smallest speed **{r_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try `s = 1, 2, 3, …` until the total hours fit."],
            "build": ["Start at speed 1.", "Increase while the total hours exceed the limit."],
            "complexity": ["**Time O(n · answer):** up to 10⁹ · 10⁴ steps. **Space O(1).**"],
            "limits": ["Tries every speed. The fits/doesn't-fit answer is monotone, so binary search tries about 30."],
        },
        1: {
            "idea": ["Binary search the smallest speed in `[1, max(books)]` whose total hours `Σ ⌈p / s⌉` is at most `hours`."],
            "build": ["Range `[1, max(books)]`.", "Total hours at the middle speed.", "Fits → `hi = mid`, else `lo = mid + 1`."],
            "complexity": ["**Time O(n log max(books)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum rate to finish in time:** binary search on the rate; the check sums ceilings.
        - `⌈p / s⌉ = (p + s − 1) // s` in integers.
        - **Pitfall:** starting the range at 0 (division by zero).
        """
    ],
}


# ---------------------------------------------------------------- smallest-divisor
loads, thr = [1, 2, 5, 9], 6
tot = lambda d: sum((x + d - 1) // d for x in loads)
d_rows, d_ans = search_min(1, max(loads), lambda d: tot(d) <= thr, lambda d, ok: f"total {tot(d)} → {'≤' if ok else '>'} {thr}")
EXTRA["smallest-divisor"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Each term is at least 1 (rounding up), so the total is at least the number of loads; the threshold is guaranteed to allow that.
        - `d = max(loads)` makes every term 1, so it always works.
        - Rounding up, not down.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **Monotone.** A bigger divisor never makes `⌈x / d⌉` larger, so the total only shrinks as `d` grows: find the
        smallest `d` with total `≤ threshold`, searching `[1, max(loads)]`. For `{loads}`, threshold {thr}:
        """,
        table(HEAD, *d_rows),
        f"Smallest divisor **{d_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Try `d = 1, 2, …` until the total fits."],
            "build": ["Increase `d` while the total is too big."],
            "complexity": ["**Time O(n · answer).** **Space O(1).**"],
            "limits": ["Linear in the answer (up to 10⁶ tries of O(n) each)."],
        },
        1: {
            "idea": ["Binary search the smallest `d` in `[1, max(loads)]` with `Σ ⌈x / d⌉ ≤ threshold`."],
            "build": ["Range `[1, max(loads)]`.", "Compute the total for `mid`.", "Fits → `hi = mid`, else `lo = mid + 1`."],
            "complexity": ["**Time O(n log max(loads)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - Same template as the reading speed: monotone sum of ceilings.
        - Upper bound = the value that makes every term 1.
        - **Pitfall:** floor division instead of ceiling.
        """
    ],
}


# ---------------------------------------------------------------- shuttle-rounds
rt, total = [3, 5, 8], 7
rounds = lambda t: sum(t // r for r in rt)
s_rows, s_ans = search_min(1, min(rt) * total, lambda t: rounds(t) >= total, lambda t, ok: f"{rounds(t)} rounds")
EXTRA["shuttle-rounds"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only completed rounds count: `⌊t / roundTime⌋`.
        - One shuttle: the answer is `roundTime · totalRounds`.
        - The answer can reach `10⁷ × 10⁷ = 10¹⁴`: use 64 bits.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **Monotone in time.** More minutes never means fewer finished rounds. The range: at least 1 minute, and at most
        the time for the **fastest** shuttle to do all rounds alone, `min(roundTime) · totalRounds`. For `{rt}` and
        {total} rounds:
        """,
        table(HEAD, *s_rows),
        f"Earliest time **{s_ans}** minutes.",
    ],
    "approaches": {
        0: {
            "idea": ["Advance the clock one minute at a time, counting rounds, until there are enough."],
            "build": ["Minute by minute.", "Count rounds."],
            "complexity": ["**Time O(n · answer):** hopeless for answers near 10¹⁴. **Space O(1).**"],
            "limits": ["Steps through every minute. The round count is monotone in time, so binary search needs about 47 checks."],
        },
        1: {
            "idea": ["Binary search the smallest `t` in `[1, min(roundTime) · totalRounds]` with `Σ ⌊t / r⌋ ≥ totalRounds`."],
            "build": ["Upper bound from the fastest shuttle.", "Count rounds at `mid`.", "Enough → `hi = mid`, else `lo = mid + 1`."],
            "complexity": ["**Time O(n log(answer)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Minimum time for parallel workers:** binary search on time, count completed work.
        - A safe upper bound: the fastest worker alone.
        - **Pitfall:** summing rounds in 32 bits for a large candidate time; use 64 bits (or stop summing once enough rounds are counted).
        """
    ],
}


# ---------------------------------------------------------------- print-shop-daily-limit
pages, days = [4, 2, 7, 3, 5, 6, 1], 3


def days_needed(limit):
    used, load = 1, 0
    for p in pages:
        if load + p > limit:
            used += 1
            load = 0
        load += p
    return used


p_rows, p_ans = search_min(max(pages), sum(pages), lambda L: days_needed(L) <= days, lambda L, ok: f"{days_needed(L)} days")
EXTRA["print-shop-daily-limit"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The limit can't be below the largest job (it couldn't be printed at all).
        - `days ≥ number of jobs`: the answer is the largest job.
        - One day: the answer is the total of all pages.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **The check is greedy.** For a given limit, print jobs in order, starting a new day only when the next job doesn't
        fit. Packing as much as possible into each day never uses more days than any other split, because finishing more
        jobs early can only help later days. A bigger limit never needs more days, so the question is monotone.

        **Range:** `[max(pages), sum(pages)]`: the largest job must fit in a day, and the total fits in one day. For
        `{pages}` and {days} days:
        """,
        table(HEAD, *p_rows),
        f"Smallest daily limit **{p_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Start at the largest job and increase the limit by 1 until the greedy packing fits in the allowed days."],
            "build": ["Greedy day counter.", "Increase the limit until it fits."],
            "complexity": ["**Time O(n · (sum − max)).** **Space O(1).**"],
            "limits": ["Tries every limit; the days needed are monotone in the limit, so binary search suffices."],
        },
        1: {
            "idea": ["Binary search the smallest limit in `[max(pages), sum(pages)]` for which the greedy packing uses at most `days` days."],
            "build": ["Greedy day counter.", "Range `[max, sum]`.", "Fits → `hi = mid`, else `lo = mid + 1`."],
            "complexity": ["**Time O(n log(sum)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Split an array into ≤ k contiguous parts minimising the largest part:** binary search on the limit + greedy check.
        - Greedy filling is optimal for a fixed limit.
        - **Pitfall:** a lower bound below the largest job (the greedy check then misbehaves).
        """
    ],
}


# ---------------------------------------------------------------- bouquet-day
bloom, bq, size = [3, 9, 4, 8, 2, 5, 1, 7], 2, 2


def made(day):
    m = run = 0
    for b in bloom:
        run = run + 1 if b <= day else 0
        if run == size:
            m += 1
            run = 0
    return m


b_rows, b_ans = search_min(min(bloom), max(bloom), lambda d: made(d) >= bq, lambda d, ok: f"{made(d)} bouquet(s), row " + "".join("■" if b <= d else "□" for b in bloom))
EXTRA["bouquet-day"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Not enough flowers at all (`bouquets · size > n`): −1 immediately.
        - Flowers in a bouquet must be **adjacent**; a gap restarts the count.
        - The answer is always one of the bloom days.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **The check.** On a given day, walk the row counting consecutive bloomed flowers; every `size` of them make a
        bouquet and the count restarts. Taking a bouquet as soon as `size` adjacent flowers are available is optimal (it
        uses the leftmost possible flowers). Later days only add bloomed flowers, so the number of bouquets never
        decreases: monotone. For `{bloom}`, {bq} bouquets of {size} (■ = bloomed):
        """,
        table(HEAD, *b_rows),
        f"Earliest day **{b_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["After the impossibility check, try the distinct bloom days in increasing order and return the first that allows enough bouquets."],
            "build": ["Impossible if there aren't enough flowers.", "Sort the distinct bloom days.", "Check each in order."],
            "complexity": ["**Time O(n²)** in the worst case (n distinct days, O(n) check each). **Space O(n).**"],
            "limits": ["Checks every candidate day; monotonicity lets binary search check only about 30 days."],
        },
        1: {
            "idea": ["Binary search the day in `[min(bloom), max(bloom)]` with the greedy bouquet count as the check."],
            "build": ["Impossibility check.", "Greedy count of bouquets on a day.", "Binary search the earliest day with enough."],
            "complexity": ["**Time O(n log(max bloom)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Earliest day something becomes possible:** binary search on the day.
        - Check feasibility greedily (take a bouquet as soon as possible).
        - **Pitfall:** not resetting the run after making a bouquet (flowers would be reused).
        """
    ],
}


# ---------------------------------------------------------------- spread-the-sensors
spots, sensors = [1, 9, 4, 12, 7, 20], 3
s_sorted = sorted(spots)


def placed(gap):
    cnt, last, chosen = 1, s_sorted[0], [s_sorted[0]]
    for x in s_sorted[1:]:
        if x - last >= gap:
            cnt += 1
            last = x
            chosen.append(x)
    return cnt, chosen


lo, hi, g_rows = 1, (s_sorted[-1] - s_sorted[0]) // (sensors - 1), []
while lo < hi:
    mid = (lo + hi + 1) // 2
    c, ch = placed(mid)
    ok = c >= sensors
    g_rows.append((lo, hi, mid, f"greedy places {c}: {ch}", "spacing possible: lo = mid" if ok else "too wide: hi = mid − 1"))
    if ok:
        lo = mid
    else:
        hi = mid - 1
EXTRA["spread-the-sensors"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Two sensors: the answer is the distance between the outermost spots.
        - Spots are unsorted in the input; sort first.
        - We want the **largest** spacing that still fits, so the search looks for the last yes.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **The check.** For a candidate spacing, place the first sensor at the leftmost spot, and each next sensor at the
        first spot at least that far from the previous one. Placing each sensor as far left as allowed leaves the most
        room for the rest, so if any placement fits, the greedy one does. A smaller spacing is always easier, so the
        question is **yes up to the answer, then no**: we want the last yes (round `mid` up).

        **Range:** `[1, (max − min) / (sensors − 1)]`: with the sensors evenly spread across the whole road, no spacing can
        be larger. Sorted spots `{s_sorted}`, {sensors} sensors:
        """,
        table(HEAD, *g_rows),
        f"Largest spacing **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Sort, then try spacings from the upper bound downwards until the greedy placement fits."],
            "build": ["Sort.", "Greedy placement check.", "Decrease the spacing until it fits."],
            "complexity": ["**Time O(n · range).** **Space O(n).**"],
            "limits": ["Tries every spacing; the check is monotone, so binary search finds the last yes."],
        },
        1: {
            "idea": ["Sort; binary search the largest spacing in `[1, (max − min)/(sensors − 1)]` whose greedy placement fits, with `mid` rounded up."],
            "build": ["Sort.", "Greedy placement check.", "Last-yes binary search (upper middle)."],
            "complexity": ["**Time O(n log n + n log(range)).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **Maximise the minimum distance:** binary search on the distance + greedy placement.
        - Searching for the last yes → `lo = mid`, round `mid` up.
        - **Pitfall:** rounding down with `lo = mid` (infinite loop).
        """
    ],
}


# ---------------------------------------------------------------- nth-beat
a, b, n = 4, 6, 8
lcm = a // math.gcd(a, b) * b
cnt = lambda x: x // a + x // b - x // lcm
n_rows, n_ans = search_min(1, n * min(a, b), lambda x: cnt(x) >= n, lambda x, ok: f"{x // a} + {x // b} − {x // lcm} = {cnt(x)}")
EXTRA["nth-beat"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - When `a` divides `b`, every `b` beat is also an `a` beat.
        - `n` up to 10⁹ with `a, b` up to 4 × 10⁴: the answer can reach 4 × 10¹³, beyond 32 bits.
        - Shared beats count once.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **Counting beats up to x.** Multiples of `a` up to `x`: `⌊x/a⌋`; of `b`: `⌊x/b⌋`. The shared ones are the
        multiples of `lcm(a, b)`, counted twice, so subtract `⌊x/lcm⌋` (inclusion–exclusion). This count never decreases,
        and the n-th beat is the smallest `x` whose count reaches `n`. Range: `[1, n · min(a, b)]` (the faster drummer
        alone reaches `n` beats by then). For `a = {a}`, `b = {b}` (lcm {lcm}), `n = {n}`:
        """,
        table(HEAD, *n_rows),
        f"The {n}-th beat is **{n_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Merge the two beat sequences like merging sorted lists, skipping shared beats, `n` times."],
            "build": ["Next beat of each drummer.", "Take the smaller; advance one or both.", "Repeat `n` times."],
            "complexity": ["**Time O(n):** up to 10⁹ steps. **Space O(1).**"],
            "limits": ["Linear in `n`. The count of beats up to `x` has a closed form, so binary search over `x` takes about 45 steps."],
        },
        1: {
            "idea": ["Compute `lcm(a, b)`; binary search the smallest `x` with `⌊x/a⌋ + ⌊x/b⌋ − ⌊x/lcm⌋ ≥ n`; return it modulo 10⁹ + 7."],
            "build": ["lcm via gcd.", "Inclusion–exclusion count.", "Binary search the smallest qualifying `x`."],
            "complexity": ["**Time O(log(n · min(a, b))).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **n-th element of a merged arithmetic sequence:** binary search on the value + inclusion–exclusion count.
        - `lcm = a / gcd · b` avoids overflow.
        - **Pitfall:** counting shared multiples twice.
        """
    ],
}


# ---------------------------------------------------------------- kth-closest-pair
hts, kk = [4, 1, 9, 6, 3], 4
hs = sorted(hts)


def within(d):
    total = left = 0
    for right in range(len(hs)):
        while hs[right] - hs[left] > d:
            left += 1
        total += right - left
    return total


all_gaps = sorted(abs(x - y) for i, x in enumerate(hts) for y in hts[i + 1:])
k_rows, k_ans = search_min(0, hs[-1] - hs[0], lambda d: within(d) >= kk, lambda d, ok: f"{within(d)} pairs with gap ≤ {d}")
EXTRA["kth-closest-pair"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal heights give a gap of 0.
        - `k` can be as large as `n(n − 1)/2` ≈ 2 × 10⁸: listing all gaps is too slow and too big.
        - Gaps count with multiplicity.
        """
    ],
    "think": [
        ANSWER,
        f"""
        **Counting pairs with gap ≤ d.** Sort the heights. For each right end, the left ends within `d` form a window
        that only moves right as the right end moves right (a sliding window), so all pairs with gap `≤ d` are counted in
        O(n). That count grows with `d`, and the k-th smallest gap is the smallest `d` whose count reaches `k`. Sorted
        `{hs}`, all gaps `{all_gaps}`, `k = {kk}`:
        """,
        table(HEAD, *k_rows),
        f"The {kk}-th smallest gap is **{k_ans}**.",
    ],
    "approaches": {
        0: {
            "idea": ["List every pair's gap, sort, take the k-th."],
            "build": ["All `n(n−1)/2` gaps.", "Sort.", "Index `k − 1`."],
            "complexity": ["**Time O(n² log n).** **Space O(n²):** 2 × 10⁸ gaps at the limit."],
            "limits": ["Far too much time and memory; counting gaps up to a value takes O(n) with a sliding window."],
        },
        1: {
            "idea": ["Sort; binary search the gap in `[0, max − min]`; the check counts pairs with gap `≤ mid` using a sliding window."],
            "build": ["Sort.", "Sliding-window pair count.", "Smallest gap whose count reaches `k`."],
            "complexity": ["**Time O(n log n + n log(range)).** **Space O(n).**"],
        },
    },
    "takeaways": [
        """
        - **k-th smallest pairwise distance:** binary search on the distance + a sliding-window count.
        - "Smallest value with count ≥ k" is always an actual gap.
        - **Pitfall:** restarting the left pointer for every right end, which makes each check O(n²) instead of O(n).
        """
    ],
}
