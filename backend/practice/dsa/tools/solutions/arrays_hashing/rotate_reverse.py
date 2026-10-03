"""Arrays & Hashing: rotate and reverse."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

from arrays_hashing.next_permutation import next_perm, pivot_walk


@problem
def next_arrangement():
    vals = [1, 5, 8, 4, 7, 6, 5, 3, 1]
    want = next_perm(vals)
    assert want == [1, 5, 8, 5, 1, 3, 4, 6, 7]

    w1 = Steps("Generate arrangements in increasing order; the first one larger than the input is next. None larger → wrap to the smallest.")
    from itertools import permutations
    small = [1, 3, 2]
    perms = sorted(set(permutations(small)))
    w1.step(f"A small case, {small}: its distinct arrangements in dictionary order.", Row(small))
    for p in perms:
        if list(p) > small:
            w1.step(f"{list(p)} > {small}: this is the next arrangement.", Row(list(p), st={k: "answer" for k in range(3)}), result=list(p))
            break
        w1.step(f"{list(p)}: not larger.", Row(list(p), st={k: "dim" for k in range(3)}))

    w2 = Steps("Pivot, swap with the rightmost larger value, reverse the tail. With no pivot, reverse everything (wrap around).")
    res = pivot_walk(w2, vals, word="value")
    w2.steps[-1]["result"] = str(res)
    w2.step("If the input had been fully descending (no pivot), reversing the whole list would give the first arrangement.", Row([3, 2, 1], label="e.g. [3, 2, 1]"), Row([1, 2, 3], label="→ [1, 2, 3]"))

    sol(
        "next-arrangement",
        summary="""
            This is next permutation with wrap-around: find the rightmost value smaller than its right neighbour (the
            pivot), swap it with the rightmost larger value after it, then reverse everything after the pivot. If there
            is no pivot, the list is the last arrangement, and reversing all of it gives the first. O(n), in place.
        """,
        question=[
            """
            Among all arrangements of the values, in dictionary order, return the one right **after** `values`. If
            `values` is the last arrangement (fully descending), return the first (fully ascending).

            - **Repeated values** count once per distinct arrangement: `[1, 1, 5]` → `[1, 5, 1]`.
            - **Wrap-around:** `[3, 2, 1]` → `[1, 2, 3]`.
            - **Up to 10⁵ values**, so the change must be computed directly, not by listing arrangements.
            - The same algorithm as **Next Badge Number** (on digits) and the mirror of **One Step Back**.
            """
        ],
        think=[
            f"""
            Take `{vals}`. From the right, `7, 6, 5, 3, 1` never increases: it's already the largest arrangement of
            those values, so the change must happen just before it, at the **4** (index 3). Replace the 4 with the
            smallest tail value bigger than it (5, the rightmost one larger than 4), then make the tail as small as
            possible by reversing it into ascending order: `{want}`.
            """,
            fig(Row(vals, st={3: "mark"} | {k: "found" for k in range(4, 9)}, slots=True), Row(want, st={3: "new"} | {k: "new" for k in range(4, 9)}, slots=True),
                caption="Pivot 4, swapped with 5; the tail reversed into ascending order."),
            """
            Without a pivot, the whole list is non-increasing: the last arrangement. Reversing it gives the first
            arrangement, which is exactly the wrap-around the problem asks for. So the same "reverse the tail" step
            handles both cases if the tail starts at index `pivot + 1 = 0`.
            """,
        ],
        approaches=[
            approach(
                "Generate arrangements in order",
                "brute",
                "O(n! · n)",
                "O(n)",
                idea=["Recursively build arrangements in increasing order (smallest available value first, with counts for repeats). Return the first one larger than the input. If none is larger, return the values sorted ascending."],
                walk=w1,
                build=["Count each value (0 … 100).", "Recursively fill positions trying values 0 … 100.", "At a full arrangement, return it if it's larger than the input.", "If none is, return all values in ascending order."],
                code={
                    "python": """
                        class Solution:
                            def nextArrangement(self, values: List[int]) -> List[int]:
                                count = [0] * 101  #@count
                                for v in values:  #@count
                                    count[v] += 1  #@count
                                buf = []
                                def build():  #@gen
                                    if len(buf) == len(values):  #@gen
                                        return list(buf) if buf > values else None  #@gen
                                    for v in range(101):  #@gen
                                        if count[v]:  #@gen
                                            count[v] -= 1  #@gen
                                            buf.append(v)  #@gen
                                            found = build()  #@gen
                                            buf.pop()  #@gen
                                            count[v] += 1  #@gen
                                            if found:  #@gen
                                                return found  #@gen
                                    return None  #@gen
                                return build() or sorted(values)  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int[] count = new int[101], buf, target;

                            public int[] nextArrangement(int[] values) {
                                target = values;  //@count
                                buf = new int[values.length];  //@count
                                for (int v : values) count[v]++;  //@count
                                if (build(0)) return buf;  //@ret
                                int[] out = values.clone();  //@ret
                                Arrays.sort(out);  //@ret
                                return out;  //@ret
                            }

                            private boolean build(int pos) {  //@gen
                                if (pos == buf.length) return Arrays.compare(buf, target) > 0;  //@gen
                                for (int v = 0; v <= 100; v++) {  //@gen
                                    if (count[v] == 0) continue;  //@gen
                                    count[v]--;  //@gen
                                    buf[pos] = v;  //@gen
                                    boolean found = build(pos + 1);  //@gen
                                    count[v]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            int count[101] = {0};
                            vector<int> buf, target;

                            bool build(size_t pos) {  //@gen
                                if (pos == buf.size()) return buf > target;  //@gen
                                for (int v = 0; v <= 100; v++) {  //@gen
                                    if (!count[v]) continue;  //@gen
                                    count[v]--;  //@gen
                                    buf[pos] = v;  //@gen
                                    bool found = build(pos + 1);  //@gen
                                    count[v]++;  //@gen
                                    if (found) return true;  //@gen
                                }
                                return false;  //@gen
                            }

                        public:
                            vector<int> nextArrangement(vector<int>& values) {
                                target = values;  //@count
                                buf.assign(values.size(), 0);  //@count
                                for (int v : values) count[v]++;  //@count
                                if (build(0)) return buf;  //@ret
                                vector<int> out = values;  //@ret
                                sort(out.begin(), out.end());  //@ret
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int count[101];
                        static int* buf;
                        static int* target;
                        static int len;

                        static bool build(int pos) {  //@gen
                            if (pos == len) {  //@gen
                                for (int i = 0; i < len; i++) if (buf[i] != target[i]) return buf[i] > target[i];  //@gen
                                return false;  //@gen
                            }  //@gen
                            for (int v = 0; v <= 100; v++) {  //@gen
                                if (!count[v]) continue;  //@gen
                                count[v]--;  //@gen
                                buf[pos] = v;  //@gen
                                bool found = build(pos + 1);  //@gen
                                count[v]++;  //@gen
                                if (found) return true;  //@gen
                            }
                            return false;  //@gen
                        }

                        int* nextArrangement(int* values, int valuesSize, int* returnSize) {
                            len = valuesSize;  //@count
                            target = values;  //@count
                            buf = malloc(len * sizeof(int));  //@count
                            memset(count, 0, sizeof count);  //@count
                            for (int i = 0; i < len; i++) count[values[i]]++;  //@count
                            *returnSize = len;  //@ret
                            if (build(0)) return buf;  //@ret
                            int k = 0;  //@ret
                            for (int v = 0; v <= 100; v++) for (int c = 0; c < count[v]; c++) buf[k++] = v;  //@ret
                            return buf;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "Copies of each value still available to place (values are 0 … 100)."),
                    ("gen", "Fill positions left to right, smallest value first, so arrangements come out in increasing order; return at the first one larger than the input."),
                    ("ret", "Nothing larger means the input is the last arrangement: wrap to the first, the values in ascending order."),
                ],
                complexity=["**Time O(n! · n)** in the worst case. **Space O(n).** Only practical for a handful of values."],
                limits=["The next arrangement differs from the input only in a suffix that can be found directly, so generating everything before it is pure waste."],
                slow=24,
            ),
            approach(
                "Next permutation with wrap-around",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    1. **Pivot:** the rightmost `i` with `a[i] < a[i + 1]`.
                    2. If it exists, find the rightmost `j > i` with `a[j] > a[i]` and swap them.
                    3. **Reverse** `a[i + 1 …]`. Without a pivot, `i = −1` and this reverses the whole list, which turns the
                       last arrangement into the first.
                    """
                ],
                walk=w2,
                build=["Scan i from n − 2 down while `a[i] ≥ a[i + 1]`.", "If `i ≥ 0`: scan j from the end while `a[j] ≤ a[i]`, then swap.", "Reverse from `i + 1` to the end.", "Return the array."],
                code={
                    "python": """
                        class Solution:
                            def nextArrangement(self, values: List[int]) -> List[int]:
                                a = values  #@alias
                                i = len(a) - 2  #@pivot
                                while i >= 0 and a[i] >= a[i + 1]:  #@pivot
                                    i -= 1  #@pivot
                                if i >= 0:  #@swap
                                    j = len(a) - 1  #@swap
                                    while a[j] <= a[i]:  #@swap
                                        j -= 1  #@swap
                                    a[i], a[j] = a[j], a[i]  #@swap
                                a[i + 1:] = reversed(a[i + 1:])  #@rev
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] nextArrangement(int[] values) {
                                int[] a = values;  //@alias
                                int n = a.length, i = n - 2;  //@pivot
                                while (i >= 0 && a[i] >= a[i + 1]) i--;  //@pivot
                                if (i >= 0) {  //@swap
                                    int j = n - 1;  //@swap
                                    while (a[j] <= a[i]) j--;  //@swap
                                    int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                }
                                for (int x = i + 1, y = n - 1; x < y; x++, y--) { int t = a[x]; a[x] = a[y]; a[y] = t; }  //@rev
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> nextArrangement(vector<int>& values) {
                                vector<int>& a = values;  //@alias
                                int n = a.size(), i = n - 2;  //@pivot
                                while (i >= 0 && a[i] >= a[i + 1]) i--;  //@pivot
                                if (i >= 0) {  //@swap
                                    int j = n - 1;  //@swap
                                    while (a[j] <= a[i]) j--;  //@swap
                                    swap(a[i], a[j]);  //@swap
                                }
                                reverse(a.begin() + i + 1, a.end());  //@rev
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* nextArrangement(int* values, int valuesSize, int* returnSize) {
                            int* a = values;  //@alias
                            int n = valuesSize, i = n - 2;  //@pivot
                            while (i >= 0 && a[i] >= a[i + 1]) i--;  //@pivot
                            if (i >= 0) {  //@swap
                                int j = n - 1;  //@swap
                                while (a[j] <= a[i]) j--;  //@swap
                                int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                            }
                            for (int x = i + 1, y = n - 1; x < y; x++, y--) { int t = a[x]; a[x] = a[y]; a[y] = t; }  //@rev
                            *returnSize = n;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[
                    ("alias", "Rearrange the input in place: O(1) extra space."),
                    ("pivot", "From the right, skip the non-increasing tail; stop at the first value smaller than its neighbour."),
                    ("swap", "Only when a pivot exists: swap it with the rightmost (= smallest) larger value in the tail."),
                    ("rev", "Reverse the tail into ascending order. With no pivot, `i + 1` is 0 and the whole list is reversed: last arrangement → first."),
                    ("ret", "The next arrangement."),
                ],
                complexity=["**Time O(n).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Next permutation: pivot, swap with rightmost larger, reverse suffix. Letting the reversal start at
              `pivot + 1` also handles the wrap-around when there's no pivot.
            - It's the same building block as **Next Badge Number** and **Next Mirror Number**; recognise it.
            """
        ],
    )


@problem
def rotate_the_carousel():
    slots, k = [1, 2, 3, 4, 5, 6, 7], 3
    n = len(slots)
    want = slots[-k:] + slots[:-k]

    w1 = Steps("Turn the carousel one step at a time, k times: the last seat moves to the front.")
    a = slots[:]
    for s in range(k):
        a = [a[-1]] + a[:-1]
        w1.step(f"Step {s + 1}: the last seat moves to the front; everything else shifts right ({n} moves).", Row(a, st={0: "new"}, slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Copy each seat straight to its new position (i + k) mod n in a second array.")
    out = [None] * n
    for i in range(n):
        out[(i + k) % n] = slots[i]
        w2.step(f"Seat at {i} ({slots[i]}) → position ({i} + {k}) mod {n} = {(i + k) % n}.", Row(slots, st={i: "active"}, slots=True), Row(list(out), st={(i + k) % n: "new"}, label="new array", slots=True))
    w2.steps[-1]["result"] = str(out)

    w3 = Steps("Three reversals: the whole array, then the first k, then the rest.")
    a = slots[:]
    w3.step(f"k = {k}: the last {k} seats should end up in front, both blocks keeping their order.", Row(a, st={i: "mark" for i in range(n - k, n)}, slots=True))
    a.reverse()
    w3.step("Reverse everything: the last block is now in front, but both blocks are backwards.", Row(list(a), st={i: "mark" for i in range(k)}, slots=True))
    a[:k] = reversed(a[:k])
    w3.step(f"Reverse the first {k}: that block reads forwards again.", Row(list(a), st={i: "new" for i in range(k)}, slots=True))
    a[k:] = reversed(a[k:])
    w3.step(f"Reverse the remaining {n - k}: done.", Row(list(a), st={i: "new" for i in range(k, n)}, slots=True), result=a)

    sol(
        "rotate-the-carousel",
        summary="""
            Rotating right by k moves the last `k mod n` seats to the front, keeping both blocks in order. Reversing the
            whole array, then reversing each of the two blocks, does exactly that in place: O(n) time, O(1) extra space.
        """,
        question=[
            """
            Move every seat k places toward the end, wrapping around to the front. Return the new order.

            - **k can be huge** (up to 10⁹) but rotating by n is a full turn, so only `k mod n` matters. `[9, 8]` with
              k = 3 is the same as k = 1: `[8, 9]`.
            - **k = 0** (or a multiple of n) leaves the order unchanged.
            - **Goal:** in place with O(1) extra space.
            """
        ],
        think=[
            f"""
            Take `{slots}` with k = {k}. Each seat moves {k} places right; the last {k} seats wrap to the front:
            `{want}`. In other words, the array is two blocks, `A = {slots[:n - k]}` and `B = {slots[n - k:]}`, and the
            answer is `B` followed by `A`.
            """,
            fig(Row(slots, st={i: "mark" for i in range(n - k, n)}, slots=True), Row(want, st={i: "mark" for i in range(k)}, slots=True), caption="A B → B A, each block keeping its own order."),
            """
            Swapping two blocks of different lengths in place sounds hard, but reversal does it neatly. Reverse the
            whole array: `B` comes first and `A` second, but each is backwards. Reverse each block again and both read
            forwards. Every reversal is a simple two-pointer swap loop with O(1) extra space.
            """,
        ],
        approaches=[
            approach(
                "Rotate one step, k times",
                "brute",
                "O(n · k)",
                "O(1)",
                idea=["One step right means: save the last seat, shift everything one place right, put the saved seat at the front. Do it `k mod n` times."],
                walk=w1,
                build=["`k %= n`.", "Repeat k times: save `a[n − 1]`, shift `a[0 … n − 2]` right by one, put the saved value at index 0."],
                code={
                    "python": """
                        class Solution:
                            def rotateRight(self, slots: List[int], k: int) -> List[int]:
                                n = len(slots)
                                for _ in range(k % n):  #@times
                                    last = slots[-1]  #@step
                                    for i in range(n - 1, 0, -1):  #@step
                                        slots[i] = slots[i - 1]  #@step
                                    slots[0] = last  #@step
                                return slots  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] rotateRight(int[] slots, int k) {
                                int n = slots.length;
                                for (int t = 0; t < k % n; t++) {  //@times
                                    int last = slots[n - 1];  //@step
                                    for (int i = n - 1; i > 0; i--) slots[i] = slots[i - 1];  //@step
                                    slots[0] = last;  //@step
                                }
                                return slots;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> rotateRight(vector<int>& slots, int k) {
                                int n = slots.size();
                                for (int t = 0; t < k % n; t++) {  //@times
                                    int last = slots[n - 1];  //@step
                                    for (int i = n - 1; i > 0; i--) slots[i] = slots[i - 1];  //@step
                                    slots[0] = last;  //@step
                                }
                                return slots;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* rotateRight(int* slots, int slotsSize, int k, int* returnSize) {
                            int n = slotsSize;
                            for (int t = 0; t < k % n; t++) {  //@times
                                int last = slots[n - 1];  //@step
                                for (int i = n - 1; i > 0; i--) slots[i] = slots[i - 1];  //@step
                                slots[0] = last;  //@step
                            }
                            *returnSize = n;  //@ret
                            return slots;  //@ret
                        }
                    """,
                },
                lines=[("times", "Only `k mod n` steps matter; full turns change nothing."), ("step", "One step: the last seat is saved, everything shifts right by one (back to front, so nothing is overwritten early), and the saved seat goes to the front."), ("ret", "Rotated in place.")],
                complexity=["**Time O(n · (k mod n))**, up to O(n²). **Space O(1).**"],
                limits=["Each seat is moved k times by one place instead of once by k places."],
                slow=True,
            ),
            approach(
                "Copy into a second array",
                "better",
                "O(n)",
                "O(n)",
                idea=["Seat i goes to position `(i + k) mod n`. Write every seat directly there in a new array."],
                walk=w2,
                build=["`k %= n`.", "For each i: `out[(i + k) % n] = slots[i]`.", "Return `out`."],
                code={
                    "python": """
                        class Solution:
                            def rotateRight(self, slots: List[int], k: int) -> List[int]:
                                n = len(slots)
                                out = [0] * n  #@out
                                for i in range(n):  #@move
                                    out[(i + k) % n] = slots[i]  #@move
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] rotateRight(int[] slots, int k) {
                                int n = slots.length;
                                int[] out = new int[n];  //@out
                                for (int i = 0; i < n; i++) out[(int) ((i + (long) k) % n)] = slots[i];  //@move
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> rotateRight(vector<int>& slots, int k) {
                                int n = slots.size();
                                vector<int> out(n);  //@out
                                for (int i = 0; i < n; i++) out[(i + (long long) k) % n] = slots[i];  //@move
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* rotateRight(int* slots, int slotsSize, int k, int* returnSize) {
                            int n = slotsSize;
                            int* out = malloc(n * sizeof(int));  //@out
                            for (int i = 0; i < n; i++) out[(i + (long long) k) % n] = slots[i];  //@move
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("out", "A second array of the same size."), ("move", "Each seat jumps straight to its final position.", {"java": "`i + k` can pass 2³¹ when k is near 10⁹, so add in `long` before taking `% n`.", "cpp": "`i + k` can pass 2³¹ when k is near 10⁹, so add in `long long` before `% n`.", "c": "`i + k` can pass 2³¹ when k is near 10⁹, so add in `long long` before `% n`."}), ("ret", "The rotated order.")],
                complexity=["**Time O(n).** **Space O(n)** for the copy."],
                limits=["Needs a whole second array; the problem asks for O(1) extra space."],
            ),
            approach(
                "Three reversals",
                "best",
                "O(n)",
                "O(1)",
                idea=["With `k %= n`: reverse the whole array, then reverse the first k elements, then reverse the remaining n − k. The array was A B with |B| = k; the first reversal gives B' A' (both backwards); the next two give B A."],
                walk=w3,
                build=["`k %= n`.", "Reverse `[0, n − 1]`.", "Reverse `[0, k − 1]`.", "Reverse `[k, n − 1]`."],
                code={
                    "python": """
                        class Solution:
                            def rotateRight(self, slots: List[int], k: int) -> List[int]:
                                n = len(slots)
                                k %= n  #@mod
                                def rev(i, j):  #@rev
                                    while i < j:  #@rev
                                        slots[i], slots[j] = slots[j], slots[i]  #@rev
                                        i, j = i + 1, j - 1  #@rev
                                rev(0, n - 1)  #@three
                                rev(0, k - 1)  #@three
                                rev(k, n - 1)  #@three
                                return slots  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] rotateRight(int[] slots, int k) {
                                int n = slots.length;
                                k %= n;  //@mod
                                reverse(slots, 0, n - 1);  //@three
                                reverse(slots, 0, k - 1);  //@three
                                reverse(slots, k, n - 1);  //@three
                                return slots;  //@ret
                            }

                            private void reverse(int[] a, int i, int j) {  //@rev
                                for (; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@rev
                            }  //@rev
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> rotateRight(vector<int>& slots, int k) {
                                int n = slots.size();
                                k %= n;  //@mod
                                reverse(slots.begin(), slots.end());  //@three
                                reverse(slots.begin(), slots.begin() + k);  //@three
                                reverse(slots.begin() + k, slots.end());  //@three
                                return slots;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static void reverse(int* a, int i, int j) {  //@rev
                            for (; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }  //@rev
                        }  //@rev

                        int* rotateRight(int* slots, int slotsSize, int k, int* returnSize) {
                            int n = slotsSize;
                            k %= n;  //@mod
                            reverse(slots, 0, n - 1);  //@three
                            reverse(slots, 0, k - 1);  //@three
                            reverse(slots, k, n - 1);  //@three
                            *returnSize = n;  //@ret
                            return slots;  //@ret
                        }
                    """,
                },
                lines=[
                    ("mod", "Rotating by n changes nothing, so reduce k first (also keeps it a valid index)."),
                    ("rev", "Reverse a range in place with two pointers moving towards each other."),
                    ("three", "Whole array, then the first k, then the rest. With k = 0 the second reversal is empty and the other two cancel out.", {"cpp": "The standard `reverse` does the two-pointer swapping for us."}),
                    ("ret", "Rotated in place."),
                ],
                complexity=["**Time O(n):** every element is swapped about twice. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Rotation = swapping two blocks: **A B → B A**. In place: reverse all, then reverse each block.
            - Reduce shift amounts with `k mod n` first.
            - Rotate left by k is the same trick with the blocks split at k from the front.
            """
        ],
    )
