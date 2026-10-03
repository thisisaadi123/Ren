"""Binary Search: searching on the answer."""
import math

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

TEMPLATE = """
    **Searching on the answer.** The answer is a number in a known range, and there's a yes/no test ("is this value
    good enough?") that is false for small values and true from the answer onward (or the reverse). Binary search
    that boundary: O(log range) tests, each costing one pass over the input.
"""


def answer_walk(W, lo, hi, test, last=False, max_steps=14):
    """Record a binary search for the first value with test(v) true (or the last with test true if last=True).
    test(v) returns (bool, explanation)."""
    steps = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2 if last else (lo + hi) // 2
        ok, why = test(mid)
        if steps < max_steps:
            if last:
                W.step(f"lo={lo}, hi={hi}, try {mid}: {why} → " + (f"works, so the answer is ≥ {mid}." if ok else f"fails, so the answer is < {mid}."), Vars(lo=lo, mid=mid, hi=hi))
            else:
                W.step(f"lo={lo}, hi={hi}, try {mid}: {why} → " + (f"works, so the answer is ≤ {mid}." if ok else f"fails, so the answer is > {mid}."), Vars(lo=lo, mid=mid, hi=hi))
        steps += 1
        if last:
            if ok:
                lo = mid
            else:
                hi = mid - 1
        else:
            if ok:
                hi = mid
            else:
                lo = mid + 1
    return lo


