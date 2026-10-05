"""Lesson: Quickselect (Sorting, pattern 4)."""
import random

from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

SELECT = {
    "python": """
        import random


        def kth_smallest(nums, k):
            a = list(nums)                                  #@copy
            lo, hi, want = 0, len(a) - 1, k - 1             #@range
            while True:                                     #@loop
                p = random.randint(lo, hi)                  #@pivot
                a[p], a[hi] = a[hi], a[p]                   #@pivot
                store = lo                                  #@part
                for i in range(lo, hi):                     #@part
                    if a[i] < a[hi]:                        #@part
                        a[i], a[store] = a[store], a[i]     #@part
                        store += 1                          #@part
                a[store], a[hi] = a[hi], a[store]           #@part
                if store == want:                           #@found
                    return a[store]                         #@found
                if store < want:                            #@side
                    lo = store + 1                          #@side
                else:                                       #@side
                    hi = store - 1                          #@side
    """,
    "java": """
        static final Random RNG = new Random(7);

        static void swap(int[] a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        static int kthSmallest(int[] nums, int k) {
            int[] a = nums.clone();                         //@copy
            int lo = 0, hi = a.length - 1, want = k - 1;    //@range
            while (true) {                                  //@loop
                swap(a, lo + RNG.nextInt(hi - lo + 1), hi); //@pivot
                int store = lo;                             //@part
                for (int i = lo; i < hi; i++)               //@part
                    if (a[i] < a[hi]) swap(a, i, store++);  //@part
                swap(a, store, hi);                         //@part
                if (store == want) return a[store];         //@found
                if (store < want) lo = store + 1;           //@side
                else hi = store - 1;                        //@side
            }
        }
    """,
    "cpp": """
        mt19937 rng(7);

        int kthSmallest(vector<int> a, int k) {
            int lo = 0, hi = (int)a.size() - 1, want = k - 1;   //@range
            while (true) {                                  //@loop
                swap(a[uniform_int_distribution<int>(lo, hi)(rng)], a[hi]);    //@pivot
                int store = lo;                             //@part
                for (int i = lo; i < hi; i++)               //@part
                    if (a[i] < a[hi]) swap(a[i], a[store++]);   //@part
                swap(a[store], a[hi]);                      //@part
                if (store == want) return a[store];         //@found
                if (store < want) lo = store + 1;           //@side
                else hi = store - 1;                        //@side
            }
        }
    """,
    "c": """
        static void swap(int* a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        int kthSmallest(const int* nums, int n, int k) {
            int* a = malloc(n * sizeof(int));               //@copy
            memcpy(a, nums, n * sizeof(int));               //@copy
            int lo = 0, hi = n - 1, want = k - 1;           //@range
            while (true) {                                  //@loop
                swap(a, lo + rand() % (hi - lo + 1), hi);   //@pivot
                int store = lo;                             //@part
                for (int i = lo; i < hi; i++)               //@part
                    if (a[i] < a[hi]) swap(a, i, store++);  //@part
                swap(a, store, hi);                         //@part
                if (store == want) {                        //@found
                    int answer = a[store];                  //@found
                    free(a);                                //@found
                    return answer;                          //@found
                }
                if (store < want) lo = store + 1;           //@side
                else hi = store - 1;                        //@side
            }
        }
    """,
}
SELECT_RUN = {
    "python": """
        print(kth_smallest([7, 2, 9, 4, 3, 8, 5], 3))
        print(kth_smallest([5, 5, 5, 1], 2))
        print(kth_smallest([42], 1))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(kthSmallest(new int[] {7, 2, 9, 4, 3, 8, 5}, 3));
            System.out.println(kthSmallest(new int[] {5, 5, 5, 1}, 2));
            System.out.println(kthSmallest(new int[] {42}, 1));
        }
    """,
    "cpp": """
        int main() {
            cout << kthSmallest({7, 2, 9, 4, 3, 8, 5}, 3) << "\\n";
            cout << kthSmallest({5, 5, 5, 1}, 2) << "\\n";
            cout << kthSmallest({42}, 1) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            srand(7);
            int a[] = {7, 2, 9, 4, 3, 8, 5}, b[] = {5, 5, 5, 1}, c[] = {42};
            printf("%d\\n%d\\n%d\\n", kthSmallest(a, 7, 3), kthSmallest(b, 4, 2), kthSmallest(c, 1, 1));
            return 0;
        }
    """,
}

