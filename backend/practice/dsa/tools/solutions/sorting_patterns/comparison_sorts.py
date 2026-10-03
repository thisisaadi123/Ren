"""Sorting: comparison sorts."""
import heapq

from sol import L, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def merge_steps(w, a):
    """Record a top-down merge sort, one step per merge."""
    def go(lo, hi):
        if hi - lo <= 1:
            return a[lo:hi]
        mid = (lo + hi) // 2
        left, right = go(lo, mid), go(mid, hi)
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        out += left[i:] + right[j:]
        a[lo:hi] = out
        w.step(f"Merge {left} and {right} → {out} (positions {lo}..{hi - 1}).", Row(a, st={x: "found" for x in range(lo, hi)}))
        return out
    go(0, len(a))


@problem
def sort_the_scoreboard():
    scores = [42, -7, 15, 42, 0, 9]
    want = sorted(scores)

    w1 = Steps("Insertion sort: grow a sorted prefix; each new score slides left past every bigger score.")
    a = scores[:]
    w1.step("The first score alone is a sorted prefix.", Row(a, st={0: "found"}))
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        moved = 0
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
            moved += 1
        a[j + 1] = x
        w1.step(f"Insert {x}: it slides past {moved} bigger score(s) and lands at position {j + 1}.", Row(a, st={**{t: "found" for t in range(i + 1)}, j + 1: "active"}))
    w1.step(f"Sorted: {a}.", result=str(a))

    w2 = Steps("Quick sort: pick a pivot, move smaller values to its left and larger ones to its right, then sort both sides the same way.")
    a = scores[:]

    def qs(lo, hi):
        if lo >= hi:
            return
        p = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        w2.step(f"Positions {lo}..{hi}: pivot {p} (the last one, for this walkthrough). Smaller values go left; {p} lands at position {i}, its final place.", Row(a, st={**{t: "mark" for t in range(lo, hi + 1)}, i: "found"}))
        qs(lo, i - 1)
        qs(i + 1, hi)
    qs(0, len(a) - 1)
    w2.step(f"Every pivot is in place: {a}.", result=str(a))

    w3 = Steps("Merge sort: split in half until pieces have one value, then merge sorted pieces back together, always taking the smaller front value.")
    a = scores[:]
    w3.step("Start with six scores.", Row(a))
    merge_steps(w3, a)
    w3.step(f"Sorted: {a}.", result=str(a))

    sol(
        "sort-the-scoreboard",
        summary="""
            Merge sort: split the array in half, sort each half the same way, and merge the two sorted halves by
            repeatedly taking the smaller front value. Every level of splitting does O(n) merging and there are log n
            levels, so it's O(n log n) on every input.
        """,
        question=[
            """
            Sort up to 10⁵ integers (negative ones included) from lowest to highest, **without** the language's built-in
            sort.

            - **Duplicates** are allowed and must all be kept.
            - **10⁵ values** rule out O(n²) sorts: that's up to 10¹⁰ steps.
            """
        ],
        think=[
            f"""
            Take `{scores}`. Sorted: `{want}`.

            The simple idea (insert each value into a sorted prefix) costs up to n steps per value. To do better, use the
            fact that **merging two sorted lists is cheap**: compare their fronts and take the smaller, n steps for n
            values. If we can get two sorted halves, one merge finishes the job; and each half can be sorted the same way.
            """,
            fig(Row(scores, label="scores"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Insertion sort",
                "brute",
                "O(n²)",
                "O(n)",
                idea=["Keep the first `i` values sorted. Take value `i`, shift every bigger value in the prefix one place right, and drop it into the gap."],
                walk=w1,
                build=["Copy the input.", "For each `i ≥ 1`, hold `x = a[i]` and walk `j` left while `a[j] > x`, shifting.", "Put `x` at `j + 1`."],
                code={
                    "python": """
                        class Solution:
                            def sortScores(self, scores: List[int]) -> List[int]:
                                a = scores[:]  #@copy
                                for i in range(1, len(a)):  #@loop
                                    x, j = a[i], i - 1  #@loop
                                    while j >= 0 and a[j] > x:  #@shift
                                        a[j + 1] = a[j]  #@shift
                                        j -= 1  #@shift
                                    a[j + 1] = x  #@place
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortScores(int[] scores) {
                                int[] a = scores.clone();  //@copy
                                for (int i = 1; i < a.length; i++) {  //@loop
                                    int x = a[i], j = i - 1;  //@loop
                                    while (j >= 0 && a[j] > x) {  //@shift
                                        a[j + 1] = a[j];  //@shift
                                        j--;  //@shift
                                    }
                                    a[j + 1] = x;  //@place
                                }
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortScores(vector<int>& scores) {
                                vector<int> a = scores;  //@copy
                                for (int i = 1; i < (int) a.size(); i++) {  //@loop
                                    int x = a[i], j = i - 1;  //@loop
                                    while (j >= 0 && a[j] > x) {  //@shift
                                        a[j + 1] = a[j];  //@shift
                                        j--;  //@shift
                                    }
                                    a[j + 1] = x;  //@place
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sortScores(int* scores, int scoresSize, int* returnSize) {
                            int* a = malloc(scoresSize * sizeof(int));  //@copy
                            memcpy(a, scores, scoresSize * sizeof(int));  //@copy
                            for (int i = 1; i < scoresSize; i++) {  //@loop
                                int x = a[i], j = i - 1;  //@loop
                                while (j >= 0 && a[j] > x) {  //@shift
                                    a[j + 1] = a[j];  //@shift
                                    j--;  //@shift
                                }
                                a[j + 1] = x;  //@place
                            }
                            *returnSize = scoresSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("copy", "Work on a copy."), ("loop", "`a[0..i-1]` is sorted; take the next value `x`."), ("shift", "Every bigger value in the prefix moves one place right, opening a gap."), ("place", "`x` drops into the gap: the prefix is sorted again, one longer."), ("ret", "The whole array is the prefix now.")],
                complexity=["**Time O(n²)** in the worst case (a reversed array shifts everything every time), O(n) if already sorted. **Space O(n)** for the copy."],
                limits=["Up to 5 × 10⁹ shifts for 10⁵ scores. Sorting halves and merging them avoids comparing values that are far apart one by one."],
                slow=True,
            ),
            approach(
                "Quick sort with a random pivot",
                "better",
                "O(n log n) expected",
                "O(log n) expected",
                idea=["Pick a random pivot, partition so smaller values come first and the pivot sits in its final place, then quick-sort the two sides. A random pivot splits the range reasonably evenly on average."],
                walk=w2,
                build=["Recursive `sort(lo, hi)`: stop when the range has fewer than 2 values.", "Swap a random element to `hi` as the pivot.", "Partition: walk `j` over the range, moving values smaller than the pivot to the front.", "Put the pivot after them and recurse on both sides."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def sortScores(self, scores: List[int]) -> List[int]:
                                a = scores[:]  #@copy
                                def sort(lo, hi):  #@rec
                                    if lo >= hi:  #@rec
                                        return  #@rec
                                    r = random.randint(lo, hi)  #@pivot
                                    a[r], a[hi] = a[hi], a[r]  #@pivot
                                    p, i = a[hi], lo  #@part
                                    for j in range(lo, hi):  #@part
                                        if a[j] < p:  #@part
                                            a[i], a[j] = a[j], a[i]  #@part
                                            i += 1  #@part
                                    a[i], a[hi] = a[hi], a[i]  #@place
                                    sort(lo, i - 1)  #@sides
                                    sort(i + 1, hi)  #@sides
                                sort(0, len(a) - 1)  #@ret
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            private final Random rng = new Random(7);
                            private int[] a;

                            public int[] sortScores(int[] scores) {
                                a = scores.clone();  //@copy
                                sort(0, a.length - 1);  //@ret
                                return a;  //@ret
                            }

                            private void swap(int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                            private void sort(int lo, int hi) {  //@rec
                                if (lo >= hi) return;  //@rec
                                swap(lo + rng.nextInt(hi - lo + 1), hi);  //@pivot
                                int p = a[hi], i = lo;  //@part
                                for (int j = lo; j < hi; j++) if (a[j] < p) swap(i++, j);  //@part
                                swap(i, hi);  //@place
                                sort(lo, i - 1);  //@sides
                                sort(i + 1, hi);  //@sides
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a;
                            mt19937 rng{7};

                            void sort(int lo, int hi) {  //@rec
                                if (lo >= hi) return;  //@rec
                                swap(a[lo + rng() % (hi - lo + 1)], a[hi]);  //@pivot
                                int p = a[hi], i = lo;  //@part
                                for (int j = lo; j < hi; j++) if (a[j] < p) swap(a[i++], a[j]);  //@part
                                swap(a[i], a[hi]);  //@place
                                sort(lo, i - 1);  //@sides
                                sort(i + 1, hi);  //@sides
                            }

                        public:
                            vector<int> sortScores(vector<int>& scores) {
                                a = scores;  //@copy
                                sort(0, (int) a.size() - 1);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void swap(int* a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                        static void quick(int* a, int lo, int hi) {  //@rec
                            if (lo >= hi) return;  //@rec
                            swap(a, lo + rand() % (hi - lo + 1), hi);  //@pivot
                            int p = a[hi], i = lo;  //@part
                            for (int j = lo; j < hi; j++) if (a[j] < p) swap(a, i++, j);  //@part
                            swap(a, i, hi);  //@place
                            quick(a, lo, i - 1);  //@sides
                            quick(a, i + 1, hi);  //@sides
                        }

                        int* sortScores(int* scores, int scoresSize, int* returnSize) {
                            int* a = malloc(scoresSize * sizeof(int));  //@copy
                            memcpy(a, scores, scoresSize * sizeof(int));  //@copy
                            quick(a, 0, scoresSize - 1);  //@ret
                            *returnSize = scoresSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "Work on a copy."),
                    ("rec", "Sort `a[lo..hi]`; a range of 0 or 1 values is already sorted."),
                    ("pivot", "A random pivot, moved to the end of the range. Randomness makes a terrible split unlikely, whatever the input order."),
                    ("part", "`a[lo..i-1]` holds the values smaller than the pivot found so far; each smaller `a[j]` is swapped into that region."),
                    ("place", "The pivot goes right after the smaller values: that's its final sorted position."),
                    ("sides", "Sort the two sides independently."),
                    ("ret", "Sort the whole array."),
                ],
                complexity=["**Time O(n log n) expected**, O(n²) in the unlucky worst case. **Space O(log n)** expected for the recursion."],
                limits=["Only fast on average: an unlucky run of pivots (or many equal values, which all land on one side) degrades it to O(n²) with deep recursion. Merge sort guarantees O(n log n) on every input."],
            ),
            approach(
                "Merge sort",
                "best",
                "O(n log n)",
                "O(n)",
                idea=["Sort the left half and the right half (recursively), then merge them: compare the two front values, take the smaller (the left one on ties, which keeps equal values in order), and repeat until both halves are used up."],
                walk=w3,
                build=["`sort(lo, hi)` on a half-open range; stop at length 1.", "Sort `[lo, mid)` and `[mid, hi)`.", "Merge into a buffer with two pointers, then copy the buffer back."],
                code={
                    "python": """
                        class Solution:
                            def sortScores(self, scores: List[int]) -> List[int]:
                                a = scores[:]  #@copy
                                buf = [0] * len(a)  #@copy
                                def sort(lo, hi):  #@rec
                                    if hi - lo <= 1:  #@rec
                                        return  #@rec
                                    mid = (lo + hi) // 2  #@split
                                    sort(lo, mid)  #@split
                                    sort(mid, hi)  #@split
                                    i, j, k = lo, mid, lo  #@merge
                                    while i < mid and j < hi:  #@merge
                                        if a[i] <= a[j]:  #@merge
                                            buf[k] = a[i]; i += 1  #@merge
                                        else:  #@merge
                                            buf[k] = a[j]; j += 1  #@merge
                                        k += 1  #@merge
                                    buf[k:k + mid - i] = a[i:mid]  #@rest
                                    k += mid - i  #@rest
                                    buf[k:k + hi - j] = a[j:hi]  #@rest
                                    a[lo:hi] = buf[lo:hi]  #@back
                                sort(0, len(a))  #@ret
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a, buf;

                            public int[] sortScores(int[] scores) {
                                a = scores.clone();  //@copy
                                buf = new int[a.length];  //@copy
                                sort(0, a.length);  //@ret
                                return a;  //@ret
                            }

                            private void sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return;  //@rec
                                int mid = (lo + hi) >>> 1;  //@split
                                sort(lo, mid);  //@split
                                sort(mid, hi);  //@split
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                System.arraycopy(buf, lo, a, lo, hi - lo);  //@back
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a, buf;

                            void sort(int lo, int hi) {  //@rec
                                if (hi - lo <= 1) return;  //@rec
                                int mid = (lo + hi) / 2;  //@split
                                sort(lo, mid);  //@split
                                sort(mid, hi);  //@split
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                                while (i < mid) buf[k++] = a[i++];  //@rest
                                while (j < hi) buf[k++] = a[j++];  //@rest
                                copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@back
                            }

                        public:
                            vector<int> sortScores(vector<int>& scores) {
                                a = scores;  //@copy
                                buf.assign(a.size(), 0);  //@copy
                                sort(0, (int) a.size());  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void merge_sort(int* a, int* buf, int lo, int hi) {  //@rec
                            if (hi - lo <= 1) return;  //@rec
                            int mid = lo + (hi - lo) / 2;  //@split
                            merge_sort(a, buf, lo, mid);  //@split
                            merge_sort(a, buf, mid, hi);  //@split
                            int i = lo, j = mid, k = lo;  //@merge
                            while (i < mid && j < hi) buf[k++] = a[i] <= a[j] ? a[i++] : a[j++];  //@merge
                            while (i < mid) buf[k++] = a[i++];  //@rest
                            while (j < hi) buf[k++] = a[j++];  //@rest
                            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@back
                        }

                        int* sortScores(int* scores, int scoresSize, int* returnSize) {
                            int* a = malloc(scoresSize * sizeof(int));  //@copy
                            int* buf = malloc(scoresSize * sizeof(int));  //@copy
                            memcpy(a, scores, scoresSize * sizeof(int));  //@copy
                            merge_sort(a, buf, 0, scoresSize);  //@ret
                            free(buf);  //@ret
                            *returnSize = scoresSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "A copy to sort and one buffer, reused by every merge."),
                    ("rec", "Sort the half-open range `[lo, hi)`; one value is already sorted."),
                    ("split", "Sort each half first."),
                    ("merge", "Both halves are sorted, so the smallest remaining value is one of the two fronts. `<=` takes the left one on ties, which keeps the sort stable."),
                    ("rest", "One half ran out; the rest of the other is already sorted and bigger than everything taken."),
                    ("back", "Copy the merged range back into place."),
                    ("ret", "Sort everything."),
                ],
                complexity=["**Time O(n log n)** on every input: log n levels of halving, O(n) merging per level. **Space O(n)** for the buffer, plus O(log n) recursion."],
            ),
        ],
        takeaways=[
            """
            - **Merge sort** guarantees O(n log n) and is stable; **quick sort** is in place and fast on average, but only with
              a good pivot.
            - Merging two sorted lists takes linear time: that's the heart of many problems (counting inversions, sorting
              linked lists, k-way merges).
            - Know when a quadratic sort is fine (tiny or nearly sorted inputs) and when it isn't.
            """
        ],
    )


@problem
def nearly_sorted_log():
    times, k = [3, 1, 2, 6, 4, 5, 9, 7, 8], 2
    want = sorted(times)

    w1 = Steps("Insertion sort: each entry slides left past bigger ones. Since every entry is at most k places from home, it never slides more than k steps.")
    a = times[:]
    for i in range(1, len(a)):
        x, j, moved = a[i], i - 1, 0
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]; j -= 1; moved += 1
        a[j + 1] = x
        w1.step(f"Insert {x}: {moved} step(s) left (at most k = {k}).", Row(a, st={**{t: "found" for t in range(i + 1)}, j + 1: "active"}))
    w1.step(f"Sorted: {a}.", result=str(a))

    w2 = Steps(f"A min-heap holding the next k + 1 = {k + 1} entries. The smallest entry still to place is always among them, so pop it, then let the next entry in.")
    heap, out = [], []
    for i, t in enumerate(times):
        heapq.heappush(heap, t)
        if len(heap) > k:
            out.append(heapq.heappop(heap))
            w2.step(f"Add {t}. The heap has {k + 1} entries; the smallest, {out[-1]}, is next in sorted order.", Row(times, st={i: "active"}), Row(sorted(heap), label="heap (sorted for display)"), Row(out, label="output"))
    while heap:
        out.append(heapq.heappop(heap))
    w2.step(f"Empty the heap in order. Output: {out}.", Row(out, label="output"), result=str(out))

    sol(
        "nearly-sorted-log",
        summary="""
            Every entry is at most k places from home, so the smallest entry not yet placed is always among the next k + 1
            entries. Keep those in a min-heap: push the next entry, pop the minimum into the output. O(n log k), and k is
            at most 10.
        """,
        question=[
            """
            Sort timestamps that are already **almost** sorted: each entry is at most `k` positions from where it belongs.

            - **`k` is small (≤ 10)** while `n` reaches 10⁵: the point is to use the near-sortedness.
            - **Equal timestamps** can appear.
            """
        ],
        think=[
            f"""
            Take `{times}` with `k = {k}`. The 1 sits at index 1 but belongs at index 0: one place off. Nothing is more
            than {k} places off. Sorted: `{want}`.

            Which entry goes first? The smallest one, and it must be within the first `k + 1` entries (it can't be more
            than `k` places from index 0). After placing it, the next smallest is within the next `k + 1` candidates, and
            so on. So we only ever need to look at a window of `k + 1` entries, and a min-heap gives us its smallest.
            """,
            fig(Row(times, label="log"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Built-in sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Ignore the hint and sort the copy with the language's sort."],
                build=["Copy and sort."],
                code={
                    "python": """
                        class Solution:
                            def sortLog(self, times: List[int], k: int) -> List[int]:
                                return sorted(times)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] sortLog(int[] times, int k) {
                                int[] a = times.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortLog(vector<int>& times, int k) {
                                vector<int> a = times;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a;  //@sort
                            }
                        };
                    """,
                    "c": """
                        static int cmp(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        int* sortLog(int* times, int timesSize, int k, int* returnSize) {
                            int* a = malloc(timesSize * sizeof(int));  //@sort
                            memcpy(a, times, timesSize * sizeof(int));  //@sort
                            qsort(a, timesSize, sizeof(int), cmp);  //@sort
                            *returnSize = timesSize;  //@sort
                            return a;  //@sort
                        }
                    """,
                },
                lines=[("sort", "A general-purpose O(n log n) sort.", {"c": "The comparator returns the sign without subtracting, so it can't overflow."})],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Correct, but it treats the log as random. With `k` tiny, the order is almost known already: an O(n·k) or O(n log k) method does less work."],
            ),
            approach(
                "Insertion sort",
                "better",
                "O(n·k)",
                "O(n)",
                idea=["Insertion sort moves each entry left past bigger ones. An entry at most `k` places from home passes at most `k` others, so the inner loop is short."],
                walk=w1,
                build=["Copy.", "For each `i`, shift bigger entries right and insert `a[i]`."],
                code={
                    "python": """
                        class Solution:
                            def sortLog(self, times: List[int], k: int) -> List[int]:
                                a = times[:]  #@copy
                                for i in range(1, len(a)):  #@loop
                                    x, j = a[i], i - 1  #@loop
                                    while j >= 0 and a[j] > x:  #@shift
                                        a[j + 1] = a[j]  #@shift
                                        j -= 1  #@shift
                                    a[j + 1] = x  #@shift
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortLog(int[] times, int k) {
                                int[] a = times.clone();  //@copy
                                for (int i = 1; i < a.length; i++) {  //@loop
                                    int x = a[i], j = i - 1;  //@loop
                                    while (j >= 0 && a[j] > x) a[j + 1] = a[j--];  //@shift
                                    a[j + 1] = x;  //@shift
                                }
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortLog(vector<int>& times, int k) {
                                vector<int> a = times;  //@copy
                                for (int i = 1; i < (int) a.size(); i++) {  //@loop
                                    int x = a[i], j = i - 1;  //@loop
                                    while (j >= 0 && a[j] > x) { a[j + 1] = a[j]; j--; }  //@shift
                                    a[j + 1] = x;  //@shift
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sortLog(int* times, int timesSize, int k, int* returnSize) {
                            int* a = malloc(timesSize * sizeof(int));  //@copy
                            memcpy(a, times, timesSize * sizeof(int));  //@copy
                            for (int i = 1; i < timesSize; i++) {  //@loop
                                int x = a[i], j = i - 1;  //@loop
                                while (j >= 0 && a[j] > x) { a[j + 1] = a[j]; j--; }  //@shift
                                a[j + 1] = x;  //@shift
                            }
                            *returnSize = timesSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("copy", "Work on a copy."), ("loop", "Insert entry `i` into the sorted prefix."), ("shift", "It passes only bigger entries, and at most about `k` of them (it's at most `k` from its sorted place), then drops in."), ("ret", "Sorted.")],
                complexity=["**Time O(n·k):** each entry shifts at most ~k times. **Space O(n)** for the copy."],
                limits=["Linear in `k`. A heap of `k + 1` entries does each step in O(log k), which matters when `k` grows (and it's the method that also works on a stream)."],
            ),
            approach(
                "Min-heap of k + 1 entries",
                "best",
                "O(n log k)",
                "O(k)",
                idea=["Push entries into a min-heap. Once it holds `k + 1`, pop the minimum into the output: it must be the next entry in sorted order. When the input runs out, pop the rest."],
                walk=w2,
                build=["Empty min-heap and output.", "For each entry: push; if size > k, pop the smallest to the output.", "Pop everything left."],
                code={
                    "python": """
                        import heapq

                        class Solution:
                            def sortLog(self, times: List[int], k: int) -> List[int]:
                                heap, out = [], []  #@init
                                for t in times:  #@loop
                                    heapq.heappush(heap, t)  #@push
                                    if len(heap) > k:  #@pop
                                        out.append(heapq.heappop(heap))  #@pop
                                while heap:  #@drain
                                    out.append(heapq.heappop(heap))  #@drain
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortLog(int[] times, int k) {
                                PriorityQueue<Integer> heap = new PriorityQueue<>();  //@init
                                int[] out = new int[times.length];  //@init
                                int w = 0;  //@init
                                for (int t : times) {  //@loop
                                    heap.add(t);  //@push
                                    if (heap.size() > k) out[w++] = heap.poll();  //@pop
                                }
                                while (!heap.isEmpty()) out[w++] = heap.poll();  //@drain
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortLog(vector<int>& times, int k) {
                                priority_queue<int, vector<int>, greater<int>> heap;  //@init
                                vector<int> out;  //@init
                                for (int t : times) {  //@loop
                                    heap.push(t);  //@push
                                    if ((int) heap.size() > k) { out.push_back(heap.top()); heap.pop(); }  //@pop
                                }
                                while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }  //@drain
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void push(int* h, int* n, int x) {  //@push
                            int i = (*n)++;  //@push
                            while (i > 0 && h[(i - 1) / 2] > x) { h[i] = h[(i - 1) / 2]; i = (i - 1) / 2; }  //@push
                            h[i] = x;  //@push
                        }  //@push

                        static int pop(int* h, int* n) {  //@pop
                            int top = h[0], x = h[--(*n)], i = 0;  //@pop
                            for (int c = 1; c < *n; i = c, c = 2 * c + 1) {  //@pop
                                if (c + 1 < *n && h[c + 1] < h[c]) c++;  //@pop
                                if (h[c] >= x) break;  //@pop
                                h[i] = h[c];  //@pop
                            }  //@pop
                            if (*n > 0) h[i] = x;  //@pop
                            return top;  //@pop
                        }  //@pop

                        int* sortLog(int* times, int timesSize, int k, int* returnSize) {
                            int* heap = malloc((k + 2) * sizeof(int));  //@init
                            int* out = malloc(timesSize * sizeof(int));  //@init
                            int n = 0, w = 0;  //@init
                            for (int i = 0; i < timesSize; i++) {  //@loop
                                push(heap, &n, times[i]);  //@loop
                                if (n > k) out[w++] = pop(heap, &n);  //@loop
                            }
                            while (n > 0) out[w++] = pop(heap, &n);  //@drain
                            free(heap);  //@ret
                            *returnSize = timesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A min-heap and the output.", {"c": "C has no heap, so a small array-based binary heap: it never holds more than `k + 1` entries."}),
                    ("loop", "Read the log once."),
                    ("push", "The entry joins the candidates.", {"c": "Sift up: move the new value toward the root past bigger parents."}),
                    ("pop", "With `k + 1` candidates, the next value in sorted order must be among them (it's at most `k` places away), and it's the smallest.", {"c": "Pop the root, then sift the last value down past smaller children."}),
                    ("drain", "The final candidates come out in order."),
                    ("ret", "Sorted."),
                ],
                complexity=["**Time O(n log k):** n pushes and pops on a heap of size ≤ k + 1. **Space O(k)** for the heap (plus the output)."],
            ),
        ],
        takeaways=[
            """
            - **"Each element is at most k away"** means the next answer is always in a window of k + 1: a size-k heap.
            - Insertion sort is O(n·k) on such input: simple and often good enough when k is tiny.
            - The heap version works on a stream, emitting sorted output as data arrives.
            """
        ],
    )


@problem
def sort_the_train_cars():
    cars = [4, 2, 1, 3, 2]
    want = sorted(cars)

    w1 = Steps("Copy the weights into an array, sort the array, then write the sorted values back into the cars in order.")
    w1.step("Read the weights.", L(cars), Row(cars, label="array"))
    w1.step("Sort the array.", L(cars), Row(want, label="array"))
    w1.step("Write them back car by car.", L(want), result=str(want))

    w2 = Steps("Merge sort on the list itself: find the middle with slow/fast pointers, cut, sort both halves, merge by relinking.")
    w2.step("Split at the middle: slow moves one car, fast two, so slow stops at the end of the first half.", L(cars, st={2: "active"}, ptr={"slow": 2}))
    w2.step("Cut after the middle: [4, 2, 1] and [3, 2].", L([4, 2, 1], label="left"), L([3, 2], label="right"))
    w2.step("Sorting each half the same way gives [1, 2, 4] and [2, 3].", L([1, 2, 4], label="left sorted"), L([2, 3], label="right sorted"))
    merged, a, b = [], [1, 2, 4], [2, 3]
    while a and b:
        merged.append(a.pop(0) if a[0] <= b[0] else b.pop(0))
        w2.step(f"Link the smaller front car: {merged[-1]}.", L(merged, st={len(merged) - 1: "new"}, label="merged"), L(a or ["·"], label="left"), L(b or ["·"], label="right"))
    merged += a + b
    w2.step(f"One half is empty; link the rest. Result: {merged}.", L(merged, label="merged"), result=str(merged))

    sol(
        "sort-the-train-cars",
        summary="""
            Merge sort fits linked lists perfectly: find the middle with a slow and a fast pointer, cut the list in two,
            sort each half, and merge the halves by relinking nodes, no copying. O(n log n) time and only O(log n) extra
            space for the recursion.
        """,
        question=[
            """
            Sort a singly linked list by `val` and return the new head.

            - **No random access:** you can't jump to the middle or swap by index like with an array.
            - **The list can be empty** (return null) or have one car.
            - **Up to 5 × 10⁴ cars.**
            """
        ],
        think=[
            f"""
            Cars `{cars}` should become `{want}`.

            Array sorts lean on indexing. Linked lists are good at the opposite things: cutting a list in two and splicing
            nodes together are O(1). That's exactly what merge sort needs: split in half, sort each half, and merge two
            sorted lists by always linking the smaller front node.
            """,
            fig(L(cars, label="train"), L(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Copy into an array and sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Read every value into an array, sort it with the built-in sort, and write the values back into the nodes in order."],
                walk=w1,
                build=["Walk the list, collecting values.", "Sort them.", "Walk again, overwriting each node's value."],
                code={
                    "python": """
                        class Solution:
                            def sortCars(self, head: Optional[ListNode]) -> Optional[ListNode]:
                                vals, node = [], head  #@read
                                while node:  #@read
                                    vals.append(node.val)  #@read
                                    node = node.next  #@read
                                vals.sort()  #@sort
                                node = head  #@write
                                for v in vals:  #@write
                                    node.val = v  #@write
                                    node = node.next  #@write
                                return head  #@ret
                    """,
                    "java": """
                        class Solution {
                            public ListNode sortCars(ListNode head) {
                                List<Integer> vals = new ArrayList<>();  //@read
                                for (ListNode n = head; n != null; n = n.next) vals.add(n.val);  //@read
                                Collections.sort(vals);  //@sort
                                ListNode n = head;  //@write
                                for (int v : vals) { n.val = v; n = n.next; }  //@write
                                return head;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            ListNode* sortCars(ListNode* head) {
                                vector<int> vals;  //@read
                                for (ListNode* n = head; n; n = n->next) vals.push_back(n->val);  //@read
                                sort(vals.begin(), vals.end());  //@sort
                                ListNode* n = head;  //@write
                                for (int v : vals) { n->val = v; n = n->next; }  //@write
                                return head;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int cmp(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort

                        struct ListNode* sortCars(struct ListNode* head) {
                            int n = 0;  //@read
                            for (struct ListNode* p = head; p; p = p->next) n++;  //@read
                            int* vals = malloc((n + 1) * sizeof(int));  //@read
                            int i = 0;  //@read
                            for (struct ListNode* p = head; p; p = p->next) vals[i++] = p->val;  //@read
                            qsort(vals, n, sizeof(int), cmp);  //@sort
                            i = 0;  //@write
                            for (struct ListNode* p = head; p; p = p->next) p->val = vals[i++];  //@write
                            free(vals);  //@ret
                            return head;  //@ret
                        }
                    """,
                },
                lines=[("read", "Collect the values in list order."), ("sort", "Sort them as an array."), ("write", "Overwrite node values in order; the links never change."), ("ret", "Same head node, now holding the smallest value.")],
                complexity=["**Time O(n log n).** **Space O(n)** for the array."],
                limits=["Needs an O(n) array and rewrites values rather than reordering cars (if nodes carried more data, that would be wrong). Merge sort sorts the links themselves with only recursion as extra space."],
            ),
            approach(
                "Merge sort on the list",
                "best",
                "O(n log n)",
                "O(log n)",
                idea=["`sort(head)`: if the list has 0 or 1 nodes, return it. Find the middle (slow moves 1, fast moves 2), cut after it, sort both halves, and merge them: keep a tail pointer and repeatedly link the smaller front node."],
                walk=w2,
                build=["Base case: empty or single node.", "Slow/fast pointers to the end of the first half; cut.", "Recursively sort both halves.", "Merge with a dummy head."],
                code={
                    "python": """
                        class Solution:
                            def sortCars(self, head: Optional[ListNode]) -> Optional[ListNode]:
                                if not head or not head.next:  #@base
                                    return head  #@base
                                slow, fast = head, head.next  #@mid
                                while fast and fast.next:  #@mid
                                    slow, fast = slow.next, fast.next.next  #@mid
                                right, slow.next = slow.next, None  #@cut
                                a, b = self.sortCars(head), self.sortCars(right)  #@halves
                                dummy = tail = ListNode()  #@merge
                                while a and b:  #@merge
                                    if a.val <= b.val:  #@merge
                                        tail.next, a = a, a.next  #@merge
                                    else:  #@merge
                                        tail.next, b = b, b.next  #@merge
                                    tail = tail.next  #@merge
                                tail.next = a or b  #@rest
                                return dummy.next  #@ret
                    """,
                    "java": """
                        class Solution {
                            public ListNode sortCars(ListNode head) {
                                if (head == null || head.next == null) return head;  //@base
                                ListNode slow = head, fast = head.next;  //@mid
                                while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }  //@mid
                                ListNode right = slow.next;  //@cut
                                slow.next = null;  //@cut
                                ListNode a = sortCars(head), b = sortCars(right);  //@halves
                                ListNode dummy = new ListNode(), tail = dummy;  //@merge
                                while (a != null && b != null) {  //@merge
                                    if (a.val <= b.val) { tail.next = a; a = a.next; }  //@merge
                                    else { tail.next = b; b = b.next; }  //@merge
                                    tail = tail.next;  //@merge
                                }
                                tail.next = a != null ? a : b;  //@rest
                                return dummy.next;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            ListNode* sortCars(ListNode* head) {
                                if (!head || !head->next) return head;  //@base
                                ListNode *slow = head, *fast = head->next;  //@mid
                                while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }  //@mid
                                ListNode* right = slow->next;  //@cut
                                slow->next = nullptr;  //@cut
                                ListNode *a = sortCars(head), *b = sortCars(right);  //@halves
                                ListNode dummy;  //@merge
                                ListNode* tail = &dummy;  //@merge
                                while (a && b) {  //@merge
                                    if (a->val <= b->val) { tail->next = a; a = a->next; }  //@merge
                                    else { tail->next = b; b = b->next; }  //@merge
                                    tail = tail->next;  //@merge
                                }
                                tail->next = a ? a : b;  //@rest
                                return dummy.next;  //@ret
                            }
                        };
                    """,
                    "c": """
                        struct ListNode* sortCars(struct ListNode* head) {
                            if (!head || !head->next) return head;  //@base
                            struct ListNode *slow = head, *fast = head->next;  //@mid
                            while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }  //@mid
                            struct ListNode* right = slow->next;  //@cut
                            slow->next = NULL;  //@cut
                            struct ListNode *a = sortCars(head), *b = sortCars(right);  //@halves
                            struct ListNode dummy = {0, NULL}, *tail = &dummy;  //@merge
                            while (a && b) {  //@merge
                                if (a->val <= b->val) { tail->next = a; a = a->next; }  //@merge
                                else { tail->next = b; b = b->next; }  //@merge
                                tail = tail->next;  //@merge
                            }
                            tail->next = a ? a : b;  //@rest
                            return dummy.next;  //@ret
                        }
                    """,
                },
                lines=[
                    ("base", "Zero or one car is already sorted."),
                    ("mid", "Fast moves two steps for slow's one; starting fast one ahead makes slow stop at the last node of the first half (so a 2-node list splits 1 + 1)."),
                    ("cut", "Detach the second half."),
                    ("halves", "Sort each half."),
                    ("merge", "A dummy node gives the merged list a fixed start; link whichever front node is smaller (left on ties, keeping it stable)."),
                    ("rest", "Whatever remains is sorted already: link it in one go."),
                    ("ret", "The merged list starts after the dummy."),
                ],
                complexity=["**Time O(n log n):** log n levels, each doing O(n) pointer walking. **Space O(log n)** for the recursion; no node is copied."],
            ),
        ],
        takeaways=[
            """
            - **Linked list sorting = merge sort**: splitting (slow/fast pointers) and merging (relinking) are natural on
              lists.
            - A dummy head removes the special case for the first merged node.
            - Copying values into an array works, but changes values instead of reordering nodes.
            """
        ],
    )


@problem
def sort_with_many_repeats():
    readings = [5, 3, 5, 1, 5, 3, 5]
    want = sorted(readings)

    w1 = Steps("Two-way quick sort: values smaller than the pivot go left, everything else right. Equal values all pile onto one side.")
    a = readings[:]

    def qs(lo, hi):
        if lo >= hi:
            return
        p, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        w1.step(f"Positions {lo}..{hi}: pivot {p} lands at {i}; the {sum(1 for t in range(i + 1, hi + 1) if a[t] == p)} other copies of {p} still have to be sorted on the right.", Row(a, st={**{t: "mark" for t in range(lo, hi + 1)}, i: "found"}))
        qs(lo, i - 1); qs(i + 1, hi)
    qs(0, len(a) - 1)
    w1.step(f"Sorted, but every copy of 5 needed its own partition pass: {a}.", result=str(a))

    w2 = Steps("Three-way partition: one pass splits the range into < pivot | = pivot | > pivot, and the middle part is finished at once.")
    a = readings[:]
    p = 5
    lt, i, gt = 0, 0, len(a) - 1
    w2.step(f"Pivot {p}. lt, i and gt start at the ends.", Row(a, ptr={"lt": lt, "i": i, "gt": gt}))
    while i <= gt:
        if a[i] < p:
            a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1; why = "smaller: swap it to the lt side"
        elif a[i] > p:
            a[i], a[gt] = a[gt], a[i]; gt -= 1; why = "bigger: swap it to the gt side (don't advance i)"
        else:
            i += 1; why = "equal: leave it in the middle"
        w2.step(f"a[i] was {why}.", Row(a, st={**{t: "found" for t in range(lt, i)}}, ptr={"lt": lt, "i": min(i, len(a) - 1), "gt": max(gt, 0)}))
    w2.step(f"Every 5 sits in positions {lt}..{gt} and is done. Only the smaller side [{', '.join(map(str, a[:lt]))}] still needs sorting.", Row(a, st={t: "found" for t in range(lt, gt + 1)}), result=str(want))

    sol(
        "sort-with-many-repeats",
        summary="""
            Quick sort with a **three-way partition**: one pass splits the range into values below the pivot, equal to it,
            and above it, and the equal block is finished on the spot. With few distinct values, each pass removes a whole
            value from the problem, so repeats make it faster, not slower. O(n log n) expected, O(n · distinct) at worst
            under few-distinct data.
        """,
        question=[
            """
            Sort `readings` without the built-in sort. Most readings repeat a handful of values.

            - **Up to 10⁵ readings**, possibly all equal.
            - The statement warns that a quick sort which ignores repeats becomes very slow.
            """
        ],
        think=[
            f"""
            Readings `{readings}`, sorted `{want}`.

            Ordinary (two-way) partitioning puts values equal to the pivot on one side. If all values are equal, every
            partition peels off just the pivot itself: n levels of n work, O(n²), and recursion n deep.

            The fix is to treat "equal to the pivot" as its own group. After a three-way partition, the equal block is in
            its final place and never touched again. With all-equal input, one pass finishes everything.
            """,
            fig(Row(readings, label="readings"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Two-way quick sort",
                "brute",
                "O(n²) with repeats",
                "O(n) recursion",
                idea=["Classic quick sort: random pivot, values strictly smaller go left, the rest go right, recurse on both sides."],
                walk=w1,
                build=["Random pivot swapped to the end.", "Partition by `< pivot`.", "Recurse on both sides."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def sortReadings(self, readings: List[int]) -> List[int]:
                                a = readings[:]  #@copy
                                def sort(lo, hi):  #@rec
                                    if lo >= hi:  #@rec
                                        return  #@rec
                                    r = random.randint(lo, hi)  #@part
                                    a[r], a[hi] = a[hi], a[r]  #@part
                                    p, i = a[hi], lo  #@part
                                    for j in range(lo, hi):  #@part
                                        if a[j] < p:  #@part
                                            a[i], a[j] = a[j], a[i]  #@part
                                            i += 1  #@part
                                    a[i], a[hi] = a[hi], a[i]  #@part
                                    sort(lo, i - 1)  #@sides
                                    sort(i + 1, hi)  #@sides
                                sort(0, len(a) - 1)  #@ret
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            private final Random rng = new Random(7);
                            private int[] a;

                            public int[] sortReadings(int[] readings) {
                                a = readings.clone();  //@copy
                                sort(0, a.length - 1);  //@ret
                                return a;  //@ret
                            }

                            private void swap(int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                            private void sort(int lo, int hi) {  //@rec
                                if (lo >= hi) return;  //@rec
                                swap(lo + rng.nextInt(hi - lo + 1), hi);  //@part
                                int p = a[hi], i = lo;  //@part
                                for (int j = lo; j < hi; j++) if (a[j] < p) swap(i++, j);  //@part
                                swap(i, hi);  //@part
                                sort(lo, i - 1);  //@sides
                                sort(i + 1, hi);  //@sides
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a;
                            mt19937 rng{7};

                            void sort(int lo, int hi) {  //@rec
                                if (lo >= hi) return;  //@rec
                                swap(a[lo + rng() % (hi - lo + 1)], a[hi]);  //@part
                                int p = a[hi], i = lo;  //@part
                                for (int j = lo; j < hi; j++) if (a[j] < p) swap(a[i++], a[j]);  //@part
                                swap(a[i], a[hi]);  //@part
                                sort(lo, i - 1);  //@sides
                                sort(i + 1, hi);  //@sides
                            }

                        public:
                            vector<int> sortReadings(vector<int>& readings) {
                                a = readings;  //@copy
                                sort(0, (int) a.size() - 1);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void swap(int* a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                        static void quick(int* a, int lo, int hi) {  //@rec
                            if (lo >= hi) return;  //@rec
                            swap(a, lo + rand() % (hi - lo + 1), hi);  //@part
                            int p = a[hi], i = lo;  //@part
                            for (int j = lo; j < hi; j++) if (a[j] < p) swap(a, i++, j);  //@part
                            swap(a, i, hi);  //@part
                            quick(a, lo, i - 1);  //@sides
                            quick(a, i + 1, hi);  //@sides
                        }

                        int* sortReadings(int* readings, int readingsSize, int* returnSize) {
                            int* a = malloc(readingsSize * sizeof(int));  //@copy
                            memcpy(a, readings, readingsSize * sizeof(int));  //@copy
                            quick(a, 0, readingsSize - 1);  //@ret
                            *returnSize = readingsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("copy", "Work on a copy."), ("rec", "Sort `a[lo..hi]`."), ("part", "Random pivot, then everything strictly smaller moves left. Copies of the pivot all stay on the right side."), ("sides", "Recurse. With many copies, the right side shrinks by only one element per level."), ("ret", "Sort everything.")],
                complexity=["**Time O(n²)** when values repeat heavily (all-equal input peels one element per level). **Space O(n)** recursion depth in that case."],
                limits=["Repeats defeat it: 10⁵ equal readings mean ~5 × 10⁹ comparisons and 10⁵-deep recursion. Grouping the pivot's copies in the middle removes them all at once."],
                slow=True,
            ),
            approach(
                "Three-way quick sort",
                "best",
                "O(n log n) expected",
                "O(log n) expected",
                idea=["Partition `a[lo..hi]` around a random pivot value `p` with three pointers: `a[lo..lt-1] < p`, `a[lt..i-1] = p`, `a[gt+1..hi] > p`, and `i..gt` unseen. Then recurse only on the `< p` and `> p` parts."],
                walk=w2,
                build=["Pick `p` at random; `lt = i = lo`, `gt = hi`.", "While `i ≤ gt`: smaller → swap to `lt`, advance both; bigger → swap with `gt`, shrink `gt`; equal → advance `i`.", "Recurse on `[lo, lt-1]` and `[gt+1, hi]`."],
                code={
                    "python": """
                        import random

                        class Solution:
                            def sortReadings(self, readings: List[int]) -> List[int]:
                                a = readings[:]  #@copy
                                stack = [(0, len(a) - 1)]  #@stack
                                while stack:  #@stack
                                    lo, hi = stack.pop()  #@stack
                                    if lo >= hi:  #@stack
                                        continue  #@stack
                                    p = a[random.randint(lo, hi)]  #@pivot
                                    lt, i, gt = lo, lo, hi  #@pivot
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
                                    stack.append((lo, lt - 1))  #@sides
                                    stack.append((gt + 1, hi))  #@sides
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            private final Random rng = new Random(7);
                            private int[] a;

                            public int[] sortReadings(int[] readings) {
                                a = readings.clone();  //@copy
                                sort(0, a.length - 1);  //@ret
                                return a;  //@ret
                            }

                            private void swap(int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                            private void sort(int lo, int hi) {  //@stack
                                if (lo >= hi) return;  //@stack
                                int p = a[lo + rng.nextInt(hi - lo + 1)];  //@pivot
                                int lt = lo, i = lo, gt = hi;  //@pivot
                                while (i <= gt) {  //@part
                                    if (a[i] < p) swap(lt++, i++);  //@part
                                    else if (a[i] > p) swap(i, gt--);  //@part
                                    else i++;  //@part
                                }
                                sort(lo, lt - 1);  //@sides
                                sort(gt + 1, hi);  //@sides
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a;
                            mt19937 rng{7};

                            void sort(int lo, int hi) {  //@stack
                                if (lo >= hi) return;  //@stack
                                int p = a[lo + rng() % (hi - lo + 1)];  //@pivot
                                int lt = lo, i = lo, gt = hi;  //@pivot
                                while (i <= gt) {  //@part
                                    if (a[i] < p) swap(a[lt++], a[i++]);  //@part
                                    else if (a[i] > p) swap(a[i], a[gt--]);  //@part
                                    else i++;  //@part
                                }
                                sort(lo, lt - 1);  //@sides
                                sort(gt + 1, hi);  //@sides
                            }

                        public:
                            vector<int> sortReadings(vector<int>& readings) {
                                a = readings;  //@copy
                                sort(0, (int) a.size() - 1);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void swap(int* a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@part

                        static void sort3(int* a, int lo, int hi) {  //@stack
                            if (lo >= hi) return;  //@stack
                            int p = a[lo + rand() % (hi - lo + 1)];  //@pivot
                            int lt = lo, i = lo, gt = hi;  //@pivot
                            while (i <= gt) {  //@part
                                if (a[i] < p) swap(a, lt++, i++);  //@part
                                else if (a[i] > p) swap(a, i, gt--);  //@part
                                else i++;  //@part
                            }
                            sort3(a, lo, lt - 1);  //@sides
                            sort3(a, gt + 1, hi);  //@sides
                        }

                        int* sortReadings(int* readings, int readingsSize, int* returnSize) {
                            int* a = malloc(readingsSize * sizeof(int));  //@copy
                            memcpy(a, readings, readingsSize * sizeof(int));  //@copy
                            sort3(a, 0, readingsSize - 1);  //@ret
                            *returnSize = readingsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "Work on a copy."),
                    ("stack", "Ranges still to sort.", {"python": "An explicit stack of ranges instead of recursion (Python's recursion limit is low)."}),
                    ("pivot", "A random pivot value; `lt`, `i` and `gt` mark the three regions."),
                    ("part", "Smaller values go to the front block, bigger ones to the back block, equal ones stay in the middle. A value swapped in from `gt` hasn't been looked at yet, so `i` doesn't advance then."),
                    ("sides", "The equal block `[lt, gt]` is done; only the smaller and bigger parts are sorted further."),
                    ("ret", "Sorted."),
                ],
                complexity=["**Time O(n log n) expected**; with only d distinct values it's closer to O(n log d), since each pass removes a whole value. **Space O(log n)** expected for the pending ranges."],
            ),
        ],
        takeaways=[
            """
            - **Many duplicates → three-way partition** (the "Dutch national flag" split): `< p | = p | > p`.
            - Two-way partitioning degrades to O(n²) on equal keys, which is a classic interview trap.
            - The same three-pointer partition sorts an array of only 0s, 1s and 2s in one pass.
            """
        ],
    )