@problem
def reading_speed():
    books, hours = [3, 6, 7, 11], 8

    def hrs(s):
        return sum((p + s - 1) // s for p in books)

    want = next(s for s in range(1, max(books) + 1) if hrs(s) <= hours)

    w1 = Steps("Try speeds 1, 2, 3, … and stop at the first that fits in the hours.")
    for s in range(1, want + 1):
        w1.step(f"Speed {s}: " + " + ".join(str((p + s - 1) // s) for p in books) + f" = {hrs(s)} hours" + (f" ≤ {hours}. Done." if hrs(s) <= hours else f" > {hours}."), Row(books, label="pages", slots=True), Vars(speed=s, hours=hrs(s)))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary-search the speed in [1, largest book]: hours needed only go down as speed goes up.")
    r = answer_walk(w2, 1, max(books), lambda s: (hrs(s) <= hours, f"{' + '.join(str((p + s - 1) // s) for p in books)} = {hrs(s)} hours"))
    w2.step(f"Slowest speed that fits: {r}.", Vars(speed=r), result=r)

    sol(
        "reading-speed",
        summary="""
            At speed s, book p takes ⌈p / s⌉ hours. Faster never takes longer, so "speed s fits within `hours`" flips from
            false to true exactly once. Binary-search s between 1 and the largest book (that speed always fits, since
            hours ≥ number of books): O(n log max).
        """,
        question=[
            """
            Each hour you read up to s pages from **one** book (leftover time in that hour is wasted). Return the smallest
            whole-number s that finishes all books within `hours`.

            - **One book per hour:** a 3-page book at speed 4 still costs a full hour.
            - **hours ≥ number of books**, so a speed equal to the largest book (one hour per book) always works. That's the
              top of the search range.
            - **Hours can sum past 32 bits** at low speeds (10⁴ books × 10⁹ pages at speed 1), so add them in 64 bits.
            """
        ],
        think=[
            f"""
            Take books `{books}` and {hours} hours. At speed 3: 1 + 2 + 3 + 4 = 10 hours, too slow. At speed 4:
            1 + 2 + 2 + 3 = 8 hours, fits. So the answer is 4.
            """,
            fig(Row(list(range(1, 8)), label="speed"), Row([hrs(s) for s in range(1, 8)], st={want - 1: "answer"}, label="hours needed"), caption="Hours needed never increase with speed; the answer is the first speed at or under the limit."),
            TEMPLATE,
        ],
        approaches=[
            approach(
                "Try every speed",
                "brute",
                "O(max · n)",
                "O(1)",
                idea=["Start at speed 1 and increase until the total hours fit."],
                walk=w1,
                build=["For s = 1, 2, …: total = Σ ⌈p / s⌉.", "Return the first s with total ≤ hours."],
                code={
                    "python": """
                        class Solution:
                            def minReadingSpeed(self, books: List[int], hours: int) -> int:
                                s = 1  #@try
                                while sum((p + s - 1) // s for p in books) > hours:  #@try
                                    s += 1  #@try
                                return s  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minReadingSpeed(int[] books, int hours) {
                                for (int s = 1; ; s++) {  //@try
                                    long total = 0;  //@try
                                    for (int p : books) total += (p + (long) s - 1) / s;  //@try
                                    if (total <= hours) return s;  //@ret
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minReadingSpeed(vector<int>& books, int hours) {
                                for (int s = 1; ; s++) {  //@try
                                    long long total = 0;  //@try
                                    for (int p : books) total += (p + (long long) s - 1) / s;  //@try
                                    if (total <= hours) return s;  //@ret
                                }
                            }
                        };
                    """,
                    "c": """
                        int minReadingSpeed(int* books, int booksSize, int hours) {
                            for (int s = 1; ; s++) {  //@try
                                long long total = 0;  //@try
                                for (int i = 0; i < booksSize; i++) total += (books[i] + (long long) s - 1) / s;  //@try
                                if (total <= hours) return s;  //@ret
                            }
                        }
                    """,
                },
                lines=[("try", "Hours at speed s: ⌈p / s⌉ per book, computed as `(p + s − 1) / s` with integers (64-bit, since p + s can pass 2³¹ and the total can be large)."), ("ret", "The first speed that fits is the slowest one.")],
                complexity=["**Time O(max · n):** up to 10⁹ speeds × 10⁴ books. **Space O(1).**"],
                limits=["Tests speeds one by one, although the test is monotonic: once a speed fits, every faster one fits too."],
                slow=True,
            ),
            approach(
                "Binary search on the speed",
                "best",
                "O(n log max)",
                "O(1)",
                idea=["`lo = 1`, `hi = max(books)`. If speed mid fits (Σ ⌈p / mid⌉ ≤ hours), `hi = mid`; else `lo = mid + 1`. Return `lo`."],
                walk=w2,
                build=["Range `[1, max(books)]`.", "Feasibility test: total hours at speed mid (64-bit).", "Lower-bound search for the first feasible speed."],
                code={
                    "python": """
                        class Solution:
                            def minReadingSpeed(self, books: List[int], hours: int) -> int:
                                lo, hi = 1, max(books)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    needed = sum((p + mid - 1) // mid for p in books)  #@test
                                    if needed <= hours:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minReadingSpeed(int[] books, int hours) {
                                int lo = 1, hi = 0;  //@range
                                for (int p : books) hi = Math.max(hi, p);  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long needed = 0;  //@test
                                    for (int p : books) needed += (p + (long) mid - 1) / mid;  //@test
                                    if (needed <= hours) hi = mid; else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minReadingSpeed(vector<int>& books, int hours) {
                                int lo = 1, hi = *max_element(books.begin(), books.end());  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long long needed = 0;  //@test
                                    for (int p : books) needed += (p + (long long) mid - 1) / mid;  //@test
                                    if (needed <= hours) hi = mid; else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minReadingSpeed(int* books, int booksSize, int hours) {
                            int lo = 1, hi = 0;  //@range
                            for (int i = 0; i < booksSize; i++) if (books[i] > hi) hi = books[i];  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                long long needed = 0;  //@test
                                for (int i = 0; i < booksSize; i++) needed += (books[i] + (long long) mid - 1) / mid;  //@test
                                if (needed <= hours) hi = mid; else lo = mid + 1;  //@move
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "Speed 1 is the slowest possible; reading a whole book per hour (the largest book) always fits because hours ≥ number of books."), ("loop", "Halve the speed range."), ("test", "Hours needed at speed mid: ceiling division per book, summed in 64 bits."), ("move", "Fits → the answer is mid or slower. Doesn't fit → faster."), ("ret", "The slowest speed that fits.")],
                complexity=["**Time O(n log max):** about 30 tests of n books each. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "Smallest rate that finishes in time" → binary search on the rate with a feasibility pass.
            - Ceiling division with integers: `(p + s − 1) / s`.
            - The search range's top comes from the constraints (one book per hour always works).
            """
        ],
    )


@problem
def smallest_divisor():
    loads, threshold = [1, 2, 5, 9], 6

    def tot(d):
        return sum((x + d - 1) // d for x in loads)

    want = next(d for d in range(1, max(loads) + 1) if tot(d) <= threshold)

    w1 = Steps("Try d = 1, 2, 3, … until the rounded-up total is at most the threshold.")
    for d in range(1, want + 1):
        w1.step(f"d = {d}: " + " + ".join(str((x + d - 1) // d) for x in loads) + f" = {tot(d)}" + (f" ≤ {threshold}. Done." if tot(d) <= threshold else f" > {threshold}."), Row(loads, slots=True), Vars(d=d, total=tot(d)))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary-search d in [1, max load]; the total never increases as d grows.")
    r = answer_walk(w2, 1, max(loads), lambda d: (tot(d) <= threshold, f"total {tot(d)}"))
    w2.step(f"Smallest d: {r}.", Vars(d=r), result=r)

    sol(
        "smallest-divisor",
        summary="""
            The rounded-up total Σ ⌈x / d⌉ only shrinks (or stays) as d grows, so "total ≤ threshold" flips from false to
            true once. Binary-search d in [1, max(loads)]: at d = max every term is 1, and threshold ≥ n guarantees that
            works. O(n log max).
        """,
        question=[
            """
            Choose a positive integer d; divide each load by d **rounding up**, and add the results. Return the smallest d
            whose total is at most `threshold`.

            - **Rounding up:** 5 / 2 counts as 3, and 1 / 9 counts as 1, so every term is at least 1.
            - **threshold ≥ n**, so d = max(loads) (all terms 1) always works.
            """
        ],
        think=[
            f"""
            Take `{loads}`, threshold {threshold}. d = 4: 1 + 1 + 2 + 3 = 7 (too big). d = 5: 1 + 1 + 1 + 2 = 5 (fits). So the
            answer is 5.
            """,
            fig(Row(list(range(1, 10)), label="d"), Row([tot(d) for d in range(1, 10)], st={want - 1: "answer"}, label="total"), caption="The total never increases with d: binary-searchable."),
            TEMPLATE,
        ],
        approaches=[
            approach(
                "Try every divisor",
                "brute",
                "O(max · n)",
                "O(1)",
                idea=["Increase d from 1 until the total fits."],
                walk=w1,
                build=["For d = 1, 2, …: total = Σ ⌈x / d⌉; return the first d with total ≤ threshold."],
                code={
                    "python": """
                        class Solution:
                            def smallestDivisor(self, loads: List[int], threshold: int) -> int:
                                d = 1  #@try
                                while sum((x + d - 1) // d for x in loads) > threshold:  #@try
                                    d += 1  #@try
                                return d  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int smallestDivisor(int[] loads, int threshold) {
                                for (int d = 1; ; d++) {  //@try
                                    long total = 0;  //@try
                                    for (int x : loads) total += (x + d - 1) / d;  //@try
                                    if (total <= threshold) return d;  //@ret
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int smallestDivisor(vector<int>& loads, int threshold) {
                                for (int d = 1; ; d++) {  //@try
                                    long long total = 0;  //@try
                                    for (int x : loads) total += (x + d - 1) / d;  //@try
                                    if (total <= threshold) return d;  //@ret
                                }
                            }
                        };
                    """,
                    "c": """
                        int smallestDivisor(int* loads, int loadsSize, int threshold) {
                            for (int d = 1; ; d++) {  //@try
                                long long total = 0;  //@try
                                for (int i = 0; i < loadsSize; i++) total += (loads[i] + d - 1) / d;  //@try
                                if (total <= threshold) return d;  //@ret
                            }
                        }
                    """,
                },
                lines=[("try", "Total for divisor d, rounding each quotient up with `(x + d − 1) / d`. Loads and d are ≤ 10⁶, so the sum per term fits in `int`; the total is kept in 64 bits."), ("ret", "The first d that fits is the smallest.")],
                complexity=["**Time O(max · n):** up to 10⁶ × 5 × 10⁴. **Space O(1).**"],
                limits=["Linear in the range of d; the monotonic test allows binary search."],
                slow=True,
            ),
            approach(
                "Binary search on d",
                "best",
                "O(n log max)",
                "O(1)",
                idea=["Lower-bound search in [1, max(loads)] with the test `Σ ⌈x / mid⌉ ≤ threshold`."],
                walk=w2,
                build=["Range `[1, max]`.", "Compute the total for mid.", "Fits → `hi = mid`; else `lo = mid + 1`."],
                code={
                    "python": """
                        class Solution:
                            def smallestDivisor(self, loads: List[int], threshold: int) -> int:
                                lo, hi = 1, max(loads)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if sum((x + mid - 1) // mid for x in loads) <= threshold:  #@test
                                        hi = mid  #@test
                                    else:  #@test
                                        lo = mid + 1  #@test
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int smallestDivisor(int[] loads, int threshold) {
                                int lo = 1, hi = 0;  //@range
                                for (int x : loads) hi = Math.max(hi, x);  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long total = 0;  //@test
                                    for (int x : loads) total += (x + mid - 1) / mid;  //@test
                                    if (total <= threshold) hi = mid; else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int smallestDivisor(vector<int>& loads, int threshold) {
                                int lo = 1, hi = *max_element(loads.begin(), loads.end());  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long long total = 0;  //@test
                                    for (int x : loads) total += (x + mid - 1) / mid;  //@test
                                    if (total <= threshold) hi = mid; else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int smallestDivisor(int* loads, int loadsSize, int threshold) {
                            int lo = 1, hi = 0;  //@range
                            for (int i = 0; i < loadsSize; i++) if (loads[i] > hi) hi = loads[i];  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                long long total = 0;  //@test
                                for (int i = 0; i < loadsSize; i++) total += (loads[i] + mid - 1) / mid;  //@test
                                if (total <= threshold) hi = mid; else lo = mid + 1;  //@test
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "d = max(loads) makes every term 1, which fits because threshold ≥ n."), ("loop", "Halve the range."), ("test", "Total for mid; fits → answer ≤ mid, else > mid."), ("ret", "The smallest divisor that fits.")],
                complexity=["**Time O(n log max):** about 20 passes. **Space O(1).**"],
            ),
        ],
        takeaways=["- Same template as **Reading Speed**: minimise a parameter subject to a monotonic sum-of-ceilings test."],
    )


@problem
def print_shop_daily_limit():
    pages, days = [4, 2, 7, 3, 5, 6, 1], 3

    def need(limit):
        used, load = 1, 0
        for p in pages:
            if load + p > limit:
                used += 1
                load = 0
            load += p
        return used

    lo0, hi0 = max(pages), sum(pages)
    want = next(L for L in range(lo0, hi0 + 1) if need(L) <= days)

    w1 = Steps("Try limits from the largest job upward until the jobs fit in the days.")
    for L in range(lo0, want + 1):
        w1.step(f"Limit {L}: needs {need(L)} day{'s' if need(L) != 1 else ''}" + (f" ≤ {days}. Done." if need(L) <= days else f" > {days}."), Row(pages, slots=True), Vars(limit=L, days=need(L)))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary-search the limit in [largest job, all pages]: a bigger limit never needs more days.")

    def explain(L):
        groups, cur, load = [], [], 0
        for p in pages:
            if load + p > L:
                groups.append(cur)
                cur, load = [], 0
            cur.append(p)
            load += p
        groups.append(cur)
        return need(L) <= days, f"days {' | '.join('+'.join(map(str, g)) for g in groups)} ({len(groups)} days)"

    r = answer_walk(w2, lo0, hi0, explain)
    w2.step(f"Smallest limit: {r}.", Vars(limit=r), result=r)

    sol(
        "print-shop-daily-limit",
        summary="""
            For a given daily limit, the fewest days needed is found greedily: keep adding jobs to today until the next one
            doesn't fit. A higher limit never needs more days, so binary-search the limit between the largest job and the
            total page count: O(n log(sum)).
        """,
        question=[
            """
            Jobs print in order, whole jobs only. With one fixed daily page limit, the shop prints as many whole jobs as fit
            each day. Return the smallest limit that finishes all jobs within `days` days.

            - **Order is fixed and jobs can't split:** each day prints a contiguous block of jobs.
            - **The limit must be at least the largest job**, or that job can never print.
            - **The limit never needs to exceed the total**, which prints everything in one day.
            """
        ],
        think=[
            f"""
            Take jobs `{pages}` and {days} days. With limit 10 the days go 4+2 | 7+3 | 5 | 6+1: 4 days, too many. With limit
            {want}: {explain(want)[1].replace('days ', '')}, which fits.
            """,
            fig(Row(pages, slots=True), caption="Each day prints a run of consecutive jobs up to the limit."),
            """
            **Checking one limit is easy:** fill each day greedily; when the next job doesn't fit, start a new day. Packing
            as much as possible into each day can only reduce the number of days, so greedy gives the minimum days for that
            limit.

            **Choosing the limit is the search:** days needed never increase as the limit grows. So "limit L finishes in
            time" is false, then true, and binary search finds the first true.
            """,
        ],
        approaches=[
            approach(
                "Try limits upward",
                "brute",
                "O(sum · n)",
                "O(1)",
                idea=["Start at the largest job and raise the limit by 1 until the greedy day count fits."],
                walk=w1,
                build=["Write `daysNeeded(limit)` (greedy).", "For L from max(pages) upward, return the first L with `daysNeeded(L) ≤ days`."],
                code={
                    "python": """
                        class Solution:
                            def minDailyLimit(self, pages: List[int], days: int) -> int:
                                def days_needed(limit):  #@greedy
                                    used, load = 1, 0  #@greedy
                                    for p in pages:  #@greedy
                                        if load + p > limit:  #@greedy
                                            used += 1  #@greedy
                                            load = 0  #@greedy
                                        load += p  #@greedy
                                    return used  #@greedy
                                limit = max(pages)  #@try
                                while days_needed(limit) > days:  #@try
                                    limit += 1  #@try
                                return limit  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minDailyLimit(int[] pages, int days) {
                                int limit = 0;  //@try
                                for (int p : pages) limit = Math.max(limit, p);  //@try
                                while (daysNeeded(pages, limit) > days) limit++;  //@try
                                return limit;  //@ret
                            }

                            private int daysNeeded(int[] pages, int limit) {  //@greedy
                                int used = 1, load = 0;  //@greedy
                                for (int p : pages) {  //@greedy
                                    if (load + p > limit) { used++; load = 0; }  //@greedy
                                    load += p;  //@greedy
                                }  //@greedy
                                return used;  //@greedy
                            }  //@greedy
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minDailyLimit(vector<int>& pages, int days) {
                                auto daysNeeded = [&](int limit) {  //@greedy
                                    int used = 1, load = 0;  //@greedy
                                    for (int p : pages) {  //@greedy
                                        if (load + p > limit) { used++; load = 0; }  //@greedy
                                        load += p;  //@greedy
                                    }  //@greedy
                                    return used;  //@greedy
                                };  //@greedy
                                int limit = *max_element(pages.begin(), pages.end());  //@try
                                while (daysNeeded(limit) > days) limit++;  //@try
                                return limit;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int daysNeeded(const int* pages, int n, int limit) {  //@greedy
                            int used = 1, load = 0;  //@greedy
                            for (int i = 0; i < n; i++) {  //@greedy
                                if (load + pages[i] > limit) { used++; load = 0; }  //@greedy
                                load += pages[i];  //@greedy
                            }  //@greedy
                            return used;  //@greedy
                        }  //@greedy

                        int minDailyLimit(int* pages, int pagesSize, int days) {
                            int limit = 0;  //@try
                            for (int i = 0; i < pagesSize; i++) if (pages[i] > limit) limit = pages[i];  //@try
                            while (daysNeeded(pages, pagesSize, limit) > days) limit++;  //@try
                            return limit;  //@ret
                        }
                    """,
                },
                lines=[("greedy", "Fewest days for a given limit: keep adding jobs to today; when the next job would overflow, start a new day. (Totals stay ≤ 2.5 × 10⁷, fine for `int`.)"), ("try", "Start at the largest job (smaller limits can't work) and step up."), ("ret", "The first limit that fits.")],
                complexity=["**Time O(sum · n):** up to 2.5 × 10⁷ limits × 5 × 10⁴ jobs. **Space O(1).**"],
                limits=["Steps the limit one page at a time, although days needed only decrease as the limit rises."],
                slow=True,
            ),
            approach(
                "Binary search on the limit",
                "best",
                "O(n log(sum))",
                "O(1)",
                idea=["`lo = max(pages)`, `hi = sum(pages)`. If `daysNeeded(mid) ≤ days`, `hi = mid`; else `lo = mid + 1`. Return `lo`."],
                walk=w2,
                build=["Range `[max(pages), sum(pages)]`.", "Greedy day count for mid.", "Lower-bound search for the first limit that fits."],
                code={
                    "python": """
                        class Solution:
                            def minDailyLimit(self, pages: List[int], days: int) -> int:
                                def days_needed(limit):  #@greedy
                                    used, load = 1, 0  #@greedy
                                    for p in pages:  #@greedy
                                        if load + p > limit:  #@greedy
                                            used += 1  #@greedy
                                            load = 0  #@greedy
                                        load += p  #@greedy
                                    return used  #@greedy
                                lo, hi = max(pages), sum(pages)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if days_needed(mid) <= days:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minDailyLimit(int[] pages, int days) {
                                int lo = 0, hi = 0;  //@range
                                for (int p : pages) { lo = Math.max(lo, p); hi += p; }  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (daysNeeded(pages, mid) <= days) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }

                            private int daysNeeded(int[] pages, int limit) {  //@greedy
                                int used = 1, load = 0;  //@greedy
                                for (int p : pages) {  //@greedy
                                    if (load + p > limit) { used++; load = 0; }  //@greedy
                                    load += p;  //@greedy
                                }  //@greedy
                                return used;  //@greedy
                            }  //@greedy
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minDailyLimit(vector<int>& pages, int days) {
                                auto daysNeeded = [&](int limit) {  //@greedy
                                    int used = 1, load = 0;  //@greedy
                                    for (int p : pages) {  //@greedy
                                        if (load + p > limit) { used++; load = 0; }  //@greedy
                                        load += p;  //@greedy
                                    }  //@greedy
                                    return used;  //@greedy
                                };  //@greedy
                                int lo = *max_element(pages.begin(), pages.end());  //@range
                                int hi = accumulate(pages.begin(), pages.end(), 0);  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (daysNeeded(mid) <= days) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int daysNeeded(const int* pages, int n, int limit) {  //@greedy
                            int used = 1, load = 0;  //@greedy
                            for (int i = 0; i < n; i++) {  //@greedy
                                if (load + pages[i] > limit) { used++; load = 0; }  //@greedy
                                load += pages[i];  //@greedy
                            }  //@greedy
                            return used;  //@greedy
                        }  //@greedy

                        int minDailyLimit(int* pages, int pagesSize, int days) {
                            int lo = 0, hi = 0;  //@range
                            for (int i = 0; i < pagesSize; i++) { if (pages[i] > lo) lo = pages[i]; hi += pages[i]; }  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (daysNeeded(pages, pagesSize, mid) <= days) hi = mid;  //@move
                                else lo = mid + 1;  //@move
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("greedy", "Greedy packing gives the fewest days for a limit."), ("range", "The answer is at least the largest job and at most the sum (everything in one day)."), ("loop", "Halve the limit range."), ("move", "Fits within the days → mid or less might work; otherwise more is needed."), ("ret", "The smallest workable limit.")],
                complexity=["**Time O(n log(sum)):** about 25 greedy passes. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Split an array into at most k contiguous parts minimising the largest part sum**: binary-search the largest
              sum, check with a greedy fill.
            - Range: from the largest single item to the total.
            """
        ],
    )


@problem
def bouquet_day():
    bloom, bouquets, size = [3, 9, 4, 8, 2, 5, 1, 7], 2, 2

    def can(day):
        made = run = 0
        for b in bloom:
            run = run + 1 if b <= day else 0
            if run == size:
                made += 1
                run = 0
        return made >= bouquets

    days_sorted = sorted(set(bloom))
    want = next(d for d in days_sorted if can(d))

    w1 = Steps("Try each distinct bloom day in increasing order; the first day on which enough bouquets can be made is the answer.")
    for d in days_sorted:
        w1.step(f"Day {d}: bloomed " + "".join("■" if b <= d else "□" for b in bloom) + (" → enough adjacent runs." if can(d) else " → not enough."), Row(bloom, st={i: ("found" if b <= d else "dim") for i, b in enumerate(bloom)}, slots=True), Vars(day=d))
        if can(d):
            w1.steps[-1]["result"] = str(d)
            break

    w2 = Steps("Binary-search the day in [earliest bloom, latest bloom]; more days never means fewer bouquets.")

    def explain(d):
        made = run = 0
        for b in bloom:
            run = run + 1 if b <= d else 0
            if run == size:
                made += 1
                run = 0
        return made >= bouquets, f"{made} bouquet{'s' if made != 1 else ''} possible"

    r = answer_walk(w2, min(bloom), max(bloom), explain)
    w2.step(f"Earliest day: {r}.", Row(bloom, st={i: ("found" if b <= r else "dim") for i, b in enumerate(bloom)}, slots=True), result=r)

    sol(
        "bouquet-day",
        summary="""
            On a given day, count bouquets greedily: walk the row, extend a run of bloomed flowers, and cut a bouquet each
            time the run reaches `size`. Waiting longer never hurts, so binary-search the earliest day between the first
            and last bloom. If there aren't even enough flowers in total, return −1.
        """,
        question=[
            """
            Flower i blooms on day `bloom[i]` and stays bloomed. A bouquet takes `size` **adjacent** flowers; each flower
            is used once. Return the earliest day you can make `bouquets` bouquets, or −1.

            - **Adjacent** matters: three bloomed flowers separated by an unbloomed one don't make a bouquet of 3.
            - **Impossible** exactly when `bouquets × size > n`: even on the last day there aren't enough flowers. That
              product can reach 10⁶ × 10⁵, so compute it in 64 bits.
            - **The answer is always a bloom day** (bouquet counts only change when a flower blooms).
            """
        ],
        think=[
            f"""
            Take `{bloom}`, {bouquets} bouquets of {size}. By day 5 the bloomed positions are
            {[i for i, b in enumerate(bloom) if b <= 5]}: the only adjacent run is 4–6, which gives just 1 bouquet of {size}.
            On day {want} the bloomed pattern
            `{''.join('■' if b <= want else '□' for b in bloom)}` allows {bouquets}.
            """,
            fig(Row(bloom, st={i: ("found" if b <= want else "dim") for i, b in enumerate(bloom)}, slots=True), caption=f"Bloomed by day {want} (light)."),
            """
            Two pieces:

            - **For a fixed day,** counting bouquets greedily from the left is optimal: taking the leftmost possible
              bouquet never blocks a better choice.
            - **Across days,** a later day has every flower an earlier day had, so the count never drops. The test "day d
              is enough" is monotonic: binary search on d.
            """,
        ],
        approaches=[
            approach(
                "Try each bloom day in order",
                "brute",
                "O(n² log n)",
                "O(n)",
                idea=["Sort the distinct bloom days; for each in increasing order, count bouquets; return the first day that gives enough. (Return −1 up front if there aren't enough flowers at all.)"],
                walk=w1,
                build=["If `bouquets × size > n`, return −1.", "Sort distinct bloom days.", "For each day, greedy-count bouquets; return the first that's enough."],
                code={
                    "python": """
                        class Solution:
                            def earliestBouquetDay(self, bloom: List[int], bouquets: int, size: int) -> int:
                                if bouquets * size > len(bloom):  #@impossible
                                    return -1  #@impossible
                                def count(day):  #@count
                                    made = run = 0  #@count
                                    for b in bloom:  #@count
                                        run = run + 1 if b <= day else 0  #@count
                                        if run == size:  #@count
                                            made += 1  #@count
                                            run = 0  #@count
                                    return made  #@count
                                for day in sorted(set(bloom)):  #@try
                                    if count(day) >= bouquets:  #@try
                                        return day  #@try
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int earliestBouquetDay(int[] bloom, int bouquets, int size) {
                                if ((long) bouquets * size > bloom.length) return -1;  //@impossible
                                int[] days = Arrays.stream(bloom).distinct().sorted().toArray();  //@try
                                for (int day : days) if (count(bloom, day, size) >= bouquets) return day;  //@try
                                return -1;  //@none
                            }

                            private int count(int[] bloom, int day, int size) {  //@count
                                int made = 0, run = 0;  //@count
                                for (int b : bloom) {  //@count
                                    run = b <= day ? run + 1 : 0;  //@count
                                    if (run == size) { made++; run = 0; }  //@count
                                }  //@count
                                return made;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int earliestBouquetDay(vector<int>& bloom, int bouquets, int size) {
                                if ((long long) bouquets * size > (long long) bloom.size()) return -1;  //@impossible
                                auto count = [&](int day) {  //@count
                                    int made = 0, run = 0;  //@count
                                    for (int b : bloom) {  //@count
                                        run = b <= day ? run + 1 : 0;  //@count
                                        if (run == size) { made++; run = 0; }  //@count
                                    }  //@count
                                    return made;  //@count
                                };  //@count
                                vector<int> days = bloom;  //@try
                                sort(days.begin(), days.end());  //@try
                                days.erase(unique(days.begin(), days.end()), days.end());  //@try
                                for (int day : days) if (count(day) >= bouquets) return day;  //@try
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        static int countBouquets(const int* bloom, int n, int day, int size) {  //@count
                            int made = 0, run = 0;  //@count
                            for (int i = 0; i < n; i++) {  //@count
                                run = bloom[i] <= day ? run + 1 : 0;  //@count
                                if (run == size) { made++; run = 0; }  //@count
                            }  //@count
                            return made;  //@count
                        }  //@count

                        static int cmpInt(const void* a, const void* b) {  //@try
                            int p = *(const int*) a, q = *(const int*) b;  //@try
                            return (p > q) - (p < q);  //@try
                        }  //@try

                        int earliestBouquetDay(int* bloom, int bloomSize, int bouquets, int size) {
                            if ((long long) bouquets * size > bloomSize) return -1;  //@impossible
                            int* days = malloc(bloomSize * sizeof(int));  //@try
                            memcpy(days, bloom, bloomSize * sizeof(int));  //@try
                            qsort(days, bloomSize, sizeof(int), cmpInt);  //@try
                            int answer = -1;  //@try
                            for (int i = 0; i < bloomSize && answer < 0; i++) {  //@try
                                if (i > 0 && days[i] == days[i - 1]) continue;  //@try
                                if (countBouquets(bloom, bloomSize, days[i], size) >= bouquets) answer = days[i];  //@try
                            }
                            free(days);  //@none
                            return answer;  //@none
                        }
                    """,
                },
                lines=[("impossible", "Not enough flowers even when all have bloomed (64-bit product)."), ("count", "Greedy bouquet count for one day: a run of bloomed flowers grows; at `size`, cut a bouquet and restart the run; an unbloomed flower breaks the run."), ("try", "Candidate days are the bloom days, smallest first."), ("none", "Unreachable once enough flowers exist (the last bloom day always works).")],
                complexity=["**Time O(n²)** count passes in the worst case (n distinct days), plus the sort. **Space O(n).**"],
                limits=["Tests every candidate day in order; the test is monotonic, so binary search needs only ~30 tests."],
                slow=True,
            ),
            approach(
                "Binary search on the day",
                "best",
                "O(n log(max day))",
                "O(1)",
                idea=["After the impossibility check, search the first day in `[min(bloom), max(bloom)]` with `count(day) ≥ bouquets`."],
                walk=w2,
                build=["Return −1 if `bouquets × size > n`.", "Range `[min, max]` of bloom days.", "Greedy count for mid; enough → `hi = mid`, else `lo = mid + 1`."],
                code={
                    "python": """
                        class Solution:
                            def earliestBouquetDay(self, bloom: List[int], bouquets: int, size: int) -> int:
                                if bouquets * size > len(bloom):  #@impossible
                                    return -1  #@impossible
                                def enough(day):  #@count
                                    made = run = 0  #@count
                                    for b in bloom:  #@count
                                        run = run + 1 if b <= day else 0  #@count
                                        if run == size:  #@count
                                            made += 1  #@count
                                            run = 0  #@count
                                    return made >= bouquets  #@count
                                lo, hi = min(bloom), max(bloom)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if enough(mid):  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int earliestBouquetDay(int[] bloom, int bouquets, int size) {
                                if ((long) bouquets * size > bloom.length) return -1;  //@impossible
                                int lo = Integer.MAX_VALUE, hi = 0;  //@range
                                for (int b : bloom) { lo = Math.min(lo, b); hi = Math.max(hi, b); }  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (count(bloom, mid, size) >= bouquets) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }

                            private int count(int[] bloom, int day, int size) {  //@count
                                int made = 0, run = 0;  //@count
                                for (int b : bloom) {  //@count
                                    run = b <= day ? run + 1 : 0;  //@count
                                    if (run == size) { made++; run = 0; }  //@count
                                }  //@count
                                return made;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int earliestBouquetDay(vector<int>& bloom, int bouquets, int size) {
                                if ((long long) bouquets * size > (long long) bloom.size()) return -1;  //@impossible
                                auto count = [&](int day) {  //@count
                                    int made = 0, run = 0;  //@count
                                    for (int b : bloom) {  //@count
                                        run = b <= day ? run + 1 : 0;  //@count
                                        if (run == size) { made++; run = 0; }  //@count
                                    }  //@count
                                    return made;  //@count
                                };  //@count
                                auto [mn, mx] = minmax_element(bloom.begin(), bloom.end());  //@range
                                int lo = *mn, hi = *mx;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (count(mid) >= bouquets) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int countBouquets(const int* bloom, int n, int day, int size) {  //@count
                            int made = 0, run = 0;  //@count
                            for (int i = 0; i < n; i++) {  //@count
                                run = bloom[i] <= day ? run + 1 : 0;  //@count
                                if (run == size) { made++; run = 0; }  //@count
                            }  //@count
                            return made;  //@count
                        }  //@count

                        int earliestBouquetDay(int* bloom, int bloomSize, int bouquets, int size) {
                            if ((long long) bouquets * size > bloomSize) return -1;  //@impossible
                            int lo = bloom[0], hi = bloom[0];  //@range
                            for (int i = 1; i < bloomSize; i++) { if (bloom[i] < lo) lo = bloom[i]; if (bloom[i] > hi) hi = bloom[i]; }  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (countBouquets(bloom, bloomSize, mid, size) >= bouquets) hi = mid;  //@move
                                else lo = mid + 1;  //@move
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("impossible", "Not enough flowers in total."), ("count", "Greedy bouquet count for a day."), ("range", "Before the first bloom nothing is possible; by the last bloom day everything is (given enough flowers)."), ("loop", "Halve the day range."), ("move", "Enough bouquets → that day or earlier; otherwise later."), ("ret", "The earliest workable day.")],
                complexity=["**Time O(n log(max day)):** about 30 passes. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "Earliest time when a monotonic condition holds" → binary search on time.
            - Contiguity constraints are usually checked with a greedy run counter.
            - Rule out the impossible case first, so the search always has a valid answer.
            """
        ],
    )


@problem
def shuttle_rounds():
    rt, total = [3, 5, 8], 7

    def rounds(t):
        return sum(t // x for x in rt)

    want = next(t for t in range(1, min(rt) * total + 1) if rounds(t) >= total)

    w1 = Steps("Advance the clock minute by minute until the shuttles have finished enough rounds.")
    for t in range(1, want + 1):
        if rounds(t) != rounds(t - 1) or t == want:
            w1.step(f"Minute {t}: " + " + ".join(str(t // x) for x in rt) + f" = {rounds(t)} rounds" + (f" ≥ {total}. Done." if rounds(t) >= total else "."), Row(rt, label="minutes per round", slots=True), Vars(minute=t, rounds=rounds(t)))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary-search the time in [1, fastest round × total]: rounds finished never decrease over time.")
    r = answer_walk(w2, 1, min(rt) * total, lambda t: (rounds(t) >= total, f"{' + '.join(str(t // x) for x in rt)} = {rounds(t)} rounds"))
    w2.step(f"Earliest time: {r} minutes.", Vars(minutes=r), result=r)

    sol(
        "shuttle-rounds",
        summary="""
            By minute t, shuttle i has finished ⌊t / roundTime[i]⌋ rounds; the total only grows with t. So binary-search
            the earliest t whose total reaches `totalRounds`. The fastest shuttle alone finishes in `min × totalRounds`
            minutes, which bounds the search. O(n log(min · total)).
        """,
        question=[
            """
            Shuttles run in parallel; shuttle i completes a round every `roundTime[i]` minutes. Return the earliest minute by
            which they've completed at least `totalRounds` rounds together.

            - **Only completed rounds count**, so shuttle i contributes ⌊t / roundTime[i]⌋ by minute t.
            - **The answer can exceed 32 bits:** up to 10⁷ minutes per round × 10⁷ rounds = 10¹⁴. Return a 64-bit value and
              do the search in 64 bits.
            """
        ],
        think=[
            f"""
            Take round times `{rt}` and {total} rounds. By minute {want}: {' + '.join(str(want // x) for x in rt)} = {rounds(want)}
            rounds, enough. One minute earlier, at {want - 1}: {' + '.join(str((want - 1) // x) for x in rt)} = {rounds(want - 1)},
            not enough. So the answer is {want}.
            """,
            fig(Row([t for t in range(want - 3, want + 3)], label="minute"), Row([rounds(t) for t in range(want - 3, want + 3)], st={3: "answer"}, label="rounds done"), caption="Rounds done only increase with time."),
            TEMPLATE,
        ],
        approaches=[
            approach(
                "Advance the clock one minute at a time",
                "brute",
                "O(T · n)",
                "O(1)",
                idea=["Check t = 1, 2, 3, … until the total of ⌊t / roundTime[i]⌋ reaches the target."],
                walk=w1,
                build=["For t = 1, 2, …: total = Σ ⌊t / roundTime[i]⌋ (64-bit).", "Return the first t with total ≥ target."],
                code={
                    "python": """
                        class Solution:
                            def minTimeForRounds(self, roundTime: List[int], totalRounds: int) -> int:
                                t = 1  #@tick
                                while sum(t // r for r in roundTime) < totalRounds:  #@tick
                                    t += 1  #@tick
                                return t  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long minTimeForRounds(int[] roundTime, int totalRounds) {
                                for (long t = 1; ; t++) {  //@tick
                                    long done = 0;  //@tick
                                    for (int r : roundTime) done += t / r;  //@tick
                                    if (done >= totalRounds) return t;  //@ret
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long minTimeForRounds(vector<int>& roundTime, int totalRounds) {
                                for (long long t = 1; ; t++) {  //@tick
                                    long long done = 0;  //@tick
                                    for (int r : roundTime) done += t / r;  //@tick
                                    if (done >= totalRounds) return t;  //@ret
                                }
                            }
                        };
                    """,
                    "c": """
                        long long minTimeForRounds(int* roundTime, int roundTimeSize, int totalRounds) {
                            for (long long t = 1; ; t++) {  //@tick
                                long long done = 0;  //@tick
                                for (int i = 0; i < roundTimeSize; i++) done += t / roundTime[i];  //@tick
                                if (done >= totalRounds) return t;  //@ret
                            }
                        }
                    """,
                },
                lines=[("tick", "Rounds finished by minute t, summed over shuttles (64-bit)."), ("ret", "The first minute with enough rounds.")],
                complexity=["**Time O(T · n)** for an answer of T minutes (up to 10¹⁴). **Space O(1).**"],
                limits=["One minute at a time, although rounds done only ever increase: bisect the time instead."],
                slow=True,
            ),
            approach(
                "Binary search on time",
                "best",
                "O(n log(min · total))",
                "O(1)",
                idea=["Search t in `[1, min(roundTime) × totalRounds]` (the fastest shuttle alone gets there). If rounds by mid ≥ target, `hi = mid`; else `lo = mid + 1`."],
                walk=w2,
                build=["Range `[1, min × total]` in 64 bits.", "Count rounds by mid.", "Lower-bound search."],
                code={
                    "python": """
                        class Solution:
                            def minTimeForRounds(self, roundTime: List[int], totalRounds: int) -> int:
                                lo, hi = 1, min(roundTime) * totalRounds  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if sum(mid // r for r in roundTime) >= totalRounds:  #@test
                                        hi = mid  #@test
                                    else:  #@test
                                        lo = mid + 1  #@test
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long minTimeForRounds(int[] roundTime, int totalRounds) {
                                int fastest = Integer.MAX_VALUE;  //@range
                                for (int r : roundTime) fastest = Math.min(fastest, r);  //@range
                                long lo = 1, hi = (long) fastest * totalRounds;  //@range
                                while (lo < hi) {  //@loop
                                    long mid = lo + (hi - lo) / 2;  //@loop
                                    long done = 0;  //@test
                                    for (int r : roundTime) { done += mid / r; if (done >= totalRounds) break; }  //@test
                                    if (done >= totalRounds) hi = mid; else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long minTimeForRounds(vector<int>& roundTime, int totalRounds) {
                                long long lo = 1, hi = (long long) *min_element(roundTime.begin(), roundTime.end()) * totalRounds;  //@range
                                while (lo < hi) {  //@loop
                                    long long mid = lo + (hi - lo) / 2;  //@loop
                                    long long done = 0;  //@test
                                    for (int r : roundTime) { done += mid / r; if (done >= totalRounds) break; }  //@test
                                    if (done >= totalRounds) hi = mid; else lo = mid + 1;  //@test
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long minTimeForRounds(int* roundTime, int roundTimeSize, int totalRounds) {
                            int fastest = roundTime[0];  //@range
                            for (int i = 1; i < roundTimeSize; i++) if (roundTime[i] < fastest) fastest = roundTime[i];  //@range
                            long long lo = 1, hi = (long long) fastest * totalRounds;  //@range
                            while (lo < hi) {  //@loop
                                long long mid = lo + (hi - lo) / 2;  //@loop
                                long long done = 0;  //@test
                                for (int i = 0; i < roundTimeSize && done < totalRounds; i++) done += mid / roundTime[i];  //@test
                                if (done >= totalRounds) hi = mid; else lo = mid + 1;  //@test
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("range", "Upper bound: the fastest shuttle alone completes the target by `fastest × total` minutes (64-bit: up to 10¹⁴)."), ("loop", "Halve the time range."), ("test", "Rounds finished by mid. Stopping the sum early once the target is reached keeps it from growing needlessly (each term can be up to 10¹⁴, and there are 10⁵ of them)."), ("ret", "The earliest minute.")],
                complexity=["**Time O(n log(min · total)):** about 47 passes. **Space O(1).**"],
            ),
        ],
        takeaways=["- \"Earliest time to finish k units of parallel work\" → binary search on time, counting completed units per worker."],
    )


@problem
def spread_the_sensors():
    spots, k = [1, 9, 4, 12, 7, 20], 3
    s = sorted(spots)

    def fits(g):
        placed, last = 1, s[0]
        for x in s[1:]:
            if x - last >= g:
                placed += 1
                last = x
        return placed >= k

    top = (s[-1] - s[0]) // (k - 1)
    want = max(g for g in range(1, top + 1) if fits(g))

    def placement(g):
        out, last = [s[0]], s[0]
        for x in s[1:]:
            if x - last >= g:
                out.append(x)
                last = x
        return out

    w1 = Steps("Try spacings from the largest possible downward; the first that fits is the answer.")
    for g in range(top, want - 1, -1):
        w1.step(f"Spacing {g}: greedy placement {placement(g)} → " + (f"{len(placement(g))} sensors ≥ {k}. Done." if fits(g) else f"only {len(placement(g))} sensors."), Row(s, st={s.index(x): "answer" if fits(g) else "found" for x in placement(g)}, slots=True), Vars(spacing=g))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Binary-search the spacing (find the largest that still fits). Check a spacing greedily: place at the first spot, then at the next spot at least that far away.")
    r = answer_walk(w2, 1, top, lambda g: (fits(g), f"greedy places {placement(g)}"), last=True)
    w2.step(f"Largest spacing: {r}.", Row(s, st={s.index(x): "answer" for x in placement(r)}, slots=True), result=r)

    sol(
        "spread-the-sensors",
        summary="""
            Fix a minimum spacing g. Whether k sensors fit is a greedy question: sort the spots, place one at the first spot
            and each next one at the first spot at least g further. Larger g can only fit fewer sensors, so binary-search
            the **largest** g that still fits. O(n log n + n log(range)).
        """,
        question=[
            """
            Choose `sensors` distinct spots to maximise the smallest distance between any two chosen spots. Return that
            distance.

            - **Spots are unsorted:** sort them first.
            - **Maximise the minimum:** the answer is a spacing, not a set of spots.
            - **Upper bound:** with k sensors spread over a span of (last − first), some gap is at most span / (k − 1).
            """
        ],
        think=[
            f"""
            Take spots `{spots}` (sorted `{s}`) and {k} sensors. With spacing 9: place at 1, then the first spot ≥ 10 is 12,
            then the first ≥ 21 doesn't exist: only 2 sensors. With spacing {want}: {placement(want)}, which is {k}. So the
            answer is {want}.
            """,
            fig(Row(s, st={s.index(x): "answer" for x in placement(want)}, slots=True), caption=f"Greedy placement with spacing {want}."),
            """
            **Checking a spacing:** greedy from the left is optimal. Putting the first sensor at the leftmost spot leaves the
            most room for the rest, and each next sensor goes as early as allowed for the same reason.

            **Searching:** if spacing g fits, every smaller spacing fits too. So "g fits" is true up to the answer and false
            beyond it. This time we want the **last** true, so use the upper midpoint `(lo + hi + 1) / 2` with `lo = mid` on
            success.
            """,
        ],
        approaches=[
            approach(
                "Try spacings from the top down",
                "brute",
                "O(n log n + range · n)",
                "O(n)",
                idea=["Sort the spots. For g = span/(k − 1) down to 1, run the greedy check; the first g that fits is the largest."],
                walk=w1,
                build=["Sort.", "For g from the upper bound down, greedily count sensors.", "Return the first g that fits."],
                code={
                    "python": """
                        class Solution:
                            def widestSpacing(self, spots: List[int], sensors: int) -> int:
                                s = sorted(spots)  #@sort
                                def fits(gap):  #@fits
                                    placed, last = 1, s[0]  #@fits
                                    for x in s[1:]:  #@fits
                                        if x - last >= gap:  #@fits
                                            placed += 1  #@fits
                                            last = x  #@fits
                                    return placed >= sensors  #@fits
                                gap = (s[-1] - s[0]) // (sensors - 1)  #@try
                                while not fits(gap):  #@try
                                    gap -= 1  #@try
                                return gap  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int widestSpacing(int[] spots, int sensors) {
                                int[] s = spots.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int gap = (s[s.length - 1] - s[0]) / (sensors - 1);  //@try
                                while (!fits(s, gap, sensors)) gap--;  //@try
                                return gap;  //@ret
                            }

                            private boolean fits(int[] s, int gap, int sensors) {  //@fits
                                int placed = 1, last = s[0];  //@fits
                                for (int i = 1; i < s.length; i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                                return placed >= sensors;  //@fits
                            }  //@fits
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int widestSpacing(vector<int>& spots, int sensors) {
                                vector<int> s = spots;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                auto fits = [&](int gap) {  //@fits
                                    int placed = 1, last = s[0];  //@fits
                                    for (size_t i = 1; i < s.size(); i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                                    return placed >= sensors;  //@fits
                                };  //@fits
                                int gap = (s.back() - s[0]) / (sensors - 1);  //@try
                                while (!fits(gap)) gap--;  //@try
                                return gap;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        static bool fits(const int* s, int n, int gap, int sensors) {  //@fits
                            int placed = 1, last = s[0];  //@fits
                            for (int i = 1; i < n; i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                            return placed >= sensors;  //@fits
                        }  //@fits

                        int widestSpacing(int* spots, int spotsSize, int sensors) {
                            int* s = malloc(spotsSize * sizeof(int));  //@sort
                            memcpy(s, spots, spotsSize * sizeof(int));  //@sort
                            qsort(s, spotsSize, sizeof(int), cmpInt);  //@sort
                            int gap = (s[spotsSize - 1] - s[0]) / (sensors - 1);  //@try
                            while (!fits(s, spotsSize, gap, sensors)) gap--;  //@try
                            free(s);  //@ret
                            return gap;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Positions in order."), ("fits", "Greedy check: first sensor at the leftmost spot, each next one at the earliest spot at least `gap` away. Differences of positions ≤ 10⁹ fit in `int`."), ("try", "Start from the largest spacing that could possibly work and step down. Spacing 1 always fits (spots are distinct), so the loop ends."), ("ret", "The first (largest) spacing that fits.")],
                complexity=["**Time O(n log n + range · n):** the range can be 10⁹. **Space O(n).**"],
                limits=["Steps one unit at a time through a range of up to 10⁹; the fits test is monotonic, so bisect it."],
                slow=True,
            ),
            approach(
                "Binary search for the largest spacing",
                "best",
                "O(n log n + n log(range))",
                "O(n)",
                idea=["Sort. Search g in `[1, span / (k − 1)]` for the **last** g that fits: upper midpoint; fits → `lo = mid`, else `hi = mid − 1`."],
                walk=w2,
                build=["Sort the spots.", "`lo = 1`, `hi = span / (k − 1)`.", "`mid = (lo + hi + 1) / 2`; greedy check; move.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def widestSpacing(self, spots: List[int], sensors: int) -> int:
                                s = sorted(spots)  #@sort
                                def fits(gap):  #@fits
                                    placed, last = 1, s[0]  #@fits
                                    for x in s[1:]:  #@fits
                                        if x - last >= gap:  #@fits
                                            placed += 1  #@fits
                                            last = x  #@fits
                                    return placed >= sensors  #@fits
                                lo, hi = 1, (s[-1] - s[0]) // (sensors - 1)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi + 1) // 2  #@loop
                                    if fits(mid):  #@move
                                        lo = mid  #@move
                                    else:  #@move
                                        hi = mid - 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int widestSpacing(int[] spots, int sensors) {
                                int[] s = spots.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int lo = 1, hi = (s[s.length - 1] - s[0]) / (sensors - 1);  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo + 1) / 2;  //@loop
                                    if (fits(s, mid, sensors)) lo = mid;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return lo;  //@ret
                            }

                            private boolean fits(int[] s, int gap, int sensors) {  //@fits
                                int placed = 1, last = s[0];  //@fits
                                for (int i = 1; i < s.length; i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                                return placed >= sensors;  //@fits
                            }  //@fits
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int widestSpacing(vector<int>& spots, int sensors) {
                                vector<int> s = spots;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                auto fits = [&](int gap) {  //@fits
                                    int placed = 1, last = s[0];  //@fits
                                    for (size_t i = 1; i < s.size(); i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                                    return placed >= sensors;  //@fits
                                };  //@fits
                                int lo = 1, hi = (s.back() - s[0]) / (sensors - 1);  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo + 1) / 2;  //@loop
                                    if (fits(mid)) lo = mid;  //@move
                                    else hi = mid - 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        static bool fits(const int* s, int n, int gap, int sensors) {  //@fits
                            int placed = 1, last = s[0];  //@fits
                            for (int i = 1; i < n; i++) if (s[i] - last >= gap) { placed++; last = s[i]; }  //@fits
                            return placed >= sensors;  //@fits
                        }  //@fits

                        int widestSpacing(int* spots, int spotsSize, int sensors) {
                            int* s = malloc(spotsSize * sizeof(int));  //@sort
                            memcpy(s, spots, spotsSize * sizeof(int));  //@sort
                            qsort(s, spotsSize, sizeof(int), cmpInt);  //@sort
                            int lo = 1, hi = (s[spotsSize - 1] - s[0]) / (sensors - 1);  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo + 1) / 2;  //@loop
                                if (fits(s, spotsSize, mid, sensors)) lo = mid;  //@move
                                else hi = mid - 1;  //@move
                            }
                            free(s);  //@ret
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Positions in order."), ("fits", "Greedy feasibility check for a spacing."), ("range", "Spacing 1 always fits; no spacing above span / (k − 1) can (k − 1 gaps must cover at most the span)."), ("loop", "Upper midpoint, because we keep `lo = mid` on success and must still make progress when `hi = lo + 1`."), ("move", "Fits → the answer is mid or larger. Doesn't → smaller."), ("ret", "The largest spacing that fits.")],
                complexity=["**Time O(n log n + n log(range)).** **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - **Maximise the minimum distance** → binary-search the distance, check with a greedy left-to-right placement.
            - For the *largest* feasible value use the upper midpoint and `lo = mid`.
            """
        ],
    )


@problem
def kth_closest_pair():
    h, k = [4, 1, 9, 6, 3], 4
    gaps = sorted(abs(h[i] - h[j]) for i in range(len(h)) for j in range(i + 1, len(h)))
    want = gaps[k - 1]
    s = sorted(h)

    def within(d):
        tot = left = 0
        for right in range(len(s)):
            while s[right] - s[left] > d:
                left += 1
            tot += right - left
        return tot

    w1 = Steps("List every pair's gap, sort them, take the k-th.")
    w1.step(f"All {len(gaps)} gaps sorted: {gaps}.", Row(h, slots=True), Row(gaps, st={k - 1: "answer"}, label="gaps", slots=True), result=want)
    w1.steps.insert(0, {"text": f"{len(h)} people make {len(gaps)} pairs.", "panels": [Row(h, slots=True)]})

    w2 = Steps("Sort the heights. Binary-search the gap d: count pairs with gap ≤ d using a sliding window. The answer is the smallest d with count ≥ k.")
    w2.step(f"Sorted heights: {s}. A window [left, right] with s[right] − s[left] ≤ d contains right − left pairs ending at right.", Row(s, slots=True))
    r = answer_walk(w2, 0, s[-1] - s[0], lambda d: (within(d) >= k, f"{within(d)} pairs have gap ≤ {d}"))
    w2.step(f"Smallest d with at least {k} pairs: {r}.", Vars(gap=r), result=r)

    sol(
        "kth-closest-pair",
        summary="""
            There are up to 2 × 10⁸ pairs, too many to list. But in sorted order, counting pairs with gap ≤ d takes one
            sliding-window pass, and that count grows with d. So binary-search d: the answer is the smallest d with at least
            k pairs. O(n log n + n log(max height)).
        """,
        question=[
            """
            Over all pairs i < j, the gap is |h[i] − h[j]|. Return the k-th smallest gap (duplicates counted).

            - **Pairs are by position:** equal heights give gap 0, possibly many times.
            - **n up to 2 × 10⁴** → about 2 × 10⁸ pairs. Listing and sorting them is too slow and too big.
            - **k can be up to n(n − 1)/2 ≈ 2 × 10⁸**, still inside a 32-bit `int`; pair counts are kept in 64 bits to be
              safe.
            """
        ],
        think=[
            f"""
            Take heights `{h}`, k = {k}. All gaps sorted: `{gaps}`; the {k}-th is {want}.

            Use the "binary search on the value, count how many are ≤ it" idea. For a candidate gap d: sort the heights
            (`{s}`); for each right end, the left ends within d form a window, and every left end in it makes a pair. The
            window's left edge only moves right as the right edge does, so counting is O(n).
            """,
            fig(Row(s, slots=True), Row([within(d) for d in range(0, s[-1] - s[0] + 1)], label="pairs with gap ≤ d (d = 0, 1, …)"), caption="The count grows with d; the answer is where it first reaches k."),
            """
            The smallest d with count ≥ k is always an actual gap, because the count only rises at real gap values.
            """,
        ],
        approaches=[
            approach(
                "Every pair, sorted",
                "brute",
                "O(n² log n)",
                "O(n²)",
                idea=["Compute all n(n − 1)/2 gaps, sort them, return index k − 1."],
                walk=w1,
                build=["Collect |h[i] − h[j]| for all i < j.", "Sort.", "Return element k − 1."],
                code={
                    "python": """
                        class Solution:
                            def kthPairGap(self, heights: List[int], k: int) -> int:
                                n = len(heights)
                                gaps = sorted(abs(heights[i] - heights[j]) for i in range(n) for j in range(i + 1, n))  #@all
                                return gaps[k - 1]  #@pick
                    """,
                    "java": """
                        class Solution {
                            public int kthPairGap(int[] heights, int k) {
                                int n = heights.length, t = 0;
                                int[] gaps = new int[n * (n - 1) / 2];  //@all
                                for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) gaps[t++] = Math.abs(heights[i] - heights[j]);  //@all
                                Arrays.sort(gaps);  //@all
                                return gaps[k - 1];  //@pick
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthPairGap(vector<int>& heights, int k) {
                                int n = heights.size();
                                vector<int> gaps;  //@all
                                for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) gaps.push_back(abs(heights[i] - heights[j]));  //@all
                                sort(gaps.begin(), gaps.end());  //@all
                                return gaps[k - 1];  //@pick
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@all
                            int p = *(const int*) a, q = *(const int*) b;  //@all
                            return (p > q) - (p < q);  //@all
                        }  //@all

                        int kthPairGap(int* heights, int heightsSize, int k) {
                            int n = heightsSize, t = 0;
                            int* gaps = malloc((size_t) n * (n - 1) / 2 * sizeof(int) + 1);  //@all
                            for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) gaps[t++] = abs(heights[i] - heights[j]);  //@all
                            qsort(gaps, t, sizeof(int), cmpInt);  //@all
                            int answer = gaps[k - 1];  //@pick
                            free(gaps);  //@pick
                            return answer;  //@pick
                        }
                    """,
                },
                lines=[("all", "Every pair's gap, sorted."), ("pick", "The k-th smallest.")],
                complexity=["**Time O(n² log n).** **Space O(n²)**: 2 × 10⁸ numbers at the limit."],
                limits=["Materialises every pair. Counting pairs below a threshold is cheap on sorted data, which enables binary search on the gap value."],
                slow=True,
            ),
            approach(
                "Binary search on the gap, sliding-window count",
                "best",
                "O(n log n + n log W)",
                "O(n)",
                idea=["Sort. Search d in `[0, max − min]`. `count(d)`: for each right, move left while `s[right] − s[left] > d`, add `right − left`. If `count(mid) ≥ k`, `hi = mid`; else `lo = mid + 1`."],
                walk=w2,
                build=["Sort a copy.", "Write the sliding-window count of pairs with gap ≤ d.", "Lower-bound search for the smallest d with count ≥ k."],
                code={
                    "python": """
                        class Solution:
                            def kthPairGap(self, heights: List[int], k: int) -> int:
                                s = sorted(heights)  #@sort
                                n = len(s)
                                def pairs_within(d):  #@count
                                    total = left = 0  #@count
                                    for right in range(n):  #@count
                                        while s[right] - s[left] > d:  #@count
                                            left += 1  #@count
                                        total += right - left  #@count
                                    return total  #@count
                                lo, hi = 0, s[-1] - s[0]  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if pairs_within(mid) >= k:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthPairGap(int[] heights, int k) {
                                int[] s = heights.clone();  //@sort
                                Arrays.sort(s);  //@sort
                                int lo = 0, hi = s[s.length - 1] - s[0];  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (pairsWithin(s, mid) >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }

                            private long pairsWithin(int[] s, int d) {  //@count
                                long total = 0;  //@count
                                for (int right = 0, left = 0; right < s.length; right++) {  //@count
                                    while (s[right] - s[left] > d) left++;  //@count
                                    total += right - left;  //@count
                                }  //@count
                                return total;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthPairGap(vector<int>& heights, int k) {
                                vector<int> s = heights;  //@sort
                                sort(s.begin(), s.end());  //@sort
                                int n = s.size();
                                auto pairsWithin = [&](int d) {  //@count
                                    long long total = 0;  //@count
                                    for (int right = 0, left = 0; right < n; right++) {  //@count
                                        while (s[right] - s[left] > d) left++;  //@count
                                        total += right - left;  //@count
                                    }  //@count
                                    return total;  //@count
                                };  //@count
                                int lo = 0, hi = s[n - 1] - s[0];  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (pairsWithin(mid) >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@sort
                            int p = *(const int*) a, q = *(const int*) b;  //@sort
                            return (p > q) - (p < q);  //@sort
                        }  //@sort

                        static long long pairsWithin(const int* s, int n, int d) {  //@count
                            long long total = 0;  //@count
                            for (int right = 0, left = 0; right < n; right++) {  //@count
                                while (s[right] - s[left] > d) left++;  //@count
                                total += right - left;  //@count
                            }  //@count
                            return total;  //@count
                        }  //@count

                        int kthPairGap(int* heights, int heightsSize, int k) {
                            int n = heightsSize;
                            int* s = malloc(n * sizeof(int));  //@sort
                            memcpy(s, heights, n * sizeof(int));  //@sort
                            qsort(s, n, sizeof(int), cmpInt);  //@sort
                            int lo = 0, hi = s[n - 1] - s[0];  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (pairsWithin(s, n, mid) >= k) hi = mid;  //@move
                                else lo = mid + 1;  //@move
                            }
                            free(s);  //@ret
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Sorted heights: pairs with a small gap become nearby positions."), ("count", "Pairs with gap ≤ d: for each right end, shrink the window from the left until it fits; every left index inside pairs with right. `left` never moves back, so this is O(n)."), ("range", "Gaps run from 0 to max − min."), ("loop", "Halve the gap range (≈ 20 steps for heights ≤ 10⁶)."), ("move", "At least k pairs within mid → the k-th gap is ≤ mid."), ("ret", "The smallest such d, which is an actual gap.")],
                complexity=["**Time O(n log n + n log W)** for W = max − min. **Space O(n)** for the sorted copy."],
            ),
        ],
        takeaways=[
            """
            - k-th smallest among too many derived values (pair gaps) → binary-search the value and count with an O(n)
              pass.
            - On sorted data, "pairs with difference ≤ d" is a sliding-window count.
            """
        ],
    )


@problem
def nth_beat():
    n, a, b = 8, 4, 6
    beats = sorted(set([a * i for i in range(1, 20)] + [b * i for i in range(1, 20)]))
    want = beats[n - 1]
    l = a * b // math.gcd(a, b)

    def count(x):
        return x // a + x // b - x // l

    w1 = Steps("Merge the two drummers' hit times in increasing order, counting a shared hit once, until the n-th beat.")
    i = j = 1
    cnt = 0
    while True:
        na, nb = a * i, b * j
        v = min(na, nb)
        if na == v:
            i += 1
        if nb == v:
            j += 1
        cnt += 1
        w1.step(f"Beat #{cnt}: {v}" + (" (both hit: counted once)" if na == nb else "") + ".", Vars(beat=cnt, time=v))
        if cnt == n:
            break
    w1.steps[-1]["result"] = str(want)

    w2 = Steps(f"Binary-search the time x: beats up to x = x/a + x/b − x/lcm (lcm({a}, {b}) = {l}). Find the smallest x with at least n beats.")
    r = answer_walk(w2, 1, n * min(a, b), lambda x: (count(x) >= n, f"{x // a} + {x // b} − {x // l} = {count(x)} beats"))
    w2.step(f"The {n}-th beat is at {r}.", Vars(time=r), result=r)

    sol(
        "nth-beat",
        summary="""
            Count beats up to time x with inclusion–exclusion: x/a + x/b − x/lcm(a, b) (shared hits are subtracted once).
            The count grows with x, so binary-search the smallest x with at least n beats. The answer is at most n · min(a, b),
            which bounds the search. O(log(n · min(a, b))).
        """,
        question=[
            """
            Beats are the positive multiples of a or of b (a common multiple counts once). Return the n-th beat modulo
            10⁹ + 7.

            - **Shared hits count once:** with a = 2, b = 4, every multiple of 4 is also a multiple of 2.
            - **n up to 10⁹** and a, b up to 4 × 10⁴: the answer reaches 4 × 10¹³, so search in 64 bits and take the modulo
              only at the end.
            - **The modulo doesn't affect the search**; it's just how the (exact) answer is reported.
            """
        ],
        think=[
            f"""
            Take a = {a}, b = {b}, n = {n}. Beats: {beats[:n + 2]}… (12 and 24 are shared). The {n}-th is {want}.

            How many beats are ≤ x? Multiples of a: ⌊x/a⌋. Multiples of b: ⌊x/b⌋. Shared ones (multiples of lcm(a, b) =
            {l}) were counted twice, so subtract ⌊x/{l}⌋. This count never decreases as x grows, and the n-th beat is the
            first x where it reaches n.
            """,
            fig(Row(beats[:n + 2], st={n - 1: "answer"}, label="beats"), caption=f"Multiples of {a} or {b}, each counted once."),
            """
            Range: the first drummer alone produces n beats by `n × a`, so the answer is at most `n × min(a, b)`.
            lcm(a, b) = a × b / gcd(a, b) (up to 1.6 × 10⁹, so compute it in 64 bits).
            """,
        ],
        approaches=[
            approach(
                "Merge the two beat sequences",
                "brute",
                "O(n)",
                "O(1)",
                idea=["Walk both sequences of multiples like merging two sorted lists, taking the smaller next hit each time (advancing both when equal), until n beats are counted."],
                walk=w1,
                build=["`nextA = a`, `nextB = b`.", "Repeat n times: `beat = min(nextA, nextB)`; advance whichever equals it (both if equal).", "Return `beat mod 10⁹ + 7`."],
                code={
                    "python": """
                        class Solution:
                            def nthBeat(self, n: int, a: int, b: int) -> int:
                                next_a, next_b = a, b  #@init
                                beat = 0  #@init
                                for _ in range(n):  #@merge
                                    beat = min(next_a, next_b)  #@merge
                                    if next_a == beat:  #@merge
                                        next_a += a  #@merge
                                    if next_b == beat:  #@merge
                                        next_b += b  #@merge
                                return beat % (10**9 + 7)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int nthBeat(int n, int a, int b) {
                                long nextA = a, nextB = b, beat = 0;  //@init
                                for (int t = 0; t < n; t++) {  //@merge
                                    beat = Math.min(nextA, nextB);  //@merge
                                    if (nextA == beat) nextA += a;  //@merge
                                    if (nextB == beat) nextB += b;  //@merge
                                }
                                return (int) (beat % 1_000_000_007L);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int nthBeat(int n, int a, int b) {
                                long long nextA = a, nextB = b, beat = 0;  //@init
                                for (int t = 0; t < n; t++) {  //@merge
                                    beat = min(nextA, nextB);  //@merge
                                    if (nextA == beat) nextA += a;  //@merge
                                    if (nextB == beat) nextB += b;  //@merge
                                }
                                return beat % 1000000007LL;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int nthBeat(int n, int a, int b) {
                            long long nextA = a, nextB = b, beat = 0;  //@init
                            for (int t = 0; t < n; t++) {  //@merge
                                beat = nextA < nextB ? nextA : nextB;  //@merge
                                if (nextA == beat) nextA += a;  //@merge
                                if (nextB == beat) nextB += b;  //@merge
                            }
                            return (int) (beat % 1000000007LL);  //@ret
                        }
                    """,
                },
                lines=[("init", "Each drummer's next hit time (64-bit: hits go up to 4 × 10¹³)."), ("merge", "The next beat is the earlier of the two next hits; if both drummers hit then, both advance, so the shared hit counts once."), ("ret", "Report the n-th beat modulo 10⁹ + 7.")],
                complexity=["**Time O(n):** up to 10⁹ steps. **Space O(1).**"],
                limits=["Walks every beat up to the n-th. Counting beats up to any x is O(1) with inclusion–exclusion, so the n-th beat can be binary-searched."],
                slow=True,
            ),
            approach(
                "Binary search with inclusion–exclusion",
                "best",
                "O(log(n · min(a, b)))",
                "O(1)",
                idea=["`lcm = a / gcd(a, b) × b`. Search x in `[1, n × min(a, b)]` for the first x with `x/a + x/b − x/lcm ≥ n`. Return `x mod 10⁹ + 7`."],
                walk=w2,
                build=["Compute gcd (Euclid) and lcm in 64 bits.", "`lo = 1`, `hi = n × min(a, b)`.", "Count beats ≤ mid; lower-bound search.", "Return `lo % (10⁹ + 7)`."],
                code={
                    "python": """
                        import math

                        class Solution:
                            def nthBeat(self, n: int, a: int, b: int) -> int:
                                lcm = a // math.gcd(a, b) * b  #@lcm
                                lo, hi = 1, n * min(a, b)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if mid // a + mid // b - mid // lcm >= n:  #@count
                                        hi = mid  #@count
                                    else:  #@count
                                        lo = mid + 1  #@count
                                return lo % (10**9 + 7)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int nthBeat(int n, int a, int b) {
                                long g = gcd(a, b), lcm = a / g * b;  //@lcm
                                long lo = 1, hi = (long) n * Math.min(a, b);  //@range
                                while (lo < hi) {  //@loop
                                    long mid = lo + (hi - lo) / 2;  //@loop
                                    if (mid / a + mid / b - mid / lcm >= n) hi = mid;  //@count
                                    else lo = mid + 1;  //@count
                                }
                                return (int) (lo % 1_000_000_007L);  //@ret
                            }

                            private long gcd(long x, long y) {  //@lcm
                                while (y != 0) { long t = x % y; x = y; y = t; }  //@lcm
                                return x;  //@lcm
                            }  //@lcm
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int nthBeat(int n, int a, int b) {
                                long long lcm = (long long) a / gcd(a, b) * b;  //@lcm
                                long long lo = 1, hi = (long long) n * min(a, b);  //@range
                                while (lo < hi) {  //@loop
                                    long long mid = lo + (hi - lo) / 2;  //@loop
                                    if (mid / a + mid / b - mid / lcm >= n) hi = mid;  //@count
                                    else lo = mid + 1;  //@count
                                }
                                return lo % 1000000007LL;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long gcd(long long x, long long y) {  //@lcm
                            while (y != 0) { long long t = x % y; x = y; y = t; }  //@lcm
                            return x;  //@lcm
                        }  //@lcm

                        int nthBeat(int n, int a, int b) {
                            long long lcm = a / gcd(a, b) * b;  //@lcm
                            long long lo = 1, hi = (long long) n * (a < b ? a : b);  //@range
                            while (lo < hi) {  //@loop
                                long long mid = lo + (hi - lo) / 2;  //@loop
                                if (mid / a + mid / b - mid / lcm >= n) hi = mid;  //@count
                                else lo = mid + 1;  //@count
                            }
                            return (int) (lo % 1000000007LL);  //@ret
                        }
                    """,
                },
                lines=[("lcm", "Least common multiple: shared hits happen every lcm. Divide before multiplying (a / gcd × b) to keep it small, and keep it in 64 bits.", {"cpp": "`std::gcd` (C++17, in `<numeric>`) computes the greatest common divisor."}), ("range", "The faster drummer alone reaches n beats by n × min(a, b), so the answer is at most that (64-bit)."), ("loop", "Halve the time range: about 46 steps."), ("count", "Beats up to mid by inclusion–exclusion. Enough → the n-th beat is ≤ mid."), ("ret", "The exact n-th beat, reported modulo 10⁹ + 7.")],
                complexity=["**Time O(log(n · min(a, b))).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "n-th element of a merged set of arithmetic sequences" → binary search on the value with an
              inclusion–exclusion count.
            - Search with exact 64-bit values; apply a requested modulo only to the final answer.
            """
        ],
    )
