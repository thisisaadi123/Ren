"""Binary Search: k-th element."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def kth_free_number():
    taken, k = [2, 3, 4, 7, 11, 12, 15], 6
    free = [x for x in range(1, 40) if x not in taken]
    want = free[k - 1]
    missing = [t - (i + 1) for i, t in enumerate(taken)]

    w1 = Steps("Walk through the taken numbers, counting the free numbers in each gap until k is reached.")
    left, prev = k, 0
    for t in taken:
        gap = t - prev - 1
        if gap >= left:
            w1.step(f"Gap between {prev} and {t} has {gap} free number{'s' if gap != 1 else ''}; we need {left} more, so the answer is {prev} + {left} = {prev + left}.", Row(taken, st={taken.index(t): "active"}, slots=True), Vars(still_needed=left), result=prev + left)
            break
        w1.step(f"Gap between {prev} and {t}: {gap} free. Still need {left - gap}.", Row(taken, st={taken.index(t): "active"}, slots=True), Vars(still_needed=left - gap))
        left -= gap
        prev = t

    w2 = Steps("missing(i) = taken[i] − (i + 1) counts free numbers below taken[i]. Binary-search the first i with missing(i) ≥ k.")
    w2.step("missing(i) never decreases, so it can be binary-searched.", Row(taken, label="taken", slots=True), Row(missing, label="free numbers below it", slots=True))
    lo, hi = 0, len(taken)
    while lo < hi:
        mid = (lo + hi) // 2
        ok = missing[mid] >= k
        w2.step(f"lo={lo}, hi={hi}, mid={mid}: {missing[mid]} free below {taken[mid]} " + (f"≥ {k}: the answer is below {taken[mid]}, hi = {mid}." if ok else f"< {k}: the answer is above {taken[mid]}, lo = {mid + 1}."), Row(missing, st={mid: "active"}, ptr={"lo": lo, "mid": mid, "hi": hi} if hi < len(taken) else {"lo": lo, "mid": mid}, label="free below", slots=True))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    w2.step(f"lo = {lo}: exactly {lo} taken numbers lie below the answer, so the answer is k + lo = {k} + {lo} = {k + lo}.", Row(taken, st={i: "found" for i in range(lo)}, slots=True), result=k + lo)
    assert k + lo == want

    sol(
        "kth-free-number",
        summary="""
            Below `taken[i]` there are `taken[i] − (i + 1)` free numbers, a count that never decreases with i. Binary-search
            the first i where it reaches k: then exactly `i` taken numbers lie below the answer, and the answer is simply
            `k + i`. O(log n), and it never walks through the (possibly huge) free numbers one by one.
        """,
        question=[
            """
            `taken` is a strictly increasing list of positive numbers. Return the k-th smallest positive number **not** in
            it.

            - **k can be 10⁹**, far beyond the list, so counting free numbers one at a time is too slow.
            - **The answer may be before, between or after** the taken numbers: `[5]` with k = 3 gives 3; `[1, 2, 3, 4]`
              with k = 2 gives 6.
            - **The answer fits in 32 bits:** it is at most k + n ≤ 10⁹ + 10⁵.
            """
        ],
        think=[
            f"""
            Take `taken = {taken}`, k = {k}. The free numbers are {free[:8]}…, so the {k}-th is {want}.

            How many free numbers are below `taken[i]`? There are `taken[i] − 1` positive numbers below it, and i of them
            are taken (the ones before it in the list), so `taken[i] − 1 − i` are free.
            """,
            fig(Row(taken, label="taken", slots=True), Row(missing, label="free below it", slots=True), caption="The free count only grows, so it can be binary-searched."),
            f"""
            Find the first index i where at least k numbers below `taken[i]` are free. Then the answer is below `taken[i]`
            but above all earlier taken numbers, so exactly i taken numbers are smaller than it. Among the first `k + i`
            positive numbers, i are taken and k are free, which makes `k + i` the k-th free one. If no index qualifies,
            i = n and the same formula holds. Here i = {lo}, giving {k + lo}.
            """,
        ],
        approaches=[
            approach(
                "Walk the gaps",
                "better",
                "O(n)",
                "O(1)",
                idea=["Go through the taken numbers keeping `prev` (the last taken number, starting at 0). The gap before `t` holds `t − prev − 1` free numbers. If that covers the remaining count, the answer is `prev + remaining`; otherwise subtract and move on. After the list, the answer is `prev + remaining`."],
                walk=w1,
                build=["`prev = 0`, `left = k`.", "For each t: `gap = t − prev − 1`. If `gap ≥ left`, return `prev + left`. Else `left −= gap`, `prev = t`.", "Return `prev + left`."],
                code={
                    "python": """
                        class Solution:
                            def kthFree(self, taken: List[int], k: int) -> int:
                                prev, left = 0, k  #@init
                                for t in taken:  #@gaps
                                    gap = t - prev - 1  #@gaps
                                    if gap >= left:  #@inside
                                        return prev + left  #@inside
                                    left -= gap  #@skip
                                    prev = t  #@skip
                                return prev + left  #@after
                    """,
                    "java": """
                        class Solution {
                            public int kthFree(int[] taken, int k) {
                                int prev = 0, left = k;  //@init
                                for (int t : taken) {  //@gaps
                                    int gap = t - prev - 1;  //@gaps
                                    if (gap >= left) return prev + left;  //@inside
                                    left -= gap;  //@skip
                                    prev = t;  //@skip
                                }
                                return prev + left;  //@after
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthFree(vector<int>& taken, int k) {
                                int prev = 0, left = k;  //@init
                                for (int t : taken) {  //@gaps
                                    int gap = t - prev - 1;  //@gaps
                                    if (gap >= left) return prev + left;  //@inside
                                    left -= gap;  //@skip
                                    prev = t;  //@skip
                                }
                                return prev + left;  //@after
                            }
                        };
                    """,
                    "c": """
                        int kthFree(int* taken, int takenSize, int k) {
                            int prev = 0, left = k;  //@init
                            for (int i = 0; i < takenSize; i++) {  //@gaps
                                int gap = taken[i] - prev - 1;  //@gaps
                                if (gap >= left) return prev + left;  //@inside
                                left -= gap;  //@skip
                                prev = taken[i];  //@skip
                            }
                            return prev + left;  //@after
                        }
                    """,
                },
                lines=[("init", "Nothing is passed yet (as if 0 were taken), and k free numbers are still needed."), ("gaps", "Free numbers strictly between the previous taken number and this one."), ("inside", "The answer lies in this gap."), ("skip", "This gap isn't enough: use up its free numbers and move on."), ("after", "Past the last taken number every number is free, so count on from it. At most 10⁹ + 10⁵, inside `int`.")],
                complexity=["**Time O(n).** **Space O(1).**"],
                limits=["Visits every taken number, but the \"free numbers below\" count is monotonic, so the right gap can be found by binary search."],
            ),
            approach(
                "Binary search on the free count",
                "best",
                "O(log n)",
                "O(1)",
                idea=["Find the first index i with `taken[i] − (i + 1) ≥ k` (lower-bound template over `[0, n)`). Return `k + i`."],
                walk=w2,
                build=["`lo = 0`, `hi = n`.", "If `taken[mid] − (mid + 1) < k`, `lo = mid + 1`; else `hi = mid`.", "Return `lo + k`."],
                code={
                    "python": """
                        class Solution:
                            def kthFree(self, taken: List[int], k: int) -> int:
                                lo, hi = 0, len(taken)  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if taken[mid] - (mid + 1) < k:  #@test
                                        lo = mid + 1  #@test
                                    else:  #@test
                                        hi = mid  #@test
                                return lo + k  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthFree(int[] taken, int k) {
                                int lo = 0, hi = taken.length;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (taken[mid] - (mid + 1) < k) lo = mid + 1;  //@test
                                    else hi = mid;  //@test
                                }
                                return lo + k;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthFree(vector<int>& taken, int k) {
                                int lo = 0, hi = taken.size();  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    if (taken[mid] - (mid + 1) < k) lo = mid + 1;  //@test
                                    else hi = mid;  //@test
                                }
                                return lo + k;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int kthFree(int* taken, int takenSize, int k) {
                            int lo = 0, hi = takenSize;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                if (taken[mid] - (mid + 1) < k) lo = mid + 1;  //@test
                                else hi = mid;  //@test
                            }
                            return lo + k;  //@ret
                        }
                    """,
                },
                lines=[("range", "Candidate indices 0 … n (n means \"after every taken number\")."), ("loop", "Halve the candidates."), ("test", "Fewer than k free numbers below `taken[mid]` means the answer is above it; otherwise it's below it (or below an earlier one)."), ("ret", "`lo` taken numbers are smaller than the answer, so it's the (k + lo)-th positive number.")],
                complexity=["**Time O(log n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - In a sorted list of distinct positives, `a[i] − (i + 1)` counts the missing numbers below `a[i]`: a
              monotonic quantity, so binary-searchable.
            - Once you know how many taken numbers precede the answer, the answer is just `k + that count`.
            """
        ],
    )


