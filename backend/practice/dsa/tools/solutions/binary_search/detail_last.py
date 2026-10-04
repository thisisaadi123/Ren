"""In-depth text for real-valued, unknown-size and k-th-element binary searches (merged via sol.EXTRA)."""
import math

from sol import EXTRA, table

REAL = """
**Binary search on real numbers (bisection).** When the answer is a real number, keep an interval `[lo, hi]` that
surely contains it and halve it with a monotone test, exactly like the integer version, except that `lo = mid` and
`hi = mid` (no `± 1`). Instead of looping "until close enough" with an epsilon, which can get stuck because of
floating-point rounding, run a **fixed number of halvings**: 100 halvings shrink the interval by 2¹⁰⁰, far below any
required precision.
"""

DOUBLING = """
**When there's no upper bound: double first.** If the answer could be anywhere up to a huge or unknown limit, start
with `hi = 1` and double it until the test is true. That takes about `log₂(answer)` steps and gives a range
`[hi / 2, hi]` that contains the answer, which an ordinary binary search then narrows down. Total O(log answer),
and the values tested never get much larger than the answer (no overflow from a huge guessed bound).
"""

KTH = """
**K-th element by counting or partitioning.** The k-th smallest of a structure we can't (or don't want to) sort can be
found two ways:

- **Binary search on the value:** count how many elements are `≤ v` (fast because of the structure) and find the
  smallest `v` whose count reaches `k`;
- **Binary search on a split:** decide how many of the first `k` elements come from each part, and check the split
  with a couple of comparisons.
"""


# ---------------------------------------------------------------- cube-root
v = 50.0
lo, hi, crows = -max(1.0, abs(v)), max(1.0, abs(v)), []
for step in range(12):
    mid = (lo + hi) / 2
    below = mid ** 3 < v
    crows.append((step + 1, f"{lo:.4f}", f"{hi:.4f}", f"{mid:.4f}", f"{mid ** 3:.3f}", "root is above mid" if below else "root is at or below mid"))
    if below:
        lo = mid
    else:
        hi = mid