THREE = {
    "python": """
        import random


        def kth_smallest_3way(nums, k):
            a = list(nums)                                  #@copy
            lo, hi, want = 0, len(a) - 1, k - 1             #@copy
            while True:                                     #@loop
                pivot = a[random.randint(lo, hi)]           #@pivot
                lt, i, gt = lo, lo, hi                      #@marks
                while i <= gt:                              #@scan
                    if a[i] < pivot:                        #@less
                        a[lt], a[i] = a[i], a[lt]           #@less
                        lt, i = lt + 1, i + 1               #@less
                    elif a[i] > pivot:                      #@more
                        a[i], a[gt] = a[gt], a[i]           #@more
                        gt -= 1                             #@more
                    else:                                   #@same
                        i += 1                              #@same
                if want < lt:                               #@side
                    hi = lt - 1                             #@side
                elif want > gt:                             #@side
                    lo = gt + 1                             #@side
                else:                                       #@found
                    return pivot                            #@found
    """,
    "java": """
        static final Random RNG = new Random(7);

        static void swap(int[] a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        static int kthSmallest3way(int[] nums, int k) {
            int[] a = nums.clone();                         //@copy
            int lo = 0, hi = a.length - 1, want = k - 1;    //@copy
            while (true) {                                  //@loop
                int pivot = a[lo + RNG.nextInt(hi - lo + 1)];   //@pivot
                int lt = lo, i = lo, gt = hi;               //@marks
                while (i <= gt) {                           //@scan
                    if (a[i] < pivot) swap(a, lt++, i++);   //@less
                    else if (a[i] > pivot) swap(a, i, gt--);    //@more
                    else i++;                               //@same
                }
                if (want < lt) hi = lt - 1;                 //@side
                else if (want > gt) lo = gt + 1;            //@side
                else return pivot;                          //@found
            }
        }
    """,
    "cpp": """
        mt19937 rng(7);

        int kthSmallest3way(vector<int> a, int k) {
            int lo = 0, hi = (int)a.size() - 1, want = k - 1;   //@copy
            while (true) {                                  //@loop
                int pivot = a[uniform_int_distribution<int>(lo, hi)(rng)];     //@pivot
                int lt = lo, i = lo, gt = hi;               //@marks
                while (i <= gt) {                           //@scan
                    if (a[i] < pivot) swap(a[lt++], a[i++]);    //@less
                    else if (a[i] > pivot) swap(a[i], a[gt--]); //@more
                    else i++;                               //@same
                }
                if (want < lt) hi = lt - 1;                 //@side
                else if (want > gt) lo = gt + 1;            //@side
                else return pivot;                          //@found
            }
        }
    """,
    "c": """
        static void swap(int* a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        int kthSmallest3way(const int* nums, int n, int k) {
            int* a = malloc(n * sizeof(int));               //@copy
            memcpy(a, nums, n * sizeof(int));               //@copy
            int lo = 0, hi = n - 1, want = k - 1;           //@copy
            while (true) {                                  //@loop
                int pivot = a[lo + rand() % (hi - lo + 1)]; //@pivot
                int lt = lo, i = lo, gt = hi;               //@marks
                while (i <= gt) {                           //@scan
                    if (a[i] < pivot) swap(a, lt++, i++);   //@less
                    else if (a[i] > pivot) swap(a, i, gt--);    //@more
                    else i++;                               //@same
                }
                if (want < lt) hi = lt - 1;                 //@side
                else if (want > gt) lo = gt + 1;            //@side
                else {                                      //@found
                    free(a);                                //@found
                    return pivot;                           //@found
                }
            }
        }
    """,
}
THREE_RUN = {
    "python": """
        print(kth_smallest_3way([3, 1, 3, 3, 2, 3, 3, 0], 6))
        print(kth_smallest_3way([3, 1, 3, 3, 2, 3, 3, 0], 2))
        print(kth_smallest_3way([9] * 50000, 25000))
    """,
    "java": """
        public static void main(String[] args) {
            int[] a = {3, 1, 3, 3, 2, 3, 3, 0}, same = new int[50000];
            Arrays.fill(same, 9);
            System.out.println(kthSmallest3way(a, 6));
            System.out.println(kthSmallest3way(a, 2));
            System.out.println(kthSmallest3way(same, 25000));
        }
    """,
    "cpp": """
        int main() {
            vector<int> a = {3, 1, 3, 3, 2, 3, 3, 0}, same(50000, 9);
            cout << kthSmallest3way(a, 6) << "\\n" << kthSmallest3way(a, 2) << "\\n" << kthSmallest3way(same, 25000) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            srand(7);
            int a[] = {3, 1, 3, 3, 2, 3, 3, 0};
            static int same[50000];
            for (int i = 0; i < 50000; i++) same[i] = 9;
            printf("%d\\n%d\\n%d\\n", kthSmallest3way(a, 8, 6), kthSmallest3way(a, 8, 2), kthSmallest3way(same, 50000, 25000));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

kth_smallest = py(SELECT["python"], "kth_smallest")
kth_smallest_3way = py(THREE["python"], "kth_smallest_3way")

DEMO, K = [7, 2, 9, 4, 3, 8, 5], 3
assert kth_smallest(DEMO, K) == sorted(DEMO)[K - 1] == 4

# Walkthrough with the last value as pivot, so it's easy to follow: one step per comparison.
qw = Steps(f"`kth_smallest({DEMO}, {K})`: the {K}rd smallest, which would sit at index {K - 1} if the array were sorted. (Here the pivot is always the last value in range, to keep it easy to follow.)")
a = list(DEMO)
lo, hi, want = 0, len(a) - 1, K - 1


def qw_state(lo, hi, store, scanned, placed=None):
    st = {k: "dim" for k in range(len(a)) if k < lo or k > hi}
    for k in range(lo, scanned):
        st[k] = "found" if k < store else "mark"
    if placed is None:
        st[hi] = "active"
    else:
        st[placed] = "answer"
    return st


qw.step(f"We want whatever belongs at index {want}. The whole array is still in play.",
        Row(a, ptr={"want": want}, slots=True), M({"range": f"{lo}..{hi}", "pivot": "–", "smaller found": "–"}))
while True:
    pv, store = a[hi], lo
    qw.step(f"Partition {lo}..{hi}. The pivot is its last value, {pv}.",
            Row(list(a), st=qw_state(lo, hi, store, lo), ptr={"want": want, "store": store}, slots=True), M({"range": f"{lo}..{hi}", "pivot": pv, "smaller found": 0}))
    for i in range(lo, hi):
        if a[i] < pv:
            a[i], a[store] = a[store], a[i]
            store += 1
            msg = f"{a[store - 1]} < {pv}: it joins the smaller side" + (f" (swapped into index {store - 1})." if i != store - 1 else ".")
        else:
            msg = f"{a[i]} ≥ {pv}: it stays on the bigger side."
        qw.step(msg, Row(list(a), st=qw_state(lo, hi, store, i + 1), ptr={"want": want, "store": store}, slots=True),
                M({"range": f"{lo}..{hi}", "pivot": pv, "smaller found": store - lo}))
    a[store], a[hi] = a[hi], a[store]
    st = qw_state(lo, hi, store, hi + 1, placed=store)
    if store == want:
        qw.step(f"{pv} goes into index {store}, its final place, and that's exactly the index we want. The answer is {pv}. Nothing else had to be sorted.",
                Row(list(a), st=st, ptr={"want": want, "store": store}, slots=True), M({"range": f"{lo}..{hi}", "pivot": pv, "smaller found": store - lo}), result=pv)
        break
    side = "right" if store < want else "left"
    qw.step(f"{pv} goes into index {store}, its final place. We want index {want}, which is to the {side}, so the other side is never looked at again.",
            Row(list(a), st=st, ptr={"want": want, "store": store}, slots=True), M({"range": f"{lo}..{hi}", "pivot": pv, "smaller found": store - lo}))
    if store < want:
        lo = store + 1
    else:
        hi = store - 1
QW_LEGEND = {"dim": "ruled out", "active": "the pivot", "found": "smaller than the pivot", "mark": "not smaller", "answer": "the pivot in its final place"}

# How the range shrinks on a bigger random run.
rnd = random.Random(11)
BIG = rnd.sample(range(1000), 64)
a, lo, hi, want, SIZES = list(BIG), 0, 63, 31, []
while True:
    SIZES.append(hi - lo + 1)
    p = rnd.randint(lo, hi)
    a[p], a[hi] = a[hi], a[p]
    s = lo
    for i in range(lo, hi):
        if a[i] < a[hi]:
            a[i], a[s] = a[s], a[i]
            s += 1
    a[s], a[hi] = a[hi], a[s]
    if s == want:
        break
    if s < want:
        lo = s + 1
    else:
        hi = s - 1
assert a[want] == sorted(BIG)[want]
WORK = sum(SIZES)


# Comparisons on all-equal input: two-way vs three-way.
def cmp_two(a, want):
    a, lo, hi, c = list(a), 0, len(a) - 1, 0
    while True:
        s = lo
        for i in range(lo, hi):
            c += 1
            if a[i] < a[hi]:
                a[i], a[s] = a[s], a[i]
                s += 1
        a[s], a[hi] = a[hi], a[s]
        if s == want:
            return c
        if s < want:
            lo = s + 1
        else:
            hi = s - 1


def cmp_three(a, want):
    a, lo, hi, c = list(a), 0, len(a) - 1, 0
    while True:
        pv, lt, i, gt = a[hi], lo, lo, hi
        while i <= gt:
            c += 1
            if a[i] < pv:
                a[lt], a[i] = a[i], a[lt]
                lt, i = lt + 1, i + 1
            elif a[i] > pv:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if want < lt:
            hi = lt - 1
        elif want > gt:
            lo = gt + 1
        else:
            return c


EQ_ROWS = [(str(n), str(cmp_two([4] * n, n // 2)), str(cmp_three([4] * n, n // 2))) for n in (100, 1000, 4000)]

# Three-way partition walkthrough.
TW = [3, 5, 1, 3, 4, 3, 0, 3]
assert kth_smallest_3way(TW, 6) == 3
tw = Steps(f"A three-way partition of `{TW}` around 3: smaller values to the left, equal ones in the middle, bigger ones to the right.")
a, lt, i, gt, pv = list(TW), 0, 0, len(TW) - 1, 3


def tw_state():
    return {**{k: "found" for k in range(lt)}, **{k: "answer" for k in range(lt, i)}, **{k: "mark" for k in range(gt + 1, len(a))}}


def tw_vars():
    return M({"smaller": lt - 0, "equal": i - lt, "bigger": len(a) - 1 - gt, "unexamined": max(0, gt - i + 1)})


tw.step("Three markers: before `lt` is smaller than 3, from `lt` up to `i` equals 3, after `gt` is bigger. From `i` to `gt` hasn't been looked at.",
        Row(list(a), ptr={"lt": lt, "i": i, "gt": gt}, slots=True), tw_vars())
while i <= gt:
    v = a[i]
    if v < pv:
        a[lt], a[i] = a[i], a[lt]
        lt, i = lt + 1, i + 1
        msg = f"{v} < 3: swap it to the end of the smaller part; `lt` and `i` both move on."
    elif v > pv:
        a[i], a[gt] = a[gt], a[i]
        gt -= 1
        msg = f"{v} > 3: swap it into the bigger part at `gt`, which moves left. `i` stays, because the value that came back ({a[i]}) hasn't been looked at."
    else:
        i += 1
        msg = "Equal to 3: it's already in the middle part. `i` moves on."
    tw.step(msg, Row(list(a), st=tw_state(), ptr={"lt": lt, "i": i if i < len(a) else None, "gt": gt}, slots=True), tw_vars())
tw.steps[-1]["text"] += f" Done. Indices {lt} to {gt} all hold 3, so any k from {lt + 1} to {gt + 1} is answered at once."
TW_LT, TW_GT = lt, gt

lesson(
    "sorting",
    "quickselect",
    """
    To find the k-th smallest value you don't need to sort everything. Partition around a pivot as quick sort does:
    the pivot lands in its final sorted position. If that's position k, you're done; otherwise the answer is on one
    side, so throw the other side away and repeat. On average that's O(n), not O(n log n).
    """,
    [
        ("idea", "The idea", [
            """
            Say a class of 30 students lines up by height, and you only want to know who would be 10th shortest. Sorting
            the whole line is overkill. Pick any student, say Ravi, and send everyone shorter than him to the left and
            everyone taller to the right. If 12 students went left, Ravi is 13th, and the 10th shortest must be among those
            12 on the left. The 17 on the right can go home. Now do the same with just the 12.

            Each round sends part of the class home, and on average about half. So the total work is roughly
            `30 + 15 + 8 + 4 + …`, which is less than `2 × 30`. Sorting everyone would cost far more.

            That's **quickselect**: quick sort's partition, but recursing into only the side that holds the answer.
            """,
            fig(Bars(SIZES, labels=list(range(1, len(SIZES) + 1)), label=f"values still in play, round by round (n = {len(BIG)}, looking for the median)"),
                caption=f"A real run: {len(SIZES)} rounds, {WORK} values looked at in total, compared with about {round(len(BIG) * 6)} for a full sort."),
            key("""
            Want index `k - 1` of the sorted order. Partition `[lo, hi]` around a random pivot; it lands at `p`. If
            `p == k - 1`, return it. If `p < k - 1`, search `[p + 1, hi]`; otherwise `[lo, p - 1]`. Expected O(n).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            "The k-th smallest (or largest)", "the median", "the top k" or "the k closest", when you don't need them in
            order and don't want to pay for a full sort. Phrases like "in O(n) on average" or "faster than sorting" point
            here too.

            Converting the question:

            - The k-th largest of `n` values is the `(n - k + 1)`-th smallest.
            - The median of an odd number of values is the `(n + 1) / 2`-th smallest.
            - For the k smallest in any order, select the k-th. The first `k` positions of the array then hold the `k`
              smallest values (unordered), because every partition put smaller values to the left.

            Not a fit:

            - You need the top k *in order* and `k` is close to `n`: just sort.
            - Values arrive one at a time and you need the k-th after each one: keep a heap of size `k` (Heaps topic).
            - Many questions about different `k` on the same data: sort once, then each answer is an index.
            """,
            table(["approach", "time", "best when"],
                  ["sort, then index", "O(n log n)", "several k on the same data"],
                  ["heap of size k", "O(n log k)", "k is small, or data arrives as a stream"],
                  ["quickselect", "O(n) on average", "one k, all data available, order of the rest doesn't matter"]),
        ]),
        ("theory", "Why it works", [
            """
            ### The pivot lands in its final position

            After a partition, every value left of the pivot is smaller and every value right of it is not. So the pivot
            sits exactly where it would in the sorted array, and the values on each side are the right *set*, even though
            they're in a jumble. If the pivot is at index `p` and we want index `k - 1`:

            - `p == k - 1`: the pivot is the answer;
            - `p < k - 1`: the answer is one of the values right of `p`, and those values keep their positions relative
              to the whole array, so we keep looking for index `k - 1` there;
            - `p > k - 1`: likewise on the left.

            The target index never changes; only the range around it shrinks.

            ### Why it's O(n) on average

            With a random pivot, the expected size of the side we keep is at most about three quarters of the range.
            So the expected work is at most `n + ¾n + (¾)²n + …`, a geometric series that adds up to `4n`. A finer count
            gives about `3.4n` comparisons to find the median, and less for k near either end. Either way it's linear,
            whereas sorting is `n log n`.

            ### The worst case, and the guarantee

            Unlucky pivots (always the smallest or largest in range) shrink the range by one each time, which is O(n²).
            Random pivots make that astronomically unlikely. If you need a *guaranteed* O(n), the "median of medians"
            method picks the pivot by splitting the values into groups of 5, taking each group's median, and recursively
            selecting the median of those. That pivot always keeps at least 30% of the values out of each side. It's
            slower in practice and rarely asked for in interviews, but it's good to know it exists.

            ### Repeated values

            With many equal values, the two-way partition puts every value equal to the pivot on the same side, just as
            in quick sort, and the range shrinks by one each round. Counting comparisons on arrays where every value is
            the same:
            """,
            table(["n (all values equal)", "two-way partition", "three-way partition"], *EQ_ROWS),
            """
            A three-way partition groups the values equal to the pivot in the middle. If the target index falls among
            them, the answer is the pivot, and you stop at once.
            """,
        ]),
        ("template", "The template", [
            "The k-th smallest value (k counts from 1), on a copy so the caller's array is left alone.",
            code(
                "Quickselect",
                SELECT,
                [
                    ("copy", "Work on a copy: quickselect rearranges the array."),
                    ("range", "The part still in play, and the sorted index we want (k is 1-based, indices are 0-based).",
                     {"cpp": "Taking `a` by value already made the copy."}),
                    ("loop", "Each round partitions the range and keeps one side. A valid `k` guarantees the loop ends."),
                    ("pivot", "A random pivot, parked at the end of the range."),
                    ("part", "The same partition as in quick sort: smaller values to the left, then the pivot into its final "
                             "position `store`."),
                    ("found", "The pivot landed on the index we want: that's the answer.",
                     {"c": "Free the copy before returning."}),
                    ("side", "Otherwise keep only the side that contains the wanted index."),
                ],
                SELECT_RUN,
                "kth_smallest([7, 2, 9, 4, 3, 8, 5], 3); ([5, 5, 5, 1], 2); ([42], 1)",
            ),
        ]),
        ("trace", "Trace it by hand", [
            "Grey values have been ruled out. Notice that the target index never moves:",
            walk(qw, legend=QW_LEGEND),
        ]),
        ("examples", "More examples", [
            f"""
            ### The k-th largest

            The 2nd largest of `{DEMO}` is the 6th smallest (`7 - 2 + 1`). Converting at the start keeps the template
            unchanged, and avoids the classic off-by-one of mixing "from the top" and "from the bottom".

            ### The k smallest, not just the k-th

            After `kth_smallest` (on the array itself rather than a copy), positions `0` to `k - 1` hold the `k` smallest
            values, in no particular order. If you need them sorted, sort just those `k`: O(n + k log k) in total. If the
            items are records, partition by whatever value defines "smallest", such as a distance.

            ### Many repeats

            Readings from a sensor often repeat the same few values. Here's the three-way partition on `{TW}`, which
            sorts values into smaller, equal and bigger in one pass:
            """,
            walk(tw, legend={"found": "smaller than 3", "answer": "equal to 3", "mark": "bigger than 3"}),
        ]),
        ("variations", "Variations", [
            """
            ### Three-way quickselect

            The template with a three-way partition (the "Dutch national flag" partition). If the wanted index falls
            inside the block of values equal to the pivot, the pivot is the answer. It's never slower than the two-way
            version by more than a little, and it's much faster when values repeat. The third test below is 50,000
            equal values.
            """,
            code(
                "Quickselect with a three-way partition",
                THREE,
                [
                    ("copy", "A copy, the range, and the wanted index."),
                    ("loop", "One partition per round."),
                    ("pivot", "Pick a random pivot *value*; the three-way partition doesn't need it parked anywhere."),
                    ("marks", "`[lo, lt)` is smaller than the pivot, `[lt, i)` equals it, `(gt, hi]` is bigger, and `[i, gt]` "
                              "is still unexamined."),
                    ("scan", "Until nothing is unexamined."),
                    ("less", "A smaller value swaps to the end of the smaller part. The value it swaps with is equal to the "
                             "pivot (or is itself), so `i` can move on."),
                    ("more", "A bigger value swaps to the bigger part. The value that comes back hasn't been examined, so `i` "
                             "stays put."),
                    ("same", "An equal value is already in the right part."),
                    ("side", "The wanted index is in the smaller part or the bigger part: keep only that one."),
                    ("found", "Otherwise it's in the equal part, and the pivot is the answer.",
                     {"c": "Free the copy before returning."}),
                ],
                THREE_RUN,
                "kth_smallest_3way([3, 1, 3, 3, 2, 3, 3, 0], 6); (same, 2); (50,000 nines, 25,000)",
            ),
            """
            ### Library versions

            C++ has `std::nth_element(first, nth, last)`, which is quickselect (introselect, with a worst-case guarantee):
            afterwards `*nth` is the value that would be there if sorted, with smaller values before it and bigger ones
            after. Python has no quickselect, but `heapq.nsmallest(k, items)` and `heapq.nlargest` do the heap version in
            O(n log k). Java's `PriorityQueue` gives you the same heap approach.

            ### Choosing a pivot well

            A random pivot is simplest. "Median of three" (the median of the first, middle and last values) avoids the
            worst case on sorted input without randomness, but adversarial inputs can still beat it. For guarantees, use
            median of medians.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Expected O(n) time with random pivots; O(n²) in the worst case (vanishingly unlikely with random pivots; made
            impossible with median of medians). O(1) extra space for the iterative version working in place, or O(n) if
            you copy the input first.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Sort, then index", "O(n log n)", "O(1) to O(n)"],
                ["Heap of size k", "O(n log k)", "O(k)"],
                ["Quickselect (random pivot)", "O(n) expected, O(n²) worst", "O(1) in place"],
                ["Three-way quickselect", "O(n) expected, fast with repeats", "O(1) in place"],
                ["Median of medians", "O(n) worst case", "O(log n) recursion"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `random.randint(lo, hi)` includes both ends. For one-off answers, `sorted(nums)[k - 1]` is often fast enough
            and hard to get wrong; `heapq.nsmallest(k, nums)[-1]` is the O(n log k) alternative. Write quickselect
            iteratively to stay clear of the recursion limit.

            ### Java

            `new Random(seed).nextInt(bound)` gives `0..bound-1`, so add `lo`. Clone the input if the caller still needs
            its order. `PriorityQueue<Integer>` with a size limit gives the heap approach.

            ### C++

            Prefer `std::nth_element(v.begin(), v.begin() + (k - 1), v.end())` in real code; it's well tested and has a
            worst-case guarantee. `uniform_int_distribution<int>(lo, hi)` includes both ends.

            ### C

            `rand() % (hi - lo + 1)` is good enough for pivots. Copy the input with `malloc` and `memcpy` if it's
            `const`, and `free` it on every return path.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Mixing 1-based `k` with 0-based indices. Convert once (`want = k - 1`) and never again.
            - Converting "k-th largest" wrongly: it's index `n - k` in sorted order (0-based).
            - A fixed pivot (first or last value) on sorted input: O(n²).
            - Many equal values with a two-way partition: O(n²) even with a random pivot.
            - Recursing into *both* sides, which turns quickselect back into quick sort.
            - Forgetting that quickselect rearranges the array. Copy it if the caller cares.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does quickselect only recurse into one side?",
                 "After the partition, the pivot is in its final sorted position, and the wanted index is either the pivot's index or on one side of it. The other side can't contain the answer."),
                ("Why is it O(n) on average, when quick sort is O(n log n)?",
                 "Quick sort works on both sides at every level. Quickselect keeps one side, so the work shrinks geometrically: n + about ¾n + … adds up to a constant times n."),
                ("Which sorted index holds the 3rd largest of 10 values?",
                 "Index 7 (0-based), since the 3rd largest is the 8th smallest."),
                ("After quickselect for k = 4 on the array itself, what do the first four positions hold?",
                 "The four smallest values, in no particular order."),
                ("Why does the three-way partition help when values repeat?",
                 "All values equal to the pivot are grouped in the middle. If the wanted index is among them, you're done; otherwise they're all discarded at once instead of one per round."),
            ),
        ]),
    ],
)