@problem
def kth_in_times_table():
    rows, cols, k = 3, 4, 7
    vals = sorted(i * j for i in range(1, rows + 1) for j in range(1, cols + 1))
    want = vals[k - 1]
    table_grid = [[i * j for j in range(1, cols + 1)] for i in range(1, rows + 1)]

    w1 = Steps("Write out every product, sort them, and pick the k-th.")
    w1.step(f"The {rows} × {cols} table.", Grid(table_grid))
    w1.step(f"All {rows * cols} products sorted: {vals}. The {k}-th is {want}.", Row(vals, st={k - 1: "answer"}, slots=True), result=want)

    w2 = Steps("Binary-search the value v. Count how many cells are ≤ v (row i has min(v // i, cols) of them). The answer is the smallest v with count ≥ k.")
    lo, hi = 1, rows * cols
    while lo < hi:
        mid = (lo + hi) // 2
        per_row = [min(mid // i, cols) for i in range(1, rows + 1)]
        cnt = sum(per_row)
        st = {(i, j): "found" for i in range(rows) for j in range(cols) if table_grid[i][j] <= mid}
        w2.step(f"v = {mid}: rows contribute {' + '.join(map(str, per_row))} = {cnt} cells ≤ {mid} → " + (f"≥ {k}, so the answer is ≤ {mid}." if cnt >= k else f"< {k}, so the answer is > {mid}."), Grid(table_grid, st=st), Vars(lo=lo, hi=hi, count=cnt))
        if cnt >= k:
            hi = mid
        else:
            lo = mid + 1
    w2.step(f"lo = hi = {lo}: the {k}-th smallest product.", Grid(table_grid, st={(i, j): "answer" for i in range(rows) for j in range(cols) if table_grid[i][j] == lo}), result=lo)

    sol(
        "kth-in-times-table",
        summary="""
            The table can have 9 × 10⁸ cells, too many to list. But counting how many cells are ≤ v is easy: row i holds
            i, 2i, 3i, …, so it has `min(v // i, cols)` of them. That count grows with v, so binary-search the smallest v
            whose count reaches k. O(rows · log(rows · cols)).
        """,
        question=[
            """
            Cell (i, j) of a `rows × cols` table holds `i × j` (both from 1). Return the k-th smallest value, counting
            equal values in different cells separately.

            - **Duplicates count:** in a 3 × 3 table, 2 appears twice (1×2 and 2×1), 3 twice, and so on.
            - **Up to 3 × 10⁴ × 3 × 10⁴ = 9 × 10⁸ cells**, so building or sorting the table is impossible.
            - **The answer is at most rows × cols ≤ 9 × 10⁸**, inside a 32-bit `int`; counts (up to 9 × 10⁸) fit too.
            """
        ],
        think=[
            f"""
            Take a {rows} × {cols} table and k = {k}. Sorted, its products are `{vals}`; the {k}-th is {want}.
            """,
            fig(Grid(table_grid), caption="Row i is the i-times table: i, 2i, 3i, …"),
            f"""
            Instead of finding the k-th value directly, ask a yes/no question about a candidate v: **are at least k cells
            ≤ v?** For small v the answer is no, for large v it's yes, and it flips exactly at the k-th smallest value.
            (The k-th value v* has at least k cells ≤ it; any smaller v has fewer.)

            The count is cheap: row i contains i, 2i, …, cols·i, and `i·j ≤ v` means `j ≤ v // i`, capped at cols. Summing
            over rows takes O(rows). Binary search over v in [1, rows · cols] needs about 30 such counts.
            """,
        ],
        approaches=[
            approach(
                "List and sort every product",
                "brute",
                "O(rc log(rc))",
                "O(rc)",
                idea=["Generate all r · c products, sort them, return the one at index k − 1."],
                walk=w1,
                build=["Collect `i × j` for all cells.", "Sort.", "Return element k − 1."],
                code={
                    "python": """
                        class Solution:
                            def kthInTable(self, rows: int, cols: int, k: int) -> int:
                                vals = sorted(i * j for i in range(1, rows + 1) for j in range(1, cols + 1))  #@all
                                return vals[k - 1]  #@pick
                    """,
                    "java": """
                        class Solution {
                            public int kthInTable(int rows, int cols, int k) {
                                int[] vals = new int[rows * cols];  //@all
                                int t = 0;  //@all
                                for (int i = 1; i <= rows; i++) for (int j = 1; j <= cols; j++) vals[t++] = i * j;  //@all
                                Arrays.sort(vals);  //@all
                                return vals[k - 1];  //@pick
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthInTable(int rows, int cols, int k) {
                                vector<int> vals;  //@all
                                for (int i = 1; i <= rows; i++) for (int j = 1; j <= cols; j++) vals.push_back(i * j);  //@all
                                sort(vals.begin(), vals.end());  //@all
                                return vals[k - 1];  //@pick
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@all
                            int p = *(const int*) a, q = *(const int*) b;  //@all
                            return (p > q) - (p < q);  //@all
                        }  //@all

                        int kthInTable(int rows, int cols, int k) {
                            int* vals = malloc((size_t) rows * cols * sizeof(int));  //@all
                            int t = 0;  //@all
                            for (int i = 1; i <= rows; i++) for (int j = 1; j <= cols; j++) vals[t++] = i * j;  //@all
                            qsort(vals, t, sizeof(int), cmpInt);  //@all
                            int answer = vals[k - 1];  //@pick
                            free(vals);  //@pick
                            return answer;  //@pick
                        }
                    """,
                },
                lines=[("all", "Every product in the table, sorted."), ("pick", "The k-th smallest (k is 1-based).")],
                complexity=["**Time O(rc log(rc)).** **Space O(rc):** up to 9 × 10⁸ numbers, about 3.6 GB. Hopeless at full size."],
                limits=[
                    """
                    Materialising the table is the problem. A min-heap that merges the sorted rows (pop k times) avoids
                    storing everything, but k can still be 9 × 10⁸ pops. The structure we actually need is cheaper: the
                    *number* of cells ≤ v can be computed without listing them.
                    """
                ],
                slow=28,
            ),
            approach(
                "Binary search on the value, counting cells ≤ v",
                "best",
                "O(r · log(rc))",
                "O(1)",
                idea=["Search v in [1, r · c]. `count(v) = Σ min(v // i, cols)` over rows i. If `count(mid) ≥ k`, the answer is ≤ mid (`hi = mid`); else `lo = mid + 1`. Swapping so that rows ≤ cols makes each count loop as short as possible."],
                walk=w2,
                build=["Make `rows ≤ cols` (the table is symmetric).", "`lo = 1`, `hi = rows × cols`.", "Count cells ≤ mid row by row; move the bounds.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def kthInTable(self, rows: int, cols: int, k: int) -> int:
                                if rows > cols:  #@swap
                                    rows, cols = cols, rows  #@swap
                                lo, hi = 1, rows * cols  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    count = sum(min(mid // i, cols) for i in range(1, rows + 1))  #@count
                                    if count >= k:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthInTable(int rows, int cols, int k) {
                                if (rows > cols) { int t = rows; rows = cols; cols = t; }  //@swap
                                int lo = 1, hi = rows * cols;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long count = 0;  //@count
                                    for (int i = 1; i <= rows; i++) count += Math.min(mid / i, cols);  //@count
                                    if (count >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthInTable(int rows, int cols, int k) {
                                if (rows > cols) swap(rows, cols);  //@swap
                                int lo = 1, hi = rows * cols;  //@range
                                while (lo < hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    long long count = 0;  //@count
                                    for (int i = 1; i <= rows; i++) count += min(mid / i, cols);  //@count
                                    if (count >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int kthInTable(int rows, int cols, int k) {
                            if (rows > cols) { int t = rows; rows = cols; cols = t; }  //@swap
                            int lo = 1, hi = rows * cols;  //@range
                            while (lo < hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                long long count = 0;  //@count
                                for (int i = 1; i <= rows; i++) count += (mid / i < cols) ? mid / i : cols;  //@count
                                if (count >= k) hi = mid;  //@move
                                else lo = mid + 1;  //@move
                            }
                            return lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("swap", "i × j = j × i, so the table's values don't change if rows and columns swap. Looping over the shorter side keeps each count cheap."),
                    ("range", "Every value lies in [1, rows · cols] (≤ 9 × 10⁸, fits in `int`)."),
                    ("loop", "Halve the value range."),
                    ("count", "Row i holds i, 2i, …, cols·i; exactly `min(mid / i, cols)` of them are ≤ mid."),
                    ("move", "At least k cells ≤ mid: the k-th value is ≤ mid. Otherwise it's bigger."),
                    ("ret", "The smallest v with at least k cells ≤ v, which is the k-th smallest value (it must actually appear in the table, since the count only rises at real values)."),
                ],
                complexity=["**Time O(r · log(rc))** with r the smaller side: about 30 × 3 × 10⁴ = 9 × 10⁵ steps. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **k-th smallest without listing:** binary-search the *value* v and count elements ≤ v. The answer is the
              smallest v whose count reaches k.
            - It works whenever counting "≤ v" is cheap, even if the elements themselves are too many to store.
            - The smallest such v is always an actual element, because the count only increases at element values.
            """
        ],
    )


@problem
def kth_of_two_lists():
    a, b, k = [1, 4, 6, 9, 12], [2, 3, 7, 10, 15, 20], 6
    want = sorted(a + b)[k - 1]

    w1 = Steps("Concatenate both lists, sort, pick index k − 1.")
    allv = sorted(a + b)
    w1.step(f"Put the two lists side by side: {a + b}.", Row(a, label="a"), Row(b, label="b"), Row(a + b, label="concatenated", slots=True))
    w1.step(f"Together, sorted: {allv}. The {k}-th is {want}.", Row(a, label="a"), Row(b, label="b"), Row(allv, st={k - 1: "answer"}, label="merged", slots=True), result=want)

    w2 = Steps("Merge from the front with two pointers, taking the smaller head each time; the k-th value taken is the answer.")
    i = j = 0
    for step in range(1, k + 1):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            v, src, idx = a[i], "a", i
            i += 1
        else:
            v, src, idx = b[j], "b", j
            j += 1
        w2.step(f"Take #{step}: {v} from {src}.", Row(a, st={**{q: "dim" for q in range(i)}} | ({idx: "answer" if step == k else "active"} if src == "a" else {}), label="a", slots=True), Row(b, st={**{q: "dim" for q in range(j)}} | ({idx: "answer" if step == k else "active"} if src == "b" else {}), label="b", slots=True))
    w2.steps[-1]["result"] = str(want)

    w3 = Steps("Decide how many of the k smallest come from a (i) and from b (j = k − i). Binary-search i so that both 'cuts' are consistent.")
    lo, hi = max(0, k - len(b)), min(k, len(a))
    w3.step(f"i (taken from a) is in [{lo}, {hi}]; j = k − i comes from b.", Row(a, label="a", slots=True), Row(b, label="b", slots=True), Vars(lo=lo, hi=hi))
    while lo < hi:
        i = (lo + hi) // 2
        j = k - i
        ok = a[i] >= b[j - 1]
        w3.step(f"Try i = {i}, j = {j}: next unused a is a[{i}] = {a[i]}, last used b is b[{j - 1}] = {b[j - 1]}. " + ("a[i] ≥ b[j − 1]: taking this many from a is enough or too many, so hi = i." if ok else "a[i] < b[j − 1]: a's next value should have been used instead, so take more from a: lo = i + 1."),
                Row(a, st={q: "found" for q in range(i)} | {i: "mark"}, label="a", slots=True), Row(b, st={q: "found" for q in range(j)} | {j - 1: "mark"}, label="b", slots=True), Vars(lo=lo, hi=hi))
        if ok:
            hi = i
        else:
            lo = i + 1
    i, j = lo, k - lo
    cand = max(a[i - 1] if i else float("-inf"), b[j - 1] if j else float("-inf"))
    w3.step(f"i = {i}, j = {j}: the k smallest are a's first {i} and b's first {j}; the k-th is the larger of their last elements: {cand}.", Row(a, st={q: "answer" for q in range(i)}, label="a", slots=True), Row(b, st={q: "answer" for q in range(j)}, label="b", slots=True), result=int(cand))
    assert cand == want

    sol(
        "kth-of-two-lists",
        summary="""
            The k smallest values of both lists together are always "the first i of a plus the first k − i of b" for some
            i. The right i is the one where these two prefixes are consistent with each other, and that can be
            binary-searched over i in O(log min(m, n)), without merging anything.
        """,
        question=[
            """
            Both lists are sorted. Return the k-th smallest value of all values together (duplicates count separately).

            - **Either list may be empty.**
            - **k counts from 1**, up to m + n.
            - **The goal is O(log(m + n))**, faster than merging.
            """
        ],
        think=[
            f"""
            Take `a = {a}`, `b = {b}`, k = {k}. Merged: `{allv}`; the {k}-th is {want}.

            Look at which elements make up the first {k}: some prefix of a and some prefix of b. Here it's a's first
            {lo} and b's first {k - lo}. So the problem is really: **how many come from a?** Call it i (then j = k − i come
            from b).
            """,
            fig(Row(a, st={q: "answer" for q in range(lo)}, label="a", slots=True), Row(b, st={q: "answer" for q in range(k - lo)}, label="b", slots=True), caption="The k smallest = a prefix of a + a prefix of b."),
            """
            A choice of i is right when nothing left out is smaller than something taken: `a[i] ≥ b[j − 1]` and
            `b[j] ≥ a[i − 1]`. If `a[i] < b[j − 1]`, then a's next value beats something taken from b, so i is too small.
            That test changes from "too small" to "fine" only once as i grows, so binary-search i over its valid range
            `[max(0, k − n), min(k, m)]`. The answer is then the larger of the two last taken values.
            """,
        ],
        approaches=[
            approach(
                "Concatenate and sort",
                "brute",
                "O((m + n) log(m + n))",
                "O(m + n)",
                idea=["Put both lists together, sort, return index k − 1."],
                walk=w1,
                build=["Concatenate.", "Sort.", "Return element k − 1."],
                code={
                    "python": """
                        class Solution:
                            def kthOfTwo(self, a: List[int], b: List[int], k: int) -> int:
                                return sorted(a + b)[k - 1]  #@all
                    """,
                    "java": """
                        class Solution {
                            public int kthOfTwo(int[] a, int[] b, int k) {
                                int[] all = new int[a.length + b.length];  //@all
                                System.arraycopy(a, 0, all, 0, a.length);  //@all
                                System.arraycopy(b, 0, all, a.length, b.length);  //@all
                                Arrays.sort(all);  //@all
                                return all[k - 1];  //@all
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthOfTwo(vector<int>& a, vector<int>& b, int k) {
                                vector<int> all = a;  //@all
                                all.insert(all.end(), b.begin(), b.end());  //@all
                                sort(all.begin(), all.end());  //@all
                                return all[k - 1];  //@all
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* x, const void* y) {  //@all
                            int p = *(const int*) x, q = *(const int*) y;  //@all
                            return (p > q) - (p < q);  //@all
                        }  //@all

                        int kthOfTwo(int* a, int aSize, int* b, int bSize, int k) {
                            int* all = malloc((aSize + bSize) * sizeof(int) + 1);  //@all
                            memcpy(all, a, aSize * sizeof(int));  //@all
                            memcpy(all + aSize, b, bSize * sizeof(int));  //@all
                            qsort(all, aSize + bSize, sizeof(int), cmpInt);  //@all
                            int answer = all[k - 1];  //@all
                            free(all);  //@all
                            return answer;  //@all
                        }
                    """,
                },
                lines=[("all", "Both lists in one array, sorted; the k-th smallest is at index k − 1.", {"c": "The `+ 1` byte keeps `malloc` from receiving 0 when both lists are empty (not possible here, but harmless)."})],
                complexity=["**Time O((m + n) log(m + n)).** **Space O(m + n).**"],
                limits=["Re-sorts data that is already sorted, and processes all m + n values when only k matter."],
            ),
            approach(
                "Merge k steps",
                "better",
                "O(k)",
                "O(1)",
                idea=["Walk both lists from the front with two pointers, each time taking the smaller head; the k-th value taken is the answer."],
                walk=w2,
                build=["`i = j = 0`.", "Repeat k times: take from a if b is used up or `a[i] ≤ b[j]`; else from b.", "Return the last value taken."],
                code={
                    "python": """
                        class Solution:
                            def kthOfTwo(self, a: List[int], b: List[int], k: int) -> int:
                                i = j = 0  #@init
                                for _ in range(k):  #@take
                                    if j == len(b) or (i < len(a) and a[i] <= b[j]):  #@take
                                        value = a[i]  #@take
                                        i += 1  #@take
                                    else:  #@take
                                        value = b[j]  #@take
                                        j += 1  #@take
                                return value  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthOfTwo(int[] a, int[] b, int k) {
                                int i = 0, j = 0, value = 0;  //@init
                                for (int t = 0; t < k; t++) {  //@take
                                    if (j == b.length || (i < a.length && a[i] <= b[j])) value = a[i++];  //@take
                                    else value = b[j++];  //@take
                                }
                                return value;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthOfTwo(vector<int>& a, vector<int>& b, int k) {
                                size_t i = 0, j = 0;  //@init
                                int value = 0;  //@init
                                for (int t = 0; t < k; t++) {  //@take
                                    if (j == b.size() || (i < a.size() && a[i] <= b[j])) value = a[i++];  //@take
                                    else value = b[j++];  //@take
                                }
                                return value;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int kthOfTwo(int* a, int aSize, int* b, int bSize, int k) {
                            int i = 0, j = 0, value = 0;  //@init
                            for (int t = 0; t < k; t++) {  //@take
                                if (j == bSize || (i < aSize && a[i] <= b[j])) value = a[i++];  //@take
                                else value = b[j++];  //@take
                            }
                            return value;  //@ret
                        }
                    """,
                },
                lines=[("init", "Both lists unread."), ("take", "Take the smaller front value (from a when b is exhausted). After k takes, the last one is the k-th smallest."), ("ret", "The k-th value.")],
                complexity=["**Time O(k)**, up to O(m + n). **Space O(1).**"],
                limits=["Still linear in k. Since only the *split* between a and b matters, binary-search the split instead of walking to it."],
            ),
            approach(
                "Binary-search how many come from a",
                "best",
                "O(log min(m, n))",
                "O(1)",
                idea=["Make a the shorter list. Search i (count from a) in `[max(0, k − n), min(k, m)]`, with `j = k − i`. If `a[i] < b[j − 1]`, i is too small (`lo = i + 1`); otherwise `hi = i`. At the end, the answer is `max(a[i − 1], b[j − 1])`, skipping a side that contributes nothing."],
                walk=w3,
                build=["Swap so `len(a) ≤ len(b)`.", "`lo = max(0, k − n)`, `hi = min(k, m)`.", "Binary-search with the test `a[i] < b[k − i − 1]`.", "Return the larger of the last taken values."],
                code={
                    "python": """
                        class Solution:
                            def kthOfTwo(self, a: List[int], b: List[int], k: int) -> int:
                                if len(a) > len(b):  #@swap
                                    a, b = b, a  #@swap
                                m, n = len(a), len(b)
                                lo, hi = max(0, k - n), min(k, m)  #@range
                                while lo < hi:  #@loop
                                    i = (lo + hi) // 2  #@loop
                                    if a[i] < b[k - i - 1]:  #@test
                                        lo = i + 1  #@test
                                    else:  #@test
                                        hi = i  #@test
                                i, j = lo, k - lo  #@ret
                                left_a = a[i - 1] if i > 0 else float("-inf")  #@ret
                                left_b = b[j - 1] if j > 0 else float("-inf")  #@ret
                                return max(left_a, left_b)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthOfTwo(int[] a, int[] b, int k) {
                                if (a.length > b.length) { int[] t = a; a = b; b = t; }  //@swap
                                int m = a.length, n = b.length;
                                int lo = Math.max(0, k - n), hi = Math.min(k, m);  //@range
                                while (lo < hi) {  //@loop
                                    int i = lo + (hi - lo) / 2;  //@loop
                                    if (a[i] < b[k - i - 1]) lo = i + 1;  //@test
                                    else hi = i;  //@test
                                }
                                int i = lo, j = k - lo;  //@ret
                                if (i == 0) return b[j - 1];  //@ret
                                if (j == 0) return a[i - 1];  //@ret
                                return Math.max(a[i - 1], b[j - 1]);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthOfTwo(vector<int>& a, vector<int>& b, int k) {
                                if (a.size() > b.size()) return kthOfTwo(b, a, k);  //@swap
                                int m = a.size(), n = b.size();
                                int lo = max(0, k - n), hi = min(k, m);  //@range
                                while (lo < hi) {  //@loop
                                    int i = lo + (hi - lo) / 2;  //@loop
                                    if (a[i] < b[k - i - 1]) lo = i + 1;  //@test
                                    else hi = i;  //@test
                                }
                                int i = lo, j = k - lo;  //@ret
                                if (i == 0) return b[j - 1];  //@ret
                                if (j == 0) return a[i - 1];  //@ret
                                return max(a[i - 1], b[j - 1]);  //@ret
                            }
                        };
                    """,
                    "c": """
                        int kthOfTwo(int* a, int aSize, int* b, int bSize, int k) {
                            if (aSize > bSize) return kthOfTwo(b, bSize, a, aSize, k);  //@swap
                            int m = aSize, n = bSize;
                            int lo = k - n > 0 ? k - n : 0, hi = k < m ? k : m;  //@range
                            while (lo < hi) {  //@loop
                                int i = lo + (hi - lo) / 2;  //@loop
                                if (a[i] < b[k - i - 1]) lo = i + 1;  //@test
                                else hi = i;  //@test
                            }
                            int i = lo, j = k - lo;  //@ret
                            if (i == 0) return b[j - 1];  //@ret
                            if (j == 0) return a[i - 1];  //@ret
                            return a[i - 1] > b[j - 1] ? a[i - 1] : b[j - 1];  //@ret
                        }
                    """,
                },
                lines=[
                    ("swap", "Search over the shorter list: fewer candidates, and it guarantees the indices below stay in range."),
                    ("range", "i can't be negative or exceed m, and j = k − i can't exceed n, so i ≥ k − n."),
                    ("loop", "Halve the candidate splits."),
                    ("test", "If a's next unused value is smaller than b's last used value, the split is wrong in a's disfavour: take more from a. In this range `i < m` and `j ≥ 1`, so both indices are valid."),
                    ("ret", "With the split fixed, the k-th smallest is the larger of the last element taken from each list (a side contributing nothing is skipped)."),
                ],
                complexity=["**Time O(log min(m, n)).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - "k smallest of two sorted lists" = choose a **split**: i from a, k − i from b.
            - A split is valid when the cut-off elements are ordered consistently; the "too few from a" test is
              monotonic in i, so binary-search i.
            - Search over the shorter list to keep indices in range and the search short.
            """
        ],
    )


@problem
def median_of_two_queues():
    a, b = [1, 5, 8, 12], [2, 3, 9, 10, 15]
    allv = sorted(a + b)
    tot = len(allv)
    want = allv[tot // 2] if tot % 2 else (allv[tot // 2 - 1] + allv[tot // 2]) / 2

    w1 = Steps("Merge from the front until reaching the middle of the combined list.")
    i = j = 0
    taken = []
    while len(taken) <= tot // 2:
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            taken.append(a[i])
            i += 1
        else:
            taken.append(b[j])
            j += 1
        w1.step(f"Take {taken[-1]} (#{len(taken)}).", Row(a, st={q: "found" for q in range(i)}, label="a", slots=True), Row(b, st={q: "found" for q in range(j)}, label="b", slots=True), Row(taken, label="merged so far"))
    w1.step(f"{tot} values in total (odd), so the median is the middle one, #{tot // 2 + 1}: {want}.", Row(taken, st={len(taken) - 1: "answer"}, label="merged so far"), result=want)

    w2 = Steps("Split both lists so the left parts hold half of all values and every left value ≤ every right value. Binary-search the split in the shorter list.")
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    INF = float("inf")
    while True:
        i = (lo + hi) // 2
        j = half - i
        al = a[i - 1] if i > 0 else -INF
        ar = a[i] if i < m else INF
        bl = b[j - 1] if j > 0 else -INF
        br = b[j] if j < n else INF
        fmt = lambda v: "−∞" if v == -INF else ("+∞" if v == INF else str(v))
        if al <= br and bl <= ar:
            med = max(al, bl) if (m + n) % 2 else (max(al, bl) + min(ar, br)) / 2
            w2.step(f"i = {i}, j = {j}: {fmt(al)} ≤ {fmt(br)} and {fmt(bl)} ≤ {fmt(ar)}. Valid split. Odd total, so the median is max(left) = {fmt(max(al, bl))}.", Row(a, st={q: "found" for q in range(i)}, label="a", slots=True), Row(b, st={q: "found" for q in range(j)}, label="b", slots=True), result=med)
            break
        if al > br:
            w2.step(f"i = {i}, j = {j}: a's left max {fmt(al)} > b's right min {fmt(br)}: too much from a, hi = {i - 1}.", Row(a, st={q: "found" for q in range(i)} | ({i - 1: "mark"} if i else {}), label="a", slots=True), Row(b, st={q: "found" for q in range(j)} | ({j: "mark"} if j < n else {}), label="b", slots=True))
            hi = i - 1
        else:
            w2.step(f"i = {i}, j = {j}: b's left max {fmt(bl)} > a's right min {fmt(ar)}: too little from a, lo = {i + 1}.", Row(a, st={q: "found" for q in range(i)} | ({i: "mark"} if i < m else {}), label="a", slots=True), Row(b, st={q: "found" for q in range(j)} | ({j - 1: "mark"} if j else {}), label="b", slots=True))
            lo = i + 1
    a, b = [1, 5, 8, 12], [2, 3, 9, 10, 15]

    sol(
        "median-of-two-queues",
        summary="""
            The median splits the combined values into a left half and a right half. That split consists of a prefix of
            a and a prefix of b, and only the cut position in the shorter list is free: the other follows from "left side
            holds half the values". Binary-search that cut until every left value ≤ every right value: O(log min(m, n)).
        """,
        question=[
            """
            Two sorted lists; return the median of all their values combined: the middle value for an odd total, the
            average of the two middle values for an even total.

            - **Either list can be empty** (but not both).
            - **The result is a decimal number** (`[1, 2]` and `[3, 4]` → 2.5).
            - **Goal O(log(m + n))**, faster than merging.
            """
        ],
        think=[
            f"""
            Take `a = {a}`, `b = {b}`. Combined and sorted: `{allv}` ({tot} values), so the median is the 5th: {want}.

            Draw a line through the combined sorted list right after the median (for an odd total, the median goes on the
            left). Everything left of the line is a prefix of a plus a prefix of b, with **(m + n + 1) / 2** values in
            total. So if we pick how many come from a (call it i), the number from b is forced: j = half − i.
            """,
            fig(Row(allv, st={q: "found" for q in range((tot + 1) // 2)}, slots=True), caption="Left half (shaded) = a prefix of a + a prefix of b."),
            """
            A cut (i, j) is the real median split when the left parts are all ≤ the right parts. Within each list that's
            automatic, so only the cross pairs matter: `a[i − 1] ≤ b[j]` and `b[j − 1] ≤ a[i]`. If `a[i − 1] > b[j]`, too
            many came from a, so move i left; if `b[j − 1] > a[i]`, move i right. Binary search over i in the shorter list
            finds the valid cut. Then the median is `max(left parts)` (odd total) or the average of `max(left)` and
            `min(right)` (even). Missing neighbours at the list ends act as −∞ and +∞.
            """,
        ],
        approaches=[
            approach(
                "Merge up to the middle",
                "brute",
                "O(m + n)",
                "O(1)",
                idea=["Walk both lists from the front with two pointers, remembering the last two values taken. Stop just after the middle position; return the middle value, or the average of the two middle ones for an even total."],
                walk=w1,
                build=["`total = m + n`; walk `total // 2 + 1` steps, keeping the previous and current values.", "Odd total: return the current value. Even: return the average of previous and current."],
                code={
                    "python": """
                        class Solution:
                            def combinedMedian(self, a: List[int], b: List[int]) -> float:
                                total = len(a) + len(b)  #@init
                                i = j = 0  #@init
                                prev = cur = 0  #@init
                                for _ in range(total // 2 + 1):  #@walk
                                    prev = cur  #@walk
                                    if j == len(b) or (i < len(a) and a[i] <= b[j]):  #@walk
                                        cur = a[i]  #@walk
                                        i += 1  #@walk
                                    else:  #@walk
                                        cur = b[j]  #@walk
                                        j += 1  #@walk
                                return float(cur) if total % 2 else (prev + cur) / 2  #@ret
                    """,
                    "java": """
                        class Solution {
                            public double combinedMedian(int[] a, int[] b) {
                                int total = a.length + b.length, i = 0, j = 0, prev = 0, cur = 0;  //@init
                                for (int t = 0; t <= total / 2; t++) {  //@walk
                                    prev = cur;  //@walk
                                    if (j == b.length || (i < a.length && a[i] <= b[j])) cur = a[i++];  //@walk
                                    else cur = b[j++];  //@walk
                                }
                                return total % 2 == 1 ? cur : (prev + cur) / 2.0;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double combinedMedian(vector<int>& a, vector<int>& b) {
                                int total = a.size() + b.size(), prev = 0, cur = 0;  //@init
                                size_t i = 0, j = 0;  //@init
                                for (int t = 0; t <= total / 2; t++) {  //@walk
                                    prev = cur;  //@walk
                                    if (j == b.size() || (i < a.size() && a[i] <= b[j])) cur = a[i++];  //@walk
                                    else cur = b[j++];  //@walk
                                }
                                return total % 2 == 1 ? cur : (prev + cur) / 2.0;  //@ret
                            }
                        };
                    """,
                    "c": """
                        double combinedMedian(int* a, int aSize, int* b, int bSize) {
                            int total = aSize + bSize, i = 0, j = 0, prev = 0, cur = 0;  //@init
                            for (int t = 0; t <= total / 2; t++) {  //@walk
                                prev = cur;  //@walk
                                if (j == bSize || (i < aSize && a[i] <= b[j])) cur = a[i++];  //@walk
                                else cur = b[j++];  //@walk
                            }
                            return total % 2 == 1 ? cur : (prev + cur) / 2.0;  //@ret
                        }
                    """,
                },
                lines=[("init", "Pointers into both lists, and the last two values taken."), ("walk", "Take the smaller front value, total/2 + 1 times; `prev` keeps the one before."), ("ret", "Odd total: the middle value. Even: the average of the two middle values (divide by 2.0 to get a decimal).")],
                complexity=["**Time O(m + n).** **Space O(1).**"],
                limits=["Walks half of all values. The median split is determined by one cut position in the shorter list, which can be binary-searched."],
            ),
            approach(
                "Binary-search the partition",
                "best",
                "O(log min(m, n))",
                "O(1)",
                idea=["Make a the shorter list; `half = (m + n + 1) / 2`. Search i in `[0, m]`, with `j = half − i`. Using ±∞ for missing neighbours: if `a[i − 1] > b[j]`, `hi = i − 1`; if `b[j − 1] > a[i]`, `lo = i + 1`; otherwise the split is valid and the median comes from the four boundary values."],
                walk=w2,
                build=["Swap so `m ≤ n`; `half = (m + n + 1) / 2`.", "Loop: `i = (lo + hi) / 2`, `j = half − i`; read the four boundary values with ±∞ at the ends.", "Valid → odd: `max(aLeft, bLeft)`; even: average of that and `min(aRight, bRight)`.", "Else move lo or hi."],
                code={
                    "python": """
                        class Solution:
                            def combinedMedian(self, a: List[int], b: List[int]) -> float:
                                if len(a) > len(b):  #@swap
                                    a, b = b, a  #@swap
                                m, n = len(a), len(b)
                                half = (m + n + 1) // 2  #@half
                                lo, hi = 0, m  #@half
                                INF = float("inf")
                                while True:  #@cut
                                    i = (lo + hi) // 2  #@cut
                                    j = half - i  #@cut
                                    a_left = a[i - 1] if i > 0 else -INF  #@edges
                                    a_right = a[i] if i < m else INF  #@edges
                                    b_left = b[j - 1] if j > 0 else -INF  #@edges
                                    b_right = b[j] if j < n else INF  #@edges
                                    if a_left <= b_right and b_left <= a_right:  #@valid
                                        if (m + n) % 2:  #@valid
                                            return float(max(a_left, b_left))  #@valid
                                        return (max(a_left, b_left) + min(a_right, b_right)) / 2  #@valid
                                    if a_left > b_right:  #@move
                                        hi = i - 1  #@move
                                    else:  #@move
                                        lo = i + 1  #@move
                    """,
                    "java": """
                        class Solution {
                            public double combinedMedian(int[] a, int[] b) {
                                if (a.length > b.length) return combinedMedian(b, a);  //@swap
                                int m = a.length, n = b.length;
                                int half = (m + n + 1) / 2, lo = 0, hi = m;  //@half
                                while (true) {  //@cut
                                    int i = (lo + hi) / 2, j = half - i;  //@cut
                                    long aLeft = i > 0 ? a[i - 1] : Long.MIN_VALUE;  //@edges
                                    long aRight = i < m ? a[i] : Long.MAX_VALUE;  //@edges
                                    long bLeft = j > 0 ? b[j - 1] : Long.MIN_VALUE;  //@edges
                                    long bRight = j < n ? b[j] : Long.MAX_VALUE;  //@edges
                                    if (aLeft <= bRight && bLeft <= aRight) {  //@valid
                                        if ((m + n) % 2 == 1) return Math.max(aLeft, bLeft);  //@valid
                                        return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2.0;  //@valid
                                    }
                                    if (aLeft > bRight) hi = i - 1;  //@move
                                    else lo = i + 1;  //@move
                                }
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            double combinedMedian(vector<int>& a, vector<int>& b) {
                                if (a.size() > b.size()) return combinedMedian(b, a);  //@swap
                                int m = a.size(), n = b.size();
                                int half = (m + n + 1) / 2, lo = 0, hi = m;  //@half
                                while (true) {  //@cut
                                    int i = (lo + hi) / 2, j = half - i;  //@cut
                                    long long aLeft = i > 0 ? a[i - 1] : LLONG_MIN;  //@edges
                                    long long aRight = i < m ? a[i] : LLONG_MAX;  //@edges
                                    long long bLeft = j > 0 ? b[j - 1] : LLONG_MIN;  //@edges
                                    long long bRight = j < n ? b[j] : LLONG_MAX;  //@edges
                                    if (aLeft <= bRight && bLeft <= aRight) {  //@valid
                                        if ((m + n) % 2 == 1) return max(aLeft, bLeft);  //@valid
                                        return (max(aLeft, bLeft) + min(aRight, bRight)) / 2.0;  //@valid
                                    }
                                    if (aLeft > bRight) hi = i - 1;  //@move
                                    else lo = i + 1;  //@move
                                }
                            }
                        };
                    """,
                    "c": """
                        double combinedMedian(int* a, int aSize, int* b, int bSize) {
                            if (aSize > bSize) return combinedMedian(b, bSize, a, aSize);  //@swap
                            int m = aSize, n = bSize;
                            int half = (m + n + 1) / 2, lo = 0, hi = m;  //@half
                            while (1) {  //@cut
                                int i = (lo + hi) / 2, j = half - i;  //@cut
                                long long aLeft = i > 0 ? a[i - 1] : LLONG_MIN;  //@edges
                                long long aRight = i < m ? a[i] : LLONG_MAX;  //@edges
                                long long bLeft = j > 0 ? b[j - 1] : LLONG_MIN;  //@edges
                                long long bRight = j < n ? b[j] : LLONG_MAX;  //@edges
                                if (aLeft <= bRight && bLeft <= aRight) {  //@valid
                                    long long leftMax = aLeft > bLeft ? aLeft : bLeft;  //@valid
                                    if ((m + n) % 2 == 1) return (double) leftMax;  //@valid
                                    long long rightMin = aRight < bRight ? aRight : bRight;  //@valid
                                    return (leftMax + rightMin) / 2.0;  //@valid
                                }
                                if (aLeft > bRight) hi = i - 1;  //@move
                                else lo = i + 1;  //@move
                            }
                        }
                    """,
                },
                lines=[
                    ("swap", "Search the cut in the shorter list; then j = half − i is always a valid count for the longer one."),
                    ("half", "The left side must hold (m + n + 1) / 2 values: half, with the extra one for odd totals. The cut in a can be anywhere from 0 to m."),
                    ("cut", "Try i values from a; the rest of the left side, j, comes from b."),
                    ("edges", "The four values next to the cuts. A cut at a list's start or end has no neighbour there; −∞ / +∞ stand in so the comparisons still work.", {"java": "`Long.MIN_VALUE` / `Long.MAX_VALUE` act as ±∞; the real values (±10⁶) are widened to `long`.", "cpp": "`LLONG_MIN` / `LLONG_MAX` act as ±∞.", "c": "`LLONG_MIN` / `LLONG_MAX` act as ±∞."}),
                    ("valid", "Every left value ≤ every right value: this is the median split. Odd total: the median is the largest left value. Even: average the largest left and smallest right values. (A valid split never has ±∞ in those, because the left side is non-empty and so is the right side when the total is even.)"),
                    ("move", "a's left part reaches too high: take fewer from a. Otherwise b's left part reaches too high: take more from a."),
                ],
                complexity=["**Time O(log min(m, n)).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Median of two sorted arrays:** partition both so the left sides hold half the values and
              `maxLeft ≤ minRight`; binary-search the cut in the shorter array.
            - Use ±∞ sentinels for cuts at the ends of a list instead of special cases.
            - The same partition idea answers the general k-th smallest of two lists.
            """
        ],
    )