EXTRA["cube-root"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Negative volumes have negative cube roots (unlike square roots).
        - Volumes between −1 and 1: the root's magnitude is **larger** than the volume's, so the starting interval must be
          at least `[−1, 1]`.
        - 0 → 0.
        """
    ],
    "think": [
        REAL,
        f"""
        **The interval.** `r³` increases with `r`, so "is `mid³ < volume`?" is monotone. The root lies in
        `[−max(1, |v|), max(1, |v|)]`: for `|v| ≥ 1` the root's magnitude is at most `|v|`; for `|v| < 1` it's at most 1.
        First twelve halvings for `v = {v:g}` (the root is {v ** (1 / 3):.6f}):
        """,
        table(["step", "lo", "hi", "mid", "mid³", "decision"], *crows),
        "After 200 halvings the interval is far narrower than 10⁻⁶.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Newton's method: improve a guess `r` with `r − (r³ − v) / (3r²)`, the point where the tangent of `r³ − v`
                crosses zero. Near the root it converges very fast (the number of correct digits roughly doubles each step).
                """
            ],
            "build": ["Handle 0 separately (the formula divides by `r²`).", "Start at `r = v`.", "Iterate the Newton update."],
            "complexity": ["**Time O(iterations):** a fixed 100 here, usually converged long before. **Space O(1).**"],
            "limits": ["Needs the derivative and a reasonable start, and can misbehave near 0. Bisection only needs a monotone test and always converges."],
        },
        1: {
            "idea": ["Bisection on `[−max(1, |v|), max(1, |v|)]` for 200 steps: if `mid³ < v`, move `lo` up, else move `hi` down. Return the midpoint."],
            "build": ["Bracket the root.", "Halve with the monotone test.", "Fixed number of steps."],
            "complexity": ["**Time O(200)** = O(log(range / precision)). **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Real-valued roots:** bisection with a fixed iteration count; Newton's method if speed matters.
        - Bracket carefully for values between −1 and 1.
        - **Pitfall:** `while hi − lo > eps` with a tiny `eps` and large values (rounding can prevent it from ever ending).
        """
    ],
}


# ---------------------------------------------------------------- rope-pieces
ropes, pieces = [8, 5, 13], 7
lo, hi, rrows = 0.0, float(max(ropes)), []
for step in range(10):
    mid = (lo + hi) / 2
    cnt = sum(int(r / mid) for r in ropes)
    ok = cnt >= pieces
    rrows.append((step + 1, f"{lo:.4f}", f"{hi:.4f}", f"{mid:.4f}", cnt, "enough: lo = mid" if ok else "too few: hi = mid"))
    if ok:
        lo = mid
    else:
        hi = mid
best_exact = max(r / m for r in ropes for m in range(1, pieces + 1) if sum(int(x * m // r) for x in ropes) >= pieces)
EXTRA["rope-pieces"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Pieces can't be joined, and leftovers are wasted.
        - The answer can be fractional.
        - Very many pieces from short ropes: tiny lengths.
        """
    ],
    "think": [
        REAL,
        f"""
        **Monotone.** A shorter piece length never gives fewer pieces (`⌊rope / L⌋` grows as `L` shrinks), so "at least
        `pieces` pieces?" is yes up to the answer: find the **largest** yes. Range `(0, max(ropes)]`. For `{ropes}` and
        {pieces} pieces (the exact answer is {best_exact:.6f}):
        """,
        table(["step", "lo", "hi", "mid", "pieces at mid", "decision"], *rrows),
    ],
    "approaches": {
        0: {
            "idea": [
                """
                The best length always splits some rope exactly into `m` equal parts (otherwise it could be increased a little
                without losing a piece). So try every candidate `rope / m` and keep the largest that yields enough pieces.
                """
            ],
            "build": ["Candidates `r / m` for every rope and `m ≤ pieces`.", "Count pieces for each.", "Keep the largest that works."],
            "complexity": ["**Time O(n² · pieces):** only for tiny inputs. **Space O(1).**"],
            "limits": ["Enumerates a huge set of candidates; bisection on the length needs about 100 checks."],
        },
        1: {
            "idea": ["Bisection on `[0, max(ropes)]` for 100 steps: if `Σ ⌊r / mid⌋ ≥ pieces`, `lo = mid`, else `hi = mid`. Return `lo`."],
            "build": ["Interval `[0, max]`.", "Count pieces at the middle.", "Keep the half containing the largest feasible length."],
            "complexity": ["**Time O(100 · n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Largest equal piece length:** bisection on the length with a floor-count check.
        - Return the side that is known to be feasible (`lo` here).
        - **Pitfall:** `mid = 0` in the first step if `lo = hi = 0` (division by zero); start `hi` at the longest rope.
        """
    ],
}


# ---------------------------------------------------------------- charging-stations
stations, extra = [0, 4, 15, 21], 4
gaps = [b - a for a, b in zip(stations, stations[1:])]
lo, hi, srows = 0.0, float(max(gaps)), []
for step in range(10):
    mid = (lo + hi) / 2
    need = sum(math.ceil(g / mid) - 1 for g in gaps)
    ok = need <= extra
    srows.append((step + 1, f"{lo:.4f}", f"{hi:.4f}", f"{mid:.4f}", need, "possible: hi = mid" if ok else "needs too many: lo = mid"))
    if ok:
        hi = mid
    else:
        lo = mid
EXTRA["charging-stations"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - New stations can be at non-integer positions.
        - Spreading `s` new stations evenly in a gap `g` splits it into `s + 1` equal parts.
        - Answers within 10⁻⁶ are accepted.
        """
    ],
    "think": [
        REAL,
        f"""
        **Check a target maximum gap `D`.** A gap `g` needs `⌈g / D⌉ − 1` new stations to bring every piece down to at
        most `D`. Summing over the gaps gives the stations needed; `D` is achievable when that's at most `extra`. A larger
        `D` never needs more stations, so find the smallest achievable `D`. Gaps `{gaps}`, {extra} extra stations:
        """,
        table(["step", "lo", "hi", "mid", "stations needed", "decision"], *srows),
        f"The interval converges to **{hi:.4f}** (after 100 steps, within 10⁻⁶).",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Place the stations one at a time, each into the gap whose current pieces are longest (a gap `g` with `a`
                stations added has pieces of `g / (a + 1)`). After all are placed, the largest piece is the answer.
                """
            ],
            "build": ["Gaps and a count of stations added to each.", "Each new station goes to the gap with the longest pieces.", "Report the longest piece."],
            "complexity": ["**Time O(extra · n)** with a linear scan per station. **Space O(n).**"],
            "limits": ["One step per extra station; with up to 10⁶ stations that's slow. Bisection on the answer checks a target in O(n)."],
        },
        1: {
            "idea": ["Bisection on `D` in `[0, max gap]` for 100 steps: stations needed = `Σ (⌈g / D⌉ − 1)`; feasible → `hi = D`, else `lo = D`."],
            "build": ["Gaps between stations.", "Stations needed for a target D.", "Bisection toward the smallest feasible D."],
            "complexity": ["**Time O(100 · n).** **Space O(n)** for the gaps."],
        },
    },
    "takeaways": [
        """
        - **Minimise the maximum gap by adding points:** bisection on the gap; each gap needs `⌈g / D⌉ − 1` points.
        - Fixed iteration counts beat epsilon loops for floats.
        - **Pitfall:** `⌈g / D⌉` instead of `⌈g / D⌉ − 1` (counts pieces, not added stations).
        """
    ],
}


# ---------------------------------------------------------------- stack-of-cans
cans = 1000
hi, drows = 1, []
while hi * (hi + 1) // 2 < cans:
    drows.append((hi, hi * (hi + 1) // 2, "not enough: double"))
    hi *= 2
drows.append((hi, hi * (hi + 1) // 2, "enough: range found"))
lo = hi // 2
brows = []
while lo < hi:
    mid = (lo + hi) // 2
    ok = mid * (mid + 1) // 2 >= cans
    brows.append((lo, hi, mid, mid * (mid + 1) // 2, "enough: hi = mid" if ok else "not enough: lo = mid + 1"))
    if ok:
        hi = mid
    else:
        lo = mid + 1
EXTRA["stack-of-cans"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Exactly triangular numbers (like 1, 3, 6, 10): the answer fits exactly.
        - Up to 9 × 10¹⁵ cans: the answer is about 1.34 × 10⁸, and `r(r + 1)/2` must be computed without overflow.
        - 1 can → 1 row.
        """
    ],
    "think": [
        DOUBLING,
        f"""
        **Monotone question:** "do `r` rows hold at least `cans`?" For {cans} cans, doubling first:
        """,
        table(["rows", "cans held", "decision"], *drows),
        "**Then binary search inside `[hi / 2, hi]`:**",
        table(["lo", "hi", "mid", "cans held", "decision"], *brows),
        f"Answer **{lo}** rows.",
    ],
    "approaches": {
        0: {
            "idea": ["Add rows one at a time until the total reaches `cans`."],
            "build": ["Rows and total start at 0.", "Add the next row until enough."],
            "complexity": ["**Time O(√cans):** about 1.3 × 10⁸ steps at the limit. **Space O(1).**"],
            "limits": ["Linear in the answer. The question is monotone, so binary search applies."],
        },
        1: {
            "idea": ["Binary search `r` in a hand-derived range `[1, 2 × 10⁸]` (enough because `2 × 10⁸` rows hold far more than 9 × 10¹⁵ cans)."],
            "build": ["Range from a worked-out bound.", "Test `mid(mid + 1)/2 ≥ cans`.", "Standard smallest-yes search."],
            "complexity": ["**Time O(log(2 × 10⁸)) ≈ 28 steps.** **Space O(1).**"],
            "limits": ["Relies on a bound computed by hand; doubling finds a tight bound automatically."],
        },
        2: {
            "idea": ["Double `hi` until `hi` rows are enough, then binary search in `[hi / 2, hi]`."],
            "build": ["Doubling phase.", "Binary search in the last doubling interval."],
            "complexity": ["**Time O(log answer).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Unknown or huge upper bound:** exponential (doubling) search, then binary search.
        - Doubling keeps tested values close to the answer, avoiding overflow.
        - **Pitfall:** searching `[1, cans]`, where `mid²` overflows 64 bits for large inputs.
        """
    ],
}


# ---------------------------------------------------------------- zeros-at-the-end
def zeros_of(n):
    t = 0
    while n:
        n //= 5
        t += n
    return t


zt = 30
hi, zrows = 1, []
while zeros_of(hi) < zt:
    zrows.append((hi, zeros_of(hi), "not enough: double"))
    hi *= 2
zrows.append((hi, zeros_of(hi), "enough: range found"))
lo = hi // 2
zb = []
while lo < hi:
    mid = (lo + hi) // 2
    ok = zeros_of(mid) >= zt
    zb.append((lo, hi, mid, zeros_of(mid), "enough: hi = mid" if ok else "not enough: lo = mid + 1"))
    if ok:
        hi = mid
    else:
        lo = mid + 1
EXTRA["zeros-at-the-end"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `zeros = 0`: the answer is 0 (`0! = 1`).
        - Some zero counts are skipped entirely (24! has 4 zeros, 25! has 6), so "at least" matters.
        - `zeros` up to 2 × 10¹⁵: the answer is about 8 × 10¹⁵.
        """
    ],
    "think": [
        DOUBLING,
        f"""
        **Counting trailing zeros.** A trailing zero needs a factor 10 = 2 × 5, and 2s are far more common than 5s, so the
        zeros of `n!` equal the number of factors 5 in `1 … n`: `⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …`. This never decreases as `n`
        grows, so "does `n!` have at least `zeros` zeros?" is monotone. For {zt} zeros, doubling first:
        """,
        table(["n", "zeros of n!", "decision"], *zrows),
        "**Binary search in `[hi / 2, hi]`:**",
        table(["lo", "hi", "mid", "zeros of mid!", "decision"], *zb),
        f"Smallest n: **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Count `n` up from 0, computing the zeros of `n!` each time, until they reach the target."],
            "build": ["Zero-count helper.", "Increase `n` until enough."],
            "complexity": ["**Time O(answer · log answer):** hopeless for answers near 10¹⁶. **Space O(1).**"],
            "limits": ["Linear in the answer; the zero count is monotone and cheap, so doubling plus binary search needs about 100 evaluations."],
        },
        1: {
            "idea": ["Handle 0. Double `hi` until `zeros(hi) ≥ target`, then binary search the smallest `n` in `[hi / 2, hi]`."],
            "build": ["Zero count via repeated division by 5.", "Doubling phase.", "Binary search."],
            "complexity": ["**Time O(log² answer):** O(log answer) evaluations, each O(log answer). **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Trailing zeros of n! = number of factors 5** (Legendre's formula).
        - Monotone count + unknown bound → doubling, then binary search.
        - **Pitfall:** assuming every zero count is reachable ("at least" handles the gaps).
        """
    ],
}


# ---------------------------------------------------------------- kth-free-number
taken, kf = [2, 3, 4, 7, 11, 12, 15], 6
free_before = [t - (i + 1) for i, t in enumerate(taken)]
lo, hi, frows = 0, len(taken), []
while lo < hi:
    mid = (lo + hi) // 2
    ok = taken[mid] - (mid + 1) < kf
    frows.append((lo, hi, mid, taken[mid], taken[mid] - (mid + 1), "fewer than k free before it: go right" if ok else "at least k free before it: hi = mid"))
    if ok:
        lo = mid + 1
    else:
        hi = mid
EXTRA["kth-free-number"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - The answer may be before the first taken number, between two, or after the last.
        - `k` up to 10⁹, so listing free numbers is too slow.
        - Taken numbers are strictly increasing.
        """
    ],
    "think": [
        KTH,
        f"""
        **Free numbers before each taken one.** Before `taken[i]` there are `taken[i] − 1` positive numbers, of which `i`
        are taken, so `taken[i] − (i + 1)` are free. This count never decreases with `i`. For `{taken}`:
        """,
        table(["i", "taken[i]", "free numbers below it"], *[(i, t, f) for i, (t, f) in enumerate(zip(taken, free_before))]),
        f"""
        **Binary search** for the first index with at least `k = {kf}` free numbers before it:
        """,
        table(["lo", "hi", "mid", "taken[mid]", "free below", "decision"], *frows),
        f"""
        With `lo = {lo}` taken numbers before the answer, the answer is `lo + k = {lo + kf}`: counting `k` free numbers plus
        the `lo` taken numbers that sit among them.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Walk the gaps between consecutive taken numbers, subtracting each gap's free count from `k` until the k-th free number falls inside a gap (or after the last taken number)."],
            "build": ["Previous taken number and remaining `k`.", "Each gap holds `t − prev − 1` free numbers.", "Answer inside a gap or after the end."],
            "complexity": ["**Time O(n).** **Space O(1).**"],
            "limits": ["Linear in the number of taken values; the free-before count is monotone, so binary search finds the right gap in O(log n)."],
        },
        1: {
            "idea": ["Binary search the first index `i` with `taken[i] − (i + 1) ≥ k`; the answer is `i + k`."],
            "build": ["Half-open range `[0, n)`.", "Compare the free count before `taken[mid]` with `k`.", "Return `lo + k`."],
            "complexity": ["**Time O(log n).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **k-th missing number:** `taken[i] − (i + 1)` free numbers precede `taken[i]`; binary search on that count.
        - Answer = (taken numbers before it) + k.
        - **Pitfall:** off-by-one in the free count (`taken[i] − i` counts the number itself).
        """
    ],
}


# ---------------------------------------------------------------- kth-in-times-table
R, C, kt = 3, 4, 7
vals = sorted(i * j for i in range(1, R + 1) for j in range(1, C + 1))
lo, hi, trows = 1, R * C, []
while lo < hi:
    mid = (lo + hi) // 2
    per_row = [min(mid // i, C) for i in range(1, R + 1)]
    cnt = sum(per_row)
    trows.append((lo, hi, mid, " + ".join(map(str, per_row)) + f" = {cnt}", "≥ k: hi = mid" if cnt >= kt else "< k: lo = mid + 1"))
    if cnt >= kt:
        hi = mid
    else:
        lo = mid + 1
EXTRA["kth-in-times-table"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Equal products in different cells count separately.
        - Tables up to 3 × 10⁴ by 3 × 10⁴: listing all 9 × 10⁸ products is impossible.
        - `k = rows · cols` is the largest product.
        """
    ],
    "think": [
        KTH,
        f"""
        **Counting cells `≤ v`.** Row `i` holds `i, 2i, 3i, …`, so it has `min(⌊v / i⌋, cols)` cells `≤ v`. Summing over the
        (shorter) dimension counts the whole table in O(rows). The k-th smallest is the smallest `v` with count `≥ k`.
        For a {R} × {C} table, sorted products `{vals}`, `k = {kt}`:
        """,
        table(["lo", "hi", "mid", "cells ≤ mid (row by row)", "decision"], *trows),
        f"Answer **{lo}**.",
    ],
    "approaches": {
        0: {
            "idea": ["List all products, sort, take the k-th."],
            "build": ["All `rows · cols` products.", "Sort.", "Index `k − 1`."],
            "complexity": ["**Time O(rc log(rc)).** **Space O(rc):** up to 9 × 10⁸ values."],
            "limits": ["Impossible at full size; counting cells ≤ v takes O(min(rows, cols))."],
        },
        1: {
            "idea": ["Make `rows` the smaller dimension; binary search `v` in `[1, rows · cols]` with `count(v) = Σ min(v // i, cols)`."],
            "build": ["Use the smaller dimension for the loop.", "Count cells ≤ mid.", "Smallest value with count ≥ k."],
            "complexity": ["**Time O(min(r, c) · log(rc)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **k-th smallest in a multiplication table:** binary search on the value; row `i` contributes `min(v // i, cols)`.
        - Loop over the smaller dimension.
        - **Pitfall:** forgetting the `min(…, cols)` cap.
        """
    ],
}


# ---------------------------------------------------------------- kth-of-two-lists
A, B, kk = [1, 4, 6, 9, 12], [2, 3, 7, 10, 15, 20], 6
a, b = (A, B) if len(A) <= len(B) else (B, A)
m, n = len(a), len(b)
lo, hi, prows = max(0, kk - n), min(kk, m), []
while lo < hi:
    i = (lo + hi) // 2
    ok = a[i] < b[kk - i - 1]
    prows.append((lo, hi, i, kk - i, f"a[{i}] = {a[i]} vs b[{kk - i - 1}] = {b[kk - i - 1]}", "take more from a" if ok else "take at most i from a"))
    if ok:
        lo = i + 1
    else:
        hi = i
i, j = lo, kk - lo
ansk = max(a[i - 1] if i > 0 else -10**18, b[j - 1] if j > 0 else -10**18)
EXTRA["kth-of-two-lists"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One list may be empty.
        - All of the first `k` may come from one list.
        - Duplicates count separately.
        """
    ],
    "think": [
        KTH,
        f"""
        **A split, not a value.** The first `k` elements of the merged order are a prefix of `a` (say `i` elements) plus a
        prefix of `b` (`k − i` elements). The split is right when the last element taken from each list is no bigger than
        the first element **not** taken from the other. If `a[i] < b[k − i − 1]`, an element of `a` that we didn't take is
        smaller than one we did take from `b`: take more from `a`. This test is monotone in `i`, so binary search `i`
        over `[max(0, k − n), min(k, m)]` (searching the shorter list). For `a = {A}`, `b = {B}`, `k = {kk}`:
        """,
        table(["lo", "hi", "i (from a)", "k − i (from b)", "compare", "decision"], *prows),
        f"Take {i} from a and {j} from b; the k-th is the larger of their last elements: **{ansk}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Concatenate, sort, take the k-th."],
            "build": ["Concatenate.", "Sort.", "Index `k − 1`."],
            "complexity": ["**Time O((m + n) log(m + n)).** **Space O(m + n).**"],
            "limits": ["Re-sorts two already sorted lists."],
        },
        1: {
            "idea": ["Merge the two lists for `k` steps, always taking the smaller front."],
            "build": ["Two pointers.", "Take the smaller front `k` times."],
            "complexity": ["**Time O(k).** **Space O(1).**"],
            "limits": ["Linear in `k`; binary searching the split takes O(log min(m, n))."],
        },
        2: {
            "idea": ["Swap so `a` is shorter. Binary search `i` (elements from `a`) in `[max(0, k − n), min(k, m)]` with the test `a[i] < b[k − i − 1]`; the answer is `max(a[i − 1], b[k − i − 1])` with missing elements treated as −∞."],
            "build": ["Search the shorter list.", "Valid range for `i`.", "Monotone split test.", "Larger of the two last-taken elements."],
            "complexity": ["**Time O(log min(m, n)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **k-th of two sorted lists:** binary search how many come from the shorter list.
        - Clamp the split range so neither list is over- or under-used.
        - **Pitfall:** searching the longer list (indices can run out of range in the other).
        """
    ],
}


# ---------------------------------------------------------------- median-of-two-queues
QA, QB = [1, 5, 8, 12], [2, 3, 9, 10, 15]
a, b = (QA, QB) if len(QA) <= len(QB) else (QB, QA)
m, n = len(a), len(b)
half = (m + n + 1) // 2
INF = float("inf")
lo, hi, mrows, med = 0, m, [], None
while True:
    i = (lo + hi) // 2
    j = half - i
    al = a[i - 1] if i > 0 else -INF
    ar = a[i] if i < m else INF
    bl = b[j - 1] if j > 0 else -INF
    br = b[j] if j < n else INF
    fmt = lambda x: "−∞" if x == -INF else ("∞" if x == INF else str(x))
    if al <= br and bl <= ar:
        med = float(max(al, bl)) if (m + n) % 2 else (max(al, bl) + min(ar, br)) / 2
        mrows.append((i, j, f"{fmt(al)} | {fmt(ar)}", f"{fmt(bl)} | {fmt(br)}", "valid partition"))
        break
    if al > br:
        mrows.append((i, j, f"{fmt(al)} | {fmt(ar)}", f"{fmt(bl)} | {fmt(br)}", "a's left part too big: fewer from a"))
        hi = i - 1
    else:
        mrows.append((i, j, f"{fmt(al)} | {fmt(ar)}", f"{fmt(bl)} | {fmt(br)}", "b's left part too big: more from a"))
        lo = i + 1
EXTRA["median-of-two-queues"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - One queue empty.
        - Even total: average of the two middle values.
        - All values of one queue smaller than the other's.
        """
    ],
    "think": [
        KTH,
        f"""
        **Partition both lists.** Put a cut in each list so that the left sides together hold `⌈(m + n) / 2⌉` values. The
        cut is correct when everything on the left is no bigger than everything on the right, which only needs two checks:
        `a_left ≤ b_right` and `b_left ≤ a_right`. If `a_left > b_right`, too much was taken from `a`; if `b_left > a_right`,
        too little. The median is then the largest left value (odd total), or the average of the largest left and smallest
        right values (even total). Missing neighbours act as ±∞. For `a = {QA}`, `b = {QB}`:
        """,
        table(["i (left of a)", "j (left of b)", "a: left | right", "b: left | right", "decision"], *mrows),
        f"Median **{med:g}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Merge the two lists up to the middle, remembering the last two values seen; the median is the middle one (odd total) or their average."],
            "build": ["Two pointers.", "Advance `(m + n)/2 + 1` times.", "Median from the last one or two values."],
            "complexity": ["**Time O(m + n).** **Space O(1).**"],
            "limits": ["Linear; the partition can be found by binary search over the shorter list."],
        },
        1: {
            "idea": ["Swap so `a` is shorter. Binary search the cut `i` in `a` (with `j = half − i` in `b`) until the two cross-checks hold; compute the median from the four boundary values."],
            "build": ["Search the shorter list.", "Boundary values with ±∞ for missing ones.", "Move the cut by the failing check.", "Median from the boundaries."],
            "complexity": ["**Time O(log min(m, n)).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Median of two sorted arrays:** binary search a partition of the shorter array.
        - Validity needs only the two cross comparisons at the cut.
        - **Pitfall:** forgetting ±∞ for empty sides of a cut.
        """
    ],
}
