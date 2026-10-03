"""Binary Search: unknown bounds (exponential search)."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def zeros_of(n):
    t = 0
    while n:
        n //= 5
        t += n
    return t


@problem
def stack_of_cans():
    cans = 1000
    r = 1
    while r * (r + 1) // 2 < cans:
        r += 1
    want = r
    assert want == 45

    w1 = Steps("Add rows one at a time until the stack holds enough cans.")
    total = 0
    for k in range(1, want + 1):
        total += k
        if k <= 3 or k >= want - 1:
            w1.step(f"Row {k}: the stack holds {total} cans" + (f" ≥ {cans}. Done." if total >= cans else "."), Vars(rows=k, holds=total))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary search on rows in a fixed range [1, 2 × 10⁸] that safely contains every answer.")
    lo, hi = 1, 200_000_000
    steps = 0
    while lo < hi:
        mid = (lo + hi) // 2
        ok = mid * (mid + 1) // 2 >= cans
        steps += 1
        if steps <= 6 or hi - lo < 64:
            w2.step(f"lo={lo}, hi={hi}, mid={mid}: holds {mid * (mid + 1) // 2} → " + ("enough: hi = mid." if ok else "too few: lo = mid + 1."), Vars(lo=lo, mid=mid, hi=hi))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    w2.step(f"{steps} halvings: {lo} rows.", Vars(rows=lo), result=lo)

    w3 = Steps("Double hi (1, 2, 4, 8, …) until it's big enough, then binary-search between hi/2 and hi.")
    hi = 1
    while hi * (hi + 1) // 2 < cans:
        w3.step(f"hi = {hi}: holds {hi * (hi + 1) // 2} < {cans}. Double it.", Vars(hi=hi))
        hi *= 2
    w3.step(f"hi = {hi}: holds {hi * (hi + 1) // 2} ≥ {cans}. The answer is in ({hi // 2}, {hi}].", Vars(hi=hi))
    lo = hi // 2
    while lo < hi:
        mid = (lo + hi) // 2
        ok = mid * (mid + 1) // 2 >= cans
        w3.step(f"lo={lo}, hi={hi}, mid={mid}: holds {mid * (mid + 1) // 2} → " + ("enough." if ok else "too few."), Vars(lo=lo, mid=mid, hi=hi))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    w3.steps[-1]["result"] = str(lo)

    sol(
        "stack-of-cans",
        summary="""
            The capacity r(r + 1)/2 grows with r, so the answer is the first r whose capacity reaches `cans`: a lower-bound
            binary search on r. When you don't know how big r can get, find an upper bound first by doubling (1, 2, 4, …).
            That's exponential search: O(log r) steps, and every number stays small enough not to overflow.
        """,
        question=[
            """
            A triangular stack with r rows holds r(r + 1)/2 cans. Return the smallest r that holds at least `cans`.

            - **At least:** 7 cans need 4 rows (3 rows hold only 6).
            - **cans up to 9 × 10¹⁵**, so the answer is about 1.3 × 10⁸. Counting rows one at a time is slow, and computing
              r(r + 1) for r as large as `cans` overflows 64 bits.
            """
        ],
        think=[
            f"""
            Take {cans} cans. 44 rows hold 990, 45 rows hold 1035, so the answer is {want}.

            "Does r rows hold enough?" is false for small r and true from the answer on: binary search on r. The question
            is the range. Searching `[1, cans]` is valid but squaring numbers near 9 × 10¹⁵ overflows. Two fixes:

            - **Work out a safe bound by hand:** r = 2 × 10⁸ already holds 2 × 10¹⁶ > 9 × 10¹⁵ cans.
            - **Find a bound automatically:** try r = 1, 2, 4, 8, … until it's enough. The first r that works is less than
              twice the answer, so it never overshoots by much (and never overflows). Then binary-search between r/2 and r.
            """,
            fig(Row(["1", "2", "4", "8", "16", "32", "64"], st={6: "answer"}, label="r tried while doubling"), caption="64 rows is the first power of two holding ≥ 1000 cans; the answer is in (32, 64]."),
        ],
        approaches=[
            approach(
                "Add rows one at a time",
                "brute",
                "O(√cans)",
                "O(1)",
                idea=["Keep adding rows (1 can, 2 cans, 3 cans, …) until the running total reaches `cans`."],
                walk=w1,
                build=["`rows = 0`, `total = 0`.", "While `total < cans`: `rows += 1`, `total += rows`.", "Return `rows`."],
                code={
                    "python": """
                        class Solution:
                            def rowsNeeded(self, cans: int) -> int:
                                rows = total = 0  #@init
                                while total < cans:  #@add
                                    rows += 1  #@add
                                    total += rows  #@add
                                return rows  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long rowsNeeded(long cans) {
                                long rows = 0, total = 0;  //@init
                                while (total < cans) {  //@add
                                    rows++;  //@add
                                    total += rows;  //@add
                                }
                                return rows;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long rowsNeeded(long long cans) {
                                long long rows = 0, total = 0;  //@init
                                while (total < cans) {  //@add
                                    rows++;  //@add
                                    total += rows;  //@add
                                }
                                return rows;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long rowsNeeded(long long cans) {
                            long long rows = 0, total = 0;  //@init
                            while (total < cans) {  //@add
                                rows++;  //@add
                                total += rows;  //@add
                            }
                            return rows;  //@ret
                        }
                    """,
                },
                lines=[("init", "No rows yet."), ("add", "The next row has one more can than the previous one."), ("ret", "The first row count that holds enough.")],
                complexity=["**Time O(√cans):** about 1.3 × 10⁸ iterations at the limit. **Space O(1).**"],
                limits=["One row per step, while the capacity check is monotonic in r and could be bisected."],
                slow=True,
            ),
            approach(
                "Binary search in a hand-derived range",
                "better",
                "O(log B)",
                "O(1)",
                idea=["Search r in `[1, 2 × 10⁸]`, a range worked out from the constraint (2 × 10⁸ rows hold more than 9 × 10¹⁵ cans, and mid(mid + 1) stays below 4 × 10¹⁶, inside 64 bits). Lower bound: first r with r(r + 1)/2 ≥ cans."],
                walk=w2,
                build=["`lo = 1`, `hi = 2 × 10⁸`.", "If `mid(mid + 1)/2 ≥ cans`, `hi = mid`; else `lo = mid + 1`.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def rowsNeeded(self, cans: int) -> int:
                                lo, hi = 1, 200_000_000  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if mid * (mid + 1) // 2 >= cans:  #@test
                                        hi = mid  #@test
                                    else:  #@test
                                        lo = mid + 1  #@test
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long rowsNeeded(long cans) {
                                long lo = 1, hi = 200_000_000L;  //@range
                                while (lo < hi) {  //@loop
                                    long mid = lo + (hi - lo) / 2;  //@loop
                                    if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@test
                                    else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long rowsNeeded(long long cans) {
                                long long lo = 1, hi = 200000000LL;  //@range
                                while (lo < hi) {  //@loop
                                    long long mid = lo + (hi - lo) / 2;  //@loop
                                    if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@test
                                    else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long rowsNeeded(long long cans) {
                            long long lo = 1, hi = 200000000LL;  //@range
                            while (lo < hi) {  //@loop
                                long long mid = lo + (hi - lo) / 2;  //@loop
                                if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@test
                                else lo = mid + 1;  //@test
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "A bound derived from the constraints: big enough for any input, small enough that mid·(mid + 1) can't overflow."), ("loop", "Lower-bound loop."), ("test", "Enough cans → the answer is mid or smaller."), ("ret", "The fewest rows.")],
                complexity=["**Time O(log B)** with B = 2 × 10⁸: about 28 steps. **Space O(1).**"],
                limits=["It relies on working out a bound by hand. If the limits change (or the function is harder to invert), a wrong bound silently breaks it. Exponential search finds a tight bound by itself."],
            ),
            approach(
                "Exponential search, then binary search",
                "best",
                "O(log r)",
                "O(1)",
                idea=["Double `hi` from 1 until `hi(hi + 1)/2 ≥ cans`. The answer is then in `(hi/2, hi]`, because `hi/2` was still too small. Binary-search that interval. Since `hi < 2r`, every product stays far below the overflow limit."],
                walk=w3,
                build=["`hi = 1`; while it's not enough, `hi *= 2`.", "`lo = hi / 2`.", "Lower-bound binary search in `[lo, hi]`.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def rowsNeeded(self, cans: int) -> int:
                                hi = 1  #@grow
                                while hi * (hi + 1) // 2 < cans:  #@grow
                                    hi *= 2  #@grow
                                lo = hi // 2  #@search
                                while lo < hi:  #@search
                                    mid = (lo + hi) // 2  #@search
                                    if mid * (mid + 1) // 2 >= cans:  #@search
                                        hi = mid  #@search
                                    else:  #@search
                                        lo = mid + 1  #@search
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long rowsNeeded(long cans) {
                                long hi = 1;  //@grow
                                while (hi * (hi + 1) / 2 < cans) hi *= 2;  //@grow
                                long lo = hi / 2;  //@search
                                while (lo < hi) {  //@search
                                    long mid = lo + (hi - lo) / 2;  //@search
                                    if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@search
                                    else lo = mid + 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long rowsNeeded(long long cans) {
                                long long hi = 1;  //@grow
                                while (hi * (hi + 1) / 2 < cans) hi *= 2;  //@grow
                                long long lo = hi / 2;  //@search
                                while (lo < hi) {  //@search
                                    long long mid = lo + (hi - lo) / 2;  //@search
                                    if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@search
                                    else lo = mid + 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long rowsNeeded(long long cans) {
                            long long hi = 1;  //@grow
                            while (hi * (hi + 1) / 2 < cans) hi *= 2;  //@grow
                            long long lo = hi / 2;  //@search
                            while (lo < hi) {  //@search
                                long long mid = lo + (hi - lo) / 2;  //@search
                                if (mid * (mid + 1) / 2 >= cans) hi = mid;  //@search
                                else lo = mid + 1;  //@search
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("grow", "Double until the capacity is enough: about log₂(r) ≈ 28 doublings at most. hi stays below 2r ≈ 2.7 × 10⁸, so hi·(hi + 1) is about 7 × 10¹⁶, safely inside 64 bits."), ("search", "hi/2 was too small (or is 0 when hi = 1), so the answer is in (hi/2, hi]: standard lower-bound search there."), ("ret", "The fewest rows.")],
                complexity=["**Time O(log r):** doubling plus bisecting. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Exponential (galloping) search:** when the range is unknown, double an upper bound until the condition
              holds, then binary-search the last doubling interval. Cost O(log answer).
            - It also keeps intermediate values close to the answer's size, which avoids overflow.
            """
        ],
    )


