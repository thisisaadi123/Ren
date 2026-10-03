"""Arrays & Hashing: prefix and suffix products (and maxima)."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


@problem
def everyone_elses_product():
    nums = [3, -1, 2, 2, -2]
    n = len(nums)
    want = []
    for i in range(n):
        p = 1
        for j in range(n):
            if j != i:
                p *= nums[j]
        want.append(p)

    w1 = Steps("For each index, multiply every other element.")
    for i in range(n):
        w1.step(f"Index {i}: " + " × ".join(str(nums[j]) for j in range(n) if j != i) + f" = {want[i]}.", Row(nums, st={j: ("dim" if j == i else "active") for j in range(n)}, slots=True), Row(want[:i + 1] + [None] * (n - i - 1), st={i: "new"}, label="answer", slots=True))
    w1.steps[-1]["result"] = str(want)

    pre = [1] * n
    for i in range(1, n):
        pre[i] = pre[i - 1] * nums[i - 1]
    suf = [1] * n
    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] * nums[i + 1]
    w2 = Steps("prefix[i] = product of everything left of i; suffix[i] = product of everything right of i. The answer is their product.")
    w2.step("prefix[0] = 1 (nothing on the left); each next one multiplies in one more element.", Row(nums, slots=True), Row(pre, label="prefix (left of i)", slots=True))
    w2.step("suffix[n − 1] = 1 (nothing on the right); built the same way from the right.", Row(nums, slots=True), Row(pre, label="prefix", slots=True), Row(suf, label="suffix (right of i)", slots=True))
    w2.step("answer[i] = prefix[i] × suffix[i].", Row(pre, label="prefix", slots=True), Row(suf, label="suffix", slots=True), Row(want, label="answer", st={k: "answer" for k in range(n)}, slots=True), result=want)

    w3 = Steps("Store the left products in the answer array, then sweep from the right with a running product.")
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    w3.step("Left pass: out[i] = product of everything before i.", Row(nums, slots=True), Row(list(out), label="out", slots=True))
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        w3.step(f"Right pass at {i}: multiply by right = {right} (product of everything after {i}) → {out[i]}.", Row(nums, st={i: "active"}, slots=True), Row(list(out), st={i: "new"}, label="out", slots=True), Vars(right=right))
        right *= nums[i]
    w3.steps[-1]["result"] = str(out)

    sol(
        "everyone-elses-product",
        summary="""
            "Product of everything except index i" = (product of everything **left** of i) × (product of everything
            **right** of i). Both are running products: one pass from the left, one from the right. Storing the left
            products in the answer array itself and carrying the right product in a variable gives O(n) time and
            O(1) extra space, with no division.
        """,
        question=[
            """
            For every index i, return the product of all elements **except** `nums[i]`, without using division.

            - **Why no division?** The obvious trick, "total product ÷ nums[i]", breaks on zeros: with one zero,
              every other answer is 0 but the zero's own answer isn't; with two zeros, all answers are 0. The
              no-division rule forces an approach that handles zeros naturally.
            - **Values are −2 … 2**, and at most 60 of them are ±2, so every answer fits in a 64-bit integer
              (|answer| ≤ 2⁶⁰). Use `long` in Java and C++/C.
            - **Size:** up to 10⁵, so the O(n²) "multiply all the others" is too slow.
            """
        ],
        think=[
            """
            Take `[3, −1, 2, 2, −2]`. For index 2, the answer is `3 × (−1)` (left of it) times `2 × (−2)` (right of
            it) = −3 × −4 = 12.
            """,
            fig(Row(nums, st={0: "found", 1: "found", 2: "mark", 3: "active", 4: "active"}, slots=True),
                caption="Everything except index 2 = the left block × the right block."),
            """
            Every answer splits the same way: left block × right block. And the left blocks grow one element at a
            time as i moves right (`1`, `3`, `3 × −1`, …), so all of them come from **one running product**. The
            same is true of the right blocks from the other end. Two passes, no division, and zeros need no special
            handling: a zero simply makes every block that contains it 0.
            """,
        ],
        approaches=[
            approach(
                "Multiply all the others for each index",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each i, loop over every j ≠ i and multiply. Direct, but each answer redoes almost the same work."],
                walk=w1,
                build=["For each i: start a product at 1.", "Multiply in every `nums[j]` with `j ≠ i` (64-bit).", "Store it."],
                code={
                    "python": """
                        class Solution:
                            def productOfOthers(self, nums: List[int]) -> List[int]:
                                n = len(nums)
                                out = []
                                for i in range(n):  #@each
                                    p = 1  #@prod
                                    for j in range(n):  #@prod
                                        if j != i:  #@prod
                                            p *= nums[j]  #@prod
                                    out.append(p)  #@store
                                return out  #@store
                    """,
                    "java": """
                        class Solution {
                            public long[] productOfOthers(int[] nums) {
                                int n = nums.length;
                                long[] out = new long[n];
                                for (int i = 0; i < n; i++) {  //@each
                                    long p = 1;  //@prod
                                    for (int j = 0; j < n; j++) if (j != i) p *= nums[j];  //@prod
                                    out[i] = p;  //@store
                                }
                                return out;  //@store
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<long long> productOfOthers(vector<int>& nums) {
                                int n = nums.size();
                                vector<long long> out(n);
                                for (int i = 0; i < n; i++) {  //@each
                                    long long p = 1;  //@prod
                                    for (int j = 0; j < n; j++) if (j != i) p *= nums[j];  //@prod
                                    out[i] = p;  //@store
                                }
                                return out;  //@store
                            }
                        };
                    """,
                    "c": """
                        long long* productOfOthers(int* nums, int numsSize, int* returnSize) {
                            long long* out = malloc(numsSize * sizeof(long long));
                            for (int i = 0; i < numsSize; i++) {  //@each
                                long long p = 1;  //@prod
                                for (int j = 0; j < numsSize; j++) if (j != i) p *= nums[j];  //@prod
                                out[i] = p;  //@store
                            }
                            *returnSize = numsSize;  //@store
                            return out;  //@store
                        }
                    """,
                },
                lines=[
                    ("each", "One answer per index."),
                    ("prod", "Multiply every element except the one at i. 64-bit, since products reach 2⁶⁰."),
                    ("store", "Save the answer."),
                ],
                complexity=["**Time O(n²).** **Space O(1)** besides the output."],
                limits=["The products for i and i + 1 share all but two factors, yet each is rebuilt from scratch. Running products from both ends share that work."],
                slow=True,
            ),
            approach(
                "Prefix and suffix product arrays",
                "better",
                "O(n)",
                "O(n)",
                idea=["Build `prefix[i]` = product of `nums[0 … i − 1]` (with `prefix[0] = 1`) and `suffix[i]` = product of `nums[i + 1 … n − 1]` (with `suffix[n − 1] = 1`). Then `answer[i] = prefix[i] × suffix[i]`."],
                walk=w2,
                build=["`prefix[0] = 1`; `prefix[i] = prefix[i − 1] × nums[i − 1]`.", "`suffix[n − 1] = 1`; `suffix[i] = suffix[i + 1] × nums[i + 1]`.", "`answer[i] = prefix[i] × suffix[i]`."],
                code={
                    "python": """
                        class Solution:
                            def productOfOthers(self, nums: List[int]) -> List[int]:
                                n = len(nums)
                                prefix = [1] * n  #@pre
                                for i in range(1, n):  #@pre
                                    prefix[i] = prefix[i - 1] * nums[i - 1]  #@pre
                                suffix = [1] * n  #@suf
                                for i in range(n - 2, -1, -1):  #@suf
                                    suffix[i] = suffix[i + 1] * nums[i + 1]  #@suf
                                return [prefix[i] * suffix[i] for i in range(n)]  #@combine
                    """,
                    "java": """
                        class Solution {
                            public long[] productOfOthers(int[] nums) {
                                int n = nums.length;
                                long[] prefix = new long[n], suffix = new long[n], out = new long[n];
                                prefix[0] = 1;  //@pre
                                for (int i = 1; i < n; i++) prefix[i] = prefix[i - 1] * nums[i - 1];  //@pre
                                suffix[n - 1] = 1;  //@suf
                                for (int i = n - 2; i >= 0; i--) suffix[i] = suffix[i + 1] * nums[i + 1];  //@suf
                                for (int i = 0; i < n; i++) out[i] = prefix[i] * suffix[i];  //@combine
                                return out;  //@combine
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<long long> productOfOthers(vector<int>& nums) {
                                int n = nums.size();
                                vector<long long> prefix(n, 1), suffix(n, 1), out(n);
                                for (int i = 1; i < n; i++) prefix[i] = prefix[i - 1] * nums[i - 1];  //@pre
                                for (int i = n - 2; i >= 0; i--) suffix[i] = suffix[i + 1] * nums[i + 1];  //@suf
                                for (int i = 0; i < n; i++) out[i] = prefix[i] * suffix[i];  //@combine
                                return out;  //@combine
                            }
                        };
                    """,
                    "c": """
                        long long* productOfOthers(int* nums, int numsSize, int* returnSize) {
                            int n = numsSize;
                            long long* prefix = malloc(n * sizeof(long long));
                            long long* suffix = malloc(n * sizeof(long long));
                            long long* out = malloc(n * sizeof(long long));
                            prefix[0] = 1;  //@pre
                            for (int i = 1; i < n; i++) prefix[i] = prefix[i - 1] * nums[i - 1];  //@pre
                            suffix[n - 1] = 1;  //@suf
                            for (int i = n - 2; i >= 0; i--) suffix[i] = suffix[i + 1] * nums[i + 1];  //@suf
                            for (int i = 0; i < n; i++) out[i] = prefix[i] * suffix[i];  //@combine
                            free(prefix);  //@combine
                            free(suffix);  //@combine
                            *returnSize = n;  //@combine
                            return out;  //@combine
                        }
                    """,
                },
                lines=[
                    ("pre", "Product of everything strictly left of i. Index 0 has nothing on its left, so its product is the empty product, 1."),
                    ("suf", "Product of everything strictly right of i, built from the end the same way."),
                    ("combine", "Left part × right part = everything except i.", {"c": "Free the two helper arrays; the caller frees `out`."}),
                ],
                complexity=["**Time O(n):** three passes. **Space O(n)** for the two helper arrays."],
                limits=["Two extra arrays of size n. The output array can hold the prefix products, and the suffix product only needs to exist one index at a time."],
            ),
            approach(
                "Left products in the output, right product on the fly",
                "best",
                "O(n)",
                "O(1)",
                idea=["Pass 1 (left to right): write the running left product into `out[i]` *before* multiplying in `nums[i]`. Pass 2 (right to left): keep `right`, the product of everything after i, multiply it into `out[i]`, then multiply `nums[i]` into `right`."],
                walk=w3,
                build=["`left = 1`; for i from 0: `out[i] = left`, then `left *= nums[i]`.", "`right = 1`; for i from n − 1 down: `out[i] *= right`, then `right *= nums[i]`.", "Return `out`."],
                code={
                    "python": """
                        class Solution:
                            def productOfOthers(self, nums: List[int]) -> List[int]:
                                n = len(nums)
                                out = [1] * n  #@out
                                left = 1  #@left
                                for i in range(n):  #@left
                                    out[i] = left  #@left
                                    left *= nums[i]  #@left
                                right = 1  #@right
                                for i in range(n - 1, -1, -1):  #@right
                                    out[i] *= right  #@right
                                    right *= nums[i]  #@right
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long[] productOfOthers(int[] nums) {
                                int n = nums.length;
                                long[] out = new long[n];  //@out
                                long left = 1;  //@left
                                for (int i = 0; i < n; i++) {  //@left
                                    out[i] = left;  //@left
                                    left *= nums[i];  //@left
                                }
                                long right = 1;  //@right
                                for (int i = n - 1; i >= 0; i--) {  //@right
                                    out[i] *= right;  //@right
                                    right *= nums[i];  //@right
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<long long> productOfOthers(vector<int>& nums) {
                                int n = nums.size();
                                vector<long long> out(n);  //@out
                                long long left = 1;  //@left
                                for (int i = 0; i < n; i++) {  //@left
                                    out[i] = left;  //@left
                                    left *= nums[i];  //@left
                                }
                                long long right = 1;  //@right
                                for (int i = n - 1; i >= 0; i--) {  //@right
                                    out[i] *= right;  //@right
                                    right *= nums[i];  //@right
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long* productOfOthers(int* nums, int numsSize, int* returnSize) {
                            int n = numsSize;
                            long long* out = malloc(n * sizeof(long long));  //@out
                            long long left = 1;  //@left
                            for (int i = 0; i < n; i++) {  //@left
                                out[i] = left;  //@left
                                left *= nums[i];  //@left
                            }
                            long long right = 1;  //@right
                            for (int i = n - 1; i >= 0; i--) {  //@right
                                out[i] *= right;  //@right
                                right *= nums[i];  //@right
                            }
                            *returnSize = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("out", "The answer array doubles as storage for the left products."),
                    ("left", "Write the product of everything **before** i, then include `nums[i]` for the next index. The order of these two lines is what excludes `nums[i]` itself."),
                    ("right", "Same idea from the right: multiply in the product of everything **after** i, then include `nums[i]`."),
                    ("ret", "Each `out[i]` = left part × right part."),
                ],
                complexity=["**Time O(n):** two passes. **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - "All except i" = **prefix up to i − 1** combined with **suffix from i + 1**. Works for products, sums,
              maxima, …
            - Write the running value *before* folding in the current element to exclude it.
            - The output array can store one direction's results; carry the other direction in a variable.
            """
        ],
    )


@problem
def rain_on_the_skyline():
    w = [3, 0, 2, 0, 4, 1, 0, 2]
    n = len(w)
    lmax = [max(w[:i + 1]) for i in range(n)]
    rmax = [max(w[i:]) for i in range(n)]
    water = [min(lmax[i], rmax[i]) - w[i] for i in range(n)]
    total = sum(water)
    assert total == 10

    w1 = Steps("For each column, find the tallest wall on its left and on its right by scanning. Water = the lower of the two − its own height.")
    for i in range(n):
        L, R = max(w[:i + 1]), max(w[i:])
        w1.step(f"Column {i} (height {w[i]}): tallest left {L}, tallest right {R}; water min({L}, {R}) − {w[i]} = {min(L, R) - w[i]}.", Row(w, st={**{k: "dim" for k in range(n)}, **{w.index(L) if L in w[:i + 1] else i: "found"}, i: "active"}, slots=True), Row(water[:i + 1] + [None] * (n - i - 1), st={i: "new"}, label="water", slots=True))
    w1.step(f"Total {total}.", Row(water, label="water", slots=True), result=total)

    w2 = Steps("Precompute the running maximum from the left and from the right, then combine.")
    w2.step("leftMax[i] = tallest of columns 0 … i.", Row(w, label="height", slots=True), Row(lmax, label="leftMax", slots=True))
    w2.step("rightMax[i] = tallest of columns i … n − 1.", Row(w, label="height", slots=True), Row(lmax, label="leftMax", slots=True), Row(rmax, label="rightMax", slots=True))
    w2.step("water[i] = min(leftMax[i], rightMax[i]) − height[i].", Row(lmax, label="leftMax", slots=True), Row(rmax, label="rightMax", slots=True), Row(water, label="water", st={k: "answer" for k in range(n) if water[k]}, slots=True), result=total)

    w3 = Steps("Two pointers. Always settle the side whose wall is lower: its water is decided by its own running max.")
    lo, hi, lm, rm, tot = 0, n - 1, 0, 0, 0
    while lo < hi:
        if w[lo] < w[hi]:
            lm = max(lm, w[lo])
            tot += lm - w[lo]
            w3.step(f"Left wall {w[lo]} < right wall {w[hi]}: something on the right is at least {w[hi]}, so column {lo} holds leftMax − height = {lm} − {w[lo]} = {lm - w[lo]}.", Row(w, st={lo: "active", hi: "mark"}, ptr={"lo": lo, "hi": hi}, slots=True), Vars(leftMax=lm, rightMax=rm, total=tot))
            lo += 1
        else:
            rm = max(rm, w[hi])
            tot += rm - w[hi]
            w3.step(f"Right wall {w[hi]} ≤ left wall {w[lo]}: column {hi} holds rightMax − height = {rm} − {w[hi]} = {rm - w[hi]}.", Row(w, st={hi: "active", lo: "mark"}, ptr={"lo": lo, "hi": hi}, slots=True), Vars(leftMax=lm, rightMax=rm, total=tot))
            hi -= 1
    w3.step(f"Pointers met. Total {tot}.", Row(w, slots=True), result=tot)
    assert tot == total

    sol(
        "rain-on-the-skyline",
        summary="""
            The water above a column is decided by the **lower** of the tallest wall to its left and the tallest wall
            to its right, minus the column's own height. Running maxima from both ends give every column's answer in
            O(n). The two-pointer version notices that the lower side's limit is already known, and drops the arrays:
            O(n) time, O(1) space.
        """,
        question=[
            """
            Columns of width 1 have heights `walls[i]`. After rain, water sits wherever it's held in by taller columns on
            **both** sides; anything over the ends runs off. Return the total water, in unit squares.

            - **Both sides matter:** water above column i can rise only as high as the shorter of its two
              surrounding "dam walls".
            - **The ends hold nothing** (water runs off the edge), and a strictly rising or falling skyline holds
              nothing.
            - **The total can be large:** up to 10⁵ columns × 10⁵ height ≈ 10¹⁰, more than 32 bits. Use 64-bit.
            - **Size:** up to 10⁵ columns, so the per-column scan in both directions (O(n²)) is too slow.
            """
        ],
        think=[
            """
            Take `walls = [3, 0, 2, 0, 4, 1, 0, 2]`. Look at column 3 (height 0). The tallest wall to its left is 3,
            the tallest to its right is 4. Water above it rises until it would spill over the **lower** of those,
            so it reaches level 3: 3 units of water.
            """,
            fig(Row(w, label="height", slots=True), Row(water, label="water above", st={k: "answer" for k in range(n) if water[k]}, slots=True),
                caption=f"Per column: min(tallest left, tallest right) − own height. Total {total}."),
            """
            So for every column, `water[i] = min(leftMax[i], rightMax[i]) − walls[i]`, where the maxima include the
            column itself (which makes the value never negative). The rest is computing those maxima efficiently:

            - by scanning both ways for each column (O(n²));
            - with running maxima from each end (O(n), two arrays);
            - or with two pointers that settle the lower side first (O(n), no arrays).
            """,
        ],
        approaches=[
            approach(
                "Scan both ways for every column",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each column, scan left for the tallest wall (including itself) and right for the tallest wall (including itself). Add `min(left, right) − height`."],
                walk=w1,
                build=["For each i: `L` = max of `walls[0 … i]`, `R` = max of `walls[i … n − 1]`.", "Add `min(L, R) − walls[i]` to a 64-bit total."],
                code={
                    "python": """
                        class Solution:
                            def trappedWater(self, walls: List[int]) -> int:
                                n = len(walls)
                                total = 0
                                for i in range(n):  #@each
                                    left = max(walls[:i + 1])  #@scan
                                    right = max(walls[i:])  #@scan
                                    total += min(left, right) - walls[i]  #@add
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long trappedWater(int[] walls) {
                                int n = walls.length;
                                long total = 0;
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = 0, right = 0;  //@scan
                                    for (int k = 0; k <= i; k++) left = Math.max(left, walls[k]);  //@scan
                                    for (int k = i; k < n; k++) right = Math.max(right, walls[k]);  //@scan
                                    total += Math.min(left, right) - walls[i];  //@add
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long trappedWater(vector<int>& walls) {
                                int n = walls.size();
                                long long total = 0;
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = 0, right = 0;  //@scan
                                    for (int k = 0; k <= i; k++) left = max(left, walls[k]);  //@scan
                                    for (int k = i; k < n; k++) right = max(right, walls[k]);  //@scan
                                    total += min(left, right) - walls[i];  //@add
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long trappedWater(int* walls, int wallsSize) {
                            int n = wallsSize;
                            long long total = 0;
                            for (int i = 0; i < n; i++) {  //@each
                                int left = 0, right = 0;  //@scan
                                for (int k = 0; k <= i; k++) if (walls[k] > left) left = walls[k];  //@scan
                                for (int k = i; k < n; k++) if (walls[k] > right) right = walls[k];  //@scan
                                total += (left < right ? left : right) - walls[i];  //@add
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("each", "Water is computed column by column."),
                    ("scan", "Tallest wall at or left of i, and at or right of i. Including i itself makes `min − height` at least 0."),
                    ("add", "The lower dam decides the water level; subtract the column's own height."),
                    ("ret", "Total water (64-bit)."),
                ],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Neighbouring columns repeat almost the same scans. The left maximum for i + 1 is just `max(leftMax for i, walls[i + 1])`: a running maximum."],
                slow=True,
            ),
            approach(
                "Running maxima from both ends",
                "better",
                "O(n)",
                "O(n)",
                idea=["`leftMax[i] = max(leftMax[i − 1], walls[i])` from the left; `rightMax[i] = max(rightMax[i + 1], walls[i])` from the right. Then sum `min(leftMax[i], rightMax[i]) − walls[i]`."],
                walk=w2,
                build=["Fill `leftMax` left to right.", "Fill `rightMax` right to left.", "Sum `min(leftMax[i], rightMax[i]) − walls[i]` (64-bit)."],
                code={
                    "python": """
                        class Solution:
                            def trappedWater(self, walls: List[int]) -> int:
                                n = len(walls)
                                left_max = [0] * n  #@left
                                left_max[0] = walls[0]  #@left
                                for i in range(1, n):  #@left
                                    left_max[i] = max(left_max[i - 1], walls[i])  #@left
                                right_max = [0] * n  #@right
                                right_max[-1] = walls[-1]  #@right
                                for i in range(n - 2, -1, -1):  #@right
                                    right_max[i] = max(right_max[i + 1], walls[i])  #@right
                                return sum(min(left_max[i], right_max[i]) - walls[i] for i in range(n))  #@sum
                    """,
                    "java": """
                        class Solution {
                            public long trappedWater(int[] walls) {
                                int n = walls.length;
                                int[] leftMax = new int[n], rightMax = new int[n];
                                leftMax[0] = walls[0];  //@left
                                for (int i = 1; i < n; i++) leftMax[i] = Math.max(leftMax[i - 1], walls[i]);  //@left
                                rightMax[n - 1] = walls[n - 1];  //@right
                                for (int i = n - 2; i >= 0; i--) rightMax[i] = Math.max(rightMax[i + 1], walls[i]);  //@right
                                long total = 0;  //@sum
                                for (int i = 0; i < n; i++) total += Math.min(leftMax[i], rightMax[i]) - walls[i];  //@sum
                                return total;  //@sum
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long trappedWater(vector<int>& walls) {
                                int n = walls.size();
                                vector<int> leftMax(n), rightMax(n);
                                leftMax[0] = walls[0];  //@left
                                for (int i = 1; i < n; i++) leftMax[i] = max(leftMax[i - 1], walls[i]);  //@left
                                rightMax[n - 1] = walls[n - 1];  //@right
                                for (int i = n - 2; i >= 0; i--) rightMax[i] = max(rightMax[i + 1], walls[i]);  //@right
                                long long total = 0;  //@sum
                                for (int i = 0; i < n; i++) total += min(leftMax[i], rightMax[i]) - walls[i];  //@sum
                                return total;  //@sum
                            }
                        };
                    """,
                    "c": """
                        long long trappedWater(int* walls, int wallsSize) {
                            int n = wallsSize;
                            int* leftMax = malloc(n * sizeof(int));
                            int* rightMax = malloc(n * sizeof(int));
                            leftMax[0] = walls[0];  //@left
                            for (int i = 1; i < n; i++) leftMax[i] = walls[i] > leftMax[i - 1] ? walls[i] : leftMax[i - 1];  //@left
                            rightMax[n - 1] = walls[n - 1];  //@right
                            for (int i = n - 2; i >= 0; i--) rightMax[i] = walls[i] > rightMax[i + 1] ? walls[i] : rightMax[i + 1];  //@right
                            long long total = 0;  //@sum
                            for (int i = 0; i < n; i++) total += (leftMax[i] < rightMax[i] ? leftMax[i] : rightMax[i]) - walls[i];  //@sum
                            free(leftMax);  //@sum
                            free(rightMax);  //@sum
                            return total;  //@sum
                        }
                    """,
                },
                lines=[
                    ("left", "Tallest wall from the start up to and including i, built incrementally."),
                    ("right", "Tallest wall from i to the end, built from the right."),
                    ("sum", "Each column's water from the two maxima, added in 64 bits.", {"c": "Free both helper arrays."}),
                ],
                complexity=["**Time O(n):** three passes. **Space O(n)** for the two arrays."],
                limits=["Both arrays are only ever needed at one index at a time, if we process columns in the right order. Two pointers find that order."],
            ),
            approach(
                "Two pointers, settle the lower side",
                "best",
                "O(n)",
                "O(1)",
                idea=[
                    """
                    Pointers `lo` and `hi` start at the ends, with `leftMax` (tallest seen from the left) and `rightMax`
                    (tallest seen from the right).

                    The left pointer only ever moves when its wall is **lower** than the wall under the right
                    pointer. So every wall it has stood on (including the current one) is lower than some wall at or
                    beyond `hi`, which lies to the right of `lo`. That means the tallest wall on `lo`'s right is at
                    least `leftMax`, so `min(leftMax, tallest on the right) = leftMax`, and column `lo` holds exactly
                    `leftMax − walls[lo]`. Settle it and move `lo` right.

                    When `walls[hi] ≤ walls[lo]`, the same argument works in mirror image: settle column `hi` with
                    `rightMax` and move `hi` left.
                    """
                ],
                walk=w3,
                build=["`lo = 0`, `hi = n − 1`, both maxima 0, total 0.", "While `lo < hi`: if `walls[lo] < walls[hi]`, update `leftMax`, add `leftMax − walls[lo]`, `lo += 1`.", "Else update `rightMax`, add `rightMax − walls[hi]`, `hi −= 1`.", "Return the total."],
                code={
                    "python": """
                        class Solution:
                            def trappedWater(self, walls: List[int]) -> int:
                                lo, hi = 0, len(walls) - 1  #@init
                                left_max = right_max = total = 0  #@init
                                while lo < hi:  #@loop
                                    if walls[lo] < walls[hi]:  #@left
                                        left_max = max(left_max, walls[lo])  #@left
                                        total += left_max - walls[lo]  #@left
                                        lo += 1  #@left
                                    else:  #@right
                                        right_max = max(right_max, walls[hi])  #@right
                                        total += right_max - walls[hi]  #@right
                                        hi -= 1  #@right
                                return total  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long trappedWater(int[] walls) {
                                int lo = 0, hi = walls.length - 1, leftMax = 0, rightMax = 0;  //@init
                                long total = 0;  //@init
                                while (lo < hi) {  //@loop
                                    if (walls[lo] < walls[hi]) {  //@left
                                        leftMax = Math.max(leftMax, walls[lo]);  //@left
                                        total += leftMax - walls[lo];  //@left
                                        lo++;  //@left
                                    } else {  //@right
                                        rightMax = Math.max(rightMax, walls[hi]);  //@right
                                        total += rightMax - walls[hi];  //@right
                                        hi--;  //@right
                                    }
                                }
                                return total;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long trappedWater(vector<int>& walls) {
                                int lo = 0, hi = walls.size() - 1, leftMax = 0, rightMax = 0;  //@init
                                long long total = 0;  //@init
                                while (lo < hi) {  //@loop
                                    if (walls[lo] < walls[hi]) {  //@left
                                        leftMax = max(leftMax, walls[lo]);  //@left
                                        total += leftMax - walls[lo];  //@left
                                        lo++;  //@left
                                    } else {  //@right
                                        rightMax = max(rightMax, walls[hi]);  //@right
                                        total += rightMax - walls[hi];  //@right
                                        hi--;  //@right
                                    }
                                }
                                return total;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long trappedWater(int* walls, int wallsSize) {
                            int lo = 0, hi = wallsSize - 1, leftMax = 0, rightMax = 0;  //@init
                            long long total = 0;  //@init
                            while (lo < hi) {  //@loop
                                if (walls[lo] < walls[hi]) {  //@left
                                    if (walls[lo] > leftMax) leftMax = walls[lo];  //@left
                                    total += leftMax - walls[lo];  //@left
                                    lo++;  //@left
                                } else {  //@right
                                    if (walls[hi] > rightMax) rightMax = walls[hi];  //@right
                                    total += rightMax - walls[hi];  //@right
                                    hi--;  //@right
                                }
                            }
                            return total;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "One pointer per end and the tallest wall each side has seen so far."),
                    ("loop", "Each step settles one column for good; stop when the pointers meet (the last column is a peak and holds nothing extra)."),
                    ("left", "The left wall is the lower one. Every wall the left pointer has passed is lower than some wall the right pointer has seen, so the right side is guaranteed to be at least as tall as `leftMax`: the water here is `leftMax − height`."),
                    ("right", "Mirror case: the right side is the bottleneck, so `rightMax` decides this column's water."),
                    ("ret", "Total water."),
                ],
                complexity=["**Time O(n):** each column is settled once. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Water above a column = `min(max to the left, max to the right) − height`. Get both maxima with running
              prefix/suffix maxima.
            - **Two pointers** can replace both arrays: always process the side with the lower wall, because its
              bound is already known.
            - Totals over 10⁵ columns of height 10⁵ need 64-bit integers.
            """
        ],
    )


@problem
def taller_ahead():
    h = [4, 9, 2, 7, 3, 3, 1]
    n = len(h)
    want = [max(h[i + 1:]) if i < n - 1 else -1 for i in range(n)]

    w1 = Steps("For each building, scan everything after it for the tallest.")
    for i in range(n):
        rest = list(range(i + 1, n))
        st = {k: "dim" for k in range(i)}
        st[i] = "active"
        if rest:
            best = max(rest, key=lambda k: (h[k], -k))
            for k in rest:
                st[k] = "mark"
            st[best] = "answer"
            w1.step(f"Building {i}: tallest after it is {h[best]}.", Row(h, st=st, slots=True), Row(want[:i + 1] + [None] * (n - i - 1), st={i: "new"}, label="answer", slots=True))
        else:
            w1.step(f"Building {i} is the last one: −1.", Row(h, st=st, slots=True), Row(want, st={i: "new"}, label="answer", slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Walk from the right, carrying the tallest building seen so far.")
    best = -1
    out = [None] * n
    for i in range(n - 1, -1, -1):
        out[i] = best
        w2.step(f"Building {i}: answer = tallest seen so far ({best}); then fold in its own height {h[i]} → {max(best, h[i])}.", Row(h, st={i: "active", **{k: "dim" for k in range(i + 1, n)}}, slots=True), Row(list(out), st={i: "new"}, label="answer", slots=True), Vars(tallest_after=best))
        best = max(best, h[i])
    w2.steps[-1]["result"] = str(out)

    sol(
        "taller-ahead",
        summary="""
            "Tallest building strictly after i" is a **suffix maximum** that excludes i itself. Walk from the right end,
            write the running maximum into the answer **before** including the current building, then update it. One
            pass, O(n), O(1) extra space.
        """,
        question=[
            """
            For each building, return the height of the tallest building **strictly after** it, or −1 for the last
            building.

            - **Strictly after:** the building itself doesn't count. For `[2, 2, 2]` the answer is `[2, 2, −1]`: the
              first building sees two buildings of height 2.
            - **It's the maximum, not the next taller one.** `[4, 9, 2, 7, 3]` gives 9 for the first building even
              though 9 is just one step away; for building 2 (height 2) it's 7.
            - **Size:** up to 10⁵, so scanning the rest of the street for every building is too slow.
            """
        ],
        think=[
            """
            Take `[4, 9, 2, 7, 3, 3, 1]`. The answers are `[9, 7, 7, 3, 3, 1, −1]`.

            Read the answers from the **right**: −1, then 1, 3, 3, 7, 7, 9. Each one is the maximum of everything
            already passed when walking leftwards. So walk from the right carrying `best`, the tallest building seen
            so far; that is exactly the tallest building after the current one.
            """,
            fig(Row(h, label="height", slots=True), Row(want, label="tallest after", slots=True),
                caption="Reading right to left, the answers are a running maximum."),
            """
            The only subtlety is order: write `best` into the answer **before** adding the current building to it,
            so a building never counts as being "after" itself.
            """,
        ],
        approaches=[
            approach(
                "Scan the rest of the street for each building",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each i, scan `heights[i + 1 …]` and take the maximum, or −1 if there's nothing after it."],
                walk=w1,
                build=["For each i, set `best = −1`.", "Scan j from i + 1 to the end, keeping the maximum.", "Store `best`."],
                code={
                    "python": """
                        class Solution:
                            def tallestAhead(self, heights: List[int]) -> List[int]:
                                n = len(heights)
                                out = []
                                for i in range(n):  #@each
                                    best = -1  #@scan
                                    for j in range(i + 1, n):  #@scan
                                        best = max(best, heights[j])  #@scan
                                    out.append(best)  #@store
                                return out  #@store
                    """,
                    "java": """
                        class Solution {
                            public int[] tallestAhead(int[] heights) {
                                int n = heights.length;
                                int[] out = new int[n];
                                for (int i = 0; i < n; i++) {  //@each
                                    int best = -1;  //@scan
                                    for (int j = i + 1; j < n; j++) best = Math.max(best, heights[j]);  //@scan
                                    out[i] = best;  //@store
                                }
                                return out;  //@store
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> tallestAhead(vector<int>& heights) {
                                int n = heights.size();
                                vector<int> out(n);
                                for (int i = 0; i < n; i++) {  //@each
                                    int best = -1;  //@scan
                                    for (int j = i + 1; j < n; j++) best = max(best, heights[j]);  //@scan
                                    out[i] = best;  //@store
                                }
                                return out;  //@store
                            }
                        };
                    """,
                    "c": """
                        int* tallestAhead(int* heights, int heightsSize, int* returnSize) {
                            int n = heightsSize;
                            int* out = malloc(n * sizeof(int));
                            for (int i = 0; i < n; i++) {  //@each
                                int best = -1;  //@scan
                                for (int j = i + 1; j < n; j++) if (heights[j] > best) best = heights[j];  //@scan
                                out[i] = best;  //@store
                            }
                            *returnSize = n;  //@store
                            return out;  //@store
                        }
                    """,
                },
                lines=[
                    ("each", "One answer per building."),
                    ("scan", "Maximum over the buildings strictly after i; −1 stays if there are none (heights are ≥ 1, so −1 never wins otherwise)."),
                    ("store", "Save it."),
                ],
                complexity=["**Time O(n²).** **Space O(1)** besides the output."],
                limits=["The scans for i and i + 1 overlap almost entirely. The answer for i is just `max(heights[i + 1], answer for i + 1)`."],
                slow=True,
            ),
            approach(
                "Running maximum from the right",
                "best",
                "O(n)",
                "O(1)",
                idea=["Walk i from the last building to the first with `best = −1`. Set `out[i] = best` (the tallest strictly after i), then `best = max(best, heights[i])` so building i counts for everything before it."],
                walk=w2,
                build=["`best = −1`.", "For i from n − 1 down to 0: `out[i] = best`, then `best = max(best, heights[i])`.", "Return `out`."],
                code={
                    "python": """
                        class Solution:
                            def tallestAhead(self, heights: List[int]) -> List[int]:
                                out = [-1] * len(heights)  #@init
                                best = -1  #@init
                                for i in range(len(heights) - 1, -1, -1):  #@loop
                                    out[i] = best  #@write
                                    best = max(best, heights[i])  #@fold
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] tallestAhead(int[] heights) {
                                int[] out = new int[heights.length];  //@init
                                int best = -1;  //@init
                                for (int i = heights.length - 1; i >= 0; i--) {  //@loop
                                    out[i] = best;  //@write
                                    best = Math.max(best, heights[i]);  //@fold
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> tallestAhead(vector<int>& heights) {
                                vector<int> out(heights.size());  //@init
                                int best = -1;  //@init
                                for (int i = (int) heights.size() - 1; i >= 0; i--) {  //@loop
                                    out[i] = best;  //@write
                                    best = max(best, heights[i]);  //@fold
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* tallestAhead(int* heights, int heightsSize, int* returnSize) {
                            int* out = malloc(heightsSize * sizeof(int));  //@init
                            int best = -1;  //@init
                            for (int i = heightsSize - 1; i >= 0; i--) {  //@loop
                                out[i] = best;  //@write
                                if (heights[i] > best) best = heights[i];  //@fold
                            }
                            *returnSize = heightsSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("init", "Nothing has been seen yet from the right, so the tallest-so-far is −1 (the answer for the last building)."),
                    ("loop", "Right to left, so everything after i has already been seen."),
                    ("write", "Record the tallest building strictly after i **before** including i itself."),
                    ("fold", "Now include building i, for the buildings to its left."),
                    ("ret", "All answers."),
                ],
                complexity=["**Time O(n):** one pass. **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - "Best of everything after i" = a **suffix** running value, computed right to left.
            - Strictly after: write the running value *before* folding in the current element.
            - Prefix/suffix running values turn many O(n²) "look at the rest" problems into O(n).
            """
        ],
    )
