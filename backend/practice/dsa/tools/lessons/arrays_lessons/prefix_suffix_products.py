"""Lesson: Prefix and suffix passes (Arrays & Hashing, pattern 9)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

PIVOTS = {
    "python": """
        def count_pivots(nums):
            n = len(nums)                                   #@n
            right_min = [0] * n                             #@suffix
            smallest = float('inf')                         #@suffix
            for i in range(n - 1, -1, -1):                  #@suffix
                right_min[i] = smallest                     #@store
                smallest = min(smallest, nums[i])           #@fold
            count = 0                                       #@count
            left_max = float('-inf')                        #@count
            for i in range(n):                              #@scan
                if left_max < nums[i] < right_min[i]:       #@test
                    count += 1                              #@test
                left_max = max(left_max, nums[i])           #@left
            return count                                    #@ret
    """,
    "java": """
        static int countPivots(int[] nums) {
            int n = nums.length;                                    //@n
            long[] rightMin = new long[n];                          //@suffix
            long smallest = Long.MAX_VALUE;                         //@suffix
            for (int i = n - 1; i >= 0; i--) {                      //@suffix
                rightMin[i] = smallest;                             //@store
                smallest = Math.min(smallest, nums[i]);             //@fold
            }
            int count = 0;                                          //@count
            long leftMax = Long.MIN_VALUE;                          //@count
            for (int i = 0; i < n; i++) {                           //@scan
                if (leftMax < nums[i] && nums[i] < rightMin[i]) count++;  //@test
                leftMax = Math.max(leftMax, nums[i]);               //@left
            }
            return count;                                           //@ret
        }
    """,
    "cpp": """
        int countPivots(const vector<int>& nums) {
            int n = nums.size();                                    //@n
            vector<long long> rightMin(n);                          //@suffix
            long long smallest = LLONG_MAX;                         //@suffix
            for (int i = n - 1; i >= 0; i--) {                      //@suffix
                rightMin[i] = smallest;                             //@store
                smallest = min(smallest, (long long)nums[i]);       //@fold
            }
            int count = 0;                                          //@count
            long long leftMax = LLONG_MIN;                          //@count
            for (int i = 0; i < n; i++) {                           //@scan
                if (leftMax < nums[i] && nums[i] < rightMin[i]) count++;  //@test
                leftMax = max(leftMax, (long long)nums[i]);         //@left
            }
            return count;                                           //@ret
        }
    """,
    "c": """
        int countPivots(const int* nums, int n) {
            long long* rightMin = malloc((n > 0 ? n : 1) * sizeof(long long));  //@suffix
            long long smallest = LLONG_MAX;                         //@suffix
            for (int i = n - 1; i >= 0; i--) {                      //@suffix
                rightMin[i] = smallest;                             //@store
                if (nums[i] < smallest) smallest = nums[i];         //@fold
            }
            int count = 0;                                          //@count
            long long leftMax = LLONG_MIN;                          //@count
            for (int i = 0; i < n; i++) {                           //@scan
                if (leftMax < nums[i] && nums[i] < rightMin[i]) count++;  //@test
                if (nums[i] > leftMax) leftMax = nums[i];           //@left
            }
            free(rightMin);                                         //@ret
            return count;                                           //@ret
        }
    """,
}
PIVOTS_RUN = {
    "python": """
        print(count_pivots([2, 1, 4, 3, 6, 8, 7, 9]))
        print(count_pivots([5, 4, 3]))
        print(count_pivots([1, 2, 3]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countPivots(new int[] {2, 1, 4, 3, 6, 8, 7, 9}));
            System.out.println(countPivots(new int[] {5, 4, 3}));
            System.out.println(countPivots(new int[] {1, 2, 3}));
        }
    """,
    "cpp": """
        int main() {
            cout << countPivots({2, 1, 4, 3, 6, 8, 7, 9}) << "\\n" << countPivots({5, 4, 3}) << "\\n" << countPivots({1, 2, 3}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {2, 1, 4, 3, 6, 8, 7, 9}, b[] = {5, 4, 3}, c[] = {1, 2, 3};
            printf("%d\\n%d\\n%d\\n", countPivots(a, 8), countPivots(b, 3), countPivots(c, 3));
            return 0;
        }
    """,
}

FLIP = {
    "python": """
        def longest_after_flip(bits):
            n = len(bits)                                   #@n
            left = [0] * n                                  #@left
            for i in range(n):                              #@left
                if bits[i] == 1:                            #@left
                    left[i] = (left[i - 1] if i > 0 else 0) + 1     #@left
            right = [0] * n                                 #@right
            for i in range(n - 1, -1, -1):                  #@right
                if bits[i] == 1:                            #@right
                    right[i] = (right[i + 1] if i < n - 1 else 0) + 1   #@right
            best = max(left, default=0)                     #@noflip
            for i in range(n):                              #@zero
                if bits[i] == 0:                            #@zero
                    l = left[i - 1] if i > 0 else 0         #@join
                    r = right[i + 1] if i < n - 1 else 0    #@join
                    best = max(best, l + 1 + r)             #@join
            return best                                     #@ret
    """,
    "java": """
        static int longestAfterFlip(int[] bits) {
            int n = bits.length;                                    //@n
            int[] left = new int[n], right = new int[n];            //@left
            for (int i = 0; i < n; i++) {                           //@left
                if (bits[i] == 1) left[i] = (i > 0 ? left[i - 1] : 0) + 1;  //@left
            }
            for (int i = n - 1; i >= 0; i--) {                      //@right
                if (bits[i] == 1) right[i] = (i < n - 1 ? right[i + 1] : 0) + 1;  //@right
            }
            int best = 0;                                           //@noflip
            for (int x : left) best = Math.max(best, x);            //@noflip
            for (int i = 0; i < n; i++) {                           //@zero
                if (bits[i] == 0) {                                 //@zero
                    int l = i > 0 ? left[i - 1] : 0;                //@join
                    int r = i < n - 1 ? right[i + 1] : 0;           //@join
                    best = Math.max(best, l + 1 + r);               //@join
                }
            }
            return best;                                            //@ret
        }
    """,
    "cpp": """
        int longestAfterFlip(const vector<int>& bits) {
            int n = bits.size();                                    //@n
            vector<int> left(n, 0), right(n, 0);                    //@left
            for (int i = 0; i < n; i++) {                           //@left
                if (bits[i] == 1) left[i] = (i > 0 ? left[i - 1] : 0) + 1;  //@left
            }
            for (int i = n - 1; i >= 0; i--) {                      //@right
                if (bits[i] == 1) right[i] = (i < n - 1 ? right[i + 1] : 0) + 1;  //@right
            }
            int best = 0;                                           //@noflip
            for (int x : left) best = max(best, x);                 //@noflip
            for (int i = 0; i < n; i++) {                           //@zero
                if (bits[i] == 0) {                                 //@zero
                    int l = i > 0 ? left[i - 1] : 0;                //@join
                    int r = i < n - 1 ? right[i + 1] : 0;           //@join
                    best = max(best, l + 1 + r);                    //@join
                }
            }
            return best;                                            //@ret
        }
    """,
    "c": """
        int longestAfterFlip(const int* bits, int n) {
            int* left = calloc(n + 1, sizeof(int));                 //@left
            int* right = calloc(n + 1, sizeof(int));                //@left
            for (int i = 0; i < n; i++) {                           //@left
                if (bits[i] == 1) left[i] = (i > 0 ? left[i - 1] : 0) + 1;  //@left
            }
            for (int i = n - 1; i >= 0; i--) {                      //@right
                if (bits[i] == 1) right[i] = (i < n - 1 ? right[i + 1] : 0) + 1;  //@right
            }
            int best = 0;                                           //@noflip
            for (int i = 0; i < n; i++) if (left[i] > best) best = left[i];  //@noflip
            for (int i = 0; i < n; i++) {                           //@zero
                if (bits[i] == 0) {                                 //@zero
                    int l = i > 0 ? left[i - 1] : 0;                //@join
                    int r = i < n - 1 ? right[i + 1] : 0;           //@join
                    if (l + 1 + r > best) best = l + 1 + r;         //@join
                }
            }
            free(left); free(right);                                //@ret
            return best;                                            //@ret
        }
    """,
}
FLIP_RUN = {
    "python": """
        print(longest_after_flip([1, 1, 0, 1, 1, 1, 0, 1, 0, 1]))
        print(longest_after_flip([1, 1, 1]))
        print(longest_after_flip([0, 0]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(longestAfterFlip(new int[] {1, 1, 0, 1, 1, 1, 0, 1, 0, 1}));
            System.out.println(longestAfterFlip(new int[] {1, 1, 1}));
            System.out.println(longestAfterFlip(new int[] {0, 0}));
        }
    """,
    "cpp": """
        int main() {
            cout << longestAfterFlip({1, 1, 0, 1, 1, 1, 0, 1, 0, 1}) << "\\n" << longestAfterFlip({1, 1, 1}) << "\\n" << longestAfterFlip({0, 0}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 1, 0, 1, 1, 1, 0, 1, 0, 1}, b[] = {1, 1, 1}, c[] = {0, 0};
            printf("%d\\n%d\\n%d\\n", longestAfterFlip(a, 10), longestAfterFlip(b, 3), longestAfterFlip(c, 2));
            return 0;
        }
    """,
}

PROFIT = {
    "python": """
        def best_profit(prices):
            lowest = prices[0]                              #@start
            best = 0                                        #@start
            for p in prices[1:]:                            #@loop
                best = max(best, p - lowest)                #@sell
                lowest = min(lowest, p)                     #@low
            return best                                     #@ret
    """,
    "java": """
        static int bestProfit(int[] prices) {
            int lowest = prices[0], best = 0;               //@start
            for (int i = 1; i < prices.length; i++) {       //@loop
                best = Math.max(best, prices[i] - lowest);  //@sell
                lowest = Math.min(lowest, prices[i]);       //@low
            }
            return best;                                    //@ret
        }
    """,
    "cpp": """
        int bestProfit(const vector<int>& prices) {
            int lowest = prices[0], best = 0;               //@start
            for (size_t i = 1; i < prices.size(); i++) {    //@loop
                best = max(best, prices[i] - lowest);       //@sell
                lowest = min(lowest, prices[i]);            //@low
            }
            return best;                                    //@ret
        }
    """,
    "c": """
        int bestProfit(const int* prices, int n) {
            int lowest = prices[0], best = 0;               //@start
            for (int i = 1; i < n; i++) {                   //@loop
                if (prices[i] - lowest > best) best = prices[i] - lowest;  //@sell
                if (prices[i] < lowest) lowest = prices[i]; //@low
            }
            return best;                                    //@ret
        }
    """,
}
PROFIT_RUN = {
    "python": """
        print(best_profit([8, 3, 6, 2, 7, 5, 4]))
        print(best_profit([9, 7, 4, 1]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(bestProfit(new int[] {8, 3, 6, 2, 7, 5, 4}));
            System.out.println(bestProfit(new int[] {9, 7, 4, 1}));
        }
    """,
    "cpp": """
        int main() {
            cout << bestProfit({8, 3, 6, 2, 7, 5, 4}) << "\\n" << bestProfit({9, 7, 4, 1}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {8, 3, 6, 2, 7, 5, 4}, b[] = {9, 7, 4, 1};
            printf("%d\\n%d\\n", bestProfit(a, 7), bestProfit(b, 4));
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

count_pivots = py(PIVOTS["python"], "count_pivots")
longest_after_flip = py(FLIP["python"], "longest_after_flip")
best_profit = py(PROFIT["python"], "best_profit")

DEMO = [2, 1, 4, 3, 6, 8, 7, 9]
n = len(DEMO)
PMAX = [None] * n  # max strictly before i
SMIN = [None] * n  # min strictly after i
m = None
for i in range(n):
    PMAX[i] = m
    m = DEMO[i] if m is None else max(m, DEMO[i])
m = None
for i in range(n - 1, -1, -1):
    SMIN[i] = m
    m = DEMO[i] if m is None else min(m, DEMO[i])
PIV = [i for i in range(n) if (PMAX[i] is None or PMAX[i] < DEMO[i]) and (SMIN[i] is None or DEMO[i] < SMIN[i])]
assert len(PIV) == count_pivots(DEMO)


def brute_pivots(a):
    return sum(1 for i in range(len(a)) if all(a[j] < a[i] for j in range(i)) and all(a[j] > a[i] for j in range(i + 1, len(a))))


assert brute_pivots(DEMO) == len(PIV)
show = lambda xs: ["–" if x is None else x for x in xs]

pw = Steps(f"`count_pivots({DEMO})`. First a right-to-left pass records the smallest value after each index, then a left-to-right pass checks each one.")
pw.step("Pass 1 goes right to left, carrying the smallest value seen so far. Nothing is to the right of the last element.", Row(DEMO, slots=True, label="nums"), Row([None] * n, slots=True, label="smallest after"))
filled = [None] * n
for i in range(n - 1, -1, -1):
    filled[i] = SMIN[i] if SMIN[i] is not None else "–"
    cur = min(DEMO[i:])
    pw.step(f"Index {i}: the smallest value after it is {SMIN[i] if SMIN[i] is not None else 'nothing (it is the last one)'}. Store that, then fold in {DEMO[i]}: the running smallest becomes {cur}.",
            Row(DEMO, st={i: "active", **{j: "dim" for j in range(i + 1, n)}}, ptr={"i": i}, slots=True, label="nums"), Row(list(filled), st={i: "new"}, slots=True, label="smallest after"))
lm = None
for i in range(n):
    ok = i in PIV
    left = "nothing" if PMAX[i] is None else str(PMAX[i])
    right = "nothing" if SMIN[i] is None else str(SMIN[i])
    msg = f"Pass 2, index {i}: biggest before it is {left}, smallest after it is {right}. {DEMO[i]} " + ("beats everything before and is below everything after: a pivot." if ok else "fails one of the two tests.")
    pw.step(msg, Row(DEMO, st={**{p: "answer" for p in PIV if p < i}, i: "answer" if ok else "active"}, ptr={"i": i}, slots=True, label="nums"),
            M({"biggest before": left, "smallest after": right}))
pw.steps[-1]["result"] = str(len(PIV))

BITS = [1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
L = [0] * len(BITS)
R = [0] * len(BITS)
for i in range(len(BITS)):
    if BITS[i]:
        L[i] = (L[i - 1] if i else 0) + 1
for i in range(len(BITS) - 1, -1, -1):
    if BITS[i]:
        R[i] = (R[i + 1] if i < len(BITS) - 1 else 0) + 1
joins = []
for i, b in enumerate(BITS):
    if b == 0:
        l = L[i - 1] if i else 0
        r = R[i + 1] if i < len(BITS) - 1 else 0
        joins.append((i, l, r, l + 1 + r))
BEST_FLIP = longest_after_flip(BITS)
best_zero = max(joins, key=lambda t: t[3])
assert BEST_FLIP == best_zero[3]

PRICES = [8, 3, 6, 2, 7, 5, 4]
PROF = best_profit(PRICES)
assert PROF == max(max(PRICES[j] - PRICES[i] for i in range(len(PRICES)) for j in range(i + 1, len(PRICES))), 0)
prw = Steps(f"`best_profit({PRICES})`: buy once, sell later. The prefix minimum is the only thing we need to remember.")
lowest, best = PRICES[0], 0
lows = [PRICES[0]]
prw.step(f"Day 0 costs {lowest}. You can't sell on the day you buy, so no profit yet.", Bars(PRICES, st={0: "mark"}, label="price"), M({"cheapest so far": lowest, "best profit": best}))
for d in range(1, len(PRICES)):
    p = PRICES[d]
    gain = p - lowest
    old_best = best
    best = max(best, gain)
    low_day = PRICES.index(lowest)
    msg = f"Day {d}: price {p}. Selling now after buying at {lowest} makes {gain}" + (f", the best so far." if best > old_best else ", which doesn't beat {old_best}.".format(old_best=old_best))
    if p < lowest:
        msg += f" {p} is also the new cheapest day."
    lowest = min(lowest, p)
    prw.step(msg, Bars(PRICES, st={low_day: "mark", d: "answer" if best > old_best else "active"}, label="price"), M({"cheapest so far": lowest, "best profit": best}))

# Example: longest "mountain" through each index (up then down).
MT = [1, 3, 5, 4, 2, 6, 7, 3, 1]
UP = [1] * len(MT)
DN = [1] * len(MT)
for i in range(1, len(MT)):
    if MT[i] > MT[i - 1]:
        UP[i] = UP[i - 1] + 1
for i in range(len(MT) - 2, -1, -1):
    if MT[i] > MT[i + 1]:
        DN[i] = DN[i + 1] + 1
MOUNT = [UP[i] + DN[i] - 1 if UP[i] > 1 and DN[i] > 1 else 0 for i in range(len(MT))]
TOPM = max(MOUNT)
TOPI = MOUNT.index(TOPM)

# Example: left sum minus right sum.
LS = [3, 1, 4, 1, 5]
TOT = sum(LS)
lr_rows, run = [], 0
for i, x in enumerate(LS):
    right = TOT - run - x
    lr_rows.append((str(i), str(x), str(run), str(right), str(abs(run - right))))
    run += x

lesson(
    "arrays-hashing",
    "prefix-suffix-products",
    """
    Some questions ask, for every index, about everything to its left *and* everything to its right. Rather than
    looking both ways from every index (O(n²)), make one pass from the left and one from the right, saving a running
    summary each time, and combine them.
    """,
    [
        ("idea", "The idea", [
            """
            Imagine everyone in a queue wants to know two things: who's the tallest person in front of them, and who's
            the shortest person behind them. Asking each person to turn around and look at everyone is slow. Instead, walk
            from the front of the queue to the back once, announcing "the tallest so far is…", and everyone writes it
            down. Then walk from the back to the front announcing "the shortest so far is…". Two walks, and everyone has
            both answers.

            That's the pattern. A **prefix pass** goes left to right and records, for each index, a summary of everything
            before it: the largest, the smallest, a sum, a product, the length of a run. A **suffix pass** does the same
            from the right. Then each index combines its two summaries.
            """,
            fig(Bars(DEMO, st={p: "answer" for p in PIV}, label="nums (pivots highlighted)"),
                Row(show(PMAX), slots=True, label="biggest before i"), Row(show(SMIN), slots=True, label="smallest after i"),
                caption=f"An element is a pivot when it's bigger than everything before it and smaller than everything after it. Two summary rows answer that for every index at once."),
            key("""
            When each index needs "something about everything to my left" and "something about everything to my right",
            build both with one left-to-right pass and one right-to-left pass, then combine them per index. O(n) instead
            of O(n²).
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Phrases like "for each element, … all elements before it / after it", "except itself", "everything to the
            left and right", "the tallest to the right", "water trapped between", "best day to buy before selling".

            The summaries have to be things you can update one element at a time: max, min, sum, product, count, the
            length of a run that's still going. If you can say "the summary for `i + 1` is the summary for `i`, plus
            element `i`", a prefix pass works.

            Related patterns, so you can tell them apart:

            - Prefix sums answer "the sum of any range `l..r`" by subtracting. Prefix and suffix passes answer "for
              each index, its left side and its right side". Max and min work here even though they can't be
              subtracted, because we never need a middle range, only "everything before" and "everything after".
            - Monotonic stacks (in the Stack & Queue topic) answer "the *nearest* bigger element to the right", which
              a suffix max can't, because a running max forgets *where* things are.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Running summaries

            Take "the biggest value before index `i`". Call it `before[i]`. Then `before[0]` is "nothing" (use -∞), and
            `before[i + 1] = max(before[i], nums[i])`. Each entry needs only the previous entry and one element, so a
            single left-to-right loop fills the whole array in O(n). The same works from the right:
            `after[n - 1]` is "nothing" (+∞), and `after[i - 1] = min(after[i], nums[i])`.

            This works for any summary that can be **folded** one element at a time: max, min, sum, product, gcd, "has a
            zero appeared", "length of the run of 1s ending here". It's the same idea as a prefix sum, just with other
            operations.

            ### Strictly before vs including

            Be precise about whether the summary at `i` includes `nums[i]` or not. "The biggest *before* `i`" excludes
            it; "the biggest *up to* `i`" includes it. Both are fine, but the combine step changes. Storing the value
            *before* folding in `nums[i]` gives the strict version, which is what the template does.

            ### Saving memory: fold one pass into a variable

            You often don't need both arrays. If the combine step goes left to right, you can keep the left summary in a
            single variable during the second pass and only store the right-hand array. That's what `count_pivots` does.
            And when the question only looks one way (like "the cheapest day before today"), the whole pattern shrinks to
            one variable and one pass, as in the buy-and-sell example.

            ### Why not just look both ways?

            Looking left and right from every index is O(n) per index, O(n²) in total. The two passes reuse work: the
            biggest value before index 7 is the biggest before index 6 plus one more comparison. For `n = 100,000`
            that's about 200,000 steps instead of 10 billion.
            """,
        ]),
        ("template", "The template", [
            """
            Count the **pivots** of an array: elements bigger than everything before them and smaller than everything
            after them. (The first element has nothing before it, and the last has nothing after it, so those tests pass
            automatically.)
            """,
            code(
                "Count pivot elements",
                PIVOTS,
                [
                    ("n", "The length."),
                    ("suffix", "Pass 1, right to left. `smallest` carries the minimum of everything to the right; it starts "
                               "as +∞ because nothing is to the right of the last element.",
                     {"java": "Long sentinels avoid any trouble with values at the edges of the `int` range.",
                      "c": "`LLONG_MAX` from `<limits.h>` plays the part of +∞."}),
                    ("store", "Save the minimum of everything *after* `i`, before `nums[i]` is folded in."),
                    ("fold", "Now include `nums[i]`, so the index to its left sees it."),
                    ("count", "Pass 2 keeps the left-hand summary in a variable instead of an array."),
                    ("scan", "Left to right."),
                    ("test", "Bigger than everything before, smaller than everything after."),
                    ("left", "Fold `nums[i]` into the running maximum for the next index."),
                    ("ret", "The number of pivots.", {"c": "Free the suffix array first."}),
                ],
                PIVOTS_RUN,
                "count_pivots([2, 1, 4, 3, 6, 8, 7, 9]); count_pivots([5, 4, 3]); count_pivots([1, 2, 3])",
            ),
            """
            In a decreasing array nothing qualifies except possibly the ends, and here even they fail (5 isn't smaller than
            what follows; 3 isn't bigger than what came before). In an increasing array every element is a pivot.
            """,
        ]),
        ("trace", "Trace it by hand", [
            walk(pw),
            table(["i", "nums[i]", "biggest before", "smallest after", "pivot?"],
                  *[(str(i), str(DEMO[i]), "–" if PMAX[i] is None else str(PMAX[i]), "–" if SMIN[i] is None else str(SMIN[i]), "yes" if i in PIV else "") for i in range(n)]),
        ]),
        ("examples", "More examples", [
            f"""
            ### The longest climb-then-descent through each point

            For `{MT}`, how long is the longest stretch that goes strictly up to an index and then strictly down after
            it? A left pass records how long the climb ending at each index is; a right pass records how long the descent
            starting at each index is. Their sum minus one (the peak is counted twice) is the stretch through that index,
            as long as there's both a climb and a descent:
            """,
            table(["i", "value", "climb ending here", "descent starting here", "stretch through i"],
                  *[(str(i), str(MT[i]), str(UP[i]), str(DN[i]), str(MOUNT[i]) if MOUNT[i] else "–") for i in range(len(MT))]),
            fig(Bars(MT, st={**{j: "found" for j in range(TOPI - UP[TOPI] + 1, TOPI + DN[TOPI])}, TOPI: "answer"}, label="values"),
                caption=f"The longest one peaks at index {TOPI} and is {TOPM} long."),
            f"""
            ### How lopsided is each index?

            For `{LS}` (total {TOT}), compare the sum to the left of each index with the sum to its right. A running left
            sum plus the total gives the right side without a second array:
            """,
            table(["i", "value", "left sum", "right sum", "difference"], *lr_rows),
        ]),
        ("variations", "Variations", [
            """
            ### Joining runs from both sides

            The longest run of 1s if you're allowed to flip one 0 into a 1. A left pass counts the 1s ending at each
            index; a right pass counts the 1s starting at each index. Flipping a 0 joins the run that ends just before it
            to the run that starts just after it.
            """,
            fig(Row(BITS, st={best_zero[0]: "answer"}, slots=True, label="bits"), Row(L, slots=True, label="1s ending here"), Row(R, slots=True, label="1s starting here"),
                caption=f"Flipping the 0 at index {best_zero[0]} joins {best_zero[1]} ones on its left with {best_zero[2]} on its right: {best_zero[1]} + 1 + {best_zero[2]} = {best_zero[3]}."),
            code(
                "Longest run of 1s after flipping one 0",
                FLIP,
                [
                    ("n", "The length."),
                    ("left", "Left pass: how many 1s end at each index. A 1 extends the run before it; a 0 resets to 0.",
                     {"c": "`calloc` gives zeros, and one spare slot keeps an empty array from becoming a zero-size allocation."}),
                    ("right", "Right pass: how many 1s start at each index, building from the right."),
                    ("noflip", "If there's no 0 to flip, the answer is the longest existing run."),
                    ("zero", "Try flipping each 0."),
                    ("join", "The run ending just before it, the flipped 0 itself, and the run starting just after it. At the "
                             "edges, the missing side counts as 0."),
                    ("ret", "The longest run found.", {"c": "Free both arrays first."}),
                ],
                FLIP_RUN,
                "longest_after_flip([1, 1, 0, 1, 1, 1, 0, 1, 0, 1]); longest_after_flip([1, 1, 1]); longest_after_flip([0, 0])",
            ),
            """
            ### When one side is enough: buy low, sell high

            Buy a share on one day and sell it on a later day; what's the best profit? For each selling day you want the
            cheapest day *before* it, which is a prefix minimum. And since you only ever look left, the prefix array
            collapses into a single variable.
            """,
            walk(prw),
            code(
                "Best single buy and sell",
                PROFIT,
                [
                    ("start", "Day 0 is the cheapest so far. No sale yet, so the best profit is 0 (doing nothing)."),
                    ("loop", "Every later day is a possible selling day."),
                    ("sell", "Selling today after buying at the cheapest earlier day. That's the best sale for today."),
                    ("low", "Then fold today's price into the prefix minimum, for the days after it."),
                    ("ret", "The best profit, or 0 if prices only fell."),
                ],
                PROFIT_RUN,
                "best_profit([8, 3, 6, 2, 7, 5, 4]); best_profit([9, 7, 4, 1])",
            ),
            """
            Notice the order inside the loop: sell first, then update the minimum. Updating first would let you buy and
            sell on the same day, which gives a profit of 0 and does no harm here, but in other problems that ordering
            mistake gives wrong answers.

            ### Products from both sides

            Products work exactly like the maxima above: a running product from the left and one from the right. One of
            the practice problems is built on this, so it's worth thinking through how zeros affect it before you start.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Each pass is O(n), and there are a constant number of them, so the whole thing is O(n) time. Memory is O(n)
            for the stored summary arrays, often reduced to one array (keep the other side in a variable) or even O(1)
            when only one side is needed.

            The direct approach, scanning left and right from every index, is O(n²).
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Look both ways from every index", "O(n²)", "O(1)"],
                ["Prefix array + suffix array", "O(n)", "O(n)"],
                ["Suffix array + running prefix variable", "O(n)", "O(n), one array"],
                ["One running variable (one-sided questions)", "O(n)", "O(1)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `float('inf')` and `float('-inf')` make convenient "nothing yet" values for max and min. For prefix maxima as
            a list, `itertools.accumulate(nums, max)` does a running max in one line.

            ### Java

            Use `Integer.MIN_VALUE` / `MAX_VALUE` (or the `Long` ones) as sentinels, but be careful: if real values can
            equal the sentinel, a strict `<` test can go wrong. Using `long` sentinels with `int` data avoids that.

            ### C++

            `LLONG_MIN` and `LLONG_MAX` from `<climits>`, or `numeric_limits<int>::min()`. `partial_sum` with a custom
            operation gives prefix maxima, but the explicit loop is usually clearer.

            ### C

            `LLONG_MIN` / `LLONG_MAX` from `<limits.h>`. Allocate the summary arrays with `malloc` or `calloc` and free them
            before returning.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Including `nums[i]` in its own summary when the question says "before" or "after". Store first, then fold.
            - Off-by-one at the ends: index 0 has nothing to the left, index `n - 1` nothing to the right. Decide what
              "nothing" means (-∞, +∞, 0, 1, an empty run).
            - Sentinels that real values can equal.
            - Products overflowing, and zeros. One zero makes every product that includes it 0.
            - Updating the running value before using it in a one-sided loop.
            - Thinking prefix max answers range max. It only answers "everything before", not an arbitrary range.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why can prefix and suffix passes use max and min, when prefix sums can't answer range maximums?",
                 "Prefix sums answer middle ranges by subtracting, and you can't subtract a max. Here we only ever need \"everything before i\" and \"everything after i\", which a running max or min gives directly."),
                ("In `count_pivots`, why is `right_min[i]` stored before folding in `nums[i]`?",
                 "So it holds the minimum of the elements strictly after `i`. Folding first would include `nums[i]` itself, and the test `nums[i] < right_min[i]` could never pass."),
                ("bits = [0, 1, 1, 0, 1]. What does `longest_after_flip` return?",
                 "Flipping index 0 gives 0 + 1 + 2 = 3. Flipping index 3 gives 2 + 1 + 1 = 4. The answer is 4."),
                ("Why does `best_profit` only need one variable instead of a prefix array?",
                 "Each day only asks about the cheapest day before it, and we go left to right, so the running minimum at that moment is exactly that value. Nothing later needs older summaries."),
                ("nums = [4, 0, 2]. What are \"biggest before\" and \"smallest after\" for index 1, and is it a pivot?",
                 "Biggest before is 4 and smallest after is 2. 0 isn't bigger than 4, so it's not a pivot."),
            ),
        ]),
    ],
)
