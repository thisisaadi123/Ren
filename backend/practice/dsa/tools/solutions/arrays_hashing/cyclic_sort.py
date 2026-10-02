"""Arrays & Hashing: cyclic sort."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401

CYCLE_STATES = ["answer", "found", "mark", "active", "new"]


def cycles_of(order):
    n = len(order)
    seen = [False] * n
    out = []
    for i in range(n):
        if not seen[i]:
            cyc, j = [], i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = order[j] - 1
            out.append(cyc)
    return out


@problem
def fewest_swaps_to_sort():
    order = [2, 3, 1, 5, 4, 7, 6]
    n = len(order)
    cyc = cycles_of(order)
    assert n - len(cyc) == 4

    w1 = Steps("Left to right: if position i has the wrong bib, find bib i + 1 and swap it in.")
    a = order[:]
    swaps = 0
    w1.step("Position i should hold bib i + 1.", Row(a, slots=True), Vars(swaps=0))
    for i in range(n):
        if a[i] == i + 1:
            w1.step(f"Position {i} already holds {i + 1}. Nothing to do.", Row(a, st={**{q: "found" for q in range(i)}, i: "found"}, ptr={"i": i}, slots=True), Vars(swaps=swaps))
            continue
        j = a.index(i + 1)
        st = {q: "found" for q in range(i)}
        st[i] = "active"
        st[j] = "mark"
        w1.step(f"Position {i} holds {a[i]}, but should hold {i + 1}. Scan: {i + 1} is at position {j}.", Row(a, st=st, ptr={"i": i, "j": j}, slots=True), Vars(swaps=swaps))
        a[i], a[j] = a[j], a[i]
        swaps += 1
        w1.step(f"Swap them. Position {i} is now final. Swaps: {swaps}.", Row(a, st={**{q: "found" for q in range(i)}, i: "found", j: "new"}, ptr={"i": i}, slots=True), Vars(swaps=swaps))
    w1.step(f"Sorted with {swaps} swaps.", Row(a, st={q: "found" for q in range(n)}, slots=True), result=swaps)

    w2 = Steps("Follow 'where does this bib belong?' until you loop back. Each loop of length L costs L − 1 swaps.")
    seen = [False] * n
    cycles = 0
    st = {}
    w2.step("Position i holds bib order[i], which belongs at position order[i] − 1. Follow those arrows.", Row(order, slots=True), Vars(cycles=0))
    for i in range(n):
        if seen[i]:
            continue
        cycles += 1
        path, j = [], i
        while not seen[j]:
            seen[j] = True
            path.append(j)
            j = order[j] - 1
        for p in path:
            st[p] = CYCLE_STATES[(cycles - 1) % len(CYCLE_STATES)]
        arrows = " → ".join(f"{p}" for p in path) + f" → {path[0]}"
        w2.step(f"New cycle from position {i}: positions {arrows}. Length {len(path)}, so {len(path) - 1} swap{'s' if len(path) != 2 else ''}." if len(path) > 1 else f"Position {i} is its own cycle (already in place): 0 swaps.",
                Row(order, st=dict(st), slots=True), Vars(cycles=cycles))
    w2.step(f"{cycles} cycles among {n} positions: {n} − {cycles} = {n - cycles} swaps.", Row(order, st=dict(st), slots=True), result=n - cycles)

    sol(
        "fewest-swaps-to-sort",
        summary="""
            Every bib "points" at the position where it belongs. Following those pointers splits the
            positions into separate cycles, and a cycle of length L needs exactly L − 1 swaps. So the answer
            is `n − (number of cycles)`, found in one O(n) pass.
        """,
        question=[
            """
            The list holds the bibs 1 to n in some order. A swap exchanges any two positions (they don't have
            to be next to each other). Find the **smallest** number of swaps that sorts the list.

            - **Any two positions can be swapped**, which is different from sorting by swapping neighbours
              (that would count inversions instead).
            - **Every bib appears exactly once**, so bib `b` has exactly one correct home: position `b − 1`
              (0-indexed). This is what makes the problem easy to reason about.
            - **You count swaps, you don't perform them.** You may simulate them, but only the number is
              returned.
            - **Size:** up to 10⁵ bibs, so anything quadratic is too slow.
            """
        ],
        think=[
            """
            Take `order = [2, 3, 1, 5, 4, 7, 6]`.

            Look at position 0: it holds bib 2, which belongs at position 1. Position 1 holds bib 3, which
            belongs at position 2. Position 2 holds bib 1, which belongs back at position 0. These three
            positions form a **closed loop**: their bibs only need to move among themselves.
            """,
            fig(Row(order, st={0: "answer", 1: "answer", 2: "answer", 3: "found", 4: "found", 5: "mark", 6: "mark"}, slots=True),
                caption="Same shade = same cycle: positions 0 → 1 → 2 → 0, then 3 ↔ 4, then 5 ↔ 6."),
            """
            Now count swaps per loop. A loop of 2 (bibs 5 and 4 swapped) takes **1** swap. For the loop of
            3, one swap can put one bib home (swap bib 1 into position 0), which leaves a loop of 2, one more
            swap: **2** in total. In general, each swap can send at most one more bib home *within* a loop,
            and the last swap sends two home at once, so a loop of length L takes **L − 1** swaps.

            Can you do better by swapping across two loops? No: that merges them into one bigger loop, which
            only adds work. So the minimum is the sum of (L − 1) over the loops:

            `(3 − 1) + (2 − 1) + (2 − 1) = 4` = n − (number of loops) = 7 − 3.

            A bib already in place is a loop of length 1 and costs 0, which fits the same formula.
            """,
        ],
        approaches=[
            approach(
                "Fix positions left to right, searching for each bib",
                "brute",
                "O(n²)",
                "O(n)",
                idea=[
                    """
                    Work on a copy. For each position `i` from left to right: if it doesn't hold `i + 1`,
                    search the rest of the list for bib `i + 1` and swap it in. Count the swaps.

                    Each swap puts bib `i + 1` home for good, and it never swaps when position `i` is already
                    right. In cycle terms, every swap splits one bib off its cycle (a cycle of L becomes a cycle
                    of L − 1 plus a fixed point), so it uses exactly L − 1 swaps per cycle: the minimum.
                    """
                ],
                walk=w1,
                build=[
                    "Copy the list (so the input isn't changed).",
                    "For `i` from 0 to n − 1: if `a[i] == i + 1`, continue.",
                    "Otherwise find `j > i` with `a[j] == i + 1` by scanning, swap `a[i]` and `a[j]`, and count the swap.",
                    "Return the count.",
                ],
                code={
                    "python": """
                        class Solution:
                            def minSwaps(self, order: List[int]) -> int:
                                a = order[:]  #@copy
                                swaps = 0
                                for i in range(len(a)):  #@loop
                                    if a[i] != i + 1:  #@check
                                        j = a.index(i + 1, i + 1)  #@find
                                        a[i], a[j] = a[j], a[i]  #@swap
                                        swaps += 1  #@swap
                                return swaps  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minSwaps(int[] order) {
                                int[] a = order.clone();  //@copy
                                int n = a.length, swaps = 0;
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (a[i] != i + 1) {  //@check
                                        int j = i + 1;  //@find
                                        while (a[j] != i + 1) j++;  //@find
                                        int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                        swaps++;  //@swap
                                    }
                                }
                                return swaps;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minSwaps(vector<int>& order) {
                                vector<int> a = order;  //@copy
                                int n = a.size(), swaps = 0;
                                for (int i = 0; i < n; i++) {  //@loop
                                    if (a[i] != i + 1) {  //@check
                                        int j = i + 1;  //@find
                                        while (a[j] != i + 1) j++;  //@find
                                        swap(a[i], a[j]);  //@swap
                                        swaps++;  //@swap
                                    }
                                }
                                return swaps;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minSwaps(int* order, int orderSize) {
                            int* a = malloc(orderSize * sizeof(int));  //@copy
                            memcpy(a, order, orderSize * sizeof(int));  //@copy
                            int swaps = 0;
                            for (int i = 0; i < orderSize; i++) {  //@loop
                                if (a[i] != i + 1) {  //@check
                                    int j = i + 1;  //@find
                                    while (a[j] != i + 1) j++;  //@find
                                    int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                    swaps++;  //@swap
                                }
                            }
                            free(a);  //@ret
                            return swaps;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "Work on a copy so the caller's list stays as it was."),
                    ("loop", "Fix positions in order. Everything left of `i` is already final."),
                    ("check", "Position `i` should hold bib `i + 1`. If it does, there's nothing to do (and doing nothing is what keeps the count minimal)."),
                    ("find", "Bib `i + 1` must be somewhere to the right: everything to the left is already final. Scan for it.",
                     {"python": "`index(value, start)` searches from `start` onwards."}),
                    ("swap", "Bring it home with one swap and count it. The bib that was at `i` moves to `j`; it'll be handled later."),
                    ("ret", "This count equals n minus the number of cycles, the minimum.", {"c": "Free the copy, then return."}),
                ],
                complexity=[
                    """
                    **Time O(n²):** each search can scan most of the list. A reversed list of 10⁵ bibs means
                    billions of steps.

                    **Space O(n)** for the copy.
                    """
                ],
                limits=[
                    """
                    The swaps are already minimal; only the **searching** is slow. Two fixes exist: keep a
                    "where is each bib?" array so each search is O(1), or skip the swapping altogether and just
                    count cycles, which is what the best approach does.
                    """
                ],
                slow=True,
            ),
            approach(
                "Count the cycles",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Position `i` holds bib `order[i]`, which belongs at position `order[i] − 1`. Starting from
                    any position and repeatedly jumping to "where my bib belongs" always comes back to the
                    start, tracing one cycle. Mark the positions you visit so each cycle is traced once.

                    A cycle of length L needs L − 1 swaps (and can't do with fewer: each swap inside a cycle
                    raises the number of cycles by at most one, and the sorted list has n cycles of length 1).
                    Adding up, the answer is `n − cycles`.
                    """
                ],
                walk=w2,
                build=[
                    "Make a `seen` array of n falses and set `cycles = 0`.",
                    "For each position `i` not yet seen: it starts a new cycle, so add 1 to `cycles`.",
                    "Trace the cycle: `j = i`; while `j` isn't seen, mark it and jump to `j = order[j] − 1`.",
                    "Return `n − cycles`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def minSwaps(self, order: List[int]) -> int:
                                n = len(order)
                                seen = [False] * n  #@seen
                                cycles = 0
                                for i in range(n):  #@start
                                    if seen[i]:  #@start
                                        continue  #@start
                                    cycles += 1  #@count
                                    j = i  #@trace
                                    while not seen[j]:  #@trace
                                        seen[j] = True  #@trace
                                        j = order[j] - 1  #@trace
                                return n - cycles  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int minSwaps(int[] order) {
                                int n = order.length;
                                boolean[] seen = new boolean[n];  //@seen
                                int cycles = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    if (seen[i]) continue;  //@start
                                    cycles++;  //@count
                                    for (int j = i; !seen[j]; j = order[j] - 1) {  //@trace
                                        seen[j] = true;  //@trace
                                    }
                                }
                                return n - cycles;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int minSwaps(vector<int>& order) {
                                int n = order.size();
                                vector<bool> seen(n, false);  //@seen
                                int cycles = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    if (seen[i]) continue;  //@start
                                    cycles++;  //@count
                                    for (int j = i; !seen[j]; j = order[j] - 1) {  //@trace
                                        seen[j] = true;  //@trace
                                    }
                                }
                                return n - cycles;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int minSwaps(int* order, int orderSize) {
                            bool* seen = calloc(orderSize, sizeof(bool));  //@seen
                            int cycles = 0;
                            for (int i = 0; i < orderSize; i++) {  //@start
                                if (seen[i]) continue;  //@start
                                cycles++;  //@count
                                for (int j = i; !seen[j]; j = order[j] - 1) {  //@trace
                                    seen[j] = true;  //@trace
                                }
                            }
                            free(seen);  //@ret
                            return orderSize - cycles;  //@ret
                        }
                    """,
                },
                lines=[
                    ("seen", "Marks positions whose cycle has already been traced."),
                    ("start", "Visit each position once; a position already marked belongs to a cycle we've counted."),
                    ("count", "An unmarked position starts a cycle we haven't seen yet."),
                    ("trace", "Jump from each position to where its bib belongs (`order[j] − 1`) until we land on a marked position. Because each position has exactly one bib and each bib exactly one home, that marked position is always the start `i`: the walk is a closed loop."),
                    ("ret", "Each cycle of length L costs L − 1 swaps, and those add up to n − cycles.", {"c": "Free the marks, then return."}),
                ],
                complexity=[
                    """
                    **Time O(n):** every position is marked exactly once, and each mark costs O(1). The inner
                    loop doesn't make it quadratic, because it only ever visits unmarked positions.

                    **Space O(n)** for the marks. If you're allowed to modify the input, you can mark a visited
                    position by negating `order[j]` instead (and read `abs(order[j])`), for O(1) extra space.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - In a permutation, **"where does this element belong?"** links every position to exactly one
              other, which splits the positions into disjoint cycles.
            - Minimum arbitrary swaps to sort a permutation = **n − number of cycles**.
            - Tracing cycles with a visited marker is O(n) even though it looks like a nested loop: each
              element is visited once in total.
            - If swaps were restricted to neighbours, the answer would instead be the number of inversions,
              a different problem.
            """
        ],
    )


