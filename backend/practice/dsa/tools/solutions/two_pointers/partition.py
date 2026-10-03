"""Two Pointers: partitioning an array into groups."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

C_CMP = """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort
""".strip("\n")


@problem
def three_colours():
    balls = [2, 0, 1, 2, 1, 0, 0]
    want = sorted(balls)

    w1 = Steps("Count each colour, then rewrite the row: all the 0s, then the 1s, then the 2s.")
    c = [balls.count(x) for x in range(3)]
    w1.step(f"Counts: {c[0]} zeros, {c[1]} ones, {c[2]} twos.", Row(balls))
    w1.step(f"Rewrite: {want}.", Row(want), result=str(want))

    w2 = Steps("Three pointers: everything before lo is 0, everything after hi is 2, mid scans the unknown middle.")
    a = balls[:]
    lo, mid, hi = 0, 0, len(a) - 1
    w2.step("Start: the whole row is unknown.", Row(a, ptr={"lo": lo, "mid": mid, "hi": hi}))
    while mid <= hi:
        if a[mid] == 0:
            a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1; why = "0: swap it to the lo side; both move on"
        elif a[mid] == 2:
            a[mid], a[hi] = a[hi], a[mid]; hi -= 1; why = "2: swap it to the hi side; the ball swapped in is unknown, so mid stays"
        else:
            mid += 1; why = "1: already in the middle; mid moves on"
        w2.step(f"a[mid] was {why}.", Row(a, st={**{t: "found" for t in range(lo)}, **{t: "found" for t in range(hi + 1, len(a))}}, ptr={"lo": lo, "mid": min(mid, len(a) - 1), "hi": max(hi, 0)}))
    w2.step(f"Sorted: {a}.", result=str(a))

    sol(
        "three-colours",
        summary="""
            Keep three regions: 0s at the front (before `lo`), 2s at the back (after `hi`), and 1s in between, with `mid`
            scanning the unknown part. A 0 is swapped to `lo`, a 2 to `hi`, a 1 is left alone. One pass, O(1) extra space.
        """,
        question=[
            """
            Sort a row of 0s, 1s and 2s in **one pass**, **without counting**, using O(1) extra space.

            - Only three values exist.
            - **Up to 10⁵ balls.**
            """
        ],
        think=[
            f"""
            `{balls}` → `{want}`.

            Picture the row as four zones: known 0s | known 1s | unknown | known 2s. Look at the first unknown ball. A 1
            just extends the 1s zone. A 0 swaps with the first 1 (at `lo`), growing the 0s zone. A 2 swaps with the last
            unknown ball (at `hi`), growing the 2s zone; the ball that comes back is unknown, so look at it again. Each
            step shrinks the unknown zone by one.
            """,
            fig(Row(balls, label="balls"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Built-in sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort a copy."],
                build=["Copy and sort."],
                code={
                    "python": """
                        class Solution:
                            def sortColours(self, balls: List[int]) -> List[int]:
                                return sorted(balls)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] sortColours(int[] balls) {
                                int[] a = balls.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortColours(vector<int>& balls) {
                                vector<int> a = balls;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a;  //@sort
                            }
                        };
                    """,
                    "c": C_CMP + """

                        int* sortColours(int* balls, int ballsSize, int* returnSize) {
                            int* a = malloc(ballsSize * sizeof(int));  //@sort
                            memcpy(a, balls, ballsSize * sizeof(int));  //@sort
                            qsort(a, ballsSize, sizeof(int), cmp_int);  //@sort
                            *returnSize = ballsSize;  //@sort
                            return a;  //@sort
                        }
                    """,
                },
                lines=[("sort", "A general sort.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Ignores that there are only three values. Counting would be O(n), and the three-pointer partition is O(n) in a single pass."],
            ),
            approach(
                "Count, then rewrite",
                "better",
                "O(n)",
                "O(1)",
                idea=["Count the 0s, 1s and 2s, then write that many of each in order."],
                walk=w1,
                build=["Three counters.", "Rewrite the row."],
                code={
                    "python": """
                        class Solution:
                            def sortColours(self, balls: List[int]) -> List[int]:
                                count = [0, 0, 0]  #@count
                                for b in balls:  #@count
                                    count[b] += 1  #@count
                                return [0] * count[0] + [1] * count[1] + [2] * count[2]  #@write
                    """,
                    "java": """
                        class Solution {
                            public int[] sortColours(int[] balls) {
                                int[] count = new int[3];  //@count
                                for (int b : balls) count[b]++;  //@count
                                int[] out = new int[balls.length];  //@write
                                int w = 0;  //@write
                                for (int c = 0; c < 3; c++) for (int i = 0; i < count[c]; i++) out[w++] = c;  //@write
                                return out;  //@write
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortColours(vector<int>& balls) {
                                int count[3] = {0, 0, 0};  //@count
                                for (int b : balls) count[b]++;  //@count
                                vector<int> out;  //@write
                                for (int c = 0; c < 3; c++) out.insert(out.end(), count[c], c);  //@write
                                return out;  //@write
                            }
                        };
                    """,
                    "c": """
                        int* sortColours(int* balls, int ballsSize, int* returnSize) {
                            int count[3] = {0, 0, 0};  //@count
                            for (int i = 0; i < ballsSize; i++) count[balls[i]]++;  //@count
                            int* out = malloc(ballsSize * sizeof(int));  //@write
                            int w = 0;  //@write
                            for (int c = 0; c < 3; c++) for (int i = 0; i < count[c]; i++) out[w++] = c;  //@write
                            *returnSize = ballsSize;  //@write
                            return out;  //@write
                        }
                    """,
                },
                lines=[("count", "How many balls of each colour."), ("write", "That many 0s, then 1s, then 2s.")],
                complexity=["**Time O(n)** over two passes. **Space O(1)** beyond the output."],
                limits=["Two passes, and it counts, which the task forbids. It also only works because the balls carry no other data: real objects can't be recreated from counts. The three-pointer partition moves the actual items in one pass."],
            ),
            approach(
                "Three pointers (one pass)",
                "best",
                "O(n)",
                "O(1)",
                idea=["`lo = mid = 0`, `hi = n − 1`. While `mid ≤ hi`: a 0 swaps with `a[lo]` (both advance); a 2 swaps with `a[hi]` (`hi` retreats, `mid` stays); a 1 just advances `mid`."],
                walk=w2,
                build=["Copy; three pointers.", "Case on `a[mid]`.", "Stop when `mid` passes `hi`."],
                code={
                    "python": """
                        class Solution:
                            def sortColours(self, balls: List[int]) -> List[int]:
                                a = balls[:]  #@init
                                lo, mid, hi = 0, 0, len(a) - 1  #@init
                                while mid <= hi:  #@loop
                                    if a[mid] == 0:  #@zero
                                        a[lo], a[mid] = a[mid], a[lo]  #@zero
                                        lo += 1  #@zero
                                        mid += 1  #@zero
                                    elif a[mid] == 2:  #@two
                                        a[mid], a[hi] = a[hi], a[mid]  #@two
                                        hi -= 1  #@two
                                    else:  #@one
                                        mid += 1  #@one
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] sortColours(int[] balls) {
                                int[] a = balls.clone();  //@init
                                int lo = 0, mid = 0, hi = a.length - 1;  //@init
                                while (mid <= hi) {  //@loop
                                    if (a[mid] == 0) { int t = a[lo]; a[lo++] = a[mid]; a[mid++] = t; }  //@zero
                                    else if (a[mid] == 2) { int t = a[hi]; a[hi--] = a[mid]; a[mid] = t; }  //@two
                                    else mid++;  //@one
                                }
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortColours(vector<int>& balls) {
                                vector<int> a = balls;  //@init
                                int lo = 0, mid = 0, hi = (int) a.size() - 1;  //@init
                                while (mid <= hi) {  //@loop
                                    if (a[mid] == 0) swap(a[lo++], a[mid++]);  //@zero
                                    else if (a[mid] == 2) swap(a[mid], a[hi--]);  //@two
                                    else mid++;  //@one
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* sortColours(int* balls, int ballsSize, int* returnSize) {
                            int* a = malloc(ballsSize * sizeof(int));  //@init
                            memcpy(a, balls, ballsSize * sizeof(int));  //@init
                            int lo = 0, mid = 0, hi = ballsSize - 1;  //@init
                            while (mid <= hi) {  //@loop
                                if (a[mid] == 0) { int t = a[lo]; a[lo++] = a[mid]; a[mid++] = t; }  //@zero
                                else if (a[mid] == 2) { int t = a[hi]; a[hi--] = a[mid]; a[mid] = t; }  //@two
                                else mid++;  //@one
                            }
                            *returnSize = ballsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "`[0, lo)` holds 0s, `[lo, mid)` 1s, `[mid, hi]` unknown, `(hi, n)` 2s."), ("loop", "Until nothing is unknown."), ("zero", "Swap the 0 with the first 1 (or itself); the ball arriving at `mid` is a known 1, so both advance."), ("two", "Swap the 2 to the back; the ball arriving at `mid` hasn't been looked at, so `mid` stays."), ("one", "A 1 is already in place."), ("ret", "Sorted in one pass.")],
                complexity=["**Time O(n):** each step shrinks the unknown zone. **Space O(1)** beyond the copy."],
            ),
        ],
        takeaways=[
            """
            - **Dutch national flag:** three regions with `lo`, `mid`, `hi`; one pass, O(1) space.
            - After swapping with `hi`, re-examine the incoming element; after swapping with `lo`, it's already known.
            - It's the same three-way partition that makes quick sort handle duplicates.
            """
        ],
    )


