"""Lesson: Merge sort and quick sort (Sorting, pattern 1)."""
from lesson import Bars, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

MERGE = {
    "python": """
        def sort_range(a, buf, lo, hi):
            if hi - lo < 2:                             #@base
                return                                  #@base
            mid = (lo + hi) // 2                        #@split
            sort_range(a, buf, lo, mid)                 #@halves
            sort_range(a, buf, mid, hi)                 #@halves
            i, j, k = lo, mid, lo                       #@ptrs
            while i < mid and j < hi:                   #@merge
                if a[i] <= a[j]:                        #@pick
                    buf[k] = a[i]                       #@pick
                    i += 1                              #@pick
                else:                                   #@pick
                    buf[k] = a[j]                       #@pick
                    j += 1                              #@pick
                k += 1                                  #@merge
            while i < mid:                              #@rest
                buf[k] = a[i]                           #@rest
                i, k = i + 1, k + 1                     #@rest
            while j < hi:                               #@rest
                buf[k] = a[j]                           #@rest
                j, k = j + 1, k + 1                     #@rest
            a[lo:hi] = buf[lo:hi]                       #@copy


        def merge_sort(a):
            buf = [0] * len(a)                          #@buf
            sort_range(a, buf, 0, len(a))               #@buf
            return a                                    #@ret
    """,
    "java": """
        static void sortRange(int[] a, int[] buf, int lo, int hi) {
            if (hi - lo < 2) return;                    //@base
            int mid = (lo + hi) >>> 1;                  //@split
            sortRange(a, buf, lo, mid);                 //@halves
            sortRange(a, buf, mid, hi);                 //@halves
            int i = lo, j = mid, k = lo;                //@ptrs
            while (i < mid && j < hi) {                 //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];    //@pick
                else buf[k++] = a[j++];                 //@pick
            }
            while (i < mid) buf[k++] = a[i++];          //@rest
            while (j < hi) buf[k++] = a[j++];           //@rest
            System.arraycopy(buf, lo, a, lo, hi - lo);  //@copy
        }

        static int[] mergeSort(int[] a) {
            sortRange(a, new int[a.length], 0, a.length);   //@buf
            return a;                                   //@ret
        }
    """,
    "cpp": """
        void sortRange(vector<int>& a, vector<int>& buf, int lo, int hi) {
            if (hi - lo < 2) return;                    //@base
            int mid = lo + (hi - lo) / 2;               //@split
            sortRange(a, buf, lo, mid);                 //@halves
            sortRange(a, buf, mid, hi);                 //@halves
            int i = lo, j = mid, k = lo;                //@ptrs
            while (i < mid && j < hi) {                 //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];    //@pick
                else buf[k++] = a[j++];                 //@pick
            }
            while (i < mid) buf[k++] = a[i++];          //@rest
            while (j < hi) buf[k++] = a[j++];           //@rest
            copy(buf.begin() + lo, buf.begin() + hi, a.begin() + lo);  //@copy
        }

        vector<int>& mergeSort(vector<int>& a) {
            vector<int> buf(a.size());                  //@buf
            sortRange(a, buf, 0, a.size());             //@buf
            return a;                                   //@ret
        }
    """,
    "c": """
        static void sortRange(int* a, int* buf, int lo, int hi) {
            if (hi - lo < 2) return;                    //@base
            int mid = lo + (hi - lo) / 2;               //@split
            sortRange(a, buf, lo, mid);                 //@halves
            sortRange(a, buf, mid, hi);                 //@halves
            int i = lo, j = mid, k = lo;                //@ptrs
            while (i < mid && j < hi) {                 //@merge
                if (a[i] <= a[j]) buf[k++] = a[i++];    //@pick
                else buf[k++] = a[j++];                 //@pick
            }
            while (i < mid) buf[k++] = a[i++];          //@rest
            while (j < hi) buf[k++] = a[j++];           //@rest
            memcpy(a + lo, buf + lo, (hi - lo) * sizeof(int));  //@copy
        }

        void mergeSort(int* a, int n) {
            int* buf = malloc((n > 0 ? n : 1) * sizeof(int));   //@buf
            sortRange(a, buf, 0, n);                    //@buf
            free(buf);                                  //@ret
        }
    """,
}
MERGE_RUN = {
    "python": """
        print(*merge_sort([38, 27, 43, 3, 9, 82, 10]))
        print(*merge_sort([5, 1, 5, 1]))
        print(*merge_sort([7]))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(mergeSort(new int[] {38, 27, 43, 3, 9, 82, 10}));
            show(mergeSort(new int[] {5, 1, 5, 1}));
            show(mergeSort(new int[] {7}));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            vector<int> a = {38, 27, 43, 3, 9, 82, 10}, b = {5, 1, 5, 1}, c = {7};
            show(mergeSort(a));
            show(mergeSort(b));
            show(mergeSort(c));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            int a[] = {38, 27, 43, 3, 9, 82, 10}, b[] = {5, 1, 5, 1}, c[] = {7};
            mergeSort(a, 7);
            mergeSort(b, 4);
            mergeSort(c, 1);
            show(a, 7);
            show(b, 4);
            show(c, 1);
            return 0;
        }
    """,
}

