"""Sliding Window: windows of a fixed length k, updated in O(1) per step."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def slide_steps(w, values, k, score, label="value", better=lambda a, b: a > b, shown=None, extra=None):
    """One step per window: highlight it, show its score and the best so far."""
    n = len(values)
    best = None
    for i in range(n - k + 1):
        cur = score(i)
        if best is None or better(cur, best):
            best = cur
        how = "first window, summed directly" if i == 0 else f"add {values[i + k - 1]}, drop {values[i - 1]}"
        w.step(f"Window {i}..{i + k - 1} ({how}): {cur}.", Row(shown or values, st={x: "active" for x in range(i, i + k)}, label=label), Vars(window=cur, best=best, **(extra(i) if extra else {})))
    return best


@problem
def best_sales_week():
    sales, k = [3, -2, 5, -1, 4, -6, 2, 3], 3
    want = max(sum(sales[i:i + k]) for i in range(len(sales) - k + 1))

    w1 = Steps("Add up every window of k days from scratch.")
    for i in range(len(sales) - k + 1):
        w1.step(f"Days {i}..{i + k - 1}: {' + '.join(map(str, sales[i:i + k]))} = {sum(sales[i:i + k])}.", Row(sales, st={x: "active" for x in range(i, i + k)}))
    w1.step(f"Largest: {want}.", result=want)

    w2 = Steps("Sum the first window once; every later window is the previous total plus the day entering minus the day leaving.")
    got = slide_steps(w2, sales, k, lambda i: sum(sales[i:i + k]), "sales")
    w2.step(f"Largest total: {got}.", result=got)

    sol(
        "best-sales-week",
        summary="""
            Neighbouring windows share all but two days. Keep a running total: start with the first `k` days, then for each
            step add the day entering and subtract the day leaving, tracking the maximum. O(n) time, O(1) space; the total
            fits easily in 64 bits.
        """,
        question=[
            """
            Return the largest total of any `k` consecutive values in `sales` (values can be negative).

            - **n up to 10⁵**, `k` up to `n`.
            - The answer is returned as a 64-bit integer.
            """
        ],
        think=[
            f"""
            `sales = {sales}`, `k = {k}` → **{want}**.

            Summing each window separately repeats almost all the work: moving the window right by one changes exactly two
            days. So the next total is the current one plus the new day minus the old day, an O(1) update.

            Negative values don't matter here (unlike variable-size windows), because the length is fixed: every window is
            considered, and only the best is kept.
            """,
            fig(Row(sales, label="sales")),
        ],
        approaches=[
            approach(
                "Sum every window",
                "brute",
                "O(n · k)",
                "O(1)",
                idea=["For each start `i`, add `sales[i..i+k)` and keep the maximum."],
                walk=w1,
                build=["Loop over starts.", "Inner sum.", "Keep the best."],
                code={
                    "python": """
                        class Solution:
                            def bestWeek(self, sales: List[int], k: int) -> int:
                                best = None  #@init
                                for i in range(len(sales) - k + 1):  #@starts
                                    total = sum(sales[i:i + k])  #@sum
                                    if best is None or total > best:  #@best
                                        best = total  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestWeek(int[] sales, int k) {
                                long best = Long.MIN_VALUE;  //@init
                                for (int i = 0; i + k <= sales.length; i++) {  //@starts
                                    long total = 0;  //@sum
                                    for (int j = i; j < i + k; j++) total += sales[j];  //@sum
                                    best = Math.max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestWeek(vector<int>& sales, int k) {
                                long long best = LLONG_MIN;  //@init
                                for (int i = 0; i + k <= (int) sales.size(); i++) {  //@starts
                                    long long total = 0;  //@sum
                                    for (int j = i; j < i + k; j++) total += sales[j];  //@sum
                                    best = max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestWeek(int* sales, int salesSize, int k) {
                            long long best = LLONG_MIN;  //@init
                            for (int i = 0; i + k <= salesSize; i++) {  //@starts
                                long long total = 0;  //@sum
                                for (int j = i; j < i + k; j++) total += sales[j];  //@sum
                                if (total > best) best = total;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "No window seen yet (totals can be negative, so don't start at 0)."), ("starts", "Every window start."), ("sum", "Add the window's `k` days."), ("best", "Keep the largest."), ("ret", "Best total.")],
                complexity=["**Time O(n · k):** up to 2.5 × 10⁹ additions when `k = n/2`. **Space O(1).**"],
                limits=["Consecutive windows share `k − 1` days, which this re-adds every time."],
                slow=True,
            ),
            approach(
                "Running total",
                "best",
                "O(n)",
                "O(1)",
                idea=["`total = sum(sales[0..k))`. For `i = k..n−1`: `total += sales[i] − sales[i−k]`; keep the maximum."],
                walk=w2,
                build=["First window.", "Slide: add the new day, drop the old one.", "Track the maximum."],
                code={
                    "python": """
                        class Solution:
                            def bestWeek(self, sales: List[int], k: int) -> int:
                                total = sum(sales[:k])  #@first
                                best = total  #@first
                                for i in range(k, len(sales)):  #@slide
                                    total += sales[i] - sales[i - k]  #@slide
                                    best = max(best, total)  #@best
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long bestWeek(int[] sales, int k) {
                                long total = 0;  //@first
                                for (int i = 0; i < k; i++) total += sales[i];  //@first
                                long best = total;  //@first
                                for (int i = k; i < sales.length; i++) {  //@slide
                                    total += sales[i] - sales[i - k];  //@slide
                                    best = Math.max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long bestWeek(vector<int>& sales, int k) {
                                long long total = 0;  //@first
                                for (int i = 0; i < k; i++) total += sales[i];  //@first
                                long long best = total;  //@first
                                for (int i = k; i < (int) sales.size(); i++) {  //@slide
                                    total += sales[i] - sales[i - k];  //@slide
                                    best = max(best, total);  //@best
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long bestWeek(int* sales, int salesSize, int k) {
                            long long total = 0;  //@first
                            for (int i = 0; i < k; i++) total += sales[i];  //@first
                            long long best = total;  //@first
                            for (int i = k; i < salesSize; i++) {  //@slide
                                total += sales[i] - sales[i - k];  //@slide
                                if (total > best) best = total;  //@best
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("first", "The first window is summed directly and is the best so far."), ("slide", "Day `i` enters, day `i − k` leaves."), ("best", "Compare each new window."), ("ret", "Best total.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Fixed-size window:** compute the first window, then update by `+ entering − leaving`.
            - Start the best at the first window (not 0) when values can be negative.
            - Any windowed quantity that can be updated in O(1) fits this pattern (sums, counts, matches).
            """
        ],
    )


@problem
def calm_shift():
    customers, moody, minutes = [2, 0, 4, 1, 3, 5, 1, 2], [0, 1, 1, 0, 1, 1, 0, 1], 2
    n = len(customers)
    base = sum(c for c, m in zip(customers, moody) if not m)
    lost = [c * m for c, m in zip(customers, moody)]
    gain = max(sum(lost[i:i + minutes]) for i in range(n - minutes + 1))
    want = base + gain

    w1 = Steps("For every placement of the calm stretch, count the happy customers over the whole day.")
    for i in range(n - minutes + 1):
        happy = sum(c for j, (c, m) in enumerate(zip(customers, moody)) if not m or i <= j < i + minutes)
        w1.step(f"Calm during {i}..{i + minutes - 1}: {happy} happy.", Row(customers, st={x: "active" for x in range(i, i + minutes)}, label="customers"), Row(moody, label="moody"))
    w1.step(f"Best: {want}.", result=want)

    w2 = Steps(f"Customers in non-moody minutes are happy no matter what: {base}. The calm stretch only rescues moody minutes, so slide a window over the rescued counts customers[i]·moody[i].")
    got = slide_steps(w2, lost, minutes, lambda i: sum(lost[i:i + minutes]), "rescuable")
    w2.step(f"{base} always happy + {got} rescued = {base + got}.", result=base + got)

    sol(
        "calm-shift",
        summary="""
            Split the answer in two. Customers served in non-moody minutes are happy regardless. The calm stretch adds the
            customers of moody minutes inside it, so slide a window of length `minutes` over `customers[i] · moody[i]` and
            take the largest window total. Answer: the fixed part plus the best window. O(n).
        """,
        question=[
            """
            Customers served in a minute with `moody[i] = 1` leave unhappy, unless that minute is inside the owner's single
            calm stretch of `minutes` consecutive minutes. Return the most customers that can leave happy.

            - **n up to 10⁵.**
            """
        ],
        think=[
            f"""
            `customers = {customers}`, `moody = {moody}`, `minutes = {minutes}` → **{want}**.

            Whatever we choose, the {base} customers of non-moody minutes stay happy. The choice only affects the moody
            minutes, and it rescues exactly those inside the stretch. So the question becomes: which window of length
            `{minutes}` holds the most customers from moody minutes? That's a fixed-size window over
            `{lost}`.
            """,
            fig(Row(customers, label="customers"), Row(moody, label="moody"), Row(lost, label="rescuable")),
        ],
        approaches=[
            approach(
                "Try every stretch, recount the day",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start `i`, count happy customers across all minutes: non-moody, or inside `[i, i + minutes)`."],
                walk=w1,
                build=["Every placement.", "Full recount.", "Keep the best."],
                code={
                    "python": """
                        class Solution:
                            def mostServed(self, customers: List[int], moody: List[int], minutes: int) -> int:
                                n, best = len(customers), 0  #@init
                                for i in range(n - minutes + 1):  #@starts
                                    happy = sum(customers[j] for j in range(n) if not moody[j] or i <= j < i + minutes)  #@count
                                    best = max(best, happy)  #@count
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mostServed(int[] customers, int[] moody, int minutes) {
                                int n = customers.length, best = 0;  //@init
                                for (int i = 0; i + minutes <= n; i++) {  //@starts
                                    int happy = 0;  //@count
                                    for (int j = 0; j < n; j++) if (moody[j] == 0 || (j >= i && j < i + minutes)) happy += customers[j];  //@count
                                    best = Math.max(best, happy);  //@count
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mostServed(vector<int>& customers, vector<int>& moody, int minutes) {
                                int n = customers.size(), best = 0;  //@init
                                for (int i = 0; i + minutes <= n; i++) {  //@starts
                                    int happy = 0;  //@count
                                    for (int j = 0; j < n; j++) if (moody[j] == 0 || (j >= i && j < i + minutes)) happy += customers[j];  //@count
                                    best = max(best, happy);  //@count
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mostServed(int* customers, int customersSize, int* moody, int moodySize, int minutes) {
                            int n = customersSize, best = 0;  //@init
                            (void) moodySize;  //@init
                            for (int i = 0; i + minutes <= n; i++) {  //@starts
                                int happy = 0;  //@count
                                for (int j = 0; j < n; j++) if (moody[j] == 0 || (j >= i && j < i + minutes)) happy += customers[j];  //@count
                                if (happy > best) best = happy;  //@count
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Best so far."), ("starts", "Every place the calm stretch can go."), ("count", "Recount the whole day for this placement."), ("ret", "The best placement's count.")],
                complexity=["**Time O(n²):** 10¹⁰ steps at the limit. **Space O(1).**"],
                limits=["The non-moody part is the same for every placement, and neighbouring placements differ by two minutes."],
                slow=True,
            ),
            approach(
                "Fixed part + best sliding window of rescues",
                "best",
                "O(n)",
                "O(1)",
                idea=["`base` = customers in non-moody minutes. Slide a window of length `minutes` over `customers[i] · moody[i]`, tracking the largest sum `gain`. Return `base + gain`."],
                walk=w2,
                build=["Always-happy total.", "First window of rescues.", "Slide and track the max."],
                code={
                    "python": """
                        class Solution:
                            def mostServed(self, customers: List[int], moody: List[int], minutes: int) -> int:
                                base = sum(c for c, m in zip(customers, moody) if m == 0)  #@base
                                gain = sum(customers[i] * moody[i] for i in range(minutes))  #@first
                                best = gain  #@first
                                for i in range(minutes, len(customers)):  #@slide
                                    gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes]  #@slide
                                    best = max(best, gain)  #@slide
                                return base + best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mostServed(int[] customers, int[] moody, int minutes) {
                                int n = customers.length, base = 0, gain = 0;  //@base
                                for (int i = 0; i < n; i++) if (moody[i] == 0) base += customers[i];  //@base
                                for (int i = 0; i < minutes; i++) gain += customers[i] * moody[i];  //@first
                                int best = gain;  //@first
                                for (int i = minutes; i < n; i++) {  //@slide
                                    gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes];  //@slide
                                    best = Math.max(best, gain);  //@slide
                                }
                                return base + best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mostServed(vector<int>& customers, vector<int>& moody, int minutes) {
                                int n = customers.size(), base = 0, gain = 0;  //@base
                                for (int i = 0; i < n; i++) if (moody[i] == 0) base += customers[i];  //@base
                                for (int i = 0; i < minutes; i++) gain += customers[i] * moody[i];  //@first
                                int best = gain;  //@first
                                for (int i = minutes; i < n; i++) {  //@slide
                                    gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes];  //@slide
                                    best = max(best, gain);  //@slide
                                }
                                return base + best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mostServed(int* customers, int customersSize, int* moody, int moodySize, int minutes) {
                            int n = customersSize, base = 0, gain = 0;  //@base
                            (void) moodySize;  //@base
                            for (int i = 0; i < n; i++) if (moody[i] == 0) base += customers[i];  //@base
                            for (int i = 0; i < minutes; i++) gain += customers[i] * moody[i];  //@first
                            int best = gain;  //@first
                            for (int i = minutes; i < n; i++) {  //@slide
                                gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes];  //@slide
                                if (gain > best) best = gain;  //@slide
                            }
                            return base + best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("base", "Customers in calm-anyway minutes; independent of the choice."),
                    ("first", "Rescued customers if the stretch starts at minute 0. `customers[i] · moody[i]` is the number rescued at minute `i`."),
                    ("slide", "Minute `i` enters the stretch, minute `i − minutes` leaves."),
                    ("ret", "Always-happy plus the best rescue (at most 10⁸, fits in an int)."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Split the answer** into a part the choice can't change and a part a window controls.
            - Turn conditions into weights (`customers · moody`) so the window is a plain sum.
            - Then it's an ordinary fixed-size window maximum.
            """
        ],
    )


@problem
def calm_stretches():
    noise, k, limit = [4, 6, 2, 3, 8, 1, 2, 5], 3, 4
    n = len(noise)
    cap = limit * k
    want = sum(1 for i in range(n - k + 1) if sum(noise[i:i + k]) <= cap)

    w1 = Steps("Average every window from scratch and compare it with the limit.")
    for i in range(n - k + 1):
        t = sum(noise[i:i + k])
        w1.step(f"{noise[i:i + k]}: average {t}/{k} = {t / k:.2f} → {'calm' if t <= cap else 'too loud'}.", Row(noise, st={x: ("found" if t <= cap else "mark") for x in range(i, i + k)}))
    w1.step(f"Calm stretches: {want}.", result=want)

    w2 = Steps(f"Average ≤ limit is the same as sum ≤ limit · k = {cap}. Slide the window sum and count the windows at or under it.")
    count, total = 0, 0
    for i in range(n - k + 1):
        total = sum(noise[i:i + k])
        count += total <= cap
        how = "first window" if i == 0 else f"+{noise[i + k - 1]} −{noise[i - 1]}"
        w2.step(f"Window {i}..{i + k - 1} ({how}): sum {total} {'≤' if total <= cap else '>'} {cap}.", Row(noise, st={x: ("found" if total <= cap else "mark") for x in range(i, i + k)}), Vars(sum=total, calm=count))
    w2.step(f"Calm stretches: {count}.", result=count)

    sol(
        "calm-stretches",
        summary="""
            Compare sums, not averages: a window's average is at most `limit` exactly when its sum is at most `limit · k`,
            which avoids division and rounding. Slide the window sum in O(1) per step and count the windows at or under
            the cap. O(n).
        """,
        question=[
            """
            Count the windows of exactly `k` consecutive values in `noise` whose average is at most `limit`.

            - **n up to 10⁵.**
            - Sums reach 10⁹, so `limit · k` fits in 32 bits, but only just.
            """
        ],
        think=[
            f"""
            `noise = {noise}`, `k = {k}`, `limit = {limit}` → **{want}**.

            Every window has the same length, so "average ≤ limit" is "sum ≤ limit · k = {cap}". Integers only, no
            floating point. Then it's a fixed-size window with a running sum.
            """,
            fig(Row(noise, label="noise")),
        ],
        approaches=[
            approach(
                "Average every window",
                "brute",
                "O(n · k)",
                "O(1)",
                idea=["For each start, sum the window and test `sum ≤ limit · k`."],
                walk=w1,
                build=["Loop over starts.", "Sum and compare."],
                code={
                    "python": """
                        class Solution:
                            def countCalm(self, noise: List[int], k: int, limit: int) -> int:
                                count = 0  #@init
                                for i in range(len(noise) - k + 1):  #@starts
                                    if sum(noise[i:i + k]) <= limit * k:  #@test
                                        count += 1  #@test
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countCalm(int[] noise, int k, int limit) {
                                int count = 0;  //@init
                                for (int i = 0; i + k <= noise.length; i++) {  //@starts
                                    long total = 0;  //@test
                                    for (int j = i; j < i + k; j++) total += noise[j];  //@test
                                    if (total <= (long) limit * k) count++;  //@test
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countCalm(vector<int>& noise, int k, int limit) {
                                int count = 0;  //@init
                                for (int i = 0; i + k <= (int) noise.size(); i++) {  //@starts
                                    long long total = 0;  //@test
                                    for (int j = i; j < i + k; j++) total += noise[j];  //@test
                                    if (total <= (long long) limit * k) count++;  //@test
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countCalm(int* noise, int noiseSize, int k, int limit) {
                            int count = 0;  //@init
                            for (int i = 0; i + k <= noiseSize; i++) {  //@starts
                                long long total = 0;  //@test
                                for (int j = i; j < i + k; j++) total += noise[j];  //@test
                                if (total <= (long long) limit * k) count++;  //@test
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("starts", "Every window."), ("test", "Sum it and compare with `limit · k` (64-bit to be safe)."), ("ret", "Calm windows.")],
                complexity=["**Time O(n · k).** **Space O(1).**"],
                limits=["Re-adds `k − 1` shared values for every window."],
                slow=True,
            ),
            approach(
                "Running sum against limit · k",
                "best",
                "O(n)",
                "O(1)",
                idea=["`cap = limit · k`. Sum the first window; then `total += noise[i] − noise[i−k]`. Count windows with `total ≤ cap`."],
                walk=w2,
                build=["Cap in integer form.", "First window.", "Slide and count."],
                code={
                    "python": """
                        class Solution:
                            def countCalm(self, noise: List[int], k: int, limit: int) -> int:
                                cap = limit * k  #@cap
                                total = sum(noise[:k])  #@first
                                count = 1 if total <= cap else 0  #@first
                                for i in range(k, len(noise)):  #@slide
                                    total += noise[i] - noise[i - k]  #@slide
                                    if total <= cap:  #@slide
                                        count += 1  #@slide
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countCalm(int[] noise, int k, int limit) {
                                long cap = (long) limit * k, total = 0;  //@cap
                                for (int i = 0; i < k; i++) total += noise[i];  //@first
                                int count = total <= cap ? 1 : 0;  //@first
                                for (int i = k; i < noise.length; i++) {  //@slide
                                    total += noise[i] - noise[i - k];  //@slide
                                    if (total <= cap) count++;  //@slide
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countCalm(vector<int>& noise, int k, int limit) {
                                long long cap = (long long) limit * k, total = 0;  //@cap
                                for (int i = 0; i < k; i++) total += noise[i];  //@first
                                int count = total <= cap ? 1 : 0;  //@first
                                for (int i = k; i < (int) noise.size(); i++) {  //@slide
                                    total += noise[i] - noise[i - k];  //@slide
                                    if (total <= cap) count++;  //@slide
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countCalm(int* noise, int noiseSize, int k, int limit) {
                            long long cap = (long long) limit * k, total = 0;  //@cap
                            for (int i = 0; i < k; i++) total += noise[i];  //@first
                            int count = total <= cap ? 1 : 0;  //@first
                            for (int i = k; i < noiseSize; i++) {  //@slide
                                total += noise[i] - noise[i - k];  //@slide
                                if (total <= cap) count++;  //@slide
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("cap", "Multiply instead of dividing: exact, with no rounding."), ("first", "The first window's sum and verdict."), ("slide", "Enter `noise[i]`, leave `noise[i − k]`, then test."), ("ret", "Calm windows.")],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Average ≤ x over a fixed length ⇔ sum ≤ x · k:** stay in integers.
            - The running-sum window counts as easily as it maximises.
            - Watch for overflow in `x · k`; use 64-bit when in doubt.
            """
        ],
    )


@problem
def seat_the_team():
    seats = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
    n, t = len(seats), sum(seats)
    best_in, best_start = -1, 0
    for i in range(n):
        inside = sum(seats[(i + j) % n] for j in range(t))
        if inside > best_in:
            best_in, best_start = inside, i
    want = t - best_in

    w1 = Steps(f"There are {t} team members, so the final group fills some arc of {t} seats. Try each arc and count the guests in it.")
    for i in range(n):
        arc = [(i + j) % n for j in range(t)]
        guests = sum(1 for x in arc if seats[x] == 0)
        w1.step(f"Arc starting at seat {i}: {guests} guest(s) to swap out.", Row(seats, st={x: ("mark" if seats[x] == 0 else "found") for x in arc}))
    w1.step(f"Fewest guests in any arc: {want}.", result=want)

    w2 = Steps(f"Slide a window of {t} seats around the circle (index modulo n), keeping the count of members inside.")
    inside = sum(seats[:t])
    best = inside
    w2.step(f"Seats 0..{t - 1}: {inside} members.", Row(seats, st={x: "active" for x in range(t)}), Vars(inside=inside, best=best))
    for i in range(t, n + t - 1):
        inside += seats[i % n] - seats[(i - t) % n]
        best = max(best, inside)
        arc = [(i - t + 1 + j) % n for j in range(t)]
        if i - t + 1 in (1, 2, 3, best_start, n - 1):
            w2.step(f"Window starting at seat {(i - t + 1) % n}: add seat {i % n}, drop seat {(i - t) % n} → {inside} members.", Row(seats, st={x: "active" for x in arc}), Vars(inside=inside, best=best))
    w2.step(f"At most {best} members already sit together, so {t} − {best} = {t - best} swaps.", result=t - best)

    sol(
        "seat-the-team",
        summary="""
            With `t` team members, the final group occupies some arc of exactly `t` seats. Each swap can move one member
            from outside into a guest's seat inside, so an arc needs as many swaps as it has guests. Slide a window of `t`
            seats around the circle (indices modulo `n`) to find the arc with the most members; the answer is `t` minus
            that. O(n).
        """,
        question=[
            """
            Seats form a circle; `1` is a team member, `0` a guest. Any two people can swap seats. Return the fewest swaps to
            make all members sit together.

            - **n up to 10⁵.**
            - The first and last seats are neighbours.
            """
        ],
        think=[
            f"""
            `seats = {seats}` → **{want}** swap(s).

            The team has {t} members, so the target is a block of {t} consecutive seats (around the circle). Inside that
            block, every guest has to leave and a member from outside has to come in: one swap fixes exactly one such
            pair, and nothing does better. So the cost of a block is its number of guests, and we want the block with the
            fewest guests, i.e. the most members.

            Going around the circle is handled by indexing `i % n`, so the window can wrap past the end.
            """,
            fig(Row(seats, label="seats")),
        ],
        approaches=[
            approach(
                "Count guests in every arc",
                "brute",
                "O(n · t)",
                "O(1)",
                idea=["For each start `i`, count members in seats `i, i+1, …, i+t−1` (mod n). Answer: `t − max`."],
                walk=w1,
                build=["Count members.", "Every arc start.", "Recount each arc."],
                code={
                    "python": """
                        class Solution:
                            def fewestSwaps(self, seats: List[int]) -> int:
                                n, t = len(seats), sum(seats)  #@init
                                best = 0  #@init
                                for i in range(n):  #@arcs
                                    inside = sum(seats[(i + j) % n] for j in range(t))  #@count
                                    best = max(best, inside)  #@count
                                return t - best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int fewestSwaps(int[] seats) {
                                int n = seats.length, t = 0, best = 0;  //@init
                                for (int x : seats) t += x;  //@init
                                for (int i = 0; i < n; i++) {  //@arcs
                                    int inside = 0;  //@count
                                    for (int j = 0; j < t; j++) inside += seats[(i + j) % n];  //@count
                                    best = Math.max(best, inside);  //@count
                                }
                                return t - best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int fewestSwaps(vector<int>& seats) {
                                int n = seats.size(), t = 0, best = 0;  //@init
                                for (int x : seats) t += x;  //@init
                                for (int i = 0; i < n; i++) {  //@arcs
                                    int inside = 0;  //@count
                                    for (int j = 0; j < t; j++) inside += seats[(i + j) % n];  //@count
                                    best = max(best, inside);  //@count
                                }
                                return t - best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int fewestSwaps(int* seats, int seatsSize) {
                            int n = seatsSize, t = 0, best = 0;  //@init
                            for (int i = 0; i < n; i++) t += seats[i];  //@init
                            for (int i = 0; i < n; i++) {  //@arcs
                                int inside = 0;  //@count
                                for (int j = 0; j < t; j++) inside += seats[(i + j) % n];  //@count
                                if (inside > best) best = inside;  //@count
                            }
                            return t - best;  //@ret
                        }
                    """,
                },
                lines=[("init", "`t` = team size = the arc length."), ("arcs", "Every arc start around the circle."), ("count", "Members already inside this arc."), ("ret", "Guests in the best arc = swaps needed. No members gives 0.")],
                complexity=["**Time O(n · t).** **Space O(1).**"],
                limits=["Neighbouring arcs share `t − 1` seats; recounting them is wasted work."],
                slow=True,
            ),
            approach(
                "Circular sliding window",
                "best",
                "O(n)",
                "O(1)",
                idea=["Count members in seats `0..t−1`. For `i = t .. n+t−2`: add `seats[i % n]`, drop `seats[(i − t) % n]`; keep the max. Answer `t − max`."],
                walk=w2,
                build=["Team size and first window.", "Slide around the circle with `% n`.", "Answer from the fullest arc."],
                code={
                    "python": """
                        class Solution:
                            def fewestSwaps(self, seats: List[int]) -> int:
                                n, t = len(seats), sum(seats)  #@init
                                if t == 0:  #@init
                                    return 0  #@init
                                inside = sum(seats[:t])  #@first
                                best = inside  #@first
                                for i in range(t, n + t - 1):  #@slide
                                    inside += seats[i % n] - seats[(i - t) % n]  #@slide
                                    best = max(best, inside)  #@slide
                                return t - best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int fewestSwaps(int[] seats) {
                                int n = seats.length, t = 0;  //@init
                                for (int x : seats) t += x;  //@init
                                if (t == 0) return 0;  //@init
                                int inside = 0;  //@first
                                for (int i = 0; i < t; i++) inside += seats[i];  //@first
                                int best = inside;  //@first
                                for (int i = t; i < n + t - 1; i++) {  //@slide
                                    inside += seats[i % n] - seats[(i - t) % n];  //@slide
                                    best = Math.max(best, inside);  //@slide
                                }
                                return t - best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int fewestSwaps(vector<int>& seats) {
                                int n = seats.size(), t = 0;  //@init
                                for (int x : seats) t += x;  //@init
                                if (t == 0) return 0;  //@init
                                int inside = 0;  //@first
                                for (int i = 0; i < t; i++) inside += seats[i];  //@first
                                int best = inside;  //@first
                                for (int i = t; i < n + t - 1; i++) {  //@slide
                                    inside += seats[i % n] - seats[(i - t) % n];  //@slide
                                    best = max(best, inside);  //@slide
                                }
                                return t - best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int fewestSwaps(int* seats, int seatsSize) {
                            int n = seatsSize, t = 0;  //@init
                            for (int i = 0; i < n; i++) t += seats[i];  //@init
                            if (t == 0) return 0;  //@init
                            int inside = 0;  //@first
                            for (int i = 0; i < t; i++) inside += seats[i];  //@first
                            int best = inside;  //@first
                            for (int i = t; i < n + t - 1; i++) {  //@slide
                                inside += seats[i % n] - seats[(i - t) % n];  //@slide
                                if (inside > best) best = inside;  //@slide
                            }
                            return t - best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Team size `t`; with nobody to group, no swaps."),
                    ("first", "Members in the arc of seats `0..t−1`."),
                    ("slide", "Move the arc one seat clockwise: seat `i % n` enters, seat `(i − t) % n` leaves. The loop covers all `n` starting seats."),
                    ("ret", "Every guest in the best arc costs one swap."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Grouping k items** = choose a window of size k; its cost is what doesn't belong inside it.
            - **Circular arrays:** let the index run past `n` and use `i % n` (or append the array to itself).
            - A swap fixes one misplaced pair, so the cost is the number of outsiders in the window.
            """
        ],
    )


@problem
def vowel_rich_window():
    s, k = "rhythmaeiouxqueue", 5
    vowel = [1 if c in "aeiou" else 0 for c in s]
    want = max(sum(vowel[i:i + k]) for i in range(len(s) - k + 1))

    w1 = Steps("Count the vowels of every window from scratch.")
    for i in range(len(s) - k + 1):
        w1.step(f"'{s[i:i + k]}': {sum(vowel[i:i + k])} vowels.", Row(list(s), st={x: ("found" if vowel[x] else "active") for x in range(i, i + k)}))
    w1.step(f"Most: {want}.", result=want)

    w2 = Steps("Keep the vowel count of the current window; each step adds 1 if the entering letter is a vowel and subtracts 1 if the leaving one was.")
    got = slide_steps(w2, vowel, k, lambda i: sum(vowel[i:i + k]), "vowel?", shown=list(s))
    w2.step(f"Most vowels in a window: {got}.", result=got)

    sol(
        "vowel-rich-window",
        summary="""
            Treat each letter as 1 (vowel) or 0, and slide a window of length `k` keeping its count: add the entering letter,
            subtract the leaving one, track the maximum. You can also stop early once the count reaches `k`. O(n).
        """,
        question=[
            """
            Return the most vowels (`a e i o u`) in any substring of exactly `k` letters.

            - **n up to 10⁵.**
            """
        ],
        think=[
            f"""
            `"{s}"`, `k = {k}` → **{want}**.

            A vowel count is a sum of 0/1 flags, so this is the fixed-window sum again: moving right changes the count by
            at most one in each direction.
            """,
            fig(Row(list(s), label="s"), Row(vowel, label="vowel?")),
        ],
        approaches=[
            approach(
                "Count every window",
                "brute",
                "O(n · k)",
                "O(1)",
                idea=["For each start, count the vowels in the next `k` letters."],
                walk=w1,
                build=["Loop over starts.", "Count vowels.", "Keep the best."],
                code={
                    "python": """
                        class Solution:
                            def mostVowels(self, s: str, k: int) -> int:
                                best = 0  #@init
                                for i in range(len(s) - k + 1):  #@starts
                                    count = sum(1 for c in s[i:i + k] if c in "aeiou")  #@count
                                    best = max(best, count)  #@count
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int mostVowels(String s, int k) {
                                int best = 0;  //@init
                                for (int i = 0; i + k <= s.length(); i++) {  //@starts
                                    int count = 0;  //@count
                                    for (int j = i; j < i + k; j++) if ("aeiou".indexOf(s.charAt(j)) >= 0) count++;  //@count
                                    best = Math.max(best, count);  //@count
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int mostVowels(string& s, int k) {
                                int best = 0;  //@init
                                for (int i = 0; i + k <= (int) s.size(); i++) {  //@starts
                                    int count = 0;  //@count
                                    for (int j = i; j < i + k; j++) if (string("aeiou").find(s[j]) != string::npos) count++;  //@count
                                    best = max(best, count);  //@count
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int mostVowels(char* s, int k) {
                            int n = strlen(s), best = 0;  //@init
                            for (int i = 0; i + k <= n; i++) {  //@starts
                                int count = 0;  //@count
                                for (int j = i; j < i + k; j++) if (strchr("aeiou", s[j])) count++;  //@count
                                if (count > best) best = count;  //@count
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Best so far."), ("starts", "Every window."), ("count", "Vowels in this window."), ("ret", "Most vowels.")],
                complexity=["**Time O(n · k).** **Space O(1).**"],
                limits=["Re-counts `k − 1` shared letters each step."],
                slow=True,
            ),
            approach(
                "Sliding vowel count",
                "best",
                "O(n)",
                "O(1)",
                idea=["Count vowels in the first `k` letters; then for each `i ≥ k`, `count += isVowel(s[i]) − isVowel(s[i−k])`; keep the max."],
                walk=w2,
                build=["Vowel test.", "First window.", "Slide and track the max."],
                code={
                    "python": """
                        class Solution:
                            def mostVowels(self, s: str, k: int) -> int:
                                vowel = [c in "aeiou" for c in s]  #@test
                                count = sum(vowel[:k])  #@first
                                best = count  #@first
                                for i in range(k, len(s)):  #@slide
                                    count += vowel[i] - vowel[i - k]  #@slide
                                    best = max(best, count)  #@slide
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int vowel(char c) {  //@test
                                return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ? 1 : 0;  //@test
                            }  //@test

                            public int mostVowels(String s, int k) {
                                int count = 0;  //@first
                                for (int i = 0; i < k; i++) count += vowel(s.charAt(i));  //@first
                                int best = count;  //@first
                                for (int i = k; i < s.length(); i++) {  //@slide
                                    count += vowel(s.charAt(i)) - vowel(s.charAt(i - k));  //@slide
                                    best = Math.max(best, count);  //@slide
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            static int vowel(char c) {  //@test
                                return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';  //@test
                            }  //@test

                        public:
                            int mostVowels(string& s, int k) {
                                int count = 0;  //@first
                                for (int i = 0; i < k; i++) count += vowel(s[i]);  //@first
                                int best = count;  //@first
                                for (int i = k; i < (int) s.size(); i++) {  //@slide
                                    count += vowel(s[i]) - vowel(s[i - k]);  //@slide
                                    best = max(best, count);  //@slide
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int vowel(char c) {  //@test
                            return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';  //@test
                        }  //@test

                        int mostVowels(char* s, int k) {
                            int n = strlen(s), count = 0;  //@first
                            for (int i = 0; i < k; i++) count += vowel(s[i]);  //@first
                            int best = count;  //@first
                            for (int i = k; i < n; i++) {  //@slide
                                count += vowel(s[i]) - vowel(s[i - k]);  //@slide
                                if (count > best) best = count;  //@slide
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("test", "1 for a vowel, 0 otherwise.", {"python": "Booleans add as 0/1 in Python."}), ("first", "Vowels in the first window."), ("slide", "The entering and leaving letters change the count by at most one each."), ("ret", "Most vowels.")],
                complexity=["**Time O(n).** **Space O(1)** (O(n) for Python's flag list, which is optional)."],
            ),
        ],
        takeaways=[
            """
            - **Counting a property in a fixed window** = sliding sum of 0/1 flags.
            - Only the two edge letters change per step.
            """
        ],
    )