@problem
def zeros_at_the_end():
    zeros = 7
    n = 0
    while zeros_of(n) < zeros:
        n += 1
    want = n
    assert want == 30

    w1 = Steps("Try n = 0, 1, 2, … computing the trailing zeros of n! each time (count factors of 5).")
    for k in [0, 4, 5, 10, 24, 25, 29, 30]:
        w1.step(f"n = {k}: n! ends with {zeros_of(k)} zero{'s' if zeros_of(k) != 1 else ''}" + (f" ≥ {zeros}. Answer." if zeros_of(k) >= zeros else "."), Vars(n=k, zeros=zeros_of(k)))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Double hi until hi! has enough zeros, then binary-search between hi/2 and hi.")
    hi = 1
    while zeros_of(hi) < zeros:
        w2.step(f"hi = {hi}: {zeros_of(hi)} zeros < {zeros}. Double.", Vars(hi=hi, zeros=zeros_of(hi)))
        hi *= 2
    w2.step(f"hi = {hi}: {zeros_of(hi)} zeros ≥ {zeros}. The answer is in ({hi // 2}, {hi}].", Vars(hi=hi, zeros=zeros_of(hi)))
    lo = hi // 2
    while lo < hi:
        mid = (lo + hi) // 2
        ok = zeros_of(mid) >= zeros
        w2.step(f"lo={lo}, hi={hi}, mid={mid}: {zeros_of(mid)} zeros → " + ("enough: hi = mid." if ok else "too few: lo = mid + 1."), Vars(lo=lo, mid=mid, hi=hi))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    w2.steps[-1]["result"] = str(lo)

    sol(
        "zeros-at-the-end",
        summary="""
            n! ends in as many zeros as it has factors of 5 (twos are always more plentiful): ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ….
            That count never decreases as n grows, so the answer is the first n whose count reaches `zeros`. Without a known
            upper bound, double a guess until it's large enough, then binary-search: O(log² n).
        """,
        question=[
            """
            Return the smallest n such that n! ends with **at least** `zeros` zeros. (0! = 1 has no trailing zeros.)

            - **At least:** some zero counts are skipped. 24! ends in 4 zeros and 25! in 6, so asking for 5 zeros gives 25.
            - **zeros = 0** → n = 0.
            - **zeros up to 2 × 10¹⁵**, so n reaches about 8 × 10¹⁵. Never compute n! itself; count factors of 5.
            """
        ],
        think=[
            f"""
            A trailing zero comes from a factor 10 = 2 × 5. Among 1 … n there are far more factors of 2 than of 5, so the
            number of zeros equals the number of 5s: multiples of 5 give one each, multiples of 25 an extra one, multiples
            of 125 another, and so on. So `zeros(n) = n/5 + n/25 + n/125 + …` (integer divisions).

            Take {zeros} zeros: zeros(29) = 5 + 1 = 6, zeros(30) = 6 + 1 = 7. The answer is {want}.
            """,
            fig(Row([0, 4, 5, 10, 24, 25, 29, 30], label="n"), Row([zeros_of(x) for x in [0, 4, 5, 10, 24, 25, 29, 30]], label="zeros of n!"), caption="Non-decreasing in n, jumping by 2 at multiples of 25."),
            """
            Non-decreasing means "zeros(n) ≥ target" is false, then true: binary search on n. The problem doesn't give a
            bound for n, so find one by doubling: 1, 2, 4, 8, … until zeros(hi) ≥ target, then search `(hi/2, hi]`.
            """,
        ],
        approaches=[
            approach(
                "Count up from 0",
                "brute",
                "O(n log n)",
                "O(1)",
                idea=["Try n = 0, 1, 2, … and stop at the first n whose factor-of-5 count reaches the target."],
                walk=w1,
                build=["Write `zeros(n)`: add n/5, n/25, … by repeatedly dividing by 5.", "Increase n from 0 until `zeros(n) ≥ target`."],
                code={
                    "python": """
                        class Solution:
                            def smallestWithZeros(self, zeros: int) -> int:
                                def count(n):  #@count
                                    total = 0  #@count
                                    while n:  #@count
                                        n //= 5  #@count
                                        total += n  #@count
                                    return total  #@count
                                n = 0  #@walk
                                while count(n) < zeros:  #@walk
                                    n += 1  #@walk
                                return n  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long smallestWithZeros(long zeros) {
                                long n = 0;  //@walk
                                while (count(n) < zeros) n++;  //@walk
                                return n;  //@ret
                            }

                            private long count(long n) {  //@count
                                long total = 0;  //@count
                                while (n > 0) { n /= 5; total += n; }  //@count
                                return total;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                            long long count(long long n) {  //@count
                                long long total = 0;  //@count
                                while (n > 0) { n /= 5; total += n; }  //@count
                                return total;  //@count
                            }  //@count

                        public:
                            long long smallestWithZeros(long long zeros) {
                                long long n = 0;  //@walk
                                while (count(n) < zeros) n++;  //@walk
                                return n;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long countFives(long long n) {  //@count
                            long long total = 0;  //@count
                            while (n > 0) { n /= 5; total += n; }  //@count
                            return total;  //@count
                        }  //@count

                        long long smallestWithZeros(long long zeros) {
                            long long n = 0;  //@walk
                            while (countFives(n) < zeros) n++;  //@walk
                            return n;  //@ret
                        }
                    """,
                },
                lines=[("count", "Trailing zeros of n! = factors of 5 in 1 … n: n/5 numbers give one, n/25 give a second, and so on. Repeated division by 5 adds exactly those terms."), ("walk", "Step n up until the count reaches the target."), ("ret", "The first such n.")],
                complexity=["**Time O(n log n):** n can be 8 × 10¹⁵. **Space O(1).**"],
                limits=["Walks through every n, although the count is non-decreasing and can be bisected. (Even stepping n by 5, since the count only changes at multiples of 5, is still linear.)"],
                slow=16,
            ),
            approach(
                "Exponential search, then binary search",
                "best",
                "O(log² n)",
                "O(1)",
                idea=["Return 0 for zero zeros. Otherwise double `hi` from 1 until `count(hi) ≥ zeros`; then binary-search the first n in `(hi/2, hi]` with `count(n) ≥ zeros`."],
                walk=w2,
                build=["Handle `zeros == 0`.", "Double hi until it has enough zeros.", "Lower-bound search in `[hi/2, hi]`.", "Return lo."],
                code={
                    "python": """
                        class Solution:
                            def smallestWithZeros(self, zeros: int) -> int:
                                def count(n):  #@count
                                    total = 0  #@count
                                    while n:  #@count
                                        n //= 5  #@count
                                        total += n  #@count
                                    return total  #@count
                                if zeros == 0:  #@zero
                                    return 0  #@zero
                                hi = 1  #@grow
                                while count(hi) < zeros:  #@grow
                                    hi *= 2  #@grow
                                lo = hi // 2  #@search
                                while lo < hi:  #@search
                                    mid = (lo + hi) // 2  #@search
                                    if count(mid) >= zeros:  #@search
                                        hi = mid  #@search
                                    else:  #@search
                                        lo = mid + 1  #@search
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long smallestWithZeros(long zeros) {
                                if (zeros == 0) return 0;  //@zero
                                long hi = 1;  //@grow
                                while (count(hi) < zeros) hi *= 2;  //@grow
                                long lo = hi / 2;  //@search
                                while (lo < hi) {  //@search
                                    long mid = lo + (hi - lo) / 2;  //@search
                                    if (count(mid) >= zeros) hi = mid; else lo = mid + 1;  //@search
                                }
                                return lo;  //@ret
                            }

                            private long count(long n) {  //@count
                                long total = 0;  //@count
                                while (n > 0) { n /= 5; total += n; }  //@count
                                return total;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                            long long count(long long n) {  //@count
                                long long total = 0;  //@count
                                while (n > 0) { n /= 5; total += n; }  //@count
                                return total;  //@count
                            }  //@count

                        public:
                            long long smallestWithZeros(long long zeros) {
                                if (zeros == 0) return 0;  //@zero
                                long long hi = 1;  //@grow
                                while (count(hi) < zeros) hi *= 2;  //@grow
                                long long lo = hi / 2;  //@search
                                while (lo < hi) {  //@search
                                    long long mid = lo + (hi - lo) / 2;  //@search
                                    if (count(mid) >= zeros) hi = mid; else lo = mid + 1;  //@search
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long countFives(long long n) {  //@count
                            long long total = 0;  //@count
                            while (n > 0) { n /= 5; total += n; }  //@count
                            return total;  //@count
                        }  //@count

                        long long smallestWithZeros(long long zeros) {
                            if (zeros == 0) return 0;  //@zero
                            long long hi = 1;  //@grow
                            while (countFives(hi) < zeros) hi *= 2;  //@grow
                            long long lo = hi / 2;  //@search
                            while (lo < hi) {  //@search
                                long long mid = lo + (hi - lo) / 2;  //@search
                                if (countFives(mid) >= zeros) hi = mid; else lo = mid + 1;  //@search
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("count", "Factors of 5 in n!, in O(log n)."), ("zero", "Asking for at least 0 zeros: n = 0 already qualifies (0! = 1)."), ("grow", "Double until enough zeros. n ≤ 8 × 10¹⁵ means at most ~53 doublings, and hi stays below 2⁵⁴, inside 64 bits."), ("search", "hi/2 had too few zeros, so the answer is in (hi/2, hi]: lower-bound binary search."), ("ret", "The smallest n.")],
                complexity=["**Time O(log² n):** O(log n) counts during doubling and bisecting, each O(log n). **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Trailing zeros of n! = Σ ⌊n / 5ᵏ⌋: a monotonic function of n.
            - When no bound is given, **gallop**: double until the condition holds, then binary-search the last interval.
            - Some targets are skipped (no n gives exactly 5 zeros), which is why the problem asks for "at least".
            """
        ],
    )