QUICK = {
    "python": """
        import random


        def partition(a, lo, hi):
            p = random.randint(lo, hi)                  #@pivot
            a[p], a[hi] = a[hi], a[p]                   #@pivot
            pivot = a[hi]                               #@pivot
            store = lo                                  #@store
            for i in range(lo, hi):                     #@scan
                if a[i] < pivot:                        #@small
                    a[i], a[store] = a[store], a[i]     #@small
                    store += 1                          #@small
            a[store], a[hi] = a[hi], a[store]           #@place
            return store                                #@place


        def quick_range(a, lo, hi):
            while lo < hi:                              #@loop
                p = partition(a, lo, hi)                #@part
                if p - lo < hi - p:                     #@smaller
                    quick_range(a, lo, p - 1)           #@smaller
                    lo = p + 1                          #@smaller
                else:                                   #@smaller
                    quick_range(a, p + 1, hi)           #@smaller
                    hi = p - 1                          #@smaller


        def quick_sort(a):
            quick_range(a, 0, len(a) - 1)               #@start
            return a                                    #@start
    """,
    "java": """
        static final Random RNG = new Random(7);

        static void swap(int[] a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        static int partition(int[] a, int lo, int hi) {
            swap(a, lo + RNG.nextInt(hi - lo + 1), hi); //@pivot
            int pivot = a[hi];                          //@pivot
            int store = lo;                             //@store
            for (int i = lo; i < hi; i++)               //@scan
                if (a[i] < pivot) swap(a, i, store++);  //@small
            swap(a, store, hi);                         //@place
            return store;                               //@place
        }

        static void quickRange(int[] a, int lo, int hi) {
            while (lo < hi) {                           //@loop
                int p = partition(a, lo, hi);           //@part
                if (p - lo < hi - p) {                  //@smaller
                    quickRange(a, lo, p - 1);           //@smaller
                    lo = p + 1;                         //@smaller
                } else {                                //@smaller
                    quickRange(a, p + 1, hi);           //@smaller
                    hi = p - 1;                         //@smaller
                }
            }
        }

        static int[] quickSort(int[] a) {
            quickRange(a, 0, a.length - 1);             //@start
            return a;                                   //@start
        }
    """,
    "cpp": """
        mt19937 rng(7);

        int partition(vector<int>& a, int lo, int hi) {
            swap(a[uniform_int_distribution<int>(lo, hi)(rng)], a[hi]);    //@pivot
            int pivot = a[hi];                          //@pivot
            int store = lo;                             //@store
            for (int i = lo; i < hi; i++)               //@scan
                if (a[i] < pivot) swap(a[i], a[store++]);   //@small
            swap(a[store], a[hi]);                      //@place
            return store;                               //@place
        }

        void quickRange(vector<int>& a, int lo, int hi) {
            while (lo < hi) {                           //@loop
                int p = partition(a, lo, hi);           //@part
                if (p - lo < hi - p) {                  //@smaller
                    quickRange(a, lo, p - 1);           //@smaller
                    lo = p + 1;                         //@smaller
                } else {                                //@smaller
                    quickRange(a, p + 1, hi);           //@smaller
                    hi = p - 1;                         //@smaller
                }
            }
        }

        vector<int>& quickSort(vector<int>& a) {
            quickRange(a, 0, (int)a.size() - 1);        //@start
            return a;                                   //@start
        }
    """,
    "c": """
        static void swap(int* a, int i, int j) {
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }

        static int partition(int* a, int lo, int hi) {
            swap(a, lo + rand() % (hi - lo + 1), hi);   //@pivot
            int pivot = a[hi];                          //@pivot
            int store = lo;                             //@store
            for (int i = lo; i < hi; i++)               //@scan
                if (a[i] < pivot) swap(a, i, store++);  //@small
            swap(a, store, hi);                         //@place
            return store;                               //@place
        }

        static void quickRange(int* a, int lo, int hi) {
            while (lo < hi) {                           //@loop
                int p = partition(a, lo, hi);           //@part
                if (p - lo < hi - p) {                  //@smaller
                    quickRange(a, lo, p - 1);           //@smaller
                    lo = p + 1;                         //@smaller
                } else {                                //@smaller
                    quickRange(a, p + 1, hi);           //@smaller
                    hi = p - 1;                         //@smaller
                }
            }
        }

        void quickSort(int* a, int n) {
            quickRange(a, 0, n - 1);                    //@start
        }
    """,
}
QUICK_RUN = {
    "python": """
        print(*quick_sort([7, 2, 9, 4, 3, 8, 5]))
        print(*quick_sort([4, 4, 1, 4, 0]))
        print(*quick_sort(list(range(10, 0, -1))))
    """,
    "java": """
        static void show(int[] a) {
            StringBuilder sb = new StringBuilder();
            for (int x : a) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }

        public static void main(String[] args) {
            show(quickSort(new int[] {7, 2, 9, 4, 3, 8, 5}));
            show(quickSort(new int[] {4, 4, 1, 4, 0}));
            show(quickSort(new int[] {10, 9, 8, 7, 6, 5, 4, 3, 2, 1}));
        }
    """,
    "cpp": """
        void show(const vector<int>& a) {
            for (size_t i = 0; i < a.size(); i++) cout << (i ? " " : "") << a[i];
            cout << "\\n";
        }

        int main() {
            vector<int> a = {7, 2, 9, 4, 3, 8, 5}, b = {4, 4, 1, 4, 0}, c = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
            show(quickSort(a));
            show(quickSort(b));
            show(quickSort(c));
        }
    """,
    "c": """
        static void show(const int* a, int n) {
            for (int i = 0; i < n; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
        }

        int main(void) {
            srand(7);
            int a[] = {7, 2, 9, 4, 3, 8, 5}, b[] = {4, 4, 1, 4, 0}, c[] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
            quickSort(a, 7);
            quickSort(b, 5);
            quickSort(c, 10);
            show(a, 7);
            show(b, 5);
            show(c, 10);
            return 0;
        }
    """,
}