@problem
def split_around_a_pivot():
    values, pivot = [9, 12, 5, 10, 3, 10, 14], 10
    want = [x for x in values if x < pivot] + [x for x in values if x == pivot] + [x for x in values if x > pivot]

    w1 = Steps("Sort by group (less = 0, equal = 1, greater = 2) with a stable sort, which keeps the original order inside each group.")
    keys = [0 if x < pivot else (1 if x == pivot else 2) for x in values]
    w1.step("Group of each value.", Row(values), Row(keys, label="group"))
    w1.step(f"Stable sort by group: {want}.", Row(want), result=str(want))

    w2 = Steps("Count the smaller and equal values to know where each group starts, then place every value at its group's next free slot.")
    less = sum(x < pivot for x in values)
    equal = sum(x == pivot for x in values)
    out = ["·"] * len(values)
    a, b, c = 0, less, less + equal
    w2.step(f"{less} values are less than {pivot} and {equal} equal: the groups start at 0, {less} and {less + equal}.", Row(values), Vars(less_at=0, equal_at=less, greater_at=less + equal))
    for x in values:
        if x < pivot:
            out[a] = x; at = a; a += 1
        elif x == pivot:
            out[b] = x; at = b; b += 1
        else:
            out[c] = x; at = c; c += 1
        w2.step(f"Place {x} at {at}.", Row(out, st={at: "new"}, label="output"))
    w2.step(f"Result: {out}.", result=str(want))

    sol(
        "split-around-a-pivot",
        summary="""
            Count how many values are less than and equal to the pivot; that tells you where each group starts in the
            output. Then walk the input once, dropping each value into the next free slot of its group. Every group keeps
            its original order (stable), in O(n).
        """,
        question=[
            """
            Rearrange so values `< pivot` come first, then `= pivot`, then `> pivot`, **keeping the original order inside
            each group**.

            - **Stability is required**, so in-place swapping (the flag partition) won't do: swaps reorder elements.
            - **Up to 10⁵ values.**
            """
        ],
        think=[
            f"""
            `{values}` with pivot {pivot} → `{want}`. 9, 5, 3 stay in that order; so do 12, 14.

            The in-place three-pointer partition would scramble the order inside groups. Instead, since every group's
            final position is known once we count the groups' sizes, each value can go straight to its spot.
            """,
            fig(Row(values, label="values"), Row(want, label="split")),
        ],
        approaches=[
            approach(
                "Stable sort by group",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort the values by a key: 0 for less, 1 for equal, 2 for greater. A stable sort keeps the original order among equal keys."],
                walk=w1,
                build=["Key function.", "Stable sort."],
                code={
                    "python": """
                        class Solution:
                            def splitAround(self, values: List[int], pivot: int) -> List[int]:
                                group = lambda x: 0 if x < pivot else (1 if x == pivot else 2)  #@key
                                return sorted(values, key=group)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] splitAround(int[] values, int pivot) {
                                Integer[] a = Arrays.stream(values).boxed().toArray(Integer[]::new);  //@key
                                Arrays.sort(a, Comparator.comparingInt(x -> x < pivot ? 0 : (x == pivot ? 1 : 2)));  //@sort
                                return Arrays.stream(a).mapToInt(Integer::intValue).toArray();  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> splitAround(vector<int>& values, int pivot) {
                                auto group = [pivot](int x) { return x < pivot ? 0 : (x == pivot ? 1 : 2); };  //@key
                                vector<int> a = values;  //@sort
                                stable_sort(a.begin(), a.end(), [&](int x, int y) { return group(x) < group(y); });  //@sort
                                return a;  //@sort
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int value, group, at; } Item;

                        static int by_group(const void* p, const void* q) {  //@key
                            const Item *a = p, *b = q;  //@key
                            return a->group != b->group ? a->group - b->group : a->at - b->at;  //@key
                        }  //@key

                        int* splitAround(int* values, int valuesSize, int pivot, int* returnSize) {
                            Item* items = malloc(valuesSize * sizeof(Item));  //@sort
                            for (int i = 0; i < valuesSize; i++)  //@sort
                                items[i] = (Item){values[i], values[i] < pivot ? 0 : (values[i] == pivot ? 1 : 2), i};  //@sort
                            qsort(items, valuesSize, sizeof(Item), by_group);  //@sort
                            int* out = malloc(valuesSize * sizeof(int));  //@sort
                            for (int i = 0; i < valuesSize; i++) out[i] = items[i].value;  //@sort
                            free(items);  //@sort
                            *returnSize = valuesSize;  //@sort
                            return out;  //@sort
                        }
                    """,
                },
                lines=[("key", "Each value's group.", {"c": "`qsort` isn't stable, so the original position breaks ties."}), ("sort", "A stable sort by group keeps each group in original order.", {"java": "`Arrays.sort` on objects is stable.", "cpp": "`stable_sort`, not `sort`."})],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Sorting is overkill with only three groups: their sizes fix every value's destination, so one counting pass plus one placing pass suffices."],
            ),
            approach(
                "Count the groups, then place",
                "best",
                "O(n)",
                "O(n)",
                idea=["Count `less` and `equal`. Write pointers start at `0`, `less` and `less + equal`. Walk the values, writing each at its group's pointer and advancing it."],
                walk=w2,
                build=["Count less and equal.", "Three write pointers.", "Place in one pass."],
                code={
                    "python": """
                        class Solution:
                            def splitAround(self, values: List[int], pivot: int) -> List[int]:
                                less = sum(1 for x in values if x < pivot)  #@count
                                equal = sum(1 for x in values if x == pivot)  #@count
                                out = [0] * len(values)  #@starts
                                a, b, c = 0, less, less + equal  #@starts
                                for x in values:  #@place
                                    if x < pivot:  #@place
                                        out[a] = x; a += 1  #@place
                                    elif x == pivot:  #@place
                                        out[b] = x; b += 1  #@place
                                    else:  #@place
                                        out[c] = x; c += 1  #@place
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] splitAround(int[] values, int pivot) {
                                int less = 0, equal = 0;  //@count
                                for (int x : values) { if (x < pivot) less++; else if (x == pivot) equal++; }  //@count
                                int[] out = new int[values.length];  //@starts
                                int a = 0, b = less, c = less + equal;  //@starts
                                for (int x : values) {  //@place
                                    if (x < pivot) out[a++] = x;  //@place
                                    else if (x == pivot) out[b++] = x;  //@place
                                    else out[c++] = x;  //@place
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> splitAround(vector<int>& values, int pivot) {
                                int less = 0, equal = 0;  //@count
                                for (int x : values) { if (x < pivot) less++; else if (x == pivot) equal++; }  //@count
                                vector<int> out(values.size());  //@starts
                                int a = 0, b = less, c = less + equal;  //@starts
                                for (int x : values) {  //@place
                                    if (x < pivot) out[a++] = x;  //@place
                                    else if (x == pivot) out[b++] = x;  //@place
                                    else out[c++] = x;  //@place
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* splitAround(int* values, int valuesSize, int pivot, int* returnSize) {
                            int less = 0, equal = 0;  //@count
                            for (int i = 0; i < valuesSize; i++) { if (values[i] < pivot) less++; else if (values[i] == pivot) equal++; }  //@count
                            int* out = malloc(valuesSize * sizeof(int));  //@starts
                            int a = 0, b = less, c = less + equal;  //@starts
                            for (int i = 0; i < valuesSize; i++) {  //@place
                                if (values[i] < pivot) out[a++] = values[i];  //@place
                                else if (values[i] == pivot) out[b++] = values[i];  //@place
                                else out[c++] = values[i];  //@place
                            }
                            *returnSize = valuesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("count", "Sizes of the first two groups."), ("starts", "Each group's first slot in the output."), ("place", "In input order, each value goes to its group's next slot, so order within a group is kept."), ("ret", "The split list.")],
                complexity=["**Time O(n):** two passes. **Space O(n)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Stable three-way split:** count group sizes, then place with one write pointer per group.
            - The in-place flag partition is O(1) space but **not stable**.
            - Counting group sizes to find destinations is the core of counting sort.
            """
        ],
    )


@problem
def sort_k_colours():
    balls, k = [3, 1, 4, 2, 4, 1, 3, 2], 4
    want = sorted(balls)

    w2 = Steps("Split the colour range in half: move colours 1..mid to the left and mid+1..k to the right with two pointers, then sort each side with its half of the colours.")
    a = balls[:]

    def go(left, right, lo, hi, depth=0):
        if left >= right or lo >= hi:
            return
        mid = (lo + hi) // 2
        i, j = left, right
        while i <= j:
            while i <= j and a[i] <= mid:
                i += 1
            while i <= j and a[j] > mid:
                j -= 1
            if i < j:
                a[i], a[j] = a[j], a[i]
        w2.step(f"Positions {left}..{right}, colours {lo}..{hi}: colours ≤ {mid} to the left ({left}..{j}), the rest to the right.", Row(a, st={**{t: "mark" for t in range(left, j + 1)}, **{t: "active" for t in range(i, right + 1)}}))
        go(left, j, lo, mid)
        go(i, right, mid + 1, hi)
    go(0, len(a) - 1, 1, k)
    w2.step(f"Sorted: {a}.", result=str(a))

    sol(
        "sort-k-colours",
        summary="""
            Partition by **colour range**, not by a pivot element: split colours `lo..hi` at `mid`, move colours `≤ mid` left
            and the rest right with two pointers, then recurse on each side with its half of the colours. Each level is
            O(n) and there are log k levels: O(n log k), with no counting array.
        """,
        question=[
            """
            Sort balls coloured `1..k` in **O(n log k)** without an extra array of size `k` (so no counting sort).

            - **k can be as large as n**, in which case this is just O(n log n) sorting.
            - **Up to 10⁵ balls.**
            """
        ],
        think=[
            f"""
            `{balls}` with k = {k} → `{want}`.

            The three-colour trick partitions around fixed values. Generalise it: split the colour range in half. All
            colours `1..2` must end up left of colours `3..4`, so one two-pointer pass separates them. Each half is then the
            same problem with half as many colours. After log k rounds, each range holds a single colour: sorted.
            """,
            fig(Row(balls, label="balls"), Row(want, label="sorted")),
        ],
        approaches=[
            approach(
                "Comparison sort",
                "brute",
                "O(n log n)",
                "O(n)",
                idea=["Sort with the built-in sort."],
                build=["Copy and sort."],
                code={
                    "python": """
                        class Solution:
                            def sortKColours(self, balls: List[int], k: int) -> List[int]:
                                return sorted(balls)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] sortKColours(int[] balls, int k) {
                                int[] a = balls.clone();  //@sort
                                Arrays.sort(a);  //@sort
                                return a;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> sortKColours(vector<int>& balls, int k) {
                                vector<int> a = balls;  //@sort
                                sort(a.begin(), a.end());  //@sort
                                return a;  //@sort
                            }
                        };
                    """,
                    "c": C_CMP + """

                        int* sortKColours(int* balls, int ballsSize, int k, int* returnSize) {
                            int* a = malloc(ballsSize * sizeof(int));  //@sort
                            memcpy(a, balls, ballsSize * sizeof(int));  //@sort
                            qsort(a, ballsSize, sizeof(int), cmp_int);  //@sort
                            *returnSize = ballsSize;  //@sort
                            return a;  //@sort
                        }
                    """,
                },
                lines=[("sort", "A general sort.")],
                complexity=["**Time O(n log n).** **Space O(n).**"],
                limits=["Doesn't use the small number of colours: with k much smaller than n, splitting the colour range does only log k passes."],
            ),
            approach(
                "Split the colour range in half",
                "best",
                "O(n log k)",
                "O(log k)",
                idea=["`sort(left, right, lo, hi)`: if the range has under 2 balls or one colour, stop. `mid = (lo + hi) / 2`. Two pointers: `i` skips colours `≤ mid` from the left, `j` skips colours `> mid` from the right; swap when both stop. Recurse on `[left, j]` with colours `lo..mid` and `[i, right]` with `mid+1..hi`."],
                walk=w2,
                build=["Copy.", "Recursive (or stack-based) range partition.", "Two-pointer split around the colour midpoint."],
                code={
                    "python": """
                        class Solution:
                            def sortKColours(self, balls: List[int], k: int) -> List[int]:
                                a = balls[:]  #@init
                                stack = [(0, len(a) - 1, 1, k)]  #@init
                                while stack:  #@loop
                                    left, right, lo, hi = stack.pop()  #@loop
                                    if left >= right or lo >= hi:  #@loop
                                        continue  #@loop
                                    mid = (lo + hi) // 2  #@split
                                    i, j = left, right  #@split
                                    while i <= j:  #@split
                                        while i <= j and a[i] <= mid:  #@split
                                            i += 1  #@split
                                        while i <= j and a[j] > mid:  #@split
                                            j -= 1  #@split
                                        if i < j:  #@split
                                            a[i], a[j] = a[j], a[i]  #@split
                                    stack.append((left, j, lo, mid))  #@halves
                                    stack.append((i, right, mid + 1, hi))  #@halves
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] a;

                            public int[] sortKColours(int[] balls, int k) {
                                a = balls.clone();  //@init
                                sort(0, a.length - 1, 1, k);  //@init
                                return a;  //@ret
                            }

                            private void sort(int left, int right, int lo, int hi) {  //@loop
                                if (left >= right || lo >= hi) return;  //@loop
                                int mid = (lo + hi) / 2, i = left, j = right;  //@split
                                while (i <= j) {  //@split
                                    while (i <= j && a[i] <= mid) i++;  //@split
                                    while (i <= j && a[j] > mid) j--;  //@split
                                    if (i < j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@split
                                }
                                sort(left, j, lo, mid);  //@halves
                                sort(i, right, mid + 1, hi);  //@halves
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            vector<int> a;

                            void sort(int left, int right, int lo, int hi) {  //@loop
                                if (left >= right || lo >= hi) return;  //@loop
                                int mid = (lo + hi) / 2, i = left, j = right;  //@split
                                while (i <= j) {  //@split
                                    while (i <= j && a[i] <= mid) i++;  //@split
                                    while (i <= j && a[j] > mid) j--;  //@split
                                    if (i < j) swap(a[i], a[j]);  //@split
                                }
                                sort(left, j, lo, mid);  //@halves
                                sort(i, right, mid + 1, hi);  //@halves
                            }

                        public:
                            vector<int> sortKColours(vector<int>& balls, int k) {
                                a = balls;  //@init
                                sort(0, (int) a.size() - 1, 1, k);  //@init
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void sort_range(int* a, int left, int right, int lo, int hi) {  //@loop
                            if (left >= right || lo >= hi) return;  //@loop
                            int mid = (lo + hi) / 2, i = left, j = right;  //@split
                            while (i <= j) {  //@split
                                while (i <= j && a[i] <= mid) i++;  //@split
                                while (i <= j && a[j] > mid) j--;  //@split
                                if (i < j) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@split
                            }
                            sort_range(a, left, j, lo, mid);  //@halves
                            sort_range(a, i, right, mid + 1, hi);  //@halves
                        }

                        int* sortKColours(int* balls, int ballsSize, int k, int* returnSize) {
                            int* a = malloc(ballsSize * sizeof(int));  //@init
                            memcpy(a, balls, ballsSize * sizeof(int));  //@init
                            sort_range(a, 0, ballsSize - 1, 1, k);  //@init
                            *returnSize = ballsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "A copy; start with all positions and all colours `1..k`.", {"python": "An explicit stack of (positions, colours) ranges instead of recursion."}),
                    ("loop", "A range with fewer than two balls, or only one colour, is already sorted."),
                    ("split", "Split the colours at `mid`. `i` skips balls that belong left, `j` skips balls that belong right; when both stop, the two balls are on the wrong sides, so swap. Afterwards `[left, j]` holds colours `≤ mid` and `[i, right]` the rest."),
                    ("halves", "Each side has half the colours: the recursion depth is log k."),
                    ("ret", "Sorted."),
                ],
                complexity=["**Time O(n log k):** every level of colour-halving touches each ball once. **Space O(log k)** for the recursion (or the stack)."],
            ),
        ],
        takeaways=[
            """
            - **Partition by value range** (binary search on the colours) generalises the three-colour flag to k colours.
            - O(n log k) beats O(n log n) when k ≪ n, without a counting array.
            - With O(k) extra space allowed, counting sort would be O(n + k).
            """
        ],
    )


@problem
def fewest_swaps_three_colours():
    balls = [2, 0, 1, 0, 2, 1, 0]
    target = sorted(balls)
    c = [[0] * 3 for _ in range(3)]
    for have, want_ in zip(balls, target):
        c[have][want_] += 1
    moves, cc = 0, [row[:] for row in c]
    for a in range(3):
        for b in range(a + 1, 3):
            m = min(cc[a][b], cc[b][a]); moves += m; cc[a][b] -= m; cc[b][a] -= m
    left = sum(cc[a][b] for a in range(3) for b in range(3) if a != b)
    want = moves + 2 * left // 3

    w = Steps("Compare the row with its sorted version. Count misplaced balls by (colour it is, colour the slot needs).")
    w.step(f"Sorted target: {target}.", Row(balls, st={i: "mark" for i in range(len(balls)) if balls[i] != target[i]}, label="now"), Row(target, label="target"))
    w.step("Misplaced counts: a 'have a, need b' ball and a 'have b, need a' ball fix each other with one swap.", Vars(**{f"{a}→{b}": c[a][b] for a in range(3) for b in range(3) if a != b}))
    w.step(f"Direct pair swaps: {moves}. {left} misplaced balls remain; they form 3-cycles (0→1→2→0), each fixed with 2 swaps: {2 * left // 3}.", Vars(pair_swaps=moves, cycle_swaps=2 * left // 3))
    w.step(f"Fewest moves: {want}.", result=want)

    sol(
        "fewest-swaps-three-colours",
        summary="""
            Compare each position with the sorted row and count misplaced balls by type: "a 1 sitting where a 0 belongs",
            and so on. Two balls that are in each other's places are fixed by one swap, so pair those up first. Whatever is
            left forms 3-cycles (0 → 1 → 2 → 0), and each 3-cycle needs exactly 2 swaps. O(n).
        """,
        question=[
            """
            Any two balls may be swapped. Find the fewest swaps to arrange the row as 0s, then 1s, then 2s.

            - **Swaps aren't limited to neighbours**, unlike counting inversions.
            - **Up to 10⁵ balls.**
            """
        ],
        think=[
            f"""
            `{balls}` must become `{target}`, which takes **{want}** swaps.

            Only misplaced balls matter. Label each by what it is and what its slot needs: a "1 in a 0-slot" and a "0 in a
            1-slot" swap with each other and both become correct: the best possible, two fixes per swap. After using all
            such pairs, the leftovers can't pair up, so they chase each other in cycles of three (a 0 in a 1-slot, a 1 in
            a 2-slot, a 2 in a 0-slot), and any 3-cycle needs 2 swaps for 3 balls.
            """,
            fig(Row(balls, label="now"), Row(target, label="target")),
        ],
        approaches=[
            approach(
                "Count misplacements, pair them, then cycles",
                "best",
                "O(n)",
                "O(1)",
                idea=["Count the sorted target with three counters (no full sort needed: the first `n0` slots need 0, the next `n1` need 1). Tally `c[have][need]` for misplaced balls. Swaps = Σ min(c[a][b], c[b][a]) over pairs, plus 2 × (remaining misplaced) / 3."],
                walk=w,
                build=["Count colours to know each slot's target.", "Tally `c[have][need]`.", "Pair swaps, then 3-cycles."],
                code={
                    "python": """
                        class Solution:
                            def minSwapsThreeColours(self, balls: List[int]) -> int:
                                n0, n1 = balls.count(0), balls.count(1)  #@target
                                c = [[0] * 3 for _ in range(3)]  #@tally
                                for i, b in enumerate(balls):  #@tally
                                    need = 0 if i < n0 else (1 if i < n0 + n1 else 2)  #@tally
                                    c[b][need] += 1  #@tally
                                moves = 0  #@pairs
                                for a in range(3):  #@pairs
                                    for b in range(a + 1, 3):  #@pairs
                                        m = min(c[a][b], c[b][a])  #@pairs
                                        moves += m  #@pairs
                                        c[a][b] -= m  #@pairs
                                        c[b][a] -= m  #@pairs
                                left = c[0][1] + c[0][2] + c[1][0] + c[1][2] + c[2][0] + c[2][1]  #@cycles
                                return moves + 2 * left // 3  #@cycles
                    """,
                    "java": """
                        class Solution {
                            public int minSwapsThreeColours(int[] balls) {
                                int n0 = 0, n1 = 0;  //@target
                                for (int b : balls) { if (b == 0) n0++; else if (b == 1) n1++; }  //@target
                                int[][] c = new int[3][3];  //@tally
                                for (int i = 0; i < balls.length; i++) {  //@tally
                                    int need = i < n0 ? 0 : (i < n0 + n1 ? 1 : 2);  //@tally
                                    c[balls[i]][need]++;  //@tally
                                }
                                int moves = 0;  //@pairs
                                for (int a = 0; a < 3; a++)  //@pairs
                                    for (int b = a + 1; b < 3; b++) {  //@pairs
                                        int m = Math.min(c[a][b], c[b][a]);  //@pairs
                                        moves += m;  //@pairs
                                        c[a][b] -= m;  //@pairs
                                        c[b][a] -= m;  //@pairs
                                    }
                                int left = c[0][1] + c[0][2] + c[1][0] + c[1][2] + c[2][0] + c[2][1];  //@cycles
                                return moves + 2 * left / 3;  //@cycles
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minSwapsThreeColours(vector<int>& balls) {
                                int n0 = count(balls.begin(), balls.end(), 0), n1 = count(balls.begin(), balls.end(), 1);  //@target
                                int c[3][3] = {};  //@tally
                                for (int i = 0; i < (int) balls.size(); i++) {  //@tally
                                    int need = i < n0 ? 0 : (i < n0 + n1 ? 1 : 2);  //@tally
                                    c[balls[i]][need]++;  //@tally
                                }
                                int moves = 0;  //@pairs
                                for (int a = 0; a < 3; a++)  //@pairs
                                    for (int b = a + 1; b < 3; b++) {  //@pairs
                                        int m = min(c[a][b], c[b][a]);  //@pairs
                                        moves += m;  //@pairs
                                        c[a][b] -= m;  //@pairs
                                        c[b][a] -= m;  //@pairs
                                    }
                                int left = c[0][1] + c[0][2] + c[1][0] + c[1][2] + c[2][0] + c[2][1];  //@cycles
                                return moves + 2 * left / 3;  //@cycles
                            }
                        };
                    """,
                    "c": """
                        int minSwapsThreeColours(int* balls, int ballsSize) {
                            int n0 = 0, n1 = 0;  //@target
                            for (int i = 0; i < ballsSize; i++) { if (balls[i] == 0) n0++; else if (balls[i] == 1) n1++; }  //@target
                            int c[3][3] = {{0}};  //@tally
                            for (int i = 0; i < ballsSize; i++) {  //@tally
                                int need = i < n0 ? 0 : (i < n0 + n1 ? 1 : 2);  //@tally
                                c[balls[i]][need]++;  //@tally
                            }
                            int moves = 0;  //@pairs
                            for (int a = 0; a < 3; a++)  //@pairs
                                for (int b = a + 1; b < 3; b++) {  //@pairs
                                    int m = c[a][b] < c[b][a] ? c[a][b] : c[b][a];  //@pairs
                                    moves += m;  //@pairs
                                    c[a][b] -= m;  //@pairs
                                    c[b][a] -= m;  //@pairs
                                }
                            int left = c[0][1] + c[0][2] + c[1][0] + c[1][2] + c[2][0] + c[2][1];  //@cycles
                            return moves + 2 * left / 3;  //@cycles
                        }
                    """,
                },
                lines=[
                    ("target", "How many 0s and 1s there are: the sorted row has 0s in `[0, n0)`, 1s in `[n0, n0+n1)`, 2s after."),
                    ("tally", "`c[have][need]` counts balls of colour `have` sitting in a slot that needs `need` (the diagonal is correct balls)."),
                    ("pairs", "An `a` in a `b`-slot and a `b` in an `a`-slot swap with each other: one swap, two balls fixed."),
                    ("cycles", "What's left forms 3-cycles in equal numbers, so `left` is a multiple of 3; each cycle of 3 balls takes 2 swaps."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Minimum arbitrary swaps to sort = n − (number of cycles)** in the misplacement graph; with few values, count
              2-cycles and 3-cycles directly.
            - Pair up mutual misplacements first: each swap fixes two items.
            - Neighbour-only swaps are a different problem (count inversions instead).
            """
        ],
    )
