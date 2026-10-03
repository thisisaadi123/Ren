"""Sorting: quickselect (selection without a full sort)."""
import heapq

from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def select_walk(title, values, target, describe):
    """Three-way quickselect with the middle element as pivot (deterministic for the walkthrough)."""
    w = Steps(title)
    a = values[:]
    lo, hi = 0, len(a) - 1
    w.step(f"We want the value that would sit at index {target} after sorting ({describe}).", Row(a, ptr={"lo": lo, "hi": hi}))
    while True:
        p = a[(lo + hi) // 2]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] < p:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        if target < lt:
            w.step(f"Pivot {p}: smaller values fill {lo}..{lt - 1}, copies of {p} fill {lt}..{gt}. Index {target} is in the smaller part: keep only that part.", Row(a, st={**{t: "mark" for t in range(lo, lt)}, **{t: "found" for t in range(lt, gt + 1)}}, ptr={"lo": lo, "hi": lt - 1}))
            hi = lt - 1
        elif target > gt:
            w.step(f"Pivot {p}: copies of {p} fill {lt}..{gt}. Index {target} is in the bigger part {gt + 1}..{hi}: keep only that part.", Row(a, st={**{t: "found" for t in range(lt, gt + 1)}, **{t: "mark" for t in range(gt + 1, hi + 1)}}, ptr={"lo": gt + 1, "hi": hi}))
            lo = gt + 1
        else:
            w.step(f"Pivot {p} fills {lt}..{gt}, which includes index {target}: the answer is {p}.", Row(a, st={t: "found" for t in range(lt, gt + 1)}), result=p)
            return w


QS_PY = """
                                lo, hi = 0, len(a) - 1  #@range
                                while True:  #@range
                                    p = a[random.randint(lo, hi)]  #@part
                                    lt, i, gt = lo, lo, hi  #@part
                                    while i <= gt:  #@part
                                        if a[i] < p:  #@part
                                            a[lt], a[i] = a[i], a[lt]  #@part
                                            lt += 1  #@part
                                            i += 1  #@part
                                        elif a[i] > p:  #@part
                                            a[i], a[gt] = a[gt], a[i]  #@part
                                            gt -= 1  #@part
                                        else:  #@part
                                            i += 1  #@part
                                    if target < lt:  #@keep
                                        hi = lt - 1  #@keep
                                    elif target > gt:  #@keep
                                        lo = gt + 1  #@keep
                                    else:  #@keep
                                        return p  #@keep
"""

QS_JAVA = """
                                int lo = 0, hi = a.length - 1;  //@range
                                while (true) {  //@range
                                    int p = a[lo + rng.nextInt(hi - lo + 1)];  //@part
                                    int lt = lo, i = lo, gt = hi;  //@part
                                    while (i <= gt) {  //@part
                                        if (a[i] < p) { int t = a[lt]; a[lt++] = a[i]; a[i++] = t; }  //@part
                                        else if (a[i] > p) { int t = a[gt]; a[gt--] = a[i]; a[i] = t; }  //@part
                                        else i++;  //@part
                                    }
                                    if (target < lt) hi = lt - 1;  //@keep
                                    else if (target > gt) lo = gt + 1;  //@keep
                                    else return p;  //@keep
                                }
"""

QS_CPP = """
                                int lo = 0, hi = (int) a.size() - 1;  //@range
                                mt19937 rng(5);  //@range
                                while (true) {  //@range
                                    int p = a[lo + rng() % (hi - lo + 1)];  //@part
                                    int lt = lo, i = lo, gt = hi;  //@part
                                    while (i <= gt) {  //@part
                                        if (a[i] < p) swap(a[lt++], a[i++]);  //@part
                                        else if (a[i] > p) swap(a[i], a[gt--]);  //@part
                                        else i++;  //@part
                                    }
                                    if (target < lt) hi = lt - 1;  //@keep
                                    else if (target > gt) lo = gt + 1;  //@keep
                                    else return p;  //@keep
                                }
"""

QS_C = """
                            int lo = 0, hi = n - 1, answer = 0;  //@range
                            while (1) {  //@range
                                int p = a[lo + rand() % (hi - lo + 1)];  //@part
                                int lt = lo, i = lo, gt = hi;  //@part
                                while (i <= gt) {  //@part
                                    if (a[i] < p) { int t = a[lt]; a[lt++] = a[i]; a[i++] = t; }  //@part
                                    else if (a[i] > p) { int t = a[gt]; a[gt--] = a[i]; a[i] = t; }  //@part
                                    else i++;  //@part
                                }
                                if (target < lt) hi = lt - 1;  //@keep
                                else if (target > gt) lo = gt + 1;  //@keep
                                else { answer = p; break; }  //@keep
                            }
"""


def strip(s):
    return s.strip("\n")


C_CMP = """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort
"""

QS_LINES = [
    ("range", "The answer is somewhere in `a[lo..hi]`; at first, the whole array."),
    ("part", "Three-way partition around a random pivot value: `< p` to the front, `> p` to the back, copies of `p` in the middle."),
    ("keep", "After partitioning, `a[lt..gt]` holds exactly the pivot's copies, in their sorted positions. If the target index is among them, that's the answer; otherwise keep only the side that contains it."),
]


@problem
def kth_highest_bid():
    bids, k = [12, 40, 7, 40, 25, 3, 18], 3
    want = sorted(bids, reverse=True)[k - 1]
    target = len(bids) - k

    w1 = Steps("Sort from highest to lowest and read position k.")
    s = sorted(bids, reverse=True)
    w1.step(f"Sorted high to low: {s}.", Row(s, st={k - 1: "found"}))
    w1.step(f"Position {k}: {want}.", result=want)

    w2 = Steps(f"Keep a min-heap of the {k} highest bids seen so far; its top is the k-th highest.")
    heap = []
    for b in bids:
        heapq.heappush(heap, b)
        if len(heap) > k:
            out = heapq.heappop(heap)
            w2.step(f"Add {b}; more than {k} kept, so drop the smallest, {out}.", Row(sorted(heap), label="heap (sorted for display)"))
        else:
            w2.step(f"Add {b}.", Row(sorted(heap), label="heap (sorted for display)"))
    w2.step(f"The heap's smallest is the {k}-th highest: {heap[0]}.", result=heap[0])

    w3 = select_walk("Quickselect: the k-th highest is the value at index n − k in ascending order. Partition, then keep only the side holding that index.", bids, target, f"n − k = {len(bids)} − {k}")

    sol(
        "kth-highest-bid",
        summary="""
            The k-th highest bid is the value at index `n − k` of the sorted bids. Quickselect finds it without sorting:
            partition around a random pivot (three ways, so repeats are handled), then continue only in the part that
            contains index `n − k`. Expected O(n).
        """,
        question=[
            """
            Return the k-th highest bid, counting repeats: in `[9, 9, 5]` the 2nd highest is 9.

            - **Repeats count separately**, so this is "the value at sorted position k from the top".
            - **Up to 10⁵ bids** and k anywhere from 1 to n.
            """
        ],
        think=[
            f"""
            Bids `{bids}`, `k = {k}`. Sorted high to low: `{s}`, so the 3rd highest is **{want}** (the two 40s are 1st and
            2nd).

            Sorting does more than needed: we want one position, not the whole order. Partitioning around a pivot puts
            the pivot in its final sorted place and splits the rest into smaller and bigger. Only the side containing our
            position matters, so we throw the other away each round: n + n/2 + n/4 + … ≈ 2n work on average.
            """,
            fig(Row(bids, label="bids"), Row(s, label="sorted high → low")),
        ],
        approaches=[
            approach(
                "Sort and index",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort ascending; the k-th highest is at index `n − k`."],
                walk=w1,
                build=["Sort a copy.", "Return `a[n − k]`."],
                code={
                    "python": """
                        class Solution:
                            def kthHighest(self, bids: List[int], k: int) -> int:
                                return sorted(bids)[len(bids) - k]  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int kthHighest(int[] bids, int k) {
                                int[] a = bids.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a[a.length - k];  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthHighest(vector<int>& bids, int k) {
                                vector<int> a = bids;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a[a.size() - k];  //@sort
                            }
                        };
                    """,
                    "c": strip(C_CMP) + """

                        int kthHighest(int* bids, int bidsSize, int k) {
                            int* a = malloc(bidsSize * sizeof(int));  //@sort
                            memcpy(a, bids, bidsSize * sizeof(int));  //@sort
                            qsort(a, bidsSize, sizeof(int), cmp_int);  //@sort
                            int answer = a[bidsSize - k];  //@sort
                            free(a);  //@sort
                            return answer;  //@sort
                        }
                    """,
                },
                lines=[("sort", "Sort ascending; the k-th highest sits k places from the end.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Orders every bid when only one position is wanted. A size-k heap or quickselect does less."],
            ),
            approach(
                "Min-heap of the k highest",
                "better",
                "O(n log k)",
                "O(k)",
                idea=["Push every bid into a min-heap; whenever it holds more than k, pop the smallest. At the end the heap holds the k highest bids, and its top is the k-th highest."],
                walk=w2,
                build=["Min-heap.", "Push each bid; pop when size > k.", "Return the top."],
                code={
                    "python": """
                        import heapq

                        class Solution:
                            def kthHighest(self, bids: List[int], k: int) -> int:
                                heap = []  #@init
                                for b in bids:  #@push
                                    heapq.heappush(heap, b)  #@push
                                    if len(heap) > k:  #@pop
                                        heapq.heappop(heap)  #@pop
                                return heap[0]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthHighest(int[] bids, int k) {
                                PriorityQueue<Integer> heap = new PriorityQueue<>();  //@init
                                for (int b : bids) {  //@push
                                    heap.add(b);  //@push
                                    if (heap.size() > k) heap.poll();  //@pop
                                }
                                return heap.peek();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthHighest(vector<int>& bids, int k) {
                                priority_queue<int, vector<int>, greater<int>> heap;  //@init
                                for (int b : bids) {  //@push
                                    heap.push(b);  //@push
                                    if ((int) heap.size() > k) heap.pop();  //@pop
                                }
                                return heap.top();  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void push(int* h, int* n, int x) {  //@push
                            int i = (*n)++;  //@push
                            while (i > 0 && h[(i - 1) / 2] > x) { h[i] = h[(i - 1) / 2]; i = (i - 1) / 2; }  //@push
                            h[i] = x;  //@push
                        }  //@push

                        static void pop(int* h, int* n) {  //@pop
                            int x = h[--(*n)], i = 0;  //@pop
                            for (int c = 1; c < *n; i = c, c = 2 * c + 1) {  //@pop
                                if (c + 1 < *n && h[c + 1] < h[c]) c++;  //@pop
                                if (h[c] >= x) break;  //@pop
                                h[i] = h[c];  //@pop
                            }  //@pop
                            if (*n > 0) h[i] = x;  //@pop
                        }  //@pop

                        int kthHighest(int* bids, int bidsSize, int k) {
                            int* heap = malloc((k + 1) * sizeof(int));  //@init
                            int n = 0;  //@init
                            for (int i = 0; i < bidsSize; i++) {  //@push
                                push(heap, &n, bids[i]);  //@push
                                if (n > k) pop(heap, &n);  //@pop
                            }
                            int answer = heap[0];  //@ret
                            free(heap);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A min-heap that will hold the k highest bids seen so far.", {"c": "A small array-based binary heap."}),
                    ("push", "Every bid gets a chance.", {"c": "Sift up past bigger parents."}),
                    ("pop", "More than k kept: the smallest can't be among the k highest any more.", {"c": "Remove the root and sift the last value down."}),
                    ("ret", "The smallest of the k highest is the k-th highest."),
                ],
                complexity=["**Time O(n log k).** **Space O(k).**"],
                limits=["Good for streams or small k, but O(n log n) when k is near n/2. Quickselect is O(n) expected for any k."],
            ),
            approach(
                "Three-way quickselect",
                "best",
                "O(n) expected",
                "O(n)",
                idea=["Target index `n − k` in ascending order. Repeatedly partition `a[lo..hi]` three ways around a random pivot. If the target falls in the pivot's block, return the pivot; otherwise continue in the side that contains it."],
                walk=w3,
                build=["Copy; `target = n − k`.", "Loop: random pivot, three-way partition.", "Return or shrink the range."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def kthHighest(self, bids: List[int], k: int) -> int:
                                a = bids[:]  #@init
                                target = len(a) - k  #@init
                    """.rstrip(" ") + strip(QS_PY) + "\n",
                    "java": """
                        class Solution {
                            private final Random rng = new Random(5);

                            public int kthHighest(int[] bids, int k) {
                                int[] a = bids.clone();  //@init
                                int target = a.length - k;  //@init
                    """.rstrip(" ") + strip(QS_JAVA) + """
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthHighest(vector<int>& bids, int k) {
                                vector<int> a = bids;  //@init
                                int target = a.size() - k;  //@init
                    """.rstrip(" ") + strip(QS_CPP) + """
                            }
                        };
                    """,
                    "c": """
                        int kthHighest(int* bids, int bidsSize, int k) {
                            int n = bidsSize;  //@init
                            int* a = malloc(n * sizeof(int));  //@init
                            memcpy(a, bids, n * sizeof(int));  //@init
                            int target = n - k;  //@init
                    """.rstrip(" ") + strip(QS_C) + """
                            free(a);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy to rearrange, and the target index: the k-th highest is at `n − k` in ascending order.")] + QS_LINES + [("ret", "Free the copy and return the value found.")],
                complexity=["**Time O(n) expected:** each round keeps a fraction of the range, so the work is n + n/2 + … ≈ 2n on average (O(n²) only with extremely unlucky pivots). **Space O(n)** for the copy."],
            ),
        ],
        takeaways=[
            """
            - **One order statistic (k-th smallest/largest) → quickselect**, expected O(n).
            - Three-way partitioning makes repeated values harmless and lets you stop as soon as the target lands in the
              pivot block.
            - A size-k heap is the streaming alternative: O(n log k) with O(k) memory.
            """
        ],
    )


@problem
def middle_reading():
    readings = [8, -3, 15, 4, 4, 11, 0]
    n = len(readings)
    want = sorted(readings)[n // 2]

    w1 = Steps("Sort and take the middle.")
    s = sorted(readings)
    w1.step(f"Sorted: {s}. The middle index is {n // 2}.", Row(s, st={n // 2: "found"}))
    w1.step(f"Median: {want}.", result=want)
    w2 = select_walk("Quickselect for index n / 2: partition, then keep only the side holding the middle index.", readings, n // 2, f"the middle of {n}")

    sol(
        "middle-reading",
        summary="""
            The median of an odd number of readings is the value at index `n / 2` of the sorted order. Quickselect finds that
            single position in expected O(n): partition three ways around a random pivot and continue only in the part that
            contains the middle index.
        """,
        question=[
            """
            Return the median of an **odd** number of readings: the value in the middle if they were sorted.

            - **Odd length** means there's exactly one middle value; no averaging.
            - **Values repeat and can be negative.**
            """
        ],
        think=[
            f"""
            Readings `{readings}` sorted are `{s}`; the middle (index {n // 2}) is **{want}**.

            Like any "k-th smallest" question, the median doesn't need the full sort. Partition around a pivot: if the
            middle index lands among the pivot's copies, done; otherwise continue on the one side that contains it.
            """,
            fig(Row(readings, label="readings"), Row(s, label="sorted")),
        ],
        approaches=[
            approach(
                "Sort and take the middle",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort and return the element at index `n / 2`."],
                walk=w1,
                build=["Sort a copy.", "Middle element."],
                code={
                    "python": """
                        class Solution:
                            def middleReading(self, readings: List[int]) -> int:
                                return sorted(readings)[len(readings) // 2]  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int middleReading(int[] readings) {
                                int[] a = readings.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a[a.length / 2];  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int middleReading(vector<int>& readings) {
                                vector<int> a = readings;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a[a.size() / 2];  //@sort
                            }
                        };
                    """,
                    "c": strip(C_CMP) + """

                        int middleReading(int* readings, int readingsSize) {
                            int* a = malloc(readingsSize * sizeof(int));  //@sort
                            memcpy(a, readings, readingsSize * sizeof(int));  //@sort
                            qsort(a, readingsSize, sizeof(int), cmp_int);  //@sort
                            int answer = a[readingsSize / 2];  //@sort
                            free(a);  //@sort
                            return answer;  //@sort
                        }
                    """,
                },
                lines=[("sort", "Sort, then the middle index of an odd-length array.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Sorts everything to read one position. Quickselect reaches that position in expected linear time."],
            ),
            approach(
                "Quickselect for the middle index",
                "best",
                "O(n) expected",
                "O(n)",
                idea=["Run three-way quickselect for index `n / 2`."],
                walk=w2,
                build=["Copy; `target = n / 2`.", "Partition around random pivots, keeping the side with the target.", "Return when the target is in the pivot block."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def middleReading(self, readings: List[int]) -> int:
                                a = readings[:]  #@init
                                target = len(a) // 2  #@init
                    """.rstrip(" ") + strip(QS_PY) + "\n",
                    "java": """
                        class Solution {
                            private final Random rng = new Random(5);

                            public int middleReading(int[] readings) {
                                int[] a = readings.clone();  //@init
                                int target = a.length / 2;  //@init
                    """.rstrip(" ") + strip(QS_JAVA) + """
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int middleReading(vector<int>& readings) {
                                vector<int> a = readings;  //@init
                                int target = a.size() / 2;  //@init
                    """.rstrip(" ") + strip(QS_CPP) + """
                            }
                        };
                    """,
                    "c": """
                        int middleReading(int* readings, int readingsSize) {
                            int n = readingsSize;  //@init
                            int* a = malloc(n * sizeof(int));  //@init
                            memcpy(a, readings, n * sizeof(int));  //@init
                            int target = n / 2;  //@init
                    """.rstrip(" ") + strip(QS_C) + """
                            free(a);  //@ret
                            return answer;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy to rearrange; the median is at index `n / 2`.")] + QS_LINES + [("ret", "Free the copy and return the median.")],
                complexity=["**Time O(n) expected.** **Space O(n)** for the copy."],
            ),
        ],
        takeaways=[
            """
            - **Median = k-th smallest with k = n / 2**: quickselect, expected O(n).
            - For an even count, select both middle positions (or select one and take the max of the left part).
            - For a stream of readings, use two heaps instead.
            """
        ],
    )


@problem
def nearest_stations():
    stations, k = [[3, 4], [-1, 1], [0, -2], [2, 2], [-2, 0], [5, 0]], 3
    key = lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1])  # noqa: E731
    want = sorted(stations, key=key)[:k]

    w1 = Steps("Sort every station by (squared distance, x, y) and keep the first k.")
    s = sorted(stations, key=key)
    w1.step("Squared distances (no square root needed to compare).", Row([f"{x},{y}" for x, y in stations], label="station"), Row([x * x + y * y for x, y in stations], label="distance²"))
    w1.step(f"Sorted: {[f'{x},{y}' for x, y in s]}.", Row([f"{x},{y}" for x, y in s], st={i: "found" for i in range(k)}))
    w1.step(f"First {k}: {want}.", result=str(want))

    w2 = Steps("Quickselect on the keys puts the k smallest in front (in some order); then sort just those k.")
    keys = sorted([key(p) for p in stations])
    w2.step(f"Keys (distance², x, y): {[key(p) for p in stations]}.", Row([f"{d}" for d, _, _ in [key(p) for p in stations]], label="distance²"))
    w2.step(f"Partition until index {k - 1} is settled: the first {k} keys are now the {k} smallest.", Row([f"{d}" for d, _, _ in keys[:k]] + ["|"] + [f"{d}" for d, _, _ in keys[k:]], st={i: "found" for i in range(k)}))
    w2.step(f"Sort only those {k}: {want}.", result=str(want))

    sol(
        "nearest-stations",
        summary="""
            Compare stations by the key (squared distance, x, y); no square roots are needed. Quickselect moves the k
            smallest keys to the front in expected O(n), and sorting just those k gives the required order:
            O(n + k log k).
        """,
        question=[
            """
            Return the `k` stations closest to `(0, 0)`, closest first; ties by smaller `x`, then smaller `y`.

            - **Compare squared distances**: `x² + y²` orders points exactly like the true distance, with whole numbers.
            - **Up to 10⁵ stations**, coordinates up to 10⁴ (so `x² + y²` fits in 32 bits).
            """
        ],
        think=[
            f"""
            Stations `{stations}`, `k = {k}`. Squared distances: {[x * x + y * y for x, y in stations]}. `[-1, 1]` is
            closest (2). `[0, -2]` and `[-2, 0]` tie at 4, and the smaller x wins, so `[-2, 0]` comes first. Answer:
            `{want}`.

            We need the k smallest keys **in order**, but not the order of the other n − k. Quickselect for index `k − 1`
            leaves the k smallest keys in front; sorting just those is cheap when k is small.
            """,
            table(["station", "distance²"], *[(f"{x},{y}", x * x + y * y) for x, y in s]),
        ],
        approaches=[
            approach(
                "Sort everything",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort all stations by `(x² + y², x, y)` and return the first k."],
                walk=w1,
                build=["Sort with the key.", "Slice k."],
                code={
                    "python": """
                        class Solution:
                            def nearestStations(self, stations: List[List[int]], k: int) -> List[List[int]]:
                                ordered = sorted(stations, key=lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1]))  #@sort
                                return ordered[:k]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] nearestStations(int[][] stations, int k) {
                                int[][] a = stations.clone();  //@sort
                                Arrays.sort(a, (p, q) -> {  //@sort
                                    int dp = p[0] * p[0] + p[1] * p[1], dq = q[0] * q[0] + q[1] * q[1];  //@sort
                                    if (dp != dq) return Integer.compare(dp, dq);  //@sort
                                    return p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]);  //@sort
                                });  //@sort
                                return Arrays.copyOf(a, k);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> nearestStations(vector<vector<int>>& stations, int k) {
                                vector<tuple<int, int, int>> keys;  //@sort
                                for (auto& p : stations) keys.push_back({p[0] * p[0] + p[1] * p[1], p[0], p[1]});  //@sort
                                sort(keys.begin(), keys.end());  //@sort
                                vector<vector<int>> out;  //@ret
                                for (int i = 0; i < k; i++) out.push_back({get<1>(keys[i]), get<2>(keys[i])});  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int d, x, y; } Key;

                        static int by_key(const void* p, const void* q) {  //@sort
                            const Key *a = p, *b = q;  //@sort
                            if (a->d != b->d) return (a->d > b->d) - (a->d < b->d);  //@sort
                            if (a->x != b->x) return (a->x > b->x) - (a->x < b->x);  //@sort
                            return (a->y > b->y) - (a->y < b->y);  //@sort
                        }  //@sort

                        int** nearestStations(int** stations, int stationsSize, int* stationsColSize, int k, int* returnSize, int** returnColumnSizes) {
                            Key* keys = malloc(stationsSize * sizeof(Key));  //@sort
                            for (int i = 0; i < stationsSize; i++) {  //@sort
                                int x = stations[i][0], y = stations[i][1];  //@sort
                                keys[i] = (Key){x * x + y * y, x, y};  //@sort
                            }
                            qsort(keys, stationsSize, sizeof(Key), by_key);  //@sort
                            int** out = malloc(k * sizeof(int*));  //@ret
                            *returnColumnSizes = malloc(k * sizeof(int));  //@ret
                            for (int i = 0; i < k; i++) {  //@ret
                                out[i] = malloc(2 * sizeof(int));  //@ret
                                out[i][0] = keys[i].x;  //@ret
                                out[i][1] = keys[i].y;  //@ret
                                (*returnColumnSizes)[i] = 2;  //@ret
                            }
                            free(keys);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("sort", "Order by squared distance, then x, then y."), ("ret", "The first k stations.", {"c": "Each output row has 2 columns."})],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Sorts all n stations though only the first k need ordering. Quickselect separates the k nearest in expected O(n)."],
            ),
            approach(
                "Quickselect the k nearest, then sort them",
                "best",
                "O(n + k log k) expected",
                "O(n)",
                idea=["Build keys `(d, x, y)`. Quickselect for index `k − 1` (three-way partition on whole keys) so the k smallest keys occupy `a[0..k−1]`. Sort that prefix and return its points."],
                walk=w2,
                build=["Keys for every station.", "Quickselect until index k − 1 is in a pivot block.", "Sort the first k keys.", "Return their points."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def nearestStations(self, stations: List[List[int]], k: int) -> List[List[int]]:
                                a = [(x * x + y * y, x, y) for x, y in stations]  #@keys
                                lo, hi, target = 0, len(a) - 1, k - 1  #@select
                                while lo < hi:  #@select
                                    p = a[random.randint(lo, hi)]  #@select
                                    lt, i, gt = lo, lo, hi  #@select
                                    while i <= gt:  #@select
                                        if a[i] < p:  #@select
                                            a[lt], a[i] = a[i], a[lt]  #@select
                                            lt += 1  #@select
                                            i += 1  #@select
                                        elif a[i] > p:  #@select
                                            a[i], a[gt] = a[gt], a[i]  #@select
                                            gt -= 1  #@select
                                        else:  #@select
                                            i += 1  #@select
                                    if target < lt:  #@narrow
                                        hi = lt - 1  #@narrow
                                    elif target > gt:  #@narrow
                                        lo = gt + 1  #@narrow
                                    else:  #@narrow
                                        break  #@narrow
                                return [[x, y] for _, x, y in sorted(a[:k])]  #@ret
                    """,
                    "java": """
                        class Solution {
                            private final Random rng = new Random(11);

                            private static int compare(int[] p, int[] q) {  //@keys
                                if (p[0] != q[0]) return Integer.compare(p[0], q[0]);  //@keys
                                if (p[1] != q[1]) return Integer.compare(p[1], q[1]);  //@keys
                                return Integer.compare(p[2], q[2]);  //@keys
                            }  //@keys

                            public int[][] nearestStations(int[][] stations, int k) {
                                int n = stations.length;  //@keys
                                int[][] a = new int[n][];  //@keys
                                for (int i = 0; i < n; i++) a[i] = new int[] {stations[i][0] * stations[i][0] + stations[i][1] * stations[i][1], stations[i][0], stations[i][1]};  //@keys
                                int lo = 0, hi = n - 1, target = k - 1;  //@select
                                while (lo < hi) {  //@select
                                    int[] p = a[lo + rng.nextInt(hi - lo + 1)];  //@select
                                    int lt = lo, i = lo, gt = hi;  //@select
                                    while (i <= gt) {  //@select
                                        int c = compare(a[i], p);  //@select
                                        if (c < 0) { int[] t = a[lt]; a[lt++] = a[i]; a[i++] = t; }  //@select
                                        else if (c > 0) { int[] t = a[gt]; a[gt--] = a[i]; a[i] = t; }  //@select
                                        else i++;  //@select
                                    }
                                    if (target < lt) hi = lt - 1;  //@narrow
                                    else if (target > gt) lo = gt + 1;  //@narrow
                                    else break;  //@narrow
                                }
                                int[][] first = Arrays.copyOf(a, k);  //@ret
                                Arrays.sort(first, Solution::compare);  //@ret
                                int[][] out = new int[k][];  //@ret
                                for (int i = 0; i < k; i++) out[i] = new int[] {first[i][1], first[i][2]};  //@ret
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> nearestStations(vector<vector<int>>& stations, int k) {
                                vector<tuple<int, int, int>> a;  //@keys
                                for (auto& p : stations) a.push_back({p[0] * p[0] + p[1] * p[1], p[0], p[1]});  //@keys
                                mt19937 rng(11);  //@select
                                int lo = 0, hi = (int) a.size() - 1, target = k - 1;  //@select
                                while (lo < hi) {  //@select
                                    auto p = a[lo + rng() % (hi - lo + 1)];  //@select
                                    int lt = lo, i = lo, gt = hi;  //@select
                                    while (i <= gt) {  //@select
                                        if (a[i] < p) swap(a[lt++], a[i++]);  //@select
                                        else if (p < a[i]) swap(a[i], a[gt--]);  //@select
                                        else i++;  //@select
                                    }
                                    if (target < lt) hi = lt - 1;  //@narrow
                                    else if (target > gt) lo = gt + 1;  //@narrow
                                    else break;  //@narrow
                                }
                                sort(a.begin(), a.begin() + k);  //@ret
                                vector<vector<int>> out;  //@ret
                                for (int i = 0; i < k; i++) out.push_back({get<1>(a[i]), get<2>(a[i])});  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int d, x, y; } Key;

                        static int by_key(const void* p, const void* q) {  //@keys
                            const Key *a = p, *b = q;  //@keys
                            if (a->d != b->d) return (a->d > b->d) - (a->d < b->d);  //@keys
                            if (a->x != b->x) return (a->x > b->x) - (a->x < b->x);  //@keys
                            return (a->y > b->y) - (a->y < b->y);  //@keys
                        }  //@keys

                        int** nearestStations(int** stations, int stationsSize, int* stationsColSize, int k, int* returnSize, int** returnColumnSizes) {
                            int n = stationsSize;  //@keys
                            Key* a = malloc(n * sizeof(Key));  //@keys
                            for (int i = 0; i < n; i++) {  //@keys
                                int x = stations[i][0], y = stations[i][1];  //@keys
                                a[i] = (Key){x * x + y * y, x, y};  //@keys
                            }
                            int lo = 0, hi = n - 1, target = k - 1;  //@select
                            while (lo < hi) {  //@select
                                Key p = a[lo + rand() % (hi - lo + 1)];  //@select
                                int lt = lo, i = lo, gt = hi;  //@select
                                while (i <= gt) {  //@select
                                    int c = by_key(&a[i], &p);  //@select
                                    if (c < 0) { Key t = a[lt]; a[lt++] = a[i]; a[i++] = t; }  //@select
                                    else if (c > 0) { Key t = a[gt]; a[gt--] = a[i]; a[i] = t; }  //@select
                                    else i++;  //@select
                                }
                                if (target < lt) hi = lt - 1;  //@narrow
                                else if (target > gt) lo = gt + 1;  //@narrow
                                else break;  //@narrow
                            }
                            qsort(a, k, sizeof(Key), by_key);  //@ret
                            int** out = malloc(k * sizeof(int*));  //@ret
                            *returnColumnSizes = malloc(k * sizeof(int));  //@ret
                            for (int i = 0; i < k; i++) {  //@ret
                                out[i] = malloc(2 * sizeof(int));  //@ret
                                out[i][0] = a[i].x;  //@ret
                                out[i][1] = a[i].y;  //@ret
                                (*returnColumnSizes)[i] = 2;  //@ret
                            }
                            free(a);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("keys", "A key per station: squared distance, then x, then y. Comparing keys compares stations by the required order."),
                    ("select", "Three-way partition on whole keys around a random pivot key."),
                    ("narrow", "Keep the side containing index `k − 1`. When it's inside the pivot block, everything before it is smaller, so the first k keys are exactly the k smallest."),
                    ("ret", "Sort just those k and return their points.", {"c": "Each output row has 2 columns."}),
                ],
                complexity=["**Time O(n + k log k) expected.** **Space O(n)** for the keys."],
            ),
        ],
        takeaways=[
            """
            - **k smallest, in order:** quickselect the boundary, then sort only the k.
            - Compare squared distances to stay in exact integer arithmetic.
            - A size-k max-heap is the streaming alternative: O(n log k).
            """
        ],
    )