@problem
def first_k_missing():
    nums, k = [4, 3, 2, 7, 8, 2, 3, 1], 3
    have = set(nums)
    out, x = [], 1
    while len(out) < k:
        if x not in have:
            out.append(x)
        x += 1
    assert out == [5, 6, 9]

    w1 = Steps("Try 1, 2, 3, … and scan the whole list for each one.")
    found, x = [], 1
    w1.step("k = 3. Candidates start at 1.", Row(nums, slots=True), Vars(missing="[]"))
    while len(found) < k:
        hit = [i for i, v in enumerate(nums) if v == x]
        if hit:
            w1.step(f"{x}: scan… found at index {hit[0]}. Taken.", Row(nums, st={hit[0]: "found"}, slots=True), Vars(missing=str(found)))
        else:
            found.append(x)
            w1.step(f"{x}: scan the whole list, not there. Missing #{len(found)}.", Row(nums, st={i: "dim" for i in range(len(nums))}, slots=True), Vars(missing=str(found)))
        x += 1
    w1.step(f"Found {k}: {found}.", Row(nums, slots=True), result=found)

    w2 = Steps("Put the numbers in a hash set, then count up from 1 with O(1) checks.")
    w2.step("The set holds every number once: {1, 2, 3, 4, 7, 8}.", Row(nums, slots=True), Row(sorted(have), label="set (any order)"))
    found, x = [], 1
    while len(found) < k:
        if x in have:
            w2.step(f"{x} is in the set.", Row(sorted(have), st={sorted(have).index(x): "found"}, label="set"), Vars(missing=str(found)))
        else:
            found.append(x)
            w2.step(f"{x} isn't in the set: missing #{len(found)}.", Row(sorted(have), label="set"), Vars(missing=str(found)))
        x += 1
    w2.step(f"Answer {found}.", Row(sorted(have), label="set"), result=found)

    n = len(nums)
    size = n + k
    present = [False] * (size + 1)
    w3 = Steps(f"The answers can't go past n + k = {size}. Mark which of 1 … {size} appear, then read off the first k gaps.")
    marks = [None] * size
    w3.step(f"n = {n}, k = {k}. Only the numbers 1 … {size} can matter. Make {size} empty flags.", Row(nums, slots=True), Row(marks, label="present? (1 … n + k)"))
    for v in nums:
        if 1 <= v <= size and not present[v]:
            present[v] = True
            marks[v - 1] = v
            w3.step(f"{v} is in range: flag it.", Row(nums, st={nums.index(v): "active"}, slots=True), Row(marks, st={v - 1: "new"}, label="present? (1 … n + k)"))
    gaps = [i + 1 for i in range(size) if not present[i + 1]][:k]
    w3.step(f"Read the flags left to right; the first {k} empty ones are {gaps}.", Row(marks, st={g - 1: "answer" for g in gaps}, label="present? (1 … n + k)"), result=gaps)

    sol(
        "first-k-missing",
        summary="""
            The answers can never be larger than `n + k`: n numbers can block at most n of the values
            `1 … n + k`, so at least k of them are free. That bound turns the problem into marking flags in
            an array of size `n + k` and reading off the first k empty ones, O(n + k) with no hashing.
        """,
        question=[
            """
            List the `k` smallest positive integers (1, 2, 3, …) that don't appear in `nums`, in increasing
            order.

            - **Only positive answers.** 0 and negative numbers in `nums` never block anything, because
              they aren't candidates.
            - **Repeats block a value once.** Two 3s still only remove 3.
            - **Answers can go past the largest number in the list.** For `nums = [2, 3, 4]` and k = 3 the
              answer is `[1, 5, 6]`: after 1, the next free values are above 4.
            - **Huge values in `nums` (up to 10⁹)** are irrelevant unless they fall among the first few
              free numbers, which they can't, as we'll see.
            - **Size:** n and k each up to 10⁵.
            """
        ],
        think=[
            """
            Take `nums = [4, 3, 2, 7, 8, 2, 3, 1]` and `k = 3`. Counting up by hand: 1 ✓ taken, 2 ✓, 3 ✓,
            4 ✓, **5** free, **6** free, 7 ✓, 8 ✓, **9** free. Answer `[5, 6, 9]`.

            The doing-it-by-hand method is already the algorithm: count up from 1 and skip what's taken. The
            only question is how quickly you can ask "is x taken?", and how far up you might have to go.

            **How far?** Look at the values `1 … n + k`. There are n + k of them, and the list has only n
            numbers, so at most n of those values are taken. That leaves at least k free values inside
            `1 … n + k`. So the counting never needs to pass `n + k`, and any number in `nums` bigger than
            that can be ignored.
            """,
            fig(Row([1, 2, 3, 4, None, None, 7, 8, None, None, None], st={4: "answer", 5: "answer", 8: "answer"}, label="values 1 … n + k = 11 (blank = free)"),
                caption="With 8 numbers and k = 3, everything happens inside 1 … 11, and the first three blanks are the answer."),
            """
            That bound is what lets a plain array replace a hash set: index `v` of an array of size `n + k`
            answers "is v taken?".
            """,
        ],
        approaches=[
            approach(
                "Count up and scan the list each time",
                "brute",
                "O((n + k) · n)",
                "O(1)",
                idea=[
                    """
                    Try candidates 1, 2, 3, … in order. For each one, scan `nums`. If it's not there, it's
                    missing: add it to the answer. Stop once you have k.

                    At most n + k candidates are tried (by the bound above), and each scan costs n.
                    """
                ],
                walk=w1,
                build=[
                    "Start with an empty answer and `x = 1`.",
                    "While the answer has fewer than k numbers: scan `nums` for `x`; if absent, append `x`.",
                    "Increase `x` and repeat.",
                ],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int], k: int) -> List[int]:
                                out, x = [], 1  #@init
                                while len(out) < k:  #@loop
                                    if x not in nums:  #@scan
                                        out.append(x)  #@scan
                                    x += 1  #@next
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] firstMissing(int[] nums, int k) {
                                int[] out = new int[k];  //@init
                                int found = 0, x = 1;  //@init
                                while (found < k) {  //@loop
                                    boolean taken = false;  //@scan
                                    for (int v : nums) if (v == x) { taken = true; break; }  //@scan
                                    if (!taken) out[found++] = x;  //@scan
                                    x++;  //@next
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> firstMissing(vector<int>& nums, int k) {
                                vector<int> out;  //@init
                                int x = 1;  //@init
                                while ((int) out.size() < k) {  //@loop
                                    if (find(nums.begin(), nums.end(), x) == nums.end()) {  //@scan
                                        out.push_back(x);  //@scan
                                    }
                                    x++;  //@next
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* firstMissing(int* nums, int numsSize, int k, int* returnSize) {
                            int* out = malloc(k * sizeof(int));  //@init
                            int found = 0, x = 1;  //@init
                            while (found < k) {  //@loop
                                bool taken = false;  //@scan
                                for (int i = 0; i < numsSize && !taken; i++) taken = nums[i] == x;  //@scan
                                if (!taken) out[found++] = x;  //@scan
                                x++;  //@next
                            }
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "The answer so far, and the first candidate, 1.",
                     {"java": "We know the answer has exactly k numbers, so allocate them up front and fill with `found`.",
                      "c": "Room for exactly k answers; `found` counts how many are filled."}),
                    ("loop", "Keep going until k missing numbers are collected."),
                    ("scan", "Look for `x` in the whole list. Not there means it's missing."),
                    ("next", "Move on to the next candidate."),
                    ("ret", "The answers were found in increasing order, so no sorting is needed.", {"c": "Report the length through `returnSize`; the caller frees `out`."}),
                ],
                complexity=["**Time O((n + k) · n):** up to n + k candidates, each scanning n numbers (≈ 2 × 10¹⁰ at the limits). **Space O(1)** beyond the answer."],
                limits=["Every membership question costs a full scan. Store the numbers somewhere with O(1) lookups and the scans disappear."],
                slow=True,
            ),
            approach(
                "Hash set, then count up",
                "better",
                "O(n + k)",
                "O(n)",
                idea=[
                    """
                    Put every number in a hash set once. Then count up from 1 exactly as before, but each
                    "is x taken?" is now an O(1) lookup.
                    """
                ],
                walk=w2,
                build=[
                    "Build a hash set of `nums`.",
                    "Count `x` up from 1, appending each `x` not in the set, until there are k answers.",
                ],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int], k: int) -> List[int]:
                                have = set(nums)  #@set
                                out, x = [], 1  #@loop
                                while len(out) < k:  #@loop
                                    if x not in have:  #@check
                                        out.append(x)  #@check
                                    x += 1  #@loop
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] firstMissing(int[] nums, int k) {
                                Set<Integer> have = new HashSet<>();  //@set
                                for (int v : nums) have.add(v);  //@set
                                int[] out = new int[k];  //@loop
                                for (int found = 0, x = 1; found < k; x++) {  //@loop
                                    if (!have.contains(x)) out[found++] = x;  //@check
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> firstMissing(vector<int>& nums, int k) {
                                unordered_set<int> have(nums.begin(), nums.end());  //@set
                                vector<int> out;  //@loop
                                for (int x = 1; (int) out.size() < k; x++) {  //@loop
                                    if (!have.count(x)) out.push_back(x);  //@check
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        // A small hash set of ints: open addressing, linear probing.
                        typedef struct { int key; bool used; } Slot;  //@cset

                        static unsigned slotOf(int key, unsigned mask) {  //@cset
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@cset
                            return (unsigned) (h >> 32) & mask;  //@cset
                        }  //@cset

                        int* firstMissing(int* nums, int numsSize, int k, int* returnSize) {
                            unsigned cap = 1;  //@set
                            while (cap < 2u * numsSize) cap <<= 1;  //@set
                            Slot* have = calloc(cap, sizeof(Slot));  //@set
                            for (int i = 0; i < numsSize; i++) {  //@set
                                unsigned s = slotOf(nums[i], cap - 1);  //@set
                                while (have[s].used && have[s].key != nums[i]) s = (s + 1) & (cap - 1);  //@set
                                have[s] = (Slot) {nums[i], true};  //@set
                            }  //@set
                            int* out = malloc(k * sizeof(int));  //@loop
                            for (int found = 0, x = 1; found < k; x++) {  //@loop
                                unsigned s = slotOf(x, cap - 1);  //@check
                                while (have[s].used && have[s].key != x) s = (s + 1) & (cap - 1);  //@check
                                if (!have[s].used) out[found++] = x;  //@check
                            }
                            free(have);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cset", "C has no hash set, so here's a minimal one: a slot holds a key and an in-use flag, and `slotOf` scrambles a key into a starting slot (multiply by a large odd constant, keep the high bits)."),
                    ("set", "Every number goes into the set once; repeats collapse.",
                     {"c": "The table is a power of two at least 2n in size. Each number probes forward from its slot until it finds itself or an empty slot, then claims it."}),
                    ("loop", "Candidates 1, 2, 3, … until k answers are collected."),
                    ("check", "An O(1) average lookup replaces the scan.", {"c": "Probe from `x`'s slot; reaching an empty slot means `x` was never added."}),
                    ("ret", "Answers come out in increasing order.", {"c": "Free the table and report the length."}),
                ],
                complexity=["**Time O(n + k)** on average: n inserts and at most n + k lookups. **Space O(n)** for the set."],
                limits=[
                    """
                    Fast enough, but the set stores numbers that can never matter (negatives, zeros, anything
                    above n + k), and hash lookups are O(1) only on average. Knowing that every answer is at
                    most n + k lets us use plain array indices instead.
                    """
                ],
            ),
            approach(
                "Flags for 1 … n + k",
                "best",
                "O(n + k)",
                "O(n + k)",
                idea=[
                    """
                    Every answer is at most `n + k` (n numbers can block at most n of the values
                    `1 … n + k`). So make a boolean array `present` of size `n + k + 1`, flag each number of
                    `nums` that falls in `1 … n + k`, and ignore the rest. Then walk `1, 2, …` and collect the
                    first k unflagged values.
                    """
                ],
                walk=w3,
                build=[
                    "Let `limit = n + k` and make `present` with `limit + 1` falses.",
                    "For each `v` in `nums` with `1 ≤ v ≤ limit`, set `present[v] = true`.",
                    "Walk `x` from 1 upward, appending every `x` with `present[x]` false, until k are found. It can't run past `limit`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def firstMissing(self, nums: List[int], k: int) -> List[int]:
                                limit = len(nums) + k  #@limit
                                present = [False] * (limit + 1)  #@limit
                                for v in nums:  #@mark
                                    if 1 <= v <= limit:  #@mark
                                        present[v] = True  #@mark
                                out = []  #@read
                                x = 1  #@read
                                while len(out) < k:  #@read
                                    if not present[x]:  #@read
                                        out.append(x)  #@read
                                    x += 1  #@read
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] firstMissing(int[] nums, int k) {
                                int limit = nums.length + k;  //@limit
                                boolean[] present = new boolean[limit + 1];  //@limit
                                for (int v : nums) {  //@mark
                                    if (v >= 1 && v <= limit) present[v] = true;  //@mark
                                }
                                int[] out = new int[k];  //@read
                                for (int found = 0, x = 1; found < k; x++) {  //@read
                                    if (!present[x]) out[found++] = x;  //@read
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> firstMissing(vector<int>& nums, int k) {
                                int limit = nums.size() + k;  //@limit
                                vector<bool> present(limit + 1, false);  //@limit
                                for (int v : nums) {  //@mark
                                    if (v >= 1 && v <= limit) present[v] = true;  //@mark
                                }
                                vector<int> out;  //@read
                                for (int x = 1; (int) out.size() < k; x++) {  //@read
                                    if (!present[x]) out.push_back(x);  //@read
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* firstMissing(int* nums, int numsSize, int k, int* returnSize) {
                            int limit = numsSize + k;  //@limit
                            bool* present = calloc(limit + 1, sizeof(bool));  //@limit
                            for (int i = 0; i < numsSize; i++) {  //@mark
                                if (nums[i] >= 1 && nums[i] <= limit) present[nums[i]] = true;  //@mark
                            }
                            int* out = malloc(k * sizeof(int));  //@read
                            for (int found = 0, x = 1; found < k; x++) {  //@read
                                if (!present[x]) out[found++] = x;  //@read
                            }
                            free(present);  //@ret
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("limit", "The answers all lie in `1 … n + k`, so that's the only range worth tracking. One flag per value (index 0 is unused, so index `v` means value `v`).",
                     {"c": "`calloc` starts every flag at false."}),
                    ("mark", "Flag each number that could block an answer. Zeros, negatives and anything above `limit` can't, so they're skipped (and they'd be out of the array's range anyway)."),
                    ("read", "Collect unflagged values in increasing order until there are k of them. Because at least k values in `1 … limit` are unflagged, `x` never runs past `limit`."),
                    ("ret", "Return the k smallest missing positives.", {"c": "Free the flags and report the length; the caller frees `out`."}),
                ],
                complexity=[
                    """
                    **Time O(n + k):** one pass to flag, at most n + k steps to read. No hashing, so it's
                    O(1) per step in the worst case, not just on average.

                    **Space O(n + k)** for the flags (2 × 10⁵ booleans at most).
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - **Bound the answer first.** "n items can block at most n values" tells you every answer lies in
              `1 … n + k`, and a small known range means an array can replace a hash set.
            - Values outside the useful range are noise: skip them before indexing.
            - For the classic k = 1 version, the same bound is `1 … n + 1`, and if you're allowed to
              rearrange the input you can even do it in O(1) extra space by parking each value `v` at index
              `v − 1` (cyclic sort). See **First Missing Ticket**.
            """
        ],
    )


@problem
def swapped_label():
    labels = [3, 1, 2, 5, 3]
    n = len(labels)
    assert sorted(labels) != list(range(1, n + 1))

    w1 = Steps("For every number 1 … n, count its copies by scanning the shelf.")
    dup = miss = None
    for x in range(1, n + 1):
        c = labels.count(x)
        st = {i: ("mark" if c == 2 else "found") for i, v in enumerate(labels) if v == x}
        if c == 2:
            dup = x
        if c == 0:
            miss = x
        w1.step(f"{x}: {c} cop{'y' if c == 1 else 'ies'}" + (" → the duplicate." if c == 2 else " → the missing one." if c == 0 else "."), Row(labels, st=st, slots=True), Vars(duplicate=dup, missing=miss))
    w1.step(f"Answer [{dup}, {miss}].", Row(labels, slots=True), result=[dup, miss])

    w2 = Steps("Tally each label in a count array, then read off the 2 and the 0.")
    cnt = [0] * (n + 1)
    for v in labels:
        cnt[v] += 1
        w2.step(f"Label {v}: count[{v}] = {cnt[v]}.", Row(labels, st={labels.index(v): "active"}, slots=True), Row(cnt[1:], st={v - 1: "new"}, label="count of 1 … n"))
    w2.step(f"count is 2 for {cnt.index(2)} and 0 for {cnt[1:].index(0) + 1}.", Row(cnt[1:], st={cnt.index(2) - 1: "mark", cnt[1:].index(0): "answer"}, label="count of 1 … n"), result=[cnt.index(2), cnt[1:].index(0) + 1])

    w3 = Steps("Park every label at index label − 1. The one spot that can't be filled reveals both answers.")
    a = labels[:]
    w3.step("Goal: position i holds i + 1.", Row(a, slots=True))
    i = 0
    guard = 0
    while i < n and guard < 40:
        guard += 1
        j = a[i] - 1
        if a[i] != a[j]:
            w3.step(f"Position {i} holds {a[i]}, which belongs at {j} (holding {a[j]}). Swap.", Row(a, st={i: "active", j: "mark"}, ptr={"i": i}, slots=True))
            a[i], a[j] = a[j], a[i]
        else:
            why = "already home" if i == j else f"its home {j} already holds a {a[j]}: this is the duplicate copy"
            w3.step(f"Position {i} holds {a[i]}, {why}. Move on.", Row(a, st={i: "found" if i == j else "mark"}, ptr={"i": i}, slots=True))
            i += 1
    bad = next(p for p in range(n) if a[p] != p + 1)
    w3.step(f"Only position {bad} is wrong: it holds {a[bad]} (the duplicate) instead of {bad + 1} (the missing number).", Row(a, st={bad: "answer"}, slots=True), result=[a[bad], bad + 1])

    total, squares = sum(labels), sum(v * v for v in labels)
    d1 = total - n * (n + 1) // 2
    d2 = squares - n * (n + 1) * (2 * n + 1) // 6
    w4 = Steps("Compare the sum and the sum of squares with what 1 … n would give.")
    w4.step(f"Sum of labels {total}; sum of 1 … {n} is {n * (n + 1) // 2}. Difference: duplicate − missing = {d1}.", Row(labels, slots=True), Vars(diff=d1))
    w4.step(f"Sum of squares {squares}; for 1 … {n} it's {n * (n + 1) * (2 * n + 1) // 6}. Difference: duplicate² − missing² = {d2}.", Row([v * v for v in labels], label="squares"), Vars(diff=d1, sq_diff=d2))
    w4.step(f"duplicate² − missing² = (duplicate − missing)(duplicate + missing), so duplicate + missing = {d2} / {d1} = {d2 // d1}.", Row(labels, slots=True), Vars(diff=d1, total=d2 // d1))
    w4.step(f"duplicate = ({d1} + {d2 // d1}) / 2 = {(d1 + d2 // d1) // 2}, missing = {d2 // d1} − {(d1 + d2 // d1) // 2} = {d2 // d1 - (d1 + d2 // d1) // 2}.", Row(labels, st={i: "mark" for i, v in enumerate(labels) if v == 3}, slots=True), result=[(d1 + d2 // d1) // 2, d2 // d1 - (d1 + d2 // d1) // 2])

    sol(
        "swapped-label",
        summary="""
            Every number from 1 to n should appear once; one appears twice and one not at all. Counting
            finds both in O(n) with O(n) space. To get O(1) extra space, either park each label at index
            `label − 1` (cyclic sort), or compare the sum and the sum of squares with those of `1 … n` and
            solve two small equations.
        """,
        question=[
            """
            The shelf should carry the labels 1 to n once each. One label got printed twice, replacing
            another label. Return `[the duplicate, the missing one]`.

            - **Exactly one duplicate and one missing value**, and they're different numbers.
            - **All labels are between 1 and n**, so every label is a valid index once you subtract 1. That
              property is what the cyclic-sort approach relies on.
            - **Order of the answer matters:** duplicate first.
            - **Size:** n up to 10⁵. Sums go up to ~10¹⁰ and sums of squares up to ~3 × 10¹⁴, so the
              arithmetic approach needs 64-bit integers.
            """
        ],
        think=[
            """
            Take `labels = [3, 1, 2, 5, 3]` (n = 5). By hand you'd tick off each number from 1 to 5: 1 ✓,
            2 ✓, 3 ✓✓ (twice!), 4 ✗ (never), 5 ✓. So the answer is `[3, 4]`.

            The ticking-off is a **count per value**. Every approach below is some way of getting those
            counts, or enough information to deduce the two odd ones out:

            - A count array indexed by label (simple, O(n) space).
            - Using the shelf itself as the count array: if label `v` goes to index `v − 1`, the duplicate
              finds its spot taken, and the missing number's spot is left holding the duplicate.
            - Arithmetic: compared with 1 … n, the sum is off by `duplicate − missing`. One equation isn't
              enough for two unknowns, so add a second one from the sum of squares.
            """,
            fig(Row([3, 1, 2, 5, 3], slots=True), Row([1, 2, 3, None, 5], st={2: "mark", 3: "answer"}, label="where each label belongs"),
                caption="Placing each label at index label − 1: two labels want index 2, and index 3 stays empty."),
        ],
        approaches=[
            approach(
                "Count each number by scanning",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each value from 1 to n, scan the shelf and count its copies: 2 copies is the duplicate, 0 is the missing one."],
                walk=w1,
                build=[
                    "For `x` from 1 to n, count how many labels equal `x` with a scan.",
                    "Count 2: remember `x` as the duplicate. Count 0: remember it as missing.",
                    "Return `[duplicate, missing]`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def findMislabel(self, labels: List[int]) -> List[int]:
                                dup = missing = -1
                                for x in range(1, len(labels) + 1):  #@each
                                    c = labels.count(x)  #@count
                                    if c == 2:  #@decide
                                        dup = x  #@decide
                                    elif c == 0:  #@decide
                                        missing = x  #@decide
                                return [dup, missing]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findMislabel(int[] labels) {
                                int n = labels.length, dup = -1, missing = -1;
                                for (int x = 1; x <= n; x++) {  //@each
                                    int c = 0;  //@count
                                    for (int v : labels) if (v == x) c++;  //@count
                                    if (c == 2) dup = x;  //@decide
                                    else if (c == 0) missing = x;  //@decide
                                }
                                return new int[] {dup, missing};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findMislabel(vector<int>& labels) {
                                int n = labels.size(), dup = -1, missing = -1;
                                for (int x = 1; x <= n; x++) {  //@each
                                    int c = count(labels.begin(), labels.end(), x);  //@count
                                    if (c == 2) dup = x;  //@decide
                                    else if (c == 0) missing = x;  //@decide
                                }
                                return {dup, missing};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findMislabel(int* labels, int labelsSize, int* returnSize) {
                            int dup = -1, missing = -1;
                            for (int x = 1; x <= labelsSize; x++) {  //@each
                                int c = 0;  //@count
                                for (int i = 0; i < labelsSize; i++) if (labels[i] == x) c++;  //@count
                                if (c == 2) dup = x;  //@decide
                                else if (c == 0) missing = x;  //@decide
                            }
                            int* out = malloc(2 * sizeof(int));  //@ret
                            out[0] = dup;  //@ret
                            out[1] = missing;  //@ret
                            *returnSize = 2;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("each", "Every label that should be on the shelf."),
                    ("count", "Count its copies with a full scan."),
                    ("decide", "Two copies: the duplicate. None: the missing label. One: normal."),
                    ("ret", "Duplicate first, then missing.", {"c": "The answer is a new 2-element array; its length goes in `returnSize`."}),
                ],
                complexity=["**Time O(n²):** n scans of n labels. **Space O(1).**"],
                limits=["n separate scans to build what is really one table of counts. Build the table in one pass instead."],
                slow=True,
            ),
            approach(
                "Count array",
                "better",
                "O(n)",
                "O(n)",
                idea=["One pass fills `count[v]` for every label (labels are 1 … n, so they index an array directly). Then the value with count 2 is the duplicate and the value with count 0 is missing."],
                walk=w2,
                build=[
                    "Make `count` of size n + 1, all zeros.",
                    "For each label `v`, add 1 to `count[v]`.",
                    "Scan `v` from 1 to n: `count[v] == 2` → duplicate, `count[v] == 0` → missing.",
                ],
                code={
                    "python": """
                        class Solution:
                            def findMislabel(self, labels: List[int]) -> List[int]:
                                n = len(labels)
                                count = [0] * (n + 1)  #@tally
                                for v in labels:  #@tally
                                    count[v] += 1  #@tally
                                dup = missing = -1
                                for v in range(1, n + 1):  #@read
                                    if count[v] == 2:  #@read
                                        dup = v  #@read
                                    elif count[v] == 0:  #@read
                                        missing = v  #@read
                                return [dup, missing]  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] findMislabel(int[] labels) {
                                int n = labels.length;
                                int[] count = new int[n + 1];  //@tally
                                for (int v : labels) count[v]++;  //@tally
                                int dup = -1, missing = -1;
                                for (int v = 1; v <= n; v++) {  //@read
                                    if (count[v] == 2) dup = v;  //@read
                                    else if (count[v] == 0) missing = v;  //@read
                                }
                                return new int[] {dup, missing};  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findMislabel(vector<int>& labels) {
                                int n = labels.size();
                                vector<int> count(n + 1, 0);  //@tally
                                for (int v : labels) count[v]++;  //@tally
                                int dup = -1, missing = -1;
                                for (int v = 1; v <= n; v++) {  //@read
                                    if (count[v] == 2) dup = v;  //@read
                                    else if (count[v] == 0) missing = v;  //@read
                                }
                                return {dup, missing};  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* findMislabel(int* labels, int labelsSize, int* returnSize) {
                            int n = labelsSize;
                            int* count = calloc(n + 1, sizeof(int));  //@tally
                            for (int i = 0; i < n; i++) count[labels[i]]++;  //@tally
                            int* out = malloc(2 * sizeof(int));  //@read
                            for (int v = 1; v <= n; v++) {  //@read
                                if (count[v] == 2) out[0] = v;  //@read
                                else if (count[v] == 0) out[1] = v;  //@read
                            }
                            free(count);  //@ret
                            *returnSize = 2;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("tally", "Labels are 1 … n, so `count[label]` is a valid index (index 0 goes unused). One pass tallies everything."),
                    ("read", "The odd ones out: the count of 2 and the count of 0.", {"c": "Write them straight into the answer array."}),
                    ("ret", "Duplicate, then missing.", {"c": "Free the counts and report the length."}),
                ],
                complexity=["**Time O(n):** two passes. **Space O(n)** for the counts."],
                limits=["Correct and fast, but it allocates a second array as big as the input. Two approaches get the answer in O(1) extra space."],
            ),
            approach(
                "Park each label at its own index",
                "better",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Use the shelf itself as the table. Label `v` belongs at index `v − 1`. Walk with `i`:

                    - If `labels[i]` isn't at its home and its home doesn't already hold the same value, swap
                      it home. (Stay at `i`: a new label just arrived there.)
                    - Otherwise move on: either it's home, or its home already has that value, which means
                      it's the duplicate's extra copy.

                    Every swap sends one label home for good, so there are fewer than n swaps. At the end,
                    every index holds its own label except one: index `m − 1`, where `m` is the missing label,
                    and it holds the duplicate.
                    """
                ],
                walk=w3,
                build=[
                    "Set `i = 0`. While `i < n`: let `j = labels[i] − 1` (its home).",
                    "If `labels[i] != labels[j]`, swap them and don't advance `i`.",
                    "Else advance `i`. (Comparing values, not indices, is what stops an endless swap of two equal labels.)",
                    "Scan for the index `p` with `labels[p] != p + 1`: return `[labels[p], p + 1]`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def findMislabel(self, labels: List[int]) -> List[int]:
                                a = labels  #@alias
                                i = 0  #@park
                                while i < len(a):  #@park
                                    j = a[i] - 1  #@park
                                    if a[i] != a[j]:  #@swap
                                        a[i], a[j] = a[j], a[i]  #@swap
                                    else:  #@stay
                                        i += 1  #@stay
                                for p, v in enumerate(a):  #@find
                                    if v != p + 1:  #@find
                                        return [v, p + 1]  #@find
                                return [-1, -1]  #@none
                    """,
                    "java": """
                        class Solution {
                            public int[] findMislabel(int[] labels) {
                                int[] a = labels;  //@alias
                                int i = 0;  //@park
                                while (i < a.length) {  //@park
                                    int j = a[i] - 1;  //@park
                                    if (a[i] != a[j]) {  //@swap
                                        int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                    } else {  //@stay
                                        i++;  //@stay
                                    }
                                }
                                for (int p = 0; p < a.length; p++) {  //@find
                                    if (a[p] != p + 1) return new int[] {a[p], p + 1};  //@find
                                }
                                return new int[] {-1, -1};  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findMislabel(vector<int>& labels) {
                                vector<int>& a = labels;  //@alias
                                int i = 0, n = a.size();  //@park
                                while (i < n) {  //@park
                                    int j = a[i] - 1;  //@park
                                    if (a[i] != a[j]) swap(a[i], a[j]);  //@swap
                                    else i++;  //@stay
                                }
                                for (int p = 0; p < n; p++) {  //@find
                                    if (a[p] != p + 1) return {a[p], p + 1};  //@find
                                }
                                return {-1, -1};  //@none
                            }
                        };
                    """,
                    "c": """
                        int* findMislabel(int* labels, int labelsSize, int* returnSize) {
                            int* a = labels;  //@alias
                            int i = 0;  //@park
                            while (i < labelsSize) {  //@park
                                int j = a[i] - 1;  //@park
                                if (a[i] != a[j]) {  //@swap
                                    int t = a[i]; a[i] = a[j]; a[j] = t;  //@swap
                                } else {  //@stay
                                    i++;  //@stay
                                }
                            }
                            int* out = malloc(2 * sizeof(int));  //@find
                            *returnSize = 2;  //@find
                            out[0] = out[1] = -1;  //@find
                            for (int p = 0; p < labelsSize; p++) {  //@find
                                if (a[p] != p + 1) { out[0] = a[p]; out[1] = p + 1; break; }  //@find
                            }
                            return out;  //@find
                        }
                    """,
                },
                lines=[
                    ("alias", "We rearrange the input in place; that's what makes the extra space O(1). (If the caller needs the original order, copy it first and the space becomes O(n).)"),
                    ("park", "Look at the label at `i` and its home index `j = label − 1`. Labels are 1 … n, so `j` is always a valid index."),
                    ("swap", "Its home holds a different value, so send it home. Don't move `i`: the label that came back from `j` hasn't been placed yet."),
                    ("stay", "Either it's already home (`i == j`), or its home already holds the same value: this is the duplicate's spare copy, which has nowhere to go. Leave it and move on."),
                    ("find", "Now every label sits at home except the spare copy of the duplicate, which occupies the missing label's home. That one mismatch gives both answers.",
                     {"c": "Allocate the answer and fill it from the mismatch."}),
                    ("none", "Unreachable with valid input."),
                ],
                complexity=[
                    """
                    **Time O(n):** every swap puts one label home permanently, so there are at most n − 1
                    swaps, and `i` advances n times.

                    **Space O(1)** extra, but it **rearranges the input**.
                    """
                ],
                limits=[
                    """
                    It changes the caller's array, and the loop has a classic trap: comparing indices
                    (`i != j`) instead of values (`a[i] != a[j]`) swaps the two equal copies forever. The
                    arithmetic approach needs neither swaps nor mutation.
                    """
                ],
            ),
            approach(
                "Two equations from the sum and the sum of squares",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Call the duplicate `d` and the missing number `m`. Compared with the perfect shelf
                    `1 … n`, the actual labels have an extra `d` and lack an `m`, so:

                    - `sum(labels) − (1 + 2 + … + n) = d − m`
                    - `sum(labels²) − (1² + 2² + … + n²) = d² − m² = (d − m)(d + m)`

                    Divide the second by the first to get `d + m`. Then `d = ((d − m) + (d + m)) / 2` and
                    `m = (d + m) − d`. Since `d ≠ m`, the first difference is never zero, so the division is
                    safe.

                    The formulas `1 + … + n = n(n + 1)/2` and `1² + … + n² = n(n + 1)(2n + 1)/6` avoid a second
                    loop.
                    """
                ],
                walk=w4,
                build=[
                    "In one pass, add up the labels and their squares (64-bit).",
                    "`diff = sum − n(n + 1)/2`, which equals d − m.",
                    "`sqDiff = squares − n(n + 1)(2n + 1)/6`, which equals d² − m².",
                    "`both = sqDiff / diff` (= d + m). Then `d = (diff + both) / 2` and `m = both − d`.",
                ],
                code={
                    "python": """
                        class Solution:
                            def findMislabel(self, labels: List[int]) -> List[int]:
                                n = len(labels)
                                total = sum(labels)  #@sums
                                squares = sum(v * v for v in labels)  #@sums
                                diff = total - n * (n + 1) // 2  #@diff
                                sq_diff = squares - n * (n + 1) * (2 * n + 1) // 6  #@sq
                                both = sq_diff // diff  #@both
                                dup = (diff + both) // 2  #@solve
                                return [dup, both - dup]  #@solve
                    """,
                    "java": """
                        class Solution {
                            public int[] findMislabel(int[] labels) {
                                long n = labels.length, total = 0, squares = 0;
                                for (int v : labels) {  //@sums
                                    total += v;  //@sums
                                    squares += (long) v * v;  //@sums
                                }
                                long diff = total - n * (n + 1) / 2;  //@diff
                                long sqDiff = squares - n * (n + 1) * (2 * n + 1) / 6;  //@sq
                                long both = sqDiff / diff;  //@both
                                long dup = (diff + both) / 2;  //@solve
                                return new int[] {(int) dup, (int) (both - dup)};  //@solve
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> findMislabel(vector<int>& labels) {
                                long long n = labels.size(), total = 0, squares = 0;
                                for (int v : labels) {  //@sums
                                    total += v;  //@sums
                                    squares += (long long) v * v;  //@sums
                                }
                                long long diff = total - n * (n + 1) / 2;  //@diff
                                long long sqDiff = squares - n * (n + 1) * (2 * n + 1) / 6;  //@sq
                                long long both = sqDiff / diff;  //@both
                                long long dup = (diff + both) / 2;  //@solve
                                return {(int) dup, (int) (both - dup)};  //@solve
                            }
                        };
                    """,
                    "c": """
                        int* findMislabel(int* labels, int labelsSize, int* returnSize) {
                            long long n = labelsSize, total = 0, squares = 0;
                            for (int i = 0; i < labelsSize; i++) {  //@sums
                                total += labels[i];  //@sums
                                squares += (long long) labels[i] * labels[i];  //@sums
                            }
                            long long diff = total - n * (n + 1) / 2;  //@diff
                            long long sqDiff = squares - n * (n + 1) * (2 * n + 1) / 6;  //@sq
                            long long both = sqDiff / diff;  //@both
                            long long dup = (diff + both) / 2;  //@solve
                            int* out = malloc(2 * sizeof(int));  //@solve
                            out[0] = (int) dup;  //@solve
                            out[1] = (int) (both - dup);  //@solve
                            *returnSize = 2;  //@solve
                            return out;  //@solve
                        }
                    """,
                },
                lines=[
                    ("sums", "One pass for the sum and the sum of squares. Both need 64 bits: the squares add up to about 3 × 10¹⁴ for n = 10⁵.",
                     {"java": "`(long) v * v` widens before multiplying; `v * v` alone is fine for v ≤ 10⁵, but widening is the safe habit.",
                      "cpp": "`(long long) v * v` widens before multiplying.",
                      "c": "`(long long)` widens before multiplying."}),
                    ("diff", "The perfect shelf sums to n(n + 1)/2. Ours has an extra d and lacks m, so the difference is d − m (never 0, since d ≠ m)."),
                    ("sq", "Same idea for squares: 1² + … + n² = n(n + 1)(2n + 1)/6, and the difference is d² − m². The product n(n + 1)(2n + 1) is about 2 × 10¹⁵, comfortably inside 64 bits."),
                    ("both", "d² − m² = (d − m)(d + m), so dividing by d − m leaves d + m. The division is exact."),
                    ("solve", "Two equations, two unknowns: adding `d − m` and `d + m` gives `2d`.", {"c": "Pack both into the answer array and report its length."}),
                ],
                complexity=[
                    """
                    **Time O(n):** one pass.

                    **Space O(1):** a few numbers, and the input is left untouched.
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - When values are exactly `1 … n` (with a defect or two), **value − 1 is an index**. That lets an
              array, or the input itself, act as the count table.
            - In-place cyclic sort: swap a value home until its home already holds an equal value. Compare
              **values**, not indices, to avoid infinite swaps with duplicates.
            - Two unknowns need two independent equations: sum gives `d − m`, sum of squares gives
              `d² − m²`. Mind 64-bit overflow on the squares.
            """
        ],
    )
