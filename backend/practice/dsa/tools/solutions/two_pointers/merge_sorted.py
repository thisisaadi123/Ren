"""Two Pointers: walking two sorted sequences together."""
from sol import L, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

C_CMP = """
                        static int cmp_int(const void* x, const void* y) {  //@sort
                            int a = *(const int*) x, b = *(const int*) y;  //@sort
                            return (a > b) - (a < b);  //@sort
                        }  //@sort
""".strip("\n")


@problem
def merge_two_shelves():
    left, right = [2, 5, 9, 12], [1, 5, 7, 15, 20]
    want = sorted(left + right)

    w1 = Steps("Put both shelves together and sort.")
    w1.step(f"Together: {left + right}.", Row(left + right))
    w1.step(f"Sorted: {want}.", Row(want), result=str(want))

    w2 = Steps("One pointer per shelf. Take the shorter front book each time (the left one on ties); when a shelf runs out, take the rest of the other.")
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1; side = "left"
        else:
            out.append(right[j]); j += 1; side = "right"
        w2.step(f"Take {out[-1]} from the {side} shelf.", Row(left, st={t: "mark" for t in range(i)}, ptr={"i": min(i, len(left) - 1)}, label="left"), Row(right, st={t: "mark" for t in range(j)}, ptr={"j": min(j, len(right) - 1)}, label="right"), Row(out, label="merged"))
    out += left[i:] + right[j:]
    w2.step(f"One shelf is empty; append the rest: {out}.", Row(out, label="merged"), result=str(out))

    sol(
        "merge-two-shelves",
        summary="""
            Both shelves are sorted, so the smallest remaining book is always at the front of one of them. Compare the two
            fronts, take the smaller, advance that pointer; when one shelf runs out, append the rest of the other.
            O(n + m).
        """,
        question=[
            """
            Merge two sorted lists into one sorted list.

            - **Either list can be empty** (but not both).
            - **Equal heights** can appear in both.
            - **Up to 10⁵ each.**
            """
        ],
        think=[
            f"""
            `{left}` and `{right}` merge into `{want}`.

            The first merged book must be the smaller of the two front books. After taking it, the same is true of what's
            left. So a single pass with one pointer per list builds the merge.
            """,
            fig(Row(left, label="left"), Row(right, label="right"), Row(want, label="merged")),
        ],
        approaches=[
            approach(
                "Concatenate and sort",
                "brute",
                "O((n + m) log(n + m))",
                "O(n + m)",
                idea=["Join the two lists and sort."],
                walk=w1,
                build=["Concatenate.", "Sort."],
                code={
                    "python": """
                        class Solution:
                            def mergeShelves(self, left: List[int], right: List[int]) -> List[int]:
                                return sorted(left + right)  #@sort
                    """,
                    "java": """
                        class Solution {
                            public int[] mergeShelves(int[] left, int[] right) {
                                int[] out = Arrays.copyOf(left, left.length + right.length);  //@sort
                                System.arraycopy(right, 0, out, left.length, right.length);  //@sort
                                Arrays.sort(out);  //@sort
                                return out;  //@sort
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> mergeShelves(vector<int>& left, vector<int>& right) {
                                vector<int> out = left;  //@sort
                                out.insert(out.end(), right.begin(), right.end());  //@sort
                                sort(out.begin(), out.end());  //@sort
                                return out;  //@sort
                            }
                        };
                    """,
                    "c": C_CMP + """

                        int* mergeShelves(int* left, int leftSize, int* right, int rightSize, int* returnSize) {
                            int n = leftSize + rightSize;  //@sort
                            int* out = malloc(n * sizeof(int));  //@sort
                            memcpy(out, left, leftSize * sizeof(int));  //@sort
                            memcpy(out + leftSize, right, rightSize * sizeof(int));  //@sort
                            qsort(out, n, sizeof(int), cmp_int);  //@sort
                            *returnSize = n;  //@sort
                            return out;  //@sort
                        }
                    """,
                },
                lines=[("sort", "Everything together, then a general sort.")],
                complexity=["**Time O((n + m) log(n + m)).** **Space O(n + m).**"],
                limits=["Throws away the fact that each shelf is already sorted. Merging uses it to finish in one linear pass."],
            ),
            approach(
                "Merge with two pointers",
                "best",
                "O(n + m)",
                "O(n + m)",
                idea=["`i` on `left`, `j` on `right`. While both have books, append the smaller front (`left` on ties). Then append the remainder."],
                walk=w2,
                build=["Two pointers and an output.", "Take the smaller front.", "Append leftovers."],
                code={
                    "python": """
                        class Solution:
                            def mergeShelves(self, left: List[int], right: List[int]) -> List[int]:
                                out, i, j = [], 0, 0  #@init
                                while i < len(left) and j < len(right):  #@merge
                                    if left[i] <= right[j]:  #@merge
                                        out.append(left[i]); i += 1  #@merge
                                    else:  #@merge
                                        out.append(right[j]); j += 1  #@merge
                                out.extend(left[i:])  #@rest
                                out.extend(right[j:])  #@rest
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] mergeShelves(int[] left, int[] right) {
                                int[] out = new int[left.length + right.length];  //@init
                                int i = 0, j = 0, k = 0;  //@init
                                while (i < left.length && j < right.length) out[k++] = left[i] <= right[j] ? left[i++] : right[j++];  //@merge
                                while (i < left.length) out[k++] = left[i++];  //@rest
                                while (j < right.length) out[k++] = right[j++];  //@rest
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> mergeShelves(vector<int>& left, vector<int>& right) {
                                vector<int> out;  //@init
                                size_t i = 0, j = 0;  //@init
                                while (i < left.size() && j < right.size()) out.push_back(left[i] <= right[j] ? left[i++] : right[j++]);  //@merge
                                while (i < left.size()) out.push_back(left[i++]);  //@rest
                                while (j < right.size()) out.push_back(right[j++]);  //@rest
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* mergeShelves(int* left, int leftSize, int* right, int rightSize, int* returnSize) {
                            int* out = malloc((leftSize + rightSize) * sizeof(int));  //@init
                            int i = 0, j = 0, k = 0;  //@init
                            while (i < leftSize && j < rightSize) out[k++] = left[i] <= right[j] ? left[i++] : right[j++];  //@merge
                            while (i < leftSize) out[k++] = left[i++];  //@rest
                            while (j < rightSize) out[k++] = right[j++];  //@rest
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "Output and one pointer per shelf."), ("merge", "The smaller front is the next smallest book overall; `<=` takes from the left first on ties."), ("rest", "One shelf ran out; the other's remaining books are all larger and already in order."), ("ret", "Merged.")],
                complexity=["**Time O(n + m).** **Space O(n + m)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Merging two sorted lists:** compare fronts, take the smaller, linear time.
            - It's the step merge sort is built on, and it extends to k lists with a heap.
            - Don't forget the leftovers after the loop.
            """
        ],
    )


@problem
def merge_two_train_lines():
    first, second = [1, 4, 6], [2, 3, 6, 9]
    want = sorted(first + second)

    w1 = Steps("Read every car number into an array, sort it, and build a brand-new train.")
    w1.step("Read both trains.", L(first, label="first"), L(second, label="second"), Row(first + second, label="array"))
    w1.step(f"Sort and build new cars: {want}.", L(want, label="new train"), result=str(want))

    w2 = Steps("Splice the existing cars: a tail pointer links whichever front car has the smaller number.")
    a, b, out = first[:], second[:], []
    while a and b:
        if a[0] <= b[0]:
            out.append(a.pop(0)); side = "first"
        else:
            out.append(b.pop(0)); side = "second"
        w2.step(f"Link car {out[-1]} from the {side} train.", L(out, st={len(out) - 1: "new"}, label="merged"), L(a or ["·"], label="first"), L(b or ["·"], label="second"))
    out += a + b
    w2.step(f"One train is empty: link the rest in one step. {out}.", L(out, label="merged"), result=str(want))

    sol(
        "merge-two-train-lines",
        summary="""
            Merge by relinking: a dummy node starts the result, and a tail pointer links whichever front car has the
            smaller number, then advances. When one train runs out, link the other's remainder in one step. O(n + m) time,
            O(1) extra space, no new cars.
        """,
        question=[
            """
            Merge two sorted linked lists into one sorted list, **reusing the existing nodes**, and return its head.

            - **Either list can be empty** (or both).
            - **Up to 5 × 10⁴ nodes each.**
            """
        ],
        think=[
            f"""
            `{first}` and `{second}` become `{want}`.

            It's the array merge, but instead of copying values into an output, we change `next` pointers. A dummy head
            avoids special-casing the first node: the merged list is whatever follows the dummy.
            """,
            fig(L(first, label="first"), L(second, label="second")),
        ],
        approaches=[
            approach(
                "Copy, sort, rebuild",
                "brute",
                "O((n + m) log(n + m))",
                "O(n + m)",
                idea=["Collect all values, sort them, and create a new list."],
                walk=w1,
                build=["Collect values from both lists.", "Sort.", "Build new nodes."],
                code={
                    "python": """
                        class Solution:
                            def mergeLines(self, first: Optional[ListNode], second: Optional[ListNode]) -> Optional[ListNode]:
                                vals = []  #@read
                                for node in (first, second):  #@read
                                    while node:  #@read
                                        vals.append(node.val)  #@read
                                        node = node.next  #@read
                                vals.sort()  #@sort
                                dummy = tail = ListNode()  #@build
                                for v in vals:  #@build
                                    tail.next = ListNode(v)  #@build
                                    tail = tail.next  #@build
                                return dummy.next  #@ret
                    """,
                    "java": """
                        class Solution {
                            public ListNode mergeLines(ListNode first, ListNode second) {
                                List<Integer> vals = new ArrayList<>();  //@read
                                for (ListNode n = first; n != null; n = n.next) vals.add(n.val);  //@read
                                for (ListNode n = second; n != null; n = n.next) vals.add(n.val);  //@read
                                Collections.sort(vals);  //@sort
                                ListNode dummy = new ListNode(), tail = dummy;  //@build
                                for (int v : vals) { tail.next = new ListNode(v); tail = tail.next; }  //@build
                                return dummy.next;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            ListNode* mergeLines(ListNode* first, ListNode* second) {
                                vector<int> vals;  //@read
                                for (ListNode* n = first; n; n = n->next) vals.push_back(n->val);  //@read
                                for (ListNode* n = second; n; n = n->next) vals.push_back(n->val);  //@read
                                sort(vals.begin(), vals.end());  //@sort
                                ListNode dummy;  //@build
                                ListNode* tail = &dummy;  //@build
                                for (int v : vals) { tail->next = new ListNode(v); tail = tail->next; }  //@build
                                return dummy.next;  //@ret
                            }
                        };
                    """,
                    "c": C_CMP + """

                        struct ListNode* mergeLines(struct ListNode* first, struct ListNode* second) {
                            int n = 0;  //@read
                            for (struct ListNode* p = first; p; p = p->next) n++;  //@read
                            for (struct ListNode* p = second; p; p = p->next) n++;  //@read
                            int* vals = malloc((n + 1) * sizeof(int));  //@read
                            int k = 0;  //@read
                            for (struct ListNode* p = first; p; p = p->next) vals[k++] = p->val;  //@read
                            for (struct ListNode* p = second; p; p = p->next) vals[k++] = p->val;  //@read
                            qsort(vals, n, sizeof(int), cmp_int);  //@sort
                            struct ListNode dummy = {0, NULL}, *tail = &dummy;  //@build
                            for (int i = 0; i < n; i++) {  //@build
                                tail->next = malloc(sizeof(struct ListNode));  //@build
                                tail = tail->next;  //@build
                                tail->val = vals[i];  //@build
                                tail->next = NULL;  //@build
                            }
                            free(vals);  //@ret
                            return dummy.next;  //@ret
                        }
                    """,
                },
                lines=[("read", "Every value from both trains."), ("sort", "Sort them."), ("build", "A new car for each value."), ("ret", "The new train.")],
                complexity=["**Time O((n + m) log(n + m)).** **Space O(n + m)** for the values and new nodes."],
                limits=["Builds new cars instead of reusing them, and sorts data that is already in two sorted runs. Relinking merges in one pass with no new nodes."],
            ),
            approach(
                "Splice with a dummy head",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`tail` starts at a dummy node. While both lists have nodes, link the smaller front to `tail.next` and advance it and `tail`. Then link whichever list is left."],
                walk=w2,
                build=["Dummy node and tail.", "Link the smaller front.", "Link the remainder."],
                code={
                    "python": """
                        class Solution:
                            def mergeLines(self, first: Optional[ListNode], second: Optional[ListNode]) -> Optional[ListNode]:
                                dummy = tail = ListNode()  #@init
                                a, b = first, second  #@init
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
                            public ListNode mergeLines(ListNode first, ListNode second) {
                                ListNode dummy = new ListNode(), tail = dummy;  //@init
                                ListNode a = first, b = second;  //@init
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
                            ListNode* mergeLines(ListNode* first, ListNode* second) {
                                ListNode dummy;  //@init
                                ListNode *tail = &dummy, *a = first, *b = second;  //@init
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
                        struct ListNode* mergeLines(struct ListNode* first, struct ListNode* second) {
                            struct ListNode dummy = {0, NULL}, *tail = &dummy;  //@init
                            struct ListNode *a = first, *b = second;  //@init
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
                lines=[("init", "A dummy node before the result, and the tail of the merged part."), ("merge", "Link the smaller front car and move on in that train; the tail follows."), ("rest", "Whatever remains is already sorted: link it all at once."), ("ret", "The merged train starts after the dummy.")],
                complexity=["**Time O(n + m).** **Space O(1)** extra: only pointers change."],
            ),
        ],
        takeaways=[
            """
            - **Linked-list merge = array merge with pointer splicing**, O(1) extra space.
            - A dummy head removes the "which node is first?" special case.
            - The leftover list attaches in one step.
            """
        ],
    )


@problem
def closest_across_lists():
    a, b = [1, 7, 15, 30], [4, 12, 19, 28, 40]
    want = min(abs(x - y) for x in a for y in b)

    w1 = Steps("Compare every value of a with every value of b.")
    for i, x in enumerate(a):
        bj = min(range(len(b)), key=lambda j: abs(x - b[j]))
        w1.step(f"{x}: the closest in b is {b[bj]} (difference {abs(x - b[bj])}).", Row(a, st={i: "active"}, label="a"), Row(b, st={bj: "found"}, label="b"))
    w1.step(f"Smallest difference: {want}.", result=want)

    w2 = Steps("For each value in a, binary-search b for where it would go; only the neighbours on either side can be closest.")
    import bisect
    best = None
    for i, x in enumerate(a):
        p = bisect.bisect_left(b, x)
        cands = [b[q] for q in (p - 1, p) if 0 <= q < len(b)]
        d = min(abs(x - y) for y in cands)
        best = d if best is None else min(best, d)
        w2.step(f"{x} would go at position {p} in b: check {cands}. Best so far {best}.", Row(a, st={i: "active"}, label="a"), Row(b, st={q: "found" for q in (p - 1, p) if 0 <= q < len(b)}, label="b"))
    w2.step(f"Smallest difference: {best}.", result=best)

    w3 = Steps("Walk both lists together: compare the fronts, then advance the pointer at the smaller value (moving the larger one would only widen the gap).")
    i = j = 0
    best = abs(a[0] - b[0])
    while i < len(a) and j < len(b):
        best = min(best, abs(a[i] - b[j]))
        w3.step(f"|{a[i]} − {b[j]}| = {abs(a[i] - b[j])}. Best {best}. Advance the {'a' if a[i] < b[j] else 'b'} pointer.", Row(a, st={i: "active"}, label="a"), Row(b, st={j: "active"}, label="b"), Vars(best=best))
        if a[i] < b[j]:
            i += 1
        else:
            j += 1
    w3.step(f"One list is used up. Smallest difference: {best}.", result=best)

    sol(
        "closest-across-lists",
        summary="""
            Walk both sorted lists together. Compare `a[i]` with `b[j]` and record the difference; then advance the pointer
            at the smaller value, since moving the larger one could only make the gap wider. O(n + m).
        """,
        question=[
            """
            Pick one value from each sorted list to minimise `|a[i] − b[j]|`. Return that minimum.

            - **Values up to ±10⁹**: differences reach 2 × 10⁹, which still fits a signed 32-bit result but should be
              computed in 64 bits.
            - **Up to 10⁵ values each.**
            """
        ],
        think=[
            f"""
            `a = {a}`, `b = {b}`. The closest pair is 30 and 28: **{want}**.

            Suppose `a[i] < b[j]`. Pairing `b[j]` with any later `b` value only moves further from `a[i]`, so `a[i]` has
            already met its best partner on this side; the only way to find a closer pair is to raise `a[i]`. So advance
            the smaller one, exactly like merging.
            """,
            fig(Row(a, label="a"), Row(b, label="b")),
        ],
        approaches=[
            approach(
                "Every pair",
                "brute",
                "O(n·m)",
                "O(1)",
                idea=["Compute `|a[i] − b[j]|` for all pairs; keep the minimum."],
                walk=w1,
                build=["Double loop.", "64-bit differences."],
                code={
                    "python": """
                        class Solution:
                            def closestAcross(self, a: List[int], b: List[int]) -> int:
                                return min(abs(x - y) for x in a for y in b)  #@pairs
                    """,
                    "java": """
                        class Solution {
                            public int closestAcross(int[] a, int[] b) {
                                long best = Long.MAX_VALUE;  //@pairs
                                for (int x : a) for (int y : b) best = Math.min(best, Math.abs((long) x - y));  //@pairs
                                return (int) best;  //@pairs
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestAcross(vector<int>& a, vector<int>& b) {
                                long long best = LLONG_MAX;  //@pairs
                                for (int x : a) for (int y : b) best = min(best, llabs((long long) x - y));  //@pairs
                                return (int) best;  //@pairs
                            }
                        };
                    """,
                    "c": """
                        int closestAcross(int* a, int aSize, int* b, int bSize) {
                            long long best = LLONG_MAX;  //@pairs
                            for (int i = 0; i < aSize; i++)  //@pairs
                                for (int j = 0; j < bSize; j++)  //@pairs
                                    if (llabs((long long) a[i] - b[j]) < best) best = llabs((long long) a[i] - b[j]);  //@pairs
                            return (int) best;  //@pairs
                        }
                    """,
                },
                lines=[("pairs", "Every pair's distance, in 64 bits; the smallest fits in an `int`.")],
                complexity=["**Time O(n·m)**, up to 10¹⁰. **Space O(1).**"],
                limits=["Ignores that both lists are sorted. For each value only its neighbours in the other list matter, which binary search or a merge-style walk finds."],
                slow=True,
            ),
            approach(
                "Binary search for each value",
                "better",
                "O(n log m)",
                "O(1)",
                idea=["For each `x` in `a`, find the first `b[p] ≥ x`; the closest value in `b` is `b[p]` or `b[p − 1]`."],
                walk=w2,
                build=["Lower-bound search in `b` for each `x`.", "Check both neighbours.", "Keep the minimum."],
                code={
                    "python": """
                        import bisect

                        class Solution:
                            def closestAcross(self, a: List[int], b: List[int]) -> int:
                                best = abs(a[0] - b[0])  #@init
                                for x in a:  #@search
                                    p = bisect.bisect_left(b, x)  #@search
                                    if p < len(b):  #@near
                                        best = min(best, b[p] - x)  #@near
                                    if p > 0:  #@near
                                        best = min(best, x - b[p - 1])  #@near
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestAcross(int[] a, int[] b) {
                                long best = Math.abs((long) a[0] - b[0]);  //@init
                                for (int x : a) {  //@search
                                    int lo = 0, hi = b.length;  //@search
                                    while (lo < hi) { int mid = (lo + hi) >>> 1; if (b[mid] < x) lo = mid + 1; else hi = mid; }  //@search
                                    if (lo < b.length) best = Math.min(best, (long) b[lo] - x);  //@near
                                    if (lo > 0) best = Math.min(best, (long) x - b[lo - 1]);  //@near
                                }
                                return (int) best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestAcross(vector<int>& a, vector<int>& b) {
                                long long best = llabs((long long) a[0] - b[0]);  //@init
                                for (int x : a) {  //@search
                                    int p = lower_bound(b.begin(), b.end(), x) - b.begin();  //@search
                                    if (p < (int) b.size()) best = min(best, (long long) b[p] - x);  //@near
                                    if (p > 0) best = min(best, (long long) x - b[p - 1]);  //@near
                                }
                                return (int) best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int closestAcross(int* a, int aSize, int* b, int bSize) {
                            long long best = llabs((long long) a[0] - b[0]);  //@init
                            for (int i = 0; i < aSize; i++) {  //@search
                                int lo = 0, hi = bSize;  //@search
                                while (lo < hi) { int mid = (lo + hi) / 2; if (b[mid] < a[i]) lo = mid + 1; else hi = mid; }  //@search
                                if (lo < bSize && (long long) b[lo] - a[i] < best) best = (long long) b[lo] - a[i];  //@near
                                if (lo > 0 && (long long) a[i] - b[lo - 1] < best) best = (long long) a[i] - b[lo - 1];  //@near
                            }
                            return (int) best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Any pair gives a starting answer."), ("search", "Where `x` would sit in `b`: the first `b[p] ≥ x`."), ("near", "The closest `b` value is just above (`b[p]`) or just below (`b[p − 1]`) that spot."), ("ret", "The smallest gap.")],
                complexity=["**Time O(n log m).** **Space O(1).**"],
                limits=["Each search starts from scratch, but as `x` grows its position in `b` only moves right. A single merge-style walk reuses that progress: O(n + m)."],
            ),
            approach(
                "Walk both lists together",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`i = j = 0`. Record `|a[i] − b[j]|`; advance the pointer at the smaller value. Stop when either list ends."],
                walk=w3,
                build=["Pointers at both starts.", "Record the gap.", "Advance the smaller side."],
                code={
                    "python": """
                        class Solution:
                            def closestAcross(self, a: List[int], b: List[int]) -> int:
                                i = j = 0  #@init
                                best = abs(a[0] - b[0])  #@init
                                while i < len(a) and j < len(b):  #@walk
                                    best = min(best, abs(a[i] - b[j]))  #@walk
                                    if a[i] < b[j]:  #@move
                                        i += 1  #@move
                                    else:  #@move
                                        j += 1  #@move
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int closestAcross(int[] a, int[] b) {
                                int i = 0, j = 0;  //@init
                                long best = Math.abs((long) a[0] - b[0]);  //@init
                                while (i < a.length && j < b.length) {  //@walk
                                    best = Math.min(best, Math.abs((long) a[i] - b[j]));  //@walk
                                    if (a[i] < b[j]) i++;  //@move
                                    else j++;  //@move
                                }
                                return (int) best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int closestAcross(vector<int>& a, vector<int>& b) {
                                size_t i = 0, j = 0;  //@init
                                long long best = llabs((long long) a[0] - b[0]);  //@init
                                while (i < a.size() && j < b.size()) {  //@walk
                                    best = min(best, llabs((long long) a[i] - b[j]));  //@walk
                                    if (a[i] < b[j]) i++;  //@move
                                    else j++;  //@move
                                }
                                return (int) best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int closestAcross(int* a, int aSize, int* b, int bSize) {
                            int i = 0, j = 0;  //@init
                            long long best = llabs((long long) a[0] - b[0]);  //@init
                            while (i < aSize && j < bSize) {  //@walk
                                long long d = llabs((long long) a[i] - b[j]);  //@walk
                                if (d < best) best = d;  //@walk
                                if (a[i] < b[j]) i++;  //@move
                                else j++;  //@move
                            }
                            return (int) best;  //@ret
                        }
                    """,
                },
                lines=[("init", "Pointers at the starts; the first pair's gap."), ("walk", "Record the current gap (64-bit)."), ("move", "Raise the smaller value: the larger one can only drift further away from it."), ("ret", "The smallest gap.")],
                complexity=["**Time O(n + m).** **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Two sorted lists → walk them together**, advancing the smaller side.
            - The binary-search version is a good stepping stone and works when one list is much longer.
            - Compute differences in 64 bits near the 32-bit limits.
            """
        ],
    )


@problem
def pairs_within_budget():
    mains, sides, budget = [5, 8, 12, 20], [2, 4, 9, 11], 16
    want = sum(1 for x in mains for y in sides if x + y <= budget)

    w1 = Steps("Check every (main, side) combination.")
    for i, x in enumerate(mains):
        ok = [y for y in sides if x + y <= budget]
        w1.step(f"Main {x}: {len(ok)} side(s) fit ({ok}).", Row(mains, st={i: "active"}, label="mains"), Row(sides, st={j: "found" for j, y in enumerate(sides) if x + y <= budget}, label="sides"))
    w1.step(f"Total: {want}.", result=want)

    w2 = Steps("For each main, binary-search how many sides cost at most budget − main.")
    import bisect
    total = 0
    for i, x in enumerate(mains):
        c = bisect.bisect_right(sides, budget - x)
        total += c
        w2.step(f"Main {x}: sides ≤ {budget - x} are the first {c}.", Row(mains, st={i: "active"}, label="mains"), Row(sides, st={j: "found" for j in range(c)}, label="sides"), Vars(total=total))
    w2.step(f"Total: {total}.", result=total)

    w3 = Steps("Cheapest main first, with a pointer on the dearest side that still fits. As mains get pricier, the pointer only moves left.")
    total, j = 0, len(sides) - 1
    for i, x in enumerate(mains):
        while j >= 0 and x + sides[j] > budget:
            j -= 1
        total += j + 1
        w3.step(f"Main {x}: the pointer settles on {'side ' + str(sides[j]) if j >= 0 else 'nothing'}, so {j + 1} side(s) fit.", Row(mains, st={i: "active"}, label="mains"), Row(sides, st={t: "found" for t in range(j + 1)}, ptr={"j": max(j, 0)}, label="sides"), Vars(total=total))
    w3.step(f"Total: {total}.", result=total)

    sol(
        "pairs-within-budget",
        summary="""
            For the cheapest main, find the dearest side that still fits; every cheaper side fits too. As mains get
            pricier, that boundary can only move toward cheaper sides, so one pointer sweeping down the sides handles all
            mains: O(n + m). The count can exceed 2³¹, so use 64 bits.
        """,
        question=[
            """
            Count (main, side) pairs with `main + side ≤ budget`. Both price lists are sorted.

            - **Up to 10⁵ of each**: up to 10¹⁰ pairs, so the count needs 64 bits.
            - Prices up to 10⁹: sums up to 2 × 10⁹, use 64-bit sums.
            """
        ],
        think=[
            f"""
            Mains `{mains}`, sides `{sides}`, budget {budget}: **{want}** pairs fit.

            For a fixed main, the sides that fit form a prefix of the sorted sides (all prices up to `budget − main`).
            The prefix length is what we add. And when the main gets more expensive, the allowed prefix can only shrink, so
            the boundary pointer never needs to move back.
            """,
            fig(Row(mains, label="mains"), Row(sides, label="sides")),
        ],
        approaches=[
            approach(
                "Every combination",
                "brute",
                "O(n·m)",
                "O(1)",
                idea=["Count every pair whose total is within budget."],
                walk=w1,
                build=["Double loop.", "64-bit sums and count."],
                code={
                    "python": """
                        class Solution:
                            def countPairsWithin(self, mains: List[int], sides: List[int], budget: int) -> int:
                                return sum(1 for x in mains for y in sides if x + y <= budget)  #@pairs
                    """,
                    "java": """
                        class Solution {
                            public long countPairsWithin(int[] mains, int[] sides, int budget) {
                                long count = 0;  //@pairs
                                for (int x : mains) for (int y : sides) if ((long) x + y <= budget) count++;  //@pairs
                                return count;  //@pairs
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countPairsWithin(vector<int>& mains, vector<int>& sides, int budget) {
                                long long count = 0;  //@pairs
                                for (int x : mains) for (int y : sides) if ((long long) x + y <= budget) count++;  //@pairs
                                return count;  //@pairs
                            }
                        };
                    """,
                    "c": """
                        long long countPairsWithin(int* mains, int mainsSize, int* sides, int sidesSize, int budget) {
                            long long count = 0;  //@pairs
                            for (int i = 0; i < mainsSize; i++)  //@pairs
                                for (int j = 0; j < sidesSize; j++)  //@pairs
                                    if ((long long) mains[i] + sides[j] <= budget) count++;  //@pairs
                            return count;  //@pairs
                        }
                    """,
                },
                lines=[("pairs", "Every pair, with a 64-bit sum and count.")],
                complexity=["**Time O(n·m).** **Space O(1).**"],
                limits=["Up to 10¹⁰ pairs. The fitting sides form a prefix, so we can count them without visiting them."],
                slow=True,
            ),
            approach(
                "Binary search per main",
                "better",
                "O(n log m)",
                "O(1)",
                idea=["For each main `x`, count sides `≤ budget − x` with an upper-bound binary search."],
                walk=w2,
                build=["Upper-bound search for `budget − x`.", "Add the count."],
                code={
                    "python": """
                        import bisect

                        class Solution:
                            def countPairsWithin(self, mains: List[int], sides: List[int], budget: int) -> int:
                                total = 0  #@init
                                for x in mains:  #@search
                                    total += bisect.bisect_right(sides, budget - x)  #@search
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countPairsWithin(int[] mains, int[] sides, int budget) {
                                long total = 0;  //@init
                                for (int x : mains) {  //@search
                                    long cap = (long) budget - x;  //@search
                                    int lo = 0, hi = sides.length;  //@search
                                    while (lo < hi) { int mid = (lo + hi) >>> 1; if (sides[mid] <= cap) lo = mid + 1; else hi = mid; }  //@search
                                    total += lo;  //@search
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countPairsWithin(vector<int>& mains, vector<int>& sides, int budget) {
                                long long total = 0;  //@init
                                for (int x : mains) {  //@search
                                    long long cap = (long long) budget - x;  //@search
                                    total += upper_bound(sides.begin(), sides.end(), cap, [](long long c, int s) { return c < s; }) - sides.begin();  //@search
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countPairsWithin(int* mains, int mainsSize, int* sides, int sidesSize, int budget) {
                            long long total = 0;  //@init
                            for (int i = 0; i < mainsSize; i++) {  //@search
                                long long cap = (long long) budget - mains[i];  //@search
                                int lo = 0, hi = sidesSize;  //@search
                                while (lo < hi) { int mid = (lo + hi) / 2; if (sides[mid] <= cap) lo = mid + 1; else hi = mid; }  //@search
                                total += lo;  //@search
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "The running count (64-bit)."), ("search", "The number of sides that cost at most `budget − x`: the first index with a bigger price."), ("ret", "Total.")],
                complexity=["**Time O(n log m).** **Space O(1).**"],
                limits=["Each search restarts, even though the boundary only moves one way as mains grow. A single sweeping pointer makes it linear."],
            ),
            approach(
                "One sweeping pointer",
                "best",
                "O(n + m)",
                "O(1)",
                idea=["`j` starts at the dearest side. For each main from cheapest to dearest, move `j` left while `main + sides[j] > budget`; add `j + 1`."],
                walk=w3,
                build=["`j` at the last side.", "Shrink while over budget.", "Add the prefix length."],
                code={
                    "python": """
                        class Solution:
                            def countPairsWithin(self, mains: List[int], sides: List[int], budget: int) -> int:
                                total, j = 0, len(sides) - 1  #@init
                                for x in mains:  #@loop
                                    while j >= 0 and x + sides[j] > budget:  #@shrink
                                        j -= 1  #@shrink
                                    total += j + 1  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countPairsWithin(int[] mains, int[] sides, int budget) {
                                long total = 0;  //@init
                                int j = sides.length - 1;  //@init
                                for (int x : mains) {  //@loop
                                    while (j >= 0 && (long) x + sides[j] > budget) j--;  //@shrink
                                    total += j + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countPairsWithin(vector<int>& mains, vector<int>& sides, int budget) {
                                long long total = 0;  //@init
                                int j = (int) sides.size() - 1;  //@init
                                for (int x : mains) {  //@loop
                                    while (j >= 0 && (long long) x + sides[j] > budget) j--;  //@shrink
                                    total += j + 1;  //@add
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countPairsWithin(int* mains, int mainsSize, int* sides, int sidesSize, int budget) {
                            long long total = 0;  //@init
                            int j = sidesSize - 1;  //@init
                            for (int i = 0; i < mainsSize; i++) {  //@loop
                                while (j >= 0 && (long long) mains[i] + sides[j] > budget) j--;  //@shrink
                                total += j + 1;  //@add
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[("init", "Count, and `j` on the dearest side."), ("loop", "Mains from cheapest to dearest."), ("shrink", "Drop sides that no longer fit with this (or any pricier) main."), ("add", "Sides `0..j` all fit."), ("ret", "Total (64-bit).")],
                complexity=["**Time O(n + m):** `j` only moves left. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - **Counting pairs under a bound across two sorted lists:** one pointer per list, moving monotonically.
            - When a boundary only moves one way, a sweep beats repeated binary searches.
            - Counts of pairs can exceed 32 bits.
            """
        ],
    )
