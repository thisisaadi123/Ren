"""Two Pointers: a read pointer and a write pointer over the same array."""
from sol import Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def rw_walk(title, values, keep, desc):
    """Narrate a read/write pass; keep(a, w, x) decides whether x is kept."""
    w = Steps(title)
    a = values[:]
    wr = 0
    for r, x in enumerate(values):
        if keep(a, wr, x):
            a[wr] = x
            w.step(f"Read {x}: {desc(True, x)}, write it at {wr}.", Row(a, st={**{t: "found" for t in range(wr + 1)}}, ptr={"read": r, "write": wr}))
            wr += 1
        else:
            w.step(f"Read {x}: {desc(False, x)}, skip it.", Row(a, st={t: "found" for t in range(wr)}, ptr={"read": r, "write": wr}))
    return w, a[:wr]


@problem
def remove_the_blanks():
    cells, blank = [4, 0, 7, 0, 0, 3, 8], 0
    want = [x for x in cells if x != blank]

    w1 = Steps("Find a blank, delete it by shifting everything after it one place left, and repeat.")
    a = cells[:]
    w1.step("Start.", Row(a))
    while blank in a:
        i = a.index(blank)
        w1.step(f"Blank at {i}: shift the {len(a) - i - 1} cells after it left.", Row(a, st={i: "mark"}))
        a.pop(i)
    w1.step(f"Left: {a}.", Row(a), result=str(a))
    w2, got = rw_walk("A read pointer visits every cell; a write pointer marks where the next kept cell goes.", cells, lambda a, w, x: x != blank, lambda k, x: "not blank" if k else "blank")
    w2.step(f"The first {len(got)} cells are the answer: {got}.", result=str(got))

    sol(
        "remove-the-blanks",
        summary="""
            Use two pointers on the same array: `read` visits every cell, `write` marks the end of the kept part. Each
            non-blank cell is copied to `write`, which then advances. The first `write` cells are the answer, in order.
            O(n) time, O(1) extra space.
        """,
        question=[
            """
            Remove every cell equal to `blank`, keep the others in order, and return them, ideally in place.

            - **Order matters**: the kept cells stay in their original order.
            - **Up to 10⁵ cells.**
            """
        ],
        think=[
            f"""
            `{cells}` with blank {blank} → `{want}`.

            Deleting a blank by shifting the rest left is O(n) each time. Instead, notice that every kept cell only ever
            moves **left**, to the next free spot in the kept prefix. A write pointer tracks that spot; it never overtakes
            the read pointer, so we never overwrite a cell we haven't read yet.
            """,
            fig(Row(cells, label="cells"), Row(want, label="kept")),
        ],
        approaches=[
            approach(
                "Delete by shifting",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["While a blank exists, remove it by shifting every later cell left one place."],
                walk=w1,
                build=["Scan for a blank.", "Shift the tail left.", "Repeat."],
                code={
                    "python": """
                        class Solution:
                            def removeValue(self, cells: List[int], blank: int) -> List[int]:
                                a, n, i = cells[:], len(cells), 0  #@init
                                while i < n:  #@scan
                                    if a[i] == blank:  #@shift
                                        for j in range(i, n - 1):  #@shift
                                            a[j] = a[j + 1]  #@shift
                                        n -= 1  #@shift
                                    else:  #@scan
                                        i += 1  #@scan
                                return a[:n]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] removeValue(int[] cells, int blank) {
                                int[] a = cells.clone();  //@init
                                int n = a.length, i = 0;  //@init
                                while (i < n) {  //@scan
                                    if (a[i] == blank) {  //@shift
                                        for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                        n--;  //@shift
                                    } else i++;  //@scan
                                }
                                return Arrays.copyOf(a, n);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> removeValue(vector<int>& cells, int blank) {
                                vector<int> a = cells;  //@init
                                int n = a.size(), i = 0;  //@init
                                while (i < n) {  //@scan
                                    if (a[i] == blank) {  //@shift
                                        for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                        n--;  //@shift
                                    } else i++;  //@scan
                                }
                                a.resize(n);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* removeValue(int* cells, int cellsSize, int blank, int* returnSize) {
                            int* a = malloc(cellsSize * sizeof(int));  //@init
                            memcpy(a, cells, cellsSize * sizeof(int));  //@init
                            int n = cellsSize, i = 0;  //@init
                            while (i < n) {  //@scan
                                if (a[i] == blank) {  //@shift
                                    for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                    n--;  //@shift
                                } else i++;  //@scan
                            }
                            *returnSize = n;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy and its live length."), ("scan", "Move on past kept cells."), ("shift", "Delete the blank: everything after it moves one place left. Don't advance `i`: a new cell has arrived there."), ("ret", "The live part.")],
                complexity=["**Time O(n²)** with many blanks. **Space O(1)** beyond the copy."],
                limits=["Each deletion shifts the whole tail. Writing each kept cell straight to its final spot moves every cell at most once."],
                slow=True,
            ),
            approach(
                "Read and write pointers",
                "best",
                "O(n)",
                "O(1)",
                idea=["`write = 0`. For each cell (the read pointer), if it isn't blank, copy it to `a[write]` and advance `write`. Return the first `write` cells."],
                walk=w2,
                build=["Copy; `write = 0`.", "Copy kept cells forward.", "Trim to `write`."],
                code={
                    "python": """
                        class Solution:
                            def removeValue(self, cells: List[int], blank: int) -> List[int]:
                                a, write = cells[:], 0  #@init
                                for x in cells:  #@read
                                    if x != blank:  #@keep
                                        a[write] = x  #@keep
                                        write += 1  #@keep
                                return a[:write]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] removeValue(int[] cells, int blank) {
                                int[] a = cells.clone();  //@init
                                int write = 0;  //@init
                                for (int x : cells)  //@read
                                    if (x != blank) a[write++] = x;  //@keep
                                return Arrays.copyOf(a, write);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> removeValue(vector<int>& cells, int blank) {
                                vector<int> a = cells;  //@init
                                int write = 0;  //@init
                                for (int x : cells)  //@read
                                    if (x != blank) a[write++] = x;  //@keep
                                a.resize(write);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* removeValue(int* cells, int cellsSize, int blank, int* returnSize) {
                            int* a = malloc(cellsSize * sizeof(int));  //@init
                            int write = 0;  //@init
                            for (int i = 0; i < cellsSize; i++)  //@read
                                if (cells[i] != blank) a[write++] = cells[i];  //@keep
                            *returnSize = write;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "`write` = how many cells are kept so far, and where the next one goes."), ("read", "Every cell, in order."), ("keep", "A kept cell moves to the end of the kept part. `write ≤ read` always, so nothing unread is overwritten."), ("ret", "The kept prefix.")],
                complexity=["**Time O(n).** **Space O(1)** extra (in place)."],
            ),
        ],
        takeaways=[
            """
            - **Filter in place = read pointer + write pointer.** Kept items move left to `write`.
            - `write` never passes `read`, so in-place copying is safe.
            - The same skeleton dedups, compacts and filters arrays.
            """
        ],
    )


@problem
def compact_the_shelf():
    slots = [0, 5, 0, 0, 3, 9, 0, 2]
    items = [x for x in slots if x != 0]
    want = items + [0] * (len(slots) - len(items))

    w1 = Steps("Bubble each empty slot to the right by swapping it with the item next to it, pass after pass.")
    a = slots[:]
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] == 0 and a[i + 1] != 0:
                a[i], a[i + 1] = a[i + 1], a[i]
                changed = True
        w1.step("One pass of swapping empties rightward.", Row(a))
    w1.step(f"Done: {a}.", result=str(a))
    w2, got = rw_walk("Read every slot; write each item at the next free position on the left. Then fill the rest with empties.", slots, lambda a, w, x: x != 0, lambda k, x: "an item" if k else "empty")
    w2.step(f"Fill positions {len(got)}.. with 0: {want}.", Row(want, st={t: "found" for t in range(len(got))}), result=str(want))

    sol(
        "compact-the-shelf",
        summary="""
            Read every slot; copy each item to the next free position from the left (a write pointer), keeping their order.
            When the read is done, everything from the write pointer to the end becomes empty (0). O(n), in place.
        """,
        question=[
            """
            Slide every item (non-zero) to the left end, keeping their order, so all empty slots (0) end up on the right.

            - **Items keep their relative order.**
            - **Up to 10⁵ slots**; items can be negative.
            """
        ],
        think=[
            f"""
            `{slots}` → `{want}`.

            The items' final positions are simply 0, 1, 2, … in reading order. So read left to right, writing each item at
            the next position; afterwards, the positions not written are the empties.
            """,
            fig(Row(slots, label="shelf"), Row(want, label="compacted")),
        ],
        approaches=[
            approach(
                "Bubble the empties right",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Repeat passes swapping an empty slot with the item to its right, until no swap happens."],
                walk=w1,
                build=["Repeated passes.", "Swap empty-then-item pairs.", "Stop when stable."],
                code={
                    "python": """
                        class Solution:
                            def compactShelf(self, slots: List[int]) -> List[int]:
                                a, changed = slots[:], True  #@init
                                while changed:  #@pass
                                    changed = False  #@pass
                                    for i in range(len(a) - 1):  #@pass
                                        if a[i] == 0 and a[i + 1] != 0:  #@swap
                                            a[i], a[i + 1] = a[i + 1], a[i]  #@swap
                                            changed = True  #@swap
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] compactShelf(int[] slots) {
                                int[] a = slots.clone();  //@init
                                boolean changed = true;  //@init
                                while (changed) {  //@pass
                                    changed = false;  //@pass
                                    for (int i = 0; i + 1 < a.length; i++)  //@pass
                                        if (a[i] == 0 && a[i + 1] != 0) { a[i] = a[i + 1]; a[i + 1] = 0; changed = true; }  //@swap
                                }
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> compactShelf(vector<int>& slots) {
                                vector<int> a = slots;  //@init
                                bool changed = true;  //@init
                                while (changed) {  //@pass
                                    changed = false;  //@pass
                                    for (size_t i = 0; i + 1 < a.size(); i++)  //@pass
                                        if (a[i] == 0 && a[i + 1] != 0) { swap(a[i], a[i + 1]); changed = true; }  //@swap
                                }
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* compactShelf(int* slots, int slotsSize, int* returnSize) {
                            int* a = malloc(slotsSize * sizeof(int));  //@init
                            memcpy(a, slots, slotsSize * sizeof(int));  //@init
                            int changed = 1;  //@init
                            while (changed) {  //@pass
                                changed = 0;  //@pass
                                for (int i = 0; i + 1 < slotsSize; i++)  //@pass
                                    if (a[i] == 0 && a[i + 1] != 0) { a[i] = a[i + 1]; a[i + 1] = 0; changed = 1; }  //@swap
                            }
                            *returnSize = slotsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy to rearrange."), ("pass", "Pass over the shelf until nothing moves."), ("swap", "An empty slot before an item: swap them, moving the empty one step right."), ("ret", "Compacted.")],
                complexity=["**Time O(n²):** an item may need many passes to slide left. **Space O(1)** beyond the copy."],
                limits=["Each item moves one step per pass. A write pointer puts every item directly in its final slot in a single pass."],
                slow=True,
            ),
            approach(
                "Write pointer, then fill with empties",
                "best",
                "O(n)",
                "O(1)",
                idea=["Copy each non-zero slot to `a[write++]`. Then set `a[write..n−1]` to 0."],
                walk=w2,
                build=["Write pointer pass.", "Zero the tail."],
                code={
                    "python": """
                        class Solution:
                            def compactShelf(self, slots: List[int]) -> List[int]:
                                a, write = slots[:], 0  #@init
                                for x in slots:  #@move
                                    if x != 0:  #@move
                                        a[write] = x  #@move
                                        write += 1  #@move
                                for i in range(write, len(a)):  #@fill
                                    a[i] = 0  #@fill
                                return a  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] compactShelf(int[] slots) {
                                int[] a = slots.clone();  //@init
                                int write = 0;  //@init
                                for (int x : slots) if (x != 0) a[write++] = x;  //@move
                                for (int i = write; i < a.length; i++) a[i] = 0;  //@fill
                                return a;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> compactShelf(vector<int>& slots) {
                                vector<int> a = slots;  //@init
                                int write = 0;  //@init
                                for (int x : slots) if (x != 0) a[write++] = x;  //@move
                                for (int i = write; i < (int) a.size(); i++) a[i] = 0;  //@fill
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* compactShelf(int* slots, int slotsSize, int* returnSize) {
                            int* a = malloc(slotsSize * sizeof(int));  //@init
                            int write = 0;  //@init
                            for (int i = 0; i < slotsSize; i++) if (slots[i] != 0) a[write++] = slots[i];  //@move
                            for (int i = write; i < slotsSize; i++) a[i] = 0;  //@fill
                            *returnSize = slotsSize;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "Write pointer at the left end."), ("move", "Items go to the next free slot on the left, in reading order."), ("fill", "Everything after the last item is empty."), ("ret", "Compacted shelf.")],
                complexity=["**Time O(n).** **Space O(1)** extra."],
            ),
        ],
        takeaways=[
            """
            - **Move-to-front while keeping order:** write pointer pass, then fill the tail.
            - Swapping (`a[write], a[read] = a[read], a[write]`) does both in one pass with the same result.
            - Bubble-style approaches are quadratic; write each element once.
            """
        ],
    )


@problem
def unique_stock_codes():
    codes = [3, 3, 5, 8, 8, 8, 11]
    want = sorted(set(codes))

    w1 = Steps("Whenever a code equals the one before it, delete it by shifting the rest left.")
    a = codes[:]
    i = 1
    w1.step("Start.", Row(a))
    while i < len(a):
        if a[i] == a[i - 1]:
            w1.step(f"{a[i]} repeats: shift the {len(a) - i - 1} codes after it left.", Row(a, st={i: "mark"}))
            a.pop(i)
        else:
            i += 1
    w1.step(f"Left: {a}.", result=str(a))
    w2, got = rw_walk("The list is sorted, so repeats sit together: keep a code only if it differs from the last kept one.", codes, lambda a, w, x: w == 0 or a[w - 1] != x, lambda k, x: "a new code" if k else "same as the last kept code")
    w2.step(f"Unique codes: {got}.", result=str(got))

    sol(
        "unique-stock-codes",
        summary="""
            In a sorted list, copies of a code sit next to each other. Read left to right with a write pointer: keep a code
            only if it differs from the last code kept (`a[write − 1]`). The kept prefix is the answer. O(n), in place.
        """,
        question=[
            """
            Codes are sorted with repeats. Keep each code once, in increasing order, ideally in place.

            - **Sorted** means equal codes are adjacent.
            - **Up to 10⁵ codes.**
            """
        ],
        think=[
            f"""
            `{codes}` → `{want}`.

            Because the list is sorted, a code is a repeat exactly when it equals the code just before it, or, even more
            simply, the last code we've kept. That comparison is all the read/write loop needs.
            """,
            fig(Row(codes, label="codes"), Row(want, label="unique")),
        ],
        approaches=[
            approach(
                "Delete repeats by shifting",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["Walk the list; when a code equals its predecessor, delete it by shifting everything after it left."],
                walk=w1,
                build=["Compare with the previous code.", "Shift to delete.", "Continue."],
                code={
                    "python": """
                        class Solution:
                            def uniqueSorted(self, codes: List[int]) -> List[int]:
                                a, n, i = codes[:], len(codes), 1  #@init
                                while i < n:  #@scan
                                    if a[i] == a[i - 1]:  #@shift
                                        for j in range(i, n - 1):  #@shift
                                            a[j] = a[j + 1]  #@shift
                                        n -= 1  #@shift
                                    else:  #@scan
                                        i += 1  #@scan
                                return a[:n]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] uniqueSorted(int[] codes) {
                                int[] a = codes.clone();  //@init
                                int n = a.length, i = 1;  //@init
                                while (i < n) {  //@scan
                                    if (a[i] == a[i - 1]) {  //@shift
                                        for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                        n--;  //@shift
                                    } else i++;  //@scan
                                }
                                return Arrays.copyOf(a, n);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> uniqueSorted(vector<int>& codes) {
                                vector<int> a = codes;  //@init
                                int n = a.size(), i = 1;  //@init
                                while (i < n) {  //@scan
                                    if (a[i] == a[i - 1]) {  //@shift
                                        for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                        n--;  //@shift
                                    } else i++;  //@scan
                                }
                                a.resize(n);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* uniqueSorted(int* codes, int codesSize, int* returnSize) {
                            int* a = malloc(codesSize * sizeof(int));  //@init
                            memcpy(a, codes, codesSize * sizeof(int));  //@init
                            int n = codesSize, i = 1;  //@init
                            while (i < n) {  //@scan
                                if (a[i] == a[i - 1]) {  //@shift
                                    for (int j = i; j < n - 1; j++) a[j] = a[j + 1];  //@shift
                                    n--;  //@shift
                                } else i++;  //@scan
                            }
                            *returnSize = n;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "A copy and its live length."), ("scan", "A new code: move on."), ("shift", "A repeat: delete it by shifting the tail; stay at `i` to check the code that moved in."), ("ret", "The live part.")],
                complexity=["**Time O(n²)** with many repeats. **Space O(1)** beyond the copy."],
                limits=["Each deletion shifts the tail. Keeping codes with a write pointer moves each kept code once."],
                slow=True,
            ),
            approach(
                "Write pointer, compare with the last kept",
                "best",
                "O(n)",
                "O(1)",
                idea=["`write = 1` (the first code is always kept). For each later code, if it differs from `a[write − 1]`, copy it to `a[write++]`."],
                walk=w2,
                build=["Keep the first code.", "Compare each code with the last kept one.", "Return the kept prefix."],
                code={
                    "python": """
                        class Solution:
                            def uniqueSorted(self, codes: List[int]) -> List[int]:
                                a, write = codes[:], 1  #@init
                                for i in range(1, len(a)):  #@read
                                    if a[i] != a[write - 1]:  #@keep
                                        a[write] = a[i]  #@keep
                                        write += 1  #@keep
                                return a[:write]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] uniqueSorted(int[] codes) {
                                int[] a = codes.clone();  //@init
                                int write = 1;  //@init
                                for (int i = 1; i < a.length; i++)  //@read
                                    if (a[i] != a[write - 1]) a[write++] = a[i];  //@keep
                                return Arrays.copyOf(a, write);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> uniqueSorted(vector<int>& codes) {
                                vector<int> a = codes;  //@init
                                int write = 1;  //@init
                                for (int i = 1; i < (int) a.size(); i++)  //@read
                                    if (a[i] != a[write - 1]) a[write++] = a[i];  //@keep
                                a.resize(write);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* uniqueSorted(int* codes, int codesSize, int* returnSize) {
                            int* a = malloc(codesSize * sizeof(int));  //@init
                            memcpy(a, codes, codesSize * sizeof(int));  //@init
                            int write = 1;  //@init
                            for (int i = 1; i < codesSize; i++)  //@read
                                if (a[i] != a[write - 1]) a[write++] = a[i];  //@keep
                            *returnSize = write;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "The first code is always kept (the list has at least one)."), ("read", "Every later code."), ("keep", "Different from the last kept code means it's new (the list is sorted)."), ("ret", "The unique prefix.")],
                complexity=["**Time O(n).** **Space O(1)** extra."],
            ),
        ],
        takeaways=[
            """
            - **Dedup a sorted array in place:** compare with the last kept element.
            - Sortedness makes "seen before" a single comparison instead of a hash set.
            - Generalises to "at most k copies": compare with `a[write − k]`.
            """
        ],
    )


@problem
def at_most_twice():
    values = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    want = []
    for x in values:
        if len(want) < 2 or x != want[-2]:
            want.append(x)

    w1 = Steps("Walk the runs of equal values and copy at most two of each into a new list.")
    out, i = [], 0
    while i < len(values):
        j = i
        while j < len(values) and values[j] == values[i]:
            j += 1
        take = min(2, j - i)
        out += [values[i]] * take
        w1.step(f"Run of {j - i} × {values[i]}: keep {take}.", Row(values, st={t: ("found" if t < i + take else "mark") for t in range(i, j)}), Row(out, label="output"))
        i = j
    w1.step(f"Result: {out}.", result=str(out))
    w2, got = rw_walk("Keep a value unless the kept part already ends with two copies of it: compare with the element two places back in the kept part.", values, lambda a, w, x: w < 2 or a[w - 2] != x, lambda k, x: "fewer than two kept so far" if k else "two already kept")
    w2.step(f"Result: {got}.", result=str(got))

    sol(
        "at-most-twice",
        summary="""
            Read/write pointers with a look-back of two: keep value `x` if fewer than two values are kept, or if
            `a[write − 2] ≠ x`. Since the list is sorted, `a[write − 2] == x` means the last two kept values are both `x`
            already. O(n), in place.
        """,
        question=[
            """
            In a sorted list, keep each value **at most twice**, preserving order, in place with O(1) extra space.

            - **Sorted** input: copies are adjacent.
            - **Up to 10⁵ values.**
            """
        ],
        think=[
            f"""
            `{values}` → `{want}`.

            When deciding about the next value `x`, look at the kept part. If its last two entries are both `x`, a third
            would be too many. Thanks to sorting, checking just the entry **two back** (`a[write − 2]`) is enough: if it
            equals `x`, so does everything after it.
            """,
            fig(Row(values, label="values"), Row(want, label="at most twice")),
        ],
        approaches=[
            approach(
                "Copy at most two per run",
                "better",
                "O(n)",
                "O(n)",
                idea=["Find each run of equal values and append `min(2, run length)` copies to a new list."],
                walk=w1,
                build=["Scan runs with an inner pointer.", "Append up to two."],
                code={
                    "python": """
                        class Solution:
                            def keepAtMostTwo(self, values: List[int]) -> List[int]:
                                out, i = [], 0  #@init
                                while i < len(values):  #@run
                                    j = i  #@run
                                    while j < len(values) and values[j] == values[i]:  #@run
                                        j += 1  #@run
                                    out += [values[i]] * min(2, j - i)  #@take
                                    i = j  #@take
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] keepAtMostTwo(int[] values) {
                                List<Integer> out = new ArrayList<>();  //@init
                                int i = 0;  //@init
                                while (i < values.length) {  //@run
                                    int j = i;  //@run
                                    while (j < values.length && values[j] == values[i]) j++;  //@run
                                    for (int c = 0; c < Math.min(2, j - i); c++) out.add(values[i]);  //@take
                                    i = j;  //@take
                                }
                                return out.stream().mapToInt(Integer::intValue).toArray();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> keepAtMostTwo(vector<int>& values) {
                                vector<int> out;  //@init
                                size_t i = 0;  //@init
                                while (i < values.size()) {  //@run
                                    size_t j = i;  //@run
                                    while (j < values.size() && values[j] == values[i]) j++;  //@run
                                    out.insert(out.end(), min<size_t>(2, j - i), values[i]);  //@take
                                    i = j;  //@take
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* keepAtMostTwo(int* values, int valuesSize, int* returnSize) {
                            int* out = malloc(valuesSize * sizeof(int));  //@init
                            int w = 0, i = 0;  //@init
                            while (i < valuesSize) {  //@run
                                int j = i;  //@run
                                while (j < valuesSize && values[j] == values[i]) j++;  //@run
                                for (int c = 0; c < 2 && c < j - i; c++) out[w++] = values[i];  //@take
                                i = j;  //@take
                            }
                            *returnSize = w;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "A separate output list."), ("run", "Find where the run of `values[i]` ends."), ("take", "Up to two copies, then jump to the next run."), ("ret", "The trimmed list.")],
                complexity=["**Time O(n).** **Space O(n)** for the separate output."],
                limits=["Builds a second list, but the task asks for O(1) extra space. The same decision can be made in place by looking two places back in the kept part."],
            ),
            approach(
                "Write pointer, look back two",
                "best",
                "O(n)",
                "O(1)",
                idea=["For each `x`: if `write < 2` or `a[write − 2] != x`, set `a[write] = x` and advance."],
                walk=w2,
                build=["Copy; `write = 0`.", "Keep `x` unless the kept part ends with two `x`s.", "Return the prefix."],
                code={
                    "python": """
                        class Solution:
                            def keepAtMostTwo(self, values: List[int]) -> List[int]:
                                a, write = values[:], 0  #@init
                                for x in values:  #@read
                                    if write < 2 or a[write - 2] != x:  #@keep
                                        a[write] = x  #@keep
                                        write += 1  #@keep
                                return a[:write]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] keepAtMostTwo(int[] values) {
                                int[] a = values.clone();  //@init
                                int write = 0;  //@init
                                for (int x : values)  //@read
                                    if (write < 2 || a[write - 2] != x) a[write++] = x;  //@keep
                                return Arrays.copyOf(a, write);  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> keepAtMostTwo(vector<int>& values) {
                                vector<int> a = values;  //@init
                                int write = 0;  //@init
                                for (int x : values)  //@read
                                    if (write < 2 || a[write - 2] != x) a[write++] = x;  //@keep
                                a.resize(write);  //@ret
                                return a;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* keepAtMostTwo(int* values, int valuesSize, int* returnSize) {
                            int* a = malloc(valuesSize * sizeof(int));  //@init
                            int write = 0;  //@init
                            for (int i = 0; i < valuesSize; i++)  //@read
                                if (write < 2 || a[write - 2] != values[i]) a[write++] = values[i];  //@keep
                            *returnSize = write;  //@ret
                            return a;  //@ret
                        }
                    """,
                },
                lines=[("init", "The kept part grows from the left."), ("read", "Each value in order (read from the original, so overwrites can't confuse us)."), ("keep", "Two back in the kept part: if it's `x`, the kept part already ends with `x, x`."), ("ret", "The kept prefix.")],
                complexity=["**Time O(n).** **Space O(1)** extra."],
            ),
        ],
        takeaways=[
            """
            - **At most k copies:** keep `x` unless `a[write − k] == x`.
            - k = 1 is the plain dedup.
            - Works because the input is sorted (copies are contiguous).
            """
        ],
    )


@problem
def run_length_code():
    text = "aaabccddddx"
    out, i = [], 0
    runs = []
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1
        out.append(text[i] + (str(j - i) if j - i > 1 else ""))
        runs.append((i, j))
        i = j
    want = "".join(out)

    w = Steps("Two pointers mark each run: i at its start, j moves until the character changes.")
    acc = ""
    for i, j in runs:
        acc += text[i] + (str(j - i) if j - i > 1 else "")
        w.step(f"Run '{text[i]}' × {j - i} → '{text[i]}{j - i if j - i > 1 else ''}'.", Row(list(text), st={t: "active" for t in range(i, j)}, ptr={"i": i, "j": min(j, len(text) - 1)}), Vars(output=acc))
    w.step(f"Compressed: {want}.", result=want)

    sol(
        "run-length-code",
        summary="""
            Walk the text with two pointers: `i` at the start of a run, `j` advancing while the character repeats. Append
            the character and, if the run is longer than 1, its length. Then jump `i` to `j`. O(n) with a string builder.
        """,
        question=[
            """
            Replace each run of a repeated character with the character followed by the run length; runs of length 1 are
            just the character. `"aaabcc"` → `"a3bc2"`.

            - **Lengths can have several digits** (a run of 12 becomes `a12`).
            - **Up to 10⁵ characters.**
            """
        ],
        think=[
            f"""
            `{text}` → `{want}`.

            Each run is found by moving a second pointer until the character changes; its length is the distance between
            the pointers. Build the output with a string builder (or list) rather than repeated string concatenation,
            which would copy the whole output each time.
            """,
            fig(Row(list(text), label="text")),
        ],
        approaches=[
            approach(
                "Two pointers over runs",
                "best",
                "O(n)",
                "O(n)",
                idea=["`i = 0`. While `i < n`: move `j` from `i` while `text[j] == text[i]`; output `text[i]` and `j − i` if > 1; set `i = j`."],
                walk=w,
                build=["Builder for the output.", "Find each run with `j`.", "Emit character and count."],
                code={
                    "python": """
                        class Solution:
                            def compress(self, text: str) -> str:
                                out, i = [], 0  #@init
                                while i < len(text):  #@run
                                    j = i  #@run
                                    while j < len(text) and text[j] == text[i]:  #@run
                                        j += 1  #@run
                                    out.append(text[i])  #@emit
                                    if j - i > 1:  #@emit
                                        out.append(str(j - i))  #@emit
                                    i = j  #@next
                                return "".join(out)  #@ret
                    """,
                    "java": """
                        class Solution {
                            public String compress(String text) {
                                StringBuilder out = new StringBuilder();  //@init
                                int i = 0, n = text.length();  //@init
                                while (i < n) {  //@run
                                    int j = i;  //@run
                                    while (j < n && text.charAt(j) == text.charAt(i)) j++;  //@run
                                    out.append(text.charAt(i));  //@emit
                                    if (j - i > 1) out.append(j - i);  //@emit
                                    i = j;  //@next
                                }
                                return out.toString();  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            string compress(string& text) {
                                string out;  //@init
                                size_t i = 0, n = text.size();  //@init
                                while (i < n) {  //@run
                                    size_t j = i;  //@run
                                    while (j < n && text[j] == text[i]) j++;  //@run
                                    out += text[i];  //@emit
                                    if (j - i > 1) out += to_string(j - i);  //@emit
                                    i = j;  //@next
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        char* compress(char* text) {
                            int n = strlen(text), i = 0, w = 0;  //@init
                            char* out = malloc(n + 1);  //@init
                            while (i < n) {  //@run
                                int j = i;  //@run
                                while (j < n && text[j] == text[i]) j++;  //@run
                                out[w++] = text[i];  //@emit
                                if (j - i > 1) w += sprintf(out + w, "%d", j - i);  //@emit
                                i = j;  //@next
                            }
                            out[w] = '\\0';  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "An output builder and the start of the first run.", {"c": "The output is never longer than the input (a run of length ≥ 2 shrinks to the letter plus at most as many digits), so `n + 1` bytes are enough."}),
                    ("run", "`j` moves past every copy of `text[i]`: the run is `[i, j)`."),
                    ("emit", "The character, then its count if the run is longer than 1."),
                    ("next", "The next run starts where this one ended."),
                    ("ret", "The compressed text."),
                ],
                complexity=["**Time O(n):** each character is passed by `j` once. **Space O(n)** for the output."],
            ),
        ],
        takeaways=[
            """
            - **Runs = two pointers:** start and end of the current group.
            - Build strings with a builder or list, not repeated concatenation.
            - Multi-digit counts need number-to-text conversion, not a single character.
            """
        ],
    )
