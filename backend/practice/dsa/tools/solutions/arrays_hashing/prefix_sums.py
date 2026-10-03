"""Arrays & Hashing: prefix sums."""
from collections import Counter

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def prefix_of(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p


@problem
def running_balance():
    ch = [5, -2, 10, -7, 3]
    want = prefix_of(ch)[1:]

    w1 = Steps("For each day, add up every change from day 0 to that day.")
    for i in range(len(ch)):
        w1.step(f"Day {i}: " + " + ".join(map(str, ch[:i + 1])) + f" = {want[i]} ({i + 1} additions).", Row(ch, st={k: "active" for k in range(i + 1)}, slots=True), Row(want[:i + 1] + [None] * (len(ch) - i - 1), st={i: "new"}, label="balance", slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Carry the balance forward: today's balance = yesterday's balance + today's change.")
    bal = 0
    for i, c in enumerate(ch):
        bal += c
        w2.step(f"Day {i}: {bal - c} + ({c}) = {bal}.", Row(ch, st={i: "active"}, slots=True), Row(want[:i + 1] + [None] * (len(ch) - i - 1), st={i: "new"}, label="balance", slots=True), Vars(balance=bal))
    w2.steps[-1]["result"] = str(want)

    sol(
        "running-balance",
        summary="""
            Each day's balance is the previous day's balance plus that day's change. Carrying one running total
            through the list gives every answer in a single O(n) pass. This running total is the **prefix sum**, the
            building block for every other problem in this pattern.
        """,
        question=[
            """
            The account starts at 0 and changes by `changes[i]` on day i. Return the balance at the **end** of each day.

            - **End of day:** day 0's balance already includes `changes[0]`. `[5, −2, 10]` → `[5, 3, 13]`.
            - **Withdrawals are negative**, so the balance can go below zero.
            - **Range:** at most 10⁵ days of ±10⁴, so any balance is within ±10⁹, which fits in a 32-bit `int`.
            """
        ],
        think=[
            """
            Take `[5, −2, 10, −7, 3]`. Day 3's balance is 5 − 2 + 10 − 7 = 6. Day 4's is 5 − 2 + 10 − 7 + 3: the same
            sum **plus one more term**. So never re-add from the start; take yesterday's answer and add today's change.
            """,
            fig(Row(ch, label="change", slots=True), Row(want, label="balance", slots=True), caption="balance[i] = balance[i − 1] + change[i]."),
        ],
        approaches=[
            approach(
                "Re-add from the start for each day",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For day i, sum `changes[0 … i]` from scratch."],
                walk=w1,
                build=["For each day i, loop k from 0 to i adding `changes[k]`.", "Store the sum."],
                code={
                    "python": """
                        class Solution:
                            def runningBalance(self, changes: List[int]) -> List[int]:
                                out = []
                                for i in range(len(changes)):  #@each
                                    total = 0  #@sum
                                    for k in range(i + 1):  #@sum
                                        total += changes[k]  #@sum
                                    out.append(total)  #@store
                                return out  #@store
                    """,
                    "java": """
                        class Solution {
                            public int[] runningBalance(int[] changes) {
                                int n = changes.length;
                                int[] out = new int[n];
                                for (int i = 0; i < n; i++) {  //@each
                                    int total = 0;  //@sum
                                    for (int k = 0; k <= i; k++) total += changes[k];  //@sum
                                    out[i] = total;  //@store
                                }
                                return out;  //@store
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> runningBalance(vector<int>& changes) {
                                int n = changes.size();
                                vector<int> out(n);
                                for (int i = 0; i < n; i++) {  //@each
                                    int total = 0;  //@sum
                                    for (int k = 0; k <= i; k++) total += changes[k];  //@sum
                                    out[i] = total;  //@store
                                }
                                return out;  //@store
                            }
                        };
                    """,
                    "c": """
                        int* runningBalance(int* changes, int changesSize, int* returnSize) {
                            int* out = malloc(changesSize * sizeof(int));
                            for (int i = 0; i < changesSize; i++) {  //@each
                                int total = 0;  //@sum
                                for (int k = 0; k <= i; k++) total += changes[k];  //@sum
                                out[i] = total;  //@store
                            }
                            *returnSize = changesSize;  //@store
                            return out;  //@store
                        }
                    """,
                },
                lines=[("each", "One balance per day."), ("sum", "Everything from day 0 through day i."), ("store", "Save it.")],
                complexity=["**Time O(n²):** 1 + 2 + … + n additions. **Space O(1)** besides the output."],
                limits=["Day i's sum contains day i − 1's sum in full. Reuse it."],
                slow=True,
            ),
            approach(
                "Running total",
                "best",
                "O(n)",
                "O(1)",
                idea=["Keep `balance`; for each change, add it and record the new balance."],
                walk=w2,
                build=["`balance = 0`.", "For each change: `balance += change`, append `balance`."],
                code={
                    "python": """
                        class Solution:
                            def runningBalance(self, changes: List[int]) -> List[int]:
                                out, balance = [], 0  #@init
                                for c in changes:  #@loop
                                    balance += c  #@loop
                                    out.append(balance)  #@loop
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] runningBalance(int[] changes) {
                                int[] out = new int[changes.length];  //@init
                                int balance = 0;  //@init
                                for (int i = 0; i < changes.length; i++) {  //@loop
                                    balance += changes[i];  //@loop
                                    out[i] = balance;  //@loop
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> runningBalance(vector<int>& changes) {
                                vector<int> out;  //@init
                                int balance = 0;  //@init
                                for (int c : changes) {  //@loop
                                    balance += c;  //@loop
                                    out.push_back(balance);  //@loop
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* runningBalance(int* changes, int changesSize, int* returnSize) {
                            int* out = malloc(changesSize * sizeof(int));  //@init
                            int balance = 0;  //@init
                            for (int i = 0; i < changesSize; i++) {  //@loop
                                balance += changes[i];  //@loop
                                out[i] = balance;  //@loop
                            }
                            *returnSize = changesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("init", "The account starts at 0."), ("loop", "Apply today's change to yesterday's balance and record it."), ("ret", "Every end-of-day balance.")],
                complexity=["**Time O(n).** **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - A **prefix sum** is a running total: `prefix[i] = prefix[i − 1] + a[i]`.
            - It's the foundation for range sums (`prefix[r + 1] − prefix[l]`), counting subarrays with a target sum,
              and balance-point problems.
            """
        ],
    )


@problem
def balance_point():
    wts = [2, 5, -3, 7, 1, 2, 1]
    total = sum(wts)
    want = next((i for i in range(len(wts)) if sum(wts[:i]) == sum(wts[i + 1:])), -1)
    assert want == 3
    L3, R3 = sum(wts[:3]), sum(wts[4:])

    w1 = Steps("For each index, add up its left side and its right side separately.")
    for i in range(want + 1):
        L, R = sum(wts[:i]), sum(wts[i + 1:])
        w1.step(f"Index {i}: left {L}, right {R}" + (" — equal. Balance point." if L == R else "."), Row(wts, st={**{k: "found" for k in range(i)}, i: ("answer" if L == R else "active"), **{k: "mark" for k in range(i + 1, len(wts))}}, slots=True), Vars(left=L, right=R))
    w1.steps[-1]["result"] = str(want)

    pre = prefix_of(wts)
    w2 = Steps("Build prefix sums once; left of i is prefix[i], right of i is total − prefix[i + 1].")
    w2.step(f"prefix[k] = sum of the first k weights. total = {total}.", Row(wts, slots=True), Row(pre, label="prefix", slots=True))
    for i in range(want + 1):
        L, R = pre[i], total - pre[i + 1]
        w2.step(f"Index {i}: left = prefix[{i}] = {L}; right = {total} − prefix[{i + 1}] = {R}" + (" → balance point." if L == R else "."), Row(pre, st={i: "found", i + 1: "mark"}, label="prefix", slots=True), Vars(left=L, right=R))
    w2.steps[-1]["result"] = str(want)

    w3 = Steps("Know the total; walk once keeping the left sum. right = total − left − weights[i].")
    left = 0
    for i, x in enumerate(wts):
        right = total - left - x
        w3.step(f"Index {i}: left {left}, right = {total} − {left} − {x} = {right}" + (" → equal." if left == right else "; add the weight to left."), Row(wts, st={**{k: "found" for k in range(i)}, i: ("answer" if left == right else "active")}, slots=True), Vars(total=total, left=left, right=right))
        if left == right:
            w3.steps[-1]["result"] = str(i)
            break
        left += x

    sol(
        "balance-point",
        summary="""
            The right side of index i is everything except the left side and the weight at i: `total − left − w[i]`.
            So compute the total once, walk left to right keeping the left sum, and return the first index where the
            two sides match. O(n) time, O(1) space.
        """,
        question=[
            """
            Return the **leftmost** index where the sum of weights strictly to its left equals the sum strictly to its
            right, or −1.

            - **Strictly:** the weight at the index itself is in neither side.
            - **An empty side sums to 0.** In `[2, 1, −1]`, index 0 has left 0 and right 1 + (−1) = 0: it's a balance
              point.
            - **Weights can be negative**, so the sides don't simply grow as you move; you can't stop early or
              binary-search.
            - **Leftmost:** scan from the left and return the first hit.
            - **Range:** sums stay within ±10⁸, inside a 32-bit `int`.
            """
        ],
        think=[
            f"""
            Take `{wts}` (total {total}). At index 3 (weight 7): left = 2 + 5 − 3 = {L3}, right = 1 + 2 + 1 = {R3}.
            Equal, and no earlier index works, so the answer is 3.
            """,
            fig(Row(wts, st={0: "found", 1: "found", 2: "found", 3: "answer", 4: "mark", 5: "mark", 6: "mark"}, slots=True),
                caption=f"Left of index 3 sums to {L3}; right of it sums to {R3}."),
            """
            Recomputing both sides for every index is wasteful. Notice **left + w[i] + right = total**. With the total
            known and the left sum carried along as you walk (add each weight after checking it), the right sum costs
            nothing: `right = total − left − w[i]`.
            """,
        ],
        approaches=[
            approach(
                "Sum both sides for every index",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each index, loop over the weights before it and after it, and compare the sums."],
                walk=w1,
                build=["For each i: `left` = sum of `w[0 … i − 1]`, `right` = sum of `w[i + 1 … n − 1]`.", "Return i if they're equal.", "Return −1 after the loop."],
                code={
                    "python": """
                        class Solution:
                            def balancePoint(self, weights: List[int]) -> int:
                                for i in range(len(weights)):  #@each
                                    if sum(weights[:i]) == sum(weights[i + 1:]):  #@sides
                                        return i  #@sides
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int balancePoint(int[] weights) {
                                int n = weights.length;
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = 0, right = 0;  //@sides
                                    for (int k = 0; k < i; k++) left += weights[k];  //@sides
                                    for (int k = i + 1; k < n; k++) right += weights[k];  //@sides
                                    if (left == right) return i;  //@sides
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int balancePoint(vector<int>& weights) {
                                int n = weights.size();
                                for (int i = 0; i < n; i++) {  //@each
                                    int left = 0, right = 0;  //@sides
                                    for (int k = 0; k < i; k++) left += weights[k];  //@sides
                                    for (int k = i + 1; k < n; k++) right += weights[k];  //@sides
                                    if (left == right) return i;  //@sides
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int balancePoint(int* weights, int weightsSize) {
                            for (int i = 0; i < weightsSize; i++) {  //@each
                                int left = 0, right = 0;  //@sides
                                for (int k = 0; k < i; k++) left += weights[k];  //@sides
                                for (int k = i + 1; k < weightsSize; k++) right += weights[k];  //@sides
                                if (left == right) return i;  //@sides
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("each", "Try indices from the left, so the first hit is the leftmost."), ("sides", "Add up each side from scratch and compare."), ("none", "No index balances.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Each index re-adds almost the same weights as the previous one. Prefix sums make each side an O(1) lookup."],
                slow=True,
            ),
            approach(
                "Prefix sums",
                "better",
                "O(n)",
                "O(n)",
                idea=["`prefix[k]` = sum of the first k weights. Left of i is `prefix[i]`; right of i is `prefix[n] − prefix[i + 1]`."],
                walk=w2,
                build=["Build `prefix` of length n + 1 with `prefix[0] = 0`.", "For each i, compare `prefix[i]` with `prefix[n] − prefix[i + 1]`."],
                code={
                    "python": """
                        class Solution:
                            def balancePoint(self, weights: List[int]) -> int:
                                n = len(weights)
                                prefix = [0] * (n + 1)  #@prefix
                                for i, w in enumerate(weights):  #@prefix
                                    prefix[i + 1] = prefix[i] + w  #@prefix
                                for i in range(n):  #@check
                                    if prefix[i] == prefix[n] - prefix[i + 1]:  #@check
                                        return i  #@check
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int balancePoint(int[] weights) {
                                int n = weights.length;
                                int[] prefix = new int[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + weights[i];  //@prefix
                                for (int i = 0; i < n; i++) {  //@check
                                    if (prefix[i] == prefix[n] - prefix[i + 1]) return i;  //@check
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int balancePoint(vector<int>& weights) {
                                int n = weights.size();
                                vector<int> prefix(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + weights[i];  //@prefix
                                for (int i = 0; i < n; i++) {  //@check
                                    if (prefix[i] == prefix[n] - prefix[i + 1]) return i;  //@check
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int balancePoint(int* weights, int weightsSize) {
                            int n = weightsSize;
                            int* prefix = calloc(n + 1, sizeof(int));  //@prefix
                            for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + weights[i];  //@prefix
                            int found = -1;  //@check
                            for (int i = 0; i < n && found < 0; i++) {  //@check
                                if (prefix[i] == prefix[n] - prefix[i + 1]) found = i;  //@check
                            }
                            free(prefix);  //@none
                            return found;  //@none
                        }
                    """,
                },
                lines=[("prefix", "`prefix[k]` holds the sum of the first k weights; `prefix[0] = 0` is the empty sum."), ("check", "Left of i is the first i weights; right of i is the total minus the first i + 1 weights."), ("none", "No balance point.", {"c": "Free the prefix array first."})],
                complexity=["**Time O(n).** **Space O(n)** for the prefix array."],
                limits=["Only `prefix[i]` (the running left sum) and `prefix[n]` (the total) are ever used, so the array isn't needed."],
            ),
            approach(
                "Total and a running left sum",
                "best",
                "O(n)",
                "O(1)",
                idea=["Compute the total. Walk left to right with `left = 0`: at index i, `right = total − left − w[i]`; if equal, return i; otherwise add `w[i]` to `left`."],
                walk=w3,
                build=["`total = sum(weights)`, `left = 0`.", "For each i: if `left == total − left − weights[i]`, return i.", "Then `left += weights[i]`.", "Return −1."],
                code={
                    "python": """
                        class Solution:
                            def balancePoint(self, weights: List[int]) -> int:
                                total, left = sum(weights), 0  #@init
                                for i, w in enumerate(weights):  #@loop
                                    if left == total - left - w:  #@check
                                        return i  #@check
                                    left += w  #@grow
                                return -1  #@none
                    """,
                    "java": """
                        class Solution {
                            public int balancePoint(int[] weights) {
                                int total = 0, left = 0;  //@init
                                for (int w : weights) total += w;  //@init
                                for (int i = 0; i < weights.length; i++) {  //@loop
                                    if (left == total - left - weights[i]) return i;  //@check
                                    left += weights[i];  //@grow
                                }
                                return -1;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int balancePoint(vector<int>& weights) {
                                int total = accumulate(weights.begin(), weights.end(), 0), left = 0;  //@init
                                for (int i = 0; i < (int) weights.size(); i++) {  //@loop
                                    if (left == total - left - weights[i]) return i;  //@check
                                    left += weights[i];  //@grow
                                }
                                return -1;  //@none
                            }
                        };
                    """,
                    "c": """
                        int balancePoint(int* weights, int weightsSize) {
                            int total = 0, left = 0;  //@init
                            for (int i = 0; i < weightsSize; i++) total += weights[i];  //@init
                            for (int i = 0; i < weightsSize; i++) {  //@loop
                                if (left == total - left - weights[i]) return i;  //@check
                                left += weights[i];  //@grow
                            }
                            return -1;  //@none
                        }
                    """,
                },
                lines=[("init", "The total, and an empty left side."), ("loop", "Left to right, so the first match is the leftmost."), ("check", "Right side = everything that is neither left of i nor at i."), ("grow", "Move past index i: its weight joins the left side for the next index."), ("none", "No balance point.")],
                complexity=["**Time O(n):** two passes. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - `left + w[i] + right = total`: knowing two parts gives the third for free.
            - Sums of contiguous blocks are differences of prefix sums; if only one running prefix is needed, keep a
              variable instead of an array.
            - With negative numbers, sums aren't monotonic, so a linear scan (not binary search) is the right tool.
            """
        ],
    )


@problem
def range_totals():
    sales = [3, -1, 4, 1, 5, 9, -2]
    qs = [[0, 2], [1, 4], [3, 3], [2, 6]]
    pre = prefix_of(sales)
    want = [pre[r + 1] - pre[l] for l, r in qs]

    w1 = Steps("Answer every query by adding up its range directly.")
    for l, r in qs:
        w1.step(f"Query [{l}, {r}]: " + " + ".join(map(str, sales[l:r + 1])) + f" = {sum(sales[l:r + 1])} ({r - l + 1} additions).", Row(sales, st={k: "active" for k in range(l, r + 1)}, slots=True))
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Build prefix sums once; each query is then one subtraction.")
    w2.step("prefix[k] = total of the first k days; prefix[0] = 0.", Row(sales, slots=True), Row(pre, label="prefix", slots=True))
    for l, r in qs:
        w2.step(f"Query [{l}, {r}] = prefix[{r + 1}] − prefix[{l}] = {pre[r + 1]} − {pre[l]} = {pre[r + 1] - pre[l]}.", Row(sales, st={k: "active" for k in range(l, r + 1)}, slots=True), Row(pre, st={l: "mark", r + 1: "answer"}, label="prefix", slots=True))
    w2.steps[-1]["result"] = str(want)

    sol(
        "range-totals",
        summary="""
            With many range-sum questions on the same data, precompute prefix sums once: `prefix[k]` = total of the
            first k days. Then the total from day l to day r is `prefix[r + 1] − prefix[l]`, one subtraction per query.
            O(n + q) instead of O(n · q).
        """,
        question=[
            """
            For each query `[l, r]`, return `sales[l] + … + sales[r]` (both ends included), in query order.

            - **Many queries on unchanged data:** up to 10⁵ queries over up to 10⁵ days. Summing each range directly
              could take 10¹⁰ steps.
            - **Big numbers:** values reach ±10⁹ and a range can contain 10⁵ of them, so totals reach ±10¹⁴. Use
              64-bit integers for the prefix sums (`[10⁹, 10⁹]` already sums past the 32-bit limit).
            - **Single-day queries** like `[3, 3]` are allowed.
            """
        ],
        think=[
            f"""
            Take `sales = {sales}`. The total of days 1 … 4 is −1 + 4 + 1 + 5 = {sum(sales[1:5])}.

            Think of the running total `prefix`: `prefix[k]` is the sum of the first k days. The first 5 days sum to
            `prefix[5] = {pre[5]}`, and the first 1 day to `prefix[1] = {pre[1]}`. Days 1 … 4 are "the first 5 days
            minus the first 1 day": {pre[5]} − {pre[1]} = {pre[5] - pre[1]}.
            """,
            fig(Row(sales, label="sales", st={k: "active" for k in range(1, 5)}, slots=True), Row(pre, label="prefix", st={1: "mark", 5: "answer"}, slots=True),
                caption="Days l … r = prefix[r + 1] − prefix[l]."),
            """
            The extra slot `prefix[0] = 0` (the sum of no days) is what makes ranges starting at day 0 work without a
            special case.
            """,
        ],
        approaches=[
            approach(
                "Add up each range",
                "brute",
                "O(n · q)",
                "O(1)",
                idea=["For each query, loop from l to r adding sales (64-bit)."],
                walk=w1,
                build=["For each query: `total = 0`; add `sales[k]` for k in l … r.", "Append `total`."],
                code={
                    "python": """
                        class Solution:
                            def rangeTotals(self, sales: List[int], queries: List[List[int]]) -> List[int]:
                                return [sum(sales[l:r + 1]) for l, r in queries]  #@sum
                    """,
                    "java": """
                        class Solution {
                            public long[] rangeTotals(int[] sales, int[][] queries) {
                                long[] out = new long[queries.length];
                                for (int q = 0; q < queries.length; q++) {  //@sum
                                    long total = 0;  //@sum
                                    for (int k = queries[q][0]; k <= queries[q][1]; k++) total += sales[k];  //@sum
                                    out[q] = total;  //@sum
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<long long> rangeTotals(vector<int>& sales, vector<vector<int>>& queries) {
                                vector<long long> out;
                                for (auto& q : queries) {  //@sum
                                    long long total = 0;  //@sum
                                    for (int k = q[0]; k <= q[1]; k++) total += sales[k];  //@sum
                                    out.push_back(total);  //@sum
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long* rangeTotals(int* sales, int salesSize, int** queries, int queriesSize, int* queriesColSize, int* returnSize) {
                            long long* out = malloc(queriesSize * sizeof(long long));
                            for (int q = 0; q < queriesSize; q++) {  //@sum
                                long long total = 0;  //@sum
                                for (int k = queries[q][0]; k <= queries[q][1]; k++) total += sales[k];  //@sum
                                out[q] = total;  //@sum
                            }
                            *returnSize = queriesSize;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[("sum", "Each query walks its whole range, adding in 64 bits."), ("ret", "Answers in query order.")],
                complexity=["**Time O(n · q)** in the worst case (every query spans everything). **Space O(1)** besides the output."],
                limits=["Overlapping ranges are added again and again. Precomputing running totals lets every query reuse the same work."],
                slow=True,
            ),
            approach(
                "Prefix sums",
                "best",
                "O(n + q)",
                "O(n)",
                idea=["`prefix[0] = 0`, `prefix[k + 1] = prefix[k] + sales[k]` (64-bit). Each query `[l, r]` is `prefix[r + 1] − prefix[l]`."],
                walk=w2,
                build=["Build `prefix` of length n + 1.", "For each query, append `prefix[r + 1] − prefix[l]`."],
                code={
                    "python": """
                        class Solution:
                            def rangeTotals(self, sales: List[int], queries: List[List[int]]) -> List[int]:
                                prefix = [0]  #@prefix
                                for s in sales:  #@prefix
                                    prefix.append(prefix[-1] + s)  #@prefix
                                return [prefix[r + 1] - prefix[l] for l, r in queries]  #@answer
                    """,
                    "java": """
                        class Solution {
                            public long[] rangeTotals(int[] sales, int[][] queries) {
                                long[] prefix = new long[sales.length + 1];  //@prefix
                                for (int i = 0; i < sales.length; i++) prefix[i + 1] = prefix[i] + sales[i];  //@prefix
                                long[] out = new long[queries.length];  //@answer
                                for (int q = 0; q < queries.length; q++) out[q] = prefix[queries[q][1] + 1] - prefix[queries[q][0]];  //@answer
                                return out;  //@answer
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<long long> rangeTotals(vector<int>& sales, vector<vector<int>>& queries) {
                                vector<long long> prefix(sales.size() + 1, 0);  //@prefix
                                for (size_t i = 0; i < sales.size(); i++) prefix[i + 1] = prefix[i] + sales[i];  //@prefix
                                vector<long long> out;  //@answer
                                for (auto& q : queries) out.push_back(prefix[q[1] + 1] - prefix[q[0]]);  //@answer
                                return out;  //@answer
                            }
                        };
                    """,
                    "c": """
                        long long* rangeTotals(int* sales, int salesSize, int** queries, int queriesSize, int* queriesColSize, int* returnSize) {
                            long long* prefix = malloc((salesSize + 1) * sizeof(long long));  //@prefix
                            prefix[0] = 0;  //@prefix
                            for (int i = 0; i < salesSize; i++) prefix[i + 1] = prefix[i] + sales[i];  //@prefix
                            long long* out = malloc(queriesSize * sizeof(long long));  //@answer
                            for (int q = 0; q < queriesSize; q++) out[q] = prefix[queries[q][1] + 1] - prefix[queries[q][0]];  //@answer
                            free(prefix);  //@answer
                            *returnSize = queriesSize;  //@answer
                            return out;  //@answer
                        }
                    """,
                },
                lines=[("prefix", "Running totals, one longer than the input so `prefix[0]` is the empty sum. 64-bit, because totals reach 10¹⁴."), ("answer", "Days l … r = (first r + 1 days) − (first l days).", {"c": "Free the prefix array; the caller frees `out`."})],
                complexity=["**Time O(n + q):** one pass to build, O(1) per query. **Space O(n)** for the prefix sums."],
            ),
        ],
        takeaways=[
            """
            - **Many range-sum queries on static data → prefix sums.** `sum(l … r) = prefix[r + 1] − prefix[l]`.
            - Give the prefix array a leading 0 to avoid special-casing ranges that start at 0.
            - Watch the width: sums of many 32-bit values need 64 bits.
            """
        ],
    )


@problem
def longest_even_stretch():
    bits = [1, 0, 0, 1, 1, 1, 0, 1, 0]
    n = len(bits)
    best_brute = 0
    for i in range(n):
        bal = 0
        for j in range(i, n):
            bal += 1 if bits[j] else -1
            if bal == 0:
                best_brute = max(best_brute, j - i + 1)
    bal = [0]
    for b in bits:
        bal.append(bal[-1] + (1 if b else -1))

    w1 = Steps("Try every start; extend to every end, tracking (#1s − #0s). A balance of 0 means equal counts.")
    best = 0
    for i in range(n):
        b = 0
        for j in range(i, n):
            b += 1 if bits[j] else -1
            if b == 0 and j - i + 1 > best:
                best = j - i + 1
                w1.step(f"Start {i}, end {j}: ones and zeros match. New best length {best}.", Row(bits, st={k: "answer" for k in range(i, j + 1)}, slots=True), Vars(best=best))
    w1.step(f"All {n * (n + 1) // 2} stretches checked: {best}.", Row(bits, slots=True), result=best)

    w2 = Steps("Running balance (+1 for a 1, −1 for a 0). Two positions with the same balance enclose an even stretch. Remember the first position of each balance.")
    first = {0: -1}
    best = 0
    w2.step("Before the first bit the balance is 0, 'seen at position −1'.", Row(bits, slots=True), Vars(best=0))
    run = 0
    for i, x in enumerate(bits):
        run += 1 if x else -1
        if run in first:
            length = i - first[run]
            note = f"balance {run} was first seen at {first[run]}, so positions {first[run] + 1}…{i} are even (length {length})"
            if length > best:
                best = length
                note += " — new best"
            w2.step(f"Index {i}: {note}.", Row(bits, st={k: "answer" for k in range(first[run] + 1, i + 1)}, slots=True), Vars(balance=run, best=best))
        else:
            first[run] = i
            w2.step(f"Index {i}: balance {run} is new; remember position {i}.", Row(bits, st={i: "active"}, slots=True), Vars(balance=run, best=best))
    w2.steps[-1]["result"] = str(best)
    assert best == best_brute

    sol(
        "longest-even-stretch",
        summary="""
            Count +1 for every 1 and −1 for every 0. A stretch has equal numbers exactly when its sum is 0, i.e. when
            the running balance is the **same** at both of its ends. So for each position, the longest even stretch
            ending there starts right after the **first** position with the same balance. Remember first positions
            and the whole thing is one O(n) pass.
        """,
        question=[
            """
            Find the longest run of consecutive bits containing as many 0s as 1s. Return its length, or 0.

            - **Consecutive:** you can't skip elements.
            - **Equal counts** means the length is always even.
            - **No such run** (e.g. `[1, 1, 1]`) gives 0.
            - **Size:** up to 10⁵ bits, so checking all ~5 × 10⁹ runs is too slow.
            """
        ],
        think=[
            f"""
            Take `bits = {bits}`. Replace each 0 with −1 and keep a running sum (the **balance**):
            """,
            fig(Row(bits, label="bit", slots=True), Row(bal[1:], label="balance after it", slots=True),
                caption="A stretch is even exactly when the balance before it equals the balance at its end."),
            f"""
            A run from index a to index b has equal counts exactly when its +1s and −1s cancel, i.e. when
            `balance after b == balance before a`. So the question becomes: **for each position, where is the earliest
            position with the same balance?** The farther back that is, the longer the stretch.

            The balance before any bit is 0 (think of it as position −1). Storing the first position of each balance
            value as you go answers each lookup in O(1), and since the balance stays within −n … n, a plain array of
            size 2n + 1 can hold the first positions. The longest here is {best}.
            """,
        ],
        approaches=[
            approach(
                "Extend from every start",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start i, extend j to the right keeping `ones − zeros`; whenever it's 0, the stretch i … j is even, so update the best length."],
                walk=w1,
                build=["For each i, set `balance = 0`.", "For each j ≥ i: add +1 or −1; if balance is 0, `best = max(best, j − i + 1)`.", "Return `best`."],
                code={
                    "python": """
                        class Solution:
                            def longestEvenStretch(self, bits: List[int]) -> int:
                                n, best = len(bits), 0
                                for i in range(n):  #@start
                                    balance = 0  #@start
                                    for j in range(i, n):  #@extend
                                        balance += 1 if bits[j] else -1  #@extend
                                        if balance == 0:  #@check
                                            best = max(best, j - i + 1)  #@check
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestEvenStretch(int[] bits) {
                                int n = bits.length, best = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int balance = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        balance += bits[j] == 1 ? 1 : -1;  //@extend
                                        if (balance == 0) best = Math.max(best, j - i + 1);  //@check
                                    }
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestEvenStretch(vector<int>& bits) {
                                int n = bits.size(), best = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int balance = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        balance += bits[j] == 1 ? 1 : -1;  //@extend
                                        if (balance == 0) best = max(best, j - i + 1);  //@check
                                    }
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestEvenStretch(int* bits, int bitsSize) {
                            int best = 0;
                            for (int i = 0; i < bitsSize; i++) {  //@start
                                int balance = 0;  //@start
                                for (int j = i; j < bitsSize; j++) {  //@extend
                                    balance += bits[j] == 1 ? 1 : -1;  //@extend
                                    if (balance == 0 && j - i + 1 > best) best = j - i + 1;  //@check
                                }
                            }
                            return best;  //@ret
                        }
                    """,
                },
                lines=[("start", "Every possible starting position, with an empty balance."), ("extend", "Grow the stretch one bit at a time: +1 for a 1, −1 for a 0."), ("check", "Balance 0 means equal counts; keep the longest."), ("ret", "The longest even stretch, or 0.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Each start re-walks the same bits. The balance of a stretch is the difference of two running balances, so one pass plus a lookup of earlier balances is enough."],
                slow=True,
            ),
            approach(
                "First position of each running balance",
                "best",
                "O(n)",
                "O(n)",
                idea=[
                    """
                    Walk once with `balance` (+1 per 1, −1 per 0). Keep `first[b]`, the earliest position where the balance
                    was b, with `first[0] = −1`. At position i:

                    - if `balance` was seen before, the stretch `first[balance] + 1 … i` is even: length `i − first[balance]`;
                    - otherwise record `first[balance] = i`.

                    Only the **first** occurrence is stored, because the earliest start gives the longest stretch. The
                    balance stays in −n … n, so an array with an offset of n works as the map.
                    """
                ],
                walk=w2,
                build=["Make `first` of size 2n + 1 filled with \"unseen\"; set `first[0 + n] = −1`.", "Walk the bits updating `balance`.", "Seen before: update `best` with `i − first[balance + n]`. New: store `i`.", "Return `best`."],
                code={
                    "python": """
                        class Solution:
                            def longestEvenStretch(self, bits: List[int]) -> int:
                                first = {0: -1}  #@first
                                best = balance = 0
                                for i, b in enumerate(bits):  #@walk
                                    balance += 1 if b else -1  #@walk
                                    if balance in first:  #@seen
                                        best = max(best, i - first[balance])  #@seen
                                    else:  #@new
                                        first[balance] = i  #@new
                                return best  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int longestEvenStretch(int[] bits) {
                                int n = bits.length;
                                int[] first = new int[2 * n + 1];  //@first
                                Arrays.fill(first, -2);  //@first
                                first[n] = -1;  //@first
                                int best = 0, balance = 0;
                                for (int i = 0; i < n; i++) {  //@walk
                                    balance += bits[i] == 1 ? 1 : -1;  //@walk
                                    if (first[balance + n] != -2) best = Math.max(best, i - first[balance + n]);  //@seen
                                    else first[balance + n] = i;  //@new
                                }
                                return best;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int longestEvenStretch(vector<int>& bits) {
                                int n = bits.size();
                                vector<int> first(2 * n + 1, -2);  //@first
                                first[n] = -1;  //@first
                                int best = 0, balance = 0;
                                for (int i = 0; i < n; i++) {  //@walk
                                    balance += bits[i] == 1 ? 1 : -1;  //@walk
                                    if (first[balance + n] != -2) best = max(best, i - first[balance + n]);  //@seen
                                    else first[balance + n] = i;  //@new
                                }
                                return best;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int longestEvenStretch(int* bits, int bitsSize) {
                            int n = bitsSize;
                            int* first = malloc((2 * n + 1) * sizeof(int));  //@first
                            for (int k = 0; k <= 2 * n; k++) first[k] = -2;  //@first
                            first[n] = -1;  //@first
                            int best = 0, balance = 0;
                            for (int i = 0; i < n; i++) {  //@walk
                                balance += bits[i] == 1 ? 1 : -1;  //@walk
                                if (first[balance + n] != -2) {  //@seen
                                    if (i - first[balance + n] > best) best = i - first[balance + n];  //@seen
                                } else {  //@new
                                    first[balance + n] = i;  //@new
                                }
                            }
                            free(first);  //@ret
                            return best;  //@ret
                        }
                    """,
                },
                lines=[
                    ("first", "Earliest position of each balance value. Balance 0 is \"seen\" at position −1, before the first bit.", {"java": "The balance ranges over −n … n, so `balance + n` indexes an array of 2n + 1 slots; −2 marks \"never seen\".", "cpp": "The balance ranges over −n … n, so `balance + n` indexes an array of 2n + 1 slots; −2 marks \"never seen\".", "c": "The balance ranges over −n … n, so `balance + n` indexes an array of 2n + 1 slots; −2 marks \"never seen\"."}),
                    ("walk", "Running balance: +1 for a 1, −1 for a 0."),
                    ("seen", "Same balance as at an earlier position: everything after that position up to here is even. Measuring from the first occurrence gives the longest such stretch ending here."),
                    ("new", "First time at this balance: remember where. Later positions never overwrite it, because later starts only give shorter stretches."),
                    ("ret", "The longest even stretch.", {"c": "Free the array first."}),
                ],
                complexity=["**Time O(n).** **Space O(n)** for the first positions."],
            ),
        ],
        takeaways=[
            """
            - "Equal numbers of two kinds" → map them to +1/−1; equal counts = **sum 0**.
            - Subarray sum 0 ⇔ the running prefix sum repeats. For the **longest**, store each prefix value's
              **first** position.
            - A prefix value with a small known range can index an array (with an offset) instead of a hash map.
            """
        ],
    )


@problem
def subarrays_hitting_target():
    nums, target = [1, 2, 1, 2, 1, 3], 3
    n = len(nums)
    count = sum(1 for i in range(n) for j in range(i, n) if sum(nums[i:j + 1]) == target)
    pre = prefix_of(nums)

    w1 = Steps("Try every start; extend to every end with a running sum; count the sums equal to the target.")
    c = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == target:
                c += 1
                w1.step(f"Stretch {i}…{j} sums to {target}. Count {c}.", Row(nums, st={k: "answer" for k in range(i, j + 1)}, slots=True), Vars(count=c))
    w1.step(f"All stretches checked: {c}.", Row(nums, slots=True), result=c)

    w2 = Steps(f"A stretch ending at i sums to {target} when some earlier prefix equals prefix − {target}. Count earlier prefixes in a hash map.")
    seen = Counter({0: 1})
    p = 0
    tot = 0
    w2.step("The empty prefix (sum 0) has been seen once.", Row(nums, slots=True), Row(["0×1"], label="prefix sum × times seen"), Vars(count=0))
    for i, x in enumerate(nums):
        p += x
        add = seen[p - target]
        tot += add
        w2.step(f"Index {i}: prefix {p}; need earlier prefix {p} − {target} = {p - target}, seen {add} time{'s' if add != 1 else ''} → count {tot}. Then record prefix {p}.", Row(nums, st={i: "active", **{k: "dim" for k in range(i)}}, slots=True), Row([f"{k}×{v}" for k, v in seen.items()], st={list(seen).index(p - target): "answer"} if add else None, label="prefix sum × times seen"), Vars(count=tot))
        seen[p] += 1
    w2.steps[-1]["result"] = str(tot)
    assert tot == count

    sol(
        "subarrays-hitting-target",
        summary="""
            A stretch `a … b` sums to `target` exactly when `prefix[b + 1] − prefix[a] = target`, i.e. when an earlier
            prefix sum equals `currentPrefix − target`. Walk once, keep a hash map counting the prefix sums seen so far,
            and add the count of `prefix − target` at every step. O(n).
        """,
        question=[
            """
            Count the non-empty runs of consecutive elements whose sum is exactly `target`.

            - **Counts runs by position:** two different runs with the same values both count. In `[0, 0]` with
              target 0 there are 3 runs: each single 0 and the pair.
            - **Negative numbers are allowed**, so a run's sum can go up and down. That rules out the sliding-window
              trick (which needs sums that only grow as the window grows).
            - **Size:** up to 10⁵ elements; the count can reach about 5 × 10⁹ (all-zero input, target 0), so return
              it as a 64-bit integer.
            """
        ],
        think=[
            f"""
            Take `nums = {nums}` with target {target}. Write down the prefix sums (the sum of the first k elements):
            """,
            fig(Row(nums, label="nums", slots=True), Row(pre, label="prefix (first k)", slots=True),
                caption=f"Runs summing to {target} are pairs of prefix sums that differ by {target}."),
            f"""
            The run from index a to index b sums to `prefix[b + 1] − prefix[a]`. So when you're at the end of a run
            with running sum `p`, the runs ending here that hit the target are exactly the earlier prefixes equal to
            `p − {target}`, however many of them there are.

            So keep a **count of every prefix sum seen so far** (starting with the empty prefix, 0, seen once). At
            each element: add `count[p − target]` to the answer, then record `p`. Here that totals {count}.
            """,
        ],
        approaches=[
            approach(
                "Every start, running sum",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start i, extend j with a running sum; count every time it equals the target. (Re-adding each run from scratch would be O(n³); carrying the sum while extending saves a factor of n.)"],
                walk=w1,
                build=["For each i: `s = 0`.", "For each j ≥ i: `s += nums[j]`; if `s == target`, count it.", "Return the count (64-bit)."],
                code={
                    "python": """
                        class Solution:
                            def countTargetStretches(self, nums: List[int], target: int) -> int:
                                n, count = len(nums), 0
                                for i in range(n):  #@start
                                    s = 0  #@start
                                    for j in range(i, n):  #@extend
                                        s += nums[j]  #@extend
                                        if s == target:  #@check
                                            count += 1  #@check
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countTargetStretches(int[] nums, int target) {
                                int n = nums.length;
                                long count = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += nums[j];  //@extend
                                        if (s == target) count++;  //@check
                                    }
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countTargetStretches(vector<int>& nums, int target) {
                                int n = nums.size();
                                long long count = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    int s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += nums[j];  //@extend
                                        if (s == target) count++;  //@check
                                    }
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countTargetStretches(int* nums, int numsSize, int target) {
                            long long count = 0;
                            for (int i = 0; i < numsSize; i++) {  //@start
                                int s = 0;  //@start
                                for (int j = i; j < numsSize; j++) {  //@extend
                                    s += nums[j];  //@extend
                                    if (s == target) count++;  //@check
                                }
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("start", "Each possible first element."), ("extend", "Grow the run one element at a time, carrying its sum (within ±10⁸, fine for `int`)."), ("check", "A hit."), ("ret", "The number of runs, 64-bit.")],
                complexity=["**Time O(n²).** **Space O(1).**"],
                limits=["Each run's sum is a difference of two prefix sums. Instead of pairing every start with every end, look up how many earlier prefixes complete the target."],
                slow=True,
            ),
            approach(
                "Prefix sums with a hash map of counts",
                "best",
                "O(n)",
                "O(n)",
                idea=["Keep `seen[s]`, how many prefixes so far had sum s, starting with `seen[0] = 1`. For each element: update the running prefix `p`, add `seen[p − target]` to the answer, then do `seen[p] += 1`."],
                walk=w2,
                build=["`seen = {0: 1}`, `p = 0`, `count = 0`.", "For each x: `p += x`; `count += seen[p − target]`; `seen[p] += 1`.", "Return `count`."],
                code={
                    "python": """
                        from collections import Counter

                        class Solution:
                            def countTargetStretches(self, nums: List[int], target: int) -> int:
                                seen = Counter({0: 1})  #@init
                                count = prefix = 0  #@init
                                for x in nums:  #@loop
                                    prefix += x  #@loop
                                    count += seen[prefix - target]  #@look
                                    seen[prefix] += 1  #@record
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countTargetStretches(int[] nums, int target) {
                                Map<Integer, Integer> seen = new HashMap<>();  //@init
                                seen.put(0, 1);  //@init
                                long count = 0;  //@init
                                int prefix = 0;  //@init
                                for (int x : nums) {  //@loop
                                    prefix += x;  //@loop
                                    count += seen.getOrDefault(prefix - target, 0);  //@look
                                    seen.merge(prefix, 1, Integer::sum);  //@record
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countTargetStretches(vector<int>& nums, int target) {
                                unordered_map<int, int> seen{{0, 1}};  //@init
                                long long count = 0;  //@init
                                int prefix = 0;  //@init
                                for (int x : nums) {  //@loop
                                    prefix += x;  //@loop
                                    auto it = seen.find(prefix - target);  //@look
                                    if (it != seen.end()) count += it->second;  //@look
                                    seen[prefix]++;  //@record
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        // A small hash map from a prefix sum to how many times it occurred.
                        typedef struct { int key; int count; bool used; } Slot;  //@table

                        static Slot* slotFor(Slot* t, unsigned mask, int key) {  //@table
                            unsigned long long h = (unsigned long long) (long long) key * 0x9E3779B97F4A7C15ULL;  //@table
                            unsigned s = (unsigned) (h >> 32) & mask;  //@table
                            while (t[s].used && t[s].key != key) s = (s + 1) & mask;  //@table
                            return &t[s];  //@table
                        }  //@table

                        long long countTargetStretches(int* nums, int numsSize, int target) {
                            unsigned cap = 1;  //@init
                            while (cap < 2u * (numsSize + 1)) cap <<= 1;  //@init
                            Slot* seen = calloc(cap, sizeof(Slot));  //@init
                            Slot* zero = slotFor(seen, cap - 1, 0);  //@init
                            *zero = (Slot) {0, 1, true};  //@init
                            long long count = 0;  //@init
                            int prefix = 0;  //@init
                            for (int i = 0; i < numsSize; i++) {  //@loop
                                prefix += nums[i];  //@loop
                                Slot* want = slotFor(seen, cap - 1, prefix - target);  //@look
                                if (want->used) count += want->count;  //@look
                                Slot* mine = slotFor(seen, cap - 1, prefix);  //@record
                                mine->key = prefix;  //@record
                                mine->used = true;  //@record
                                mine->count++;  //@record
                            }
                            free(seen);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("table", "C has no hash map: `slotFor` hashes a prefix sum to a starting slot and walks forward to its entry or to the empty slot where it would go."),
                    ("init", "The empty prefix (before any element) has sum 0 and has been seen once; that lets runs starting at index 0 be counted.", {"c": "The table holds up to n + 1 distinct prefix sums, so it's sized at least twice that."}),
                    ("loop", "Running prefix sum, including the current element (within ±10⁸)."),
                    ("look", "Every earlier prefix equal to `prefix − target` starts a run that ends here and sums to the target."),
                    ("record", "Only now add the current prefix, so a run can't be empty (it would need `target = 0` with start = end)."),
                    ("ret", "The total count, 64-bit.", {"c": "Free the table first."}),
                ],
                complexity=["**Time O(n)** on average. **Space O(n)** for up to n + 1 distinct prefix sums."],
            ),
        ],
        takeaways=[
            """
            - **Count subarrays with sum = k:** walk with a running prefix sum and a hash map of how often each prefix
              occurred; add `count[prefix − k]` each step. Start with `count[0] = 1`.
            - Look up before recording, so empty subarrays aren't counted.
            - With negatives present, sliding windows don't work; prefix sums do.
            """
        ],
    )


@problem
def sums_in_bounds():
    nums, lower, upper = [3, -2, 4, -5, 1], -1, 2
    n = len(nums)
    want = sum(1 for i in range(n) for j in range(i, n) if lower <= sum(nums[i:j + 1]) <= upper)
    pre = prefix_of(nums)

    w1 = Steps(f"Every start, every end, running sum; count sums within [{lower}, {upper}].")
    c = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if lower <= s <= upper:
                c += 1
                w1.step(f"Run {i}…{j} sums to {s}: inside the bounds. Count {c}.", Row(nums, st={k: "answer" for k in range(i, j + 1)}, slots=True), Vars(count=c))
    w1.step(f"Total {c}.", Row(nums, slots=True), result=c)

    w2 = Steps("Count pairs of prefix sums (i < j) with lower ≤ P[j] − P[i] ≤ upper, using merge sort: count across halves while both halves are sorted.")
    w2.step(f"Prefix sums P = {pre}. Every run is a pair i < j of these, with sum P[j] − P[i].", Row(nums, label="nums", slots=True), Row(pre, label="P", slots=True))
    mid = len(pre) // 2
    L, R = sorted(pre[:mid]), sorted(pre[mid:])
    w2.step(f"Split P into halves; recursively each half counts its own pairs and comes back sorted.", Row(L, label="left half (sorted)"), Row(R, label="right half (sorted)"))
    lo = hi = 0
    cross = 0
    for p in L:
        while lo < len(R) and R[lo] - p < lower:
            lo += 1
        while hi < len(R) and R[hi] - p <= upper:
            hi += 1
        cross += hi - lo
        w2.step(f"Left value {p}: right values in [{p + lower}, {p + upper}] are positions {lo}…{hi - 1} of the right half: {hi - lo} pair{'s' if hi - lo != 1 else ''}. Both pointers only move right.", Row(L, st={L.index(p): "active"}, label="left"), Row(R, st={k: "answer" for k in range(lo, hi)}, ptr={"lo": lo, "hi": hi} if hi < len(R) else {"lo": lo}, label="right"), Vars(cross_pairs=cross))
    w2.step(f"Cross pairs at this level: {cross}. Adding the pairs counted inside each half (recursively) gives {want} in total. Then merge the halves so the level above also sees sorted input.", Row(sorted(pre), label="merged"), result=want)

    sol(
        "sums-in-bounds",
        summary="""
            Every run's sum is `P[j] − P[i]` for prefix sums `P` with i < j, so the task is to count index pairs whose
            prefix difference lies in `[lower, upper]`. Merge sort counts such pairs in O(n log n): when merging two
            sorted halves, the right-half values compatible with each left value form one contiguous window, found
            with two pointers that only move forward.
        """,
        question=[
            """
            Count the non-empty runs of consecutive elements whose sum lies in `[lower, upper]` (inclusive).

            - **Values are huge:** each element can be anywhere in the 32-bit range, and up to 3 × 10⁴ of them add up
              to about ±6.4 × 10¹³. All sums must be 64-bit.
            - **Negatives allowed**, so no sliding window.
            - **n up to 3 × 10⁴:** the O(n²) count (~4.5 × 10⁸ runs) is explicitly too slow; aim for O(n log n).
            """
        ],
        think=[
            f"""
            Take `nums = {nums}`, bounds [{lower}, {upper}]. Prefix sums: `P = {pre}` (P[0] = 0 is the empty prefix).
            Run `i … j − 1` has sum `P[j] − P[i]`. So we're counting pairs `i < j` with
            `{lower} ≤ P[j] − P[i] ≤ {upper}`, i.e. for each `P[i]`, the later `P[j]` in `[P[i] + {lower}, P[i] + {upper}]`.
            """,
            fig(Row(nums, label="nums", slots=True), Row(pre, label="P", slots=True), caption="Each run = a pair of prefix sums, later minus earlier."),
            f"""
            "Count later values within a window" is easy if the later values are **sorted**: the matching ones form a
            contiguous block. But we must also respect "later". Merge sort gives both at once: split P into a left half
            (earlier positions) and a right half (later positions); after recursively sorting each half, every
            left-right pair is automatically "earlier, later", and both halves are sorted, so two forward-moving
            pointers find each left value's window in the right half. The answer here is {want}.
            """,
        ],
        approaches=[
            approach(
                "Every run with a running sum",
                "brute",
                "O(n²)",
                "O(1)",
                idea=["For each start, extend to every end carrying a 64-bit sum; count sums inside the bounds."],
                walk=w1,
                build=["For each i: `s = 0` (64-bit).", "For each j ≥ i: `s += nums[j]`; count it if `lower ≤ s ≤ upper`."],
                code={
                    "python": """
                        class Solution:
                            def countSumsInBounds(self, nums: List[int], lower: int, upper: int) -> int:
                                n, count = len(nums), 0
                                for i in range(n):  #@start
                                    s = 0  #@start
                                    for j in range(i, n):  #@extend
                                        s += nums[j]  #@extend
                                        if lower <= s <= upper:  #@check
                                            count += 1  #@check
                                return count  #@ret
                    """,
                    "java": """
                        class Solution {
                            public long countSumsInBounds(int[] nums, int lower, int upper) {
                                int n = nums.length;
                                long count = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    long s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += nums[j];  //@extend
                                        if (s >= lower && s <= upper) count++;  //@check
                                    }
                                }
                                return count;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            long long countSumsInBounds(vector<int>& nums, int lower, int upper) {
                                int n = nums.size();
                                long long count = 0;
                                for (int i = 0; i < n; i++) {  //@start
                                    long long s = 0;  //@start
                                    for (int j = i; j < n; j++) {  //@extend
                                        s += nums[j];  //@extend
                                        if (s >= lower && s <= upper) count++;  //@check
                                    }
                                }
                                return count;  //@ret
                            }
                        };
                    """,
                    "c": """
                        long long countSumsInBounds(int* nums, int numsSize, int lower, int upper) {
                            long long count = 0;
                            for (int i = 0; i < numsSize; i++) {  //@start
                                long long s = 0;  //@start
                                for (int j = i; j < numsSize; j++) {  //@extend
                                    s += nums[j];  //@extend
                                    if (s >= lower && s <= upper) count++;  //@check
                                }
                            }
                            return count;  //@ret
                        }
                    """,
                },
                lines=[("start", "Each start, with a 64-bit sum (32-bit values add up fast)."), ("extend", "Extend the run one element."), ("check", "Inside the bounds?"), ("ret", "Total runs.")],
                complexity=["**Time O(n²):** about 4.5 × 10⁸ runs at the limit. **Space O(1).**"],
                limits=["It enumerates every pair explicitly. Counting pairs within a range is a job for sorted data: merge sort can count all valid pairs in O(n log n) without listing them."],
                slow=True,
            ),
            approach(
                "Merge sort over prefix sums",
                "best",
                "O(n log n)",
                "O(n)",
                idea=[
                    """
                    Build the n + 1 prefix sums. `sortCount(lo, hi)` sorts `P[lo … hi)` and returns how many pairs inside it
                    have a difference in bounds:

                    1. Split at `mid`; recurse on both halves (each returns its internal count and comes back sorted).
                    2. **Cross pairs:** for each left value `p` (in increasing order), the right values in
                       `[p + lower, p + upper]` form a contiguous block `[a, b)`. As `p` grows, both ends of the block only
                       move right, so two pointers scan the right half once in total.
                    3. Merge the halves so the caller gets sorted data.
                    """
                ],
                walk=w2,
                build=["Prefix sums `P[0 … n]` in 64 bits.", "Recursive `sortCount(lo, hi)`; base case of 0 or 1 values counts nothing.", "Count cross pairs with two forward pointers `a` (first ≥ p + lower) and `b` (first > p + upper).", "Merge into a temporary buffer and copy back. Return the sum of the three counts."],
                code={
                    "python": """
                        class Solution:
                            def countSumsInBounds(self, nums: List[int], lower: int, upper: int) -> int:
                                prefix = [0]  #@prefix
                                for x in nums:  #@prefix
                                    prefix.append(prefix[-1] + x)  #@prefix

                                def sort_count(a):  #@split
                                    if len(a) <= 1:  #@split
                                        return a, 0  #@split
                                    mid = len(a) // 2  #@split
                                    left, c1 = sort_count(a[:mid])  #@split
                                    right, c2 = sort_count(a[mid:])  #@split
                                    count, lo, hi = c1 + c2, 0, 0  #@cross
                                    for p in left:  #@cross
                                        while lo < len(right) and right[lo] - p < lower:  #@cross
                                            lo += 1  #@cross
                                        while hi < len(right) and right[hi] - p <= upper:  #@cross
                                            hi += 1  #@cross
                                        count += hi - lo  #@cross
                                    merged, i, j = [], 0, 0  #@merge
                                    while i < len(left) and j < len(right):  #@merge
                                        if left[i] <= right[j]:  #@merge
                                            merged.append(left[i]); i += 1  #@merge
                                        else:  #@merge
                                            merged.append(right[j]); j += 1  #@merge
                                    merged += left[i:] + right[j:]  #@merge
                                    return merged, count  #@merge

                                return sort_count(prefix)[1]  #@ret
                    """,
                    "java": """
                        class Solution {
                            private int lower, upper;

                            public long countSumsInBounds(int[] nums, int lower, int upper) {
                                this.lower = lower;
                                this.upper = upper;
                                int n = nums.length;
                                long[] p = new long[n + 1];  //@prefix
                                for (int i = 0; i < n; i++) p[i + 1] = p[i] + nums[i];  //@prefix
                                return sortCount(p, new long[n + 1], 0, n + 1);  //@ret
                            }

                            private long sortCount(long[] p, long[] tmp, int lo, int hi) {  //@split
                                if (hi - lo <= 1) return 0;  //@split
                                int mid = (lo + hi) >>> 1;  //@split
                                long count = sortCount(p, tmp, lo, mid) + sortCount(p, tmp, mid, hi);  //@split
                                int a = mid, b = mid;  //@cross
                                for (int i = lo; i < mid; i++) {  //@cross
                                    while (a < hi && p[a] - p[i] < lower) a++;  //@cross
                                    while (b < hi && p[b] - p[i] <= upper) b++;  //@cross
                                    count += b - a;  //@cross
                                }
                                int i = lo, j = mid, k = lo;  //@merge
                                while (i < mid && j < hi) tmp[k++] = p[i] <= p[j] ? p[i++] : p[j++];  //@merge
                                while (i < mid) tmp[k++] = p[i++];  //@merge
                                while (j < hi) tmp[k++] = p[j++];  //@merge
                                System.arraycopy(tmp, lo, p, lo, hi - lo);  //@merge
                                return count;  //@merge
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                            long long lower, upper;
                            vector<long long> p, tmp;

                            long long sortCount(int lo, int hi) {  //@split
                                if (hi - lo <= 1) return 0;  //@split
                                int mid = lo + (hi - lo) / 2;  //@split
                                long long count = sortCount(lo, mid) + sortCount(mid, hi);  //@split
                                int a = mid, b = mid;  //@cross
                                for (int i = lo; i < mid; i++) {  //@cross
                                    while (a < hi && p[a] - p[i] < lower) a++;  //@cross
                                    while (b < hi && p[b] - p[i] <= upper) b++;  //@cross
                                    count += b - a;  //@cross
                                }
                                merge(p.begin() + lo, p.begin() + mid, p.begin() + mid, p.begin() + hi, tmp.begin() + lo);  //@merge
                                copy(tmp.begin() + lo, tmp.begin() + hi, p.begin() + lo);  //@merge
                                return count;  //@merge
                            }

                        public:
                            long long countSumsInBounds(vector<int>& nums, int lower, int upper) {
                                this->lower = lower;
                                this->upper = upper;
                                int n = nums.size();
                                p.assign(n + 1, 0);  //@prefix
                                for (int i = 0; i < n; i++) p[i + 1] = p[i] + nums[i];  //@prefix
                                tmp.assign(n + 1, 0);  //@prefix
                                return sortCount(0, n + 1);  //@ret
                            }
                        };
                    """,
                    "c": """
                        static long long gLower, gUpper;

                        static long long sortCount(long long* p, long long* tmp, int lo, int hi) {  //@split
                            if (hi - lo <= 1) return 0;  //@split
                            int mid = lo + (hi - lo) / 2;  //@split
                            long long count = sortCount(p, tmp, lo, mid) + sortCount(p, tmp, mid, hi);  //@split
                            int a = mid, b = mid;  //@cross
                            for (int i = lo; i < mid; i++) {  //@cross
                                while (a < hi && p[a] - p[i] < gLower) a++;  //@cross
                                while (b < hi && p[b] - p[i] <= gUpper) b++;  //@cross
                                count += b - a;  //@cross
                            }
                            int i = lo, j = mid, k = lo;  //@merge
                            while (i < mid && j < hi) tmp[k++] = p[i] <= p[j] ? p[i++] : p[j++];  //@merge
                            while (i < mid) tmp[k++] = p[i++];  //@merge
                            while (j < hi) tmp[k++] = p[j++];  //@merge
                            memcpy(p + lo, tmp + lo, (hi - lo) * sizeof(long long));  //@merge
                            return count;  //@merge
                        }

                        long long countSumsInBounds(int* nums, int numsSize, int lower, int upper) {
                            gLower = lower;
                            gUpper = upper;
                            long long* p = malloc((numsSize + 1) * sizeof(long long));  //@prefix
                            long long* tmp = malloc((numsSize + 1) * sizeof(long long));  //@prefix
                            p[0] = 0;  //@prefix
                            for (int i = 0; i < numsSize; i++) p[i + 1] = p[i] + nums[i];  //@prefix
                            long long count = sortCount(p, tmp, 0, numsSize + 1);  //@ret
                            free(p);  //@ret
                            free(tmp);  //@ret
                            return count;  //@ret
                        }
                    """,
                },
                lines=[
                    ("prefix", "n + 1 prefix sums in 64 bits, including the empty prefix 0. Every run is a pair of them."),
                    ("split", "Split the range in half; each recursive call counts the pairs fully inside its half and leaves that half sorted."),
                    ("cross", "Pairs with the earlier prefix in the left half and the later one in the right half. For each left value p (increasing), `a` stops at the first right value ≥ p + lower and `b` at the first > p + upper; the `b − a` values between them complete in-bounds runs. Since p only grows, `a` and `b` never move back."),
                    ("merge", "Merge the two sorted halves (via a buffer) so the level above gets sorted input.", {"cpp": "`std::merge` writes the merged range into the buffer, then it's copied back."}),
                    ("ret", "The count for the whole array.", {"c": "Free both buffers."}),
                ],
                complexity=["**Time O(n log n):** log n levels, each doing O(n) pointer moves and merging. **Space O(n)** for the buffer (plus O(log n) recursion)."],
            ),
        ],
        takeaways=[
            """
            - Subarray sums = **differences of prefix sums**; "count subarrays with a property of the sum" becomes "count
              pairs i < j of prefix sums".
            - **Merge sort counts pairs:** while merging, the left half is all earlier and the right half all later, and
              both are sorted, so ranges can be counted with forward-only pointers. (Counting inversions is the classic
              example.)
            - A Fenwick tree over compressed prefix values is another O(n log n) route.
            """
        ],
    )
