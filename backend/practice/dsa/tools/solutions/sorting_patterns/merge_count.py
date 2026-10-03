"""Sorting: counting pairs while merge sorting."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def inversion_walk(title, a, label="value"):
    """Merge sort that narrates how many cross pairs each merge counts."""
    w = Steps(title)
    a = a[:]
    total = [0]

    def go(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        go(lo, mid)
        go(mid, hi)
        left, right = a[lo:mid], a[mid:hi]
        i = j = 0
        out, got = [], 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                got += len(left) - i
                out.append(right[j]); j += 1
        out += left[i:] + right[j:]
        total[0] += got
        a[lo:hi] = out
        w.step(f"Merge {left} with {right}: each time the right side's front is smaller, it beats every value still waiting on the left. +{got}.", Row(a, st={x: "found" for x in range(lo, hi)}), Vars(pairs=total[0]))
    go(0, len(a))
    return w, total[0]


@problem
def out_of_order_pairs():
    ranks = [4, 1, 3, 9, 2]
    pairs = [(ranks[i], ranks[j]) for i in range(len(ranks)) for j in range(i + 1, len(ranks)) if ranks[i] > ranks[j]]
    want = len(pairs)

    w1 = Steps("Check every pair i < j.")
    for i in range(len(ranks)):
        later = [ranks[j] for j in range(i + 1, len(ranks)) if ranks[j] < ranks[i]]
        w1.step(f"{ranks[i]} has {len(later)} smaller rank(s) after it: {later}.", Row(ranks, st={i: "active", **{j: "mark" for j in range(i + 1, len(ranks)) if ranks[j] < ranks[i]}}))
    w1.step(f"Total: {want}.", result=want)
    w2, got = inversion_walk("Merge sort, counting while merging: when a value from the right half is taken before values still left in the left half, each of those forms an out-of-order pair with it.", ranks)
    w2.step(f"Total: {got}.", result=got)

    sol(
        "out-of-order-pairs",
        summary="""
            Out-of-order pairs are inversions. Merge sort finds them all at once: when merging two sorted halves, taking a
            value from the right half means every value still waiting in the left half is larger and earlier, so add their
            number. O(n log n).
        """,
        question=[
            """
            Count pairs `i < j` with `ranks[i] > ranks[j]`.

            - **Equal ranks** are not out of order.
            - Up to 1000 ranks here, but the method should scale.
            """
        ],
        think=[
            f"""
            `{ranks}` has {want} such pairs: {', '.join(f'({a}, {b})' for a, b in pairs)}.

            Checking all pairs is O(n²). The faster idea: split the list in two. Pairs inside each half are counted
            recursively; pairs with one value in each half are easy once both halves are sorted. During the merge, if the
            right half's front is smaller than the left half's front, it's smaller than **everything still left** in the
            left half, and all of those came earlier.
            """,
            fig(Row(ranks, label="ranks")),
        ],
        approaches=[
            approach(
                "Check every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Two nested loops over `i < j`, counting `ranks[i] > ranks[j]`."],
                walk=w1,
                build=["Double loop.", "Count."],
                code={
                    "python": """
                        class Solution:
                            def countOutOfOrder(self, ranks: List[int]) -> int:
                                n, count = len(ranks), 0  #@init
                                for i in range(n):  #@pairs
                                    for j in range(i + 1, n):  #@pairs
                                        if ranks[i] > ranks[j]:  #@pairs
                                            count += 1  #@pairs
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int countOutOfOrder(int[] ranks) {
                                int n = ranks.length, count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@pairs
                                    for (int j = i + 1; j < n; j++)  //@pairs
                                        if (ranks[i] > ranks[j]) count++;  //@pairs
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int countOutOfOrder(vector<int>& ranks) {
                                int n = ranks.size(), count = 0;  //@init
                                for (int i = 0; i < n; i++)  //@pairs
                                    for (int j = i + 1; j < n; j++)  //@pairs
                                        if (ranks[i] > ranks[j]) count++;  //@pairs
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int countOutOfOrder(int* ranks, int ranksSize) {
                            int count = 0;  //@init
                            for (int i = 0; i < ranksSize; i++)  //@pairs
                                for (int j = i + 1; j < ranksSize; j++)  //@pairs
                                    if (ranks[i] > ranks[j]) count++;  //@pairs
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count."), ("pairs", "Every earlier/later pair, counted when the earlier rank is larger."), ("ret", "Total.")],
                complexity=["**Time O(n²):** fine for 1000 ranks (500,000 pairs), but 10⁵ would mean 5 × 10⁹. **Space O(1).**"],
                limits=["Quadratic: it doesn't scale. Merge sort counts the cross pairs between two sorted halves in linear time."],
            ),
            approach(
                "Count during merge sort",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Merge sort a copy. While merging `[lo, mid)` and `[mid, hi)`, whenever the right front is strictly smaller than the left front, take it and add `mid − i` (the values left in the left half)."],
                walk=w2,
                build=["Recursive merge sort with a buffer.", "In the merge, add `mid − i` when taking from the right.", "Sum all counts."],
                code={
                    "python": """
                        class Solution:
                            def countOutOfOrder(self, ranks: List[int]) -> int:
                                a, buf = ranks[:], [0] * len(ranks)  #@init
                                def sort(lo, hi):  #@rec
                                    if hi - lo <= 1:  #@rec
                                        return 0  #@rec
                                    mid = (lo + hi) // 2  #@rec
                                    count = sort(lo, mid) + sort(mid, hi)  #@rec
                                    i, j, k = lo, mid, lo  #@merge
                                    while i < mid and j < hi:  #@merge
                                        if a[i] <= a[j]:  #@merge
                                            buf[k] = a[i]; i += 1  #@merge
                                        else:  #@cross
                                            buf[k] = a[j]; j += 1  #@cross
                                            count += mid - i  #@cross
                                        k += 1  #@merge
                                    buf[k:k + mid - i] = a[i:mid]  #@rest
                                    k += mid - i  #@rest
                                    buf[k:k + hi - j] = a[j:hi]  #@rest
                                    a[lo:hi] = buf[lo:hi]  #@rest
                                    return count  #@rest
                                return sort(0, len(a))  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a, buf;

                            public int countOutOfOrder(int[] ranks) {
                                a = ranks.clone();  //@init
                                buf = new int[a.length];  //@init
                                return sort(0, a.length);  //@ret
                            }

                            private int sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) >>> 1;  //@rec
                                int count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) {  //@merge
                                    if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                    else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                                }
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                System.arraycopy(buf, lo, a, lo, hi - lo);  //@rest
                                return count;  //@rest
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a, buf;

                            int sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) / 2;  //@rec
                                int count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) {  //@merge
                                    if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                    else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                                }
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@rest
                                return count;  //@rest
                            }

                        public:
                            int countOutOfOrder(vector<int>& ranks) {
                                a = ranks;  //@init
                                buf.assign(a.size(), 0);  //@init
                                return sort(0, a.size());  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int count_sort(int* a, int* buf, int lo, int hi) {  //@rec
                            if (hi - lo <= 1) return 0;  //@rec
                            int mid = lo + (hi - lo) / 2;  //@rec
                            int count = count_sort(a, buf, lo, mid) + count_sort(a, buf, mid, hi);  //@rec
                            int i = lo, j = mid, k = lo;  //@merge
                            while (i < mid && j < hi) {  //@merge
                                if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                            }
                            while (i < mid) buf[k++] = a[i++];  //@rest
                            while (j < hi) buf[k++] = a[j++];  //@rest
                            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@rest
                            return count;  //@rest
                        }

                        int countOutOfOrder(int* ranks, int ranksSize) {
                            int* a = malloc(ranksSize * sizeof(int));  //@init
                            int* buf = malloc(ranksSize * sizeof(int));  //@init
                            memcpy(a, ranks, ranksSize * sizeof(int));  //@init
                            int count = count_sort(a, buf, 0, ranksSize);  //@ret
                            free(a); free(buf);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A copy to sort (the input stays intact) and a merge buffer."),
                    ("rec", "Pairs inside each half are counted by the recursive calls."),
                    ("merge", "Standard merge; `<=` keeps equal ranks from being counted."),
                    ("cross", "The right front is smaller than the left front, so it's smaller than all `mid − i` values still on the left, and each of those performed earlier: that many out-of-order pairs."),
                    ("rest", "Finish the merge and copy it back; return the count for this range."),
                    ("ret", "Pairs over the whole list."),
                ],
                complexity=["**Time O(n log n).** **Space O(n)** for the copy and buffer."],
            ),
        ],
        takeaways=[
            """
            - **Inversion counting = merge sort + one line**: add `mid − i` when the right side wins.
            - Pairs split into: inside left, inside right, across. Sorting makes the "across" count easy.
            - Use `<=` in the merge so equal values aren't counted.
            """
        ],
    )


@problem
def fewest_neighbour_swaps():
    heights = [3, 1, 2, 5, 4, 2]
    a, swaps = heights[:], 0
    w1 = Steps("Bubble sort, counting swaps: each swap of two neighbours fixes exactly one out-of-order pair.")
    w1.step("Start.", Row(a))
    for end in range(len(a) - 1, 0, -1):
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swaps += 1
                w1.step(f"Swap {a[i + 1]} and {a[i]}. Swaps so far: {swaps}.", Row(a, st={i: "mark", i + 1: "mark"}), Vars(swaps=swaps))
    w1.step(f"Sorted after {swaps} swaps.", result=swaps)
    w2, got = inversion_walk("Count inversions with merge sort instead of performing the swaps.", heights)
    w2.step(f"{got} inversions = {got} swaps.", result=got)

    sol(
        "fewest-neighbour-swaps",
        summary="""
            Swapping two neighbours that are out of order fixes exactly one out-of-order pair and changes no other pair, so
            the fewest swaps equals the number of out-of-order pairs (inversions). Count them with merge sort in
            O(n log n); the answer can exceed 2³¹, so use 64-bit.
        """,
        question=[
            """
            Sort students by height using only swaps of **neighbours**. Equal heights can be in either order. Return the
            minimum number of swaps.

            - **Up to 10⁵ students:** up to ~5 × 10⁹ swaps, which needs a 64-bit result.
            """
        ],
        think=[
            f"""
            Heights `{heights}` need **{swaps}** swaps.

            Why is that the number of out-of-order pairs (`i < j`, `h[i] > h[j]`)? Swapping two neighbours only changes
            the relative order of those two: if they were out of order, the count of out-of-order pairs drops by exactly
            one. The sorted line has zero such pairs, so we need at least that many swaps, and bubble sort achieves exactly
            that. So the answer is just the inversion count; no swapping required.
            """,
            fig(Row(heights, label="heights"), Row(sorted(heights), label="sorted")),
        ],
        approaches=[
            approach(
                "Bubble sort and count swaps",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Run bubble sort on a copy, counting every swap of an out-of-order neighbour pair."],
                walk=w1,
                build=["Repeated passes, swapping neighbours with `a[i] > a[i+1]`.", "Count swaps."],
                code={
                    "python": """
                        class Solution:
                            def minAdjacentSwaps(self, heights: List[int]) -> int:
                                a, swaps = heights[:], 0  #@init
                                for end in range(len(a) - 1, 0, -1):  #@pass
                                    for i in range(end):  #@pass
                                        if a[i] > a[i + 1]:  #@swap
                                            a[i], a[i + 1] = a[i + 1], a[i]  #@swap
                                            swaps += 1  #@swap
                                return swaps  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long minAdjacentSwaps(int[] heights) {
                                int[] a = heights.clone();  //@init
                                long swaps = 0;  //@init
                                for (int end = a.length - 1; end > 0; end--)  //@pass
                                    for (int i = 0; i < end; i++)  //@pass
                                        if (a[i] > a[i + 1]) { int t = a[i]; a[i] = a[i + 1]; a[i + 1] = t; swaps++; }  //@swap
                                return swaps;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long minAdjacentSwaps(vector<int>& heights) {
                                vector<int> a = heights;  //@init
                                long long swaps = 0;  //@init
                                for (int end = (int) a.size() - 1; end > 0; end--)  //@pass
                                    for (int i = 0; i < end; i++)  //@pass
                                        if (a[i] > a[i + 1]) { swap(a[i], a[i + 1]); swaps++; }  //@swap
                                return swaps;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long minAdjacentSwaps(int* heights, int heightsSize) {
                            int* a = malloc(heightsSize * sizeof(int));  //@init
                            memcpy(a, heights, heightsSize * sizeof(int));  //@init
                            long long swaps = 0;  //@init
                            for (int end = heightsSize - 1; end > 0; end--)  //@pass
                                for (int i = 0; i < end; i++)  //@pass
                                    if (a[i] > a[i + 1]) { int t = a[i]; a[i] = a[i + 1]; a[i + 1] = t; swaps++; }  //@swap
                            free(a);  //@ret
                            return swaps;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy and the swap counter (64-bit)."), ("pass", "Each pass bubbles the largest remaining value to the end."), ("swap", "Swap only out-of-order neighbours: each swap removes exactly one inversion."), ("ret", "Swaps performed = the minimum.")],
                complexity=["**Time O(n²).** **Space O(n).**"],
                limits=["Performs every swap, up to ~5 × 10⁹. Since the answer is just the inversion count, merge sort can count them without swapping."],
                slow=True,
            ),
            approach(
                "Count inversions with merge sort",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Merge sort a copy; whenever the right half's front is strictly smaller, add the number of values left in the left half. Sum in 64 bits."],
                walk=w2,
                build=["Merge sort with a buffer.", "Add `mid − i` when the right side wins.", "Return the total."],
                code={
                    "python": """
                        class Solution:
                            def minAdjacentSwaps(self, heights: List[int]) -> int:
                                a, buf = heights[:], [0] * len(heights)  #@init
                                def sort(lo, hi):  #@rec
                                    if hi - lo <= 1:  #@rec
                                        return 0  #@rec
                                    mid = (lo + hi) // 2  #@rec
                                    count = sort(lo, mid) + sort(mid, hi)  #@rec
                                    i, j, k = lo, mid, lo  #@merge
                                    while i < mid and j < hi:  #@merge
                                        if a[i] <= a[j]:  #@merge
                                            buf[k] = a[i]; i += 1  #@merge
                                        else:  #@cross
                                            buf[k] = a[j]; j += 1  #@cross
                                            count += mid - i  #@cross
                                        k += 1  #@merge
                                    buf[k:k + mid - i] = a[i:mid]  #@rest
                                    k += mid - i  #@rest
                                    buf[k:k + hi - j] = a[j:hi]  #@rest
                                    a[lo:hi] = buf[lo:hi]  #@rest
                                    return count  #@rest
                                return sort(0, len(a))  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a, buf;

                            public long minAdjacentSwaps(int[] heights) {
                                a = heights.clone();  //@init
                                buf = new int[a.length];  //@init
                                return sort(0, a.length);  //@ret
                            }

                            private long sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) >>> 1;  //@rec
                                long count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) {  //@merge
                                    if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                    else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                                }
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                System.arraycopy(buf, lo, a, lo, hi - lo);  //@rest
                                return count;  //@rest
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a, buf;

                            long long sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) / 2;  //@rec
                                long long count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) {  //@merge
                                    if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                    else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                                }
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@rest
                                return count;  //@rest
                            }

                        public:
                            long long minAdjacentSwaps(vector<int>& heights) {
                                a = heights;  //@init
                                buf.assign(a.size(), 0);  //@init
                                return sort(0, a.size());  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long count_sort(int* a, int* buf, int lo, int hi) {  //@rec
                            if (hi - lo <= 1) return 0;  //@rec
                            int mid = lo + (hi - lo) / 2;  //@rec
                            long long count = count_sort(a, buf, lo, mid) + count_sort(a, buf, mid, hi);  //@rec
                            int i = lo, j = mid, k = lo;  //@merge
                            while (i < mid && j < hi) {  //@merge
                                if (a[i] <= a[j]) buf[k++] = a[i++];  //@merge
                                else { buf[k++] = a[j++]; count += mid - i; }  //@cross
                            }
                            while (i < mid) buf[k++] = a[i++];  //@rest
                            while (j < hi) buf[k++] = a[j++];  //@rest
                            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@rest
                            return count;  //@rest
                        }

                        long long minAdjacentSwaps(int* heights, int heightsSize) {
                            int* a = malloc(heightsSize * sizeof(int));  //@init
                            int* buf = malloc(heightsSize * sizeof(int));  //@init
                            memcpy(a, heights, heightsSize * sizeof(int));  //@init
                            long long count = count_sort(a, buf, 0, heightsSize);  //@ret
                            free(a); free(buf);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A copy to sort and a merge buffer."),
                    ("rec", "Inversions inside each half, counted recursively (64-bit counts)."),
                    ("merge", "Merge; equal heights don't count (`<=`), since they may stay in either order."),
                    ("cross", "The right front jumps ahead of every value still in the left half: one inversion with each."),
                    ("rest", "Finish the merge, copy back, return this range's count."),
                    ("ret", "Total inversions = fewest neighbour swaps."),
                ],
                complexity=["**Time O(n log n).** **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - **Fewest adjacent swaps to sort = number of inversions.** Each adjacent swap fixes exactly one.
            - Count inversions with merge sort instead of simulating swaps.
            - Check the result's size: n = 10⁵ allows ~5 × 10⁹ inversions, beyond 32 bits.
            """
        ],
    )


@problem
def big_drops():
    prices = [7, 3, 10, 2, 1, 6]
    pairs = [(prices[i], prices[j]) for i in range(len(prices)) for j in range(i + 1, len(prices)) if prices[i] > 2 * prices[j]]
    want = len(pairs)

    w1 = Steps("Check every pair i < j for prices[i] > 2 · prices[j].")
    for i in range(len(prices)):
        hits = [j for j in range(i + 1, len(prices)) if prices[i] > 2 * prices[j]]
        w1.step(f"{prices[i]} is more than double {[prices[j] for j in hits] or 'nothing'} later.", Row(prices, st={i: "active", **{j: "mark" for j in hits}}))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("Merge sort. Before merging two sorted halves, count cross pairs with two pointers: for each left value, how many right values are less than half of it.")
    a = prices[:]
    total = [0]

    def go(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        go(lo, mid)
        go(mid, hi)
        j, got = mid, 0
        for i in range(lo, mid):
            while j < hi and a[i] > 2 * a[j]:
                j += 1
            got += j - mid
        total[0] += got
        left, right = a[lo:mid], a[mid:hi]
        a[lo:hi] = sorted(a[lo:hi])
        w2.step(f"Halves {left} and {right}: the pointer only moves forward, as left values grow. +{got}. Then merge.", Row(a, st={x: "found" for x in range(lo, hi)}), Vars(drops=total[0]))
    go(0, len(a))
    w2.step(f"Total: {total[0]}.", result=total[0])

    sol(
        "big-drops",
        summary="""
            A merge-sort count where the counting rule (`a > 2b`) differs from the merge rule (`a <= b`), so count in a
            separate pass before each merge: with both halves sorted, a pointer into the right half only moves forward as
            the left values grow. O(n log n), with 64-bit arithmetic for `2 · price`.
        """,
        question=[
            """
            Count pairs of days `i < j` with `prices[i] > 2 · prices[j]`.

            - **Prices span the whole 32-bit range**, negatives included, so `2 · price` overflows 32-bit integers.
            - **Up to 5 × 10⁴ prices.**
            """
        ],
        think=[
            f"""
            Prices `{prices}`: the big drops are {', '.join(f'({a}, {b})' for a, b in pairs)}, so **{want}**.

            Like counting inversions, split the list: pairs inside each half are counted recursively; pairs across the halves
            are easy when both halves are sorted. For a left value `x`, the right values that qualify are those below
            `x / 2`: a prefix of the sorted right half. And as `x` grows, that prefix only grows, so one pointer sweeps the
            right half once per merge.

            The twist compared with inversions: the merge itself uses `<=`, a different test, so do the counting sweep
            first, then merge.
            """,
            fig(Row(prices, label="prices")),
        ],
        approaches=[
            approach(
                "Check every pair",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Double loop over `i < j`, counting `prices[i] > 2 · prices[j]` in 64-bit."],
                walk=w1,
                build=["Double loop.", "Compare in 64 bits."],
                code={
                    "python": """
                        class Solution:
                            def countBigDrops(self, prices: List[int]) -> int:
                                n, count = len(prices), 0  #@init
                                for i in range(n):  #@pairs
                                    for j in range(i + 1, n):  #@pairs
                                        if prices[i] > 2 * prices[j]:  #@pairs
                                            count += 1  #@pairs
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countBigDrops(int[] prices) {
                                long count = 0;  //@init
                                for (int i = 0; i < prices.length; i++)  //@pairs
                                    for (int j = i + 1; j < prices.length; j++)  //@pairs
                                        if (prices[i] > 2L * prices[j]) count++;  //@pairs
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countBigDrops(vector<int>& prices) {
                                long long count = 0;  //@init
                                for (size_t i = 0; i < prices.size(); i++)  //@pairs
                                    for (size_t j = i + 1; j < prices.size(); j++)  //@pairs
                                        if (prices[i] > 2LL * prices[j]) count++;  //@pairs
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countBigDrops(int* prices, int pricesSize) {
                            long long count = 0;  //@init
                            for (int i = 0; i < pricesSize; i++)  //@pairs
                                for (int j = i + 1; j < pricesSize; j++)  //@pairs
                                    if (prices[i] > 2LL * prices[j]) count++;  //@pairs
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("init", "The count (64-bit)."), ("pairs", "Every pair; `2 · prices[j]` is computed in 64 bits so it can't overflow.", {"python": "Python integers don't overflow."}), ("ret", "Total.")],
                complexity=["**Time O(n²):** about 1.25 × 10⁹ pairs for 5 × 10⁴ prices. **Space O(1).**"],
                limits=["Too many pairs. As with inversions, sorted halves let one forward-moving pointer count all cross pairs in linear time."],
                slow=True,
            ),
            approach(
                "Merge sort with a counting sweep",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Merge sort a copy. Before each merge of sorted `[lo, mid)` and `[mid, hi)`: keep `j` at `mid`; for each `i` in the left half (increasing), advance `j` while `a[i] > 2 · a[j]`, and add `j − mid`. Then merge as usual."],
                walk=w2,
                build=["Recursive merge sort with a buffer.", "Counting sweep with a forward pointer.", "Ordinary merge.", "Sum the counts."],
                code={
                    "python": """
                        class Solution:
                            def countBigDrops(self, prices: List[int]) -> int:
                                a, buf = prices[:], [0] * len(prices)  #@init
                                def sort(lo, hi):  #@rec
                                    if hi - lo <= 1:  #@rec
                                        return 0  #@rec
                                    mid = (lo + hi) // 2  #@rec
                                    count = sort(lo, mid) + sort(mid, hi)  #@rec
                                    j = mid  #@sweep
                                    for i in range(lo, mid):  #@sweep
                                        while j < hi and a[i] > 2 * a[j]:  #@sweep
                                            j += 1  #@sweep
                                        count += j - mid  #@sweep
                                    i, j, k = lo, mid, lo  #@merge
                                    while i < mid and j < hi:  #@merge
                                        if a[i] <= a[j]:  #@merge
                                            buf[k] = a[i]; i += 1  #@merge
                                        else:  #@merge
                                            buf[k] = a[j]; j += 1  #@merge
                                        k += 1  #@merge
                                    buf[k:k + mid - i] = a[i:mid]  #@merge
                                    k += mid - i  #@merge
                                    buf[k:k + hi - j] = a[j:hi]  #@merge
                                    a[lo:hi] = buf[lo:hi]  #@merge
                                    return count  #@merge
                                return sort(0, len(a))  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a, buf;

                            public long countBigDrops(int[] prices) {
                                a = prices.clone();  //@init
                                buf = new int[a.length];  //@init
                                return sort(0, a.length);  //@ret
                            }

                            private long sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) >>> 1;  //@rec
                                long count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int j = mid;  //@sweep
                                for (int i = lo; i < mid; i++) {  //@sweep
                                    while (j < hi && a[i] > 2L * a[j]) j++;  //@sweep
                                    count += j - mid;  //@sweep
                                }
                                int i = lo, k = lo;  //@merge
                                j = mid;  //@merge
                                while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                                while (i < mid) buf[k++] = a[i++];  //@merge
                                while (j < hi) buf[k++] = a[j++];  //@merge
                                System.arraycopy(buf, lo, a, lo, hi - lo);  //@merge
                                return count;  //@merge
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a, buf;

                            long long sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return 0;  //@rec
                                int mid = (lo + hi) / 2;  //@rec
                                long long count = sort(lo, mid) + sort(mid, hi);  //@rec
                                int j = mid;  //@sweep
                                for (int i = lo; i < mid; i++) {  //@sweep
                                    while (j < hi && a[i] > 2LL * a[j]) j++;  //@sweep
                                    count += j - mid;  //@sweep
                                }
                                int i = lo, k = lo;  //@merge
                                j = mid;  //@merge
                                while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                                while (i < mid) buf[k++] = a[i++];  //@merge
                                while (j < hi) buf[k++] = a[j++];  //@merge
                                copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@merge
                                return count;  //@merge
                            }

                        public:
                            long long countBigDrops(vector<int>& prices) {
                                a = prices;  //@init
                                buf.assign(a.size(), 0);  //@init
                                return sort(0, a.size());  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long drops(int* a, int* buf, int lo, int hi) {  //@rec
                            if (hi - lo <= 1) return 0;  //@rec
                            int mid = lo + (hi - lo) / 2;  //@rec
                            long long count = drops(a, buf, lo, mid) + drops(a, buf, mid, hi);  //@rec
                            int j = mid;  //@sweep
                            for (int i = lo; i < mid; i++) {  //@sweep
                                while (j < hi && a[i] > 2LL * a[j]) j++;  //@sweep
                                count += j - mid;  //@sweep
                            }
                            int i = lo, k = lo;  //@merge
                            j = mid;  //@merge
                            while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                            while (i < mid) buf[k++] = a[i++];  //@merge
                            while (j < hi) buf[k++] = a[j++];  //@merge
                            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@merge
                            return count;  //@merge
                        }

                        long long countBigDrops(int* prices, int pricesSize) {
                            int* a = malloc(pricesSize * sizeof(int));  //@init
                            int* buf = malloc(pricesSize * sizeof(int));  //@init
                            memcpy(a, prices, pricesSize * sizeof(int));  //@init
                            long long count = drops(a, buf, 0, pricesSize);  //@ret
                            free(a); free(buf);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A copy to sort and a buffer."),
                    ("rec", "Pairs within each half, counted recursively."),
                    ("sweep", "Both halves are sorted. For bigger left values, more right values qualify, so `j` only moves forward: O(length) for the whole sweep. `2 · a[j]` in 64 bits."),
                    ("merge", "Then an ordinary merge, so the parent call gets a sorted range."),
                    ("ret", "All big drops."),
                ],
                complexity=["**Time O(n log n).** **Space O(n).**"],
            ),
        ],
        takeaways=[
            """
            - When the **counting condition differs from the sort order**, count in a separate two-pointer sweep before
              merging.
            - Sorted halves make "how many on the right satisfy this" a monotone pointer.
            - Watch overflow: doubling a 32-bit value needs 64 bits.
            """
        ],
    )


@problem
def shorter_behind():
    heights = [5, 2, 6, 1, 3]
    n = len(heights)
    want = [sum(1 for j in range(i + 1, n) if heights[j] < heights[i]) for i in range(n)]

    w1 = Steps("For each person, look at everyone behind and count the shorter ones.")
    for i in range(n):
        w1.step(f"{heights[i]}: {want[i]} shorter behind.", Row(heights, st={i: "active", **{j: "mark" for j in range(i + 1, n) if heights[j] < heights[i]}}), Row(want[:i + 1] + ["·"] * (n - i - 1), label="count"))
    w1.step(f"Counts: {want}.", result=str(want))

    w2 = Steps("Merge sort the positions by height. When a left-half person is placed, every right-half person already placed is shorter and behind them.")
    idx = list(range(n))
    out = [0] * n

    def go(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        go(lo, mid)
        go(mid, hi)
        i, j, merged = lo, mid, []
        while i < mid or j < hi:
            if j < hi and (i == mid or heights[idx[j]] < heights[idx[i]]):
                merged.append(idx[j]); j += 1
            else:
                out[idx[i]] += j - mid
                merged.append(idx[i]); i += 1
        idx[lo:hi] = merged
        w2.step(f"Merge positions {lo}..{hi - 1}: each left person gains the number of right people already taken (shorter).", Row([heights[x] for x in idx], st={x: "found" for x in range(lo, hi)}, label="heights by sort order"), Row(out, label="count"))
    go(0, n)
    w2.step(f"Counts: {out}.", result=str(out))

    w3 = Steps("Walk from the back with a tally of heights seen so far (a Fenwick tree): each person asks how many seen heights are smaller.")
    seen = []
    for i in range(n - 1, -1, -1):
        c = sum(1 for h in seen if h < heights[i])
        seen.append(heights[i])
        w3.step(f"{heights[i]}: {c} of the heights behind are smaller. Add {heights[i]} to the tally.", Row(heights, st={i: "active"}), Row(sorted(seen), label="heights behind (sorted for display)"), Row(["·"] * i + want[i:], label="count"))
    w3.step(f"Counts: {want}.", result=str(want))

    sol(
        "shorter-behind",
        summary="""
            Scan from the back of the queue, keeping a Fenwick tree (binary indexed tree) of the heights already seen. For
            each person, a prefix-sum query counts the seen heights below theirs, then their height is added. Heights lie
            in −10⁴..10⁴, so the tree is small and each step is O(log R). (Merge sort on indices also works.)
        """,
        question=[
            """
            For every person, count the people **behind** them who are **strictly shorter**.

            - **Heights repeat** and can be negative (−10⁴ to 10⁴).
            - **Up to 10⁵ people**, so O(n²) is too slow.
            """
        ],
        think=[
            f"""
            Heights `{heights}` give counts `{want}`: the 5 has 2, 1 and 3 behind it, all shorter.

            This is inversion counting, but **per element**. Two ways to get it fast:

            - Merge sort the positions by height and credit each left-half person with the right-half people placed before
              them.
            - Or walk from the back keeping a running tally of heights seen; each person asks "how many heights in the tally
              are smaller than mine?" A Fenwick tree over the small height range answers that in O(log R).
            """,
            fig(Row(heights, label="heights"), Row(want, label="shorter behind")),
        ],
        approaches=[
            approach(
                "Look behind each person",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["For each `i`, count `j > i` with `heights[j] < heights[i]`."],
                walk=w1,
                build=["Double loop.", "Store each count."],
                code={
                    "python": """
                        class Solution:
                            def countShorterBehind(self, heights: List[int]) -> List[int]:
                                n = len(heights)  #@init
                                out = [0] * n  #@init
                                for i in range(n):  #@scan
                                    for j in range(i + 1, n):  #@scan
                                        if heights[j] < heights[i]:  #@scan
                                            out[i] += 1  #@scan
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] countShorterBehind(int[] heights) {
                                int n = heights.length;  //@init
                                int[] out = new int[n];  //@init
                                for (int i = 0; i < n; i++)  //@scan
                                    for (int j = i + 1; j < n; j++)  //@scan
                                        if (heights[j] < heights[i]) out[i]++;  //@scan
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> countShorterBehind(vector<int>& heights) {
                                int n = heights.size();  //@init
                                vector<int> out(n, 0);  //@init
                                for (int i = 0; i < n; i++)  //@scan
                                    for (int j = i + 1; j < n; j++)  //@scan
                                        if (heights[j] < heights[i]) out[i]++;  //@scan
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* countShorterBehind(int* heights, int heightsSize, int* returnSize) {
                            int n = heightsSize;  //@init
                            int* out = calloc(n, sizeof(int));  //@init
                            for (int i = 0; i < n; i++)  //@scan
                                for (int j = i + 1; j < n; j++)  //@scan
                                    if (heights[j] < heights[i]) out[i]++;  //@scan
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "One count per person."), ("scan", "Everyone behind person `i` who is strictly shorter."), ("ret", "All counts.")],
                complexity=["**Time O(n²).** **Space O(1)** beyond the output."],
                limits=["5 × 10⁹ comparisons for 10⁵ people. The counts are per-element inversions, which merge sort or a tally of heights can produce in O(n log n)."],
                slow=True,
            ),
            approach(
                "Merge sort on positions",
                "better",
                "O(n log n)",
                "O(n)",
                idea=["Merge sort an array of positions, ordered by height. During a merge, when a person from the left half is placed, every right-half person placed before them is shorter and stands behind them: add `j − mid` to that person's count."],
                walk=w2,
                build=["`idx = [0..n−1]`.", "Merge sort `idx` by `heights[idx]`, taking from the right only when strictly shorter.", "When taking from the left, add `j − mid` to `out[idx[i]]`."],
                code={
                    "python": """
                        class Solution:
                            def countShorterBehind(self, heights: List[int]) -> List[int]:
                                n = len(heights)  #@init
                                out, idx, buf = [0] * n, list(range(n)), [0] * n  #@init
                                def sort(lo, hi):  #@rec
                                    if hi - lo <= 1:  #@rec
                                        return  #@rec
                                    mid = (lo + hi) // 2  #@rec
                                    sort(lo, mid)  #@rec
                                    sort(mid, hi)  #@rec
                                    i, j, k = lo, mid, lo  #@merge
                                    while i < mid:  #@merge
                                        if j < hi and heights[idx[j]] < heights[idx[i]]:  #@merge
                                            buf[k] = idx[j]; j += 1  #@merge
                                        else:  #@credit
                                            out[idx[i]] += j - mid  #@credit
                                            buf[k] = idx[i]; i += 1  #@credit
                                        k += 1  #@merge
                                    buf[k:k + hi - j] = idx[j:hi]  #@back
                                    idx[lo:hi] = buf[lo:hi]  #@back
                                sort(0, n)  #@ret
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] h, out, idx, buf;

                            public int[] countShorterBehind(int[] heights) {
                                int n = heights.length;  //@init
                                h = heights;  //@init
                                out = new int[n];  //@init
                                idx = new int[n];  //@init
                                buf = new int[n];  //@init
                                for (int i = 0; i < n; i++) idx[i] = i;  //@init
                                sort(0, n);  //@ret
                                return out;  //@ret
                            }

                            private void sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return;  //@rec
                                int mid = (lo + hi) >>> 1;  //@rec
                                sort(lo, mid);  //@rec
                                sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid) {  //@merge
                                    if (j < hi && h[idx[j]] < h[idx[i]]) buf[k++] = idx[j++];  //@merge
                                    else { out[idx[i]] += j - mid; buf[k++] = idx[i++]; }  //@credit
                                }
                                while (j < hi) buf[k++] = idx[j++];  //@back
                                System.arraycopy(buf, lo, idx, lo, hi - lo);  //@back
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> h, out, idx, buf;

                            void sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return;  //@rec
                                int mid = (lo + hi) / 2;  //@rec
                                sort(lo, mid);  //@rec
                                sort(mid, hi);  //@rec
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid) {  //@merge
                                    if (j < hi && h[idx[j]] < h[idx[i]]) buf[k++] = idx[j++];  //@merge
                                    else { out[idx[i]] += j - mid; buf[k++] = idx[i++]; }  //@credit
                                }
                                while (j < hi) buf[k++] = idx[j++];  //@back
                                copy(buf.begin() + lo, buf.begin() + hi, idx.begin() + lo);  //@back
                            }

                        public:
                            vector<int> countShorterBehind(vector<int>& heights) {
                                int n = heights.size();  //@init
                                h = heights;  //@init
                                out.assign(n, 0);  //@init
                                buf.assign(n, 0);  //@init
                                idx.resize(n);  //@init
                                iota(idx.begin(), idx.end(), 0);  //@init
                                sort(0, n);  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void sort_idx(const int* h, int* out, int* idx, int* buf, int lo, int hi) {  //@rec
                            if (hi - lo <= 1) return;  //@rec
                            int mid = lo + (hi - lo) / 2;  //@rec
                            sort_idx(h, out, idx, buf, lo, mid);  //@rec
                            sort_idx(h, out, idx, buf, mid, hi);  //@rec
                            int i = lo, j = mid, k = lo;  //@merge
                            while (i < mid) {  //@merge
                                if (j < hi && h[idx[j]] < h[idx[i]]) buf[k++] = idx[j++];  //@merge
                                else { out[idx[i]] += j - mid; buf[k++] = idx[i++]; }  //@credit
                            }
                            while (j < hi) buf[k++] = idx[j++];  //@back
                            memcpy(idx + lo, buf + lo, (hi - lo) * sizeof(int));  //@back
                        }

                        int* countShorterBehind(int* heights, int heightsSize, int* returnSize) {
                            int n = heightsSize;  //@init
                            int* out = calloc(n, sizeof(int));  //@init
                            int* idx = malloc(n * sizeof(int));  //@init
                            int* buf = malloc(n * sizeof(int));  //@init
                            for (int i = 0; i < n; i++) idx[i] = i;  //@init
                            sort_idx(heights, out, idx, buf, 0, n);  //@ret
                            free(idx); free(buf);  //@ret
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Counts, the positions to sort, and a buffer. Sorting positions (not heights) lets each count go to the right person."),
                    ("rec", "Sort each half of the positions by height."),
                    ("merge", "Take a right-half person first only when strictly shorter."),
                    ("credit", "When a left-half person is placed, the `j − mid` right-half people already taken are shorter and stand behind them."),
                    ("back", "Finish with the remaining right-half people and copy back."),
                    ("ret", "Every person's count."),
                ],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Correct, but juggling an index array through the merge is fiddly. With heights in a small range, a tally of seen heights (a Fenwick tree) answers each person's question directly, in a simple loop."],
            ),
            approach(
                "Fenwick tree over heights, from the back",
                "best",
                "O(n log R)",
                "O(R)",
                idea=["Shift heights to 1..R (R = 20001). Walk from the last person to the first: `out[i] = prefix(h[i] − 1)` counts seen heights strictly below, then `add(h[i], 1)`."],
                walk=w3,
                build=["Fenwick array of size R + 1.", "From the back: query the prefix just below the height, then add the height.", "Return the counts."],
                code={
                    "python": """
                        class Solution:
                            def countShorterBehind(self, heights: List[int]) -> List[int]:
                                R = 20001  #@init
                                tree = [0] * (R + 1)  #@init
                                out = [0] * len(heights)  #@init
                                for i in range(len(heights) - 1, -1, -1):  #@back
                                    h = heights[i] + 10001  #@back
                                    k, c = h - 1, 0  #@query
                                    while k > 0:  #@query
                                        c += tree[k]  #@query
                                        k -= k & -k  #@query
                                    out[i] = c  #@query
                                    while h <= R:  #@add
                                        tree[h] += 1  #@add
                                        h += h & -h  #@add
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] countShorterBehind(int[] heights) {
                                int R = 20001;  //@init
                                int[] tree = new int[R + 1], out = new int[heights.length];  //@init
                                for (int i = heights.length - 1; i >= 0; i--) {  //@back
                                    int h = heights[i] + 10001;  //@back
                                    int c = 0;  //@query
                                    for (int k = h - 1; k > 0; k -= k & -k) c += tree[k];  //@query
                                    out[i] = c;  //@query
                                    for (int k = h; k <= R; k += k & -k) tree[k]++;  //@add
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> countShorterBehind(vector<int>& heights) {
                                const int R = 20001;  //@init
                                vector<int> tree(R + 1, 0), out(heights.size());  //@init
                                for (int i = (int) heights.size() - 1; i >= 0; i--) {  //@back
                                    int h = heights[i] + 10001;  //@back
                                    int c = 0;  //@query
                                    for (int k = h - 1; k > 0; k -= k & -k) c += tree[k];  //@query
                                    out[i] = c;  //@query
                                    for (int k = h; k <= R; k += k & -k) tree[k]++;  //@add
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* countShorterBehind(int* heights, int heightsSize, int* returnSize) {
                            const int R = 20001;  //@init
                            int* tree = calloc(R + 1, sizeof(int));  //@init
                            int* out = malloc(heightsSize * sizeof(int));  //@init
                            for (int i = heightsSize - 1; i >= 0; i--) {  //@back
                                int h = heights[i] + 10001;  //@back
                                int c = 0;  //@query
                                for (int k = h - 1; k > 0; k -= k & -k) c += tree[k];  //@query
                                out[i] = c;  //@query
                                for (int k = h; k <= R; k += k & -k) tree[k]++;  //@add
                            }
                            free(tree);  //@ret
                            *returnSize = heightsSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A Fenwick tree over the 20,001 possible heights (shifted so −10⁴ becomes 1)."),
                    ("back", "From the back of the queue: the tree holds exactly the people behind person `i`."),
                    ("query", "Prefix sum up to `h − 1`: how many people behind are strictly shorter. `k & −k` is the lowest set bit, the size of the range each tree cell covers."),
                    ("add", "Now person `i` is behind everyone further forward: add their height."),
                    ("ret", "All counts."),
                ],
                complexity=["**Time O(n log R)** with R = 20,001. **Space O(R).**"],
            ),
        ],
        takeaways=[
            """
            - **Per-element inversion counts:** merge sort on indices, or a Fenwick tree over values scanned from one end.
            - A Fenwick tree gives prefix counts and point updates in O(log R); shift values so they start at 1.
            - With large values, compress them to ranks first; the Fenwick approach still works.
            """
        ],
    )