INSERT = {
    "python": """
        def insertion_sort(a):
            for i in range(1, len(a)):                  #@each
                x = a[i]                                #@take
                j = i - 1                               #@shift
                while j >= 0 and a[j] > x:              #@shift
                    a[j + 1] = a[j]                     #@shift
                    j -= 1                              #@shift
                a[j + 1] = x                            #@drop
            return a                                    #@ret
    """,
    "java": """
        static int[] insertionSort(int[] a) {
            for (int i = 1; i < a.length; i++) {        //@each
                int x = a[i];                           //@take
                int j = i - 1;                          //@shift
                while (j >= 0 && a[j] > x) {            //@shift
                    a[j + 1] = a[j];                    //@shift
                    j--;                                //@shift
                }
                a[j + 1] = x;                           //@drop
            }
            return a;                                   //@ret
        }
    """,
    "cpp": """
        vector<int>& insertionSort(vector<int>& a) {
            for (int i = 1; i < (int)a.size(); i++) {   //@each
                int x = a[i];                           //@take
                int j = i - 1;                          //@shift
                while (j >= 0 && a[j] > x) {            //@shift
                    a[j + 1] = a[j];                    //@shift
                    j--;                                //@shift
                }
                a[j + 1] = x;                           //@drop
            }
            return a;                                   //@ret
        }
    """,
    "c": """
        void insertionSort(int* a, int n) {
            for (int i = 1; i < n; i++) {               //@each
                int x = a[i];                           //@take
                int j = i - 1;                          //@shift
                while (j >= 0 && a[j] > x) {            //@shift
                    a[j + 1] = a[j];                    //@shift
                    j--;                                //@shift
                }
                a[j + 1] = x;                           //@drop
            }
        }
    """,
}
INSERT_RUN = {
    "python": """
        print(*insertion_sort([5, 2, 4, 6, 1, 3]))
    """,
    "java": """
        public static void main(String[] args) {
            StringBuilder sb = new StringBuilder();
            for (int x : insertionSort(new int[] {5, 2, 4, 6, 1, 3})) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }
    """,
    "cpp": """
        int main() {
            vector<int> a = {5, 2, 4, 6, 1, 3};
            auto& v = insertionSort(a);
            for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
            cout << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {5, 2, 4, 6, 1, 3};
            insertionSort(a, 6);
            for (int i = 0; i < 6; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

merge_sort = py(MERGE["python"], "merge_sort")
quick_sort = py(QUICK["python"], "quick_sort")
insertion_sort = py(INSERT["python"], "insertion_sort")

DEMO = [38, 27, 43, 3, 9, 82, 10]
SORTED = sorted(DEMO)
assert merge_sort(list(DEMO)) == SORTED and quick_sort(list(DEMO)) == SORTED


def groups_state(sizes):
    """Colour consecutive groups of the given sizes alternately."""
    st, k = {}, 0
    for g, n in enumerate(sizes):
        for _ in range(n):
            st[k] = "found" if g % 2 == 0 else "mark"
            k += 1
    return st


# Levels of the split, top-down, as group sizes.
def split_levels(n):
    levels, cur = [[n]], [n]
    while any(x > 1 for x in cur):
        nxt = []
        for x in cur:
            nxt += [x // 2, x - x // 2] if x > 1 else [x]
        levels.append(nxt)
        cur = nxt
    return levels


LEVELS = split_levels(len(DEMO))


def sorted_by_groups(a, sizes):
    out, k = [], 0
    for n in sizes:
        out += sorted(a[k:k + n])
        k += n
    return out


up_rows = [Row(sorted_by_groups(DEMO, sizes), st=groups_state(sizes), label=f"{len(sizes)} sorted piece{'s' if len(sizes) > 1 else ''}") for sizes in reversed(LEVELS)]

# Merge walkthrough: two sorted halves.
L, R = sorted(DEMO[:3]), sorted(DEMO[3:])
mw = Steps(f"Merging {L} and {R}. Both are sorted, so the smallest remaining value is always at the front of one of them.")
i = j = 0
out = []
mw.step("Two sorted halves and an empty output. `i` and `j` point at the front of each half.",
        Row(L, ptr={"i": 0}, label="left"), Row(R, ptr={"j": 0}, label="right"), Row([None] * (len(L) + len(R)), label="output"))
while i < len(L) and j < len(R):
    if L[i] <= R[j]:
        msg = f"Compare {L[i]} and {R[j]}. {L[i]} is smaller (or equal), so it goes next, and `i` moves on."
        out.append(L[i])
        i += 1
        side = "left"
    else:
        msg = f"Compare {L[i]} and {R[j]}. {R[j]} is smaller, so it goes next, and `j` moves on."
        out.append(R[j])
        j += 1
        side = "right"
    mw.step(msg, Row(L, st={k: "dim" for k in range(i)}, ptr={"i": i if i < len(L) else None}, label="left"),
            Row(R, st={k: "dim" for k in range(j)}, ptr={"j": j if j < len(R) else None}, label="right"),
            Row(out + [None] * (len(L) + len(R) - len(out)), st={len(out) - 1: "new"}, label="output"))
rest = L[i:] + R[j:]
out += rest
mw.step(f"One half has run out. Everything left in the other ({', '.join(map(str, rest))}) is bigger than what's been placed, and already sorted, so copy it across.",
        Row(L, st={k: "dim" for k in range(len(L))}, label="left"), Row(R, st={k: "dim" for k in range(len(R))}, label="right"),
        Row(out, st={k: "new" for k in range(len(out) - len(rest), len(out))}, label="output"), result=" ".join(map(str, out)))
assert out == SORTED

# Partition walkthrough with the last value as pivot (deterministic, for reading).
PD = [7, 2, 9, 4, 3, 8, 5]
pw = Steps(f"Partitioning `{PD}` around its last value, 5. Afterwards everything smaller than 5 is on its left, everything else on its right.")
a = list(PD)
hi, store, pivot = len(a) - 1, 0, a[-1]


def part_state(scanned):
    st = {k: ("found" if k < store else "mark") for k in range(scanned)}
    st[hi] = "active"
    return st


pw.step(f"The pivot is {pivot}, parked at the end. `store` marks where the next smaller value will go. Nothing has been looked at yet.",
        Row(a, st=part_state(0), ptr={"i": 0, "store": 0}, slots=True), M({"pivot": pivot, "smaller found": 0}))
for i in range(hi):
    if a[i] < pivot:
        a[i], a[store] = a[store], a[i]
        msg = f"`i` = {i}: {a[store]} < {pivot}, so it joins the smaller side. " + (f"Swap it into index {store} (where `store` points) and move `store` right." if i != store else f"It's already at `store`, so `store` just moves right.")
        store += 1
    else:
        msg = f"`i` = {i}: {a[i]} ≥ {pivot}. Leave it where it is; it's on the bigger side for now."
    pw.step(msg, Row(list(a), st=part_state(i + 1), ptr={"i": i, "store": store}, slots=True), M({"pivot": pivot, "smaller found": store}))
a[store], a[hi] = a[hi], a[store]
pw.step(f"Every value has been looked at. Swap the pivot into index {store}, the first slot after the smaller values. It is now exactly where it will be in the sorted array.",
        Row(list(a), st={**{k: "found" for k in range(store)}, **{k: "mark" for k in range(store + 1, len(a))}, store: "answer"}, ptr={"store": store}, slots=True),
        M({"pivot": pivot, "smaller found": store}), result=f"pivot at index {store}")
PART = list(a)
PSTORE = store
PART_LEGEND = {"found": "smaller than the pivot", "mark": "looked at, not smaller", "active": "the pivot, parked at the end", "answer": "the pivot in its final place"}
MERGE_LEGEND = {"dim": "already taken", "new": "just placed in the output"}

# A whole merge sort, one merge per step, in the order the recursion does them.
msw = Steps(f"The whole of `merge_sort({DEMO})`. The recursion finishes the left half completely before it starts the right half.")
arr = list(DEMO)
msw.step("Nothing merged yet. Every single value counts as a sorted piece of length 1.", Row(arr, slots=True), M({"merging": "nothing yet", "result": "–"}))


def ms_trace(lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    ms_trace(lo, mid)
    ms_trace(mid, hi)
    left, right = arr[lo:mid], arr[mid:hi]
    arr[lo:hi] = sorted(arr[lo:hi])
    whole = " This was the last merge: the array is sorted." if (lo, hi) == (0, len(arr)) else ""
    msw.step(f"Merge indices {lo}..{mid - 1} ({' '.join(map(str, left))}) with {mid}..{hi - 1} ({' '.join(map(str, right))}). Both halves were sorted by the steps before.{whole}",
             Row(list(arr), st={k: "found" for k in range(lo, hi)}, slots=True),
             M({"merging": f"{left} + {right}", "result": " ".join(map(str, arr[lo:hi]))}))


ms_trace(0, len(arr))
assert arr == SORTED

# A whole quick sort (last value as pivot, left side first), one partition per step.
QD = [7, 2, 9, 4, 3, 8, 5, 1]
qsw = Steps(f"The whole of a quick sort on `{QD}`, with the last value of each range as the pivot so you can follow it.")
arr, placed = list(QD), set()
qsw.step("Nothing is in its final place yet. The first range is the whole array.", Row(arr, slots=True), M({"range": f"0..{len(arr) - 1}", "pivot": "–", "lands at": "–"}))
todo = [(0, len(arr) - 1)]
while todo:
    lo, hi = todo.pop()
    if lo > hi:
        continue
    if lo == hi:
        placed.add(lo)
        continue
    pv, s_ = arr[hi], lo
    for i in range(lo, hi):
        if arr[i] < pv:
            arr[i], arr[s_] = arr[s_], arr[i]
            s_ += 1
    arr[s_], arr[hi] = arr[hi], arr[s_]
    placed.add(s_)
    singles = [k for k in (s_ - 1, s_ + 1) if (k == lo == s_ - 1) or (k == hi == s_ + 1)]
    for k in singles:
        placed.add(k)
    left_n, right_n = s_ - lo, hi - s_
    note = (" " + " and ".join(f"index {k} ({arr[k]})" for k in singles).capitalize() + (" is a range" if len(singles) == 1 else " are ranges") + " of one, so final too.") if singles else ""
    lopsided = f" A lopsided split: {pv} was the {'smallest' if left_n == 0 else 'largest'} value in the range, so only one value got placed." if min(left_n, right_n) == 0 and hi - lo > 1 else ""
    qsw.step(f"Partition {lo}..{hi} around {pv}: {left_n} smaller value{' goes' if left_n == 1 else 's go'} left, {right_n} {'goes' if right_n == 1 else 'go'} right, and {pv} lands at index {s_}.{lopsided}{note}",
             Row(list(arr), st={**{k: "mark" for k in range(lo, hi + 1)}, **{k: "found" for k in placed}, s_: "answer"}, slots=True),
             M({"range": f"{lo}..{hi}", "pivot": pv, "lands at": s_}))
    todo += [(s_ + 1, hi), (lo, s_ - 1)]
assert arr == sorted(QD)
qsw.step("No ranges left: every value has been a pivot or sat in a range of one, so every value is in its final place.",
         Row(list(arr), st={k: "found" for k in range(len(arr))}, slots=True), M({"range": "none left", "pivot": "–", "lands at": "–"}))

# Counting comparisons: merge sort vs quick sort with a fixed last-element pivot on sorted input.
def merge_cmp(a):
    c = 0

    def go(x):
        nonlocal c
        if len(x) < 2:
            return x
        m = len(x) // 2
        l_, r_ = go(x[:m]), go(x[m:])
        out, i, j = [], 0, 0
        while i < len(l_) and j < len(r_):
            c += 1
            if l_[i] <= r_[j]:
                out.append(l_[i]); i += 1
            else:
                out.append(r_[j]); j += 1
        return out + l_[i:] + r_[j:]
    go(list(a))
    return c


def quick_last_cmp(a):
    a, c = list(a), 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pv, s = a[hi], lo
        for i in range(lo, hi):
            c += 1
            if a[i] < pv:
                a[i], a[s] = a[s], a[i]
                s += 1
        a[s], a[hi] = a[hi], a[s]
        stack += [(lo, s - 1), (s + 1, hi)]
    return c


CMP_ROWS = []
for n in (8, 64, 512):
    CMP_ROWS.append((str(n), str(merge_cmp(list(range(n)))), str(quick_last_cmp(list(range(n)))), str(quick_last_cmp([5] * n))))
CMP_N = 512

# Stability, shown on records.
REC = [("Ana", 3), ("Ben", 1), ("Cy", 3), ("Dee", 2), ("Eve", 1)]


def merge_records(rs):
    if len(rs) < 2:
        return rs
    m = len(rs) // 2
    l_, r_ = merge_records(rs[:m]), merge_records(rs[m:])
    out, i, j = [], 0, 0
    while i < len(l_) and j < len(r_):
        if l_[i][1] <= r_[j][1]:
            out.append(l_[i]); i += 1
        else:
            out.append(r_[j]); j += 1
    return out + l_[i:] + r_[j:]


def quick_records(rs):
    rs = list(rs)

    def go(lo, hi):
        if lo >= hi:
            return
        pv, s = rs[hi][1], lo
        for i in range(lo, hi):
            if rs[i][1] < pv:
                rs[i], rs[s] = rs[s], rs[i]
                s += 1
        rs[s], rs[hi] = rs[hi], rs[s]
        go(lo, s - 1)
        go(s + 1, hi)
    go(0, len(rs) - 1)
    return rs


MS_REC, QS_REC = merge_records(REC), quick_records(REC)
assert MS_REC != QS_REC


def rec_str(rs):
    return ", ".join(f"{n} ({s})" for n, s in rs)


# Insertion sort on a nearly sorted array: shifts per element.
NEAR = [2, 1, 3, 5, 4, 6, 8, 7]
SHIFTS = []
a = list(NEAR)
for i in range(1, len(a)):
    x, j, s = a[i], i - 1, 0
    while j >= 0 and a[j] > x:
        a[j + 1] = a[j]
        j -= 1
        s += 1
    a[j + 1] = x
    SHIFTS.append(s)
assert a == sorted(NEAR)

lesson(
    "sorting",
    "comparison-sorts",
    """
    Merge sort and quick sort are the two classic ways to sort in O(n log n) by comparing values. Both split the
    problem in two and sort each part. Merge sort splits blindly and does its work while joining sorted halves
    back together; quick sort does its work while splitting, so there's nothing left to join. The sorts in most
    standard libraries are built from these two, with insertion sort for small ranges.
    """,
    [
        ("idea", "The idea", [
            """
            Imagine sorting a big stack of exam papers by score. One way: split the stack in half and hand each half
            to a friend to sort. When they hand them back, you merge the two sorted piles by repeatedly taking whichever
            top paper has the lower score. Your friends do the same thing with their halves, and so on, until someone
            gets a pile of one paper, which is already sorted. That's **merge sort**.

            Another way: pick one paper, say a 60, and make two piles: everything below 60 and everything else. The 60
            goes between them, exactly where it will end up. Now sort each pile the same way. When both are sorted,
            the whole stack is sorted, with no merging needed. That's **quick sort**, and the 60 is the **pivot**.

            Both are "divide and conquer". Merge sort's split costs nothing and all the work is in the merge. Quick
            sort spends its effort on the split and then has nothing to join.
            """,
            fig(*up_rows, caption="Merge sort, read from the top: single values are sorted pieces, and each level merges neighbouring pieces into bigger ones."),
            key("""
            Merge sort: sort each half, then merge them by repeatedly taking the smaller front value. Always O(n log n),
            stable, needs O(n) extra space. Quick sort: pick a pivot, move smaller values to its left and the rest to its
            right, then sort each side. O(n log n) on average with a random pivot, in place, not stable.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Most of the time you just call your language's sort, and that's the right call. Write these yourself when:

            - the question says so ("implement a sort", "without the built-in sort");
            - the data isn't an array you can hand to the library, such as a linked list (merge sort suits it, since
              merging lists needs no extra array);
            - the input has a shape that breaks a naive sort, such as many repeated values or nearly sorted
              data, and you need to pick or adapt a sort for it;
            - you need the *pieces* of the algorithm: partitioning around a pivot (*Quickselect*), or doing extra work
              during the merge (*Counting while merging*).

            Choosing between them:
            """,
            table(["you need", "pick", "because"],
                  ["guaranteed O(n log n)", "merge sort", "it always splits evenly"],
                  ["equal items to keep their order (stable)", "merge sort", "taking from the left half on ties keeps order"],
                  ["no extra memory", "quick sort", "it partitions in place"],
                  ["to sort a linked list", "merge sort", "lists merge by relinking, no buffer"],
                  ["only the k-th value, not a full sort", "quick sort's partition", "see *Quickselect*"],
                  ["tiny or nearly sorted input", "insertion sort", "almost no work when items are close to home"]),
        ]),
        ("theory", "Why it works", [
            """
            ### Merging two sorted lists

            If two lists are each sorted, the smallest value overall is at the front of one of them. Take it, and the
            same is true of what's left. So one pass with two pointers produces the merged list, doing at most one
            comparison per value placed. When one list runs out, the rest of the other is already in order and bigger
            than everything placed, so it's copied across as is.
            """,
            walk(mw, legend=MERGE_LEGEND),
            """
            ### Why merge sort is O(n log n)

            Each level of splitting halves the pieces, so there are about `log₂ n` levels. At every level, the merges
            together touch each value once: O(n) per level. That's O(n log n) total, and it doesn't depend on the input
            at all: sorted, reversed or random, merge sort does the same splits.

            ### Partitioning around a pivot

            Quick sort's partition scans the range once with two markers. Everything left of `store` is smaller than
            the pivot; everything between `store` and the scan is not. A small value found by the scan is swapped to
            `store`, which moves right. At the end the pivot is swapped into `store`, which is exactly its sorted
            position: all smaller values are on its left, all others on its right. Then neither side ever needs to
            look at the other again.
            """,
            walk(pw, legend=PART_LEGEND),
            f"""
            ### Why quick sort is O(n log n) on average, and when it isn't

            If the pivot splits the range roughly in half, there are about `log n` levels with O(n) work each, as with
            merge sort. But if the pivot is always the smallest or largest value, each partition only peels off one
            value, there are `n` levels, and it's O(n²). With "always take the last value" as the rule, an already
            sorted array does exactly that. Picking the pivot at random makes such bad luck vanishingly unlikely
            on any input; the expected number of comparisons is about `1.39 · n log₂ n`.

            Comparisons counted on real runs (last value as pivot, so you can see the bad case):
            """,
            table(["n", "merge sort (sorted input)", "quick sort, last pivot (sorted input)", "quick sort, all values equal"], *CMP_ROWS),
            f"""
            At n = {CMP_N}, the sorted input costs quick sort over {int(CMP_ROWS[-1][2]) // int(CMP_ROWS[-1][1])} times as many comparisons as merge sort.
            The last column is the other trap: when every value is equal, `a[i] < pivot` is never true, every partition
            puts the pivot at the very left, and it's O(n²) again, *even with a random pivot*. The cure is to partition
            into three parts (smaller, equal, bigger) and only recurse into the outer two.

            ### Stability

            A sort is **stable** if equal items keep their original order. It matters when you sort records by one
            field and their earlier order means something. Sorting `{rec_str(REC)}` by the number:
            """,
            table(["sort", "result"], ["merge sort (takes from the left on ties)", rec_str(MS_REC)], ["quick sort (swaps over long distances)", rec_str(QS_REC)]),
            """
            Merge sort is stable because, on a tie, it takes the value from the left half, which came first. Quick sort's
            long-distance swaps can jump an item over its equals, so it isn't.

            ### Nothing comparison-based beats n log n

            A comparison sort learns one yes/no answer per comparison. There are `n!` possible orders of the input, and
            it must tell them all apart, so it needs at least `log₂(n!) ≈ n log₂ n` comparisons in the worst case. To go
            faster you have to stop comparing and look at the values themselves (*Counting and bucket sort*).
            """,
        ]),
        ("template", "The template", [
            "Merge sort, with one shared buffer so the merges don't allocate new lists every time.",
            code(
                "Merge sort",
                MERGE,
                [
                    ("base", "A range of 0 or 1 values is already sorted."),
                    ("split", "The middle of the range `[lo, hi)`.",
                     {"java": "`>>> 1` is an unsigned shift: it halves `lo + hi` correctly even if the sum overflows `int`.",
                      "cpp": "`lo + (hi - lo) / 2` avoids overflowing `lo + hi`.",
                      "c": "`lo + (hi - lo) / 2` avoids overflowing `lo + hi`."}),
                    ("halves", "Sort each half (the recursion trusts itself)."),
                    ("ptrs", "`i` walks the left half, `j` the right half, `k` the buffer."),
                    ("merge", "While both halves have values left…"),
                    ("pick", "…take the smaller front value. `<=` takes from the left on ties, which keeps the sort stable."),
                    ("rest", "One half is used up; copy the rest of the other."),
                    ("copy", "Move the merged range back into `a`.",
                     {"java": "`System.arraycopy` is a fast bulk copy.", "c": "`memcpy` copies the bytes of the merged range."}),
                    ("buf", "One buffer the size of the array, shared by every merge.",
                     {"c": "`malloc` at least one element so a zero-length input doesn't ask for 0 bytes."}),
                    ("ret", "The sorted array.", {"c": "Free the buffer; the caller's array is sorted in place."}),
                ],
                MERGE_RUN,
                "merge_sort([38, 27, 43, 3, 9, 82, 10]); ([5, 1, 5, 1]); ([7])",
            ),
            "Quick sort, with a random pivot and a loop that keeps the recursion shallow.",
            code(
                "Quick sort",
                QUICK,
                [
                    ("pivot", "Choose a random pivot and park it at the end of the range.",
                     {"java": "A seeded `Random` keeps runs repeatable; any source of randomness works.",
                      "c": "`rand() % size` is fine here; it doesn't need to be perfectly uniform."}),
                    ("store", "Everything left of `store` will be smaller than the pivot."),
                    ("scan", "Look at every other value in the range once."),
                    ("small", "A smaller value moves to `store`, and the small side grows by one."),
                    ("place", "Put the pivot between the two sides. Its index is final."),
                    ("loop", "Ranges of 0 or 1 values are done."),
                    ("part", "Partition, and get the pivot's final index."),
                    ("smaller", "Recurse into the *smaller* side and loop on the bigger one. The recursion then never goes "
                                "deeper than about `log₂ n`, even on unlucky inputs."),
                    ("start", "Sort the whole array.", {"c": "C sorts the caller's array in place."}),
                ],
                QUICK_RUN,
                "quick_sort([7, 2, 9, 4, 3, 8, 5]); ([4, 4, 1, 4, 0]); (10 down to 1)",
            ),
        ]),
        ("trace", "Trace it by hand", [
            """
            You've stepped through one merge and one partition in *Why it works*. Here are whole sorts, one big step
            at a time. First merge sort: watch the sorted pieces grow from the left, because the recursion finishes the
            left half before it touches the right.
            """,
            walk(msw, legend={"found": "the range just merged (now sorted)"}),
            """
            Now quick sort. Each step is a whole partition: the pivot lands in its final place, and the range splits in
            two. Unlike merge sort, nothing is ever merged back; once every value has been placed, the sort is done.
            """,
            walk(qsw, legend={"mark": "the range being partitioned", "answer": "the pivot, placed this step", "found": "in its final place"}),
            """
            On paper, draw the recursion as a tree with one node per range. Merge sort's work shows up on the way back
            up the tree, quick sort's on the way down.
            """,
        ]),
        ("examples", "More examples", [
            f"""
            ### Nearly sorted input

            If every value is only a few places from home, use insertion sort. It takes each value in
            turn and slides it left past the bigger values before it. On `{NEAR}` the number of slides per value is
            `{SHIFTS}`, a total of {sum(SHIFTS)} instead of the ~{len(NEAR) * (len(NEAR) - 1) // 4} you'd expect on random input. In
            general, if every value is at most `k` places from home, it's O(n·k). (With large `k`, a heap does better;
            that comes in the Heaps topic.)

            ### Sorting a linked list

            You can't jump to the middle of a linked list, and swapping far-apart nodes is awkward, so quick sort is a poor
            fit. Merge sort is natural: find the middle with a slow and a fast pointer, cut the list there, sort both
            halves, and merge them by relinking nodes. No buffer is needed.

            ### Many equal values

            Look again at the last column of the comparison table. Before you use quick sort on data like "most
            values are one of three readings", make the partition group equal values together, or use merge sort.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Insertion sort

            Insertion sort is short to write and stable, needs no extra memory, and beats the others on small or nearly
            sorted arrays. Library sorts switch to it once a range drops below about 16 to 32 values.
            """,
            code(
                "Insertion sort",
                INSERT,
                [
                    ("each", "Values left of `i` are already sorted. Insert `a[i]` among them."),
                    ("take", "Lift the value out, leaving a gap."),
                    ("shift", "Slide bigger values one place right, moving the gap left. `>` (not `>=`) keeps it stable."),
                    ("drop", "Put the value into the gap."),
                    ("ret", "The sorted array."),
                ],
                INSERT_RUN,
                "insertion_sort([5, 2, 4, 6, 1, 3])",
            ),
            """
            ### Bottom-up merge sort

            Instead of recursing, merge pieces of size 1 into size 2, then 2 into 4, and so on, with a loop over the piece
            size. It's still O(n log n) and needs no recursion. The figure in *The idea* merges in this order.

            ### Hybrid sorts

            Library sorts mix these ideas. Introsort (C++'s `std::sort`) is quick sort that switches to heap
            sort if the recursion gets too deep (so it's never O(n²)), and to insertion sort for small ranges. Timsort
            (Python, Java for objects) is a merge sort that finds runs already in order and merges those, so nearly sorted
            data is close to O(n).
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Merge sort: O(n log n) time always; O(n) extra space for the buffer, plus O(log n) for the recursion. Quick
            sort: O(n log n) expected time with a random pivot, O(n²) in the worst case (and on many equal values without
            a three-way partition); O(log n) extra space when you recurse into the smaller side.
            """,
            table(
                ["Sort", "Best", "Average", "Worst", "Extra space", "Stable"],
                ["Insertion sort", "O(n)", "O(n²)", "O(n²)", "O(1)", "yes"],
                ["Merge sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "yes"],
                ["Quick sort (random pivot)", "O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "no"],
                ["Library sort (introsort / Timsort)", "O(n) to O(n log n)", "O(n log n)", "O(n log n)", "varies", "Timsort yes"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `list.sort()` (in place) and `sorted()` (new list) use Timsort: stable, O(n log n), and very fast on partly
            sorted data. Python's recursion limit (about 1000) is fine for merge sort, whose depth is `log₂ n`, but a
            quick sort that recurses into both sides can hit it on bad input.

            ### Java

            `Arrays.sort(int[])` is a dual-pivot quick sort: fast, but not stable (stability doesn't matter for plain
            numbers). `Arrays.sort(Object[])` and `Collections.sort` use Timsort, which is stable. Use `>>> 1` or
            `lo + (hi - lo) / 2` for midpoints.

            ### C++

            `std::sort` is introsort: O(n log n) worst case, not stable. `std::stable_sort` is a merge sort.
            `std::partition` and `std::nth_element` give you quick sort's pieces.

            ### C

            `qsort(base, n, size, cmp)` takes a comparator returning negative, zero or positive. Its algorithm and
            stability aren't specified. Write the comparator as `(a > b) - (a < b)`, never `a - b`, which can overflow.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Using `<` instead of `<=` when merging, which takes from the right half on ties and loses stability.
            - Forgetting to copy the leftovers after one half runs out.
            - Allocating a new list in every merge call: correct, but slow. Share one buffer.
            - Always taking the first or last value as the pivot. Sorted input becomes O(n²).
            - Many equal values with a two-way partition: O(n²) even with a random pivot.
            - Recursing into both sides of quick sort and overflowing the stack on bad input.
            - `(lo + hi) / 2` overflowing in Java, C and C++ for very large arrays.
            - Empty and single-value arrays: both sorts must handle `n = 0` and `n = 1`.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why is merge sort O(n log n) on every input?",
                 "It always splits in half, so there are about log₂ n levels, and the merges at each level touch every value once."),
                ("What makes quick sort O(n²), and how does a random pivot help?",
                 "Pivots that are always the smallest or largest value, so each partition removes only one value. A random pivot makes that very unlikely on any input, giving O(n log n) on average."),
                ("Why can't a random pivot rescue quick sort when every value is equal?",
                 "With a two-way partition, every value is 'not smaller' than the pivot, so the pivot always lands at the edge. You need a three-way partition that sets the equal values aside."),
                ("Which line makes merge sort stable?",
                 "Taking from the left half when the two front values are equal (`a[i] <= a[j]`). The left half's items came first in the input."),
                ("Why is insertion sort fast on nearly sorted input?",
                 "Each value only slides past the few bigger values before it. If every value is within k places of home, that's at most k slides each, so O(n·k)."),
            ),
        ]),
    ],
)
